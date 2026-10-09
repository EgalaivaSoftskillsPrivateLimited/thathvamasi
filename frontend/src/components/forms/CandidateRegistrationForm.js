/**
 * Thathvamasi HR Consultancy (THC) - Candidate Registration Form Component
 */

import { Storage } from '../../lib/storage.js';
import { Api } from '../../lib/api.js';
import { Validation } from '../../lib/validation.js';
import { openModal } from '../ui/Modal.js';

export function initCandidateForm() {
  const form = document.getElementById('candidateForm');
  if (!form) return;

  let currentStep = 1;
  const totalSteps = 3;
  let uploadedFile = null;

  const stepItems = document.querySelectorAll('.stepper .step-item');
  const stepPanels = document.querySelectorAll('.step-panel');
  const stepperProgress = document.getElementById('stepperProgress');

  const btnNext = document.getElementById('btnCandidateNext');
  const btnPrev = document.getElementById('btnCandidatePrev');
  const btnSubmit = document.getElementById('btnCandidateSubmit');

  const dropzone = document.getElementById('resumeDropzone');
  const fileInput = document.getElementById('resumeFileInput');
  const previewArea = document.getElementById('resumeFilePreview');
  const removeFileBtn = document.getElementById('btnRemoveFile');

  function updateStepper() {
    stepItems.forEach((item, index) => {
      const stepNum = index + 1;
      item.classList.remove('active', 'completed');
      if (stepNum < currentStep) {
        item.classList.add('completed');
      } else if (stepNum === currentStep) {
        item.classList.add('active');
      }
    });

    stepPanels.forEach((panel) => {
      const step = parseInt(panel.getAttribute('data-step'), 10);
      panel.style.display = step === currentStep ? 'block' : 'none';
    });

    if (stepperProgress) {
      const progressPercent = ((currentStep - 1) / (totalSteps - 1)) * 100;
      stepperProgress.style.width = `${progressPercent}%`;
    }

    if (btnPrev) btnPrev.style.display = currentStep > 1 ? 'inline-flex' : 'none';
    if (btnNext) btnNext.style.display = currentStep < totalSteps ? 'inline-flex' : 'none';
    if (btnSubmit) btnSubmit.style.display = currentStep === totalSteps ? 'inline-flex' : 'none';
  }

  function validateStep1() {
    const name = form.elements['candidateName']?.value.trim();
    const email = form.elements['candidateEmail']?.value.trim();
    const mobile = form.elements['candidateMobile']?.value.trim();
    const location = form.elements['candidateLocation']?.value.trim();

    if (!name || name.length < 2) {
      window.showToast('Please enter your full name', 'error');
      return false;
    }
    if (!Validation.isValidEmail(email)) {
      window.showToast('Please enter a valid email address', 'error');
      return false;
    }
    if (!Validation.isValidIndianPhone(mobile)) {
      window.showToast('Please enter a valid 10-digit mobile number', 'error');
      return false;
    }
    if (!location) {
      window.showToast('Please provide your current city/location', 'error');
      return false;
    }
    return true;
  }

  function validateStep2() {
    const qual = form.elements['candidateQualification']?.value;
    const exp = form.elements['candidateExperience']?.value;
    const skills = form.elements['candidateSkills']?.value.trim();

    if (!qual) {
      window.showToast('Please select your highest qualification', 'error');
      return false;
    }
    if (!exp) {
      window.showToast('Please select your total work experience', 'error');
      return false;
    }
    if (!skills) {
      window.showToast('Please enter key skills or competencies', 'error');
      return false;
    }
    return true;
  }

  function validateStep3() {
    if (!uploadedFile) {
      window.showToast('Please attach your resume (PDF or Word format)', 'error');
      return false;
    }
    const consent = form.elements['candidateConsent']?.checked;
    if (!consent) {
      window.showToast('You must consent to THC storing your profile for recruitment evaluation', 'error');
      return false;
    }
    return true;
  }

  if (btnNext) {
    btnNext.addEventListener('click', () => {
      if (currentStep === 1 && !validateStep1()) return;
      if (currentStep === 2 && !validateStep2()) return;
      if (currentStep < totalSteps) {
        currentStep++;
        updateStepper();
      }
    });
  }

  if (btnPrev) {
    btnPrev.addEventListener('click', () => {
      if (currentStep > 1) {
        currentStep--;
        updateStepper();
      }
    });
  }

  function handleFileSelected(file) {
    const validation = Validation.isValidFile(file);
    if (!validation.valid) {
      window.showToast(validation.error, 'error');
      return;
    }

    uploadedFile = file;

    if (previewArea) {
      const fileNameEl = previewArea.querySelector('.file-name');
      const fileSizeEl = previewArea.querySelector('.file-size');
      if (fileNameEl) fileNameEl.textContent = file.name;
      if (fileSizeEl) fileSizeEl.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB`;
      previewArea.style.display = 'flex';
    }

    if (dropzone) dropzone.style.display = 'none';
    window.showToast(`Resume attached: ${file.name}`, 'info');
  }

  if (dropzone && fileInput) {
    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelected(e.target.files[0]);
      }
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('dragover');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFileSelected(e.dataTransfer.files[0]);
      }
    });
  }

  if (removeFileBtn) {
    removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      uploadedFile = null;
      if (fileInput) fileInput.value = '';
      if (previewArea) previewArea.style.display = 'none';
      if (dropzone) dropzone.style.display = 'block';
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validateStep3()) return;

    const rawSkills = form.elements['candidateSkills']?.value || '';
    const skillsArray = rawSkills.split(',').map(s => s.trim()).filter(Boolean);

    const candidatePayload = {
      name: form.elements['candidateName']?.value.trim(),
      email: form.elements['candidateEmail']?.value.trim(),
      mobile: form.elements['candidateMobile']?.value.trim(),
      whatsapp: form.elements['candidateWhatsapp']?.value.trim() || form.elements['candidateMobile']?.value.trim(),
      currentLocation: form.elements['candidateLocation']?.value.trim(),
      preferredLocation: form.elements['candidatePrefLocation']?.value.trim() || 'Coimbatore',
      qualification: form.elements['candidateQualification']?.value,
      experience: form.elements['candidateExperience']?.value,
      currentCompany: form.elements['candidateCompany']?.value.trim() || 'Confidential',
      currentDesignation: form.elements['candidateDesignation']?.value.trim() || 'Professional',
      currentCtc: form.elements['candidateCtc']?.value.trim() ? `${form.elements['candidateCtc']?.value.trim()} LPA` : 'Not Disclosed',
      expectedCtc: form.elements['candidateExpCtc']?.value.trim() ? `${form.elements['candidateExpCtc']?.value.trim()} LPA` : 'As per norms',
      noticePeriod: form.elements['candidateNotice']?.value || 'Immediate',
      skills: skillsArray.length ? skillsArray : ['General Skills'],
      resumeFileName: uploadedFile ? uploadedFile.name : 'Resume_Uploaded.pdf',
      resumeFileSize: uploadedFile ? `${(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB` : '1.8 MB'
    };

    if (btnSubmit) {
      btnSubmit.disabled = true;
      btnSubmit.textContent = 'Registering Profile...';
    }

    try {
      const saved = await Api.submitCandidate(candidatePayload, uploadedFile);

      // Show Confirmation Modal
      const refEl = document.getElementById('candidateRefId');
      const nameEl = document.getElementById('candidateConfirmName');
      if (refEl) refEl.textContent = saved.id;
      if (nameEl) nameEl.textContent = saved.name;
      openModal('candidateSuccessModal');

      // Reset Form
      form.reset();
      uploadedFile = null;
      if (previewArea) previewArea.style.display = 'none';
      if (dropzone) dropzone.style.display = 'block';
      currentStep = 1;
      updateStepper();
    } catch (err) {
      window.showToast('Registration encountered an error. Please try again.', 'error');
    } finally {
      if (btnSubmit) {
        btnSubmit.disabled = false;
        btnSubmit.textContent = 'Submit Application';
      }
    }
  });

  updateStepper();
}
