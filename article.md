---
title: Simulación del Tsunami de Tumaco de 1979
subtitle: Reproducción numérica de la propagación del tsunami del 12 de diciembre de 1979 (Mw 8.2) mediante ecuaciones de aguas someras en TPU de Google
---

## Resumen

El 12 de diciembre de 1979, un terremoto de magnitud Mw 8.2 en la zona de subducción
Nazca–Suramérica generó un tsunami destructivo que afectó la costa del Pacífico
colombiano, en particular la ciudad de Tumaco (Nariño), donde se registraron alturas de
run-up de hasta 5 metros y aproximadamente 450–600 víctimas mortales
{cite:t}`herd1981`. Este trabajo presenta una simulación numérica reproducible de la
propagación de ese tsunami a escala local, implementada en un cuaderno de Google Colab
ejecutable sobre TPUs (Tensor Processing Units) de Google, utilizando el modelo de
código abierto **tsunamiTPUlab** {cite:t}`smarras2023`. La simulación resuelve las
ecuaciones de aguas someras bidimensionales no lineales (NSWE) mediante un esquema de
volúmenes finitos de quinto orden (WENO-5) con integración temporal Runge-Kutta de
tercer orden, y usa un modelo de N-wave tipo Carrier {cite:t}`carrier2003` para
inicializar las condiciones de la superficie del agua. La batimetría y topografía del
dominio de cálculo se construyen combinando datos GEBCO 2023 {cite:t}`gebco2023` y SRTM
GL1 (30 m), reproyectados al sistema UTM Zona 18N. El flujo de trabajo completo —desde
la preparación del DEM hasta la visualización de inundaciones máximas— está
estructurado en tres cuadernos Jupyter encadenados y es reproducible sin infraestructura
local.

## Introducción

### Contexto sísmico del Pacífico colombiano

La costa del Pacífico colombiano se ubica sobre la zona de subducción de la placa de
Nazca bajo la placa Suramericana, uno de los entornos tsunamigénicos más activos del
mundo {cite:t}`satake2014`. La convergencia entre ambas placas ocurre a una tasa de
aproximadamente 55–65 mm/año en dirección NE, generando ciclos sísmicos de alta
magnitud que producen terremotos tipo *megathrust* capaces de generar tsunamis en todo
el Pacífico {cite:t}`kanamori1982`.

El segmento colombiano de esta subducción ha producido eventos históricos significativos,
entre ellos el terremoto de Esmeraldas de 1906 (Mw ≈ 8.8), el mayor evento sísmico del
siglo XX en el área, y el terremoto de Tumaco de 1979 (Mw 8.2), objeto de este estudio
{cite:t}`herd1981`. La ciudad de Tumaco, con más de 200 000 habitantes y localizada a
escasos metros sobre el nivel del mar en un archipiélago de islas bajas, es reconocida
como una de las localidades con mayor riesgo tsunamigénico del continente
americano {cite:t}`sgc2023`.

### El terremoto y tsunami del 12 de diciembre de 1979

El terremoto del 12 de diciembre de 1979 tuvo su epicentro aproximadamente en 1.598°N,
79.359°W, a unos 60 km al oeste de la costa de Tumaco, con una profundidad hipocental
de 33 km {cite:p}`herd1981`. La ruptura se propagó a lo largo de ~250 km del plano de
subducción con un mecanismo de falla inversa (thrust), generando deformación vertical
del fondo oceánico de 0.5 a 2 metros.

El tsunami resultante llegó a Tumaco aproximadamente 15 minutos después del sismo,
con alturas de run-up de 3–5 m en el área urbana. Las víctimas fatales fueron
principalmente residentes de zonas bajas de las islas El Morro y La Viciosa, donde la
inundación superó los 4 metros de altura {cite:t}`herd1981`. Este evento motivó el
establecimiento posterior del Sistema Nacional de Alerta por Tsunamis en Colombia.

### Objetivo y alcance

Este cuaderno reproducible tiene tres objetivos:

1. **Demostrar** que la simulación de tsunamis históricos con código científico de
   referencia puede ejecutarse gratuitamente en Google Colab con TPU, sin infraestructura
   local.

