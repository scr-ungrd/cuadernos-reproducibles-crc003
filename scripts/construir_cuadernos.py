#!/usr/bin/env python3
"""Genera los tres cuadernos (notebooks/01-03) de la versión 2 sin salidas.

Uso:  python scripts/construir_cuadernos.py
Los cuadernos se ejecutan después (CI o `jupyter nbconvert --execute --inplace`).
Se genera desde un script para que el diff de cada cambio sea legible.
"""
from pathlib import Path
import nbformat as nbf

RAIZ = Path(__file__).resolve().parent.parent
COLAB = "https://colab.research.google.com/github/scr-ungrd/cuadernos-reproducibles-crc003/blob/main/notebooks/"


def md(s):
    return nbf.v4.new_markdown_cell(s.strip("\n"))


def code(s):
    return nbf.v4.new_code_cell(s.strip("\n"))


def guardar(nombre, celdas):
    nb = nbf.v4.new_notebook()
    nb.cells = celdas
    nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python"}}
    nbf.write(nb, RAIZ / "notebooks" / nombre)
    print("escrito", nombre, len(celdas), "celdas")


# --------------------------------------------------------------------------
# Bloque común: rutas y acceso a datos (idéntico en los tres cuadernos)
# --------------------------------------------------------------------------
COMUN = '''
import sys, subprocess, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

IN_COLAB = 'google.colab' in sys.modules
if IN_COLAB:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'rasterio', 'pyproj'], check=True)
import rasterio
from rasterio.crs import CRS
from pyproj import Transformer

WORK = Path('/content') if IN_COLAB else Path('.')
OUT = WORK / 'output'
OUT.mkdir(exist_ok=True)
RAW = 'https://raw.githubusercontent.com/scr-ungrd/cuadernos-reproducibles-crc003/main/data/'

def datos(nombre):
    """Ruta de un archivo de data/: local (../data) o descargado del repositorio (Colab)."""
    for base in (Path('../data'), Path('data'), WORK / 'data'):
        if (base / nombre).exists():
            return base / nombre
    import requests
    destino = WORK / 'data'
    destino.mkdir(exist_ok=True)
    r = requests.get(RAW + nombre, timeout=120)
    r.raise_for_status()
    (destino / nombre).write_bytes(r.content)
    return destino / nombre

# Epicentro del 12-dic-1979 (1,598° N, 79,359° O, según el artículo; por verificar con la fuente primaria)
EPI = (-79.359, 1.598)                       # (lon, lat)
CRS_UTM = CRS.from_epsg(32617)               # UTM 17N, meridiano central 81° O (error de escala < 0,2 % en el dominio)
TR = Transformer.from_crs(4326, 32617, always_xy=True)
G = 9.81

def ejes_lonlat(ax, paso=1):
    """Marcas de longitud y latitud sobre un mapa en coordenadas UTM (km); oeste a la izquierda, norte arriba."""
    lons = np.arange(-81, -76.5, paso); lats = np.arange(0, 4.5, paso)
    xl, yl = ax.get_xlim(), ax.get_ylim()
    ax.set_xticks([TR.transform(l, 2.0)[0] / 1e3 for l in lons]); ax.set_xticklabels([f'{abs(l):g}°O' for l in lons])
    ax.set_yticks([TR.transform(-79.0, l)[1] / 1e3 for l in lats]); ax.set_yticklabels([f'{l:g}°N' for l in lats])
    ax.set_xlim(xl); ax.set_ylim(yl)
    ax.set_xlabel('Longitud'); ax.set_ylabel('Latitud')
'''

