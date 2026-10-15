#!/usr/bin/env python3
"""Aplica la marca Spicy Suite a una copia del código de ArtCraft Launcher.

    python marca/aplicar.py <carpeta-del-original>            textos, identidad y activos
    python marca/aplicar.py <carpeta-del-original> --iconos   después de packaging/icons.sh

Solo cambia nombres, identificadores, enlaces, colores y archivos de marca; la lógica del
launcher (descargas, verificación, instalación, detección de apps) queda como en el original.
Cada regla debe encontrar el texto que busca: si el original cambió esa línea, el script se
detiene con el archivo y la regla en vez de dejar una compilación a medias.
"""

import pathlib
import shutil
import sys

MARCA = pathlib.Path(__file__).resolve().parent
ACTIVOS = MARCA / "activos"

NOMBRE = "Spicy Suite"
ID = "spicy-suite"
ID_APP = "studio.spicyrender.spicy-suite"
EDITOR = "Spicy Render"
REPO = "spicyrndr/craft-launcher"
SITIO = "https://spicyrender.studio"
# Fijos para siempre: si cambian, Windows deja de reconocer las instalaciones anteriores.
UPGRADE_CODE = "82E12527-2CAB-4A21-9D17-4FDB7C3D432F"
GUID_APP = "840C7566-644D-4ECB-8A94-3930EBFE30B3"
GUID_MENU = "BCF4A9A2-360D-42FC-8A3C-D37C3CBD8EDB"
GUID_ESCRITORIO = "CA9FEAE1-1671-46D7-8195-000054E23549"
# Otro puerto que el original, para que Spicy Suite y ArtCraft Launcher no se confundan si los dos
# están abiertos en la misma computadora.
PUERTO = "47_431"

# Archivos de texto donde aparecen el nombre y la identidad del launcher.
TEXTO = (".rs", ".tsv", ".toml", ".ps1", ".wxs", ".wxl", ".sh", ".in", ".py", ".txt")
ALCANCE = ("crates", "apps", "packaging/windows", "packaging/macos", "packaging/icons.sh")


class ReglaRota(Exception):
    pass


class Arbol:
    def __init__(self, raiz):
        self.raiz = pathlib.Path(raiz).resolve()
        if not (self.raiz / "crates/core/src/catalog.rs").is_file():
            raise ReglaRota(f"{self.raiz} no parece el código de ArtCraft Launcher")
        self.hechos = 0

    def ruta(self, rel):
        return self.raiz / rel

    def leer(self, rel):
        # Sin traducir saltos de línea: el archivo queda igual salvo lo que cambian las reglas.
        with open(self.ruta(rel), encoding="utf-8", newline="") as f:
            return f.read()

    def escribir(self, rel, texto):
        self.ruta(rel).write_text(texto, encoding="utf-8", newline="")

    def archivos(self):
        for base in ALCANCE:
            p = self.ruta(base)
            candidatos = [p] if p.is_file() else sorted(p.rglob("*"))
            for f in candidatos:
                if f.is_file() and f.suffix in TEXTO:
                    yield f.relative_to(self.raiz).as_posix()

    def cambiar(self, rel, viejo, nuevo, veces=1):
        """Cambia `viejo` por `nuevo` en un archivo; exige exactamente `veces` apariciones (None: al menos una)."""
        texto = self.leer(rel)
        n = texto.count(viejo)
        if n == 0 or (veces is not None and n != veces):
            raise ReglaRota(f"{rel}: se esperaban {veces} apariciones de {viejo!r} y hay {n}")
        self.escribir(rel, texto.replace(viejo, nuevo))
        self.hechos += n

    def cambiar_en_todos(self, viejo, nuevo, minimo=1, excepto=()):
        """Cambia `viejo` por `nuevo` en todo el alcance; exige al menos `minimo` apariciones."""
        total = 0
        for rel in self.archivos():
            if rel in excepto:
                continue
            texto = self.leer(rel)
            n = texto.count(viejo)
            if n:
                self.escribir(rel, texto.replace(viejo, nuevo))
                total += n
        if total < minimo:
            raise ReglaRota(f"se esperaban al menos {minimo} apariciones de {viejo!r} y hay {total}")
        self.hechos += total
        return total

    def cambiar_filas(self, fuente, viejo, nuevo):
        """En los catálogos de idiomas, cambia `viejo` por `nuevo` en las filas cuyo texto en inglés es `fuente`."""
        total = 0
        for f in sorted(self.ruta("crates/ui-egui/src/i18n").glob("*.tsv")):
            rel = f.relative_to(self.raiz).as_posix()
            lineas = self.leer(rel).split("\n")
            for i, linea in enumerate(lineas):
                columnas = linea.split("\t")
                if len(columnas) >= 3 and columnas[1] == fuente:
                    lineas[i] = linea.replace(viejo, nuevo)
                    total += 1
            self.escribir(rel, "\n".join(lineas))
        if total == 0:
            raise ReglaRota(f"ningún catálogo tiene la fila {fuente!r}")
        self.hechos += total

    def copiar(self, origen, destino, debe_existir=True):
        d = self.ruta(destino)
        if debe_existir and not d.is_file():
            raise ReglaRota(f"{destino} ya no existe en el original")
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ACTIVOS / origen, d)
        self.hechos += 1

    def renombrar(self, viejo, nuevo):
        if not self.ruta(viejo).is_file():
            raise ReglaRota(f"{viejo} ya no existe en el original")
        self.ruta(viejo).rename(self.ruta(nuevo))
        self.hechos += 1

    def borrar(self, patron):
        for f in sorted(self.raiz.glob(patron)):
            if f.is_file():
                f.unlink()


