# Luxxor — contexto del proyecto

Web de **Luxxor Vacation**, la vertical de estancias privadas del ecosistema Luxxor.

## Antes de tocar diseño o copy

Lee **`docs/luxxor-brand-context.md`**. Es la fuente de verdad de la marca y manda sobre
cualquier criterio genérico. Lo que sigue es solo el resumen operativo.

## Reglas que no se negocian

- **No inventar información empresarial**: ni números, ni propiedades, ni destinos
  concretos, ni años de experiencia, ni partners, ni testimonios, ni estadísticas.
  Si falta un dato real, poner un placeholder evidente o preguntar.
- **No sobrevender.** Nada de "los mejores", "líderes", "ultra exclusivo". La marca habla
  con calma y presenta, no convence.
- **No inventar branding**: ni slogans, ni submarcas, ni símbolos gráficos nuevos.
- Escribir **"Luxxor"**, nunca "Luxor" con una sola X.

## Voz

Inglés internacional, frases cortas, sin lenguaje turístico. "Private stays. Exceptional
places." sí; "¡Vive unas vacaciones inolvidables!" no.

CTAs del repertorio de marca: DISCOVER THE COLLECTION · REQUEST AVAILABILITY ·
PRIVATE ENQUIRY · VIEW PROPERTY.

## Sistema visual

| | |
|---|---|
| Navy | `#061B36` — dominante, 80-90% de la pantalla |
| Navy profundo | `#0A2342` — apoyos y overlays |
| Marfil | `#F5F2EA` — texto sobre oscuro, 5-15% |
| Dorado | `#D6A34A` — **solo acento, 2-5%**: líneas, hover, XX del logo |
| Carbón | `#16191D` — texto sobre fondos claros |

Serif editorial (Cormorant Garamond) en titulares. Sans (Inter) en interfaz.
Mucho espacio negativo: una imagen excelente + un headline + una frase + un CTA.

Animaciones lentas: fade, reveal, parallax sutil, image scale. Nada de rebotes, neones,
partículas ni glassmorphism.

## Estado del código

Landing estática, sin build ni dependencias. Se abre `index.html` y ya.

```
index.html              Hero animado + adelanto de la sección siguiente
assets/css/styles.css   Diseño y animación completos
assets/js/hero.js       Solo publica el progreso del scroll como variables CSS
assets/img/             Imágenes
docs/                   Contexto de marca
```

El JS no anima nada: calcula el progreso del scroll (0 → 1) y lo expone en `--p`,
`--p-copy`, `--p-villa`, `--p-mark`, `--p-mark-out`, `--p-veil`. Toda la animación vive en
el CSS. Para cambiar el ritmo se tocan los tramos de `hero.js`; para el aspecto, el CSS.

## Pendiente

- Fotografía real de la villa en lugar de `assets/img/villa.svg` (placeholder evidente).
- Resto de secciones de la home, según la secuencia del §18 del contexto de marca.
