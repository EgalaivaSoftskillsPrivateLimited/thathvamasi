/**
 * Thathvamasi HR Consultancy (THC) - Application Entry Point
 * Theme: Zoho-Inspired Professional Enterprise Light Theme
 */

// Stylesheets
import './styles/variables.css';
import './styles/base.css';
import './styles/components.css';
import './styles/esight-theme.css';
import './styles/admin.css';
import './styles/responsive.css';
import './styles/funnel-showcase.css';

// Core UI Components
import { initToastSystem } from './components/ui/Toast.js';
import { initModalSystem } from './components/ui/Modal.js';

// Section Components
import { initServicesSection } from './components/sections/Services.js';
import { initIndustriesSection } from './components/sections/Industries.js';
import { initInsightsSection } from './components/sections/Insights.js';
import { initAiStudio } from './components/sections/AiStudio.js';

// Scroll Reveal & Animations
import { initScrollReveal } from './lib/scrollReveal.js';
import { initSmoothScroll } from './lib/smoothScroll.js';

// Form Components
import { initCandidateForm } from './components/forms/CandidateRegistrationForm.js';
import { initClientForm } from './components/forms/ClientRequisitionForm.js';
import { initContactForm } from './components/forms/ContactForm.js';

// Admin Portal
import { initAdminDashboard } from './components/admin/AdminDashboard.js';

// Navigation & Layout Behaviors
function setupNavigation() {
  const header = document.querySelector('.main-header');
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');
  const backToTop = document.getElementById('backToTopBtn');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }

    if (window.scrollY > 350) {
      backToTop?.classList.add('visible');
    } else {
      backToTop?.classList.remove('visible');
    }
  });

  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('open');
    });

    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (!link.classList.contains('dropdown-toggle')) {
          navMenu.classList.remove('open');
        }
      });
    });
  }

  // Handle dropdown toggle for mobile/touch
  const dropdownContainers = document.querySelectorAll('.nav-item.has-dropdown, .hasDropdown');
  dropdownContainers.forEach(container => {
    const toggle = container.querySelector('.dropdown-toggle, a');
    if (toggle) {
      toggle.addEventListener('click', (e) => {
        if (window.innerWidth <= 992) {
          e.preventDefault();
          container.classList.toggle('open');
        }
      });
    }
  });
}

// View Switcher (Main Website vs HR Command Center)
function setupViewSwitching() {
  const btnToggleAdmin = document.getElementById('btnToggleAdmin');
  if (btnToggleAdmin) {
    btnToggleAdmin.addEventListener('click', (e) => {
      e.preventDefault();
      window.location.href = '/admin/';
    });
  }

  // Active navigation highlight on scroll
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    let current = '';
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 120;
      const sectionId = section.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        current = sectionId;
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });
}

// Hero & Header Search Navigation
function setupHeroSearch() {
  const btnHeaderSearch = document.getElementById('btnHeaderSearch');
  if (btnHeaderSearch) {
    btnHeaderSearch.addEventListener('click', () => {
      document.getElementById('services')?.scrollIntoView({ behavior: 'smooth' });
    });
  }

  const searchInput = document.getElementById('heroKeywordInput');
  const btnSearch = document.getElementById('btnHeroSearch');

  if (btnSearch && searchInput) {
    btnSearch.addEventListener('click', () => {
      const term = searchInput.value.trim().toLowerCase();
      if (!term) {
        window.showToast('Please type a skill or job title to search', 'info');
        return;
      }

      const candidateSkills = document.getElementById('candidateSkills');
      if (candidateSkills) {
        candidateSkills.value = term;
      }
      
      const candidateSec = document.getElementById('candidates');
      if (candidateSec) {
        candidateSec.scrollIntoView({ behavior: 'smooth' });
        window.showToast(`Search applied for: "${term}". Register your profile below!`, 'success');
      }
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        btnSearch.click();
      }
    });
  }
}

// Hero Radar Mandate Row Click Routing
function setupHeroMandates() {
  document.querySelectorAll('.radar-mandate-row, .mandate-item').forEach(item => {
    item.addEventListener('click', () => {
      const role = item.getAttribute('data-role');
      const ind = item.getAttribute('data-ind');

      const roleInput = document.getElementById('empJobTitle') || document.getElementById('empRole');
      if (roleInput && role) {
        roleInput.value = role;
      }
      const indSelect = document.getElementById('empIndustry');
      if (indSelect && ind) {
        indSelect.value = ind;
      }

      if (window.showToast && role) {
        window.showToast(`Selected Mandate: ${role}. Complete requisition details below!`, 'success');
      }
    });
  });
}

