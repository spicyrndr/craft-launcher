"""Genera los SVG de marca/activos/ con los trazos del logo de Spicy Render.

    python marca/hacer_svg.py marca/activos

Los trazos vienen de 01_Marca/logo/svg/spicy_negroOK.svg (carpeta de marca de Spicy Render). El
logo horizontal reproduce la composición de 01_Marca/logo/png/spicy-v1.png, medida en ese PNG:
RNDR va 964.2 unidades a la derecha de SPICY y 283 más arriba.
"""
import pathlib
import sys

salida = pathlib.Path(sys.argv[1])
salida.mkdir(parents=True, exist_ok=True)

ROJO = "#E43330"

SPICY = [
    '<path d="M402.69,281.11h-32.5v42.04H318.3v171.83h52.1v-76.77h32.29c54.53,0,78.6-32.9,78.6-68.24C481.29,310.67,455.09,281.11,402.69,281.11z M398.73,376.78H370.4v-53.62h28.33c20.72,0,29.55,10.36,29.55,26.81C428.28,366.42,419.45,376.78,398.73,376.78z"/>',
    '<rect x="502.61" y="281.11" width="52.1" height="213.87"/>',
    '<path d="M684.8,449.28c-31.99,0-53.92-23.76-53.92-61.54s21.93-61.54,53.92-61.54c9.9,0,18.89,2.28,26.51,6.85c3.44,2.06,6.6,4.59,9.43,7.59c2.33,2.46,4.43,5.23,6.31,8.32L765,312l0.03-0.03c-18.75-21.19-46.55-33.3-79.63-33.3c-63.06,0-107.54,45.09-107.54,109.07s44.48,108.76,107.54,108.76c50.88,0,89.26-28.33,101.45-74.64h-57.28C720.75,440.14,704.6,449.28,684.8,449.28z"/>',
    '<path d="M186.39,339.3c0-13.4,9.44-19.8,21.94-19.5c6.27,0.14,11.68,1.86,15.83,4.94c2.32,1.72,4.23,3.87,5.7,6.4L266,295l0.11-0.12c-13.94-10.97-33.48-16.81-56.87-16.81c-44.79,0-77.99,22.54-77.99,63.06c-0.61,75.86,106.33,54.53,106.33,94.14c0,12.49-9.75,20.11-24.98,20.11l1.52,41.74c49.96,0,77.99-29.86,77.99-65.81C292.1,359.71,186.39,376.47,186.39,339.3z"/>',
    '<polygon points="855.4,281.11 796.3,281.11 870.33,424.3 870.33,494.98 922.42,494.98 922.42,424.3 896.83,370.68"/>',
    '<polygon points="905.83,351.57 931.42,405.19 995.57,281.11 938.19,281.11 912.54,336.97"/>',
]
RNDR = [
    '<path d="M255.24,697.13c32.9-9.75,47.53-35.04,47.53-61.85c0-37.17-26.2-67.33-78.6-67.33h-87.44v213.87h52.1v-80.6l-0.16,0l0.16-0.13v0.13l12.49-0.13l44.48,80.73h58.8L255.24,697.13z M249.75,632.86c-0.22,13.22-9.37,21.14-28.63,21.14h-32.29v-42.79h32.29c19.5,0,28.64,8.36,28.64,21.15C249.76,632.53,249.75,632.69,249.75,632.86z"/>',
    '<path d="M221.12,611.21c19.26,0,28.4,8.54,28.63,21.64c0-0.17,0.01-0.33,0.01-0.5C249.76,619.57,240.62,611.21,221.12,611.21z"/>',
    '<polygon points="484.03,700.48 396.9,567.95 344.8,567.95 344.8,781.82 396.9,781.82 396.9,649.9 484.03,781.82 536.13,781.82 536.13,567.95 484.03,567.95"/>',
    '<path d="M635.19,568v44.15h-51.84v169.67h80.12c68.24,0,112.11-43.57,112.11-106.93c0-63.67-43.87-106.93-112.11-106.93 M660.12,736.73h-24.68v-124.3h24.68c39.3,0,62.46,23.15,62.46,62.46S699.42,736.73,660.12,736.73z"/>',
    '<path d="M933.24,697.13c32.9-9.75,47.53-35.04,47.53-61.85c0-37.17-26.2-67.33-78.6-67.33h-87.44v213.87h52.1v-80.6l12.49-0.13l44.48,80.73h58.8L933.24,697.13z M866.83,611.21h32.29c19.26,0,28.4,8.54,28.63,21.64c-0.22,13.22-9.37,21.14-28.63,21.14h-32.29V611.21z"/>',
]

