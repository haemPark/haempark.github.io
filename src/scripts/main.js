// Footer year
document.getElementById('year').textContent = new Date().getFullYear();

// Theme. Starts from the OS preference; the nav button flips it for this visit.
// (Intentionally no localStorage — see README if you want the choice to persist.)
(function () {
  var root = document.documentElement;
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
  var apply = function (dark) { root.setAttribute('data-theme', dark ? 'dark' : 'light'); };
  apply(prefersDark.matches);
  prefersDark.addEventListener('change', function (e) { apply(e.matches); });
  document.getElementById('themeBtn').addEventListener('click', function () {
    apply(root.getAttribute('data-theme') !== 'dark');
  });
})();

// Highlight the nav link for the section you're currently reading.
(function () {
  var pairs = Array.prototype.slice.call(document.querySelectorAll('.nav-links a'))
    .map(function (a) { return { link: a, el: document.querySelector(a.getAttribute('href')) }; })
    .filter(function (p) { return p.el; });
  if (!pairs.length) return;

  var queued = false;
  function update() {
    queued = false;
    var line = 100;   // a section becomes "current" once its top passes this y
    var current = null;
    pairs.forEach(function (p) {
      if (p.el.getBoundingClientRect().top <= line) current = p;
    });
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2) {
      current = pairs[pairs.length - 1];   // pin the last link at the very bottom
    }
    pairs.forEach(function (p) { p.link.classList.toggle('active', p === current); });
  }
  addEventListener('scroll', function () {
    if (!queued) { queued = true; requestAnimationFrame(update); }
  }, { passive: true });
  addEventListener('resize', update);
  update();
})();
