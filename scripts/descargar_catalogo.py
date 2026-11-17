"""Descarga las dos consultas del catálogo del USGS que usa el cuaderno, con una fecha de corte fija.

El cuaderno consulta el servicio FDSN Event del USGS (https://earthquake.usgs.gov/fdsnws/event/1/query). Con la
fecha de corte del 2026-11-16 reproduce exactamente los conteos de sus salidas guardadas:

  1. Catálogo base (sección 3): M >= 3,0, 2000-01-01 hasta la fecha de corte, recuadro 5° S a 13° N y 82° O a 65° O.
     Salida: data/usgs_catalogo_m3_2000-2026-11-16.csv (4 769 eventos).
  2. Catálogo ampliado (sección 10): M >= 2,5, desde 1900, recuadro 5° S a 16° N y 84° O a 66° O, solo terremotos.
     Salida: data/usgs_catalogo_ampliado_1900-2026-11-16.csv (11 085 eventos).

Uso:  python scripts/descargar_catalogo.py [AAAA-MM-DD]
"""
import io
import sys
import time
from pathlib import Path

import pandas as pd
import requests

RAIZ = Path(__file__).resolve().parent.parent
API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
CORTE = sys.argv[1] if len(sys.argv) > 1 else "2026-11-16"
LIMITE = 20000


def consultar(params):
    for intento in range(4):
        r = requests.get(API_URL, params=params, timeout=180)
        if r.status_code in (200, 204):
            break
        time.sleep(5 * (intento + 1))
    r.raise_for_status()
    return pd.DataFrame() if r.status_code == 204 or not r.text.strip() else pd.read_csv(io.StringIO(r.text))


def tramo(t0, t1, bbox, mag_min):
    params = dict(format="csv", orderby="time-asc", limit=LIMITE, eventtype="earthquake",
                  starttime=t0.strftime("%Y-%m-%dT%H:%M:%S"), endtime=t1.strftime("%Y-%m-%dT%H:%M:%S"),
                  minlatitude=bbox["lat_min"], maxlatitude=bbox["lat_max"],
                  minlongitude=bbox["lon_min"], maxlongitude=bbox["lon_max"], minmagnitude=mag_min)
    d = consultar(params)
    if len(d) >= LIMITE:                      # si llega al límite, se divide el tramo en dos
        tm = t0 + (t1 - t0) / 2
        return pd.concat([tramo(t0, tm, bbox, mag_min), tramo(tm, t1, bbox, mag_min)], ignore_index=True)
    return d


def base():
    params = {"format": "csv", "starttime": "2000-01-01", "endtime": CORTE, "minlatitude": -5.0, "maxlatitude": 13.0,
              "minlongitude": -82.0, "maxlongitude": -65.0, "minmagnitude": 3.0, "orderby": "time"}
    return consultar(params)


def ampliado():
    bbox = dict(lon_min=-84.0, lon_max=-66.0, lat_min=-5.0, lat_max=16.0)
    partes, t, fin = [], pd.Timestamp(year=1900, month=1, day=1), pd.Timestamp(CORTE)
    while t < fin:
        t2 = min(t + pd.DateOffset(years=10), fin)
        partes.append(tramo(t, t2, bbox, 2.5))
        t = t2
    return pd.concat([p for p in partes if len(p)], ignore_index=True).drop_duplicates("id")


if __name__ == "__main__":
    (RAIZ / "data").mkdir(exist_ok=True)
    b = base()
    b.to_csv(RAIZ / "data" / f"usgs_catalogo_m3_2000-{CORTE}.csv", index=False)
    print(f"Catálogo base: {len(b):,} eventos")
    a = ampliado()
    a.to_csv(RAIZ / "data" / f"usgs_catalogo_ampliado_1900-{CORTE}.csv", index=False)
    print(f"Catálogo ampliado: {len(a):,} eventos, {a.time.min()[:10]} a {a.time.max()[:10]}")
