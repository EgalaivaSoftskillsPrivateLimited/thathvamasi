/**
 * Global Floating WhatsApp Button Component
 * Attaches a sticky WhatsApp chat button at the bottom-right edge of every page.
 */
export function initFloatingWhatsApp() {
  if (typeof document === 'undefined') return;
  if (document.getElementById('floatingWhatsAppBtn')) return;

  const btn = document.createElement('a');
  btn.id = 'floatingWhatsAppBtn';
  btn.className = 'floating-whatsapp-btn';
  btn.href = 'https://wa.me/918940018882?text=Hello%20Thathvamasi,%20I%20would%20like%20to%20discuss%20corporate%20services';
  btn.target = '_blank';
  btn.rel = 'noopener noreferrer';
  btn.setAttribute('aria-label', 'Chat with Thathvamasi on WhatsApp');
  btn.setAttribute('title', 'Chat on WhatsApp');

  btn.innerHTML = `
    <span class="floating-whatsapp-tooltip">Chat with an Advisor</span>
    <div class="floating-whatsapp-icon-wrap" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="30" height="30" fill="currentColor">
        <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.634.044-1.02-.093-.242-.086-.554-.199-1.002-.394-1.921-.837-3.17-2.775-3.266-2.903-.095-.128-.775-1.03-.775-1.964 0-.934.489-1.393.663-1.583.174-.19.38-.238.506-.238.127 0 .253.002.364.007.119.006.277-.045.434.332.162.388.553 1.349.601 1.447.048.098.08.213.016.34-.064.127-.095.206-.19.317-.095.111-.2.248-.286.333-.095.095-.195.198-.084.388.111.19.493.813 1.057 1.316.726.647 1.338.848 1.529.943.19.095.301.079.412-.048.111-.127.475-.555.602-.745.127-.19.254-.159.428-.095.174.063 1.109.523 1.299.618.19.095.317.143.364.222.048.079.048.459-.096.864z"/>
        <path d="M12 2C6.477 2 2 6.477 2 12c0 1.891.524 3.662 1.435 5.176L2 22l4.957-1.397A9.956 9.956 0 0 0 12 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18.057c-1.616 0-3.132-.489-4.409-1.332l-.316-.21-2.943.829.837-2.871-.225-.327A8.028 8.028 0 0 1 3.943 12c0-4.442 3.615-8.057 8.057-8.057 4.443 0 8.057 3.615 8.057 8.057 0 4.443-3.614 8.057-8.057 8.057z"/>
      </svg>
    </div>
    <span class="floating-whatsapp-pulse" aria-hidden="true"></span>
  `;

  document.body.appendChild(btn);
}

// Auto-initialize when module is loaded or on DOM ready
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFloatingWhatsApp);
  } else {
    initFloatingWhatsApp();
  }
}