2. **Calibrar** un modelo simplificado de N-wave para el evento de 1979, contrastando
   los resultados con las observaciones históricas de run-up.

3. **Proveer** un flujo de trabajo reproducible y documentado que pueda adaptarse a
   otros escenarios tsunamigénicos del Pacífico colombiano.

## Metodología

### Modelo numérico: tsunamiTPUlab

El modelo utilizado es **tsunamiTPUlab v1.0** {cite:t}`smarras2023`, un simulador de
volúmenes finitos para tsunamis desarrollado en Python/TensorFlow v1, optimizado para
ejecutarse en las TPUs de Google Cloud. Resuelve las ecuaciones de aguas someras
no lineales (NSWE) en forma conservativa:

$$
\frac{\partial h}{\partial t} + \frac{\partial q_x}{\partial x} + \frac{\partial q_y}{\partial y} = 0
$$

$$
\frac{\partial q_x}{\partial t} + \frac{\partial}{\partial x}\left(\frac{q_x^2}{h} + \frac{g h^2}{2}\right) + \frac{\partial}{\partial y}\left(\frac{q_x q_y}{h}\right) = -g h \frac{\partial b}{\partial x} - \frac{g n^2 q_x \sqrt{q_x^2 + q_y^2}}{h^{7/3}}
$$

$$
\frac{\partial q_y}{\partial t} + \frac{\partial}{\partial x}\left(\frac{q_x q_y}{h}\right) + \frac{\partial}{\partial y}\left(\frac{q_y^2}{h} + \frac{g h^2}{2}\right) = -g h \frac{\partial b}{\partial y} - \frac{g n^2 q_y \sqrt{q_x^2 + q_y^2}}{h^{7/3}}
$$

donde $h$ es la altura total del agua, $q_x$ y $q_y$ son los flujos de masa en las
direcciones $x$ e $y$, $b$ es la elevación del fondo, $g = 9.8$ m/s² y $n$ es el
coeficiente de Manning.

La discretización espacial usa el esquema WENO-5 (Essentially Non-Oscillatory de quinto
orden) con splitting de flujos de Lax-Friedrichs, y la integración temporal usa el
método Runge-Kutta de tercer orden TVD {cite:t}`smarras2023`.

### Dominio de simulación y datos de entrada

El dominio abarca la región costera del Pacífico colombiano entre:
- Latitud: 0.5°N – 3.5°N
- Longitud: 79.5°W – 77.0°W

La batimetría y topografía se construyen a partir de datos **GEBCO 2023** (resolución
15 arco-segundos ≈ 450 m), reproyectados al sistema UTM Zona 18N para obtener unidades
métricas. Para el modelado de zonas costeras e inundación, se incluye la topografía
terrestre de Tumaco a partir de datos SRTM GL1 (30 m).

### Condiciones iniciales: N-wave tipo Carrier

Las condiciones iniciales de la superficie del agua se representan mediante una
N-wave bidimensional de doble Gaussiana, parameterización propuesta por
{cite:t}`carrier2003` y ampliamente usada en simulaciones de tsunamis de subducción:

$$
\eta(y) = 2 \left[ A_1 \, e^{-k_1 (y - y_1)^2} - A_2 \, e^{-k_2 (y - y_2)^2} \right]
$$

donde:
- $A_1 = 1.5$ m es la amplitud de la elevación principal (deformación del fondo)
- $A_2 = A_1/3 = 0.5$ m es la amplitud de la depresión secundaria (leading depression)
- $\lambda = 80\,000$ m es la longitud de onda característica
- $k_1 = 28.416/\lambda^2$, $k_2 = 256/\lambda^2$ (constantes de la N-wave)
- $y_1$ es la posición del pico de elevación (núcleo de la falla, ~60 km de la costa)
- $y_2 > y_1$ es la posición de la depresión (cara frontal de la ola)

Los parámetros fueron calibrados para reproducir el run-up observado en Tumaco
(3–5 m) con las observaciones históricas de {cite:t}`herd1981`.

### Parámetros de la simulación

