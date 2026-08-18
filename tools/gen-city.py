# -*- coding: utf-8 -*-
"""Genera el skyline animado que va DENTRO de las letras de LUXXOR.

Escala: la caja es 1200x300 y la tinta de las letras va de y=73 a y=228.
Para que dentro del asta de una letra (~50px) se lea "ciudad" y no "textura",
los edificios son estrechos, con cielo por encima y huecos entre ellos.

Las franjas se **hornean a WebP**. Dibujadas como cientos de <rect> vectoriales
el hero se repintaba entero en cada fotograma (medido: +7 ms). Como imagen, la
deriva es un translate y no cuesta nada. Misma regla que las nubes.
"""
import random, re, io, os, glob, json

W, H = 1200, 300
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img')
CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
random.seed(23)

SKY = ('<linearGradient id="citySky" x1="0" y1="0" x2="0" y2="1">'
       '<stop offset="0" stop-color="#061B36"/>'
       '<stop offset=".38" stop-color="#1D4670"/>'
       '<stop offset=".68" stop-color="#6E6E86"/>'
       '<stop offset=".86" stop-color="#C98A52"/>'
       '<stop offset="1" stop-color="#E6B378"/>'
       '</linearGradient>')

PATTERNS = (
  '<pattern id="winFar" width="9" height="12" patternUnits="userSpaceOnUse">'
    '<rect x="2" y="3" width="4" height="5" fill="#E4D6BC" opacity=".34"/></pattern>'
  '<pattern id="winMid" width="12" height="15" patternUnits="userSpaceOnUse">'
    '<rect x="3" y="4" width="6" height="7" fill="#FFD79A" opacity=".62"/></pattern>'
  '<pattern id="winNear" width="14" height="17" patternUnits="userSpaceOnUse">'
    '<rect x="3" y="4" width="7" height="8" fill="#FFE3B0" opacity=".66"/></pattern>'
)

