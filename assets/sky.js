/* The sky, and the page that follows it.
   The app draws seven skies through the day from SkyPalette.swift. These are
   the same stops and the same light. There are no prayer times here, so the
   window is read off the clock: near enough for a page, and the app itself
   does the real sums.
   By day the sky sits at the head of the paper, with its light where the sun
   stands (MushafGround.hour). After dark the page turns dark and the sky is
   the whole ground: the evening photograph at Maghrib, the drawn night
   before dawn and after Isha.
   ?sky=maghrib forces a window, the way the app's -sky launch argument does,
   and ?clock=21:30 forces a time. */
(function () {
  "use strict";
  // glow: SkyPalette.glowGeometry, its colour, centre and peak. The ground
  // lifts the peak by the strength times nine, up to 0.9.
  var SKIES = {
    fajr:    { dark: true,  photo: false, glow: [0x8A5F5E, .50, 1.04, .30],
               stops: ["#070C22 0%", "#131C41 34%", "#2C3159 62%", "#5B4867 84%", "#8A5F5E 100%"] },
    shuruq:  { dark: false, glow: [0xF6D9A4, .30, .88, .42],
               stops: ["#2E4E77 0%", "#6B7C93 30%", "#C58E58 56%", "#E9A85C 78%", "#F3CE8E 100%"] },
    duha:    { dark: false, glow: [0xEAF3F8, .30, .58, .26],
               stops: ["#1E63A8 0%", "#4C93C6 36%", "#94C0DC 68%", "#D3E4EE 100%"] },
    dhuhr:   { dark: false, glow: [0xF2F8FA, .50, .12, .30],
               stops: ["#2C7BB6 0%", "#66A6CE 40%", "#AECBDD 72%", "#E4EDF1 100%"] },
    asr:     { dark: false, glow: [0xE8C88C, .70, .52, .28],
               stops: ["#2A5C86 0%", "#6C7E93 32%", "#B98F5E 60%", "#D9A85F 84%", "#EBC98D 100%"] },
    maghrib: { dark: true,  photo: true,
               stops: ["#151A3C 0%", "#2E2350 22%", "#5B3059 44%", "#93435A 66%", "#BC5F67 86%", "#D68B7B 100%"] },
    isha:    { dark: true,  photo: false,
               stops: ["#03040D 0%", "#080D22 42%", "#111938 74%", "#25304F 100%"] }
  };
  var STRENGTH = 0.22;

  function windowAt(h) {
    if (h < 4) return "isha";
    if (h < 6) return "fajr";
    if (h < 7.5) return "shuruq";
    if (h < 11) return "duha";
    if (h < 15) return "dhuhr";
    if (h < 18) return "asr";
    if (h < 20) return "maghrib";
    return "isha";
  }

  var params = new URLSearchParams(location.search);
  var forced = params.get("sky");
  var clockArg = params.get("clock");
  var root = document.documentElement;
  var ground = document.querySelector(".ground");
  var hero = document.querySelector(".hero .sky");
  var meta = document.querySelector('meta[name="theme-color"]');
  var current = null;

  function now() {
    var d = new Date();
    if (clockArg && /^\d{1,2}:\d{2}$/.test(clockArg)) {
      var p = clockArg.split(":"); d.setHours(+p[0], +p[1], 0, 0);
    }
    return d;
  }

  // A seeded star field, so the sky is the same one every visit.
  function stars(canvas, bright) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    canvas.width = w * dpr; canvas.height = h * dpr;
    var c = canvas.getContext("2d");
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.clearRect(0, 0, w, h);
    var seed = 1448;
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    // a faint band across the upper half: the milky way, as the app draws it
    c.save();
    c.translate(w * .5, h * .38); c.rotate(-.42);
    var g = c.createLinearGradient(0, -h * .22, 0, h * .22);
    g.addColorStop(0, "rgba(255,255,255,0)");
    g.addColorStop(.5, "rgba(255,255,255," + (bright ? .06 : .035) + ")");
    g.addColorStop(1, "rgba(255,255,255,0)");
    c.fillStyle = g; c.fillRect(-w, -h * .22, w * 2, h * .44);
    c.restore();
    var n = Math.round(w * h / (bright ? 5200 : 9000));
    for (var i = 0; i < n; i++) {
      var x = rnd() * w, y = rnd() * h * .92;
      var r = (bright ? .45 : .35) + rnd() * rnd() * (bright ? 1.5 : 1.0);
      var a = (bright ? .35 : .22) + rnd() * (bright ? .6 : .35);
      c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2);
      c.fillStyle = "rgba(255,248,235," + a.toFixed(2) + ")"; c.fill();
    }
  }

  // The crescent, where the sky's own moon stands.
  function moon(canvas, dim) {
    var w = canvas.clientWidth, h = canvas.clientHeight;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var c = canvas.getContext("2d");
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    var x = w * .74, y = h * .24, r = Math.max(14, Math.min(w, h) * .028);
    c.save();
    c.globalAlpha = dim ? .55 : .92;
    c.shadowColor = "rgba(255,240,200,.55)"; c.shadowBlur = r * 1.6;
    c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fillStyle = "#F6ECD2"; c.fill();
    c.shadowBlur = 0;
    c.globalCompositeOperation = "destination-out";
    c.beginPath(); c.arc(x + r * .42, y - r * .18, r * .86, 0, Math.PI * 2); c.fill();
    c.restore();
  }

  function paint(name) {
    var s = SKIES[name];
    root.classList.toggle("dark", s.dark);
    root.classList.toggle("light", !s.dark);
    root.style.setProperty("--skyGrad", "linear-gradient(180deg," + s.stops.join(",") + ")");
    if (s.glow) {
      var c = s.glow[0], a = Math.min(.9, s.glow[3] * STRENGTH * 9);
      root.style.setProperty("--glow", "rgba(" + (c >> 16) + "," + ((c >> 8) & 255) + "," + (c & 255) + "," + a.toFixed(2) + ")");
      root.style.setProperty("--glowX", (s.glow[1] * 100) + "%");
      root.style.setProperty("--glowY", (s.glow[2] * 50) + "%");
    }
    var night = s.dark && !s.photo;
    if (ground) ground.classList.toggle("night", night);
    if (hero) hero.classList.toggle("night", night);
    if (night) {
      var gc = ground && ground.querySelector("canvas");
      var hc = hero && hero.querySelector("canvas");
      if (gc) stars(gc, false);
      if (hc) { stars(hc, true); moon(hc, name === "fajr"); }
    }
    if (meta) meta.setAttribute("content", s.dark ? "#14120D" : "#FAF6EC");
    current = name;
  }

  function tick() {
    var d = now();
    var name = (forced && SKIES[forced]) ? forced : windowAt(d.getHours() + d.getMinutes() / 60);
    if (name !== current) paint(name);
  }

  tick();
  setInterval(tick, 30000);
  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () { if (current && SKIES[current].dark && !SKIES[current].photo) { var c = current; current = null; paint(c); } }, 150);
  });
})();

/* An Android visitor is told the truth: the app is coming to Google Play, and
   the App Store buttons, which cannot help them, step aside. */
(function () {
  if (/Android/i.test(navigator.userAgent)) document.documentElement.classList.add("android");
})();

/* Things below the fold rise a little as they arrive. Once, then they stay. */
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
