/* ============================================================
   LUXXOR PROJECTS — Galería de las villas
   ------------------------------------------------------------
   Cada tarjeta lleva sus fotos en data-images. Al abrirla, la
   galería ocupa la pantalla y se navega con flechas, teclado o
   deslizando el dedo.
   ============================================================ */

(function () {
  'use strict';

  var box = document.getElementById('lightbox');
  if (!box) return;

  var img      = box.querySelector('.lightbox__img');
  var refLabel = box.querySelector('.lightbox__ref');
  var counter  = box.querySelector('.lightbox__counter');

  var shots = [];
  var index = 0;
  var opener = null;

  function show(i) {
    index = (i + shots.length) % shots.length;
    img.src = shots[index];
    counter.textContent = (index + 1) + ' / ' + shots.length;
  }

  function open(card) {
    shots = (card.dataset.images || '').split(' ').filter(Boolean);
    if (!shots.length) return;
    opener = card.querySelector('.villa-card__open');
    refLabel.textContent = card.dataset.ref || '';
    box.hidden = false;
    // el reflow intermedio deja que la transición de entrada se vea
    void box.offsetWidth;
    box.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    show(0);
    box.querySelector('.lightbox__close').focus();
  }

  function close() {
    box.classList.remove('is-open');
    document.body.style.overflow = '';
    // espera al fundido antes de sacarlo del árbol accesible
    setTimeout(function () { box.hidden = true; img.src = ''; }, 320);
    if (opener) opener.focus();
  }

  document.querySelectorAll('.villa-card__open').forEach(function (btn) {
    btn.addEventListener('click', function () { open(btn.closest('.villa-card')); });
  });

  box.querySelector('.lightbox__close').addEventListener('click', close);
  box.querySelector('.lightbox__nav--prev').addEventListener('click', function () { show(index - 1); });
  box.querySelector('.lightbox__nav--next').addEventListener('click', function () { show(index + 1); });

  // Clic fuera de la imagen cierra
  box.addEventListener('click', function (e) {
    if (e.target === box || e.target.classList.contains('lightbox__stage')) close();
  });

  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'Escape')     close();
    if (e.key === 'ArrowLeft')  show(index - 1);
    if (e.key === 'ArrowRight') show(index + 1);
  });

  // Deslizar en táctil
  var startX = null;
  box.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 45) show(index + (dx < 0 ? 1 : -1));
    startX = null;
  }, { passive: true });
})();
