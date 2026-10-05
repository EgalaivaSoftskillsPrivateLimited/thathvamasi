/**
 * Thathvamasi HR Consultancy (THC) - Multi-Industry Practices Component
 * TalentPro-Inspired Executive Cards with Inline Expandable Dropdown Drawer
 * Displays Indian CTC Compensation Standards, Corridors & In-Demand Roles
 */

import { INDUSTRIES_CONFIG } from '../../config/industries.config.js';
import { openModal, closeModal } from '../ui/Modal.js';

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

let activeIndustryId = null;

export function initIndustriesSection() {
  const container = document.getElementById('industriesGrid');
  const drawerEl = document.getElementById('industryDropdownDrawer');
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
      const isActive = ind.id === activeIndustryId;

      return `
        <div class="tp-card ${isActive ? 'active-card' : ''}" data-id="${ind.id}" data-category="${ind.category}" role="button" tabindex="0" aria-expanded="${isActive}">
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
              <span>${isActive ? '▲ Hide Breakdown' : '▼ Inspect CTC & Roles'}</span>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Attach click and keyboard handlers
    container.querySelectorAll('.tp-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = card.getAttribute('data-id');
        toggleIndustryDropdown(id, card);
      });
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          const id = card.getAttribute('data-id');
          toggleIndustryDropdown(id, card);
        }
      });
    });
  }

  function toggleIndustryDropdown(industryId, triggerCard) {
    if (!drawerEl) return;

    // Toggle collapse if clicking the currently open card
    if (activeIndustryId === industryId && drawerEl.classList.contains('open')) {
      drawerEl.classList.remove('open');
      drawerEl.style.display = 'none';
      if (triggerCard) {
        triggerCard.classList.remove('active-card');
        triggerCard.setAttribute('aria-expanded', 'false');
        const ind = triggerCard.querySelector('.tp-card-indicator span');
        if (ind) ind.textContent = '▼ Inspect CTC & Roles';
      }
      activeIndustryId = null;
      return;
    }

    const ind = INDUSTRIES_CONFIG.find(i => i.id === industryId);
    if (!ind) return;

    activeIndustryId = industryId;

    // Update active-card class on all cards
    container.querySelectorAll('.tp-card').forEach(c => {
      const isThis = c.getAttribute('data-id') === industryId;
      c.classList.toggle('active-card', isThis);
      c.setAttribute('aria-expanded', isThis ? 'true' : 'false');
      const indSpan = c.querySelector('.tp-card-indicator span');
      if (indSpan) indSpan.textContent = isThis ? '▲ Hide Breakdown' : '▼ Inspect CTC & Roles';
    });

    let selectedRole = ind.keyRoles[0];
    const icon = INDUSTRY_ICONS[ind.id] || `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#FFB900" stroke-width="1.6"><circle cx="12" cy="12" r="10"/></svg>`;
    const hubPills = ind.hubs.split('•').map(h => `<span class="drawer-corridor-tag">📍 ${h.trim()}</span>`).join('');

    drawerEl.innerHTML = `
      <div class="drawer-inner-box">
        <!-- Top Drawer Header -->
        <div class="drawer-header-strip">
          <div class="drawer-header-left">
            <div class="drawer-icon-wrap">${icon}</div>
            <div>
              <div class="drawer-cat-pill">${ind.category}</div>
              <h3 class="drawer-title">${ind.name}</h3>
            </div>
          </div>
          <div class="drawer-header-meta">
            <span class="drawer-meta-chip gold">💼 ${ind.ctcBand}</span>
            <span class="drawer-meta-chip green">⚡ 48-Hour SLA</span>
            <span class="drawer-meta-chip blue">🏆 ${ind.placements}</span>
            <button type="button" class="drawer-close-btn" id="btnCollapseIndustryDrawer" aria-label="Close sector details">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              <span>Close</span>
            </button>
          </div>
        </div>

        <!-- Drawer Content Grid -->
        <div class="drawer-content-grid">
          
          <!-- Left Column: Sector Context, Indian CTC Standards & Corridors -->
          <div class="drawer-main-col">
            <!-- Strategic Overview -->
            <p class="drawer-summary">${ind.summary}</p>

            <!-- Indian CTC Compensation Standards (2026 Benchmarks) -->
            <div class="drawer-block">
              <div class="drawer-block-title">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0060B4" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>
                <span>Indian CTC Compensation Benchmarks (2026 Industry Standards)</span>
              </div>
              <div class="drawer-ctc-grid">
                ${ind.compensationTiers.map(t => `
                  <div class="drawer-ctc-card">
                    <div class="ctc-level">${t.level}</div>
                    <div class="ctc-range">${t.range}</div>
                    <div class="ctc-notice">⏳ ${t.notice}</div>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Active Manufacturing & Tech Corridors -->
            <div class="drawer-block">
              <div class="drawer-block-title">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#D32F2F" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <span>Active Indian Industrial Corridors & Manufacturing Clusters</span>
              </div>
              <div class="drawer-corridors-tray">
                ${hubPills}
              </div>
            </div>

            <!-- Calibrated In-Demand Leadership Roles -->
            <div class="drawer-block">
              <div class="drawer-block-title">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                <span>Select In-Demand Leadership Role to Dispatch:</span>
              </div>
              <div class="drawer-roles-wrap" id="drawerRolesWrap">
                ${ind.keyRoles.map((r, idx) => `
                  <button type="button" class="drawer-role-pill ${idx === 0 ? 'selected' : ''}" data-role="${r}">
                    <span class="role-check">✓</span>
                    <span>${r}</span>
                  </button>
                `).join('')}
              </div>
            </div>
          </div>

          <!-- Right Column: Fast-Track Action Requisition Box -->
          <div class="drawer-side-col">
            <div class="drawer-action-card">
              <div class="action-card-badge">⚡ Instant Requisition Dispatch</div>
              <h4 class="action-card-heading">Post Practice Mandate</h4>
              <p class="action-card-text">Direct allocation to our Senior Practice Director with dedicated 48-hour sourcing pod.</p>

              <div class="action-selected-box">
                <span class="action-selected-label">Selected Role:</span>
                <strong class="action-selected-val" id="drawerSelectedRoleText">${selectedRole}</strong>
              </div>

              <div class="action-guarantee-list">
                <div class="guarantee-row">
                  <span class="check-icon">✓</span>
                  <span><strong>48-Hour Shortlist:</strong> Curated dossiers</span>
                </div>
                <div class="guarantee-row">
                  <span class="check-icon">✓</span>
                  <span><strong>90-Day Free Replacement:</strong> Zero-risk</span>
                </div>
                <div class="guarantee-row">
                  <span class="check-icon">✓</span>
                  <span><strong>100% Statutory Assured:</strong> 2026 Labor Code</span>
                </div>
              </div>

              <button type="button" class="btn-primary-submit drawer-action-btn" id="btnDrawerDispatchHire">
                Dispatch Requisition for this Sector &rarr;
              </button>

              <button type="button" class="btn-whatsapp-consult drawer-whatsapp-btn" id="btnDrawerWhatsApp">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91C2.13 13.66 2.59 15.36 3.45 16.86L2.05 22L7.3 20.62C8.75 21.41 10.38 21.83 12.04 21.83C17.5 21.83 21.95 17.38 21.95 11.92C21.95 9.27 20.92 6.78 19.05 4.91C17.18 3.03 14.69 2 12.04 2ZM12.05 20.15C10.57 20.15 9.12 19.76 7.85 19L7.55 18.83L4.43 19.65L5.26 16.61L5.07 16.3C4.24 14.98 3.8 13.47 3.8 11.91C3.8 7.37 7.5 3.67 12.05 3.67C14.25 3.67 16.31 4.53 17.87 6.09C19.42 7.65 20.28 9.72 20.28 11.92C20.28 16.46 16.58 20.15 12.05 20.15ZM16.57 14.36C16.32 14.24 15.1 13.64 14.87 13.56C14.65 13.47 14.48 13.43 14.32 13.68C14.15 13.93 13.68 14.48 13.54 14.64C13.4 14.81 13.26 14.83 13.01 14.71C12.76 14.58 11.97 14.32 11.03 13.49C10.29 12.83 9.79 12.02 9.65 11.77C9.51 11.52 9.63 11.39 9.76 11.26C9.87 11.15 10.01 10.97 10.14 10.82C10.27 10.67 10.31 10.56 10.39 10.39C10.47 10.23 10.43 10.08 10.37 9.96C10.31 9.84 9.81 8.62 9.61 8.11C9.41 7.62 9.21 7.69 9.06 7.68C8.92 7.67 8.76 7.67 8.59 7.67C8.42 7.67 8.15 7.73 7.92 7.98C7.69 8.23 7.05 8.83 7.05 10.05C7.05 11.27 7.94 12.44 8.06 12.61C8.19 12.78 9.8 15.26 12.28 16.33C12.87 16.59 13.33 16.74 13.69 16.85C14.29 17.04 14.83 17.01 15.26 16.95C15.74 16.88 16.74 16.35 16.95 15.76C17.15 15.17 17.15 14.67 17.09 14.56C17.03 14.46 16.82 14.48 16.57 14.36Z"/></svg>
                WhatsApp Practice Desk
              </button>
            </div>
          </div>

        </div>
      </div>
    `;

    // Wire up role chip clicks
    drawerEl.querySelectorAll('.drawer-role-pill').forEach(btn => {
      btn.addEventListener('click', (e) => {
        drawerEl.querySelectorAll('.drawer-role-pill').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedRole = btn.getAttribute('data-role');
        const roleLabel = document.getElementById('drawerSelectedRoleText');
        if (roleLabel) roleLabel.textContent = selectedRole;
      });
    });

    // Wire up close button
    const closeBtn = document.getElementById('btnCollapseIndustryDrawer');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        drawerEl.classList.remove('open');
        drawerEl.style.display = 'none';
        container.querySelectorAll('.tp-card').forEach(c => {
          c.classList.remove('active-card');
          c.setAttribute('aria-expanded', 'false');
          const indSpan = c.querySelector('.tp-card-indicator span');
          if (indSpan) indSpan.textContent = '▼ Inspect CTC & Roles';
        });
        activeIndustryId = null;
      });
    }

    // Wire up Requisition Dispatch button
    const dispatchBtn = document.getElementById('btnDrawerDispatchHire');
    if (dispatchBtn) {
      dispatchBtn.addEventListener('click', () => {
        const industrySelect = document.getElementById('companyIndustry');
        const posInput = document.getElementById('jobTitle');
        const employerSection = document.getElementById('employers');

        if (industrySelect) {
          let found = false;
          for (let opt of industrySelect.options) {
            if (opt.text.toLowerCase().includes(ind.name.toLowerCase()) || 
                ind.name.toLowerCase().includes(opt.value.toLowerCase())) {
              industrySelect.value = opt.value;
              found = true;
              break;
            }
          }
          if (!found) {
            const newOpt = new Option(ind.name, ind.name, true, true);
            industrySelect.add(newOpt);
          }
        }

        if (posInput && selectedRole) {
          posInput.value = selectedRole;
        }

        if (employerSection) {
          employerSection.scrollIntoView({ behavior: 'smooth' });
          if (window.showToast) {
            window.showToast(`Selected "${ind.name}" practice (${selectedRole}). Complete requisition below!`, 'success');
          }
        }
      });
    }

    // Wire up WhatsApp consultation button
    const waBtn = document.getElementById('btnDrawerWhatsApp');
    if (waBtn) {
      waBtn.addEventListener('click', () => {
        const msg = encodeURIComponent(`Hello Thathvamasi Team, I would like to consult with your Practice Director regarding hiring for "${selectedRole}" in the ${ind.name} sector.`);
        window.open(`https://wa.me/919442218900?text=${msg}`, '_blank');
      });
    }

    // Show drawer with animation
    drawerEl.style.display = 'block';
    drawerEl.classList.add('open');

    // Smooth scroll into view
    setTimeout(() => {
      const topOffset = drawerEl.getBoundingClientRect().top + window.pageYOffset - 110;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }, 50);
  }

  // Filter Tabs
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      renderIndustriesList(tab.dataset.cat || 'all');
    });
  });

  renderIndustriesList('all');
}

