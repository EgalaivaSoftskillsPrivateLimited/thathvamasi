/**
 * Thathvamasi HR Consultancy (THC) - Form Validation Utilities
 */

export const Validation = {
  isValidEmail(email) {
    if (!email) return false;
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).trim());
  },

  isValidIndianPhone(phone) {
    if (!phone) return false;
    const clean = phone.replace(/[\s\-\(\)\+]/g, '');
    return clean.length >= 10 && clean.length <= 13;
  },

  isValidFile(file, allowedExtensions = ['pdf', 'doc', 'docx'], maxSizeBytes = 5 * 1024 * 1024) {
    if (!file) return { valid: false, error: 'No file provided.' };
    const ext = file.name.split('.').pop().toLowerCase();
    if (!allowedExtensions.includes(ext)) {
      return { valid: false, error: `Invalid file format (.${ext}). Only PDF, DOC, and DOCX are permitted.` };
    }
    if (file.size > maxSizeBytes) {
      return { valid: false, error: `File size exceeds the ${(maxSizeBytes / (1024 * 1024)).toFixed(0)}MB limit.` };
    }
    return { valid: true };
  }
};
