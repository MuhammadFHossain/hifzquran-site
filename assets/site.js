/* The site's one script. Three small things, then the paintings.

   ?theme=dark or ?theme=light is read in each page's head, before the
   stylesheet paints, so a forced theme never flashes. */

/* An Android visitor sees Google Play; the App Store, which cannot help them,
   steps aside. */
(function () {
  if (/Android/i.test(navigator.userAgent)) document.documentElement.classList.add("android");
})();

/* Words and screens fade in as they arrive, once. Nothing slides or rises:
   in the app, letters fade or are written in, never moved. */
(function () {
  "use strict";
  var items = document.querySelectorAll(".reveal");
  if (!items.length) return;
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  items.forEach(function (el) { io.observe(el); });
})();

/* The footer's ayah is set in the mushaf's own face, which is large. It is
   fetched when the footer comes near, and the ayah shows once it has come. */
(function () {
  "use strict";
  var ayat = document.querySelectorAll(".foot-ayah .ar");
  if (!ayat.length) return;
  function show() { ayat.forEach(function (el) { el.classList.add("ready"); }); }
  function fetchFace() {
    if (!document.fonts || !document.fonts.load) { show(); return; }
    document.fonts.load('27px "UthmanicHafs"', ayat[0].textContent).then(show, show);
  }
  if (!("IntersectionObserver" in window)) { fetchFace(); return; }
  var io = new IntersectionObserver(function (entries) {
    if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); fetchFace(); }
  }, { rootMargin: "900px 0px 900px 0px" });
  ayat.forEach(function (el) { io.observe(el); });
})();

/* The paintings, played back as the app plays them.

   Each painting comes with maps the app ships beside it: its ground before
   anything grew (-base), when each pixel appears (-time, grey, 0 = at once),
   and what each pixel is made of (-mat: red is gold leaf, green is lapis).
   One shader grows the painting in as a clock runs, so stems grow from their
   roots and blossoms open from the middle, and lays the light on its gold:
   the shell gold's mottle and the burnisher's facets, a broad sheen where the
   window reflects, and glints where single facets face the light. It is the
   app's illumPaint and illumLight (Illumination.metal, IllumLight.h) in GLSL,
   and the page that plays it is the design page's ("Painted Moments").

   The light rests above the page, as the app's does with the phone held for
   reading. A mouse moves it. On a phone it follows the phone's tilt where the
   browser gives it freely, and otherwise the page's scroll. With Reduce
   Motion, or with no WebGL, the still painting is what shows. */
