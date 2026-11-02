# Datos del proyecto (versión 2)

## Batimetría y topografía: `dem_tumaco_noaa_15s.tif`

Recorte geográfico (EPSG:4326, 1 032 × 1 056 celdas de 15 arco-segundos, unos 460 m) del dominio **0,2° S–4,2° N y 81,2°–76,9° O**, pedido el 2 de noviembre de 2026 al
servicio de mosaico global de DEM de NOAA/NCEI:

```
https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/DEM_global_mosaic/ImageServer
```

Es un **mosaico de modelos de distinta resolución y procedencia**; no es GEBCO ni ETOPO 2022 puros. La versión 1 de este repositorio los nombraba, pero el enlace de
descarga de GEBCO que usaba responde 404 y el servicio entregaba el mosaico de NOAA. El cuaderno 1 usa esta copia y, si no está, vuelve a pedirla al servicio.

Valores de control: elevación −5 183 a 5 615 m; el punto del epicentro está a −834 m y Tumaco a unos 4 m.

## Observaciones históricas: `observaciones_1979.csv`

Ocho estaciones con run-up y tiempo de arribo del tsunami del 12 de diciembre de 1979.

| Campo | Descripción | Unidades |
|-------|-------------|---------|
| `estacion` | Nombre del lugar de observación | — |
| `lat` | Latitud | °N |
| `lon` | Longitud | °E (negativo al oeste) |
| `runup_m` | Run-up observado | m |
| `tiempo_arr_min` | Tiempo de arribo después del sismo | min |
| `fuente` | Referencia declarada en la tabla (Herd et al., 1981; base de tsunamis de NOAA/NGDC) | — |

> **Estado: sin verificar contra las fuentes primarias.** Los valores se heredaron de la versión 1 y no se han contrastado con Herd et al. (1981) ni con la base de
> NOAA/NGDC. Las coordenadas de varias estaciones son aproximadas: **San Juan** y **El Charco** caen tierra adentro, **Buenaventura** en un estuario somero y **Salinas**
> queda fuera del dominio; en el cuaderno 3 se excluyen y se declara. El arribo de Salinas (35 min a unos 460 km) exige una profundidad equivalente de unos 4 900 m a lo
> largo de toda la ruta y es físicamente sospechoso. Las cifras de run-up (3–5 m en Tumaco) tampoco coinciden con las alturas máximas de 1,9–2,3 m que Escobar et al. (2020)
> simulan para la isla de Tumaco.

## Escenario sísmico usado en la versión 2

| Parámetro | Valor | Estado |
|-----------|-------|--------|
| Mw | 8,3 | Yoshimoto et al. (2017), citado por Escobar et al. (2020) y Ávila-Guzmán et al. (2026) |
| Epicentro | 1,598° N, 79,359° O | Según Herd et al. (1981) (por verificar) |
| Profundidad del hipocentro | 33 km | Según el artículo de la versión 1 (por verificar) |
| Longitud × ancho de la falla | 200 × 80 km | **Supuesto** |
| Rumbo / buzamiento / ángulo de desplazamiento | 30° / 15° / 90° | **Supuesto** |
| Profundidad del borde superior | 12 km | **Supuesto** (el borde inferior queda a ~33 km) |
| Rigidez / Poisson | 30 GPa / 0,25 | Valores típicos |
| Deslizamiento uniforme | 7,4 m | Derivado de M₀ = μ·L·W·D |

La versión 1 documentaba otros valores (Mw 8,2; rumbo ~10°, buzamiento ~20°, 250 × 100 km, deslizamiento ~4 m), también sin fuente verificable; se corren como un caso de
sensibilidad (cuaderno 2, sección 6). La distribución de deslizamiento real del evento (Poveda y Pulido, 2019) **no se usó** porque no se tiene a mano.

## Salidas de los cuadernos (no se versionan)

`notebooks/output/` (o `/content/output/` en Colab): `dem_utm17_450m.tif`, `resultados.npz` (η máxima, mapa de arribos, 31 instantáneas, series en estaciones),
`estaciones.csv` y `sensibilidad.csv`.
