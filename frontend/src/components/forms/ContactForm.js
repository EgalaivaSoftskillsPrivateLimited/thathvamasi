/**
 * Thathvamasi HR Consultancy (THC) - Contact Form Component
 */

import { Storage } from '../../lib/storage.js';
import { Validation } from '../../lib/validation.js';
import { SITE_CONFIG } from '../../config/site.config.js';

export function initContactForm() {
  const contactForm = document.getElementById('generalContactForm');
  const whatsappFloat = document.getElementById('whatsappFloatBtn');
  const quickConsultBtn = document.getElementById('btnQuickConsultWhatsApp');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = contactForm.elements['contactName']?.value.trim();
      const email = contactForm.elements['contactEmail']?.value.trim();
      const mobile = contactForm.elements['contactMobile']?.value.trim();
      const subject = contactForm.elements['contactSubject']?.value;
      const message = contactForm.elements['contactMessage']?.value.trim();

      if (!name || !email || !message) {
        window.showToast('Please fill out all required contact fields', 'error');
        return;
      }

      if (!Validation.isValidEmail(email)) {
        window.showToast('Please enter a valid email address', 'error');
        return;
      }

      Storage.addEnquiry({
        name,
        email,
        mobile: mobile || 'Not Provided',
        subject: subject || 'General Recruitment Query',
        message
      });

      window.showToast('Thank you! Your message has been routed to our Coimbatore advisory desk. We will respond within 4 business hours.', 'success');
      contactForm.reset();
    });
  }

  function launchWhatsApp(context = 'general') {
    const phone = SITE_CONFIG.social.whatsapp;
    let text = "Hello Thathvamasi HR Consultancy! I would like to inquire about your corporate recruitment and talent services in Coimbatore.";
    
    if (context === 'candidate') {
      text = "Hello THC Team! I am an experienced professional looking to explore senior lateral opportunities.";
    } else if (context === 'client') {
      text = "Hello THC Team! Our organization has critical hiring requirements and we would like to discuss recruitment timelines.";
    }

    const url = `https://wa.me/${phone}?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank');
  }

  if (whatsappFloat) {
    whatsappFloat.addEventListener('click', () => launchWhatsApp('general'));
  }

  if (quickConsultBtn) {
    quickConsultBtn.addEventListener('click', () => launchWhatsApp('client'));
  }
}
