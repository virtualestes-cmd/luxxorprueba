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
| 0 → 0.30 | El titular y la navegación se desvanecen y se difuminan |
| 0 → 0.80 | La villa asciende y se acerca; las nubes se abren |
| 0.32 → 0.58 | Entra el wordmark **LUXXOR PROJECTS** a pantalla completa |
| 0.78 → 0.95 | El wordmark se va |
| 0.72 → 1.00 | Un velo marfil entrega la pantalla a la siguiente sección |

## Estructura

```
index.html              Marcado del hero + adelanto de la sección siguiente
assets/css/styles.css   Todo el diseño y toda la animación
assets/js/hero.js       Solo calcula el progreso del scroll (0 → 1)
assets/img/villa.svg    Placeholder de la arquitectura
assets/img/clouds-*.png Nubes (lo que carga la web)
assets/img/clouds-*.svg Fuente de las nubes, para regenerarlas
```

El reparto es a propósito: **el JS no anima nada**. Publica el progreso del
scroll como variables CSS (`--p`, `--p-copy`, `--p-villa`, `--p-mark`,
`--p-mark-out`, `--p-veil`) y el CSS decide qué hacer con ellas. Para cambiar
el ritmo de la animación se tocan los tramos en `hero.js`; para cambiar el
aspecto, solo el CSS.

## Cómo tocar las cosas

- **Velocidad de la animación**: `.hero { height: 320vh }` en el CSS. Más alto = más lento.
- **Momento de cada fase**: los rangos al final de `hero.js`.
- **Colores**: las variables de `:root` en el CSS, ya cargadas con la paleta del design system.
- **Foto real en vez del SVG**: sustituir `assets/img/villa.svg` por una imagen
  de la villa recortada sobre fondo transparente (PNG/WebP). No hay que tocar
  el CSS: misma caja, misma máscara de fundido.

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

## Pendiente

- Fotografía real de arquitectura en lugar del SVG.
- Resto de secciones de la home.
- Textos definitivos (los actuales son de trabajo).
