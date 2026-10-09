/**
 * Thathvamasi HR Consultancy (THC) - Contact Form Component
 */

import { Storage } from '../../lib/storage.js';
import { Api } from '../../lib/api.js';
import { Validation } from '../../lib/validation.js';
import { SITE_CONFIG } from '../../config/site.config.js';

export function initContactForm() {
  const contactForms = document.querySelectorAll('#generalContactForm, #contactForm');
  const whatsappFloat = document.getElementById('whatsappFloatBtn');
  const quickConsultBtn = document.getElementById('btnQuickConsultWhatsApp');

  contactForms.forEach(contactForm => {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const getVal = (key) => (
        contactForm.elements[key]?.value ||
        contactForm.querySelector(`#${key}`)?.value ||
        contactForm.querySelector(`[name="${key}"]`)?.value ||
        ''
      ).trim();

      const name = getVal('contactName');
      const email = getVal('contactEmail');
      const mobile = getVal('contactMobile');
      const subject = getVal('contactSubject');
      const message = getVal('contactMessage');

      if (!name || !email) {
        window.showToast('Please provide your name and work email address', 'error');
        return;
      }

      if (!Validation.isValidEmail(email)) {
        window.showToast('Please enter a valid email address', 'error');
        return;
      }

      if (!message) {
        window.showToast('Please provide brief details of your requirement', 'error');
        return;
      }

      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalHtml = submitBtn ? submitBtn.innerHTML : 'Submit Consultation Request &rarr;';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Transmitting Request...';
      }

      try {
        await Api.submitContactEnquiry({
          name,
          email,
          mobile: mobile || 'Not Provided',
          subject: subject || 'General Advisory Query',
          message
        });

        window.showToast('Thank you! Your message has been routed to our Coimbatore advisory desk. We will respond within 2 business hours.', 'success');
        contactForm.reset();
      } catch (err) {
        window.showToast('Could not send message. Please reach us via WhatsApp or phone.', 'error');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalHtml;
        }
      }
    });
  });

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