def nombres(a):
    # Antes que nada, porque las reglas siguientes buscan el texto ya cambiado.
    a.cambiar_en_todos("ArtCraft Launcher", NOMBRE, minimo=100)
    a.cambiar_en_todos("ArtCraftLauncher", "SpicySuite", minimo=5)


def catalogo(a):
    c = "crates/core/src/catalog.rs"
    a.cambiar(c, 'pub const WEBSITE_URL: &str = "https://getartcraft.com";', f'pub const WEBSITE_URL: &str = "{SITIO}";')
    a.cambiar(
        c,
        'pub const SOCIAL: [(&str, &str); 5] = [\n'
        '    ("X", "https://x.com/get_artcraft"),\n'
        '    ("Instagram", "https://www.instagram.com/officialartcraftstudios"),\n'
        '    ("LinkedIn", "https://www.linkedin.com/company/artcraft-ai"),\n'
        '    ("YouTube", "https://www.youtube.com/@OfficialArtcraftStudios"),\n'
        '    ("TikTok", "https://www.tiktok.com/@artcraft.studios"),\n'
        '];',
        'pub const SOCIAL: [(&str, &str); 3] = [\n'
        '    ("Instagram", "https://www.instagram.com/spicyrender.mx"),\n'
        '    ("Facebook", "https://www.facebook.com/spicyrender"),\n'
        '    ("Behance", "https://www.behance.net/SPICYRENDER"),\n'
        '];',
    )
    a.cambiar(
        c,
        'pub const LAUNCHER: CraftApp = app(\n    "artcraft-launcher",\n',
        f'pub const LAUNCHER: CraftApp = app(\n    "{ID}",\n',
    )
    a.cambiar(c, '    "storytold/craft-launcher",\n);', f'    "{REPO}",\n);')
    a.cambiar(c, 'pub const LAUNCHER_REPO: &str = "storytold/craft-launcher";', f'pub const LAUNCHER_REPO: &str = "{REPO}";')
    a.cambiar(c, 'pub const LAUNCHER_ID: &str = "artcraft-launcher";', f'pub const LAUNCHER_ID: &str = "{ID}";')
    # El launcher lleva su propio identificador de macOS; las apps conservan el suyo.
    a.cambiar(
        c,
        '    pub fn bundle_id(&self) -> String {\n        format!("ai.storyteller.{}", self.id)\n    }',
        '    pub fn bundle_id(&self) -> String {\n'
        '        if self.id == LAUNCHER_ID {\n'
        f'            return "{ID_APP}".to_string();\n'
        '        }\n'
        '        format!("ai.storyteller.{}", self.id)\n'
        '    }',
    )


