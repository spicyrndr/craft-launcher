#!/usr/bin/env python3
"""Genera la página de suite.spicyrender.studio.

    python sitio/hacer.py --original <código de ArtCraft Launcher> --version <release.json> --salida _sitio

De la versión del original con la que se compiló Spicy Suite toma la lista de programas (nombre,
descripción en español, colores e íconos); de la publicación de Spicy Suite (la respuesta de
`gh api repos/spicyrndr/craft-launcher/releases/latest`), los enlaces de descarga. Si el original
agrega un programa, aparece solo en la página.
"""

import argparse
import datetime
import html
import json
import pathlib
import re
import shutil
import sys

AQUI = pathlib.Path(__file__).resolve().parent
ACTIVOS = AQUI.parent / "marca" / "activos"

# Para ubicar cada programa de un vistazo. Un programa nuevo sin fila aquí sale sin esta línea.
ALTERNATIVA = {
    "photocraft": "Photoshop",
    "vectorcraft": "Illustrator",
    "filmcraft": "Premiere Pro y DaVinci Resolve",
    "lightcraft": "Lightroom",
    "pdfcraft": "Acrobat",
    "effectcraft": "After Effects",
    "designcraft": "InDesign",
    "wordcraft": "Word",
    "deckcraft": "PowerPoint y Keynote",
    "gridcraft": "Excel",
    "cadcraft": "AutoCAD",
    "soundcraft": "Audition",
    "figcraft": "Figma",
}
GRUPOS = {"Classic": "Clásicos", "New": "Nuevos"}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
# México no cambia de horario desde 2022.
MEXICO = datetime.timezone(datetime.timedelta(hours=-6))
DESCARGAS = {
    "msi": "-windows-x64.msi",
    "zip": "-windows-x64-portable.zip",
    "dmg": "-macos-universal.dmg",
}

APP = re.compile(
    r'app\(\s*"(?P<id>[a-z0-9-]+)",\s*"(?P<nombre>[^"]+)",\s*"(?P<tagline>[^"]+)",\s*AppGroup::(?P<grupo>\w+),\s*'
    r"\[\[(?P<color>[^\]]+)\],\s*\[(?P<claro>[^\]]+)\],\s*\[(?P<oscuro>[^\]]+)\]\],\s*\"(?P<repo>[^\"]+)\",?\s*\)"
)


class Falla(Exception):
    pass


def hex_rgb(texto):
    partes = [int(x.strip(), 16) for x in texto.split(",")]
    if len(partes) != 3:
        raise Falla(f"color inesperado: {texto}")
    return "#" + "".join(f"{p:02x}" for p in partes)


def programas(original):
    catalogo = (original / "crates/core/src/catalog.rs").read_text(encoding="utf-8")
    inicio = catalogo.find("pub const SUITE")
    fin = catalogo.find("\n];", inicio)
    if inicio < 0 or fin < 0:
        raise Falla("no se encontró la lista SUITE en catalog.rs")
    apps = [m.groupdict() for m in APP.finditer(catalogo[inicio:fin])]
    total = re.search(r"pub const SUITE: \[CraftApp; (\d+)\]", catalogo)
    if not apps or not total or len(apps) != int(total.group(1)):
        raise Falla(f"se leyeron {len(apps)} programas de catalog.rs y la lista dice {total.group(1) if total else '?'}")
    # Las descripciones en español: filas «id<TAB>inglés<TAB>español» del catálogo de idiomas.
    es = {}
    for linea in (original / "crates/ui-egui/src/i18n/es.tsv").read_text(encoding="utf-8").splitlines():
        col = linea.split("\t")
        if len(col) >= 3:
            es[(col[0], col[1])] = col[2]
    for a in apps:
        a["descripcion"] = es.get((a["id"], a["tagline"]), a["tagline"])
        a["color"], a["oscuro"] = hex_rgb(a["color"]), hex_rgb(a["oscuro"])
        a["icono"] = original / "assets/app-icons" / f"{a['id']}.png"
        if not a["icono"].is_file():
            raise Falla(f"falta el ícono de {a['nombre']}")
    return apps