# --------------------------------------------------------------------------
# Cuaderno 1
# --------------------------------------------------------------------------
nb1 = [
    md(f"""
# Cuaderno 1: Batimetría y topografía

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}01-bathymetry.ipynb)

Prepara el modelo digital de elevación (DEM) del dominio de simulación del tsunami de Tumaco de 1979:
**0,2° S–4,2° N y 81,2°–76,9° O** (unos 480 × 480 km), que cubre Tumaco, Bocagrande, Esmeraldas (Ecuador) y Buenaventura
y deja la fuente sísmica lejos de los bordes. **Runtime:** CPU, menos de 1 minuto.

**Fuente de los datos.** El DEM sale del servicio de mosaico global de NOAA/NCEI
(`DEM_mosaics/DEM_global_mosaic`), pedido a 15 arco-segundos (~460 m). Es un *mosaico* de modelos de distinta resolución y
procedencia, por lo que **no es GEBCO ni ETOPO 2022 puros** (la versión 1 de este cuaderno los nombraba; el enlace de
descarga de GEBCO que usaba ya no responde). Una copia del recorte está en `data/dem_tumaco_noaa_15s.tif` para que el cuaderno no
dependa del servidor.
"""),
    code(COMUN),
    md("## 1. Recorte geográfico del DEM"),
    code('''
BBOX = (-81.2, -0.2, -76.9, 4.2)     # lon_min, lat_min, lon_max, lat_max
NC, NR = 1032, 1056                  # 15 arco-segundos

def dem_geografico():
    """Usa la copia del repositorio; si no está, pide el recorte al servicio NOAA/NCEI."""
    try:
        return datos('dem_tumaco_noaa_15s.tif')
    except Exception as e:
        print('Copia no disponible (', type(e).__name__, '); descargando de NOAA/NCEI...')
        import requests
        url = ('https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/DEM_global_mosaic/ImageServer/exportImage'
               f'?bbox={BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}&bboxSR=4326&size={NC},{NR}&imageSR=4326'
               '&format=tiff&pixelType=F32&f=image')
        r = requests.get(url, timeout=180); r.raise_for_status()
        destino = WORK / 'data'; destino.mkdir(exist_ok=True)
        (destino / 'dem_tumaco_noaa_15s.tif').write_bytes(r.content)
        return destino / 'dem_tumaco_noaa_15s.tif'

ruta_geo = dem_geografico()
with rasterio.open(ruta_geo) as s:
    z = s.read(1); b = s.bounds
    # Comprobaciones: un DEM vacío, sintético o mal recortado no debe pasar en silencio
    assert np.isfinite(z).all(), 'DEM con valores no finitos'
    assert z.min() < -4000 and z.max() > 3000, 'rango de elevaciones inesperado'
    assert abs(b.left - BBOX[0]) < 0.01 and abs(b.top - BBOX[3]) < 0.01, 'recorte distinto al esperado'
    print(f'DEM geográfico {z.shape[1]}×{z.shape[0]} | elev. {z.min():.0f} a {z.max():.0f} m | océano {100*(z<0).mean():.0f} % del área')
    for nombre, (lon, lat) in {'Tumaco': (-78.76, 1.82), 'Epicentro': EPI}.items():
        r_, c_ = s.index(lon, lat); print(f'  {nombre}: {z[r_, c_]:.0f} m')
'''),
    md("""
## 2. Reproyección a UTM 17N (450 m)

La malla es regular, con el **norte arriba y el oeste a la izquierda** (fila 0 = norte, columna 0 = oeste). La versión 1 invertía el
eje X al guardar el DEM y eso espejaba los mapas; aquí no se invierte nada.
"""),
    code('''
from rasterio.warp import calculate_default_transform, reproject, Resampling

def a_utm(ruta, dx=450.0):
    with rasterio.open(ruta) as src:
        tf, w, h = calculate_default_transform(src.crs, CRS_UTM, src.width, src.height, *src.bounds, resolution=dx)
        arr = np.full((h, w), np.nan, 'float32')
        reproject(rasterio.band(src, 1), arr, src_transform=src.transform, src_crs=src.crs,
                  dst_transform=tf, dst_crs=CRS_UTM, resampling=Resampling.bilinear, dst_nodata=np.nan)
    return arr, tf

dem, tf = a_utm(ruta_geo, 450.0)
print(f'UTM 17N: {dem.shape[1]}×{dem.shape[0]} celdas de 450 m | {dem.shape[1]*0.45:.0f} × {dem.shape[0]*0.45:.0f} km')
print(f'Celdas sin dato (bordes de la reproyección): {np.isnan(dem).sum()} ({100*np.isnan(dem).mean():.2f} %); se tratan como tierra')

with rasterio.open(OUT / 'dem_utm17_450m.tif', 'w', driver='GTiff', height=dem.shape[0], width=dem.shape[1], count=1,
                   dtype='float32', crs=CRS_UTM, transform=tf, nodata=np.nan) as dst:
    dst.write(dem, 1)

# Orientación: el punto de mayor profundidad debe estar al oeste de la costa, no al este
ny, nx = dem.shape
x_oc = np.nanmean(np.where(dem < -3000)[1]); x_tierra = np.nanmean(np.where(dem > 500)[1])
assert x_oc < x_tierra, 'orientación invertida: el océano profundo debe quedar a la izquierda (oeste)'
print('✓ Orientación correcta: océano profundo al oeste, relieve al este')
'''),
    md("## 3. Vista general con las estaciones de 1979 y el epicentro"),
    code('''
obs = pd.read_csv(datos('observaciones_1979.csv'))
ext = [tf.c / 1e3, (tf.c + tf.a * nx) / 1e3, (tf.f + tf.e * ny) / 1e3, tf.f / 1e3]
fig, ax = plt.subplots(figsize=(8.5, 8))
ax.imshow(np.where(dem < 0, dem, np.nan), cmap='Blues_r', vmin=-5000, vmax=0, extent=ext)
ax.imshow(np.where(dem >= 0, dem, np.nan), cmap='Greys', vmin=0, vmax=3500, extent=ext, alpha=.8)
xc = np.linspace(ext[0], ext[1], nx); yc = np.linspace(ext[3], ext[2], ny)
ax.contour(xc, yc, np.nan_to_num(dem), levels=[0], colors='k', linewidths=.5)
for _, r in obs.iterrows():
    x, y = TR.transform(r.lon, r.lat)
    ax.plot(x / 1e3, y / 1e3, 'o', c='#c0392b', ms=5)
    ax.annotate(r.estacion, (x / 1e3, y / 1e3), textcoords='offset points', xytext=(5, 4), fontsize=7)
ex, ey = TR.transform(*EPI)
ax.plot(ex / 1e3, ey / 1e3, '*', c='red', mec='k', ms=18, label='Epicentro 1979')
ax.legend(loc='upper left'); ejes_lonlat(ax)
ax.set_title('Dominio de simulación: batimetría y topografía (NOAA/NCEI, 15″)')
plt.tight_layout(); plt.savefig(WORK / 'dem_overview.png', dpi=130); plt.show()
print('Estaciones fuera del dominio:', [r.estacion for _, r in obs.iterrows()
      if not (BBOX[0] <= r.lon <= BBOX[2] and BBOX[1] <= r.lat <= BBOX[3])])
'''),
]