def band(y_min, y_max, w_min, w_max, gap_min, gap_max, color, pat):
    """Una franja de skyline, dibujada hasta pasar de W para poder repetirla."""
    out, x = [], 0
    while x < W + 120:
        bw = random.randint(w_min, w_max)
        top = random.randint(y_min, y_max)
        h = H - top
        out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, top, bw, h, color))
        out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#%s)"/>' % (x, top, bw, h, pat))
        if bw > 34 and random.random() < .45:
            # remate: azotea escalonada o antena. Es lo que da lectura de ciudad.
            if random.random() < .5:
                rw = int(bw * .5)
                out.append('<rect x="%d" y="%d" width="%d" height="14" fill="%s"/>' % (x + (bw - rw) // 2, top - 14, rw, color))
            else:
                out.append('<rect x="%d" y="%d" width="4" height="20" fill="%s"/>' % (x + bw // 2, top - 20, color))
        x += bw + random.randint(gap_min, gap_max)
    return ''.join(out), x

def traffic(y, n, color, r, op):
    """Faros: a tamaño de letra, esto es lo que se ve moverse antes que el
    paralaje del skyline."""
    xs = sorted(random.sample(range(0, W), n))
    return ''.join('<rect x="%d" y="%d" width="%d" height="3" rx="1.5" fill="%s" opacity="%s"/>'
                   % (x, y + random.randint(-3, 3), r, color, op) for x in xs), W

LAYERS = []   # (nombre, markup, ancho, duración)
b, w = band(168, 218, 26, 52, 6, 16, '#3C5F84', 'winFar');  LAYERS.append(('city-far',  b, w, '110s'))
b, w = band(128, 186, 30, 62, 8, 20, '#16324F', 'winMid');  LAYERS.append(('city-mid',  b, w, '62s'))
b, w = band( 86, 158, 34, 76, 10, 26, '#04101E', 'winNear');LAYERS.append(('city-near', b, w, '34s'))
b, w = traffic(206, 22, '#FFE9C0', 9, '.8');                LAYERS.append(('city-traf1', b, w, '9s'))
b, w = traffic(218, 26, '#FFF3DA', 7, '.72');               LAYERS.append(('city-traf2', b, w, '6.5s'))

# --- horneado -------------------------------------------------------------
SCALE = 1
os.makedirs('/tmp/bake', exist_ok=True)
for name, markup, w, _dur in LAYERS:
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
           '<defs>%s</defs>%s</svg>' % (w, H, w * SCALE, H * SCALE, PATTERNS, markup))
    io.open('/tmp/bake/%s.svg' % name, 'w', encoding='utf-8').write(svg)

# El cielo se hornea aparte, del ancho de la caja, sin transparencia.
io.open('/tmp/bake/city-sky.svg', 'w', encoding='utf-8').write(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
    '<defs>%s</defs><rect width="%d" height="%d" fill="url(#citySky)"/></svg>'
    % (W, H, W * SCALE, H * SCALE, SKY, W, H))

print('franjas:', ', '.join(n for n, _m, _w, _d in LAYERS))

# --- horneado a WebP ------------------------------------------------------
def hornear():
    """Rasteriza cada franja en Chromium y la recorta a su caja de tinta."""
    from playwright.sync_api import sync_playwright
    from PIL import Image
    man = {}
    files = sorted(glob.glob('/tmp/bake/*.svg'))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for f in files:
            svg = io.open(f, encoding='utf-8').read()
            w = int(re.search(r'width="(\d+)"', svg).group(1))
            h = int(re.search(r'height="(\d+)"', svg).group(1))
            pg = b.new_page(viewport={'width': min(w, 4000), 'height': h})
            pg.set_content('<style>html,body{margin:0;background:transparent}svg{display:block}</style>' + svg)
            pg.wait_for_timeout(250)
            png = f.replace('.svg', '.png')
            pg.locator('svg').screenshot(path=png, omit_background=True)
            pg.close()
            im = Image.open(png).convert('RGBA')
            name = os.path.basename(f).replace('.svg', '')
            # Recorte a la caja con tinta: la franja lejana solo ocupa el
            # tercio bajo, y dibujar el alto entero es superficie de
            # repintado regalada en cada fotograma.
            box = im.split()[3].getbbox() or (0, 0, im.width, im.height)
            im = im.crop(box)
            im.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=88, method=6)
            man[name] = {'x': box[0], 'y': box[1], 'w': im.width, 'h': im.height}
            print(' ', name, im.size)
        b.close()
    return man

MAN = hornear()

# --- markup ---------------------------------------------------------------
def layer(name, w, dur):
    """Cada franja va recortada a su caja de tinta (manifest) y colocada en su
    sitio; el desplazamiento del bucle sigue siendo el ancho original."""
    g = MAN[name]
    img = ('<image href="assets/img/%s.webp" x="%%d" y="%d" width="%d" height="%d"/>'
           % (name, g['y'], g['w'], g['h']))
    return ('<g class="city__band" style="--w:%dpx;--dur:%s">%s%s</g>'
            % (w, dur, img % g['x'], img % (g['x'] + w)))

svg = ('<svg class="wordmark__svg" viewBox="0 58 1200 184" role="img" aria-label="Luxxor">'
       '<defs><mask id="luxxorMask">'
         '<rect width="1200" height="300" fill="#000"/>'
         '<text class="wordmark__glyphs" x="600" y="228" text-anchor="middle" fill="#fff">LUXXOR</text>'
       '</mask></defs>'
       '<g mask="url(#luxxorMask)">'
       '<image href="assets/img/city-sky.webp" x="0" y="0" width="1200" height="300" preserveAspectRatio="none"/>'
       + ''.join(layer(n, w, d) for n, _m, w, d in LAYERS) +
       '</g></svg>')

src = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
new, n = re.subn(r'<svg class="wordmark__svg".*?</svg>', lambda m: svg, src, flags=re.S)
assert n == 1, 'no se encontró el bloque del wordmark'
io.open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(new)
print('svg:', len(svg), 'bytes')
