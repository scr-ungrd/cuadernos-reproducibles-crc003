# Cambios

## 2.0.0 (2026-11-02)

**Correcciones**

- **Animación espejada y fuente desligada del epicentro.** El DEM se guardaba con el eje X invertido y el mapa salía con el oeste a la derecha. Además la onda en N se colocaba en `x_coast − 60 km`
  (la celda de mar más oriental del dominio) y no en el epicentro: nacía a unos 200 km de la estrella. Ahora el mapa tiene el oeste a la izquierda y la falla se ancla al epicentro, con una
  prueba automática (el máximo de η inicial debe quedar a menos de 150 km de él).
- **Atribución del DEM.** El enlace de GEBCO 2023 responde 404 y el servicio entregaba el mosaico global de DEM de NOAA/NCEI, no GEBCO ni ETOPO 2022. Se corrige el texto y se versiona una copia del recorte (`data/dem_tumaco_noaa_15s.tif`).
- **Amplitud inicial.** La versión 1 declaraba `A = 8 m`, pero la fórmula `2·(A·e − A/3·e)` daba un pico inicial de 16 m. Ya no hay parámetro de calibración.
- **Estaciones.** Esmeraldas, Buenaventura y Salinas quedaban fuera del dominio (o recortadas al borde) y San Juan y El Charco caen tierra adentro. Se amplía el dominio, se lee cada estación en una celda de mar de ≥ 10 m y se excluyen y declaran las que no se pueden comparar.
- **Validación.** Se retiran el RMSE y el R² (comparaban η en el mar con run-up de una tabla sin verificar). Se agrega el control de calidad de las observaciones (profundidad equivalente) y el contraste con resultados publicados.
- **Magnitud y licencia.** Mw 8,3 (Yoshimoto et al., 2017) en lugar de 8,2; la licencia del código es MIT (el `myst.yml` decía Apache-2.0).

**Métodos**

- Fuente: deformación de Okada (1985) de una falla rectangular, verificada contra pyrocko (3 geometrías, error < 1e-5 m), en lugar de una onda en N calibrada.
- Solver: malla escalonada *forward-backward* en lugar de Lax-Friedrichs (conserva el 99,96 % de la amplitud de una onda plana frente al 43 %), con fronteras abiertas.
- Dominio ampliado (0,2° S–4,2° N, 81,2–76,9° O), UTM 17N, 60 minutos.
- Análisis de sensibilidad (resolución, Mw, rumbo, buzamiento, longitud, profundidad y los parámetros de la versión 1).

**Texto**

- Marco teórico nuevo (cadena de modelación, dislocación de Okada, ondas largas, LSWE y NSWE, esquema numérico, determinista frente a probabilista), sección «Alcance» con lo que los resultados sí y no sustentan, y limitaciones actualizadas.
- Bibliografía: se agregan Escobar et al. (2020), Ávila-Guzmán et al. (2026), Sánchez et al. (2023), Paez-Ramirez et al. (2021), el Atlas de 2019 y el mosaico de NOAA; se retiran Carrier et al. (2003), GEBCO y ETOPO.

**Pendiente** (ver «Limitaciones» del artículo): distribución de deslizamiento de Poveda y Pulido (2019), NSWE con inundación, verificación de las observaciones contra Herd et al. (1981) y NOAA/NGDC.

## 1.0.0 (2026-05-11)

Versión inicial: LSWE con Lax-Friedrichs y onda en N calibrada (A = 8 m).
