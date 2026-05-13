---
title: Simulación del Tsunami de Tumaco de 1979
subtitle: Reproducción numérica de la propagación del tsunami del 12 de diciembre de 1979 (Mw 8.2) mediante ecuaciones de aguas someras linealizadas en Google Colab
---

**Cuaderno 3 — Visualización y validación:**
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/scr-ungrd/cuadernos-reproducibles-crc003/blob/main/notebooks/03-visualization.ipynb)
[![Abrir en Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc003/main?filepath=notebooks/03-visualization.ipynb)

---

## Resumen

El 12 de diciembre de 1979, un terremoto de magnitud Mw 8.2 en la zona de subducción
Nazca–Suramérica generó un tsunami destructivo que afectó la costa del Pacífico
colombiano, en particular la ciudad de Tumaco (Nariño), donde se registraron alturas de
run-up de hasta 5 metros y aproximadamente 450–600 víctimas mortales
{cite:t}`herd1981`. Este trabajo presenta una simulación numérica reproducible de la
propagación de ese tsunami a escala regional, implementada en tres cuadernos de Google
Colab ejecutables en CPU estándar sin infraestructura local. La simulación resuelve las
ecuaciones de aguas someras linealizadas (LSWE) bidimensionales mediante un esquema de
Lax-Friedrichs, y usa un modelo de N-wave tipo Carrier {cite:t}`carrier2003` para
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
   referencia puede ejecutarse gratuitamente en Google Colab en CPU, sin infraestructura
   local.

2. **Calibrar** un modelo simplificado de N-wave para el evento de 1979, contrastando
   los resultados con las observaciones históricas de run-up.

3. **Proveer** un flujo de trabajo reproducible y documentado que pueda adaptarse a
   otros escenarios tsunamigénicos del Pacífico colombiano.

## Metodología

### Modelo numérico: LSWE con Lax-Friedrichs

El modelo utilizado resuelve las **ecuaciones de aguas someras linealizadas** (LSWE,
*Linearized Shallow Water Equations*) en forma bidimensional. A diferencia de las NSWE
no lineales, la linealización en torno a la profundidad en reposo $H_0(\mathbf{x})$
permite un esquema bien-balanceado por construcción: el estado de reposo
($\eta = 0$, $u = v = 0$) es solución estacionaria exacta para cualquier fondo
batimétrico. Las ecuaciones son:

$$
\frac{\partial \eta}{\partial t} + \frac{\partial (H_0 u)}{\partial x} + \frac{\partial (H_0 v)}{\partial y} = 0
$$

$$
\frac{\partial u}{\partial t} + g \frac{\partial \eta}{\partial x} = -\frac{g n^2 |\mathbf{u}|}{H_0^{4/3}} u
$$

$$
\frac{\partial v}{\partial t} + g \frac{\partial \eta}{\partial y} = -\frac{g n^2 |\mathbf{u}|}{H_0^{4/3}} v
$$

donde $\eta$ es la perturbación de la superficie libre respecto al nivel de reposo,
$u$ y $v$ son las velocidades horizontales promediadas en la vertical, $H_0$ es la
profundidad en reposo (fija durante la simulación), $g = 9.81$ m/s² y $n$ es el
coeficiente de Manning.

La discretización espacial utiliza el esquema de **Lax-Friedrichs 2D**: cada celda
interior se actualiza como el promedio de sus cuatro vecinos (norte, sur, este, oeste)
menos la divergencia del flujo centrada en el tiempo. Las celdas terrestres ($H_0 = 0$)
actúan como paredes rígidas sin intercambio de masa o momento. La condición de borde
exterior es de tipo Neumann (gradiente nulo). El solver está implementado en
**NumPy puro** y se ejecuta en CPU estándar de Google Colab sin dependencias especiales.

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
N-wave bidimensional de doble Gaussiana, parametrización propuesta por
{cite:t}`carrier2003` y ampliamente usada en simulaciones de tsunamis de subducción:

$$
\eta(y) = 2 \left[ A_1 \, e^{-k_1 (y - y_1)^2} - A_2 \, e^{-k_2 (y - y_2)^2} \right]
$$

donde:
- $A_1 = 8.0$ m es la amplitud de calibración de la elevación principal
- $A_2 = A_1/3 \approx 2.67$ m es la amplitud de la depresión secundaria (*leading depression*)
- $\lambda = 80\,000$ m es la longitud de onda característica
- $k_1 = 28.416/\lambda^2$, $k_2 = 256/\lambda^2$ (constantes de la N-wave)
- $y_1$ es la posición del pico de elevación (núcleo de la falla, ~60 km de la costa)
- $y_2 > y_1$ es la posición de la depresión (cara frontal de la ola)

El valor $A_1 = 8.0$ m es un parámetro de calibración: la difusión numérica del
esquema Lax-Friedrichs atenúa la ola aproximadamente 4× durante los ~60 km de
propagación hasta la costa, de modo que la amplitud costero-simulada alcanza los
3–5 m observados por {cite:t}`herd1981`.

### Parámetros de la simulación

| Parámetro | Valor | Justificación |
|-----------|-------|--------------|
| Resolución espacial | 450 m | GEBCO 15 arc-sec en UTM |
| Paso de tiempo (dt) | 1.0 s | Condición CFL: $CFL = c_{max} \cdot dt \cdot \sqrt{2}/dx \approx 0.62 < 1$ |
| Duración | 1 800 s (30 min) | Tiempo de llegada histórico + 15 min post-arribo |
| Ciclos de salida | cada 60 s | 31 snapshots temporales |
| Manning (n) | 0.025 | Terreno costero mixto |
| Plataforma | Google Colab CPU | Sin requisito de TPU/GPU |
| Tiempo de ejecución | ~65 s | CPU estándar de Colab |

## Resultados

### Elevación máxima de la ola

La {numref}`fig-max-eta` muestra la distribución espacial de la elevación máxima
de la superficie marina (η) durante los 30 minutos de simulación. Los valores más
altos se concentran en la zona costera norte del dominio, frente a Tumaco y Bocagrande,
con amplitudes de hasta 3–4 m en aguas someras (profundidad < 200 m), coherentes
con las observaciones de {cite:t}`herd1981`.

:::{figure} notebooks/max_inundation_map.png
:label: fig-max-eta
:alt: Elevación máxima de la ola y amplitud costera
Panel izquierdo: elevación máxima de la superficie marina (η) durante 30 min de
simulación LSWE. Panel derecho: amplitud máxima en zona costera (profundidad < 200 m).
La estrella roja indica el epicentro del sismo del 12 de diciembre de 1979.
:::

### Series de tiempo

La {numref}`fig-timeseries` muestra la evolución temporal de η en cuatro estaciones
históricas. La ola llega a Tumaco (muelle) aproximadamente a los 15 minutos del sismo,
coincidiendo con el tiempo de arribo reportado por {cite:t}`herd1981`.

:::{figure} notebooks/time_series.png
:label: fig-timeseries
:alt: Series de tiempo en estaciones de observación históricas
Series de tiempo de la elevación de la superficie del agua (η) en cuatro estaciones
históricas. Las líneas discontinuas horizontales indican el run-up observado
{cite:p}`herd1981`; las líneas discontinuas verticales marcan el tiempo de arribo observado.
:::

### Validación cuantitativa

La {numref}`fig-validation` compara el run-up simulado con el observado en 8 estaciones
costeras. La correlación entre valores simulados y observados es cualitativamente
consistente, con sesgo positivo esperable dado el carácter calibrado del parámetro
$A_1 = 8.0$ m de la N-wave.

:::{figure} notebooks/validation.png
:label: fig-validation
:alt: Validación cuantitativa del modelo
Comparación entre run-up simulado y observado en estaciones costeras de
{cite:t}`herd1981`. Izquierda: diagrama de dispersión con línea 1:1.
Derecha: barras comparativas por estación.
:::

### Animación de la propagación

La {numref}`fig-animation` ilustra la propagación del tsunami desde el epicentro
hasta la costa colombiana durante los primeros 30 minutos. La ola avanza de oeste
a este a una velocidad de celeridad característica $c = \sqrt{gH_0}$ ≈ 200 m/s
en aguas de 4 000 m de profundidad, llegando a la costa en ~15 minutos.

:::{figure} notebooks/tsunami_propagation.gif
:label: fig-animation
:alt: Animación de la propagación del tsunami
Animación de la propagación del tsunami de Tumaco 1979 (solver LSWE, 31 frames,
t = 0–30 min). La escala de color muestra η en metros; la estrella roja indica
el epicentro.
:::

## Instrucciones de reproducción

Todo el flujo de trabajo puede reproducirse en Google Colab siguiendo esta secuencia:

1. Abrir **Cuaderno 1** (`01-bathymetry.ipynb`) y ejecutar todas las celdas.
   - Runtime de **CPU** (no requiere TPU ni GPU)
   - El cuaderno descarga y procesa el DEM automáticamente y guarda `tumaco_dem_utm.tif`

2. Abrir **Cuaderno 2** (`02-simulation.ipynb`) y ejecutar todas las celdas.
   - Runtime de **CPU** (no requiere TPU ni GPU)
   - Duración: ~1–2 minutos en CPU de Colab
   - Guarda los snapshots de altura del agua en `/content/output_1979/`

3. Abrir **Cuaderno 3** (`03-visualization.ipynb`) y ejecutar todas las celdas.
   - Genera mapas, series de tiempo y animación

:::{note}
Los tres cuadernos funcionan en CPU estándar de Google Colab (runtime predeterminado).
No se requiere cambiar el tipo de entorno de ejecución.
:::

## Limitaciones y trabajo futuro

El modelo presenta las siguientes limitaciones reconocidas:

1. **Linealización**: las LSWE no capturan efectos no lineales como el apilamiento de
   la ola en aguas muy someras (*shoaling* no lineal) ni la inundación (*run-up*) real.
   Una extensión futura debería usar las ecuaciones de Saint-Venant no lineales (NSWE)
   con tratamiento de celda seca.

2. **Difusión numérica**: el esquema Lax-Friedrichs es de primer orden y difusivo; la
   amplitud de calibración ($A_1 = 8.0$ m) compensa esta atenuación pero no representa
   el desplazamiento físico real del fondo (~1–2 m). Un esquema de orden superior (WENO,
   MacCormack) reduciría esta discrepancia.

3. **Condiciones iniciales simplificadas**: la N-wave no representa la deformación
   real del fondo marino calculada con el modelo de Okada {cite:t}`okada1985`. Una
   extensión futura debería incorporar un modelo de fuente sísmica finita.

4. **Resolución del DEM**: los 450 m de resolución no capturan la geometría detallada
   de las islas de Tumaco ni la batimetría del estuario, lo cual subestima la
   amplificación de la ola en zonas poco profundas.

5. **Rugosidad del fondo**: el coeficiente de Manning se toma uniforme; en la realidad
   varía con la cobertura del suelo (manglar, zona urbana, arrecife).

## Conclusiones

Este trabajo demuestra que es posible simular la propagación de un tsunami histórico
en el Pacífico colombiano utilizando únicamente herramientas de acceso gratuito
(Google Colab en CPU, datos públicos GEBCO/SRTM, NumPy). Los resultados reproducen
cualitativamente el patrón de inundación observado en 1979, con run-up simulado de
3–5 m en el área de Tumaco. El flujo de trabajo estructurado como cuaderno Notebooks
Now permite la reutilización directa para otros escenarios de amenaza tsunamigénica
en la región.

## Disponibilidad de datos y código

- **Batimetría GEBCO 2023**: https://doi.org/10.5285/f98b053b-0cbc-6c23-e053-6c86abc0af7b {cite:p}`gebco2023`
- **Observaciones históricas 1979**: archivo `data/observaciones_1979.csv` (este repositorio)

```{bibliography}
```
