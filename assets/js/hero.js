/* ============================================================
   LUXXOR VACATION — Motor de scroll del hero
   ------------------------------------------------------------
   Traduce la posición del scroll a un progreso 0 → 1 y lo publica
   como variables CSS. Toda la animación vive en el CSS; aquí solo
   se calcula el "cuándo".
   ============================================================ */

(function () {
  'use strict';

  var hero = document.getElementById('hero');
  if (!hero) return;

  // Respetamos la preferencia del sistema: sin movimiento, sin motor.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // Las variables se escriben en el escenario del hero, no en :root: así el
  // recálculo de estilos se queda dentro del hero en vez de invalidar la
  // página entera en cada fotograma.
  var stage = hero.querySelector('.hero__stage') || document.documentElement;
  var ticking = false;

  /** Normaliza v dentro del tramo [a, b] devolviendo 0 → 1. */
  function range(v, a, b) {
    if (v <= a) return 0;
    if (v >= b) return 1;
    return (v - a) / (b - a);
  }

  /** Suavizado (ease-in-out) para que nada arranque ni pare en seco. */
  function ease(t) {
    return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  }

  function update() {
    ticking = false;

    var scrolled = -hero.getBoundingClientRect().top;
    var travel = hero.offsetHeight - window.innerHeight;
    var p = travel > 0 ? Math.min(Math.max(scrolled / travel, 0), 1) : 0;

    stage.style.setProperty('--p', p.toFixed(4));

    // Tramos de la secuencia (los mismos beats que el vídeo de referencia)
    stage.style.setProperty('--p-copy',     ease(range(p, 0.00, 0.26)).toFixed(4)); // se va el titular
    stage.style.setProperty('--p-villa',    ease(range(p, 0.00, 0.70)).toFixed(4)); // sube la villa y sale por arriba
    stage.style.setProperty('--p-clouds',   ease(range(p, 0.16, 0.62)).toFixed(4)); // el mar de nubes la cubre
    stage.style.setProperty('--p-mark',     ease(range(p, 0.44, 0.62)).toFixed(4)); // el nombre se insinúa
    stage.style.setProperty('--p-settle',   ease(range(p, 0.58, 0.76)).toFixed(4)); // el nombre a presencia plena
    stage.style.setProperty('--p-veil',     ease(range(p, 0.80, 0.98)).toFixed(4)); // las nubes se lo tragan
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