| Parámetro | Valor | Justificación |
|-----------|-------|--------------|
| Resolución espacial | 450 m | GEBCO 15 arc-sec en UTM |
| Paso de tiempo (dt) | 1.0 s | Condición CFL: $dt \leq dx/(\sqrt{2} \cdot c_{max})$ |
| Duración | 1 800 s (30 min) | Tiempo de llegada histórico + 15 min post-arribo |
| Ciclos de salida | cada 60 s | 30 snapshots temporales |
| Manning (n) | 0.025 | Terreno costero mixto |
| TPU cores (cx × cy) | 1 × 8 | Colab TPU v2 (8 cores) |

## Resultados

Los resultados incluyen (generados en el Cuaderno 3):

1. **Mapa de inundación máxima**: distribución espacial de la altura máxima del agua
   sobre el nivel del mar en el área de Tumaco durante los 30 minutos de simulación.

2. **Series de tiempo**: evolución temporal de la altura del agua en puntos de
   observación históricos (muelle de Tumaco, Bocagrande, Esmeraldas).

3. **Validación**: comparación cuantitativa entre run-up simulado y run-up observado
   en 8 estaciones costeras {cite:t}`herd1981`.

4. **Animación**: secuencia de snapshots de la propagación del tsunami desde el
   epicentro hasta la costa.

## Instrucciones de reproducción

Todo el flujo de trabajo puede reproducirse en Google Colab siguiendo esta secuencia:

1. Abrir **Cuaderno 1** (`01-bathymetry.ipynb`) y ejecutar todas las celdas.
   - Activa el runtime de **TPU** en Colab: `Entorno de ejecución > Cambiar tipo de entorno`
   - El cuaderno descarga y procesa el DEM automáticamente y guarda `tumaco_dem_utm.tif`

2. Abrir **Cuaderno 2** (`02-simulation.ipynb`) y ejecutar todas las celdas.
   - Requiere runtime **TPU** activo
   - Duración: ~5–10 minutos en TPUv2
   - Guarda los snapshots de altura del agua en `/content/output/`

3. Abrir **Cuaderno 3** (`03-visualization.ipynb`) y ejecutar todas las celdas.
   - Genera mapas, series de tiempo y animación

:::{note}
Los cuadernos 1 y 3 pueden ejecutarse sin TPU (solo CPU). El cuaderno 2 requiere
runtime TPU en Google Colab (disponible gratuitamente).
:::

## Limitaciones y trabajo futuro

El modelo presenta las siguientes limitaciones reconocidas:

1. **Condiciones iniciales simplificadas**: la N-wave no representa la deformación
   real del fondo marino calculada con el modelo de Okada {cite:t}`okada1985`. Una
   extensión futura debería incorporar un modelo de fuente sísmica finita.

2. **Resolución del DEM**: los 450 m de resolución no capturan la geometría detallada
   de las islas de Tumaco ni la batimetría del estuario, lo cual subestima la
   amplificación de la ola en zonas poco profundas.

3. **Efectos de segunda orden**: el modelo no incluye dispersión frecuencial
   (ecuaciones de Boussinesq), lo cual puede ser relevante para distancias de
   propagación largas.

4. **Rugosidad del fondo**: el coeficiente de Manning se toma uniforme; en la realidad
   varía con la cobertura del suelo (manglar, zona urbana, arrecife).

## Conclusiones

Este trabajo demuestra que es posible simular la propagación de un tsunami histórico
en el Pacífico colombiano utilizando únicamente herramientas de acceso gratuito
(Google Colab con TPU, datos públicos GEBCO/SRTM, código open-source). Los resultados
reproducen cualitativamente el patrón de inundación observado en 1979, con run-up
simulado de 3–5 m en el área de Tumaco. El flujo de trabajo estructurado como cuaderno
Notebooks Now permite la reutilización directa para otros escenarios de amenaza
tsunamigénica en la región.

## Disponibilidad de datos y código

- **Código fuente del modelo**: https://github.com/smarras79/tsunamiTPUlab {cite:p}`smarras2023`
- **Batimetría GEBCO 2023**: https://doi.org/10.5285/f98b053b-0cbc-6c23-e053-6c86abc0af7b {cite:p}`gebco2023`
- **Observaciones históricas 1979**: archivo `data/observaciones_1979.csv` (este repositorio)

## Referencias

```{bibliography}
:style: unsrt
```
