/**
 * Thathvamasi HR Consultancy (THC) - Admin Dashboard & Command Center Component
 */

import { Storage } from '../../lib/storage.js';
import { openModal } from '../ui/Modal.js';

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
      const success = Storage.exportCandidatesCSV();
      if (success) {
        window.showToast('Candidate database exported successfully as CSV', 'success');
      } else {
        window.showToast('No candidates available to export', 'error');
      }
    });
  }

  // Add Blog Form
  const newBlogForm = document.getElementById('adminNewBlogForm');
  if (newBlogForm) {
    newBlogForm.addEventListener('submit', (e) => {
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

      Storage.addBlog({
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

  function updateKPIs() {
    const candidates = Storage.getCandidates();
    const clients = Storage.getClients();
    const enquiries = Storage.getEnquiries();

    const totalCandEl = document.getElementById('kpiTotalCandidates');
    const totalReqEl = document.getElementById('kpiTotalRequisitions');
    const shortlistedEl = document.getElementById('kpiShortlisted');
    const totalEnqEl = document.getElementById('kpiTotalEnquiries');

    const badgeCandCount = document.getElementById('sidebarCandCount');
    const badgeReqCount = document.getElementById('sidebarReqCount');

    if (totalCandEl) totalCandEl.textContent = candidates.length;
    if (totalReqEl) totalReqEl.textContent = clients.length;
    if (shortlistedEl) {
      const shortlisted = candidates.filter(c => c.status === 'shortlisted').length;
      shortlistedEl.textContent = shortlisted;
    }
    if (totalEnqEl) totalEnqEl.textContent = enquiries.length;

    if (badgeCandCount) badgeCandCount.textContent = candidates.length;
    if (badgeReqCount) badgeReqCount.textContent = clients.length;
  }

  function renderCandidatesTable() {
    const tbody = document.getElementById('adminCandidatesTableBody');
    if (!tbody) return;

    const searchTerm = candidateSearch?.value.toLowerCase().trim() || '';
    const statusFilter = candidateStatusFilter?.value || 'all';

    const candidates = Storage.getCandidates();
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
        </td>
        <td>
          <span class="table-candidate-name">${c.name}</span>
          <span class="table-candidate-email">${c.email} • ${c.mobile}</span>
        </td>
        <td>
          <span style="font-size: 0.84rem; color: #FFFFFF;">${c.currentDesignation || 'Professional'}</span>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${c.currentCompany || 'N/A'} • ${c.experience || ''}</div>
        </td>
        <td>
          <span style="font-size: 0.85rem; color: #E2E8F0;">${c.currentLocation}</span>
        </td>
        <td>
          <select class="table-select candidate-status-selector" data-id="${c.id}">
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
      sel.addEventListener('change', (e) => {
        const id = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        Storage.updateCandidateStatus(id, newStatus);
        window.showToast(`Candidate ${id} updated to ${newStatus}`, 'info');
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

  function renderClientsTable() {
    const tbody = document.getElementById('adminClientsTableBody');
    if (!tbody) return;

    const clients = Storage.getClients();
    if (clients.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 36px; color: var(--text-muted);">No employer requisitions logged.</td></tr>`;
      return;
    }

    tbody.innerHTML = clients.map(client => `
      <tr>
        <td>
          <span style="font-family: monospace; font-size: 0.8rem; color: var(--color-teal-500);">${client.id}</span>
        </td>
        <td>
          <span style="font-weight: 600; color: #FFFFFF; display: block;">${client.companyName}</span>
          <span style="font-size: 0.75rem; color: var(--text-muted);">${client.industry || ''} • ${client.location}</span>
        </td>
        <td>
          <span style="font-weight: 500; color: var(--color-accent-gold-light);">${client.position}</span>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${client.vacancies} Openings • ${client.salaryRange || 'Open'}</div>
        </td>
        <td>
          <span style="font-size: 0.84rem; color: #FFFFFF;">${client.contactPerson}</span>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${client.email}</div>
        </td>
        <td>
          <select class="table-select client-status-selector" data-id="${client.id}">
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
      sel.addEventListener('change', (e) => {
        const id = e.target.getAttribute('data-id');
        const newStatus = e.target.value;
        Storage.updateClientStatus(id, newStatus);
        window.showToast(`Requisition ${id} updated to ${newStatus}`, 'info');
      });
    });

    tbody.querySelectorAll('.btn-view-jd').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openJdModal(id);
      });
    });
  }

  function renderEnquiriesTable() {
    const tbody = document.getElementById('adminEnquiriesTableBody');
    if (!tbody) return;

    const enquiries = Storage.getEnquiries();
    if (enquiries.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; padding: 36px; color: var(--text-muted);">No general inquiries received yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = enquiries.map(enq => `
      <tr>
        <td><span style="font-weight: 600; color: #FFFFFF;">${enq.name}</span></td>
        <td><span style="font-size: 0.84rem; color: var(--text-secondary);">${enq.email}<br><small>${enq.mobile}</small></span></td>
        <td><span class="status-pill open">${enq.subject}</span></td>
        <td><span style="font-size: 0.84rem; color: var(--text-muted);">${enq.message}</span></td>
        <td><span style="font-size: 0.75rem; color: var(--text-muted);">${new Date(enq.date).toLocaleDateString()}</span></td>
      </tr>
    `).join('');
  }

  function openCandidateDetailModal(candidateId) {
    const candidate = Storage.getCandidates().find(c => c.id === candidateId);
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

          <div class="detail-box" style="background: rgba(0, 168, 150, 0.08); border-color: var(--glass-border-teal);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div class="detail-box-label" style="color: var(--color-teal-500);">Attached Resume Document</div>
                <div style="font-weight: 600; color: #FFFFFF; font-size: 0.95rem;">${candidate.resumeFileName || 'Resume.pdf'}</div>
                <div style="font-size: 0.78rem; color: var(--text-muted);">${candidate.resumeFileSize || '2.0 MB'} • Verified Document</div>
              </div>
              <button class="btn btn-teal btn-sm" onclick="window.showToast('Simulating resume download for ${candidate.name}...', 'info')">
                Download Resume
              </button>
            </div>
          </div>
        </div>
      `;
    }

    openModal('applicantDetailModal');
  }

  function openJdModal(clientId) {
    const client = Storage.getClients().find(c => c.id === clientId);
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
            <p style="margin-top: 8px; font-size: 0.92rem; color: #E2E8F0; line-height: 1.6;">${client.jdSummary}</p>
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
  });

  updateKPIs();
  renderCandidatesTable();
  renderClientsTable();
}
