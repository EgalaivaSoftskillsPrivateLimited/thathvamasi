/**
 * Thathvamasi HR Consultancy (THC) - Client Hiring Requisition Form Component
 */

import { Storage } from '../../lib/storage.js';
import { Validation } from '../../lib/validation.js';
import { openModal } from '../ui/Modal.js';

export function initClientForm() {
  const form = document.getElementById('clientRequirementForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const companyName = form.elements['companyName']?.value.trim();
    const contactPerson = form.elements['contactPerson']?.value.trim();
    const officialEmail = form.elements['officialEmail']?.value.trim();
    const mobile = form.elements['clientMobile']?.value.trim();
    const position = form.elements['jobTitle']?.value.trim();
    const vacancies = parseInt(form.elements['vacancies']?.value, 10) || 1;
    const location = form.elements['jobLocation']?.value.trim();

    if (!companyName || !contactPerson) {
      window.showToast('Please provide Company Name and Contact Person', 'error');
      return;
    }

    if (!Validation.isValidEmail(officialEmail)) {
      window.showToast('Please enter a valid official corporate email', 'error');
      return;
    }

    if (!position || !location) {
      window.showToast('Please specify Job Position and Job Location', 'error');
      return;
    }

    const clientPayload = {
      companyName,
      contactPerson,
      designation: form.elements['clientDesignation']?.value.trim() || 'HR Director / Talent Lead',
      email: officialEmail,
      mobile: mobile || 'Not Provided',
      location: form.elements['companyCity']?.value.trim() || location,
      industry: form.elements['companyIndustry']?.value || 'Corporate Enterprise',
      position,
      vacancies,
      experience: form.elements['requiredExp']?.value || '3 - 6 Years',
      salaryRange: form.elements['salaryRange']?.value.trim() || 'Best in Industry',
      employmentType: form.elements['employmentType']?.value || 'Permanent',
      timeline: form.elements['hiringTimeline']?.value || 'Within 30 Days',
      jdSummary: form.elements['jobDescriptionText']?.value.trim() || 'Detailed requirements provided during intake discussion.'
    };

    const saved = Storage.addClient(clientPayload);

    // Show Confirmation Modal
    const refEl = document.getElementById('clientRefId');
    const compEl = document.getElementById('clientConfirmCompany');
    const posEl = document.getElementById('clientConfirmRole');

    if (refEl) refEl.textContent = saved.id;
    if (compEl) compEl.textContent = saved.companyName;
    if (posEl) posEl.textContent = `${saved.position} (${saved.vacancies} Vacancies)`;

    openModal('clientSuccessModal');
    form.reset();
  });
}