# Cajas medidas en el navegador (getBBox) sobre los trazos de arriba.
APILADO = (131.25, 278.07, 995.57, 781.82)  # x0, y0, x1, y1
DX, DY = 964.2, -283.0
HORIZONTAL = (131.25, 278.07, 982.60 + DX, 781.82 + DY)

AVISO = "<!-- Spicy Render. Trazos de 01_Marca/logo/svg/spicy_negroOK.svg; no es parte de la licencia MIT/Apache. -->"


def grupo(partes):
    return "".join(partes)


def horizontal(color):
    x0, y0, x1, y1 = HORIZONTAL
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0:.2f} {y1 - y0:.2f}">{AVISO}'
        f'<g fill="{color}">{grupo(SPICY)}<g transform="translate({DX} {DY})">{grupo(RNDR)}</g></g></svg>\n'
    )


def apilado_en(cx, cy, ancho, color):
    """El logo apilado, con su centro en (cx, cy) y el ancho dado."""
    x0, y0, x1, y1 = APILADO
    s = ancho / (x1 - x0)
    tx = cx - s * (x0 + x1) / 2
    ty = cy - s * (y0 + y1) / 2
    return f'<g fill="{color}" transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{grupo(SPICY)}{grupo(RNDR)}</g>'


(salida / "spicy-logo.svg").write_text(horizontal("#0b0b0c"), encoding="utf-8")
(salida / "spicy-logo-white.svg").write_text(horizontal("#ffffff"), encoding="utf-8")

# Ícono: cuadrado rojo con el logo blanco, como el favicon del sitio. El viewBox es el que
# packaging/icons.sh espera del ícono original (le suma margen para la versión de macOS).
caja = (-10, -19.42, 136.34)
cx, cy = caja[0] + caja[2] / 2, caja[1] + caja[2] / 2
(salida / "spicy-mark.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -19.42 136.34 136.34">{AVISO}'
    f'<rect x="-10" y="-19.42" width="136.34" height="136.34" fill="{ROJO}"/>'
    f"{apilado_en(cx, cy, 136.34 * 0.765, '#ffffff')}</svg>\n",
    encoding="utf-8",
)

# Barra de menús de macOS (imagen plantilla: solo cuenta la transparencia): cuadrado negro con
# las letras caladas.
(salida / "spicy-mark-black.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{AVISO}'
    '<defs><mask id="letras"><rect width="100" height="100" fill="#fff"/>'
    f"{apilado_en(50, 50, 72, '#000')}</mask></defs>"
    '<rect x="4" y="4" width="92" height="92" fill="#000" mask="url(#letras)"/></svg>\n',
    encoding="utf-8",
)

# Fondo de la ventana del DMG (660 × 400 pt): panel rojo con el logo y una flecha de la app a
# Aplicaciones. Sin texto, para no depender de fuentes al renderizar. Los íconos van en (326, 205)
# y (574, 205), en cajas de 128 pt; la flecha deja 10 pt libres a cada lado.
(salida / "dmg-background.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="660" height="400" viewBox="0 0 660 400">'
    f"{AVISO}"
    '<rect width="660" height="400" fill="#f2f1ee"/>'
    f'<rect width="232" height="400" fill="{ROJO}"/>'
    f"{apilado_en(116, 200, 150, '#ffffff')}"
    '<line x1="232.5" y1="0" x2="232.5" y2="400" stroke="#0b0b0c" stroke-width="1.2"/>'
    '<line x1="236.5" y1="0" x2="236.5" y2="400" stroke="#0b0b0c" stroke-width="0.5"/>'
    '<line x1="404" y1="205" x2="490" y2="205" stroke="#0b0b0c" stroke-width="1.2"/>'
    '<polygon points="489,199.5 499,205 489,210.5" fill="#0b0b0c"/></svg>\n',
    encoding="utf-8",
)
print("listo:", ", ".join(sorted(p.name for p in salida.glob("*.svg"))))
