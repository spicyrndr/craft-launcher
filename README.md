<p align="center">
  <img alt="SPICY RNDR" src="marca/activos/spicy-mark.svg" width="96">
</p>

<h1 align="center">Spicy Suite</h1>

<p align="center">
  Un solo lugar para instalar, actualizar y abrir las herramientas creativas de Spicy Render:<br>
  PhotoCraft, LightCraft, FilmCraft, DesignCraft, VectorCraft, PdfCraft, EffectCraft, WordCraft,<br>
  DeckCraft, GridCraft, CADCraft, SoundCraft y FigCraft.
</p>

<p align="center">
  <a href="https://suite.spicyrender.studio"><b>suite.spicyrender.studio</b></a> ·
  <a href="https://github.com/spicyrndr/craft-launcher/releases/latest">Descargas</a> ·
  <a href="https://spicyrender.studio">spicyrender.studio</a>
</p>

Spicy Suite es [ArtCraft Launcher](https://github.com/storytold/craft-launcher) con la marca de
Spicy Render. Funciona exactamente igual que el original: descarga cada programa de su
repositorio oficial, verifica cada descarga contra sus sumas SHA-256, lo instala y avisa cuando hay
una versión nueva. Solo cambian el nombre, el logo, el ícono, los colores y los enlaces.

## Descargar e instalar

En la [última versión](https://github.com/spicyrndr/craft-launcher/releases/latest):

| Sistema | Archivo |
|---|---|
| Windows (recomendado) | `spicy-suite-<versión>-windows-x64.msi`: se instala para el usuario, sin pedir permisos de administrador |
| Windows sin instalar | `spicy-suite-<versión>-windows-x64-portable.zip`: se descomprime y se abre `spicy-suite.exe` |
| macOS (Apple Silicon e Intel) | `spicy-suite-<versión>-macos-universal.dmg`: se arrastra a Aplicaciones |

Los archivos no llevan firma digital, así que el sistema pide una confirmación la primera vez:

- **Windows:** si aparece «Windows protegió su PC», elija **Más información → Ejecutar de todas formas**.
- **macOS:** abra la app con clic derecho → **Abrir**. En macOS 15 o posterior, si no aparece la
  opción, vaya a **Ajustes del Sistema → Privacidad y seguridad** y elija **Abrir de todas formas**.

## Cómo se mantiene al día

- **Los programas** (PhotoCraft, FilmCraft…) se actualizan desde sus repositorios originales, igual
  que en ArtCraft Launcher. Spicy Suite no los modifica.
- **Spicy Suite misma:** cada día, [un flujo de GitHub Actions](.github/workflows/publicar.yml)
  revisa si [ArtCraft Launcher](https://github.com/storytold/craft-launcher/releases) publicó una
  versión nueva. Si la hay, toma su código tal cual, le aplica la marca, corre las pruebas del
  original, compila Windows y macOS y la publica aquí con el mismo número de versión.
- **En Windows**, las copias instaladas se actualizan solas desde esas publicaciones.
- **En macOS**, la actualización es manual: descargue el DMG nuevo y reemplace la app. El launcher
  solo instala apps firmadas por el equipo de Apple de ArtCraft, y Spicy Suite no tiene esa
  firma. Se puede automatizar cuando Spicy Render tenga una cuenta de desarrollador de Apple.

Si una versión nueva del original cambia algo que la marca modifica, el flujo se detiene sin
publicar nada y GitHub avisa por correo. La versión anterior de Spicy Suite sigue disponible.
Cómo arreglarlo: [marca/README.md](marca/README.md).

## La página

[suite.spicyrender.studio](https://suite.spicyrender.studio) se genera con [`sitio/hacer.py`](sitio/hacer.py) a partir de [`sitio/plantilla.html`](sitio/plantilla.html) y se publica con GitHub Pages ([`sitio.yml`](.github/workflows/sitio.yml)). Se vuelve a generar sola en cada versión: los enlaces de descarga salen de la última publicación, y la lista de programas, sus descripciones en español y sus íconos, del código del original. Para cambiar textos o diseño, edite la plantilla; la línea «Alternativa a…» de cada programa está en `hacer.py`.

## Este repositorio

| Rama | Qué tiene |
|---|---|
| `spicy` (principal) | La marca ([`marca/`](marca/)), la página de suite.spicyrender.studio ([`sitio/`](sitio/)) y la automatización ([`.github/workflows/`](.github/workflows/)) |
| `main` | El código de ArtCraft Launcher sin cambios (se puede actualizar con **Sync fork** en GitHub; la compilación no la usa, porque toma el código directamente del original) |

## Licencia y créditos

Spicy Suite se basa en [ArtCraft Launcher](https://github.com/storytold/craft-launcher), del
ArtCraft Team y sus colaboradores, con licencia MIT o Apache 2.0 a elección
([LICENSE-MIT](LICENSE-MIT), [LICENSE-APACHE](LICENSE-APACHE)). No es un producto de ArtCraft ni
está respaldado por su equipo, y no incluye sus marcas. El nombre Spicy Render, SPICY RNDR y su
logo son de Spicy Render y no están cubiertos por esas licencias. Detalles en [NOTICE](NOTICE).
