/* Dodoliza store behaviour — language toggle, cart, shop filters, product page, checkout. */
(function () {
  var D = window.DODO || { products: [], packs: [] };
  var mem = {};
  function get(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return k in mem ? mem[k] : d; } }
  function set(k, v) { mem[k] = v; try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function lang() { return document.documentElement.lang === 'en' ? 'en' : 'ar'; }
  function tr(ar, en) { return lang() === 'en' ? en : ar; }
  function money(n) { return lang() === 'en' ? 'SAR ' + n : n + ' ر.س'; }

  /* Language */
  function applyLang(l) {
    var h = document.documentElement; h.lang = l; h.dir = l === 'ar' ? 'rtl' : 'ltr';
    $$('[data-aria-ar]').forEach(function (el) { el.setAttribute('aria-label', l === 'ar' ? el.dataset.ariaAr : el.dataset.ariaEn); });
    $$('[data-ph-ar]').forEach(function (el) { el.setAttribute('placeholder', l === 'ar' ? el.dataset.phAr : el.dataset.phEn); });
    set('dodo-lang', l);
    document.dispatchEvent(new Event('dodo:lang'));
  }
  $$('[data-lang-toggle]').forEach(function (b) { b.addEventListener('click', function () { applyLang(lang() === 'ar' ? 'en' : 'ar'); }); });
  applyLang(get('dodo-lang', 'ar'));

  /* Cart */
  function cart() { return get('dodo-cart', []); }
  function saveCart(c) { set('dodo-cart', c); badge(); }
  function count() { return cart().reduce(function (s, i) { return s + i.qty; }, 0); }
  function badge() { $$('[data-cart-count]').forEach(function (b) { var n = count(); b.textContent = n; b.hidden = n === 0; }); }
  badge();
  function toast(msg) {
    var t = document.createElement('div'); t.className = 'toast'; t.setAttribute('role', 'status'); t.textContent = msg;
    document.body.appendChild(t); setTimeout(function () { t.remove(); }, 2400);
  }
  function addToCart(item) {
    var c = cart(); var f = c.filter(function (i) { return i.id === item.id && i.size === item.size && i.color === item.color && i.pack === item.pack; })[0];
    if (f) f.qty += 1; else c.push(item);
    saveCart(c); toast(tr('أُضيف إلى السلة', 'Added to cart'));
  }
  function product(id) { return D.products.filter(function (p) { return p.id === id; })[0] || D.products[0]; }
  function pack(n) { return D.packs.filter(function (p) { return p.pairs === n; })[0]; }

  /* Shop filters */
  var grid = $('[data-shop-grid]');
  if (grid) {
    var state = { length: 'all', color: 'all', size: 'all', pack: 'all' };
    function render() {
      var cards = $$('.pcard-wrap', grid), shown = 0;
      cards.forEach(function (c) {
        var ok = (state.length === 'all' || c.dataset.length === state.length) &&
          (state.color === 'all' || c.dataset.colors.split(',').indexOf(state.color) > -1) &&
          (state.size === 'all' || c.dataset.sizes.split(',').indexOf(state.size) > -1);
        c.hidden = !ok; if (ok) shown++;
      });
      $$('[data-pack-price]').forEach(function (el) {
        var p = state.pack === 'all' ? D.packs[0] : pack(+state.pack);
        el.textContent = money(p.price);
        var lbl = el.parentElement.querySelector('[data-pack-label]');
        if (lbl) lbl.textContent = tr(p.pairs + ' أزواج', p.pairs + ' pairs');
      });
      $('[data-shop-count]').textContent = shown;
      $('[data-shop-empty]').hidden = shown !== 0;
    }
    $$('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.filter; state[k] = b.dataset.value;
        $$('[data-filter="' + k + '"]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        render();
      });
    });
    var reset = $('[data-filter-reset]');
    if (reset) reset.addEventListener('click', function () {
      state = { length: 'all', color: 'all', size: 'all', pack: 'all' };
      $$('[data-filter]').forEach(function (x) { x.setAttribute('aria-pressed', x.dataset.value === 'all' ? 'true' : 'false'); });
      render();
    });
    document.addEventListener('dodo:lang', render);
    render();
  }

  /* Product page */
  var pp = $('[data-product]');
  if (pp) {
    var sel = { size: null, color: null, pack: 6 };
    var p = product(pp.dataset.product);
    function updatePrice() {
      var pk = pack(sel.pack);
      $$('[data-pp-price]').forEach(function (e) { e.textContent = money(pk.price); });
      $$('[data-pp-pairs]').forEach(function (e) { e.textContent = tr(pk.pairs + ' أزواج', pk.pairs + ' pairs'); });
    }
    function radioGroup(name, onPick) {
      $$('[data-pick="' + name + '"]').forEach(function (b) {
        b.addEventListener('click', function () {
          $$('[data-pick="' + name + '"]').forEach(function (x) { x.setAttribute('aria-checked', x === b ? 'true' : 'false'); });
          onPick(b.dataset.value);
        });
      });
    }
    radioGroup('size', function (v) { sel.size = v; $('[data-size-err]').hidden = true; });
    radioGroup('color', function (v) { sel.color = v; $('[data-color-name]').textContent = v; });
    radioGroup('pack', function (v) { sel.pack = +v; updatePrice(); });
    var firstColor = $('[data-pick="color"]'); if (firstColor) { sel.color = firstColor.dataset.value; $('[data-color-name]').textContent = sel.color; }
    $$('[data-add]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!sel.size) { var e = $('[data-size-err]'); e.hidden = false; $('#size-group').scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
        var pk = pack(sel.pack);
        addToCart({ id: p.id, nameAr: p.nameAr, nameEn: p.nameEn, size: sel.size, color: sel.color, pack: pk.pairs, price: pk.price, qty: 1 });
      });
    });
    $$('[data-thumb]').forEach(function (t) {
      t.addEventListener('click', function () {
        $$('[data-thumb]').forEach(function (x) { x.setAttribute('aria-current', x === t ? 'true' : 'false'); });
        $$('[data-slide]').forEach(function (s) { s.hidden = s.dataset.slide !== t.dataset.thumb; });
      });
    });
    $$('.zoom').forEach(function (z) {
      z.addEventListener('click', function (ev) {
        var r = z.getBoundingClientRect(), s = z.querySelector('.sock');
        if (s) s.style.transformOrigin = ((ev.clientX - r.left) / r.width * 100) + '% ' + ((ev.clientY - r.top) / r.height * 100) + '%';
        z.classList.toggle('on'); z.setAttribute('aria-pressed', z.classList.contains('on') ? 'true' : 'false');
      });
    });
    var dlg = $('#size-chart');
    $$('[data-open-chart]').forEach(function (b) { b.addEventListener('click', function () { if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); }); });
    $$('[data-close-chart]').forEach(function (b) { b.addEventListener('click', function () { dlg.close ? dlg.close() : dlg.removeAttribute('open'); }); });
    document.addEventListener('dodo:lang', updatePrice);
    updatePrice();
  }

  /* Cart page */
  var cl = $('[data-cart-list]');
  function totals() {
    var sub = cart().reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    var ship = sub === 0 || sub >= D.freeShipping ? 0 : D.shipping;
    return { sub: sub, ship: ship, total: sub + ship };
  }
  function renderTotals() {
    var t = totals();
    $$('[data-sub]').forEach(function (e) { e.textContent = money(t.sub); });
    $$('[data-ship]').forEach(function (e) { e.textContent = t.ship === 0 ? tr('مجاني', 'Free') : money(t.ship); });
    $$('[data-total]').forEach(function (e) { e.textContent = money(t.total); });
    $$('[data-free-left]').forEach(function (e) {
      var left = D.freeShipping - t.sub;
      e.textContent = left > 0 ? tr('باقي ' + left + ' ر.س على الشحن المجاني', 'SAR ' + left + ' away from free shipping') : tr('طلبك يوصلك بشحن مجاني', 'Your order ships free');
    });
  }
  if (cl) {
    function renderCart() {
      var c = cart(); cl.innerHTML = '';
      $('[data-cart-empty]').hidden = c.length !== 0; $('[data-cart-full]').hidden = c.length === 0;
      c.forEach(function (i, idx) {
        var li = document.createElement('li'); li.className = 'card'; li.style.cssText = 'padding:16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap';
        var name = document.createElement('div'); name.style.cssText = 'flex:1 1 220px;min-width:0';
        var h = document.createElement('div'); h.style.fontWeight = '700'; h.textContent = tr(i.nameAr, i.nameEn);
        var m = document.createElement('div'); m.className = 'muted small';
        m.textContent = tr(i.pack + ' أزواج · مقاس ' + i.size + ' · ' + i.color, i.pack + ' pairs · size ' + i.size + ' · ' + i.color);
        name.appendChild(h); name.appendChild(m);
        var q = document.createElement('div'); q.style.cssText = 'display:flex;align-items:center;gap:6px';
        function qb(label, aria, d) {
          var b = document.createElement('button'); b.type = 'button'; b.className = 'tool'; b.style.border = '2px solid var(--color-border)';
          b.textContent = label; b.setAttribute('aria-label', aria);
          b.addEventListener('click', function () { var cc = cart(); cc[idx].qty += d; if (cc[idx].qty <= 0) cc.splice(idx, 1); saveCart(cc); renderCart(); });
          return b;
        }
        var n = document.createElement('span'); n.className = 'num'; n.style.cssText = 'min-width:28px;text-align:center;font-weight:700'; n.textContent = i.qty;
        q.appendChild(qb('−', tr('إنقاص الكمية', 'Decrease quantity'), -1)); q.appendChild(n); q.appendChild(qb('+', tr('زيادة الكمية', 'Increase quantity'), 1));
        var pr = document.createElement('div'); pr.className = 'price'; pr.textContent = money(i.price * i.qty);
        li.appendChild(name); li.appendChild(q); li.appendChild(pr); cl.appendChild(li);
      });
      renderTotals();
    }
    document.addEventListener('dodo:lang', renderCart);
    renderCart();
  }

  /* Checkout */
  var co = $('[data-checkout]');
  if (co) {
    renderTotals();
    document.addEventListener('dodo:lang', renderTotals);
    co.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var ok = true;
      $$('[required]', co).forEach(function (f) {
        var e = co.querySelector('[data-err-for="' + f.id + '"]');
        var bad = !f.value.trim() || (f.id === 'phone' && !/^0?5\d{8}$/.test(f.value.replace(/\s/g, '')));
        if (e) e.hidden = !bad; f.setAttribute('aria-invalid', bad ? 'true' : 'false'); if (bad && ok) { f.focus(); ok = false; }
      });
      if (!ok) return;
      co.hidden = true; $('[data-done]').hidden = false; saveCart([]);
      $('[data-done]').focus();
    });
  }
})();