(function () {
  "use strict";
  var root = document.documentElement;
  var els = Array.prototype.slice.call(document.querySelectorAll(".illum[data-art]"));
  if (!els.length) return;
  window.__illum = true;
  function still(el) { el.classList.add("still"); }
  function allStill() { els.forEach(still); root.classList.remove("gl"); }
  var reduce = false;
  try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}
  if (reduce || !("IntersectionObserver" in window)) { allStill(); return; }

  // One WebGL context paints every picture; each is copied to its own canvas.
  var glc = document.createElement("canvas"), gl = null;
  try { gl = glc.getContext("webgl", { premultipliedAlpha: false, preserveDrawingBuffer: true, antialias: false, alpha: true }); } catch (e) {}
  if (!gl) { allStill(); return; }

  var VS = "attribute vec2 p; varying vec2 v; void main(){ v = vec2(p.x*0.5+0.5, 0.5-p.y*0.5); gl_Position = vec4(p,0.,1.); }";
  var FS = [
    "#ifdef GL_FRAGMENT_PRECISION_HIGH",
    "precision highp float;",
    "#else",
    "precision mediump float;",
    "#endif",
    "varying vec2 v;",
    "uniform sampler2D F, B, T, M;",
    "uniform float prog, soft;",
    "uniform vec3 L;",
    "uniform vec2 size;",
    "float hash(vec2 p){ vec3 q = fract(vec3(p.xyx) * 0.1031); q += dot(q, q.yzx + 33.33); return fract((q.x + q.y) * q.z); }",
    "float noise(vec2 p){ vec2 i = floor(p), f = fract(p); vec2 u = f*f*(3.0-2.0*f);",
    "  float a = hash(i), b = hash(i+vec2(1.,0.)), c = hash(i+vec2(0.,1.)), d = hash(i+vec2(1.,1.));",
    "  return mix(mix(a,b,u.x), mix(c,d,u.x), u.y) * 2.0 - 1.0; }",
    // the shell gold's mottle, and the burnisher's facets under half a point
    "float mottle(vec2 p){ vec2 q = p / 3.2; return 0.55*noise(q) + 0.3*noise(q*2.03+17.1) + 0.15*noise(q*4.1+31.7); }",
    "float facets(vec2 p){ return noise(p/0.55 + 5.3) + 0.35*mottle(p); }",
    "vec3 facetN(vec2 p, float depth){ float e = 0.3; float h = facets(p);",
    "  float hx = facets(p+vec2(e,0.)), hy = facets(p+vec2(0.,e));",
    "  return normalize(vec3(-(hx-h)/e*depth, -(hy-h)/e*depth, 1.0)); }",
    // where the window's reflection lies on the piece
    "float sheen(vec2 q, vec3 L){ vec2 c = L.xy*0.95; vec2 d = q - c; vec2 al = normalize(vec2(L.y, -L.x) + 1e-4);",
    "  float a = dot(d, al), b = dot(d, vec2(al.y, -al.x)); return exp(-(a*a)/0.16 - (b*b)/0.07); }",
    // single facets catching the light
    "float glints(vec2 p, vec3 H, float cell, float density){ vec2 id = floor(p/cell); float r = hash(id+0.37);",
    "  if (r < 1.0 - density) return 0.0;",
    "  vec2 j = vec2(hash(id+7.1), hash(id+13.7)) - 0.5; vec3 n = normalize(vec3(j*1.3, 1.0));",
    "  vec2 f = fract(p/cell) - 0.5; float spot = smoothstep(0.5, 0.1, length(f));",
    "  return spot * pow(max(dot(n,H),0.0), 60.0); }",
    "void main(){",
    "  vec2 pos = v * size;",
    "  vec4 full = texture2D(F, v);",
    "  vec4 ground = texture2D(B, v);",
    "  float t = texture2D(T, v).r;",
    "  float show = t < 0.004 ? 1.0 : smoothstep(t - soft, t, prog * (1.0 + soft));",
    "  vec4 col = mix(ground, full, show);",
    "  vec3 m = texture2D(M, v).rgb;",
    "  float g = m.r * show, lap = m.g * show;",
    "  vec3 lit = col.rgb;",
    "  if (g > 0.01 || lap > 0.01) {",
    "    vec3 w = vec3(0.299, 0.587, 0.114);",
    "    vec2 ex = vec2(0.6/size.x, 0.0), ey = vec2(0.0, 0.6/size.y);",
    "    float lx = dot(texture2D(F, v+ex).rgb - texture2D(F, v-ex).rgb, w);",
    "    float ly = dot(texture2D(F, v+ey).rgb - texture2D(F, v-ey).rgb, w);",
    "    vec3 grain = facetN(pos, 0.16);",
    "    vec3 n = normalize(vec3(-lx*4.0 + grain.x, -ly*4.0 + grain.y, 1.0));",
    "    vec3 H = normalize(L + vec3(0.,0.,1.));",
    "    float spec = pow(max(dot(n,H),0.0), 32.0);",
    "    float diffuse = dot(n,L) - L.z;",
    "    vec2 q = (pos - size*0.5) / max(size.x, size.y);",
    "    float sh = sheen(q, L);",
    "    vec3 warm = vec3(1.0, 0.86, 0.52);",
    "    float lum = dot(full.rgb, w);",
    "    lit = col.rgb * (1.0 + 0.5*diffuse*g);",
    "    lit += g * (0.40*sh + 0.85*spec*(0.2+sh)) * warm * (0.55 + 0.45*lum);",
    "    lit += g * 1.5 * glints(pos, H, 1.0, 0.05) * (0.35+sh) * vec3(1.0, 0.95, 0.8);",
    "    lit += g * 0.8 * glints(pos+0.5, H, 0.6, 0.08) * (0.2+sh) * vec3(1.0, 0.93, 0.75);",
    "    lit += lap * glints(pos+0.6, H, 1.5, 0.018) * (0.3+0.9*sh) * vec3(0.65, 0.75, 1.0);",
    "  }",
    "  gl_FragColor = vec4(min(lit, vec3(1.0)), col.a);",
    "}"].join("\n");

  function shader(type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null;
  }
  var vs = shader(gl.VERTEX_SHADER, VS), fs = shader(gl.FRAGMENT_SHADER, FS);
  if (!vs || !fs) { allStill(); return; }
  var prog = gl.createProgram();
  gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { allStill(); return; }
  gl.useProgram(prog);
  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  var loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  var U = {};
  ["F", "B", "T", "M", "prog", "soft", "L", "size"].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
  gl.uniform1i(U.F, 0); gl.uniform1i(U.B, 1); gl.uniform1i(U.T, 2); gl.uniform1i(U.M, 3);

  function texture(src) {
    var t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    if (src) gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, src);
    else gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([0, 0, 0, 255]));
    return t;
  }
  var NOW = texture(null);   // a time map of zero: everything shows at once
  function load(src) {
    return new Promise(function (ok, no) { var i = new Image(); i.onload = function () { ok(i); }; i.onerror = no; i.src = src; });
  }

  // the light, in the app's terms: x right, y down the glass, z out of it
  var REST = norm([0, -0.62, 0.78]);
  var light = REST.slice(), aim = REST.slice(), moving = false;
  function norm(a) { var l = Math.hypot(a[0], a[1], a[2]); return [a[0] / l, a[1] / l, a[2] / l]; }
  function aimAt(nx, ny) {
    nx = Math.max(-1, Math.min(1, nx)); ny = Math.max(-1, Math.min(1, ny));
    aim = norm([nx * 0.85, -0.62 + ny * 0.55, 0.78]); kick();
  }
  var fine = window.matchMedia && window.matchMedia("(pointer: fine)").matches;
  if (fine) {
    window.addEventListener("pointermove", function (e) {
      aimAt(e.clientX / window.innerWidth * 2 - 1, e.clientY / window.innerHeight * 2 - 1);
    }, { passive: true });
  } else {
    var tilted = false;
    window.addEventListener("deviceorientation", function (e) {
      if (e.gamma == null || e.beta == null) return;
      tilted = true;
      aimAt(e.gamma / 35, (e.beta - 50) / 35);
    }, { passive: true });
    window.addEventListener("scroll", function () {
      if (tilted) return;
      var s = window.scrollY / 700;
      aimAt(0.55 * Math.sin(s), 0.35 * Math.sin(s * 0.7));
    }, { passive: true });
  }

  var items = els.map(function (el) {
    var maps = (el.dataset.maps || "mat").split(",");
    return { el: el, img: el.querySelector("img"), path: el.dataset.art, maps: maps,
             grows: maps.indexOf("time") >= 0, dur: +(el.dataset.dur || 1.6),
             eager: el.hasAttribute("data-eager"), prog: 1, start: 0, playing: false,
             ready: false, loading: false, seen: false, visible: false };
  });

  function prepare(it) {
    if (it.loading) return;
    it.loading = true;
    var full = it.img.currentSrc || it.img.src;
    var want = [load(full),
      it.maps.indexOf("base") >= 0 ? load(it.path + "-base.webp") : null,
      it.grows ? load(it.path + "-time.png") : null,
      load(it.path + "-mat.png")];
    Promise.all(want).then(function (imgs) {
      it.tex = [texture(imgs[0]), imgs[1] ? texture(imgs[1]) : null, imgs[2] ? texture(imgs[2]) : NOW, texture(imgs[3])];
      if (!it.tex[1]) it.tex[1] = it.tex[0];
      var c = document.createElement("canvas");
      c.setAttribute("aria-hidden", "true");
      it.el.appendChild(c);
      it.canvas = c; it.ctx = c.getContext("2d");
      it.aspect = imgs[0].naturalHeight / imgs[0].naturalWidth;
      it.ready = true;
      it.prog = it.grows ? 0 : 1;
      size(it); draw(it);
      if (it.grows && (it.eager || (it.visible && it.ratio > 0.45))) play(it);
    }).catch(function () { still(it.el); });
  }
  function size(it) {
    var r = it.el.getBoundingClientRect();
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    it.w = r.width; it.h = r.width * it.aspect;
    var w = Math.max(1, Math.round(r.width * dpr)), h = Math.max(1, Math.round(it.h * dpr));
    if (it.canvas.width !== w || it.canvas.height !== h) { it.canvas.width = w; it.canvas.height = h; }
  }
  function play(it) {
    if (!it.ready || it.seen) return;
    it.seen = true; it.playing = true; it.start = performance.now(); kick();
  }
  function draw(it) {
    var w = it.canvas.width, h = it.canvas.height;
    if (glc.width < w || glc.height < h) { glc.width = Math.max(glc.width, w); glc.height = Math.max(glc.height, h); }
    gl.viewport(0, 0, w, h);
    for (var k = 0; k < 4; k++) { gl.activeTexture(gl.TEXTURE0 + k); gl.bindTexture(gl.TEXTURE_2D, it.tex[k]); }
    gl.uniform1f(U.prog, it.prog); gl.uniform1f(U.soft, 0.06);
    gl.uniform3f(U.L, light[0], light[1], light[2]);
    gl.uniform2f(U.size, it.w, it.h);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    it.ctx.clearRect(0, 0, w, h);
    it.ctx.drawImage(glc, 0, glc.height - h, w, h, 0, 0, w, h);
  }

  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var it = items.find(function (x) { return x.el === e.target; });
      if (!it) return;
      it.visible = e.isIntersecting; it.ratio = e.intersectionRatio;
      if (e.isIntersecting) prepare(it);
      if (e.isIntersecting && e.intersectionRatio > 0.45 && it.grows) play(it);
      if (e.isIntersecting && it.ready) draw(it);
    });
  }, { threshold: [0, 0.5], rootMargin: "300px 0px 300px 0px" });
  items.forEach(function (it) { if (it.eager) prepare(it); io.observe(it.el); });
  window.addEventListener("resize", function () {
    items.forEach(function (it) { if (it.ready) { size(it); draw(it); } });
  });

  // One loop, running only while something moves.
  var running = false;
  function kick() { if (!running) { running = true; requestAnimationFrame(frame); } }
  function frame(now) {
    var busy = false;
    var d = 0;
    for (var k = 0; k < 3; k++) { var step = (aim[k] - light[k]) * 0.14; light[k] += step; d += Math.abs(step); }
    var moved = d > 0.0004;
    items.forEach(function (it) {
      if (!it.ready) return;
      if (it.playing) {
        var t = (now - it.start) / (it.dur * 1000);
        if (t >= 1) { t = 1; it.playing = false; }
        it.prog = 1 - Math.pow(1 - t, 1.6);
        busy = true;
        try { draw(it); } catch (e) {}
      } else if (moved && it.visible) {
        try { draw(it); } catch (e) {}
      }
    });
    if (busy || moved) requestAnimationFrame(frame); else running = false;
  }
})();