export function openIndustryModal(industryId) {
  const ind = INDUSTRIES_CONFIG.find(i => i.id === industryId);
  if (!ind) return;

  const modalName = document.getElementById('modalIndName');
  const modalCategory = document.getElementById('modalIndCategory');
  const modalBody = document.getElementById('modalIndBody');
  const hireBtn = document.getElementById('modalIndHireBtn');

  if (modalName) modalName.textContent = ind.name;
  if (modalCategory) modalCategory.textContent = ind.category;

  let selectedRole = ind.keyRoles[0];

  if (modalBody) {
    modalBody.innerHTML = `
      <div class="industry-modal-content">
        <p class="ind-modal-summary">${ind.summary}</p>
        <div class="ind-modal-section">
          <div class="ind-modal-section-title">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0060B4" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>
            Indian CTC Compensation Standards (2026 Benchmarks)
          </div>
          <div class="ind-ctc-tiers-grid">
            ${ind.compensationTiers.map(t => `
              <div class="ind-tier-card">
                <span class="tier-level">${t.level}</span>
                <span class="tier-range">${t.range}</span>
                <span class="tier-notice">⏳ ${t.notice}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <div class="ind-modal-section">
          <div class="ind-modal-section-title">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#D32F2F" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            Active Indian Corridors & Industrial Hubs
          </div>
          <div class="ind-corridors-pill">
            ${ind.hubs}
          </div>
        </div>

        <div class="ind-modal-section">
          <div class="ind-modal-section-title">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            Select a Calibrated Leadership Role to Hire:
          </div>
          <div class="ind-roles-interactive-grid" id="modalRolesContainer">
            ${ind.keyRoles.map((r, i) => `
              <button type="button" class="modal-role-select-chip ${i === 0 ? 'selected' : ''}" data-role="${r}">
                ${r}
              </button>
            `).join('')}
          </div>
        </div>
      </div>
    `;

    modalBody.querySelectorAll('.modal-role-select-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        modalBody.querySelectorAll('.modal-role-select-chip').forEach(c => c.classList.remove('selected'));
        e.currentTarget.classList.add('selected');
        selectedRole = e.currentTarget.getAttribute('data-role');
      });
    });
  }

  if (hireBtn) {
    hireBtn.onclick = () => {
      closeModal('industryDetailModal');
      const industrySelect = document.getElementById('companyIndustry');
      const posInput = document.getElementById('jobTitle');
      const employerSection = document.getElementById('employers');

      if (industrySelect) {
        let found = false;
        for (let opt of industrySelect.options) {
          if (opt.text.toLowerCase().includes(ind.name.toLowerCase()) || 
              ind.name.toLowerCase().includes(opt.value.toLowerCase())) {
            industrySelect.value = opt.value;
            found = true;
            break;
          }
        }
        if (!found) {
          const newOpt = new Option(ind.name, ind.name, true, true);
          industrySelect.add(newOpt);
        }
      }

      if (posInput && selectedRole) {
        posInput.value = selectedRole;
      }

      if (employerSection) {
        employerSection.scrollIntoView({ behavior: 'smooth' });
        if (window.showToast) {
          window.showToast(`Selected "${ind.name}" practice (${selectedRole}). Dispatch your requirement below!`, 'success');
        }
      }
    };
  }

  openModal('industryDetailModal');
}
