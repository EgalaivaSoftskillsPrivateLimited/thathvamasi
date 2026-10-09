/**
 * Thathvamasi HR Consultancy (THC) - Client Hiring Requisition Form Component
 */

import { Storage } from '../../lib/storage.js';
import { Api } from '../../lib/api.js';
import { Validation } from '../../lib/validation.js';
import { openModal } from '../ui/Modal.js';

export function initClientForm() {
  const forms = document.querySelectorAll('#clientRequirementForm');
  if (!forms.length) return;

  forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const getVal = (key) => (
        form.elements[key]?.value ||
        form.querySelector(`#${key}`)?.value ||
        form.querySelector(`[name="${key}"]`)?.value ||
        ''
      ).trim();

      const companyName = getVal('companyName');
      const contactPerson = getVal('contactPerson');
      const officialEmail = getVal('officialEmail');
      const mobile = getVal('clientMobile');
      const position = getVal('jobTitle');
      const vacancies = parseInt(getVal('vacancies'), 10) || 1;
      const location = getVal('jobLocation');

      if (!companyName || !contactPerson) {
        window.showToast?.('Please provide Company Name and Contact Person', 'error');
        return;
      }

      if (!Validation.isValidEmail(officialEmail)) {
        window.showToast?.('Please enter a valid official corporate email', 'error');
        return;
      }

      if (!position) {
        window.showToast?.('Please specify target job position', 'error');
        return;
      }

      const clientPayload = {
        companyName,
        contactPerson,
        designation: getVal('clientDesignation') || 'HR Director / Talent Lead',
        email: officialEmail,
        mobile: mobile || 'Not Provided',
        location: getVal('companyCity') || location || 'Coimbatore',
        industry: getVal('companyIndustry') || getVal('practiceSector') || 'Corporate Enterprise',
        position,
        vacancies,
        experience: getVal('requiredExp') || '3 - 6 Years',
        salaryRange: getVal('salaryRange') || 'Best in Industry',
        employmentType: getVal('employmentType') || 'Permanent',
        timeline: getVal('hiringTimeline') || 'Within 30 Days',
        jdSummary: getVal('jobDescriptionText') || 'Detailed requirements provided during intake discussion.'
      };

      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerText : 'Submit Hiring Mandate';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Registering Requisition...';
      }

      try {
        const saved = await Api.submitClientRequisition(clientPayload);

        // Show Confirmation Modal if present on the page
        const modalEl = document.getElementById('clientSuccessModal');
        const refEl = document.getElementById('clientRefId');
        const compEl = document.getElementById('clientConfirmCompany');
        const posEl = document.getElementById('clientConfirmRole');

        if (refEl) refEl.textContent = saved.id;
        if (compEl) compEl.textContent = saved.companyName;
        if (posEl) posEl.textContent = `${saved.position} (${saved.vacancies} Vacancies)`;

        if (modalEl) {
          openModal('clientSuccessModal');
        } else {
          window.showToast?.(`Mandate registered successfully! Ref: ${saved.id}. An enterprise recruiter will contact you within 2 business hours.`, 'success');
        }
        form.reset();
      } catch (err) {
        window.showToast?.('Requisition submission encountered an error. Please retry.', 'error');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerText = originalText;
        }
      }
    });
  });
}
