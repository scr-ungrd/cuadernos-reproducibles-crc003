# Declaración de disponibilidad de datos y de código

Cuaderno CRC003: análisis de sismicidad de Colombia con el catálogo del USGS. Conforme al «Estándar de datos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-de-datos>).

## Datos de entrada

Las cinco fuentes, con su dirección exacta, consulta, licencia y restricciones, están en [`metadata/sources.csv`](metadata/sources.csv). Todas se obtienen sin credenciales y sin pago.

- **Catálogo de sismos del USGS (ComCat):** dominio público de EE. UU.; reconocer al USGS. Dos consultas con fecha de corte fija del 2026-11-16, que reproducen `scripts/descargar_catalogo.py` y están en `data/`: el catálogo base (4 769 eventos, M ≥ 3,0 desde 2000) y el ampliado (11 085 terremotos, M ≥ 2,5 desde 1900). Coinciden con las salidas guardadas del cuaderno. El USGS puede revisar eventos pasados; las sumas de verificación están en [`metadata/descargas.csv`](metadata/descargas.csv).
- **Global Significant Earthquake Database (NOAA/NCEI,** `10.7289/V5TD9V7K`**):** 83 sismos significativos de Colombia por la API de Hazel. **La licencia está por confirmar**, por lo que no se copia al repositorio; el cuaderno la consulta en vivo.
- **geoBoundaries gbOpen, Colombia ADM1:** ODbL 1.0, fijado al commit `9469f09`. Los productos derivados que lo incorporan reconocen la fuente (OpenStreetMap).
- **Natural Earth, países 1:50 millones:** dominio público, fijado al commit `9380cca`.

## Datos derivados publicados

Los 18 archivos publicados (catálogos, ficha departamental, figuras, mapas y animación) están descritos en [`metadata/data_catalog.csv`](metadata/data_catalog.csv) y sus variables en [`metadata/DATA_DICTIONARY.md`](metadata/DATA_DICTIONARY.md). Los metadatos RDLS 1.0.0 están en [`metadata/rdls/`](metadata/rdls/).

| Datos | Licencia |
|---|---|
| Catálogos del USGS (`data/`) | Dominio público (USGS) |
| Ficha, figuras, mapas y animación | CC BY 4.0, con reconocimiento al USGS y a geoBoundaries/OpenStreetMap |

La licencia de los productos que incorporan límites de geoBoundaries (ODbL 1.0) debe revisarse. <confirmar con asesoría jurídica>

## Datos con acceso restringido

Ninguno.

## Revisión CARE

- Los datos son sismos y límites administrativos; no contienen datos personales. La base de NOAA/NCEI aporta el número de víctimas por evento, sin identificación individual.
- El análisis departamental usa límites administrativos y no datos de comunidades. ¿Los territorios étnicos de Córdoba o de otros departamentos exigen consulta antes de publicar fichas? <confirmar>.

## Disponibilidad de código

- Repositorio: <https://github.com/scr-ungrd/cuadernos-reproducibles-crc003>. Licencia MIT.
- Versión: 0.1.0 (2026-11-16). Sin DOI: falta archivar un *release* en Zenodo.
- Ficha del modelo: [`MODEL_CARD.md`](MODEL_CARD.md), conforme al Estándar de modelos.
- Software: [`environment.yml`](environment.yml).

## Validación técnica y limitaciones

- Comprobaciones: magnitud de completitud, relación de Gutenberg-Richter por máxima verosimilitud y completitud del catálogo en el tiempo.
- Limitaciones: sección 17.1 del cuaderno (mezcla de tipos de magnitud, profundidades fijas, completitud desde M≈4,5 y caja de búsqueda que incluye países vecinos).
- El cuaderno es un ejercicio sin validar por una persona experta; no debe usarse para tomar decisiones.

## Compromiso de preservación

- Responsable: Subdirección para el Conocimiento del Riesgo, UNGRD (conocimiento@gestiondelriesgo.gov.co).
- Los datos se conservarán al menos cinco años después de la publicación. <confirmar el compromiso institucional>
