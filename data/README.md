# Datos del proyecto

## Batimetría y topografía

El modelo de elevación digital (DEM) combinado se genera en el cuaderno `01-bathymetry.ipynb` descargando datos de fuentes públicas. No se incluye el GeoTIFF en el repositorio por su tamaño (~40-100 MB).

### Fuentes de datos

| Dataset | Fuente | Resolución | Cobertura | Acceso |
|---------|--------|-----------|-----------|--------|
| GEBCO 2023 | British Oceanographic Data Centre | 15 arc-sec (~450 m) | Global | Libre |
| ETOPO 2022 | NOAA NCEI | 15 arc-sec (~450 m) | Global | Libre |
| SRTM GL1 | NASA/USGS | 1 arc-sec (~30 m) | Global (terrestre) | Libre |

### Descarga manual (alternativa)

Si el acceso automático falla, descarga el GeoTIFF manualmente:

**GEBCO 2023 — sub-región Tumaco:**
1. Ir a https://download.gebco.net
2. Seleccionar región: Lat 0.5° a 3.5°N, Lon 79.5° a 77.0°W
3. Formato: NetCDF o GeoTIFF
4. Subir el archivo a `/content/` en Google Colab

**ETOPO 2022 — alternativa:**
```
https://www.ncei.noaa.gov/maps/grid-extract/
```

## Observaciones históricas del tsunami de 1979

El archivo `observaciones_1979.csv` contiene datos históricos de run-up del tsunami del 12 de diciembre de 1979 (Mw 8.2), compilados de la literatura científica [Herd et al., 1981; NOAA NGDC Tsunami Database].

### Columnas

| Campo | Descripción | Unidades |
|-------|-------------|---------|
| `estacion` | Nombre del lugar de observación | — |
| `lat` | Latitud | °N |
| `lon` | Longitud | °W (negativo) |
| `runup_m` | Altura máxima de run-up observada | metros |
| `tiempo_arr_min` | Tiempo de arribo después del sismo | minutos |
| `fuente` | Referencia bibliográfica | — |

## Parámetros sísmicos del evento de 1979

| Parámetro | Valor | Fuente |
|-----------|-------|--------|
| Fecha y hora (UTC) | 1979-12-12 07:59:04 | USGS |
| Latitud epicentro | 1.598°N | USGS/Herd et al. 1981 |
| Longitud epicentro | 79.359°W | USGS/Herd et al. 1981 |
| Profundidad | 33 km | USGS |
| Magnitud Mw | 8.2 | Kanamori & McNally 1982 |
| Mecanismo focal | Falla inversa (thrust) | — |
| Strike / Dip / Rake | ~10° / ~20° / ~90° | Kanamori & McNally 1982 |
| Longitud de ruptura | ~250 km | Herd et al. 1981 |
| Ancho de ruptura | ~100 km | estimado |
| Deslizamiento promedio | ~4 m | estimado |
