# Diccionario de variables

Describe los datos de `data/` y la ficha departamental. Los vacíos son valores faltantes y se dejan en blanco. Las fechas del catálogo son ISO 8601 en UTC y las coordenadas, grados decimales (WGS 84). Fuentes: `metadata/sources.csv`.

## `data/usgs_catalogo_m3_2000-2026-11-16.csv` y `data/usgs_catalogo_ampliado_1900-2026-11-16.csv`

Una fila por evento del catálogo ComCat del USGS, sin modificar. Las columnas siguen la documentación del servicio FDSN Event del USGS.

| Columna | Descripción | Unidad |
|---|---|---|
| `time` | Hora de origen del evento (UTC, ISO 8601) | |
| `latitude` | Latitud del epicentro | grados |
| `longitude` | Longitud del epicentro | grados |
| `depth` | Profundidad del hipocentro | km |
| `mag` | Magnitud | |
| `magType` | Tipo de magnitud (por ejemplo, Mw, mb, Ml o Ms) | |
| `nst` | Número de estaciones usadas para localizar el evento | estaciones |
| `gap` | Mayor brecha azimutal entre estaciones | grados |
| `dmin` | Distancia horizontal del epicentro a la estación más cercana | grados |
| `rms` | Raíz del error cuadrático medio de los residuos de tiempo | s |
| `net` | Red que aportó el identificador del evento | |
| `id` | Identificador único del evento | |
| `updated` | Hora de la última actualización del evento | |
| `place` | Descripción textual de la región | |
| `type` | Tipo de evento (en el catálogo ampliado, solo `earthquake`) | |
| `horizontalError` | Incertidumbre horizontal de la localización | km |
| `depthError` | Incertidumbre de la profundidad | km |
| `magError` | Incertidumbre de la magnitud | |
| `magNst` | Número de estaciones usadas para la magnitud | estaciones |
| `status` | Estado de la revisión (`automatic` o `reviewed`) | |
| `locationSource` | Red que aportó la localización | |
| `magSource` | Red que aportó la magnitud | |

Los campos pueden estar vacíos cuando el USGS no los informa. Las profundidades antiguas suelen ser valores fijos asignados por la agencia (10, 33 o 35 km).

## `ficha_sismica_cordoba.json`

Indicadores sísmicos de un departamento y de su entorno, calculados por `indicadores_sismicos()` del cuaderno (sección 16) con el catálogo ampliado y los límites de geoBoundaries.

| Clave | Descripción | Unidad |
|---|---|---|
| `departamento` | Nombre del departamento según geoBoundaries | |
| `radio_km` | Radio alrededor de la frontera del departamento que define el entorno | km |
| `mag_minima_catalogo` | Magnitud mínima del catálogo usado | |
| `periodo` | Año inicial y año final del catálogo | años |
| `mag_completa` | Magnitud de completitud usada para comparar tasas | |
| `anio_completo` | Año desde el que el catálogo es completo para `mag_completa` | año |
| `n_dentro` | Sismos dentro del departamento | eventos |
| `n_hasta_50km` | Sismos a 50 km o menos de su frontera (incluye los de dentro) | eventos |
| `n_en_radio` | Sismos dentro de `radio_km` de su frontera | eventos |
| `n_completos_en_radio` | Sismos del entorno con magnitud mayor o igual que `mag_completa` desde `anio_completo` | eventos |
| `pct_superficiales` | Porcentaje de esos sismos con profundidad de 70 km o menos | % |
| `b` | Valor b de Gutenberg-Richter (estimador de Aki-Utsu) | |
| `b_error` | Error estándar de `b` (b dividido por la raíz del número de sismos completos) | |
| `retorno_anios` | Periodo de retorno de sismos de magnitud 5, 6 y 7 o mayor en el entorno, con la tasa de sismos completos y `b` | años |
| `mayor` | Mayor sismo del entorno: `mag`, `fecha` (AAAA-MM-DD), `prof_km`, `lugar` y `dist_km` (distancia a la frontera) | |
| `mayores` | Los cinco mayores sismos del entorno, con los mismos campos | |

`ficha_sismica_cordoba.md` y `ficha_sismica_cordoba.png` presentan los mismos indicadores en texto y en cuatro paneles.