# --------------------------------------------------------------------------
# Cuaderno 2
# --------------------------------------------------------------------------
nb2 = [
    md(f"""
# Cuaderno 2: Simulación del tsunami de 1979

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}02-simulation.ipynb)

Propagación del tsunami del 12 de diciembre de 1979 con **ecuaciones de aguas someras lineales (LSWE)** en **NumPy puro**. Cambios respecto a la
versión 1:

| | Versión 1 | Versión 2 |
|---|---|---|
| Fuente | Onda en N con amplitud de calibración de 8 m (pico inicial de 16 m) | Deformación del fondo de una falla rectangular con el modelo de Okada (1985); sin parámetro de calibración |
| Esquema | Lax-Friedrichs (primer orden, muy difusivo) | Malla escalonada *forward-backward* (sin difusión numérica) |
| Posición de la fuente | Franja N–S ligada a la celda de costa más oriental | Falla ligada al epicentro |
| Fronteras | Reflejantes (Neumann) | Abiertas (radiación) |
| Dominio | 0,5–3,5° N, 79,5–77° O | 0,2° S–4,2° N, 81,2–76,9° O |

**Runtime:** CPU, unos 2 minutos. **Se ejecuta el cuaderno 1 antes** (o se descarga el DEM automáticamente).
"""),
    code(COMUN),
    md("""
## 1. Escenario sísmico

La magnitud (**Mw 8,3**) viene de la literatura: Yoshimoto et al. (2017), citado por Escobar et al. (2020) y Ávila-Guzmán et al. (2026);
la versión 1 usaba 8,2. Esos trabajos tomaron la distribución de deslizamiento de Poveda y Pulido (2019). **No se tienen a la mano las dimensiones y la
geometría de ese modelo**, así que aquí se usa un **escenario sintético de deslizamiento uniforme sobre una falla rectangular**
cuyos parámetros geométricos son **supuestos, por verificar**:

| Parámetro | Valor | Estado |
|---|---|---|
| Mw | 8,3 | Literatura (Yoshimoto et al., 2017) |
| Epicentro | 1,598° N, 79,359° O | Según el artículo; por verificar |
| Longitud × ancho | 200 × 80 km | Supuesto (orden de magnitud para Mw 8,3) |
| Rumbo / buzamiento / ángulo de desplazamiento | 30° / 15° / 90° (inverso) | Supuesto (margen colombo-ecuatoriano con rumbo NNE) |
| Profundidad del borde superior | 12 km (el borde inferior queda a ~33 km) | Supuesto; el hipocentro de 33 km se ubica en el centro del borde inferior |
| Módulo de rigidez, Poisson | 30 GPa, 0,25 | Valores típicos |
| Deslizamiento | M₀ / (μ·L·W) ≈ 7,4 m | Derivado |

La deformación vertical del fondo se traslada tal cual a la superficie del agua (condición inicial instantánea, sin filtro por la columna de agua
ni componente horizontal sobre el talud).
"""),
    code('''
ESC = dict(Mw=8.3, strike=30., dip=15., rake=90., L=200e3, W=80e3, top_depth=12e3, mu=3e10, nu=0.25)
DX, DT, T_END, OUT_EVERY = 450., 1.0, 3600., 120.   # m, s, s, s (61 min simulados, 31 instantáneas)

def okada_uz(x, y, d, L, W, strike_deg, dip_deg, rake_deg, slip, nu=0.25):
    """Desplazamiento vertical en superficie (m, positivo hacia arriba) de una falla rectangular en un semiespacio elástico
    (Okada, 1985). (x, y) = (este, norte) en m respecto a la proyección en superficie del punto medio del borde INFERIOR de la falla;
    d = profundidad del borde superior (m); L = longitud a lo largo del rumbo; W = ancho a lo largo del buzamiento (m)."""
    k = 1.0 - 2.0 * nu                                  # mu / (lambda + mu)
    st, dl, rk = np.radians(strike_deg), np.radians(dip_deg), np.radians(rake_deg)
    sd, cd = np.sin(dl), np.cos(dl)
    X = x * np.sin(st) + y * np.cos(st)                 # a lo largo del rumbo
    Y = -x * np.cos(st) + y * np.sin(st)                # perpendicular, hacia el buzamiento
    d_inf = d + W * sd
    U1, U2 = slip * np.cos(rk), slip * np.sin(rk)
    p = Y * cd + d_inf * sd
    q = Y * sd - d_inf * cd
    def f(xi, eta):
        R = np.sqrt(xi**2 + eta**2 + q**2); Xq = np.sqrt(xi**2 + q**2)
        dt = eta * sd - q * cd
        with np.errstate(all='ignore'):
            I4 = k * (np.log(R + dt) - sd * np.log(R + eta)) / cd
            I5 = np.where(np.abs(xi) < 1e-9, 0.0,
                          k * 2.0 / cd * np.arctan((eta * (Xq + q * cd) + Xq * (R + Xq) * sd) / (xi * (R + Xq) * cd)))
            ss = -(dt * q / (R * (R + eta)) + q * sd / (R + eta) + I4 * sd)
            ds = -(dt * q / (R * (R + xi)) + sd * np.arctan(xi * eta / (q * R)) - I5 * sd * cd)
        return (U1 * ss + U2 * ds) / (2 * np.pi)
    xs = X + L / 2.0
    return f(xs, p) - f(xs, p - W) - f(xs - L, p) + f(xs - L, p - W)

# --- Verificación contra una implementación independiente (pyrocko, okada_ext; mismos parámetros) ---
_xs = np.array([-40e3, -10e3, 0, 20e3, 60e3, 100e3]); _ys = np.array([30e3, -20e3, 0, 40e3, -50e3, 10e3])
_ref = {(30., 15., 90., 10e3): [1.8464649, -0.704549, -0.6910644, -0.384285, -0.0361739, -0.0202239],
        (200., 25., 90., 5e3): [-0.1313679, -0.2849464, -0.1790315, 0.0740588, 0.0022756, 0.0002734],
        (75., 10., 110., 15e3): [1.3561887, -0.6388427, -0.8413563, 0.7408425, -0.0610156, -0.0539045]}
for (st_, dp_, rk_, d_), ref in _ref.items():
    err = np.abs(okada_uz(_xs, _ys, d_, 100e3, 50e3, st_, dp_, rk_, 5.0) - np.array(ref)).max()
    assert err < 1e-5, f'Okada no coincide con la referencia: {err}'
print('✓ Okada (1985) reproduce los valores de referencia de pyrocko (error máx. < 1e-5 m, 3 geometrías)')
'''),
    code('''
from rasterio.warp import calculate_default_transform, reproject, Resampling

def a_utm(ruta, dx):
    with rasterio.open(ruta) as src:
        tf, w, h = calculate_default_transform(src.crs, CRS_UTM, src.width, src.height, *src.bounds, resolution=dx)
        arr = np.full((h, w), np.nan, 'float32')
        reproject(rasterio.band(src, 1), arr, src_transform=src.transform, src_crs=src.crs,
                  dst_transform=tf, dst_crs=CRS_UTM, resampling=Resampling.bilinear, dst_nodata=np.nan)
    return arr, tf

def cargar_H(dx):
    """Profundidad en reposo H (m; 0 en tierra y en celdas sin dato) y transformación afín."""
    ruta = OUT / 'dem_utm17_450m.tif'
    if dx == 450. and ruta.exists():
        with rasterio.open(ruta) as s: dem, tf = s.read(1), s.transform
    else:
        try:
            geo = datos('dem_tumaco_noaa_15s.tif')
        except Exception as e:
            raise RuntimeError('Ejecute primero el cuaderno 1 (no se encontró el DEM).') from e
        dem, tf = a_utm(geo, dx)
    return np.where(np.isnan(dem), 0.0, np.maximum(-dem, 0.0)), tf

def eta_inicial(tf, shape, esc):
    """Deformación vertical del fondo (m) en cada celda para el escenario `esc`; devuelve (eta0, deslizamiento)."""
    M0 = 10 ** (1.5 * esc['Mw'] + 9.1)
    slip = M0 / (esc['mu'] * esc['L'] * esc['W'])
    ex, ey = TR.transform(*EPI)
    # El epicentro es la proyección del punto medio del borde inferior (hipocentro supuesto)
    ny, nx = shape
    X, Y = np.meshgrid(tf.c + tf.a * (np.arange(nx) + .5) - ex, tf.f + tf.e * (np.arange(ny) + .5) - ey)
    uz = okada_uz(X, Y, esc['top_depth'], esc['L'], esc['W'], esc['strike'], esc['dip'], esc['rake'], slip, esc['nu'])
    return uz.astype('float32'), slip

H, tf = cargar_H(DX)
ny, nx = H.shape
eta0, slip = eta_inicial(tf, H.shape, ESC)
eta0 = np.where(H > 0, eta0, 0.0)          # la deformación solo mueve agua donde hay océano
print(f'Malla {nx}×{ny} de {DX:.0f} m | deslizamiento {slip:.1f} m | η₀: máx. {eta0.max():.2f} m, mín. {eta0.min():.2f} m')
'''),
    code('''
def contorno_falla(esc, L=None, W=None):
    ex, ey = TR.transform(*EPI)
    st = np.radians(esc['strike']); up = np.radians(esc['strike'] + 270.)
    sh = esc['W'] * np.cos(np.radians(esc['dip']))
    return np.array([(ex + a * esc['L'] / 2 * np.sin(st) + b * sh * np.sin(up),
                      ey + a * esc['L'] / 2 * np.cos(st) + b * sh * np.cos(up)) for a, b in [(-1, 0), (1, 0), (1, 1), (-1, 1), (-1, 0)]]) / 1e3

ext = [tf.c / 1e3, (tf.c + tf.a * nx) / 1e3, (tf.f + tf.e * ny) / 1e3, tf.f / 1e3]
fig, ax = plt.subplots(figsize=(8.5, 8))
ax.imshow(np.where(H > 0, 0.97, 0.85), cmap='gray', vmin=0, vmax=1, extent=ext)
im = ax.imshow(np.where(H > 0, eta0, np.nan), cmap='RdBu_r', vmin=-3.5, vmax=3.5, extent=ext)
ax.contour(np.linspace(ext[0], ext[1], nx), np.linspace(ext[3], ext[2], ny), H, levels=[0.5], colors='k', linewidths=.5)
cf = contorno_falla(ESC); ax.plot(cf[:, 0], cf[:, 1], 'k--', lw=1.2, label='Proyección de la falla')
ex, ey = TR.transform(*EPI); ax.plot(ex / 1e3, ey / 1e3, '*', c='red', mec='k', ms=18, label='Epicentro 1979')
ax.legend(loc='upper left'); plt.colorbar(im, shrink=.75, label='Deformación vertical = η inicial (m)')
ax.set_xlim(tf.c / 1e3 + 20, tf.c / 1e3 + 330); ax.set_ylim(tf.f / 1e3 - 420, tf.f / 1e3 - 70); ejes_lonlat(ax)
ax.set_title(f'Fuente de Okada: Mw {ESC["Mw"]}, deslizamiento {slip:.1f} m'); plt.tight_layout()
plt.savefig(WORK / 'fuente_okada.png', dpi=130); plt.show()
'''),
    md("""
## 2. Solver LSWE en malla escalonada

Ecuaciones lineales con profundidad en reposo $H$ fija ($M = Hu$, $N = Hv$ son los flujos por unidad de ancho):

$$
\\frac{\\partial \\eta}{\\partial t} + \\frac{\\partial M}{\\partial x} + \\frac{\\partial N}{\\partial y} = 0, \\qquad
\\frac{\\partial M}{\\partial t} + gH\\frac{\\partial \\eta}{\\partial x} = 0, \\qquad
\\frac{\\partial N}{\\partial t} + gH\\frac{\\partial \\eta}{\\partial y} = 0 .
$$

$\\eta$ se define en el centro de las celdas y $M$, $N$ en sus caras (malla C de Arakawa); primero se actualiza $\\eta$ y luego los flujos con el $\\eta$ nuevo
(*forward-backward*), un esquema clásico de diferencias finitas para aguas someras. Es de segundo orden en el espacio y no añade difusión
numérica. El reposo ($\\eta=0$) es solución exacta para cualquier fondo. Las caras entre una celda de agua y una de tierra tienen flujo nulo (pared en
la línea de costa); las fronteras del dominio son abiertas con la condición de radiación $M = \\pm\\sqrt{gH}\\,\\eta$. **No hay fricción ni términos no
lineales**: el modelo no calcula inundación en tierra.
"""),
    code('''
def run_lswe(H, dx, eta0, dt, t_end, out_every, estaciones=None, umbral=0.1, frontera_ns='abierta'):
    """LSWE en malla C. Devuelve η máxima, tiempo del primer ascenso (η > umbral), instantáneas y series en `estaciones` (lista de (fila, col))."""
    ny, nx = H.shape
    mar = H > 0
    eta = np.where(mar, eta0, 0.0).astype('float64')
    M = np.zeros((ny, nx + 1)); N = np.zeros((ny + 1, nx))
    Hx = np.where(mar[:, :-1] & mar[:, 1:], np.minimum(H[:, :-1], H[:, 1:]), 0.0)
    Hy = np.where(mar[:-1, :] & mar[1:, :], np.minimum(H[:-1, :], H[1:, :]), 0.0)
    c = np.sqrt(G * H)
    cfl = c.max() * dt * np.sqrt(2.0) / dx
    assert cfl < 1.0, f'CFL = {cfl:.2f} >= 1'
    nsteps = int(round(t_end / dt)); cada = int(round(out_every / dt))
    maxeta = eta.copy(); tarr = np.full(H.shape, np.nan, 'float32')
    snap_t, snaps = [0.0], [eta.astype('float16')]
    if estaciones:
        ij = np.array(estaciones); rec = np.zeros((nsteps + 1, len(ij)), 'float32'); rec[0] = eta[ij[:, 0], ij[:, 1]]
    else:
        rec = None
    gdt = G * dt / dx
    for n in range(1, nsteps + 1):
        eta -= dt / dx * ((M[:, 1:] - M[:, :-1]) + (N[1:, :] - N[:-1, :]))
        M[:, 1:-1] -= gdt * Hx * (eta[:, 1:] - eta[:, :-1])
        N[1:-1, :] -= gdt * Hy * (eta[1:, :] - eta[:-1, :])
        M[:, 0] = -c[:, 0] * eta[:, 0];  M[:, -1] = c[:, -1] * eta[:, -1]
        if frontera_ns == 'abierta':
            N[0, :] = -c[0, :] * eta[0, :];  N[-1, :] = c[-1, :] * eta[-1, :]
        np.maximum(maxeta, eta, out=maxeta)
        if n % 5 == 0:
            nuevo = np.isnan(tarr) & (eta > umbral); tarr[nuevo] = n * dt
        if rec is not None:
            rec[n] = eta[ij[:, 0], ij[:, 1]]
        if n % cada == 0:
            snap_t.append(n * dt); snaps.append(eta.astype('float16'))
    return dict(maxeta=maxeta.astype('float32'), tarr=tarr, snap_t=np.array(snap_t), snaps=np.array(snaps), rec=rec, dt=dt, cfl=cfl)

print('✓ Solver definido')
'''),
    md("""
## 3. Verificación del solver

Una onda plana en un canal de 1 000 m de profundidad debe viajar a $c=\\sqrt{gH}$ sin perder amplitud. Se compara con el esquema de Lax-Friedrichs de la
versión 1 (reimplementado aquí solo para la prueba).
"""),
    code('''
def lf_step(eta, u, v, H0, dx, dt, g=G):
    """Esquema de Lax-Friedrichs de la versión 1 (sin fricción), solo para comparar."""
    Qu, Qv = H0 * u, H0 * v; c_ = slice(1, -1); p = slice(2, None); m = slice(0, -2)
    avg = lambda A: 0.25 * (A[c_, p] + A[c_, m] + A[p, c_] + A[m, c_])
    en, un, vn = eta.copy(), u.copy(), v.copy()
    en[c_, c_] = avg(eta) - dt / (2 * dx) * (Qu[c_, p] - Qu[c_, m]) - dt / (2 * dx) * (Qv[p, c_] - Qv[m, c_])
    un[c_, c_] = avg(u) - dt * g * (eta[c_, p] - eta[c_, m]) / (2 * dx)
    vn[c_, c_] = avg(v) - dt * g * (eta[p, c_] - eta[m, c_]) / (2 * dx)
    for a in (en, un, vn):
        a[0, :] = a[1, :]; a[-1, :] = a[-2, :]; a[:, 0] = a[:, 1]; a[:, -1] = a[:, -2]
    return en, un, vn

# Canal plano: pulso gaussiano (σ = 5 km, longitud de onda ~35 km), amplitud 1 m, se parte en dos ondas de 0,5 m
nxt, nyt, dxt, Ht, Tt = 800, 24, 450., 1000., 1200
x = (np.arange(nxt) + .5) * dxt; x0 = nxt * dxt / 2
e0 = np.tile(np.exp(-0.5 * ((x - x0) / 5e3) ** 2), (nyt, 1))
r = run_lswe(np.full((nyt, nxt), Ht), dxt, e0, 1.0, Tt, Tt, frontera_ns='pared')
der = r['snaps'][-1].astype('float64')[nyt // 2, nxt // 2:]
amp_C = der.max(); pos_C = (np.argmax(der) + nxt // 2) * dxt - x0
e, u, v = e0.copy(), np.zeros_like(e0), np.zeros_like(e0)
for _ in range(Tt): e, u, v = lf_step(e, u, v, np.full((nyt, nxt), Ht), dxt, 1.0)
amp_LF = e[nyt // 2, nxt // 2:].max()
print(f'Distancia esperada c·t = {np.sqrt(G*Ht)*Tt/1e3:.1f} km | malla escalonada: pico {pos_C/1e3:.1f} km, amplitud {amp_C:.3f} m (ideal 0,500)')
print(f'Lax-Friedrichs (versión 1): amplitud {amp_LF:.3f} m → conserva {100*amp_LF/0.5:.0f} % tras {np.sqrt(G*Ht)*Tt/1e3:.0f} km')
assert amp_C > 0.49 and abs(pos_C - np.sqrt(G * Ht) * Tt) < 2 * dxt, 'el solver escalonado no propaga bien la onda plana'

# Reposo: sin fuente no hay movimiento
r0 = run_lswe(H, DX, np.zeros_like(eta0), DT, 60., 60.)
assert np.abs(r0['maxeta']).max() == 0.0
print('✓ Reposo exacto; ✓ onda plana')
'''),
    md("""
## 4. Estaciones

Cada estación de la tabla de observaciones se lleva a la **celda de mar más cercana con profundidad de al menos 10 m y a menos de 10 km**. Con 450 m de
resolución y sin inundación, una celda en la línea de costa (profundidades de 0 a pocos metros) no es una lectura representativa. Las estaciones cuya
coordenada cae tierra adentro, en un estuario somero o fuera del dominio se **excluyen y se declara**.
"""),
    code('''
obs = pd.read_csv(datos('observaciones_1979.csv'))

def elegir_celda(H, tf, dx, lon, lat, hmin=10., rmax=10e3):
    ny, nx = H.shape; x, y = TR.transform(lon, lat)
    ri, ci = (y - tf.f) / tf.e - .5, (x - tf.c) / tf.a - .5
    if not (0 <= ri < ny and 0 <= ci < nx):
        return None, np.nan, np.nan, 'fuera del dominio'
    w = np.argwhere(H >= hmin); d = np.hypot(w[:, 0] - ri, w[:, 1] - ci) * dx; k = d.argmin()
    if d[k] > rmax:
        return None, d[k] / 1e3, np.nan, f'sin mar de ≥ 10 m a < 10 km (el más cercano, a {d[k]/1e3:.0f} km)'
    return tuple(int(v) for v in w[k]), d[k] / 1e3, H[tuple(w[k])], 'ok'

def tabla_estaciones(H, tf, dx):
    filas = []
    for _, r in obs.iterrows():
        ij, d, h, est = elegir_celda(H, tf, dx, r.lon, r.lat)
        filas.append(dict(estacion=r.estacion, fila=-1 if ij is None else ij[0], col=-1 if ij is None else ij[1],
                          dist_celda_km=d, H_celda_m=h, estado=est))
    return pd.DataFrame(filas)

est = tabla_estaciones(H, tf, DX)
est
'''),
    md("## 5. Simulación (450 m, 60 min)"),
    code('''
import time
ok = est[est.estado == 'ok']
cel = [(int(r.fila), int(r.col)) for _, r in ok.iterrows()]
t0 = time.time()
res = run_lswe(H, DX, eta0, DT, T_END, OUT_EVERY, estaciones=cel)
print(f'✓ {int(T_END/DT)} pasos en {time.time()-t0:.0f} s | CFL = {res["cfl"]:.2f} | η máx. (profundidad ≥ 10 m) = {res["maxeta"][H >= 10].max():.2f} m')

np.savez_compressed(OUT / 'resultados.npz', H=H.astype('float32'), maxeta=res['maxeta'], tarr=res['tarr'],
                    snap_t=res['snap_t'], snaps=res['snaps'], rec=res['rec'], dt=DT,
                    x0=tf.c, y0=tf.f, dx=DX, slip=slip, eta0=eta0, idx_est=ok.index.values)
est.to_csv(OUT / 'estaciones.csv', index=False)
print('Guardado en', OUT / 'resultados.npz')
'''),
    md("""
## 6. Sensibilidad

Con la malla de 900 m (4 s por corrida) se mide cuánto cambian la amplitud y el arribo en las estaciones al variar la resolución y los parámetros **supuestos** de la
fuente. Es un análisis de un parámetro a la vez, no una cuantificación de la incertidumbre.
"""),
    code('''
def correr(dx, dt, esc):
    Hh, tff = cargar_H(dx); e0, _ = eta_inicial(tff, Hh.shape, esc); e0 = np.where(Hh > 0, e0, 0.0)
    ee = tabla_estaciones(Hh, tff, dx); oo = ee[ee.estado == 'ok']
    rr = run_lswe(Hh, dx, e0, dt, 3600., 600., estaciones=[(int(a), int(b)) for a, b in zip(oo.fila, oo.col)])
    tt = np.arange(rr['rec'].shape[0]) * dt
    sal = {}
    for k, nombre in enumerate(oo.estacion):
        s = rr['rec'][:, k]; sal[nombre] = (s.max(), tt[np.argmax(s > 0.1)] / 60 if (s > 0.1).any() else np.nan)
    return sal

casos = {'base (900 m)': (900., 2.0, ESC),
         'Mw 8,2': (900., 2.0, {**ESC, 'Mw': 8.2}),
         'buzamiento 12°': (900., 2.0, {**ESC, 'dip': 12.}),
         'buzamiento 18°': (900., 2.0, {**ESC, 'dip': 18.}),
         'rumbo 20°': (900., 2.0, {**ESC, 'strike': 20.}),
         'rumbo 40°': (900., 2.0, {**ESC, 'strike': 40.}),
         'longitud 150 km': (900., 2.0, {**ESC, 'L': 150e3}),
         'longitud 250 km': (900., 2.0, {**ESC, 'L': 250e3}),
         'profundidad sup. 8 km': (900., 2.0, {**ESC, 'top_depth': 8e3}),
         'profundidad sup. 16 km': (900., 2.0, {**ESC, 'top_depth': 16e3}),
         'parámetros de la v1 (README)': (900., 2.0, {**ESC, 'Mw': 8.2, 'strike': 10., 'dip': 20., 'L': 250e3, 'W': 100e3})}
filas = []
for nombre, (dx_, dt_, esc_) in casos.items():
    s = correr(dx_, dt_, esc_)
    fila = {'caso': nombre}
    for e_, (a, t_) in s.items():
        fila[f'{e_} η máx (m)'] = round(float(a), 2); fila[f'{e_} arribo (min)'] = round(float(t_), 1)
    filas.append(fila)
# Referencia: la corrida base a 450 m
rec = res['rec']; tt = np.arange(rec.shape[0]) * DT; fila = {'caso': 'base (450 m)'}
for k, nombre in enumerate(ok.estacion):
    s = rec[:, k]; fila[f'{nombre} η máx (m)'] = round(float(s.max()), 2)
    fila[f'{nombre} arribo (min)'] = round(float(tt[np.argmax(s > 0.1)] / 60), 1)
filas.insert(0, fila)
sens = pd.DataFrame(filas).set_index('caso')
sens.to_csv(OUT / 'sensibilidad.csv')
sens.T
'''),
]