// Esight-Inspired Component Logic (Advisor Modal, FAQs, Mobile Drawer)
export function initEsightComponents() {
  const callPopup = document.getElementById('callPopup');
  const openTriggers = document.querySelectorAll('.navConatctBox, [data-action="open-call-popup"]');
  const closeBtns = document.querySelectorAll('.callPopupClose');

  openTriggers.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (callPopup) callPopup.classList.add('active');
    });
  });

  closeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      if (callPopup) callPopup.classList.remove('active');
    });
  });

  if (callPopup) {
    callPopup.addEventListener('click', (e) => {
      if (e.target === callPopup) {
        callPopup.classList.remove('active');
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && callPopup.classList.contains('active')) {
        callPopup.classList.remove('active');
      }
    });
  }

  // Interactive FAQ Accordions (Supports both .faqBox and .faqItem patterns)
  const faqBoxes = document.querySelectorAll('.faqBox');
  faqBoxes.forEach(box => {
    const head = box.querySelector('.faqBoxHead');
    const body = box.querySelector('.faqBoxBody');
    if (head && body) {
      head.addEventListener('click', () => {
        const isOpen = box.classList.contains('active');
        faqBoxes.forEach(other => {
          if (other !== box) {
            other.classList.remove('active');
            const otherBody = other.querySelector('.faqBoxBody');
            if (otherBody) otherBody.style.maxHeight = '0px';
          }
        });

        if (isOpen) {
          box.classList.remove('active');
          body.style.maxHeight = '0px';
        } else {
          box.classList.add('active');
          body.style.maxHeight = `${body.scrollHeight + 40}px`;
        }
      });
    }
  });

  const faqItems = document.querySelectorAll('.faqItem');
  faqItems.forEach(item => {
    const header = item.querySelector('.faqHeader');
    const body = item.querySelector('.faqBody');
    if (header && body) {
      header.addEventListener('click', () => {
        const isOpen = item.classList.contains('active');
        faqItems.forEach(other => {
          if (other !== item) {
            other.classList.remove('active');
            const otherBody = other.querySelector('.faqBody');
            if (otherBody) otherBody.style.maxHeight = '0px';
          }
        });

        if (isOpen) {
          item.classList.remove('active');
          body.style.maxHeight = '0px';
        } else {
          item.classList.add('active');
          body.style.maxHeight = `${body.scrollHeight + 40}px`;
        }
      });
    }
  });

  // Mobile Sidemenu
  const sidemenu = document.getElementById('sidemenu');
  const backdrop = document.getElementById('sidemenuBackdrop');
  const navToggleBtns = document.querySelectorAll('.navToggle, .navBarBox, #mobileNavToggle');
  const closeSidemenu = document.querySelectorAll('.closeSidemenu');

  function openMobileMenu() {
    if (sidemenu) sidemenu.classList.add('active');
    if (backdrop) backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    if (sidemenu) sidemenu.classList.remove('active');
    if (backdrop) backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (sidemenu) {
    navToggleBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (sidemenu.classList.contains('active')) {
          closeMobileMenu();
        } else {
          openMobileMenu();
        }
      });
    });

    closeSidemenu.forEach(btn => {
      btn.addEventListener('click', closeMobileMenu);
    });

    if (backdrop) {
      backdrop.addEventListener('click', closeMobileMenu);
    }

    // Close when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (sidemenu.classList.contains('active') && !sidemenu.contains(e.target)) {
        let isToggle = false;
        navToggleBtns.forEach(btn => {
          if (btn.contains(e.target)) isToggle = true;
        });
        if (!isToggle) closeMobileMenu();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && sidemenu.classList.contains('active')) {
        closeMobileMenu();
      }
    });

    // Mobile Sidemenu Accordion Toggle for Submenus
    const submenuToggles = sidemenu.querySelectorAll('.sidemenuToggleBtn, .sidemenuHasSub > .sidemenuLink');
    submenuToggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const parentLi = toggle.closest('.sidemenuHasSub');
        if (!parentLi) return;
        const isOpen = parentLi.classList.contains('open');

        // Close other submenus for a clean single-open accordion
        sidemenu.querySelectorAll('.sidemenuHasSub.open').forEach(item => {
          if (item !== parentLi) {
            item.classList.remove('open');
            const btn = item.querySelector('.sidemenuToggleBtn');
            if (btn) btn.setAttribute('aria-expanded', 'false');
          }
        });

        if (isOpen) {
          parentLi.classList.remove('open');
          toggle.setAttribute('aria-expanded', 'false');
        } else {
          parentLi.classList.add('open');
          toggle.setAttribute('aria-expanded', 'true');
        }
      });
    });

    // Close when clicking actual navigation destination links inside drawer
    sidemenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        const href = link.getAttribute('href');
        if (!href || href === '#' || href === 'javascript:void(0)' || link.classList.contains('sidemenuToggleBtn')) {
          return;
        }
        closeMobileMenu();
      });
    });
  }
}

// Application Initialization
document.addEventListener('DOMContentLoaded', () => {
  initToastSystem();
  initModalSystem();
  setupNavigation();
  setupViewSwitching();
  setupHeroSearch();
  setupHeroMandates();
  initEsightComponents();

  initServicesSection();
  initIndustriesSection();
  initAiStudio();
  initInsightsSection();
  initCandidateForm();
  initClientForm();
  initContactForm();
  if (document.getElementById('adminPortalView')) {
    initAdminDashboard();
  }
  initScrollReveal();
  initSmoothScroll();

  console.log("Thathvamasi HR Consultancy (THC) Enterprise Application initialized.");
});

