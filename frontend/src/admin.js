/**
 * Thathvamasi HR Consultancy (THC) - Admin Console Entry Point
 * Controls Administrator Authentication, Session Lifecycle, and Command Center
 */

import { initToastSystem } from './components/ui/Toast.js';
import { initModalSystem } from './components/ui/Modal.js';
import { Api } from './lib/api.js';
import { initAdminDashboard } from './components/admin/AdminDashboard.js';

document.addEventListener('DOMContentLoaded', async () => {
  // Initialize Toast and Modal UI systems
  initToastSystem();
  initModalSystem();

  // DOM Elements
  const adminLoginView = document.getElementById('adminLoginView');
  const adminPortalView = document.getElementById('adminPortalView');
  const adminLoginForm = document.getElementById('adminLoginForm');
  const adminSetupForm = document.getElementById('adminSetupForm');
  const adminEmailInput = document.getElementById('adminEmailInput');
  const adminPasswordInput = document.getElementById('adminPasswordInput');
  const adminSetupFullName = document.getElementById('adminSetupFullName');
  const adminSetupEmail = document.getElementById('adminSetupEmail');
  const adminSetupPassword = document.getElementById('adminSetupPassword');
  const btnModeSignIn = document.getElementById('btnModeSignIn');
  const btnModeSetup = document.getElementById('btnModeSetup');
  const authCardHeading = document.getElementById('authCardHeading');
  const authCardSubheading = document.getElementById('authCardSubheading');
  const btnAdminSetupSubmit = document.getElementById('btnAdminSetupSubmit');
  const btnTogglePassword = document.getElementById('btnTogglePassword');
  const pwdEyeOpen = document.getElementById('pwdEyeOpen');
  const pwdEyeClosed = document.getElementById('pwdEyeClosed');
  const btnAdminSubmit = document.getElementById('btnAdminSubmit');
  const loginAlertBox = document.getElementById('loginAlertBox');
  const loginAlertMsg = document.getElementById('loginAlertMsg');
  const btnHeaderLogout = document.getElementById('btnHeaderLogout');
  const btnExitAdmin = document.getElementById('btnExitAdmin');
  const headerAuthBadge = document.getElementById('headerAuthBadge');
  const sidebarUserName = document.getElementById('sidebarUserName');
  const sidebarUserRole = document.getElementById('sidebarUserRole');

  // Mobile Drawer Elements
  const adminMobileSidebarToggle = document.getElementById('adminMobileSidebarToggle');
  const adminSidebar = document.getElementById('adminSidebar');
  const adminSidebarBackdrop = document.getElementById('adminSidebarBackdrop');
  const adminSidebarClose = document.getElementById('adminSidebarClose');

  let dashboardInitialized = false;

  function showAlert(message, type = 'error') {
    if (!loginAlertBox || !loginAlertMsg) return;
    loginAlertMsg.textContent = message;
    loginAlertBox.className = `login-alert ${type}`;
    loginAlertBox.style.display = 'flex';
  }

  function hideAlert() {
    if (!loginAlertBox) return;
    loginAlertBox.style.display = 'none';
  }

  function renderAuthenticatedState(user) {
    if (adminLoginView) adminLoginView.style.display = 'none';
    if (adminPortalView) {
      adminPortalView.style.display = 'block';
      adminPortalView.classList.add('active');
    }
    if (btnHeaderLogout) btnHeaderLogout.style.display = 'inline-flex';
    if (headerAuthBadge) headerAuthBadge.style.display = 'inline-block';

    if (sidebarUserName && user) {
      sidebarUserName.textContent = user.full_name || 'Command Center';
    }
    if (sidebarUserRole && user) {
      sidebarUserRole.textContent = user.email || 'Administrator';
    }

    if (!dashboardInitialized) {
      initAdminDashboard();
      dashboardInitialized = true;
    } else {
      // Trigger update of overview KPIs if already initialized
      window.dispatchEvent(new CustomEvent('thc:data-changed'));
    }
  }

  function renderUnauthenticatedState() {
    if (adminPortalView) {
      adminPortalView.style.display = 'none';
      adminPortalView.classList.remove('active');
    }
    if (adminLoginView) adminLoginView.style.display = 'flex';
    if (btnHeaderLogout) btnHeaderLogout.style.display = 'none';
    if (headerAuthBadge) headerAuthBadge.style.display = 'none';
    hideAlert();
  }

  // 1. Auth Mode Switcher (Sign In vs Create Admin)
  function setAuthMode(mode) {
    hideAlert();
    if (mode === 'setup') {
      if (btnModeSignIn) btnModeSignIn.classList.remove('active');
      if (btnModeSetup) btnModeSetup.classList.add('active');
      if (adminLoginForm) adminLoginForm.style.display = 'none';
      if (adminSetupForm) adminSetupForm.style.display = 'block';
      if (authCardHeading) authCardHeading.textContent = 'Create Administrator Account';
      if (authCardSubheading) authCardSubheading.textContent = 'Initialize master administrator credentials for THC Command Center.';
    } else {
      if (btnModeSetup) btnModeSetup.classList.remove('active');
      if (btnModeSignIn) btnModeSignIn.classList.add('active');
      if (adminSetupForm) adminSetupForm.style.display = 'none';
      if (adminLoginForm) adminLoginForm.style.display = 'block';
      if (authCardHeading) authCardHeading.textContent = 'Administrator Sign In';
      if (authCardSubheading) authCardSubheading.textContent = 'Access the Thathvamasi Command Center to manage candidate pipelines, client requisitions, and analytics.';
    }
  }

  if (btnModeSignIn) btnModeSignIn.addEventListener('click', () => setAuthMode('signin'));
  if (btnModeSetup) btnModeSetup.addEventListener('click', () => setAuthMode('setup'));

  // 2. Check Initial Authentication State on Page Load
  async function checkInitialAuth() {
    if (Api.isAdminAuthenticated()) {
      const isValid = await Api.verifyAdminSession();
      if (isValid) {
        const user = Api.getAdminUser();
        renderAuthenticatedState(user);
        return;
      }
    }
    renderUnauthenticatedState();

    // Check if initial admin setup is required
    try {
      const status = await Api.checkSetupStatus();
      if (status && !status.has_admin) {
        setAuthMode('setup');
        showAlert('No administrator account found in the database. Please initialize your admin credentials below.', 'info');
      }
    } catch {
      // Offline or network error - defaults to sign-in
    }
  }

  // 3. Handle Login Form Submission
  if (adminLoginForm) {
    adminLoginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideAlert();

      const email = adminEmailInput ? adminEmailInput.value.trim() : '';
      const password = adminPasswordInput ? adminPasswordInput.value.trim() : '';

      if (!email || !password) {
        showAlert('Please enter both email and password.');
        return;
      }

      // Set loading state on button
      if (btnAdminSubmit) {
        btnAdminSubmit.disabled = true;
        btnAdminSubmit.innerHTML = `
          <svg class="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;">
            <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
            <path d="M4 12a8 8 0 018-8v8H4z" fill="currentColor"></path>
          </svg>
          <span>Authenticating...</span>
        `;
      }

      try {
        const result = await Api.adminLogin(email, password);

        if (result.success) {
          window.showToast?.('Authentication successful. Welcome to THC Command Center!', 'success');
          renderAuthenticatedState(result.user);
        } else {
          showAlert(result.error || 'Authentication failed. Please verify credentials.');
          window.showToast?.(result.error || 'Access denied', 'error');
        }
      } catch (err) {
        showAlert('An unexpected error occurred during authentication. Please retry.');
      } finally {
        if (btnAdminSubmit) {
          btnAdminSubmit.disabled = false;
          btnAdminSubmit.innerHTML = `
            <span>Sign In to Command Center</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          `;
        }
      }
    });
  }

  // 4. Handle Setup Admin Form Submission
  if (adminSetupForm) {
    adminSetupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideAlert();

      const fullName = adminSetupFullName ? adminSetupFullName.value.trim() : '';
      const email = adminSetupEmail ? adminSetupEmail.value.trim() : '';
      const password = adminSetupPassword ? adminSetupPassword.value.trim() : '';

      if (!fullName || !email || !password) {
        showAlert('Please fill in all setup fields.');
        return;
      }

      if (password.length < 6) {
        showAlert('Password must be at least 6 characters long.');
        return;
      }

      if (btnAdminSetupSubmit) {
        btnAdminSetupSubmit.disabled = true;
        btnAdminSetupSubmit.innerHTML = `
          <svg class="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;">
            <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
            <path d="M4 12a8 8 0 018-8v8H4z" fill="currentColor"></path>
          </svg>
          <span>Creating Administrator...</span>
        `;
      }

      try {
        const result = await Api.setupAdmin(fullName, email, password);

        if (result.success) {
          window.showToast?.('Administrator account created successfully! Accessing Command Center...', 'success');
          renderAuthenticatedState(result.user);
        } else {
          showAlert(result.error || 'Failed to create administrator account.');
          window.showToast?.(result.error || 'Setup failed', 'error');
        }
      } catch (err) {
        showAlert('An unexpected error occurred during setup. Please retry.');
      } finally {
        if (btnAdminSetupSubmit) {
          btnAdminSetupSubmit.disabled = false;
          btnAdminSetupSubmit.innerHTML = `
            <span>Create Administrator Account</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          `;
        }
      }
    });
  }

  // 5. Password Visibility Toggle
  if (btnTogglePassword && adminPasswordInput) {
    btnTogglePassword.addEventListener('click', () => {
      const isPassword = adminPasswordInput.type === 'password';
      adminPasswordInput.type = isPassword ? 'text' : 'password';
      if (pwdEyeOpen) pwdEyeOpen.style.display = isPassword ? 'none' : 'block';
      if (pwdEyeClosed) pwdEyeClosed.style.display = isPassword ? 'block' : 'none';
    });
  }

  // 6. Mobile Sidebar Drawer Controls
  function openMobileAdminSidebar() {
    if (adminSidebar) adminSidebar.classList.add('open');
    if (adminSidebarBackdrop) adminSidebarBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileAdminSidebar() {
    if (adminSidebar) adminSidebar.classList.remove('open');
    if (adminSidebarBackdrop) adminSidebarBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (adminMobileSidebarToggle) {
    adminMobileSidebarToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      if (adminSidebar && adminSidebar.classList.contains('open')) {
        closeMobileAdminSidebar();
      } else {
        openMobileAdminSidebar();
      }
    });
  }

  if (adminSidebarClose) {
    adminSidebarClose.addEventListener('click', closeMobileAdminSidebar);
  }

  if (adminSidebarBackdrop) {
    adminSidebarBackdrop.addEventListener('click', closeMobileAdminSidebar);
  }

  // Auto-close mobile sidebar when clicking a nav tab
  const navTabs = document.querySelectorAll('.admin-nav-item');
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      if (window.innerWidth <= 992) {
        closeMobileAdminSidebar();
      }
    });
  });

  // 7. Logout Action Listeners
  async function performLogout() {
    await Api.adminLogout();
    renderUnauthenticatedState();
    if (adminLoginForm) adminLoginForm.reset();
    if (adminSetupForm) adminSetupForm.reset();
    setAuthMode('signin');
    window.showToast?.('You have been logged out of the Command Center.', 'info');
  }

  if (btnHeaderLogout) btnHeaderLogout.addEventListener('click', performLogout);
  if (btnExitAdmin) btnExitAdmin.addEventListener('click', performLogout);

  // Run initial session verification
  await checkInitialAuth();
});