def identidad(a):
    a.cambiar("apps/artcraft-launcher/src/main.rs", 'const APP_ID: &str = "ai.storyteller.artcraft-launcher";', f'const APP_ID: &str = "{ID_APP}";')
    a.cambiar("crates/native/src/login.rs", 'const ID: &str = "ai.storyteller.artcraft-launcher";', f'const ID: &str = "{ID_APP}";')
    s = "crates/native/src/self_update.rs"
    a.cambiar(s, r'r"Software\Learning Machines LLC\Spicy Suite"', rf'r"Software\{EDITOR}\{NOMBRE}"')
    a.cambiar(s, "<string>ai.storyteller.artcraft-launcher</string>", f"<string>{ID_APP}</string>")
    u = "crates/native/src/single_instance.rs"
    a.cambiar(u, "const PORT: u16 = 47_413;", f"const PORT: u16 = {PUERTO};")
    a.cambiar(u, "artcraft-launcher:", f"{ID}:", veces=None)
    b = "apps/artcraft-launcher/build.rs"
    a.cambiar(b, '.set("CompanyName", "Learning Machines LLC")', f'.set("CompanyName", "{EDITOR}")')
    a.cambiar(
        b,
        '.set("LegalCopyright", "Copyright (c) the Spicy Suite authors. MIT OR Apache-2.0.")',
        '.set("LegalCopyright", "Spicy Suite, based on ArtCraft Launcher. Copyright (c) the ArtCraft Launcher authors. MIT OR Apache-2.0.")',
    )
    a.cambiar(b, '.set("OriginalFilename", "artcraft-launcher.exe")', f'.set("OriginalFilename", "{ID}.exe")')
    a.cambiar(b, '.set("InternalName", "artcraft-launcher")', f'.set("InternalName", "{ID}")')
    # El ejecutable se llama spicy-suite; el paquete de cargo conserva su nombre (Cargo.lock no cambia).
    t = "apps/artcraft-launcher/Cargo.toml"
    a.cambiar(t, 'default-run = "artcraft-launcher"', f'default-run = "{ID}"')
    a.cambiar(t, "publish = false\n", f'publish = false\nautobins = false\n\n[[bin]]\nname = "{ID}"\npath = "src/main.rs"\n')


def interfaz(a):
    a.cambiar("crates/ui-egui/src/icons.rs", "pub const ARTCRAFT_LOGO_ASPECT: f32 = 1038.05 / 108.0;", "pub const ARTCRAFT_LOGO_ASPECT: f32 = 1815.55 / 220.75;")
    a.cambiar(
        "crates/ui-egui/src/icons.rs",
        '        "LinkedIn" => egui::include_image!("../../../assets/social/linkedin.svg"),\n',
        '        "LinkedIn" => egui::include_image!("../../../assets/social/linkedin.svg"),\n'
        '        "Facebook" => egui::include_image!("../../../assets/social/facebook.svg"),\n'
        '        "Behance" => egui::include_image!("../../../assets/social/behance.svg"),\n',
    )
    th = "crates/ui-egui/src/theme.rs"
    a.cambiar(th, "accent: hex(0x2d81ff),", "accent: hex(0xe43330),", veces=2)
    a.cambiar(th, "accent_ink: hex(0x74aaff),", "accent_ink: hex(0xff6b66),")
    a.cambiar(th, "accent_ink: hex(0x1659c4),", "accent_ink: hex(0xb3201d),")
    # Textos de la marca: los enlaces de Discord y GitHub siguen siendo los de ArtCraft (soporte
    # de las apps), así que sus textos no cambian.
    a.cambiar_en_todos('tl!("ArtCraft")', f'tl!("{EDITOR}")')
    a.cambiar_filas("ArtCraft", "ArtCraft", EDITOR)
    a.cambiar_en_todos('"ArtCraft on {name}"', f'"{EDITOR} on {{name}}"')
    a.cambiar_filas("ArtCraft on {name}", "ArtCraft", EDITOR)
    a.cambiar_en_todos('"Visit getartcraft.com"', '"Visit spicyrender.studio"', minimo=2)
    a.cambiar_filas("Visit getartcraft.com", "getartcraft.com", "spicyrender.studio")


