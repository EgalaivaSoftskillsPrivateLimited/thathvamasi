/**
 * Thathvamasi HR Consultancy (THC) - Storage Service
 */

import { INITIAL_CANDIDATES, INITIAL_CLIENTS, INITIAL_BLOGS } from '../data/mockData.js';
import { exportToCSV } from './csvExporter.js';

const STORAGE_KEYS = {
  CANDIDATES: 'thc_candidates_v1',
  CLIENTS: 'thc_clients_v1',
  BLOGS: 'thc_blogs_v2',
  ENQUIRIES: 'thc_enquiries_v1'
};

class StorageService {
  constructor() {
    this.init();
  }

  init() {
    if (!localStorage.getItem(STORAGE_KEYS.CANDIDATES)) {
      localStorage.setItem(STORAGE_KEYS.CANDIDATES, JSON.stringify(INITIAL_CANDIDATES));
    }
    if (!localStorage.getItem(STORAGE_KEYS.CLIENTS)) {
      localStorage.setItem(STORAGE_KEYS.CLIENTS, JSON.stringify(INITIAL_CLIENTS));
    }
    const currentBlogs = localStorage.getItem(STORAGE_KEYS.BLOGS);
    if (!currentBlogs || JSON.parse(currentBlogs).length < 5) {
      localStorage.setItem(STORAGE_KEYS.BLOGS, JSON.stringify(INITIAL_BLOGS));
    }
    if (!localStorage.getItem(STORAGE_KEYS.ENQUIRIES)) {
      localStorage.setItem(STORAGE_KEYS.ENQUIRIES, JSON.stringify([]));
    }
  }

  getCandidates() {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.CANDIDATES);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error("Error reading candidates", e);
      return [];
    }
  }

  addCandidate(candidateData) {
    const list = this.getCandidates();
    const newCandidate = {
      id: `THC-CAN-${Math.floor(10000 + Math.random() * 90000)}`,
      status: 'new',
      appliedDate: new Date().toISOString().split('T')[0],
      ...candidateData
    };
    list.unshift(newCandidate);
    localStorage.setItem(STORAGE_KEYS.CANDIDATES, JSON.stringify(list));
    window.dispatchEvent(new CustomEvent('thc:data-changed', { detail: { type: 'candidates', item: newCandidate } }));
    return newCandidate;
  }

  updateCandidateStatus(id, newStatus) {
    const list = this.getCandidates();
    const index = list.findIndex(c => c.id === id);
    if (index !== -1) {
      list[index].status = newStatus;
      localStorage.setItem(STORAGE_KEYS.CANDIDATES, JSON.stringify(list));
      window.dispatchEvent(new CustomEvent('thc:data-changed', { detail: { type: 'candidates' } }));
      return list[index];
    }
    return null;
  }

  getClients() {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.CLIENTS);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error("Error reading clients", e);
      return [];
    }
  }

  addClient(clientData) {
    const list = this.getClients();
    const newClient = {
      id: `THC-REQ-${Math.floor(30000 + Math.random() * 70000)}`,
      status: 'open',
      submittedDate: new Date().toISOString().split('T')[0],
      ...clientData
    };
    list.unshift(newClient);
    localStorage.setItem(STORAGE_KEYS.CLIENTS, JSON.stringify(list));
    window.dispatchEvent(new CustomEvent('thc:data-changed', { detail: { type: 'clients', item: newClient } }));
    return newClient;
  }

  updateClientStatus(id, newStatus) {
    const list = this.getClients();
    const index = list.findIndex(c => c.id === id);
    if (index !== -1) {
      list[index].status = newStatus;
      localStorage.setItem(STORAGE_KEYS.CLIENTS, JSON.stringify(list));
      window.dispatchEvent(new CustomEvent('thc:data-changed', { detail: { type: 'clients' } }));
      return list[index];
    }
    return null;
  }

  getBlogs() {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.BLOGS);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error("Error reading blogs", e);
      return [];
    }
  }

  addBlog(blogData) {
    const list = this.getBlogs();
    const newBlog = {
      id: `blog-${Date.now()}`,
      slug: blogData.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, ''),
      date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      ...blogData
    };
    list.unshift(newBlog);
    localStorage.setItem(STORAGE_KEYS.BLOGS, JSON.stringify(list));
    window.dispatchEvent(new CustomEvent('thc:data-changed', { detail: { type: 'blogs', item: newBlog } }));
    return newBlog;
  }

  getEnquiries() {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.ENQUIRIES);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  }

  addEnquiry(enquiry) {
    const list = this.getEnquiries();
    const item = {
      id: `ENQ-${Date.now()}`,
      date: new Date().toISOString(),
      ...enquiry
    };
    list.unshift(item);
    localStorage.setItem(STORAGE_KEYS.ENQUIRIES, JSON.stringify(list));
    window.dispatchEvent(new CustomEvent('thc:data-changed', { detail: { type: 'enquiries', item } }));
    return item;
  }

  exportCandidatesCSV() {
    const candidates = this.getCandidates();
    if (!candidates.length) return false;

    const headers = [
      "ID", "Name", "Email", "Mobile", "Location", "Qualification",
      "Experience", "Current Company", "Designation", "Current CTC",
      "Expected CTC", "Notice Period", "Skills", "Status", "Applied Date"
    ];

    const rows = candidates.map(c => [
      c.id,
      c.name,
      c.email,
      c.mobile,
      c.currentLocation,
      c.qualification || '',
      c.experience || '',
      c.currentCompany || '',
      c.currentDesignation || '',
      c.currentCtc || '',
      c.expectedCtc || '',
      c.noticePeriod || '',
      Array.isArray(c.skills) ? c.skills.join(', ') : (c.skills || ''),
      c.status,
      c.appliedDate
    ]);

    return exportToCSV("THC_Candidates_Registry", headers, rows);
  }
}

export const Storage = new StorageService();
