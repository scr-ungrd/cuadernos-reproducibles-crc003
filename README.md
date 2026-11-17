# CRC003: análisis de sismicidad de Colombia con el catálogo del USGS

> **Cuaderno reproducible de conocimiento del riesgo.** Subdirección para el Conocimiento del Riesgo (SCR), Unidad Nacional para la Gestión del Riesgo de Desastres (UNGRD), Colombia.
> **Ejercicio sin validar por una persona experta: no usar para tomar decisiones.**

- **Sitio:** <https://scr-ungrd.github.io/cuadernos-reproducibles-crc003/>
- **Binder:** <https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc003/main>

## Qué hace

Analiza la sismicidad de Colombia con el catálogo público del USGS (2000 a 2026): magnitud de completitud, relación de Gutenberg-Richter por máxima verosimilitud, profundidad focal, variación estacional, sismos históricos, mapas y animación, cortes transversales, vista 3D y una ficha departamental (piloto de Córdoba). Describe amenaza, no riesgo. Sirve para aprender el método, no para un estudio de amenaza.

## Estructura

| Ruta | Contenido |
|---|---|
| `sismicidad-colombia.ipynb` | Cuaderno principal |
| `data/` | Catálogos del USGS fijados al 2026-11-16 |
| `metadata/` | Fuentes (`sources.csv`), catálogo y diccionario de datos, sumas SHA-256 y metadatos RDLS |
| `scripts/` | `descargar_catalogo.py`, `generar_banner.py` y `registrar_descargas.py` |
| `ficha_sismica_cordoba.*`, `*.png`, `*.html`, `*.mp4` | Productos del cuaderno |
| `DATA_STATEMENT.md`, `CITATION.cff`, `CHANGELOG.md`, `AI_USE.md` | Disponibilidad de datos y de código, cita, historial de cambios y uso de IA |

## Ejecutar

```bash
conda env create -f environment.yml
conda activate riesgos-sismicidad
jupyter lab sismicidad-colombia.ipynb
```

Las consultas al USGS tienen una fecha de corte fija (2026-11-16) y reproducen los datos de `data/`. Para actualizarlas, cambie la fecha de corte en el cuaderno y en `scripts/descargar_catalogo.py`.

## Licencia

Código bajo licencia MIT; texto y figuras bajo CC BY 4.0. Los catálogos del USGS son de dominio público. Los límites de geoBoundaries están bajo ODbL 1.0 y Natural Earth es de dominio público; la base de sismos significativos de NOAA/NCEI es de dominio público en EE. UU. y NCEI aplica CC0 a nivel internacional (véase `metadata/sources.csv`).

## Cita y DOI

Los metadatos de cita están en [`CITATION.cff`](CITATION.cff). El DOI de todas las versiones es [10.5281/zenodo.24322597](https://doi.org/10.5281/zenodo.24322597); la versión 0.1.0 tiene el DOI [10.5281/zenodo.24322598](https://doi.org/10.5281/zenodo.24322598).

## Uso de inteligencia artificial

El desarrollo de este repositorio contó con la asistencia de Claude Sonnet 5.5, según el historial de commits. El registro y la declaración están en [`AI_USE.md`](AI_USE.md).
