/* Tiny runtime: renders <template id="tpl"> with {{holes}}, <sc-for>, <sc-if>, onClick */
(function () {
  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (p) {
    Object.assign(this.state, typeof p === 'function' ? p(this.state) : p);
    if (this.__render) this.__render();
  };
  window.DCLogic = DCLogic;

  function lookup(path, scope) {
    path = path.trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    var parts = path.split('.'), v = scope;
    for (var i = 0; i < parts.length; i++) { if (v == null) return undefined; v = v[parts[i]]; }
    return v;
  }
  var HOLE = /\{\{([^}]+)\}\}/g;
  function single(str, scope) { var m = /^\s*\{\{([^}]+)\}\}\s*$/.exec(str || ''); return m ? lookup(m[1], scope) : str; }
  function interp(str, scope) { return str.replace(HOLE, function (_, p) { var v = lookup(p, scope); return v == null ? '' : String(v); }); }

  function proc(parent, scope, handlers) {
    var kids = Array.prototype.slice.call(parent.childNodes);
    kids.forEach(function (n) {
      if (n.nodeType === 3) { if (n.nodeValue.indexOf('{{') > -1) n.nodeValue = interp(n.nodeValue, scope); return; }
      if (n.nodeType !== 1) return;
      var tag = n.tagName.toLowerCase();
      if (tag === 'sc-for') {
        var list = single(n.getAttribute('list'), scope) || [], as = n.getAttribute('as') || 'item';
        var frag = document.createDocumentFragment();
        list.forEach(function (item) {
          var box = document.createElement('div');
          Array.prototype.forEach.call(n.childNodes, function (c) { box.appendChild(c.cloneNode(true)); });
          var sc = Object.create(scope); sc[as] = item;
          proc(box, sc, handlers);
          while (box.firstChild) frag.appendChild(box.firstChild);
        });
        parent.replaceChild(frag, n);
        return;
      }
      if (tag === 'sc-if') {
        if (single(n.getAttribute('value'), scope)) {
          proc(n, scope, handlers);
          var f = document.createDocumentFragment();
          while (n.firstChild) f.appendChild(n.firstChild);
          parent.replaceChild(f, n);
        } else parent.removeChild(n);
        return;
      }
      Array.prototype.slice.call(n.attributes).forEach(function (a) {
        if (a.name.indexOf('hint-') === 0) { n.removeAttribute(a.name); return; }
        if (a.value.indexOf('{{') < 0) return;
        if (a.name.indexOf('on') === 0) {
          var fn = single(a.value, scope);
          n.removeAttribute(a.name);
          if (typeof fn === 'function') n.setAttribute('data-ev-' + a.name.slice(2), String(handlers.push(fn) - 1));
          return;
        }
        var nm = a.name.indexOf('data-dc-') === 0 ? a.name.slice(8) : a.name;
        if (nm !== a.name) n.removeAttribute(a.name);
        n.setAttribute(nm, interp(a.value, scope));
      });
      proc(n, scope, handlers);
    });
  }

  window.DC = {
    mount: function (Klass) {
      var tpl = document.getElementById('tpl'), app = document.getElementById('app');
      var comp = new Klass({}), handlers = [];
      function render() {
        handlers = [];
        var vals = comp.renderVals();
        var next = document.createElement('div'); next.id = 'app';
        var frag = tpl.content.cloneNode(true), holder = frag.ownerDocument.createElement('div');
        holder.appendChild(frag);
        proc(holder, vals, handlers);
        while (holder.firstChild) next.appendChild(document.importNode(holder.firstChild, true)), holder.removeChild(holder.firstChild);
        window.morphdom(app, next, {
          onBeforeElUpdated: function (from, to) {
            if (from.tagName === 'DETAILS') { if (from.open) to.setAttribute('open', ''); else to.removeAttribute('open'); }
            if (from.tagName === 'INPUT' || from.tagName === 'TEXTAREA') return false;
            return true;
          }
        });
      }
      ['click', 'input', 'change', 'touchstart', 'touchend'].forEach(function (ev) {
        app.addEventListener(ev, function (e) {
          var t = e.target.closest('[data-ev-' + ev + ']');
          if (t) { var h = handlers[+t.getAttribute('data-ev-' + ev)]; if (h) h(e); }
        }, { passive: true });
      });
      comp.__render = render;
      render();
      if (comp.componentDidMount) comp.componentDidMount();
    }
  };
})();
