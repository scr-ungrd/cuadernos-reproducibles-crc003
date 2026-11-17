# Historial de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [0.1.0] - 2026-11-17

### Cambiado
- La base de sismos significativos de NOAA/NCEI se versiona en `data/noaa_sismos_significativos_colombia-2026-11-16.csv` (83 eventos) y el cuaderno la lee de ahí en lugar de consultar la API. Licencia: dominio público/CC0 según la política de NCEI; los metadatos del conjunto indican acceso sin restricciones (revisado el 2026-11-17).

### Agregado
- `MODEL_CARD.md` (Estándar de modelos); `DATA_STATEMENT.md`, la ficha, el diccionario, `AI_USE.md` y este historial como documentos de apoyo del sitio.
- Identificadores y fechas de las fuentes en `metadata/sources.csv`.
- RDLS del catálogo del USGS: la licencia usa el código CC0 de la lista del esquema (dominio público de EE. UU.) en lugar de texto libre.
- Cuaderno de sismicidad de Colombia (2026-11-16): descarga del catálogo del USGS, completitud, Gutenberg-Richter, profundidad focal, estacionalidad, mapas, animación, cortes transversales, vista 3D y ficha departamental de Córdoba.
- `data/` con los dos catálogos del USGS fijados al 2026-11-16 y `scripts/descargar_catalogo.py`.
- Carpeta `metadata/`: `sources.csv`, `data_catalog.csv`, `DATA_DICTIONARY.md`, `descargas.csv` y 2 archivos RDLS 1.0.0.
- `LICENSE`, `README.md`, `DATA_STATEMENT.md`, `CITATION.cff`, `AI_USE.md`, `scripts/registrar_descargas.py` y `scripts/generar_banner.py`.

### Cambiado
- La fecha de corte de las consultas al USGS es fija (2026-11-16); antes era la fecha de ejecución y cada ejecución devolvía un catálogo distinto.
- Natural Earth se lee de un commit fijo (`9380cca`) y no de la rama `master`.
- `images/banner.png` se genera con `scripts/generar_banner.py` desde el catálogo real. La imagen anterior no se generaba en el repositorio y no reproducía la sismicidad del catálogo.

### Pendiente
- Ninguno de DOI: la versión 0.1.0 está archivada en Zenodo (`10.5281/zenodo.24322598`).
- Confirmar la licencia de la base de sismos de NOAA/NCEI, aplicar la prueba CARE y archivar un *release* en Zenodo.
