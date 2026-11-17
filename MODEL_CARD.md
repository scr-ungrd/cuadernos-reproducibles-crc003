# Ficha del modelo: análisis de sismicidad de Colombia

Conforme al «Estándar de modelos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-modelos>). El cuaderno no entrena un modelo predictivo: ajusta un modelo estadístico, la relación de Gutenberg-Richter, y describe el catálogo.

## 1. Propósito y uso previsto

- **Modelo:** relación frecuencia-magnitud de Gutenberg-Richter, con la magnitud de completitud (Mc) por el método del máximo de curvatura y el parámetro *b* por máxima verosimilitud de Aki-Utsu (con regresión sobre la curva acumulada como contraste).
- **Versión:** 0.1.0 (2026-11-16). **Autoría:** Subdirección para el Conocimiento del Riesgo, UNGRD. **Licencia:** código MIT; texto y figuras CC BY 4.0.
- **Uso previsto:** caracterizar la sismicidad catalogada de Colombia y su área de influencia con fines educativos y de método (por qué un modelo estadístico: el catálogo es una muestra de eventos y no hay una física simple que la describa).
- **Usos no previstos:** estimar amenaza sísmica o riesgo (no incluye exposición ni vulnerabilidad ni amenaza dependiente del tiempo), reemplazar el catálogo del Servicio Geológico Colombiano y tomar decisiones de gestión.
- **Límites de validez:** caja de búsqueda de −5° a 13° N y −82° a −65° O (catálogo base) y de −5° a 16° N y −84° a −66° O (ampliado); incluye países vecinos; completo desde M ≈ 4,5.
- **Revisión previa a una decisión:** una persona experta en sismología. <confirmar quién>

## 2. Datos del modelo

- Catálogos del USGS (ComCat) descargados el 2026-11-16: 4 769 eventos (M ≥ 3,0, 2000–2026) y 11 085 (M ≥ 2,5, 1900–2026). Dominio público; `data/` y `metadata/sources.csv`.
- Complementos (solo descriptivos): Global Significant Earthquake Database de NOAA/NCEI (licencia por confirmar, no se copia), geoBoundaries (ODbL 1.0) y Natural Earth (dominio público).
- **Hoja de datos:** `metadata/DATA_DICTIONARY.md` y `DATA_STATEMENT.md`. Sin datos personales.
- **Etiquetas y calidad:** las magnitudes mezclan tipos (Mw, mb, Ml, Ms) sin homogeneizar; muchas profundidades antiguas son valores fijos asignados por la agencia; las magnitudes históricas se derivan de intensidades.
- Los datos no se parten en entrenamiento y prueba: el modelo es una estimación sobre todo el catálogo por encima de Mc. No hay datos sintéticos.
- Eventos raros: los de gran magnitud son pocos y el ajuste de *b* depende de la ventana de magnitud; el cuaderno lo discute.

## 3. Descripción del método

- Mc por máximo de curvatura (histograma de magnitudes); *b* por Aki-Utsu con su error estándar; regresión sobre la curva acumulada como contraste (sesgada).
- Resultado del catálogo base: Mc = 4,5 (2 042 eventos con M ≥ Mc), *b* = 1,07 ± 0,02.
- Sin hiperparámetros ajustados con datos de prueba. Sin modelos ni pesos de terceros.
- No hay pesos que guardar; los resultados son tablas, figuras y una ficha departamental (`ficha_sismica_cordoba.json`).

## 4. Validación y desempeño

- **No se validó con datos independientes** ni se comparó con una línea base ni con el método vigente del SGC. La estimación de Mc se contrasta con la curva de completitud en el tiempo (sección 12.2 del cuaderno).
- Métricas: error estándar de *b*. No hay desglose por región ni por periodo salvo la ficha de Córdoba (piloto).
- Casos de fallo conocidos: sismicidad cortical mal representada en cortes a escala de país; tipos de magnitud mezclados; conversión plana de grados a kilómetros.
- La revisión de una persona experta del dominio no se ha hecho.

## 5. Incertidumbre y sensibilidad

- Fuentes: completitud del catálogo (Mc), mezcla de tipos de magnitud, profundidades asignadas y la ventana temporal.
- Se reporta el error estándar de *b* y la diferencia entre el estimador por máxima verosimilitud (1,07) y la regresión (0,86). No hay un análisis de sensibilidad formal a Mc ni a la ventana.
- Los resultados no se entregan como probabilidades.

## 6. Reproducibilidad

- Entorno: `environment.yml`. La fecha de corte de las consultas al USGS es fija (2026-11-16) y los catálogos están en `data/` con SHA-256 en `metadata/descargas.csv`. El USGS puede revisar eventos pasados, por lo que una descarga nueva puede diferir.
- No hay aleatoriedad ni semillas. No hay registro de experimentos ni pruebas automáticas.
- Hardware: CPU estándar. <confirmar tiempo de ejecución>

## 7. Riesgos, sesgos y uso responsable

- **No hacer daño:** una *b* o una ficha departamental podrían leerse como probabilidad de sismos. El cuaderno declara que describe amenaza catalogada, no riesgo.
- **Sesgos:** cobertura desigual de estaciones y detección en el tiempo (el crecimiento aparente de eventos es de instrumentación); la caja incluye países vecinos.
- **Comunidades:** el análisis departamental usa límites administrativos y no datos de comunidades. <confirmar si los territorios étnicos exigen consulta>
- **Explicabilidad:** el método es estadístico y está descrito con sus ecuaciones en el cuaderno.

## 8. Documentación y ciclo de vida

- `README.md`, `CHANGELOG.md`, `CITATION.cff`, `DATA_STATEMENT.md` y `AI_USE.md`.
- **Obsolescencia:** el análisis se rehace cuando se actualice el catálogo o cuando se integre el Catálogo Sísmico Integrado del SGC. <confirmar quién decide>
- Uso de IA declarado en `AI_USE.md`. No se publica en un repositorio de modelos.
