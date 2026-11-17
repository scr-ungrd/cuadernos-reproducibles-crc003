# Historial de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## Sin publicar (0.1.0)

### Agregado
- Cuaderno de sismicidad de Colombia (2026-11-16): descarga del catálogo del USGS, completitud, Gutenberg-Richter, profundidad focal, estacionalidad, mapas, animación, cortes transversales, vista 3D y ficha departamental de Córdoba.
- `data/` con los dos catálogos del USGS fijados al 2026-11-16 y `scripts/descargar_catalogo.py`.
- Carpeta `metadata/`: `sources.csv`, `data_catalog.csv`, `DATA_DICTIONARY.md`, `descargas.csv` y 2 archivos RDLS 1.0.0.
- `LICENSE`, `README.md`, `DATA_STATEMENT.md`, `CITATION.cff`, `AI_USE.md`, `scripts/registrar_descargas.py` y `scripts/generar_banner.py`.

### Cambiado
- La fecha de corte de las consultas al USGS es fija (2026-11-16); antes era la fecha de ejecución y cada ejecución devolvía un catálogo distinto.
- Natural Earth se lee de un commit fijo (`9380cca`) y no de la rama `master`.
- `images/banner.png` se genera con `scripts/generar_banner.py` desde el catálogo real. La imagen anterior no se generaba en el repositorio y no reproducía la sismicidad del catálogo.

### Pendiente
- Confirmar la licencia de la base de sismos de NOAA/NCEI, aplicar la prueba CARE y archivar un *release* en Zenodo.
