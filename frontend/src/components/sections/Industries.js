/**
 * Thathvamasi HR Consultancy (THC) - Multi-Industry Practices Component
 * TalentPro-Inspired Executive Cards linking to Dedicated Practice Pages
 * Displays Indian CTC Compensation Standards, Corridors & In-Demand Roles
 */

import { INDUSTRIES_CONFIG } from '../../config/industries.config.js';

const INDUSTRY_ICONS = {
  'auto-ev': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9C2.1 11.2 2 11.6 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>`,
  'it-gcc': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/><polyline points="7 8 10 11 7 14"/><line x1="12" y1="14" x2="16" y2="14"/></svg>`,
  'engineering-foundry': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>`,
  'textiles-apparel': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`,
  'bfsi-fintech': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="21" x2="21" y2="21"/><line x1="3" y1="10" x2="21" y2="10"/><polyline points="5 6 12 3 19 6"/><line x1="4" y1="10" x2="4" y2="21"/><line x1="9" y1="10" x2="9" y2="21"/><line x1="15" y1="10" x2="15" y2="21"/><line x1="20" y1="10" x2="20" y2="21"/></svg>`,
  'pharma-healthcare': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>`,
  'fmcg-retail': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>`,
  'renewable-energy': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
  'infra-construction': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v8h4"/><path d="M18 9h2a2 2 0 0 1 2 2v11h-4"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/></svg>`,
  'logistics-supply-chain': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>`,
  'electronics-ems': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>`,
  'chemicals-materials': `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M10 2v7.31L4.17 19.86A2 2 0 0 0 5.86 23h12.28a2 2 0 0 0 1.69-3.14L14 9.31V2"/><line x1="8.5" y1="2" x2="15.5" y2="2"/><line x1="6.5" y1="15" x2="17.5" y2="15"/></svg>`
};

export function initIndustriesSection() {
  const container = document.getElementById('industriesGrid');
  const tabs = document.querySelectorAll('.industry-tabs .tab-btn');
  if (!container) return;

  function renderIndustriesList(category = 'all') {
    const filtered = INDUSTRIES_CONFIG.filter(ind => {
      if (category === 'all') return true;
      return ind.category.toLowerCase().includes(category.toLowerCase()) || 
             ind.name.toLowerCase().includes(category.toLowerCase());
    });

    container.innerHTML = filtered.map(ind => {
      const icon = INDUSTRY_ICONS[ind.id] || `<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6"><circle cx="12" cy="12" r="10"/><path d="M12 8v8M8 12h8"/></svg>`;

      return `
        <a href="/industries/${ind.id}.html" class="tp-card" data-id="${ind.id}" data-category="${ind.category}" aria-label="Explore ${ind.name} dedicated practice">
          <img src="${ind.image}" alt="${ind.name}" class="tp-card-bg" loading="lazy" onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=600&q=80';">
          <div class="tp-card-overlay"></div>
          <div class="tp-card-content">
            <div class="tp-card-icon">
              ${icon}
            </div>
            <h3 class="tp-card-title">${ind.name}</h3>
            <div class="tp-card-badge">
              <span>${ind.ctcBand}</span>
            </div>
            <div class="tp-card-indicator">
              <span>Explore Dedicated Practice &rarr;</span>
            </div>
          </div>
        </a>
      `;
    }).join('');
  }

  // Initial render
  renderIndustriesList('all');

  // Filter tabs
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const cat = tab.getAttribute('data-cat') || 'all';
      renderIndustriesList(cat);
    });
  });
}
