// main.js — all client behavior for the car-import landed-cost calculator.
// One file, linked from both form.html and result.html. Each block is guarded
// so it only runs if the elements it needs are on the page (no-op otherwise).
// Keeping it out of the HTML so the templates stay pure markup.
(function () {
  "use strict";

  // ---- mode switch: simple vs advanced ----
  // Disabled inputs are not submitted, so the calc only ever sees one entry
  // shape at a time.
  const panels = document.querySelectorAll('.mode-panel');
  if (panels.length) {
    document.querySelectorAll('.mode-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.dataset.mode;
        document.querySelectorAll('.mode-btn').forEach(b => {
          const on = b === btn;
          b.classList.toggle('active', on);
          b.setAttribute('aria-selected', on);
        });
        panels.forEach(p => {
          const on = p.dataset.panel === mode;
          p.classList.toggle('hidden', !on);
          p.querySelectorAll('input, select, button').forEach(el => {
            if (el.classList.contains('mode-btn')) return;
            if (on) el.removeAttribute('disabled');
            else el.setAttribute('disabled', '');
          });
        });
      });
    });
  }

  // ---- FOB / CIF segmented toggle (simple mode) -> hidden input ----
  document.querySelectorAll('[data-toggle]').forEach(group => {
    const hidden = group.parentElement.querySelector('input[type=hidden]');
    group.querySelectorAll('.seg-btn').forEach(b => {
      b.addEventListener('click', () => {
        group.querySelectorAll('.seg-btn').forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        if (hidden) hidden.value = b.dataset.val;
      });
    });
  });

  // ---- live FX: free, no-key, graceful fallback to manual entry ----
  async function fetchRate(btn) {
    btn.disabled = true; btn.textContent = "Getting today's rate…";
    try {
      const r = await fetch('https://open.er-api.com/v6/latest/USD');
      const d = await r.json();
      const nad = d && d.rates && d.rates.NAD;
      if (!nad) throw new Error('no NAD rate');
      const v = (Math.round(nad * 100) / 100);
      document.querySelectorAll('.fx-input').forEach(f => f.value = v);
      btn.textContent = "1 USD = " + v.toFixed(2) + " NAD today";
      btn.classList.add('ok');
    } catch (e) {
      btn.textContent = "Couldn't reach it — type the rate yourself";
      btn.classList.add('err');
    }
    setTimeout(() => { btn.disabled = false; }, 1500);
  }

  // bind the FX buttons (was onclick="fetchRate(this)" in the markup)
  document.querySelectorAll('.fx-btn').forEach(b => {
    b.addEventListener('click', () => fetchRate(b));
  });

  // ---- print / save as PDF (result page) ----
  const printBtn = document.querySelector('.print');
  if (printBtn) printBtn.addEventListener('click', () => window.print());
})();