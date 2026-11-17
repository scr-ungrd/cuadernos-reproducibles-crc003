"""Genera images/banner.png con los epicentros del catálogo base del USGS (data/usgs_catalogo_m3_*.csv).

Uso:  python scripts/generar_banner.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CSV = sorted((RAIZ / "data").glob("usgs_catalogo_m3_*.csv"))[-1]
d = pd.read_csv(CSV).sort_values("mag")
fig = plt.figure(figsize=(12.23, 4.94), dpi=100, facecolor="#0b1d3a")
ax = fig.add_axes([0.50, 0.04, 0.48, 0.92], facecolor="#0b1d3a")
ax.scatter(d.longitude, d.latitude, s=np.clip((d.mag - 2.0) ** 2.3 * 2.2, 3, 400), c=d.mag, cmap="plasma",
           vmin=3, vmax=7.5, alpha=0.7, linewidths=0)
ax.set_xlim(-82, -65); ax.set_ylim(-5, 13); ax.set_aspect(1 / np.cos(np.radians(4)))
ax.axis("off")
fig.text(0.05, 0.60, "Sismicidad de Colombia", color="white", fontsize=30, fontweight="bold")
fig.text(0.05, 0.47, f"Catálogo del USGS, 2000–{d.time.max()[:4]}, M ≥ 3,0", color="#9fc3ff", fontsize=17)
fig.text(0.05, 0.38, f"{len(d):,} epicentros".replace(",", " "), color="#9fc3ff", fontsize=17)
fig.savefig(RAIZ / "images" / "banner.png", facecolor=fig.get_facecolor())
print("banner generado:", len(d), "eventos de", CSV.name)
