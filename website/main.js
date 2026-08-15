// Navigation and interactive features for Softcover Books pSEO

document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const searchInput = document.getElementById('pseo-search');

  // Mobile menu toggle
  if (mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 1100 && sidebar.classList.contains('open')) {
        if (!e.target.closest('#sidebar') && !e.target.closest('#mobile-menu-btn')) {
          sidebar.classList.remove('open');
        }
      }
    });
  }

  // Live filter / search on books list if present
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      const cards = document.querySelectorAll('.product-grid .book-card');
      let visibleCount = 0;

      cards.forEach(card => {
        const title = (card.querySelector('h3') ? card.querySelector('h3').innerText : '').toLowerCase();
        const author = (card.querySelector('.author') ? card.querySelector('.author').innerText : '').toLowerCase();
        const series = (card.dataset.series || '').toLowerCase();
        
        if (!q || title.includes(q) || author.includes(q) || series.includes(q)) {
          card.style.display = 'flex';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      const countDisplay = document.getElementById('search-results-count');
      if (countDisplay) {
        countDisplay.innerText = q ? `${visibleCount} books found` : '';
      }
    });
  }

  // ── GA4: Track "Buy on Amazon" / Kindle clicks ────────────────────────────
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-amazon');
    if (!btn) return;

    // Only fire for Amazon/Kindle links (skip Kobo or other retailers)
    const href = btn.getAttribute('href') || '';
    if (!href.includes('amazon.com')) return;

    if (typeof gtag === 'function') {
      gtag('event', 'amazon_click', {
        book_title:  btn.dataset.title     || btn.getAttribute('aria-label') || '',
        author:      btn.dataset.author    || '',
        genre:       btn.dataset.genre     || '',
        amazon_url:  btn.dataset.amazonUrl || href,
      });
    }
  });
  // ─────────────────────────────────────────────────────────────────────────
});
