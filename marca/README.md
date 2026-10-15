# La marca de Spicy Suite

Esta carpeta convierte el código de ArtCraft Launcher en Spicy Suite al momento de compilar. El
código del original no se copia ni se edita en este repositorio: el flujo
[`publicar.yml`](../.github/workflows/publicar.yml) lo descarga en cada versión y le aplica lo que
hay aquí. Por eso las versiones nuevas del original nunca chocan con la marca.

| Archivo | Qué es |
|---|---|
| [`aplicar.py`](aplicar.py) | La lista de cambios: nombre, identificadores, enlaces, colores y archivos de marca |
| [`activos/`](activos/) | Logo horizontal (negro y blanco), ícono, versión para la barra de menús de macOS, fondo del DMG e íconos de Facebook y Behance |
| [`hacer_svg.py`](hacer_svg.py) | Genera los SVG de `activos/` a partir del logo de `01_Marca` |

## Qué cambia y qué no

Cambia lo que se ve y lo que identifica al launcher:

- **Nombre:** «ArtCraft Launcher» pasa a **Spicy Suite** en la interfaz, en los 11 idiomas, el
  instalador, el menú de inicio, la bandeja y la barra de menús.
- **Logo y colores:** el logo de SPICY RNDR en la barra superior y en el instalador, el ícono rojo
  del favicon del sitio y el rojo `#E43330` como color de acento.
- **Enlaces:** el sitio y las redes (Instagram, Facebook y Behance) llevan a Spicy Render. Discord y
  GitHub siguen llevando a ArtCraft, porque ahí está el soporte de los programas.
- **Identidad**, para que Spicy Suite y ArtCraft Launcher puedan convivir en la misma
  computadora: identificador `studio.spicyrender.spicy-suite`, ejecutable `spicy-suite.exe`,
  carpetas `Spicy Suite`, editor «Spicy Render» y otro puerto para la instancia única.
- **Actualizaciones del launcher:** se buscan en `spicyrndr/craft-launcher`, no en el original.
  Si no, la primera actualización devolvería ArtCraft Launcher.

No cambia nada de la lógica: el catálogo de programas, de dónde se descargan, la verificación con
SHA-256, la instalación, la detección de programas instalados (que reconoce al editor «Learning
Machines LLC» de los programas) ni la firma de Apple que se exige a cada programa en macOS.

## Si la compilación falla

Cada regla de `aplicar.py` busca un texto exacto del original. Si una versión nueva lo cambió, el
flujo se detiene con un mensaje como este:

```
error: crates/core/src/catalog.rs: se esperaban 1 apariciones de 'pub const SOCIAL: …' y hay 0
El original cambió una parte que la marca modifica: actualice la regla en marca/aplicar.py.
```

Para arreglarlo:

1. Vea cómo quedó esa parte en el original: `https://github.com/storytold/craft-launcher/blob/<versión>/<archivo>`.
2. Ajuste en `aplicar.py` el texto que busca la regla (y, si hace falta, el que pone).
3. Pruebe en local contra esa versión:

   ```sh
   git clone --depth 1 --branch v0.4.2 https://github.com/storytold/craft-launcher.git /tmp/original
   python marca/aplicar.py /tmp/original
   ```

   Debe terminar con `marca aplicada: N cambios`. Al subir el cambio, el flujo
   [`comprobar-marca.yml`](../.github/workflows/comprobar-marca.yml) repite la prueba contra la
   última versión del original.
4. Vuelva a correr **Publicar Spicy Suite** desde la pestaña Actions (*Run workflow*).

## Cambiar el logo o los colores

- **Logo:** edite `hacer_svg.py` y corra `python marca/hacer_svg.py marca/activos`. Los PNG, ICO
  e ICNS se generan solos al compilar.
- **Colores:** las reglas de `theme.rs` en `aplicar.py` (`accent` y `accent_ink`, en modo oscuro y
  claro) y el color de la franja del instalador en `package.ps1`.

Después, corra **Publicar Spicy Suite** con *forzar* activado para volver a compilar la versión
actual. Las copias instaladas no reciben ese cambio hasta la siguiente versión del original,
porque el número de versión es el mismo.

## Identificadores que no se deben cambiar

`UPGRADE_CODE` y los `GUID_*` de `aplicar.py` identifican la instalación de Windows. Si cambian,
Windows trata la versión nueva como otro programa y deja la anterior instalada.
