# Luxxor Projects — Landing

Primera pantalla (hero animado) de la web de Luxxor Projects.
Es una prueba: HTML, CSS y JS planos, sin build ni dependencias.

## Cómo verlo

Abrir `index.html` en el navegador. Si el navegador bloquea algo, servirlo en local:

```bash
python3 -m http.server 8000
# luego: http://localhost:8000
```

## Qué hace

Al scrollear, la pantalla del hero se queda fija y va pasando esto:

| Progreso | Qué ocurre |
|---------:|------------|
| 0 → 0.26 | El titular y la navegación se desvanecen |
| 0 → 0.70 | La villa asciende, se acerca y sale por arriba |
| 0.16 → 0.62 | El mar de nubes sube y se traga la villa |
| 0.05 → 0.24 | El nombre **LUXXOR** asoma casi al instante, translúcido, por encima de la casa |
| 0.48 → 0.72 | Coge cuerpo cuando la villa se va: la arquitectura se ve dentro de las letras, con **Real Estate** debajo |
| 0.78 → 0.97 | Las nubes suben y se lo tragan, entregando la pantalla a la sección siguiente |

Después del hero vienen tres secciones: la **colección** de villas, el **reel**
(con el vídeo pendiente) y la **introducción a Luxxor**.

## Estructura

```
index.html              Hero + reel + introducción
assets/css/styles.css   Todo el diseño y toda la animación
assets/js/hero.js       Solo calcula el progreso del scroll (0 → 1)
assets/js/villas.js     Galería a pantalla completa de cada villa
assets/img/villas/      Fotografías, una carpeta por referencia
docs/villas/            Datos publicables de cada villa
assets/img/villa.webp   Fotografía de la villa (lo que carga la web)
assets/img/villa.png    Original sin recortar, por si hay que re-exportar
assets/img/clouds-*.png Nubes: high (altas), low (mar de nubes), front (niebla de la base)
assets/img/clouds-*.svg Fuente de las nubes, para regenerarlas
assets/video/           Metraje del reel (ver el README de la carpeta)
```

El reparto es a propósito: **el JS no anima nada**. Publica el progreso del
scroll como variables CSS (`--p`, `--p-copy`, `--p-villa`, `--p-mark`,
`--p-veil`, `--p-settle`) y el CSS decide qué hacer con ellas. Para cambiar
el ritmo de la animación se tocan los tramos en `hero.js`; para cambiar el
aspecto, solo el CSS.

## Cómo tocar las cosas

- **Velocidad de la animación**: `.hero { height: 320vh }` en el CSS. Más alto = más lento.
- **Momento de cada fase**: los rangos al final de `hero.js`.
- **Colores**: las variables de `:root` en el CSS, ya cargadas con la paleta del design system.
- **Cambiar la fotografía de la villa**: tiene que venir recortada sobre fondo
  transparente y ajustada al edificio, sin margen sobrante. Al cambiarla hay
  que actualizar `width`/`height` en el `<img>` y, si la proporción cambia
  mucho, el `width` y el `bottom` de `.villa` en el CSS.

## Design system

Sigue el documento interno de Luxxor:

- Navy `#061B36` dominante, dorado `#D6A34A` solo como acento, marfil `#F5F2EA`, carbón `#16191D`.
- Serif editorial (Cormorant Garamond) en titulares; sans (Inter) en interfaz.
- Animaciones lentas y suaves, sin glow ni efectos futuristas.

El cielo es un degradado real de última hora de la tarde: arranca en el navy de
marca en el cenit y baja a azul, azul pálido y bruma cálida en el horizonte.

Las nubes no son formas dibujadas: son dos capas de ruido fractal generado con
`feTurbulence`, recortado con una curva de contraste (`feComponentTransfer`)
para que aparezcan siluetas en vez de niebla. Al no ser figuras, no se repiten
de forma reconocible.

Los `.svg` son la fuente y los `.png` son lo que carga la web. El ruido se
rasteriza una sola vez: si el navegador tiene que calcularlo en cada fotograma,
el hero se arrastra. Para cambiar las nubes se editan los `.svg` —
`baseFrequency` manda en el tamaño y el `slope`/`intercept` de la curva en
cuántas hay y cómo de densas— y luego se vuelven a exportar a `.png` al mismo
tamaño, con fondo transparente.

## Rendimiento

El hero mueve varias capas a pantalla completa, así que hay tres reglas que no
conviene romper:

1. **Animar solo `transform` y `opacity`.** Son las dos propiedades que la GPU
   compone sin repintar. La deriva de las nubes se hacía con
   `background-position` y costaba un repintado de pantalla completa por
   fotograma; ahora es un `translateX` sobre una capa interior más ancha.
2. **Nada de `filter` ni `backdrop-filter` sobre elementos que se mueven.**
   Un `blur()` animado sobre el titular obliga a rasterizarlo en cada
   fotograma.
3. **Ningún filtro SVG en caliente.** El ruido de las nubes va horneado a PNG.

Medido con scroll automatizado a 1440x900 y sin GPU: de 168 ms por fotograma
(unos 6 fps) a 17 ms (el techo de 60 fps).

Las tipografías se cargan desde Google Fonts. Si se prefiere no depender de un
tercero, hay que descargarlas a `assets/fonts/` y declararlas con `@font-face`.

## El wordmark con la fotografía dentro

Las letras no son texto de color: son una ventana a `villa.webp`. El fondo de
la caja se recorta a la forma de los glifos con `background-clip: text`, y el
texto va en `transparent`. **Todas** las letras llevan la fotografía dentro,
también las XX: el dorado se queda en el logotipo de la navegación, que es
donde el sistema visual lo pide.

**Va en sans, no en serif.** En la referencia el nombre es una sans muy
gruesa, con las letras anchas y casi pegadas. Con una serif de trazo fino y
espaciada no hay superficie dentro de los glifos donde se vea la fotografía, y
el efecto no se lee por mucho que se ajuste el tamaño.

La familia es **Archivo**, que es variable y tiene eje de anchura: con
`wdth 125` cada glifo se ensancha de verdad y la palabra sigue siendo estrecha.
Estirar con `scaleX` habría deformado también el espaciado. Las dos X se montan
ligeramente entre sí, como en el logotipo.

El bloque son dos líneas, como la referencia: el nombre y **Real Estate**
debajo, en sans sólida gris, a alrededor del 40% de su altura. El descriptor
del logotipo se queda en la navegación.

La imagen va **ampliada** (`background-size: 260%`), no en `cover`: a tamaño
`cover` la villa entera cabía dentro de una sola letra y no se reconocía nada.
Ampliada se ven fachadas, ventanas e interiores dentro de los glifos, que es
el efecto de la referencia. Para cambiar qué se ve dentro basta con mover el
`background-position` de `.wordmark__word`, o cambiar la imagen.

## Las nubes que tapan la base de la villa

La fotografía se corta en seco donde acaba la piscina. Se resuelve con dos
cosas a la vez, y hacen falta las dos:

1. **Un fundido corto** en `.villa__photo`, solo el 14% final. Un fundido
   largo dejaba media casa translúcida —se veía el cielo a través del agua—,
   que queda peor que el propio corte.
2. **Cúmulos densos por delante**, `.villa__mist`, colocados de forma que el
   canto de la fotografía caiga en su franja más opaca.

La nube va **dentro** de `.villa`, no como capa aparte: así viaja con ella y
no añade otra capa a pantalla completa que componer en cada fotograma. Medido:
como capa suelta costaba 11 ms por fotograma; dentro de la villa, nada.

Lleva fundido en sus dos bordes. Con el canto inferior lleno, la propia nube
cruzaba la pantalla como una franja blanca recta al subir con la villa.

## La colección de villas

Cuatro propiedades, cada una con sus cinco fotografías en
`assets/img/villas/<ref>/`. Los datos salen de `docs/villas/<ref>.md`, extraídos
de los dossiers.

Dos reglas que vienen del cliente y conviene no romper:

- **Cada propiedad se identifica solo por su referencia** (S023, S024…), nunca
  por el nombre comercial que figura en el dossier. Es lo que protege la
  exclusiva.
- **El precio no se publica.** Va detrás del botón *Request price*.

Al pinchar una tarjeta se abre la galería a pantalla completa: flechas, teclado
y deslizar en táctil. Ojo con `.lightbox[hidden]`: sin esa regla, el
`display: flex` anula el `hidden` del navegador y la capa se queda encima
capturando los clics de toda la página.

## Pendiente

- **Metraje del reel**: dejar `assets/video/reel.mp4`. Mientras no exista se
  ve un placeholder marcado.
- Logotipo en archivo (el wordmark está reconstruido con tipografía).
- Resto de secciones de la home.
- Destino de los CTAs y del botón *View more villas* (las 30 y pico restantes).
- Confirmar si las zonas concretas (Sa Caleta, Can Rimbau…) son publicables.
