---
title: Simulación del tsunami de Tumaco de 1979 [Versión 2, validación indicativa]
subtitle: Propagación del tsunami del 12 de diciembre de 1979 (Mw 8,3) con una fuente de Okada y aguas someras lineales en Google Colab
---

**Cuaderno 3 — Visualización y comparación con 1979:**

+++ {"no-pdf": true}

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/scr-ungrd/cuadernos-reproducibles-crc003/blob/main/notebooks/03-visualization.ipynb)
[![Abrir en Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc003/main?filepath=notebooks/03-visualization.ipynb)

+++

---

## Resumen

El 12 de diciembre de 1979 un terremoto de la zona de subducción colombo-ecuatoriana generó un tsunami que causó cerca de 452 muertes en Nariño {cite:p}`escobar2020tsunami`.
Este trabajo presenta una simulación reproducible de su propagación en tres cuadernos de Google Colab que corren en CPU. La versión 2 reemplaza la onda en N calibrada de la versión 1 por la
deformación del fondo de una falla rectangular calculada con el modelo de Okada {cite:p}`okada1985` (Mw 8,3; geometría supuesta), y reemplaza el esquema de Lax-Friedrichs por una malla
escalonada que no añade difusión numérica. La simulación cubre 60 minutos sobre un dominio de unos 480 × 480 km y 450 m de resolución. **Los tiempos de arribo son poco sensibles a la resolución y a los
parámetros de la falla (±3 min) y coinciden en orden de magnitud con los 22 min que modela TUNAMI-N2 para Tumaco {cite:p}`avila2026`; las amplitudes, en cambio, dependen mucho de la fuente (4 a 9 m en Tumaco
según el caso) y el modelo lineal las sobreestima respecto a los 1,9–2,3 m publicados para la isla {cite:p}`escobar2020tsunami`.** El producto es un flujo de trabajo y una lectura de sus límites, no un mapa de amenaza.

## Introducción

### Contexto sísmico del Pacífico colombiano

La costa Pacífica colombiana está expuesta a fuentes cercanas en la zona de subducción de la placa de Nazca bajo la suramericana. En el siglo XX esa zona produjo cuatro terremotos
de Mw > 7,7, en 1906, 1942, 1958 y 1979; el mayor fue el del 31 de enero de 1906 (Mw > 8,4), y todos generaron tsunamis con daños y pérdida de vidas en la costa de Colombia y Ecuador {cite:p}`escobar2020tsunami`.
Los eventos de 1906 y 1979 fueron desastres, el segundo grave para Tumaco {cite:p}`ungrd2019atlas`. Tumaco es además el municipio con mayor población expuesta y probabilidad de pérdidas por tsunami
del país {cite:p}`ungrd2019atlas`.

### El evento del 12 de diciembre de 1979

El sismo de 1979 se estima en Mw 8,3 (Yoshimoto et al., 2017, citado por {cite:t}`escobar2020tsunami` y {cite:t}`avila2026`; la versión 1 de este cuaderno usaba 8,2). El escenario de 1979 de Poveda y Pulido (2019) se definió invirtiendo ondas P telesísmicas {cite:p}`escobar2020tsunami`. En el departamento de Nariño
causó unas 452 muertes y 1 011 heridos, y destruyó cerca de 3 080 viviendas (Ramírez y Goberna, 1980, citado por {cite:t}`escobar2020tsunami`). El epicentro que usa este cuaderno (1,598° N, 79,359° O, a
unos 60 km al oeste de Tumaco, con 33 km de profundidad) viene de {cite:t}`herd1981` y está **por verificar** contra esa fuente primaria.

### Objetivo y alcance

1. **Demostrar** que la propagación de un tsunami histórico puede simularse con código propio, en NumPy puro y en la CPU gratuita de Colab.
2. **Anclar la fuente en la física** (dislocación elástica con Mw de la literatura) en lugar de calibrarla, y medir qué tan lejos queda el resultado de las observaciones y de otros modelos.
3. **Declarar lo que el modelo no puede decir**, para que el cuaderno sirva como paso previo al análisis de amenaza de una ciudad y no se confunda con él.

## Marco teórico

### De la ruptura al arribo: la cadena de modelación

El análisis de amenaza por tsunami de origen sísmico sigue una cadena de cuatro pasos: definir los escenarios sismotectónicos, calcular la deformación sísmica que fija las condiciones iniciales, propagar las ondas largas
en aguas someras y evaluar el impacto en la costa con información topo-batimétrica de distinta resolución {cite:p}`ungrd2019atlas`. Las modelaciones colombianas
de referencia aplican esa cadena: Guapi con TUNAMI-N2, deformación de Okada y batimetría GEBCO {cite:p}`sanchez2023guapi`; Tumaco y Buenaventura con distribuciones de deslizamiento
de banda ancha {cite:p}`escobar2020tsunami`. Este cuaderno implementa los pasos 1 a 3, con el paso 4 reducido a leer la elevación en celdas de mar cercanas a la costa.

### Generación: la dislocación elástica de Okada

El movimiento súbito de una falla deforma el fondo marino. Para una falla rectangular de longitud $L$, ancho $W$, buzamiento $\delta$ y deslizamiento $D$ en un semiespacio elástico, {cite:t}`okada1985` da expresiones
cerradas del desplazamiento en superficie. Aquí solo interesa la componente vertical $u_z$, que se toma como la elevación inicial de la superficie del agua, $\eta_0 = u_z$, con velocidades nulas. Es la
aproximación habitual de generación instantánea y desacoplada; desprecia el filtro que impone la columna de agua a las deformaciones de longitud de onda corta y el aporte del desplazamiento horizontal sobre el talud.
El deslizamiento sale del momento sísmico, con $M_0 = 10^{1,5 M_w + 9,1}$ N·m y $D = M_0/(\mu L W)$.

### Propagación: ondas largas y aguas someras

Mientras la longitud de onda sea mucho mayor que la profundidad, la teoría de aguas someras describe la propagación {cite:p}`ungrd2019atlas`, y la celeridad depende solo de la profundidad en reposo $H$:

$$
c = \sqrt{g H}
$$

(unos 200 m/s, 700 km/h, sobre 4 000 m de profundidad). Las ecuaciones **no lineales** (NSWE) incluyen la advección, la fricción y el cambio de profundidad con la propia ola, y son las que permiten calcular la inundación en tierra. Las **lineales** (LSWE) suponen
amplitud pequeña frente a la profundidad y $H$ fija. Con $M = Hu$ y $N = Hv$:

$$
\frac{\partial \eta}{\partial t} + \frac{\partial M}{\partial x} + \frac{\partial N}{\partial y} = 0, \qquad
\frac{\partial M}{\partial t} + gH\frac{\partial \eta}{\partial x} = 0, \qquad
\frac{\partial N}{\partial t} + gH\frac{\partial \eta}{\partial y} = 0 .
$$

Valen en el mar abierto y en la plataforma profunda; cerca de la costa la amplitud deja de ser pequeña frente a la profundidad y las LSWE sobreestiman la elevación porque no disipan energía. **La elevación de un modelo lineal no es el run-up.**

### Esquema numérico

La versión 1 usaba Lax-Friedrichs en una malla colocada, un esquema de primer orden cuya difusión numérica atenuaba la ola, de modo que hubo que inflar la amplitud inicial. La versión 2 usa una **malla escalonada de Arakawa C con el esquema *forward-backward***:
$\eta$ en el centro de las celdas, los flujos en las caras, y los flujos se actualizan con el $\eta$ ya actualizado. Es un esquema clásico de diferencias finitas para aguas someras. En una onda plana de 35 km de longitud de onda que recorre
119 km, el esquema de la versión 1 conserva el 43 % de la amplitud y el escalonado el 99,96 % (prueba en el cuaderno 2). Las fronteras abiertas usan la condición de radiación $M = \pm\sqrt{gH}\,\eta$.

### Determinista frente a probabilista

Una simulación de un escenario es una amenaza **determinista**: dice qué pasaría con una fuente dada. La evaluación **probabilista** pondera muchas fuentes con su frecuencia y entrega la profundidad de inundación por periodo de retorno, que es lo que
hace falta para calcular la pérdida anual esperada {cite:p}`ungrd2019atlas`. Este cuaderno es de la primera clase. En el libro *Teoría y métodos de análisis de riesgos de desastres y climáticos*
([capítulo de tsunami](https://mromerot.github.io/teoria-riesgos/)) se explica cómo encaja cada tipo en el cálculo del riesgo.

## Metodología

### Datos y dominio

El dominio abarca de 0,2° S a 4,2° N y de 81,2° a 76,9° O (479 × 488 km), con 450 m de resolución en UTM 17N. Es mayor que el de la versión 1 (0,5–3,5° N, 79,5–77° O) por dos razones: el epicentro quedaba a 15 km de la
frontera oeste y Esmeraldas (Ecuador) estaba fuera. Los datos de elevación salen del mosaico global de DEM de NOAA/NCEI {cite:p}`noaa_dem_mosaic`. **La versión 1 los atribuía a GEBCO 2023 y ETOPO 2022; no lo son:** el enlace de GEBCO ya no responde y el servicio
entrega un mosaico de modelos de distinta procedencia. Una copia del recorte se versiona en `data/`. La reproyección conserva el norte arriba y el oeste a la izquierda; la versión 1 invertía el eje X al guardar el DEM, lo que espejaba los mapas.

### Escenario sísmico

La magnitud (Mw 8,3) es de la literatura; **la geometría es un supuesto**, porque no se tiene a mano el modelo de deslizamiento de Poveda y Pulido (2019) en que se basan {cite:t}`escobar2020tsunami` y {cite:t}`avila2026`.

| Parámetro | Valor | Estado |
|---|---|---|
| Mw | 8,3 | Literatura |
| Longitud × ancho | 200 × 80 km | Supuesto |
| Rumbo / buzamiento / ángulo de desplazamiento | 30° / 15° / 90° | Supuesto |
| Profundidad del borde superior | 12 km (el inferior, ~33 km) | Supuesto; el hipocentro de 33 km se ubica en el borde inferior |
| Rigidez / Poisson | 30 GPa / 0,25 | Valores típicos |
| Deslizamiento | 7,4 m | Derivado |

El modelo de Okada implementado reproduce a 1e-5 m una implementación independiente (pyrocko) en tres geometrías. La deformación inicial va de +3,1 m (levantamiento hacia el oeste, sobre la parte somera de la falla) a −1,3 m (hundimiento hacia la costa)
({numref}`fig-fuente`).

:::{figure} notebooks/fuente_okada.png
:label: fig-fuente
:alt: Deformación vertical del fondo por la falla de Okada
Deformación vertical del fondo (η inicial) del escenario de Mw 8,3. Líneas discontinuas: proyección de la falla. La estrella roja es el epicentro, en el punto medio del borde inferior de la falla (borde este).
:::

### Parámetros de la simulación

| Parámetro | Valor | Justificación |
|---|---|---|
| Malla | 1 065 × 1 084 celdas de 450 m | DEM de 15″ reproyectado |
| Paso de tiempo | 1 s | $\mathrm{CFL}=c_{\max}\,\Delta t\,\sqrt{2}/\Delta x = 0{,}70 < 1$ |
| Duración | 3 600 s (60 min) | Incluye el arribo observado en Buenaventura (45 min, aunque se excluye, ver abajo) y ondas reflejadas |
| Instantáneas | cada 120 s | 31 cuadros para la animación |
| Fricción | Ninguna | Solo hay linealidad; los términos de Manning de la versión 1 eran no lineales y se retiran |
| Tiempo de ejecución | ~45 s para 60 min | CPU estándar |

### Estaciones y control de calidad de las observaciones

Las ocho observaciones de `data/observaciones_1979.csv` **no están verificadas contra las fuentes primarias**. Antes de compararlas se revisa que sean coherentes con una onda larga: con la distancia $d$ y el arribo $t$, la profundidad equivalente es $H_{eq}=(d/t)^2/g$,
que debe ser menor que la profundidad de la ruta (3 000–5 000 m). Salinas (Ecuador) da unos 4 900 m y queda fuera del dominio; San Juan y El Charco caen tierra adentro y Buenaventura en un estuario somero, sin mar de 10 m o más a menos de 10 km. Quedan **cuatro estaciones comparables**: Tumaco (muelle),
Tumaco (playa), Bocagrande y Esmeraldas. Cada una se lee en la celda de mar más cercana con profundidad de al menos 10 m. La versión 1 anunciaba ocho estaciones, pero varias estaban fuera del dominio o tierra adentro y quedaban recortadas al borde.

## Resultados

### Elevación máxima

La elevación máxima en celdas de 10 m de profundidad o más es de 8,9 m ({numref}`fig-max-eta`). Se concentra en una franja sobre la falla y en la costa frente al epicentro, de Tumaco hacia el sur. En celdas de menos de 10 m el modelo lineal llega a 25 m, una amplificación
sin fricción ni rotura que no se interpreta.

:::{figure} notebooks/max_eta_map.png
:label: fig-max-eta
:alt: Elevación máxima de la ola
Elevación máxima de la superficie del mar en 60 min (LSWE). Izquierda: dominio completo, solo celdas de 10 m de profundidad o más. Derecha: plataforma de Tumaco (10–200 m).
:::

### Series de tiempo

Frente a Tumaco la primera señal es un descenso del nivel (la subsidencia cosísmica inicial y un valle previo a la ola); el primer ascenso mayor de 0,1 m llega a los 23 min y la cresta máxima a los 30–31 min, seguida de un descenso de unos 9 m ({numref}`fig-timeseries`).
Ese vaivén tan grande es típico de un modelo sin fricción en una bahía somera, donde la energía queda atrapada y se refleja. En Bocagrande el primer ascenso es a los 11 min y en Esmeraldas a los 12 min.

:::{figure} notebooks/time_series.png
:label: fig-timeseries
:alt: Series de tiempo en cuatro estaciones
Series de η en cuatro estaciones. Línea discontinua roja: arribo observado (sin verificar); punteada azul: primer ascenso mayor de 0,1 m simulado; línea punto-raya: run-up observado (sin verificar).
:::

### Comparación con las observaciones y con otros modelos

| Estación | Arribo obs.* (min) | Arribo sim. (min) | Run-up obs.* (m) | η máx. sim. (m) | η sim./run-up |
|---|---|---|---|---|---|
| Tumaco (muelle) | 15 | 23 | 5,0 | 8,2 | 1,6 |
| Tumaco (playa) | 15 | 23 | 4,5 | 8,8 | 2,0 |
| Bocagrande | 18 | 11 | 3,0 | 3,9 | 1,3 |
| Esmeraldas (Ecuador) | 12 | 12 | 4,0 | 4,8 | 1,2 |

\* Observaciones sin verificar contra la fuente primaria.

Con cuatro puntos y observaciones dudosas **no se calcula un RMSE ni un R²**. Lo que sí se puede decir ({numref}`fig-validation`):

:::{figure} notebooks/validation.png
:label: fig-validation
:alt: Comparación de arribos y amplitudes
Izquierda: arribo simulado frente a observado. Derecha: run-up observado (sin verificar) y η máxima simulada en el mar; no son magnitudes equivalentes.
:::

- **Arribos.** El simulado difiere del observado entre −7 y +8 min. En Esmeraldas coincide; en Bocagrande llega antes y en Tumaco después. El modelo TUNAMI-N2 de {cite:t}`avila2026` da 22 min para la primera ola en Tumaco, muy cerca de los 23 min de aquí, lo que respalda el resultado simulado más que el observado. Los 15 min observados pueden referirse al primer movimiento (el descenso) y no al primer ascenso.
- **Amplitudes.** La η simulada es 1,2 a 2,0 veces el run-up observado, y unas cuatro veces las alturas máximas de 1,88–2,30 m que {cite:t}`escobar2020tsunami` obtienen para la isla de Tumaco con el escenario de 1979 en un modelo no lineal. Las cifras de run-up de la tabla tampoco coinciden con esas simulaciones, lo que es otra razón para verificarlas.

### Sensibilidad

Con la malla de 900 m, que corre en 4 s, se varió un parámetro a la vez ({numref}`tbl-sens`).

:::{table} Rango de la respuesta en Tumaco (muelle y playa) al variar un parámetro a la vez. «v1» son los parámetros documentados en la versión 1 (Mw 8,2; rumbo 10°; buzamiento 20°; 250 × 100 km).
:label: tbl-sens
| Variación | η máx. en Tumaco (m) | Arribo en Tumaco (min) |
|---|---|---|
| Resolución 450 → 900 m | 8,2–8,8 → 7,6–8,2 | 23,2–23,4 → 23,8–24,0 |
| Mw 8,3 → 8,2 | 7,6–8,2 → 5,4–5,8 | sin cambio apreciable |
| Buzamiento 12° y 18° | 7,5–8,3 | 23,0–24,6 |
| Rumbo 20° y 40° | 7,6–8,4 | 21,0–25,7 |
| Longitud 150 y 250 km | 6,8–8,6 | 23,7–24,3 |
| Profundidad del borde superior 8 y 16 km | 7,4–8,3 | 23,7–24,0 |
| Parámetros de la v1 | 4,2–4,5 | 26,0–26,4 |
:::

La **resolución** pesa poco (7 % en amplitud, medio minuto en arribo): el resultado es numéricamente estable. La **fuente** pesa mucho: entre el caso más pequeño (parámetros de la versión 1) y el más grande, la amplitud en Tumaco varía de 4,2 a 8,8 m. El arribo
es robusto, de 21 a 26 min en todos los casos.

### Animación de la propagación

La {numref}`fig-animation` muestra la propagación con el oeste a la izquierda y el norte arriba. El lóbulo de levantamiento nace sobre la falla, junto a la estrella, y se divide en una ola que viaja hacia la costa y otra hacia el océano abierto. La estrella
marca el epicentro; en la versión 1 el mapa estaba espejado y la fuente nacía a unos 200 km de ella.

:::{figure} notebooks/tsunami_propagation.gif
:label: fig-animation
:alt: Animación de la propagación del tsunami
Animación de la propagación del tsunami de Tumaco 1979 (LSWE de la versión 2, 31 cuadros, t = 0–60 min). Escala de color: η en metros (se omiten |η| < 0,1 m y celdas de menos de 10 m de profundidad). La estrella roja es el epicentro.
:::

## Alcance: qué se puede y qué no se puede concluir

**Lo que el cuaderno sí sustenta.**

- **El tiempo de llegada a Tumaco ronda los 20–25 min y es robusto.** Cambia poco con la resolución y con los parámetros supuestos, y coincide con un modelo no lineal publicado {cite:p}`avila2026`. Para el análisis de riesgo de una ciudad es la cifra más útil: el tiempo disponible para evacuar de una fuente cercana es de minutos {cite:p}`ungrd2019atlas`,
  y aquí son del orden de 20.
- **La ola no es una sola.** Tras un descenso inicial llegan varias crestas durante al menos 30–45 min, y la máxima no es la primera. Un plan de evacuación no debe darse por terminado con el primer ascenso.
- **El flujo de trabajo es reproducible** y verificado: Okada contra una implementación independiente, onda plana contra la solución exacta, reposo exacto y fuente ligada al epicentro (prueba automática).

**Lo que no sustenta.**

- **No es un mapa de amenaza ni da inundación.** Las LSWE no calculan inundación en tierra. Las profundidades de inundación y las zonas seguras (por ejemplo, el umbral de 0,3 m que usa {cite:t}`avila2026`) requieren NSWE con celda seca y topografía fina de las islas de Tumaco.
- **Las amplitudes no son confiables en valor absoluto.** Dependen mucho de una fuente cuya geometría es un supuesto y el modelo las sobreestima frente a lo publicado. Sirven para comparar escenarios entre sí, no para dimensionar obras ni tasas de daño.
- **No es una validación.** Cuatro observaciones sin verificar, de las que dos son de un mismo lugar, no bastan.

**Cómo entra en el cálculo del riesgo.** El producto de amenaza que necesita el cálculo es la profundidad de inundación por escenario o por periodo de retorno; este cuaderno aporta el paso de propagación y el tiempo de arribo. La
exposición (Tumaco concentra la mayor población expuesta del país {cite:p}`ungrd2019atlas`) y la vulnerabilidad física, con funciones de fragilidad como las comparadas para los edificios de Tumaco {cite:p}`paez2021tsunamifrag`, se aplican sobre
la inundación, no sobre la elevación en el mar.

## Instrucciones de reproducción

1. **Cuaderno 1** (`01-bathymetry.ipynb`): lee o descarga el DEM, lo reproyecta a UTM 17N y comprueba la orientación. Menos de 1 min.
2. **Cuaderno 2** (`02-simulation.ipynb`): escenario de Okada, solver, pruebas, simulación de 60 min y sensibilidad. Unos 2 min.
3. **Cuaderno 3** (`03-visualization.ipynb`): mapas, series, control de calidad, comparación y animación. 1–2 min.

:::{note}
Los tres cuadernos funcionan en la CPU estándar de Colab y no necesitan TPU ni GPU. Si se abren en Colab, el cuaderno 2 requiere el DEM del cuaderno 1 o la copia de `data/`.
:::

## Limitaciones y trabajo futuro

1. **Linealidad y sin fricción.** Una versión no lineal (NSWE) con fricción de Manning y tratamiento de celda seca calcularía inundación y amortiguaría los vaivenes.
2. **Fuente.** Falla única de deslizamiento uniforme con geometría supuesta. Debe reemplazarse por la distribución de deslizamiento de Poveda y Pulido (2019) y verificar el epicentro, la profundidad y el mecanismo contra Herd et al. (1981) y Yoshimoto et al. (2017).
3. **Generación instantánea y desacoplada**, sin filtro por la columna de agua ni desplazamiento horizontal sobre el talud.
4. **Resolución.** 450 m no capturan las islas de Tumaco ni el estuario; hacen falta mallas anidadas con batimetría local.
5. **Observaciones.** Verificar las ocho contra Herd et al. (1981) y la base de la NOAA, corregir las coordenadas y completar con registros mareográficos.
6. **Probabilista.** Un análisis para el cálculo de la pérdida anual esperada necesita muchas fuentes con sus frecuencias.

## Conclusiones

Se simuló la propagación del tsunami de Tumaco de 1979 con una fuente de Okada y un esquema sin difusión numérica, sin parámetro de calibración, en NumPy y en Colab. El tiempo de arribo a Tumaco (20–25 min) es robusto y consistente con un modelo publicado;
la amplitud es sensible a una geometría de falla que aún es un supuesto y se sobreestima frente a la literatura. La versión 2 corrige los errores de la versión 1 (mapa espejado, fuente desligada del epicentro, atribución de los datos, estaciones fuera del dominio) y deja
explícito lo que falta para pasar de un escenario de propagación a un análisis de amenaza.

## Disponibilidad de datos y código

- **Código:** <https://github.com/scr-ungrd/cuadernos-reproducibles-crc003> (licencia MIT; el constructor de los cuadernos está en `scripts/construir_cuadernos.py`).
- **Elevación:** recorte de {cite:t}`noaa_dem_mosaic` en `data/dem_tumaco_noaa_15s.tif`.
- **Observaciones históricas (sin verificar):** `data/observaciones_1979.csv`.

```{bibliography}
```