# --------------------------------------------------------------------------
# Cuaderno 3
# --------------------------------------------------------------------------
nb3 = [
    md(f"""
# Cuaderno 3: Visualización y comparación con 1979

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}03-visualization.ipynb)

Mapas, series de tiempo, control de calidad de las observaciones, comparación con 1979 y animación. **Requiere los resultados del cuaderno 2**
(`output/resultados.npz`). **Runtime:** CPU, 1–2 minutos.

**Qué es y qué no es la comparación.** Las ocho observaciones de la tabla `data/observaciones_1979.csv` están **sin verificar contra las fuentes primarias**, y
varias coordenadas son aproximadas (dos quedan tierra adentro). El modelo es lineal y sin inundación, de modo que su η en el mar **no es un run-up**.
Se muestran las diferencias para ubicar el orden de magnitud y los límites del modelo, no para validarlo.
"""),
    code(COMUN),
    code('''
from matplotlib.animation import FuncAnimation, PillowWriter
if not (OUT / 'resultados.npz').exists():
    raise FileNotFoundError('Falta output/resultados.npz: ejecute primero el cuaderno 2.')
R = np.load(OUT / 'resultados.npz')
H = R['H'].astype('float64'); maxeta, tarr = R['maxeta'], R['tarr']
snap_t, snaps, rec, dt = R['snap_t'], R['snaps'], R['rec'], float(R['dt'])
x0, y0, dx = float(R['x0']), float(R['y0']), float(R['dx'])
ny, nx = H.shape
ext = [x0 / 1e3, (x0 + dx * nx) / 1e3, (y0 - dx * ny) / 1e3, y0 / 1e3]   # oeste a la izquierda, norte arriba
est = pd.read_csv(OUT / 'estaciones.csv'); obs = pd.read_csv(datos('observaciones_1979.csv'))
ex, ey = TR.transform(*EPI)
tt = np.arange(rec.shape[0]) * dt
print(f'Resultados: malla {nx}×{ny}, {len(snap_t)} instantáneas (0–{snap_t[-1]/60:.0f} min), {rec.shape[1]} estaciones en el mar')

# Prueba de orientación y de fuente: el máximo de η inicial debe estar cerca del epicentro (decenas de km), no a cientos
eta_ini = snaps[0].astype('float64')
i, j = np.unravel_index(np.argmax(eta_ini), eta_ini.shape)
d_max = np.hypot(x0 + dx * (j + .5) - ex, y0 - dx * (i + .5) - ey) / 1e3
assert d_max < 150, f'la fuente está a {d_max:.0f} km del epicentro'
print(f'✓ El máximo de η inicial ({eta_ini.max():.1f} m) está a {d_max:.0f} km del epicentro')
'''),
    md("""
## 1. Control de calidad de las observaciones

Antes de comparar, se revisa que las observaciones sean físicamente coherentes con una onda larga $c=\\sqrt{gH}$: con la distancia de círculo máximo $d$ al
epicentro y el arribo $t$, la profundidad equivalente es $H_{eq}=(d/t)^2/g$. En el océano frente a Colombia las profundidades son de 3 000–4 000 m
(hasta ~5 000 m en el dominio); una profundidad equivalente mayor sobre una ruta que cruza plataforma y talud indica un dato sospechoso. Es el mismo control del
cuaderno 318 del libro *Teoría y métodos de análisis de riesgos*.
"""),
    code('''
def dist_km(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(np.radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(a))

qc = obs.copy()
qc['dist_km'] = dist_km(EPI[1], EPI[0], qc.lat, qc.lon).round(0)
qc['v_media_ms'] = (qc.dist_km * 1e3 / (qc.tiempo_arr_min * 60)).round(0)
qc['H_equiv_m'] = (qc.v_media_ms ** 2 / G).round(-1)
qc = qc.merge(est[['estacion', 'estado']], on='estacion')
dominio = (qc.lon.between(-81.2, -76.9)) & (qc.lat.between(-0.2, 4.2))
qc.loc[~dominio, 'estado'] = 'fuera del dominio'
qc['sospechoso'] = np.where(qc.H_equiv_m > 4000, 'H equiv. > 4 000 m', '')
qc[['estacion', 'dist_km', 'runup_m', 'tiempo_arr_min', 'v_media_ms', 'H_equiv_m', 'sospechoso', 'estado', 'fuente']]
'''),
    md("## 2. Elevación máxima de la ola"),
    code('''
def fondo(ax):
    ax.imshow(np.where(H > 0, 0.97, 0.86), cmap='gray', vmin=0, vmax=1, extent=ext)
def costa(ax):
    ax.contour(np.linspace(ext[0], ext[1], nx), np.linspace(ext[3], ext[2], ny), H, levels=[0.5], colors='k', linewidths=.5)

fig, axs = plt.subplots(1, 2, figsize=(15, 7.5))
ax = axs[0]; fondo(ax)
ax.contour(np.linspace(ext[0], ext[1], nx), np.linspace(ext[3], ext[2], ny), H, levels=[200, 1000, 3000], colors='#8c99a6', linewidths=.4)
im = ax.imshow(np.where(H >= 10, np.maximum(maxeta, 0), np.nan), cmap='YlOrRd', vmin=0, vmax=5, extent=ext, alpha=.9)
costa(ax); plt.colorbar(im, ax=ax, shrink=.75, label='η máxima en 60 min, profundidad ≥ 10 m (m)')
ax.plot(ex / 1e3, ey / 1e3, '*', c='red', mec='k', ms=18, label='Epicentro 1979'); ax.legend(loc='upper left'); ejes_lonlat(ax)
ax.set_title('Elevación máxima de la superficie del mar (LSWE, 0–60 min)')

ax = axs[1]; fondo(ax)
zona = (H >= 10) & (H < 200)
im2 = ax.imshow(np.where(zona, np.maximum(maxeta, 0), np.nan), cmap='YlOrRd', vmin=0, vmax=8, extent=ext)
costa(ax); plt.colorbar(im2, ax=ax, shrink=.75, label='η máxima, profundidad 10–200 m (m)')
tx, ty = TR.transform(-78.80, 1.85)
ax.set_xlim(tx / 1e3 - 55, tx / 1e3 + 55); ax.set_ylim(ty / 1e3 - 50, ty / 1e3 + 50)
for _, r in qc.iterrows():
    x, y = TR.transform(r.lon, r.lat)
    if abs(x - tx) < 55e3 and abs(y - ty) < 50e3:
        ax.plot(x / 1e3, y / 1e3, 'ko', ms=4); ax.annotate(r.estacion, (x / 1e3, y / 1e3), textcoords='offset points', xytext=(4, 4), fontsize=8)
ejes_lonlat(ax, paso=.25); ax.set_title('Zona costera de Tumaco (η máx. en plataforma)')
plt.tight_layout(); plt.savefig(WORK / 'max_eta_map.png', dpi=130, bbox_inches='tight'); plt.show()
print(f'η máxima (profundidad ≥ 10 m): {maxeta[H>=10].max():.2f} m | plataforma 10–200 m: {maxeta[zona].max():.2f} m')
print(f'(en celdas de < 10 m el modelo lineal llega a {maxeta[H>0].max():.0f} m: amplificación sin fricción ni rotura, no se interpreta)')
'''),
    md("""
## 3. Series de tiempo y arribos

El arribo simulado es el **primer instante con η > 0,1 m** (primer ascenso del nivel; en Tumaco la deformación inicial es un descenso y el primer ascenso es la llegada de la ola). La lectura se toma en la celda de mar descrita en el cuaderno 2.
"""),
    code('''
ok = est[est.estado == 'ok'].reset_index(drop=True)
sim = []
for k, r in ok.iterrows():
    s = rec[:, k]; ta = tt[np.argmax(s > 0.1)] / 60 if (s > 0.1).any() else np.nan
    sim.append(dict(estacion=r.estacion, H_celda_m=r.H_celda_m, eta_max_m=s.max(), eta_min_m=s.min(),
                    t_arribo_sim_min=ta, t_cresta_min=tt[np.argmax(s)] / 60))
sim = pd.DataFrame(sim).merge(obs[['estacion', 'runup_m', 'tiempo_arr_min']], on='estacion')
sim['razon_amplitud'] = (sim.eta_max_m / sim.runup_m).round(2)
sim['dif_arribo_min'] = (sim.t_arribo_sim_min - sim.tiempo_arr_min).round(1)

fig, axs = plt.subplots(2, 2, figsize=(14, 7.5), sharex=True)
for ax, (_, r), k in zip(axs.flat, sim.iterrows(), range(len(sim))):
    s = rec[:, k]
    ax.plot(tt / 60, s, c='#0154a5', lw=1.6)
    ax.axhline(0, c='k', lw=.4)
    ax.axvline(r.tiempo_arr_min, c='#c0392b', ls='--', lw=1.2, label=f'Arribo observado ({r.tiempo_arr_min:.0f} min)*')
    ax.axvline(r.t_arribo_sim_min, c='#0154a5', ls=':', lw=1.2, label=f'Arribo simulado ({r.t_arribo_sim_min:.0f} min)')
    ax.axhline(r.runup_m, c='#c0392b', ls='-.', lw=.8, alpha=.6, label=f'Run-up observado ({r.runup_m} m)*')
    ax.set_title(f'{r.estacion} (celda de {r.H_celda_m:.0f} m de profundidad)', fontsize=10); ax.set_ylabel('η (m)'); ax.legend(fontsize=7, loc='upper left'); ax.grid(alpha=.3)
for ax in axs[1]: ax.set_xlabel('Tiempo desde el sismo (min)')
fig.text(.01, .005, '* Observaciones de data/observaciones_1979.csv, sin verificar contra la fuente primaria.', fontsize=8)
plt.tight_layout(); plt.savefig(WORK / 'time_series.png', dpi=130, bbox_inches='tight'); plt.show()
sim.round(2)
'''),
    md("## 4. Comparación indicativa con las observaciones"),
    code('''
fig, axs = plt.subplots(1, 2, figsize=(13, 5))
ax = axs[0]
ax.plot([0, 40], [0, 40], 'k--', lw=1, label='1:1')
ax.scatter(sim.tiempo_arr_min, sim.t_arribo_sim_min, s=70, c='#0154a5', zorder=3)
for _, r in sim.iterrows(): ax.annotate(r.estacion, (r.tiempo_arr_min, r.t_arribo_sim_min), textcoords='offset points', xytext=(5, 4), fontsize=8)
ax.set(xlim=(5, 30), ylim=(5, 30), xlabel='Arribo observado* (min)', ylabel='Arribo simulado (min)', title='Tiempos de arribo'); ax.legend(); ax.grid(alpha=.3)
ax = axs[1]; xp = np.arange(len(sim)); w = .38
ax.bar(xp - w / 2, sim.runup_m, w, label='Run-up observado*', color='#c0392b', alpha=.85)
ax.bar(xp + w / 2, sim.eta_max_m, w, label='η máxima simulada (mar, sin inundación)', color='#0154a5', alpha=.85)
ax.set_xticks(xp); ax.set_xticklabels(sim.estacion, rotation=20, ha='right', fontsize=8); ax.set_ylabel('m'); ax.legend(fontsize=8); ax.grid(axis='y', alpha=.3)
ax.set_title('Amplitudes (no son magnitudes equivalentes)')
plt.tight_layout(); plt.savefig(WORK / 'validation.png', dpi=130, bbox_inches='tight'); plt.show()

print(f'Estaciones comparables: {len(sim)} de {len(obs)}')
print('Excluidas:'); print(qc[qc.estado != 'ok'][['estacion', 'estado']].to_string(index=False))
print(f'\\nArribo: diferencia simulado − observado entre {sim.dif_arribo_min.min():+.0f} y {sim.dif_arribo_min.max():+.0f} min')
print(f'Amplitud: η simulada / run-up observado entre {sim.razon_amplitud.min():.1f} y {sim.razon_amplitud.max():.1f}')
'''),
    md("""
### Contraste con resultados publicados

Dos trabajos de la literatura simularon el escenario de 1979 en Tumaco con **modelos no lineales con cálculo de inundación** (Ávila-Guzmán et al. usan TUNAMI-N2) y distribuciones
de deslizamiento de Poveda y Pulido (2019). Se citan aquí **como referencia de orden de magnitud**; su fuente, su malla y sus definiciones difieren de las de este cuaderno.
"""),
    code('''
tum = sim.estacion.str.startswith("Tumaco")
pub = pd.DataFrame([
    ['Altura máxima del tsunami, isla de Tumaco, escenario 1979 (modelo de déficit de deslizamiento)', '2,30 m', 'Escobar et al. (2020), tabla 3'],
    ['Altura máxima del tsunami, isla de Tumaco, escenario 1979 (modelo de banda ancha)', '1,88 m', 'Escobar et al. (2020), tabla 3'],
    ['Llegada de la primera ola a Tumaco', '22 min', 'Ávila-Guzmán et al. (2026)'],
    ['Este cuaderno: η máxima en celdas de mar de 10-25 m, Tumaco', f'{sim.eta_max_m[tum].min():.1f}-{sim.eta_max_m[tum].max():.1f} m', 'LSWE lineal, 450 m'],
    ['Este cuaderno: primer ascenso > 0,1 m en Tumaco', f'{sim.t_arribo_sim_min[tum].min():.0f}-{sim.t_arribo_sim_min[tum].max():.0f} min', 'LSWE lineal, 450 m']],
    columns=['Magnitud', 'Valor', 'Fuente'])
pub
'''),
    md("""
## 5. Sensibilidad (resumen del cuaderno 2)
"""),
    code('''
sp = OUT / 'sensibilidad.csv'
if sp.exists():
    sens = pd.read_csv(sp, index_col=0)
    cols = [c for c in sens.columns if 'η máx' in c]
    display(sens[cols].describe().loc[['min', 'max']].T.round(2).rename(columns={'min': 'mínimo', 'max': 'máximo'}))
    display(sens[[c for c in sens.columns if 'arribo' in c]].describe().loc[['min', 'max']].T.round(1).rename(columns={'min': 'mínimo', 'max': 'máximo'}))
else:
    print('Ejecute la sección 6 del cuaderno 2 para generar output/sensibilidad.csv')
'''),
    md("""
## 6. Animación de la propagación

Mapa con el **oeste a la izquierda y el norte arriba**; la estrella marca el epicentro y la falla se muestra con su proyección. η en metros (|η| < 0,1 m se deja transparente).
"""),
    code('''
cf_t = None
fig, ax = plt.subplots(figsize=(8.2, 8))
fondo(ax)
ax.contour(np.linspace(ext[0], ext[1], nx), np.linspace(ext[3], ext[2], ny), H, levels=[200, 1000, 3000], colors='#8c99a6', linewidths=.4)
costa(ax)
agua = ax.imshow(np.full(H.shape, np.nan), cmap='RdBu_r', vmin=-3, vmax=3, extent=ext, alpha=.9)
plt.colorbar(agua, ax=ax, shrink=.7, label='η (m)')
ax.plot(ex / 1e3, ey / 1e3, '*', c='red', mec='k', ms=18, zorder=10, label='Epicentro 1979')
for nombre, (lon, lat) in {'Tumaco': (-78.76, 1.82), 'Esmeraldas': (-79.65, 0.97), 'Buenaventura': (-77.02, 3.88)}.items():
    x, y = TR.transform(lon, lat); ax.plot(x / 1e3, y / 1e3, 'ko', ms=4, zorder=9)
    ax.annotate(nombre, (x / 1e3, y / 1e3), textcoords='offset points', xytext=(5, 4), fontsize=8)
ax.legend(loc='upper left'); ejes_lonlat(ax)
ax.set_xlim(ext[0] + 5, ext[1] - 5); ax.set_ylim(ext[2] + 5, ext[3] - 5)
titulo = ax.set_title('')

def cuadro(k):
    e = snaps[k].astype('float32'); agua.set_array(np.where((np.abs(e) > 0.1) & (H >= 10), e, np.nan))
    titulo.set_text(f't = {snap_t[k]/60:.0f} min — Tsunami de Tumaco 1979 (LSWE)')
    return [agua, titulo]

anim = FuncAnimation(fig, cuadro, frames=len(snap_t), interval=250, blit=False)
gif = WORK / 'tsunami_propagation.gif'
anim.save(str(gif), writer=PillowWriter(fps=4), dpi=80)
plt.close(fig)
print(f'✓ Animación: {len(snap_t)} cuadros, t = 0–{snap_t[-1]/60:.0f} min, {gif.stat().st_size/1e6:.1f} MB')
'''),
    code('''
from IPython.display import Image, display
display(Image(str(gif)))
'''),
    md("## 7. Resumen"),
    code('''
print('=' * 62); print('RESUMEN — TSUNAMI DE TUMACO 1979 (versión 2)'); print('=' * 62)
print(f'  Modelo:              LSWE, malla escalonada, {dx:.0f} m, dt = {dt:.0f} s')
print(f'  Fuente:              Okada (1985), Mw {8.3}, deslizamiento uniforme {float(R["slip"]):.1f} m (geometría supuesta)')
print(f'  η máx. (≥ 10 m prof.): {maxeta[H>=10].max():.2f} m | plataforma 10–200 m: {maxeta[zona].max():.2f} m')
print(f'  Estaciones:          {len(sim)} comparables de {len(obs)} (resto excluido, ver sección 4)')
print(f'  Arribo sim − obs:    {sim.dif_arribo_min.min():+.0f} a {sim.dif_arribo_min.max():+.0f} min (obs. sin verificar)')
print(f'  η sim / run-up obs:  {sim.razon_amplitud.min():.1f} a {sim.razon_amplitud.max():.1f}')
for f in ['max_eta_map.png', 'time_series.png', 'validation.png', 'tsunami_propagation.gif', 'fuente_okada.png']:
    p = WORK / f; print(f'  {"✓" if p.exists() else "✗"} {f}')
'''),
]

if __name__ == "__main__":
    guardar("01-bathymetry.ipynb", nb1)
    guardar("02-simulation.ipynb", nb2)
    guardar("03-visualization.ipynb", nb3)