def descargas(version):
    datos = json.loads(pathlib.Path(version).read_text(encoding="utf-8"))
    etiqueta = datos["tag_name"]
    numero = etiqueta.removeprefix("v")
    archivos = {}
    for clave, fin in DESCARGAS.items():
        nombre = f"spicy-suite-{numero}{fin}"
        a = next((x for x in datos["assets"] if x["name"] == nombre), None)
        if a is None:
            raise Falla(f"la publicación {etiqueta} no tiene {nombre}")
        archivos[clave] = {"nombre": nombre, "url": a["browser_download_url"], "mb": f"{a['size'] / 1e6:.1f}"}
    sumas = next((x["browser_download_url"] for x in datos["assets"] if x["name"] == "SHA256SUMS.txt"), datos["html_url"])
    f = datetime.datetime.fromisoformat(datos["published_at"].replace("Z", "+00:00")).astimezone(MEXICO)
    return {
        "etiqueta": etiqueta,
        "version": numero,
        "fecha": f"{f.day} de {MESES[f.month - 1]} de {f.year}",
        "pagina": datos["html_url"],
        "sumas": sumas,
        "archivos": archivos,
    }


def tarjeta(i, a):
    nombre = a["nombre"]
    marca = "Craft" if nombre.endswith("Craft") else ""
    inicio = html.escape(nombre[: len(nombre) - len(marca)])
    alternativa = ALTERNATIVA.get(a["id"])
    alt = f'<p class="app-alt">Alternativa a {html.escape(alternativa)}</p>' if alternativa else ""
    return (
        f'<li class="app" style="--app: {a["color"]}; --tinta: {a["oscuro"]}">'
        f'<span class="app-num">{i:02d}</span>'
        f'<img src="apps/{a["id"]}.png" alt="" width="56" height="56" loading="lazy">'
        f'<div><p class="app-nombre">{inicio}<span>{marca}</span></p>'
        f'<p class="app-desc">{html.escape(a["descripcion"])}</p>{alt}</div></li>'
    )


def grupos(apps):
    partes = []
    i = 0
    for clave, titulo in GRUPOS.items():
        del_grupo = [a for a in apps if a["grupo"] == clave]
        if not del_grupo:
            continue
        tarjetas = []
        for a in del_grupo:
            i += 1
            tarjetas.append(tarjeta(i, a))
        partes.append(
            f'<div class="grupo"><h3 class="rotulo">{titulo} <span>{len(del_grupo)}</span></h3>'
            f'<ul class="apps">{"".join(tarjetas)}</ul></div>'
        )
    if i != len(apps):
        raise Falla("hay programas de un grupo desconocido")
    return "".join(partes)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--original", required=True, type=pathlib.Path)
    p.add_argument("--version", required=True)
    p.add_argument("--salida", required=True, type=pathlib.Path)
    args = p.parse_args()
    try:
        apps = programas(args.original)
        d = descargas(args.version)
    except (Falla, KeyError, ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    valores = {
        "VERSION": d["version"],
        "ETIQUETA": d["etiqueta"],
        "FECHA": d["fecha"],
        "PAGINA_VERSION": d["pagina"],
        "SUMAS": d["sumas"],
        "N": str(len(apps)),
        "GRUPOS": grupos(apps),
    }
    for clave, a in d["archivos"].items():
        valores[f"{clave.upper()}_URL"] = a["url"]
        valores[f"{clave.upper()}_NOMBRE"] = a["nombre"]
        valores[f"{clave.upper()}_MB"] = a["mb"]
    pagina = (AQUI / "plantilla.html").read_text(encoding="utf-8")
    for clave, valor in valores.items():
        pagina = pagina.replace("{{" + clave + "}}", valor)
    sobrantes = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", pagina)))
    if sobrantes:
        print(f"error: la plantilla tiene marcas sin valor: {', '.join(sobrantes)}", file=sys.stderr)
        return 1

    salida = args.salida
    if salida.exists():
        shutil.rmtree(salida)
    (salida / "apps").mkdir(parents=True)
    (salida / "index.html").write_text(pagina, encoding="utf-8", newline="\n")
    for f in (AQUI / "public").iterdir():
        shutil.copyfile(f, salida / f.name)
    for nombre in ("spicy-logo-white.svg", "spicy-mark.svg"):
        shutil.copyfile(ACTIVOS / nombre, salida / nombre)
    for a in apps:
        shutil.copyfile(a["icono"], salida / "apps" / f"{a['id']}.png")
    print(f"página lista: Spicy Suite {d['version']}, {len(apps)} programas → {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
