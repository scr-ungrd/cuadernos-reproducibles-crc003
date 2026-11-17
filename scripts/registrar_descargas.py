"""Registra la suma de verificación SHA-256, el tamaño y el número de filas de cada archivo de data/.

Uso:  python scripts/registrar_descargas.py
Salida: metadata/descargas.csv (archivo, filas, bytes, sha256, fecha_modificacion)

Se ejecuta después de regenerar los datos con los demás scripts, para que cualquier persona pueda comprobar que
sus archivos coinciden con los publicados. La fecha es la de modificación del archivo.
"""
import csv
import hashlib
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data"
SALIDA = RAIZ / "metadata" / "descargas.csv"


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def filas(ruta):
    if ruta.suffix != ".csv":
        return ""
    with open(ruta, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f)) - 1


def main():
    SALIDA.parent.mkdir(exist_ok=True)
    archivos = sorted(p for p in DATOS.iterdir() if p.is_file() and p.suffix in {".csv", ".tif", ".nc"})
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["archivo", "filas", "bytes", "sha256", "fecha_modificacion"])
        for p in archivos:
            w.writerow([f"data/{p.name}", filas(p), p.stat().st_size, sha256(p),
                        date.fromtimestamp(p.stat().st_mtime).isoformat()])
    print(f"{len(archivos)} archivos registrados en {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
