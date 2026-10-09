/**
 * Butter-Smooth Scrolling using Lenis
 * Provides momentum-based, luxury smooth scrolling across the entire application
 */
import Lenis from 'lenis';
import 'lenis/dist/lenis.css';

let lenisInstance = null;

export function initSmoothScroll() {
  // Prevent duplicate initialization
  if (lenisInstance) return lenisInstance;

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    document.documentElement.style.scrollBehavior = 'smooth';
    return null;
  }

  try {
    lenisInstance = new Lenis({
      duration: 1.25,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // Buttery exponential ease-out
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 0.95,
      touchMultiplier: 1.4,
      infinite: false,
    });

    // Connect Lenis to requestAnimationFrame
    function raf(time) {
      lenisInstance.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Make lenis globally accessible for buttons and programmatic scrolls
    window.lenis = lenisInstance;

    // Smoothly handle anchor links (e.g. href="#consultation", href="#contact")
    document.addEventListener('click', (e) => {
      const anchor = e.target.closest('a[href^="#"]');
      if (!anchor) return;

      const hash = anchor.getAttribute('href');
      if (hash && hash !== '#' && hash.length > 1) {
        const target = document.querySelector(hash);
        if (target) {
          e.preventDefault();
          // Scroll with silky smooth momentum and offset for fixed header
          const headerHeight = document.querySelector('.main-header, .biz-header')?.offsetHeight || 80;
          lenisInstance.scrollTo(target, {
            offset: -headerHeight - 20,
            duration: 1.3,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
          });

          // Update URL hash without jumping
          if (history.pushState) {
            history.pushState(null, null, hash);
          }
        }
      }
    });

    // Provide smooth scrolling on window resize
    window.addEventListener('resize', () => {
      lenisInstance.resize();
    });

    console.log('🧈 Lenis Butter-Smooth Scrolling successfully activated.');
    return lenisInstance;
  } catch (err) {
    console.warn('Lenis smooth scrolling fallback to native:', err);
    document.documentElement.style.scrollBehavior = 'smooth';
    return null;
  }
}