def windows(a):
    p = "packaging/windows/package.ps1"
    a.cambiar(p, "$Pkg = 'artcraft-launcher'", f"$Pkg = '{ID}'")
    a.cambiar(p, "cargo build --release --locked -p $Pkg --target $Target", "cargo build --release --locked -p artcraft-launcher --target $Target")
    a.cambiar(p, "FromHtml('#2d81ff')", "FromHtml('#e43330')")
    w = "packaging/windows/artcraft-launcher.wxs"
    a.cambiar(w, "Learning Machines LLC", EDITOR, veces=None)
    a.cambiar(w, 'UpgradeCode="1AC08DBF-D4CF-4BA4-A81E-CAA5C1004974"', f'UpgradeCode="{UPGRADE_CODE}"')
    a.cambiar(w, 'Guid="55DCC431-EBEF-4C11-BABB-6D78CE0ECF4E"', f'Guid="{GUID_APP}"')
    a.cambiar(w, 'Guid="870F3DFA-BC0F-497F-85D5-A361B04826AF"', f'Guid="{GUID_MENU}"')
    a.cambiar(w, 'Guid="CF06DCF3-BE5A-4A2B-B3BF-F553CC6E5D60"', f'Guid="{GUID_ESCRITORIO}"')
    a.cambiar(w, 'Value="https://getartcraft.com/apps"', f'Value="{SITIO}"')
    a.cambiar(w, 'Value="https://github.com/storytold/craft-launcher/releases"', f'Value="https://github.com/{REPO}/releases"')
    a.cambiar(w, 'Value="ai.storyteller.artcraft-launcher"', f'Value="{ID_APP}"', veces=2)
    a.cambiar(w, "artcraft-launcher.exe", f"{ID}.exe", veces=2)
    a.renombrar(w, f"packaging/windows/{ID}.wxs")
    a.renombrar("packaging/windows/artcraft-launcher.en-us.wxl", f"packaging/windows/{ID}.en-us.wxl")
    k = "packaging/windows/check-icons.ps1"
    a.cambiar(k, "'artcraft-launcher.wxs'", f"'{ID}.wxs'")
    a.cambiar(k, "$AppId = 'ai.storyteller.artcraft-launcher'", f"$AppId = '{ID_APP}'")
    a.cambiar("packaging/windows/sign.ps1", "'https://github.com/storytold/craft-launcher'", f"'https://github.com/{REPO}'")
    a.cambiar("packaging/windows/portable.txt", "artcraft-launcher.exe", f"{ID}.exe")


def macos(a):
    m = "packaging/macos/package.sh"
    a.cambiar(m, "PKG=artcraft-launcher ", f"PKG={ID} ")
    a.cambiar(m, 'cargo build --release --locked -p "$PKG"', "cargo build --release --locked -p artcraft-launcher")
    i = "packaging/macos/Info.plist.in"
    a.cambiar(i, "<string>ai.storyteller.artcraft-launcher</string>", f"<string>{ID_APP}</string>")
    a.cambiar(
        i,
        "<string>Copyright © 2026 ArtCraft Team and the Spicy Suite contributors. MIT OR Apache-2.0.</string>",
        "<string>Spicy Suite, based on ArtCraft Launcher. Copyright © 2026 ArtCraft Team and the ArtCraft Launcher contributors. MIT OR Apache-2.0.</string>",
    )


