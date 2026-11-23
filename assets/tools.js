/* JFC Construction & Groundwork — interactive tools:
   quote wizard, area checker, gallery & review filters. */
(function () {
  const WA = '353851910576', EMAIL = 'info@jfcconstruction.ie';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const html = document.documentElement;

  /* top bar slides away once the page scrolls */
  const tb = () => html.classList.toggle('scrolled-past', scrollY > 40);
  addEventListener('scroll', tb, { passive: true }); tb();

  /* mobile menu: service groups open as drop-downs */
  $$('.mtog').forEach(b => b.addEventListener('click', () => {
    const acc = b.closest('.macc'), open = !acc.classList.contains('open');
    $$('.macc').forEach(x => { x.classList.remove('open'); $('.mtog', x).setAttribute('aria-expanded', 'false'); });
    acc.classList.toggle('open', open); b.setAttribute('aria-expanded', String(open));
  }));

  /* ---------- drop-down quote panel under the header (like vantageroofing.ie) ---------- */
  const qd = $('#qdrop');
  if (qd) {
    const setQ = open => {
      html.classList.toggle('qdrop-open', open); qd.setAttribute('aria-hidden', String(!open));
      $$('.qbtn').forEach(b => b.setAttribute('aria-expanded', String(open)));
      if (open && matchMedia('(pointer:fine)').matches) setTimeout(() => { const f = $('input:not(.hp)', qd); if (f) f.focus({ preventScroll: true }); }, 380);
    };
    $$('[data-qdrop]').forEach(b => b.addEventListener('click', e => {
      e.preventDefault(); html.classList.remove('menu-open');
      const sel = $('select[name=service]', qd); if (sel && b.dataset.svc) sel.value = b.dataset.svc;
      setQ(b.classList.contains('qbtn') ? !html.classList.contains('qdrop-open') : true);
    }));
    $$('[data-qclose]', qd).forEach(b => b.addEventListener('click', () => setQ(false)));
    $$('[data-wizard]', qd).forEach(b => b.addEventListener('click', () => setQ(false)));
    addEventListener('keydown', e => { if (e.key === 'Escape') setQ(false); });
    document.addEventListener('click', e => { if (html.classList.contains('qdrop-open') && !e.target.closest('.hdr, [data-qdrop], .wiz')) setQ(false); });
    if (location.hash === '#quote') setQ(true);
  }

  /* ---------- live opening hours (Mon–Sun 7am–10pm, Irish time) ---------- */
  function openState() { return { open: true, text: 'Free site visits across Dublin' }; }
  const os = openState();
  $$('[data-open]').forEach(el => { el.textContent = os.text; el.classList.toggle('closed', !os.open); });

  /* ---------- area checker ---------- */
  const AREAS = {
    Dublin: ['Dublin', 'Dublin City', 'Lucan', 'Blanchardstown', 'Castleknock', 'Clonsilla', 'Ongar', 'Swords', 'Malahide', 'Finglas', 'Clondalkin', 'Tallaght', 'Saggart', 'Rathcoole', 'Citywest', 'Balbriggan', 'Skerries', 'Rush', 'Lusk', 'Donabate', 'Santry', 'Glasnevin', 'Drumcondra', 'Cabra', 'Phibsborough', 'Palmerstown', 'Chapelizod', 'Ballyfermot', 'Mulhuddart', 'Tyrrelstown', 'Dundrum', 'Rathfarnham', 'Terenure', 'Crumlin', 'Rathmines', 'Ranelagh', 'Ballsbridge', 'Donnybrook', 'Sandyford', 'Stillorgan', 'Blackrock', 'Dún Laoghaire', 'Dun Laoghaire', 'Dalkey', 'Killiney', 'Cabinteely', 'Foxrock', 'Leopardstown', 'Templeogue', 'Firhouse', 'Knocklyon', 'Ballinteer', 'Raheny', 'Clontarf', 'Artane', 'Coolock', 'Beaumont', 'Howth', 'Sutton', 'Baldoyle', 'Portmarnock', 'Kinsealy']
  };
  const ALL = Object.entries(AREAS).flatMap(([c, ts]) => ts.map(t => [t, c]));
  const NEAR = ['Wicklow', 'Bray', 'Greystones', 'Kildare', 'Maynooth', 'Celbridge', 'Leixlip', 'Naas', 'Meath', 'Ashbourne', 'Dunboyne', 'Ratoath', 'Navan'];
  $$('[data-area]').forEach(box => {
    const inp = $('input', box), out = $('.area-out', box), dl = $('datalist', box);
    if (dl) dl.innerHTML = ALL.map(([t]) => `<option value="${t}">`).join('');
    const check = () => {
      const v = inp.value.trim().toLowerCase().replace(/^co\.?\s+|county\s+/, '');
      if (!v) { out.className = 'area-out'; out.textContent = ''; return; }
      const hit = ALL.find(([t]) => t.toLowerCase() === v) || ALL.find(([t]) => t.toLowerCase().startsWith(v) && v.length > 2);
      const county = Object.keys(AREAS).find(c => c.toLowerCase() === v);
      if (hit || county) { out.className = 'area-out yes'; out.innerHTML = `<b>Yes, we cover ${hit ? hit[0] + ', Co. ' + hit[1] : 'Co. ' + county}.</b> Free site visit and free quote.`; }
      else if (NEAR.some(n => n.toLowerCase().startsWith(v) && v.length > 2)) { out.className = 'area-out maybe'; out.innerHTML = `<b>Very likely.</b> We regularly work in surrounding areas. Call <a href="tel:+353851910576">085 191 0576</a> to confirm.`; }
      else { out.className = 'area-out maybe'; out.innerHTML = `<b>Give us a call to check.</b> We cover Dublin and surrounding areas: <a href="tel:+353851910576">085 191 0576</a>`; }
    };
    inp.addEventListener('input', check); box.addEventListener('submit', e => { e.preventDefault(); check(); });
  });

  /* ---------- quote wizard ---------- */
  const wiz = $('#wiz');
  if (wiz) {
    const steps = $$('.wstep', wiz), bar = $('.wbar i', wiz), lbl = $('.wcount', wiz);
    const data = {}; let i = 0;
    const show = n => {
      i = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach((s, k) => s.classList.toggle('on', k === i));
      bar.style.width = ((i + 1) / steps.length * 100) + '%'; lbl.textContent = `Step ${i + 1} of ${steps.length}`;
      $('.wback', wiz).style.visibility = i ? 'visible' : 'hidden';
      if (i === steps.length - 1) summary();
    };
    $$('.wopt', wiz).forEach(b => b.addEventListener('click', () => {
      const k = b.closest('.wstep').dataset.key; data[k] = b.dataset.v;
      $$('.wopt', b.closest('.wstep')).forEach(x => x.classList.toggle('sel', x === b));
      setTimeout(() => show(i + 1), 180);
    }));
    $('.wback', wiz).addEventListener('click', () => show(i - 1));
    const summary = () => { $('.wsum', wiz).innerHTML = [['Service', data.service], ['Property', data.property], ['When', data.urgency]].filter(r => r[1]).map(([a, b]) => `<span><small>${a}</small>${b}</span>`).join(''); };
    const msg = () => {
      const f = Object.fromEntries(new FormData($('form', wiz)).entries());
      return `Hi JFC Construction, I'd like a free quote.\n\nService: ${data.service || '-'}\nProperty: ${data.property || '-'}\nWhen: ${data.urgency || '-'}\nName: ${f.name || '-'}\nPhone: ${f.phone}\nEircode: ${(f.eircode || '').toUpperCase()}\nArea: ${f.town || '-'}\n${f.details ? 'Details: ' + f.details + '\n' : ''}`;
    };
    const valid = () => {
      let ok = true;
      $$('[required]', $('form', wiz)).forEach(x => { const g = x.value.trim() && x.checkValidity(); x.closest('label').classList.toggle('bad', !g); if (!g) ok = false; });
      return ok;
    };
    $('.wwa', wiz).addEventListener('click', e => { e.preventDefault(); if (!valid()) return; window.open(`https://wa.me/${WA}?text=${encodeURIComponent(msg() + '\n(I can send photos of the site here.)')}`, '_blank', 'noopener'); done(); });
    $('.wmail', wiz).addEventListener('click', async e => {
      e.preventDefault(); if (!valid()) return;
      const subject = 'Free quote request: ' + (data.service || 'Building work');
      const mailto = () => { location.href = `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(msg())}`; done(); };
      const F = window.JFC_FORMS || {};
      if (!F.key) return mailto();
      const btn = e.currentTarget, label = btn.innerHTML; btn.disabled = true; btn.textContent = 'Sending…';
      try {
        const f = Object.fromEntries(new FormData($('form', wiz)).entries());
        const r = await fetch(F.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({ access_key: F.key, subject, from_name: 'JFC Construction website (quote wizard)', service: data.service, property: data.property, when: data.urgency, name: f.name, phone: f.phone, eircode: (f.eircode || '').toUpperCase(), area: f.town, details: f.details, message: msg() }) });
        const j = await r.json().catch(() => ({}));
        if (!r.ok || j.success === false) throw new Error();
        done(true);
      } catch (err) { mailto(); }
      btn.disabled = false; btn.innerHTML = label;
    });
    const done = sent => {
      const d = $('.wdone', wiz);
      if (sent) { $('h3', d).textContent = 'Thanks, your request is in!'; $('p', d).innerHTML = 'We’ll be back to you with your free quote, usually the same day. Urgent? Call <a href="tel:+353851910576">085 191 0576</a>.'; }
      d.classList.add('on');
    };
    const open = (svc, e) => {
      if (e) e.preventDefault(); html.classList.add('wiz-open');
      $('.wdone', wiz).classList.remove('on');
      if (svc) { data.service = svc; $$('.wstep[data-key="service"] .wopt', wiz).forEach(x => x.classList.toggle('sel', x.dataset.v === svc)); show(1); } else show(0);
    };
    $$('[data-wizard]').forEach(b => b.addEventListener('click', e => open(b.dataset.wizard, e)));
    $$('[data-wclose]', wiz).forEach(b => b.addEventListener('click', () => html.classList.remove('wiz-open')));
    addEventListener('keydown', e => { if (e.key === 'Escape') html.classList.remove('wiz-open'); });
    if (location.hash === '#quote-wizard') open();
  }

  /* ---------- extension planning check ---------- */
  const hc = $('#health');
  if (hc) {
    const qs = $$('.hq', hc), res = $('.hres', hc), prog = $('.hprog i', hc); const ans = {};
    const upd = () => {
      const n = Object.keys(ans).length; prog.style.width = (n / qs.length * 100) + '%';
      $('.hcount', hc).textContent = `${n} of ${qs.length} answered`;
      if (n < qs.length) { res.classList.remove('on'); return; }
      const score = Object.values(ans).reduce((a, b) => a + b, 0);
      const hard = Object.values(ans).some(v => v >= 3);
      let k = hard ? 'replace' : score === 0 ? 'repair' : 'watch';
      const R = {
        repair: ['Likely exempt from planning', 'From your answers, your project looks like it may fall within the exempted development limits, so you may not need to apply for planning permission. Building regulations still apply, and we’ll confirm everything on a free site visit.', 'extensions/home-extensions'],
        watch: ['Borderline: worth checking', 'Some of your answers are close to the exempted development limits. A small change to the size or position can often keep a project exempt. Book a free site visit and we’ll talk you through the options.', 'extensions/home-extensions'],
        replace: ['Planning permission is likely needed', 'At least one answer goes beyond the usual exempted development limits, so a planning application is likely. That’s very common for larger extensions, and we can point you in the right direction before we build.', 'extensions/home-extensions']
      }[k];
      $('h3', res).textContent = R[0]; $('p', res).textContent = R[1];
      $('.hlink', res).href = $('.hlink', res).dataset.base + R[2] + '/'; $('.hlink', res).textContent = 'About home extensions';
      res.dataset.k = k; res.classList.add('on');
      $('.hscore i', res).style.width = (k === 'repair' ? 16 : k === 'watch' ? 50 : 88) + '%';
    };
    qs.forEach((q, qi) => $$('button', q).forEach(b => b.addEventListener('click', () => {
      ans[qi] = +b.dataset.s; $$('button', q).forEach(x => x.classList.toggle('sel', x === b)); q.classList.add('done'); upd();
      const nx = qs[qi + 1]; if (nx && !nx.classList.contains('done') && innerWidth < 900) nx.scrollIntoView({ behavior: 'smooth', block: 'center' });
    })));
    $('.hreset', hc).addEventListener('click', () => { Object.keys(ans).forEach(k => delete ans[k]); $$('.hq', hc).forEach(q => { q.classList.remove('done'); $$('button', q).forEach(x => x.classList.remove('sel')); }); upd(); });
    upd();
  }

  /* ---------- filters (gallery & reviews) ---------- */
  $$('[data-filters]').forEach(bar => {
    const target = $(bar.dataset.filters);
    $$('button', bar).forEach(b => b.addEventListener('click', () => {
      $$('button', bar).forEach(x => x.classList.toggle('on', x === b));
      const f = b.dataset.f;
      $$('[data-cat]', target).forEach(el => { el.hidden = !(f === 'all' || el.dataset.cat.split(' ').includes(f)); });
    }));
  });
})();
