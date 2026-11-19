# Registro del escaneo de seguridad

Constancia del escaneo previo a un *release*, según los [Requisitos de seguridad](https://scr-ungrd.github.io/cuadernos-reproducibles/requisitos-seguridad) de la colección (REL-01). Se agrega una sección por cada escaneo.

## 2026-11-19

- **Estado revisado:** commit `9966859` y los cambios sin commit de ese día.
- **Herramientas:** `gitleaks` 8.30.1 (descargada con la suma de verificación de su publicación) y `pip-audit` 2.10.1.

| Comprobación | Resultado |
|---|---|
| Secretos en todo el historial de git (`gitleaks git`) | Sin hallazgos |
| Secretos en el árbol de trabajo (`gitleaks dir`) | 2 hallazgos, ambos falsos positivos: código del tema en `_build/`, que no se versiona |
| Vulnerabilidades de las dependencias fijadas (`pip-audit --no-deps`) | Sin vulnerabilidades conocidas en los 15 paquetes |
| Rutas locales y datos personales en archivos versionados | Ninguno |
| Metadatos de imágenes (EXIF, GPS, autoría) | Sin GPS ni autoría |
| Binarios, macros y código remoto | Sin ejecutables ni archivos con macros; `curl` solo en el flujo de despliegue, ahora con suma de verificación |
| Correos de autoría en el historial | 68 campos de correo, todos personales: pendiente de decisión de la persona autora (FUG-04) |

**Limitaciones.** `pip-audit` se ejecutó con `--no-deps`, así que no cubre las dependencias indirectas. Los escaneos de patrones no detectan secretos de formato inusual. No se revisó la configuración de la cuenta de GitHub ni de Zenodo.
