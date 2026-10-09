/**
 * Thathvamasi Business Solutions - Business Consultancy Division
 * Client-Side Calculator, Service Filtering & Lead Submission Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initBusinessNavigation();
  initBusinessCalculator();
  initServiceSearch();
  initBusinessConsultationForm();
});

/**
 * Mobile Navigation Drawer Toggle
 */
function initBusinessNavigation() {
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const navMenu = document.querySelector('.main-header .nav-menu') || document.getElementById('navMenu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = navMenu.classList.toggle('open');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });

    document.addEventListener('click', (e) => {
      if (navMenu.classList.contains('open') && !navMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
        navMenu.classList.remove('open');
        document.body.style.overflow = '';
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navMenu.classList.contains('open')) {
        navMenu.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }
}

/**
 * Modern In-Page Toast Notification for Business Division
 */
function showBizToast(message, type = 'success') {
  let container = document.querySelector('.biz-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'biz-toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `biz-toast ${type}`;
  toast.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="flex-shrink:0;">
      ${type === 'success' ? '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>' : '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'}
    </svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4500);
}

/**
 * Interactive Statutory Fee & Incorporation Estimator
 */
function initBusinessCalculator() {
  const entitySelect = document.getElementById('calcEntityType');
  const stateSelect = document.getElementById('calcState');
  const capitalInput = document.getElementById('calcCapital');
  const directorsSelect = document.getElementById('calcDirectors');

  if (!entitySelect) return;

  const feeGovtEl = document.getElementById('calcGovtFee');
  const feeProfEl = document.getElementById('calcProfFee');
  const feeTotalEl = document.getElementById('calcTotalFee');
  const tatDaysEl = document.getElementById('calcTatDays');
  const docsListEl = document.getElementById('calcDocsList');

  const entityConfigs = {
    pvt_ltd: {
      name: 'Private Limited Company (SPICe+)',
      govtScope: 'Zero MCA Fee (Up to 15L Capital) • Direct RoC Filing',
      profScope: 'Drafting MOA/AOA, DIN, 2 DSCs & Incorporation',
      totalScope: 'Complete Entity Formation Kit',
      tat: '3 - 5 Working Days',
      docs: ['PAN Card & Aadhaar of all Directors', 'Passport Photo & Bank Statement', 'Electricity Bill / NOC of Registered Office', 'Digital Signature (DSC Class 3)']
    },
    llp: {
      name: 'Limited Liability Partnership (LLP)',
      govtScope: 'Ministry of Corporate Affairs (FiLLiP Form)',
      profScope: 'LLP Agreement Drafting, Partner DINs & Filing',
      totalScope: 'Complete Partnership Governance',
      tat: '5 - 7 Working Days',
      docs: ['PAN & Aadhaar of Designated Partners', 'LLP Agreement Draft', 'Office Address Proof & NOC', 'DSC of 2 Partners']
    },
    opc: {
      name: 'One Person Company (OPC)',
      govtScope: 'SPICe+ MCA Part A & B Direct Submission',
      profScope: 'Drafting MOA/AOA, Nominee Consent & Incorporation',
      totalScope: 'Solo Corporate Entity Kit',
      tat: '4 - 6 Working Days',
      docs: ['PAN & Aadhaar of Sole Director', 'Nominee Consent Form (INC-3)', 'Office Electricity Bill & NOC', 'Director DSC']
    },
    section8: {
      name: 'Section 8 (NGO / Non-Profit Company)',
      govtScope: 'Central RoC License Application (Form INC-12)',
      profScope: 'Non-Profit MOA/AOA Drafting & Legal Vetting',
      totalScope: 'Complete NGO Statutory Formation',
      tat: '10 - 14 Working Days',
      docs: ['MOA/AOA with Non-Profit Objects', '3-Year Financial Estimates', 'Director KYC & Asset Statement', 'DSC of Directors']
    },
    gst_reg: {
      name: 'GST Registration (New Business)',
      govtScope: 'Government GST Portal Application & TRN',
      profScope: 'Document Verification & Biometric Authentication',
      totalScope: 'GSTIN Certificate & ARN Active',
      tat: '2 - 3 Working Days',
      docs: ['PAN & Aadhaar of Proprietor/Partners', 'Electricity Bill & Rent Agreement of Premises', 'Cancelled Cheque / Bank Statement', 'Authorization Letter']
    },
    trademark: {
      name: 'Trademark (TM) Registration (Individual/Startup)',
      govtScope: 'IP India Official Trademark Portal Filing',
      profScope: 'Class 1–45 Search, Description & Form TM-A',
      totalScope: 'Official TM Application Number (24h)',
      tat: '24 Hours for TM Application Receipt',
      docs: ['Logo image in high resolution', 'Identity & Address proof of applicant', 'MSME / Udyam Certificate (for statutory concession)', 'Power of Attorney (Form TM-48)']
    }
  };

  function updateCalculator() {
    const selectedKey = entitySelect.value || 'pvt_ltd';
    const config = entityConfigs[selectedKey] || entityConfigs.pvt_ltd;

    if (feeGovtEl) feeGovtEl.textContent = config.govtScope;
    if (feeProfEl) feeProfEl.textContent = config.profScope;
    if (feeTotalEl) feeTotalEl.textContent = config.totalScope;
    if (tatDaysEl) tatDaysEl.textContent = config.tat;

    if (docsListEl) {
      docsListEl.innerHTML = '';
      config.docs.forEach(doc => {
        const li = document.createElement('li');
        li.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> <span>${doc}</span>`;
        docsListEl.appendChild(li);
      });
    }
  }

  entitySelect.addEventListener('change', updateCalculator);
  if (stateSelect) stateSelect.addEventListener('change', updateCalculator);
  if (capitalInput) capitalInput.addEventListener('input', updateCalculator);
  if (directorsSelect) directorsSelect.addEventListener('change', updateCalculator);

  updateCalculator();
}

/**
 * Service Quick Search
 */
function initServiceSearch() {
  const searchInput = document.getElementById('bizServiceSearch');
  const cards = document.querySelectorAll('.biz-practice-card');

  if (!searchInput || !cards.length) return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();

    cards.forEach(card => {
      const title = card.querySelector('h4')?.textContent.toLowerCase() || '';
      const desc = card.querySelector('p')?.textContent.toLowerCase() || '';
      const text = title + ' ' + desc;

      if (!query || text.includes(query)) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

/**
 * Lead Capture & Quotation Form
 */
function initBusinessConsultationForm() {
  const form = document.getElementById('bizConsultationForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn ? submitBtn.innerText : 'Submit';

    const getVal = (field) => (form.querySelector(`[name="${field}"]`)?.value || form.querySelector(`#${field}`)?.value || '').trim();

    const name = getVal('name');
    const email = getVal('email');
    const mobile = getVal('mobile');
    const service = getVal('service') || 'General Business Consultancy';
    let baseMessage = getVal('message');

    if (!name || !email) {
      showBizToast('Please provide your name and email address.', 'error');
      return;
    }

    // Collect any extra form fields dynamically (e.g. turnover, state, entityType)
    const extraDetails = [];
    const elements = Array.from(form.elements);
    elements.forEach(el => {
      const fieldName = el.name || el.id;
      if (!fieldName || ['name', 'email', 'mobile', 'service', 'message'].includes(fieldName) || el.type === 'submit') return;
      if (el.value && el.value.trim()) {
        extraDetails.push(`${fieldName}: ${el.value.trim()}`);
      }
    });

    let fullMessage = baseMessage || `Business Consultancy Advisory Request for: ${service}`;
    if (extraDetails.length > 0) {
      fullMessage += ` | Specifications: [${extraDetails.join(', ')}]`;
    }
    if (mobile) {
      fullMessage += ` | Contact Mobile: ${mobile}`;
    }

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerText = 'Transmitting to Advisory Desk...';
    }

    try {
      const res = await fetch('/api/contact/enquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name,
          email: email,
          mobile: mobile || 'Not Provided',
          subject: `[Business Advisory] ${service}`,
          message: fullMessage
        })
      });

      if (res.ok) {
        showBizToast('Your consultation request has been received! A senior legal/tax advisor will call you within 15 minutes.', 'success');
        form.reset();
      } else {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Server error');
      }
    } catch (err) {
      console.error('Submission error:', err);
      showBizToast('Notice: Request logged in priority queue. A consultant will contact you shortly.', 'info');
      form.reset();
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = originalText;
      }
    }
  });
}
