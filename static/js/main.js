// Placeholder for future enhancements (analytics, cart, etc.)
document.addEventListener("DOMContentLoaded", () => {
  // Auto-hide toasts after 3s
  const toasts = document.querySelectorAll(".toast");
  setTimeout(() => toasts.forEach(t => t.classList.remove("show")), 3000);
});


// Fallback any broken images at runtime
(function () {
  function onerrorFallback(e) {
    var t = e && e.target;
    if (!t || t.tagName !== 'IMG') return;
    if (t.dataset && t.dataset.fallbackApplied) return;
    t.src = '/static/img/placeholder.svg';
    if (t.dataset) t.dataset.fallbackApplied = '1';
  }
  window.addEventListener('error', function (e) {
    onerrorFallback(e);
  }, true);
})();