def activos(a):
    # Los archivos de marca de ArtCraft se reemplazan en su lugar: el código los sigue buscando
    # en la misma ruta y no hay que tocarlo.
    a.copiar("spicy-logo.svg", "docs/brand/artcraft-logo.svg")
    a.copiar("spicy-logo-white.svg", "docs/brand/artcraft-logo-white.svg")
    a.copiar("spicy-mark.svg", "docs/brand/artcraft-mark.svg")
    a.copiar("spicy-mark-black.svg", "docs/brand/artcraft-mark-black.svg")
    a.copiar("dmg-background.svg", "packaging/macos/dmg/background.svg")
    a.copiar("social/facebook.svg", "assets/social/facebook.svg", debe_existir=False)
    a.copiar("social/behance.svg", "assets/social/behance.svg", debe_existir=False)
    # Lo que se genera a partir de esos archivos se borra, para que la compilación falle si no se
    # vuelve a generar en vez de salir con el logo de ArtCraft.
    a.borrar("docs/brand/*.png")
    a.borrar("assets/app-icon/*.png")
    a.borrar("assets/app-icon/*.ico")
    a.borrar("assets/app-icon/*.icns")
    a.borrar("assets/app-icon/*.svg")
    a.borrar("assets/app-icon/hicolor/**/*")
    a.borrar("packaging/macos/dmg/background.tiff")
    a.borrar("packaging/macos/dmg/dmg-layout.DS_Store")


def revisar(a):
    """Lo que no debe quedar en el código que se compila."""
    prohibido = {
        # Solo queda en el crédito «based on ArtCraft Launcher» de los avisos de copyright.
        "ArtCraft Launcher": ("apps/artcraft-launcher/build.rs", "packaging/macos/Info.plist.in"),
        # icons.sh lo usa solo como nombre de archivo de los íconos, que se conserva.
        '"ai.storyteller.artcraft-launcher"': ("packaging/icons.sh",),
        '"storytold/craft-launcher"': (),
        "github.com/storytold/craft-launcher/": (),
        "getartcraft.com/apps\"": (),
        # El editor de las apps sí se queda: es como el launcher las reconoce instaladas.
        "Learning Machines LLC": ("crates/native/src/detect.rs",),
    }
    quedan = []
    for rel in a.archivos():
        texto = a.leer(rel)
        for viejo, permitido in prohibido.items():
            if viejo in texto and rel not in permitido and not rel.endswith("/tests.rs") and "/tests/" not in rel:
                quedan.append(f"{rel}: {viejo!r} ×{texto.count(viejo)}")
    return quedan


def iconos(a):
    """Después de packaging/icons.sh: los empaquetadores buscan los íconos con el nombre nuevo."""
    for ext in ("ico", "icns"):
        origen = a.ruta(f"assets/app-icon/artcraft-launcher.{ext}")
        if not origen.is_file():
            raise ReglaRota(f"falta {origen.name}: ¿corrió packaging/icons.sh?")
        shutil.copyfile(origen, a.ruta(f"assets/app-icon/{ID}.{ext}"))
    for rel in ("docs/brand/artcraft-mark-64.png", "docs/brand/artcraft-mark-black-44.png", "assets/app-icon/hicolor/256x256/apps/ai.storyteller.artcraft-launcher.png"):
        if not a.ruta(rel).is_file():
            raise ReglaRota(f"falta {rel}: ¿corrió packaging/icons.sh?")


def main(args):
    if not args or args[0].startswith("-"):
        print(__doc__)
        return 2
    try:
        a = Arbol(args[0])
        if "--iconos" in args[1:]:
            iconos(a)
            print("íconos listos")
            return 0
        for paso in (nombres, catalogo, identidad, interfaz, windows, macos, activos):
            paso(a)
        quedan = revisar(a)
    except ReglaRota as e:
        print(f"error: {e}", file=sys.stderr)
        print("El original cambió una parte que la marca modifica: actualice la regla en marca/aplicar.py.", file=sys.stderr)
        return 1
    if quedan:
        print("error: quedan textos del original que la marca debía cambiar:", file=sys.stderr)
        for q in quedan:
            print(f"  {q}", file=sys.stderr)
        return 1
    print(f"marca aplicada: {a.hechos} cambios")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
