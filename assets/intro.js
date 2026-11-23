/* Opening animation: "built from the foundations up".
   A ground line is set out on a blueprint grid, a blockwork wall is laid course by course,
   the JFC logo rises out of the ground in a puff of dust, then the hoarding gates open onto the page.
   Inlined straight after the loader markup so it starts before fonts or libraries load. */
(function () {
  const html = document.documentElement, L = document.getElementById('loader');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const rand = (a, b) => a + Math.random() * (b - a);
  const signal = n => { window['__intro_' + n] = 1; dispatchEvent(new Event('intro:' + n)); };
  const finish = () => { if (L) L.remove(); html.classList.remove('intro', 'intro-out'); signal('done'); };
  try { sessionStorage.setItem('jfc_intro', '1'); } catch (e) {}
  if (!L || !html.classList.contains('intro') || reduce) { finish(); return; }

  /* lay the blockwork: stretcher bond, bottom course first, left to right */
  const wall = L.querySelector('.wall'), ROWS = 6, COLS = 7, W = 100 / COLS, H = 100 / ROWS;
  const frag = document.createDocumentFragment();
  for (let r = 0; r < ROWS; r++) {
    const off = r % 2 ? -W / 2 : 0;
    for (let c = 0; c < COLS + (r % 2); c++) {
      const b = document.createElement('i');
      b.style.cssText = `left:${off + c * W}%;bottom:${r * H}%;width:${W}%;height:${H}%;--d:${(180 + r * 120 + c * 26 + rand(0, 40)) | 0}ms`;
      frag.appendChild(b);
    }
  }
  wall.appendChild(frag);

  const at = (ms, fn) => setTimeout(fn, ms);
  requestAnimationFrame(() => requestAnimationFrame(() => L.classList.add('go')));   // grid, ground line, blocks
  at(1050, () => {                                                                   // logo rises out of the ground
    L.classList.add('up');
    const g = L.querySelector('.ground'), r = g.getBoundingClientRect();
    for (let i = 0; i < 22; i++) {
      const d = document.createElement('i'); d.className = 'dust';
      const x = r.left + r.width * rand(.22, .78), s = rand(6, 16), dir = x < r.left + r.width / 2 ? -1 : 1;
      d.style.cssText = `left:${x}px;top:${r.top}px;width:${s}px;height:${s}px`;
      L.appendChild(d);
      d.animate([{ transform: 'translate(-50%,-50%) scale(.4)', opacity: .7 },
                 { transform: `translate(calc(-50% + ${dir * rand(30, 140)}px), calc(-50% - ${rand(10, 60)}px)) scale(${rand(1.4, 2.6)})`, opacity: 0 }],
                { duration: rand(700, 1200), easing: 'cubic-bezier(.2,.7,.3,1)', fill: 'forwards' });
    }
  });
  at(1500, () => L.classList.add('done'));                                           // tagline + glow
  at(2400, () => { html.classList.add('intro-out'); signal('open'); at(1000, finish); });  // hoarding gates open
})();
