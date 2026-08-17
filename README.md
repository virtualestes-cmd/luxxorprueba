# Luxxor Vacation — Landing

Primera pantalla (hero animado) de la web de Luxxor Vacation.
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
| 0.32 → 0.58 | Entra el wordmark **LUXXOR vacation** a pantalla completa |
| 0.78 → 0.95 | El wordmark se va |
| 0.72 → 1.00 | Un velo marfil entrega la pantalla a la siguiente sección |

## Estructura

```
index.html              Marcado del hero + adelanto de la sección siguiente
assets/css/styles.css   Todo el diseño y toda la animación
assets/js/hero.js       Solo calcula el progreso del scroll (0 → 1)
assets/img/villa.svg    Placeholder de la arquitectura
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

En vez del azul cielo del ejemplo de referencia, el cielo va de navy profundo
a hora dorada en el horizonte: mismo mecanismo, paleta de la marca.

Las tipografías se cargan desde Google Fonts. Si se prefiere no depender de un
tercero, hay que descargarlas a `assets/fonts/` y declararlas con `@font-face`.

## Pendiente

- Fotografía real de arquitectura en lugar del SVG.
- Resto de secciones de la home.
- Textos definitivos (los actuales son de trabajo).
