/**
 * Thathvamasi HR Consultancy (THC) - API Integration Service
 * Connects frontend forms and dashboards to FastAPI PostgreSQL backend
 * with graceful fallback to local storage for guaranteed offline/dev resilience.
 */

import { Storage } from './storage.js';

function resolveApiBase() {
  const envVal = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_ENDPOINT)
    ? String(import.meta.env.VITE_API_ENDPOINT).trim().replace(/\/+$/, '')
    : '/api';
  
  if (!envVal || envVal === '/') return '/api';
  if (envVal.startsWith('http') && !envVal.endsWith('/api')) {
    return `${envVal}/api`;
  }
  return envVal;
}

const API_BASE = resolveApiBase();

class ApiService {
  /**
   * Check if backend is alive
   */
  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`, { method: 'GET' });
      return res.ok;
    } catch {
      return false;
    }
  }

  /**
   * Submit candidate registration with resume upload
   */
  async submitCandidate(candidatePayload, resumeFile = null) {
    try {
      const formData = new FormData();

      if (resumeFile) {
        formData.append('resume_file', resumeFile);
      }

      // Append standard candidate fields
      formData.append('candidate_name', candidatePayload.name || '');
      formData.append('candidate_email', candidatePayload.email || '');
      formData.append('candidate_mobile', candidatePayload.mobile || '');
      formData.append('candidate_whatsapp', candidatePayload.whatsapp || candidatePayload.mobile || '');
      formData.append('candidate_location', candidatePayload.currentLocation || 'Coimbatore');
      formData.append('candidate_pref_location', candidatePayload.preferredLocation || 'Coimbatore');
      formData.append('candidate_qualification', candidatePayload.qualification || 'Graduate');
      formData.append('candidate_experience', candidatePayload.experience || '1 - 3 Years');
      formData.append('candidate_company', candidatePayload.currentCompany || 'Confidential');
      formData.append('candidate_designation', candidatePayload.currentDesignation || 'Professional');
      formData.append('candidate_ctc', candidatePayload.currentCtc || 'Not Disclosed');
      formData.append('candidate_exp_ctc', candidatePayload.expectedCtc || 'Negotiable');
      formData.append('candidate_notice', candidatePayload.noticePeriod || 'Immediate');
      formData.append('candidate_skills', Array.isArray(candidatePayload.skills) ? candidatePayload.skills.join(', ') : (candidatePayload.skills || ''));

      const response = await fetch(`${API_BASE}/candidates/submit-form`, {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        // Also save to local storage cache for offline viewing
        const savedItem = Storage.addCandidate({
          ...candidatePayload,
          id: result.data?.id || `THC-CAN-${Date.now().toString().slice(-5)}`,
          synced: true
        });
        return {
          success: true,
          id: result.data?.id || savedItem.id,
          name: result.data?.name || candidatePayload.name,
          source: 'backend'
        };
      } else {
        const errorText = await response.text();
        console.warn('Backend rejected candidate submission, falling back to local storage:', errorText);
      }
    } catch (err) {
      console.warn('Backend unreachable for candidate registration, using local storage fallback:', err);
    }

    // Graceful offline fallback
    const localSaved = Storage.addCandidate(candidatePayload);
    return {
      success: true,
      id: localSaved.id,
      name: localSaved.name,
      source: 'local'
    };
  }

  /**
   * Submit client hiring requisition
   */
  async submitClientRequisition(clientPayload) {
    try {
      const response = await fetch(`${API_BASE}/clients/requisition`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: clientPayload.companyName,
          contact_person: clientPayload.contactPerson,
          designation: clientPayload.designation || 'Hiring Lead',
          email: clientPayload.email,
          mobile: clientPayload.mobile || 'Not Provided',
          location: clientPayload.location || 'Coimbatore',
          industry: clientPayload.industry || 'Corporate Enterprise',
          position: clientPayload.position,
          vacancies: parseInt(clientPayload.vacancies, 10) || 1,
          experience: clientPayload.experience || '3 - 6 Years',
          salary_range: clientPayload.salaryRange || 'Best in Industry',
          employment_type: clientPayload.employmentType || 'permanent',
          timeline: clientPayload.timeline || 'Within 30 Days',
          jd_summary: clientPayload.jdSummary || ''
        })
      });

      if (response.ok) {
        const result = await response.json();
        const savedItem = Storage.addClient({
          ...clientPayload,
          id: result.data?.id || `THC-REQ-${Date.now().toString().slice(-5)}`,
          synced: true
        });
        return {
          success: true,
          id: result.data?.id || savedItem.id,
          companyName: clientPayload.companyName,
          position: clientPayload.position,
          vacancies: clientPayload.vacancies,
          source: 'backend'
        };
      } else {
        const errorText = await response.text();
        console.warn('Backend rejected requisition, falling back to local storage:', errorText);
      }
    } catch (err) {
      console.warn('Backend unreachable for requisition, using local storage fallback:', err);
    }

    // Graceful offline fallback
    const localSaved = Storage.addClient(clientPayload);
    return {
      success: true,
      id: localSaved.id,
      companyName: localSaved.companyName,
      position: localSaved.position,
      vacancies: localSaved.vacancies,
      source: 'local'
    };
  }

  /**
   * Submit contact form enquiry
   */
  async submitContactEnquiry(enquiryPayload) {
    try {
      const response = await fetch(`${API_BASE}/contact/enquiry`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: enquiryPayload.name,
          email: enquiryPayload.email,
          mobile: enquiryPayload.mobile || '',
          subject: enquiryPayload.subject || 'General Recruitment Query',
          message: enquiryPayload.message
        })
      });

      if (response.ok) {
        Storage.addEnquiry({ ...enquiryPayload, synced: true });
        return { success: true, source: 'backend' };
      }
    } catch (err) {
      console.warn('Backend unreachable for enquiry, using local storage fallback:', err);
    }

    Storage.addEnquiry(enquiryPayload);
    return { success: true, source: 'local' };
  }

  /**
   * Helper to get authentication headers
   */
  getAuthHeaders() {
    const token = this.getAdminToken();
    return {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
  }

  /**
   * Get candidates for Admin Command Center
   */
  async getCandidates() {
    try {
      const token = this.getAdminToken();
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const response = await fetch(`${API_BASE}/candidates/?size=100`, { method: 'GET', headers });
      if (response.ok) {
        const result = await response.json();
        if (result && Array.isArray(result.items)) {
          return result.items.map(item => {
            const primaryResume = (item.resumes && item.resumes.length > 0) ? item.resumes[0] : null;
            return {
              id: `THC-CAN-${item.id.slice(0, 6).toUpperCase()}`,
              rawId: item.id,
              name: item.personal_details?.full_name || 'Candidate',
              email: item.personal_details?.email || '',
              mobile: item.personal_details?.mobile || '',
              whatsapp: item.personal_details?.whatsapp || item.personal_details?.mobile || '',
              currentLocation: item.personal_details?.current_location || 'Coimbatore',
              preferredLocation: item.personal_details?.preferred_location || item.personal_details?.current_location || 'Coimbatore',
              qualification: item.professional_details?.highest_qualification || 'Graduate',
              experience: item.professional_details?.total_experience || '1-3 Years',
              currentCompany: item.professional_details?.current_company || 'Confidential',
              currentDesignation: item.professional_details?.current_designation || 'Professional',
              currentCtc: item.professional_details?.current_salary ? `${item.professional_details.current_salary} LPA` : 'Not Disclosed',
              expectedCtc: item.professional_details?.expected_salary ? `${item.professional_details.expected_salary} LPA` : 'Negotiable',
              noticePeriod: item.professional_details?.notice_period || 'Immediate',
              skills: item.professional_details?.skills || ['General'],
              status: item.status || 'new',
              appliedDate: item.created_at ? item.created_at.split('T')[0] : new Date().toISOString().split('T')[0],
              resumeUrl: primaryResume?.file_url || null,
              resumeFileName: primaryResume?.file_name || null,
              resumeFileSize: primaryResume?.file_size ? `${(primaryResume.file_size / (1024 * 1024)).toFixed(1)} MB` : null,
              isLive: true
            };
          });
        }
      }
    } catch (err) {
      console.warn('Unable to fetch live candidates, serving local registry:', err);
    }

    return Storage.getCandidates();
  }

  /**
   * Update Candidate Status in Live PostgreSQL Database
   */
  async updateCandidateStatus(candidateId, status) {
    try {
      const response = await fetch(`${API_BASE}/candidates/${candidateId}`, {
        method: 'PUT',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ status })
      });
      if (response.ok) {
        Storage.updateCandidateStatus(candidateId, status);
        return { success: true, source: 'backend' };
      }
    } catch (err) {
      console.warn('Backend unreachable for candidate status update:', err);
    }

    Storage.updateCandidateStatus(candidateId, status);
    return { success: true, source: 'local' };
  }

  /**
   * Get clients for Admin Command Center
   */
  async getClients() {
    try {
      const token = this.getAdminToken();
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const response = await fetch(`${API_BASE}/clients/`, { method: 'GET', headers });
      if (response.ok) {
        const result = await response.json();
        if (result && Array.isArray(result.data)) {
          return result.data.map(item => ({
            ...item,
            isLive: true
          }));
        }
      }
    } catch (err) {
      console.warn('Unable to fetch live clients, serving local cache:', err);
    }

    return Storage.getClients();
  }

  /**
   * Update Client / Requisition Status in Live PostgreSQL Database
   */
  async updateClientStatus(clientId, status) {
    try {
      const response = await fetch(`${API_BASE}/clients/${clientId}/status`, {
        method: 'PATCH',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ status })
      });
      if (response.ok) {
        Storage.updateClientStatus(clientId, status);
        return { success: true, source: 'backend' };
      }
    } catch (err) {
      console.warn('Backend unreachable for client status update:', err);
    }

    Storage.updateClientStatus(clientId, status);
    return { success: true, source: 'local' };
  }

  /**
   * Get enquiries for Admin Command Center
   */
  async getEnquiries() {
    try {
      const token = this.getAdminToken();
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
      const response = await fetch(`${API_BASE}/contact/enquiries`, { method: 'GET', headers });
      if (response.ok) {
        const result = await response.json();
        if (result && Array.isArray(result.data)) {
          return result.data.map(item => ({
            ...item,
            isLive: true
          }));
        }
      }
    } catch (err) {
      console.warn('Unable to fetch live enquiries, serving local cache:', err);
    }

    return Storage.getEnquiries();
  }

  /**
   * Publish new blog post
   */
  async createBlog(blogPayload) {
    try {
      const response = await fetch(`${API_BASE}/blogs/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(blogPayload)
      });
      if (response.ok) {
        Storage.addBlog({ ...blogPayload, synced: true });
        return { success: true, source: 'backend' };
      }
    } catch (err) {
      console.warn('Backend unreachable for publishing blog:', err);
    }

    Storage.addBlog(blogPayload);
    return { success: true, source: 'local' };
  }

  /**
   * Admin Authentication - Login
   */
  async adminLogin(email, password) {
    const cleanEmail = (email || '').trim().toLowerCase();
    const cleanPass = (password || '').trim();

    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: cleanEmail, password: cleanPass })
      });

      if (response.ok) {
        const data = await response.json();
        const token = data.access_token;
        const user = data.user || {
          email: cleanEmail,
          full_name: 'THC Administrator',
          role: 'admin'
        };

        localStorage.setItem('thc_admin_token', token);
        localStorage.setItem('thc_admin_user', JSON.stringify(user));

        return { success: true, token, user, source: 'backend' };
      }

      if (response.status === 401 || response.status === 403) {
        const errorData = await response.json().catch(() => ({}));
        return {
          success: false,
          error: errorData.detail || 'Invalid email or password. Access denied.'
        };
      }

      return {
        success: false,
        error: 'Authentication failed. Please verify your credentials.'
      };
    } catch (err) {
      console.error('Authentication service unreachable:', err);
      return {
        success: false,
        error: 'Unable to connect to authentication server. Please check your network or server status.'
      };
    }
  }

  /**
   * Get currently stored admin token
   */
  getAdminToken() {
    return localStorage.getItem('thc_admin_token');
  }

  /**
   * Get currently stored admin user profile
   */
  getAdminUser() {
    try {
      const raw = localStorage.getItem('thc_admin_user');
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  /**
   * Check if an admin token exists
   */
  isAdminAuthenticated() {
    return Boolean(this.getAdminToken());
  }

  /**
   * Admin Authentication - Logout
   */
  async adminLogout() {
    const token = this.getAdminToken();
    localStorage.removeItem('thc_admin_token');
    localStorage.removeItem('thc_admin_user');

    if (token && !token.startsWith('thc-local-jwt-')) {
      try {
        await fetch(`${API_BASE}/auth/logout`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
      } catch (err) {
        // Ignore network errors on logout
      }
    }

    return { success: true };
  }

  /**
   * Verify if current session is still valid
   */
  async verifyAdminSession() {
    const token = this.getAdminToken();
    if (!token) return false;

    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const user = await response.json();
        localStorage.setItem('thc_admin_user', JSON.stringify(user));
        return true;
      }

      await this.adminLogout();
      return false;
    } catch {
      return false;
    }
  }
}

export const Api = new ApiService();
