/**
 * Thathvamasi HR Consultancy (THC) - Comprehensive Services & Solutions Component
 * Professional Enterprise Service Catalog linking to dedicated practice pages
 */

import { SERVICES_CONFIG } from '../../config/services.config.js';

export function initServicesSection() {
  const container = document.getElementById('servicesGrid');
  const tabs = document.querySelectorAll('.services-tabs .tab-btn');
  if (!container) return;

  function renderServicesList(category = 'all') {
    const filtered = SERVICES_CONFIG.filter(s => {
      if (category === 'all') return true;
      return s.category.toLowerCase().includes(category.toLowerCase());
    });

    container.innerHTML = filtered.map(s => `
      <div class="service-card reveal-card" data-category="${s.category}">
        <div class="service-card-header">
          <div class="service-icon-wrap">${s.icon}</div>
          <span class="service-card-category">${s.category}</span>
        </div>
        <h3 class="service-card-title">${s.title}</h3>
        <p class="service-card-desc">${s.description}</p>
        <div class="service-features-list">
          ${s.features.map(f => `
            <div class="service-feature-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
              <span>${f}</span>
            </div>
          `).join('')}
        </div>
        <div class="service-card-footer">
          <a href="${s.pageUrl}" class="service-detail-link">
            Explore Dedicated Practice &rarr;
          </a>
          <button type="button" class="service-card-btn service-link" data-service="${s.title}">
            Hire for this Role
          </button>
        </div>
      </div>
    `).join('');

    container.querySelectorAll('.service-link').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const title = e.currentTarget.getAttribute('data-service');
        const posInput = document.getElementById('jobTitle');
        const employerSection = document.getElementById('employers');
        if (posInput) {
          posInput.value = `${title} Specialist`;
        }
        if (employerSection) {
          employerSection.scrollIntoView({ behavior: 'smooth' });
          if (window.showToast) {
            window.showToast(`Selected "${title}". Complete your hiring requisition below!`, 'success');
          }
        }
      });
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderServicesList(tab.dataset.cat || 'all');
    });
  });

  renderServicesList('all');
}
