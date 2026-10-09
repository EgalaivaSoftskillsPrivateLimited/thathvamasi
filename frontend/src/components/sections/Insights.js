/**
 * Thathvamasi HR Consultancy (THC) - Insights & Blog Section Component
 */

import { Storage } from '../../lib/storage.js';
import { openModal } from '../ui/Modal.js';

export function initInsightsSection() {
  const container = document.getElementById('blogsGrid');
  const searchInput = document.getElementById('blogSearchInput');
  const filterBtns = document.querySelectorAll('.blog-filter-btn');

  let activeCategory = 'all';
  let searchTerm = '';

  function renderBlogs() {
    if (!container) return;

    const blogs = Storage.getBlogs();
    const filtered = blogs.filter(blog => {
      const catLower = activeCategory.toLowerCase();
      const matchesCategory = activeCategory === 'all' || 
        blog.category.toLowerCase().includes(catLower) ||
        (blog.region && blog.region.toLowerCase().includes(catLower)) ||
        blog.title.toLowerCase().includes(catLower);

      const matchesSearch = !searchTerm || 
        blog.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
        blog.excerpt.toLowerCase().includes(searchTerm.toLowerCase()) ||
        blog.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (blog.region && blog.region.toLowerCase().includes(searchTerm.toLowerCase()));

      return matchesCategory && matchesSearch;
    });

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 48px 20px; background: #FFFFFF; border-radius: var(--radius-card); border: 1px solid var(--border-light);">
          <p style="color: var(--text-muted); font-size: 1.05rem; margin-bottom: 12px;">No regional HR reports found matching your criteria.</p>
          <button class="zwc-primary-red-btn" id="btnResetBlogFilter">Reset Corridor Filters</button>
        </div>
      `;
      const resetBtn = document.getElementById('btnResetBlogFilter');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          activeCategory = 'all';
          searchTerm = '';
          if (searchInput) searchInput.value = '';
          filterBtns.forEach(b => b.classList.toggle('active', b.dataset.category === 'all'));
          renderBlogs();
        });
      }
      return;
    }

    container.innerHTML = filtered.map(blog => `
      <article class="blog-card" data-id="${blog.id}">
        <div class="blog-image-wrap">
          <img src="${blog.image || '/images/heroes/thc_hero.jpg'}" alt="${blog.title}" class="blog-image" loading="lazy">
          <div class="blog-image-overlay"></div>
          <span class="blog-category-badge">${blog.category}</span>
          ${blog.region ? `<span class="blog-region-pill"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:-1px; margin-right:4px;"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>${blog.region.split('(')[0].trim()}</span>` : ''}
        </div>
        <div class="blog-content">
          <div class="blog-meta">
            <span class="blog-meta-item">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              ${blog.date}
            </span>
            <span class="blog-meta-item">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              ${blog.readTime || '6 min read'}
            </span>
          </div>
          <h3 class="blog-title">${blog.title}</h3>
          <p class="blog-excerpt">${blog.excerpt}</p>
          <div class="blog-author-line">
            <span>By ${blog.author}</span>
          </div>
          <div class="blog-footer-action">
            <button class="btn-read-article" data-id="${blog.id}">
              Read Executive Report &rarr;
            </button>
          </div>
        </div>
      </article>
    `).join('');

    // Attach click listeners to Read Article buttons
    container.querySelectorAll('.btn-read-article').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        openBlogDetailModal(id);
      });
    });
  }

  // Filter Buttons
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.dataset.category || 'all';
      renderBlogs();
    });
  });

  // Search Input
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.trim();
      renderBlogs();
    });
  }

  // Listen for storage changes
  window.addEventListener('thc:data-changed', (e) => {
    if (e.detail?.type === 'blogs') {
      renderBlogs();
    }
  });

  renderBlogs();
}

export function openBlogDetailModal(blogId) {
  const blogs = Storage.getBlogs();
  const blog = blogs.find(b => b.id === blogId);
  if (!blog) return;

  const titleEl = document.getElementById('modalBlogTitle');
  const catEl = document.getElementById('modalBlogCategory');
  const dateEl = document.getElementById('modalBlogDate');
  const authorEl = document.getElementById('modalBlogAuthor');
  const contentEl = document.getElementById('modalBlogContent');
  const imgEl = document.getElementById('modalBlogImage');

  if (titleEl) titleEl.textContent = blog.title;
  if (catEl) catEl.textContent = blog.category;
  if (dateEl) dateEl.textContent = `${blog.date} • ${blog.readTime || '5 min read'}`;
  if (authorEl) authorEl.textContent = `Written by ${blog.author || 'THC Strategic Research Desk'}`;
  if (contentEl) contentEl.innerHTML = blog.content || `<p>${blog.excerpt}</p>`;
  if (imgEl) imgEl.src = blog.image || '/images/team/thc_leadership.jpg';

  openModal('blogDetailModal');
}
