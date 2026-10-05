/**
 * Thathvamasi HR Consultancy (THC) - Safe, High-Performance Scroll Reveal
 * Elements are visible by default and animate smoothly without stuck hidden states
 */

export function initScrollReveal() {
  if (!('IntersectionObserver' in window)) return;

  const elements = document.querySelectorAll('.scroll-reveal, .reveal-up, .reveal-card');
  if (!elements.length) return;

  document.documentElement.classList.add('js-reveal-ready');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.02,
    rootMargin: '40px 0px 40px 0px'
  });

  elements.forEach((el) => {
    // Add staggered delay if inside a grid
    if (el.parentElement && (
        el.parentElement.classList.contains('zwc-solutions-grid') || 
        el.parentElement.classList.contains('services-grid') || 
        el.parentElement.classList.contains('industries-grid') ||
        el.parentElement.classList.contains('zwc-promo-tray'))) {
      const childIndex = Array.from(el.parentElement.children).indexOf(el);
      el.style.transitionDelay = `${(childIndex % 6) * 60}ms`;
    }

    // If already in viewport on initial load, reveal immediately
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight + 50 && rect.bottom > -50) {
      el.classList.add('is-visible');
    } else {
      observer.observe(el);
    }
  });
}
