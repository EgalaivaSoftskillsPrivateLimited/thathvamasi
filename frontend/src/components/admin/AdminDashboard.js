/**
 * Thathvamasi HR Consultancy (THC) - Admin Dashboard & Command Center Component
 */

import { Storage } from '../../lib/storage.js';
import { Api } from '../../lib/api.js';
import { openModal } from '../ui/Modal.js';
import { exportToCSV } from '../../lib/csvExporter.js';

export function initAdminDashboard() {
  const navItems = document.querySelectorAll('.admin-nav-item');
  const adminSections = document.querySelectorAll('.admin-tab-content');

  // Sub-tabs switcher
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetTab = item.getAttribute('data-tab');
      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');

      adminSections.forEach(sec => {
        sec.style.display = sec.id === `adminTab-${targetTab}` ? 'block' : 'none';
      });

      if (targetTab === 'candidates') renderCandidatesTable();
      if (targetTab === 'clients') renderClientsTable();
      if (targetTab === 'overview') updateKPIs();
      if (targetTab === 'enquiries') renderEnquiriesTable();
    });
  });

  const candidateSearch = document.getElementById('adminCandidateSearch');
  const candidateStatusFilter = document.getElementById('adminCandidateFilter');

  if (candidateSearch) {
    candidateSearch.addEventListener('input', () => renderCandidatesTable());
  }
  if (candidateStatusFilter) {
    candidateStatusFilter.addEventListener('change', () => renderCandidatesTable());
  }

  // Export to CSV
  const btnExportCSV = document.getElementById('btnExportCandidatesCSV');
  if (btnExportCSV) {
    btnExportCSV.addEventListener('click', () => {
      const candidatesToExport = (currentCandidatesList && currentCandidatesList.length > 0)
        ? currentCandidatesList
        : Storage.getCandidates();
      if (!candidatesToExport || candidatesToExport.length === 0) {
        window.showToast('No candidates available to export', 'error');
        return;
      }
      const headers = ['Ref ID', 'Candidate Name', 'Email', 'Mobile', 'Location', 'Experience', 'Designation', 'Company', 'Status', 'Applied Date'];
      const rows = candidatesToExport.map(c => [
        c.id,
        c.name,
        c.email,
        c.mobile,
        c.currentLocation,
        c.experience,
        c.currentDesignation || 'Professional',
        c.currentCompany || 'N/A',
        c.status,
        c.appliedDate
      ]);
      const success = exportToCSV('thc_candidates_live_database', headers, rows);
      if (success) {
        window.showToast('Candidate database exported successfully as CSV', 'success');
      } else {
        window.showToast('Failed to export candidate records', 'error');
      }
    });
  }

  // Add Blog Form
  const newBlogForm = document.getElementById('adminNewBlogForm');
  if (newBlogForm) {
    newBlogForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = newBlogForm.elements['blogTitle']?.value.trim();
      const category = newBlogForm.elements['blogCategory']?.value;
      const readTime = newBlogForm.elements['blogReadTime']?.value.trim() || '4 min read';
      const author = newBlogForm.elements['blogAuthor']?.value.trim() || 'THC Advisory Desk';
      const excerpt = newBlogForm.elements['blogExcerpt']?.value.trim();
      const content = newBlogForm.elements['blogContent']?.value.trim();

      if (!title || !excerpt || !content) {
        window.showToast('Please fill out all required blog fields', 'error');
        return;
      }

      await Api.createBlog({
        title,
        category,
        readTime,
        author,
        excerpt,
        content: `<div><p class="lead">${excerpt}</p><hr style="margin: 20px 0; border: none; border-top: 1px solid var(--glass-border);">${content}</div>`,
        image: '/images/team/thc_leadership.jpg'
      });

      window.showToast('New HR insight published successfully!', 'success');
      newBlogForm.reset();
    });
  }

  async function updateKPIs() {
    const candidates = await Api.getCandidates();
    const clients = await Api.getClients();
    const enquiries = await Api.getEnquiries();

    const totalCandEl = document.getElementById('kpiTotalCandidates');
    const totalReqEl = document.getElementById('kpiTotalRequisitions');
    const shortlistedEl = document.getElementById('kpiShortlisted');
    const totalEnqEl = document.getElementById('kpiTotalEnquiries');

    const badgeCandCount = document.getElementById('sidebarCandCount');
    const badgeReqCount = document.getElementById('sidebarReqCount');
    const badgeEnqCount = document.getElementById('sidebarEnqCount');

    if (totalCandEl) totalCandEl.textContent = candidates.length;
    if (totalReqEl) totalReqEl.textContent = clients.length;
    if (shortlistedEl) {
      const shortlisted = candidates.filter(c => c.status === 'shortlisted').length;
      shortlistedEl.textContent = shortlisted;
    }
    if (totalEnqEl) totalEnqEl.textContent = enquiries.length;

    if (badgeCandCount) badgeCandCount.textContent = candidates.length;
    if (badgeReqCount) badgeReqCount.textContent = clients.length;
    if (badgeEnqCount) badgeEnqCount.textContent = enquiries.length;
  }

  let currentCandidatesList = [];
  let currentClientsList = [];

  async function renderCandidatesTable() {
    const tbody = document.getElementById('adminCandidatesTableBody');
    if (!tbody) return;

    const searchTerm = candidateSearch?.value.toLowerCase().trim() || '';
    const statusFilter = candidateStatusFilter?.value || 'all';

    const candidates = await Api.getCandidates();
    currentCandidatesList = candidates;
    const filtered = candidates.filter(c => {
      const matchesStatus = statusFilter === 'all' || c.status === statusFilter;
      const matchesSearch = !searchTerm || 
        c.name.toLowerCase().includes(searchTerm) ||
        c.email.toLowerCase().includes(searchTerm) ||
        c.id.toLowerCase().includes(searchTerm) ||
        (Array.isArray(c.skills) && c.skills.some(s => s.toLowerCase().includes(searchTerm))) ||
        (c.currentCompany && c.currentCompany.toLowerCase().includes(searchTerm));
      return matchesStatus && matchesSearch;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 36px; color: var(--text-muted);">No candidate records found.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtered.map(c => `
      <tr>
        <td>
          <span style="font-family: monospace; font-size: 0.8rem; color: var(--color-accent-gold-light);">${c.id}</span>
          ${c.isLive ? '<span style="display: block; font-size: 0.65rem; color: #00c9a7; font-weight: 600;">LIVE DB</span>' : ''}
        </td>
        <td>
          <span class="table-candidate-name">${c.name}</span>
          <span class="table-candidate-email">${c.email} • ${c.mobile}</span>
        </td>
        <td>
          <span style="font-size: 0.84rem; color: var(--text-heading); font-weight: 500;">${c.currentDesignation || 'Professional'}</span>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${c.currentCompany || 'N/A'} • ${c.experience || ''}</div>
        </td>
        <td>
          <span style="font-size: 0.85rem; color: var(--text-secondary);">${c.currentLocation}</span>
        </td>
        <td>
          <select class="table-select candidate-status-selector" data-id="${c.id}" data-raw-id="${c.rawId || c.id}">
            <option value="new" ${c.status === 'new' ? 'selected' : ''}>New</option>
            <option value="contacted" ${c.status === 'contacted' ? 'selected' : ''}>Contacted</option>
            <option value="shortlisted" ${c.status === 'shortlisted' ? 'selected' : ''}>Shortlisted</option>
            <option value="rejected" ${c.status === 'rejected' ? 'selected' : ''}>Rejected</option>
          </select>
        </td>
        <td>
          <span style="font-size: 0.78rem; color: var(--text-muted);">${c.appliedDate}</span>
        </td>
        <td>
          <div class="table-actions">
            <button class="table-btn btn-view-candidate" data-id="${c.id}" title="View Full Profile">
              View Profile
            </button>
          </div>
        </td>
      </tr>
    `).join('');

    tbody.querySelectorAll('.candidate-status-selector').forEach(sel => {
      sel.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        const rawId = e.target.getAttribute('data-raw-id') || id;
        const newStatus = e.target.value;
        const res = await Api.updateCandidateStatus(rawId, newStatus);
        if (res.source === 'backend') {
          window.showToast(`Candidate status updated to "${newStatus}" in live database`, 'success');
        } else {
          window.showToast(`Candidate ${id} updated to ${newStatus}`, 'info');
        }
        updateKPIs();
      });
    });

    tbody.querySelectorAll('.btn-view-candidate').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openCandidateDetailModal(id);
      });
    });
  }

  async function renderClientsTable() {
    const tbody = document.getElementById('adminClientsTableBody');
    if (!tbody) return;

    const clients = await Api.getClients();
    currentClientsList = clients;

    const badgeReqCount = document.getElementById('sidebarReqCount');
    if (badgeReqCount) badgeReqCount.textContent = clients.length;

    if (clients.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 36px; color: var(--text-muted);">No employer requisitions logged.</td></tr>`;
      return;
    }

    tbody.innerHTML = clients.map(client => `
      <tr>
        <td>
          <span style="font-family: monospace; font-size: 0.8rem; color: var(--color-teal-500);">${client.id ? (client.id.length > 12 ? 'REQ-' + client.id.slice(0, 6).toUpperCase() : client.id) : 'REQ'}</span>
          ${client.isLive ? '<span style="display: block; font-size: 0.65rem; color: #00c9a7; font-weight: 600;">LIVE DB</span>' : ''}
        </td>
        <td>
          <span style="font-weight: 600; color: var(--text-heading); display: block;">${client.companyName}</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${client.industry || ''} • ${client.location}</span>
        </td>
        <td>
          <span style="font-weight: 500; color: var(--color-accent-gold-light);">${client.position}</span>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${client.vacancies} Openings • ${client.salaryRange || 'Open'}</div>
        </td>
        <td>
          <span style="font-size: 0.84rem; color: var(--text-heading); font-weight: 500;">${client.contactPerson}</span>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${client.email}</div>
        </td>
        <td>
          <select class="table-select client-status-selector" data-id="${client.id}">
            <option value="new" ${client.status === 'new' ? 'selected' : ''}>New</option>
            <option value="open" ${client.status === 'open' ? 'selected' : ''}>Open</option>
            <option value="sourcing" ${client.status === 'sourcing' ? 'selected' : ''}>Sourcing</option>
            <option value="shortlist_sent" ${client.status === 'shortlist_sent' ? 'selected' : ''}>Shortlist Sent</option>
            <option value="closed" ${client.status === 'closed' ? 'selected' : ''}>Closed</option>
          </select>
        </td>
        <td>
          <span style="font-size: 0.78rem; color: var(--text-muted);">${client.submittedDate}</span>
        </td>
        <td>
          <button class="table-btn btn-view-jd" data-id="${client.id}">View JD</button>
        </td>
      </tr>
    `).join('');

    tbody.querySelectorAll('.client-status-selector').forEach(sel => {
      sel.addEventListener('change', async (e) => {
        const id = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        const res = await Api.updateClientStatus(id, newStatus);
        if (res.source === 'backend') {
          window.showToast(`Requisition status updated to "${newStatus}" in live database`, 'success');
        } else {
          window.showToast(`Requisition ${id} updated to ${newStatus}`, 'info');
        }
        updateKPIs();
      });
    });

    tbody.querySelectorAll('.btn-view-jd').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openJdModal(id);
      });
    });
  }

  async function renderEnquiriesTable() {
    const tbody = document.getElementById('adminEnquiriesTableBody');
    if (!tbody) return;

    const enquiries = await Api.getEnquiries();

    // Immediately update sidebar badge and overview counter
    const badgeEnqCount = document.getElementById('sidebarEnqCount');
    if (badgeEnqCount) badgeEnqCount.textContent = enquiries.length;
    const totalEnqEl = document.getElementById('kpiTotalEnquiries');
    if (totalEnqEl) totalEnqEl.textContent = enquiries.length;

    if (enquiries.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; padding: 36px; color: var(--text-muted);">No general inquiries received yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = enquiries.map(enq => `
      <tr>
        <td>
          <span style="font-weight: 600; color: var(--text-heading); display: block;">${enq.name || 'Website Visitor'}</span>
          ${enq.isLive ? '<span style="display: block; font-size: 0.65rem; color: #00c9a7; font-weight: 600;">LIVE DB</span>' : ''}
        </td>
        <td>
          <span style="font-size: 0.84rem; color: var(--color-primary); font-weight: 600; display: block;">${enq.email || 'No email provided'}</span>
          ${enq.mobile && enq.mobile !== 'Not Provided' ? `<div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 2px;">${enq.mobile}</div>` : ''}
        </td>
        <td><span class="status-pill open" style="text-transform: none; font-size: 0.78rem;">${enq.subject || 'Consultation Query'}</span></td>
        <td><span style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4;">${enq.message || ''}</span></td>
        <td><span style="font-size: 0.78rem; color: var(--text-muted);">${enq.date || new Date().toLocaleDateString()}</span></td>
      </tr>
    `).join('');
  }

  function openCandidateDetailModal(candidateId) {
    const candidate = currentCandidatesList.find(c => c.id === candidateId) || Storage.getCandidates().find(c => c.id === candidateId);
    if (!candidate) return;

    const content = document.getElementById('applicantDetailBody');
    if (content) {
      content.innerHTML = `
        <div class="applicant-profile-card">
          <div class="applicant-hero">
            <div>
              <h3 style="margin-bottom: 4px;">${candidate.name}</h3>
              <p style="margin-bottom: 0; color: var(--color-accent-gold-light); font-size: 0.95rem;">
                ${candidate.currentDesignation || 'Candidate'} @ ${candidate.currentCompany || 'Confidential'}
              </p>
            </div>
            <div style="text-align: right;">
              <span class="status-pill ${candidate.status}">${candidate.status}</span>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;">Ref: ${candidate.id}</div>
            </div>
          </div>

          <div class="detail-grid">
            <div class="detail-box">
              <div class="detail-box-label">Email Address</div>
              <div class="detail-box-val">${candidate.email}</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Mobile & WhatsApp</div>
              <div class="detail-box-val">${candidate.mobile}</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Current & Preferred City</div>
              <div class="detail-box-val">${candidate.currentLocation} &rarr; ${candidate.preferredLocation || 'Open'}</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Education / Qualification</div>
              <div class="detail-box-val">${candidate.qualification || 'Degree Holder'}</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Experience & Notice Period</div>
              <div class="detail-box-val">${candidate.experience} • Notice: ${candidate.noticePeriod}</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Current & Expected CTC</div>
              <div class="detail-box-val">${candidate.currentCtc} / Exp: ${candidate.expectedCtc}</div>
            </div>
          </div>

          <div class="detail-box">
            <div class="detail-box-label">Key Core Competencies & Skills</div>
            <div class="skills-tags-wrap">
              ${(Array.isArray(candidate.skills) ? candidate.skills : [candidate.skills]).map(s => `<span class="skill-tag">${s}</span>`).join('')}
            </div>
          </div>

          ${candidate.resumeUrl ? `
          <div class="detail-box" style="background: rgba(0, 168, 150, 0.08); border-color: var(--glass-border-teal);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
              <div>
                <div class="detail-box-label" style="color: var(--color-teal-500);">Attached Resume Document</div>
                <div style="font-weight: 600; color: var(--text-heading); font-size: 0.95rem;">${candidate.resumeFileName || 'Candidate_Resume.pdf'}</div>
                <div style="font-size: 0.78rem; color: var(--text-muted);">${candidate.resumeFileSize || 'Verified Document'} • Database Storage</div>
              </div>
              <a href="${candidate.resumeUrl}" target="_blank" rel="noopener noreferrer" download="${candidate.resumeFileName || 'candidate_resume'}" class="btn btn-teal btn-sm" style="display: inline-flex; align-items: center; gap: 6px; text-decoration: none;">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                <span>Download Resume</span>
              </a>
            </div>
          </div>
          ` : `
          <div class="detail-box" style="background: rgba(255, 255, 255, 0.03);">
            <div class="detail-box-label">Resume Document</div>
            <div style="font-size: 0.85rem; color: var(--text-muted); font-style: italic;">No resume document was attached during submission.</div>
          </div>
          `}
        </div>
      `;
    }

    openModal('applicantDetailModal');
  }

  function openJdModal(clientId) {
    const client = currentClientsList.find(c => c.id === clientId) || Storage.getClients().find(c => c.id === clientId);
    if (!client) return;

    const content = document.getElementById('applicantDetailBody');
    if (content) {
      content.innerHTML = `
        <div class="applicant-profile-card">
          <div class="applicant-hero">
            <div>
              <h3>${client.position}</h3>
              <p style="color: var(--color-teal-500); margin-bottom: 0;">${client.companyName} • ${client.location}</p>
            </div>
            <div style="text-align: right;">
              <span class="status-pill open">${client.status}</span>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 6px;">Ref: ${client.id}</div>
            </div>
          </div>

          <div class="detail-grid">
            <div class="detail-box">
              <div class="detail-box-label">Contact Person</div>
              <div class="detail-box-val">${client.contactPerson} (${client.designation || 'Lead'})</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Official Email</div>
              <div class="detail-box-val">${client.email}</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Vacancies & Timeline</div>
              <div class="detail-box-val">${client.vacancies} Positions • ${client.timeline}</div>
            </div>
            <div class="detail-box">
              <div class="detail-box-label">Salary Band</div>
              <div class="detail-box-val">${client.salaryRange}</div>
            </div>
          </div>

          <div class="detail-box">
            <div class="detail-box-label">Job Description & Hiring Requirements</div>
            <p style="margin-top: 8px; font-size: 0.92rem; color: var(--text-secondary); line-height: 1.6;">${client.jdSummary}</p>
          </div>
        </div>
      `;
    }

    openModal('applicantDetailModal');
  }

  window.addEventListener('thc:data-changed', () => {
    updateKPIs();
    renderCandidatesTable();
    renderClientsTable();
    renderEnquiriesTable();
  });

  updateKPIs();
  renderCandidatesTable();
  renderClientsTable();
  renderEnquiriesTable();
}
