/**
 * Thathvamasi HR Consultancy (THC) - Application Entry Point
 * Theme: Zoho-Inspired Professional Enterprise Light Theme
 */

// Stylesheets
import './styles/variables.css';
import './styles/base.css';
import './styles/components.css';
import './styles/admin.css';
import './styles/responsive.css';

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
  const dropdownContainers = document.querySelectorAll('.nav-item.has-dropdown');
  dropdownContainers.forEach(container => {
    const toggle = container.querySelector('.dropdown-toggle');
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
  const btnExitAdmin = document.getElementById('btnExitAdmin');
  const mainSiteView = document.getElementById('mainSiteView');
  const adminPortalView = document.getElementById('adminPortalView');
  const navLinks = document.querySelectorAll('.nav-link');

  function showAdmin() {
    if (mainSiteView && adminPortalView) {
      mainSiteView.style.display = 'none';
      adminPortalView.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      window.showToast('Logged into THC HR Command Center (Admin Mode)', 'info');
    }
  }

  function showMainSite() {
    if (mainSiteView && adminPortalView) {
      adminPortalView.classList.remove('active');
      mainSiteView.style.display = 'block';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  if (btnToggleAdmin) btnToggleAdmin.addEventListener('click', showAdmin);
  if (btnExitAdmin) btnExitAdmin.addEventListener('click', showMainSite);

  const brandLink = document.querySelector('.brand');
  if (brandLink) {
    brandLink.addEventListener('click', () => {
      showMainSite();
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

// Application Initialization
document.addEventListener('DOMContentLoaded', () => {
  initToastSystem();
  initModalSystem();
  setupNavigation();
  setupViewSwitching();
  setupHeroSearch();
  setupHeroMandates();

  initServicesSection();
  initIndustriesSection();
  initAiStudio();
  initInsightsSection();
  initCandidateForm();
  initClientForm();
  initContactForm();
  initAdminDashboard();
  initScrollReveal();

  console.log("Thathvamasi HR Consultancy (THC) Enterprise Application initialized.");
});

