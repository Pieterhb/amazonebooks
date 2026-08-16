// Navigation and interactive features for Softcover Books pSEO

document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const searchInput = document.getElementById('pseo-search');
  const searchDropdown = document.getElementById('search-dropdown');
  const searchForm = searchInput ? searchInput.closest('form') : null;
  const noResultsMsg = document.getElementById('no-results-msg');
  const clearSearchBtn = document.getElementById('clear-search-btn');

  // Sidebar scroll position persistence across page navigations
  if (sidebar) {
    // Restore saved scroll position
    const savedPos = sessionStorage.getItem('sidebar_scroll_pos');
    if (savedPos !== null) {
      sidebar.scrollTop = parseInt(savedPos, 10);
    } else {
      // If no saved position, scroll active menu item into view
      const activeLink = sidebar.querySelector('.nav-list a.active');
      if (activeLink) {
        const linkTop = activeLink.getBoundingClientRect().top - sidebar.getBoundingClientRect().top + sidebar.scrollTop;
        sidebar.scrollTop = Math.max(0, linkTop - (sidebar.clientHeight / 2));
      }
    }

    // Save scroll position when user scrolls the sidebar
    sidebar.addEventListener('scroll', () => {
      sessionStorage.setItem('sidebar_scroll_pos', sidebar.scrollTop);
    }, { passive: true });

    // Save immediately before navigating away via sidebar link
    sidebar.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (link) {
        sessionStorage.setItem('sidebar_scroll_pos', sidebar.scrollTop);
      }
    });

    // Save on beforeunload as additional safeguard
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('sidebar_scroll_pos', sidebar.scrollTop);
    });
  }

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

  // Helper: Escape HTML
  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // ── SEARCH & FILTER ENGINE ────────────────────────────────────────────────
  const bookCards = document.querySelectorAll('.product-grid .book-card');
  const countDisplay = document.getElementById('search-results-count');

  // Filter existing cards on catalog/list pages
  function filterCards(query) {
    const q = (query || '').toLowerCase().trim();
    let visibleCount = 0;

    bookCards.forEach(card => {
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

    if (countDisplay) {
      countDisplay.innerText = q ? `${visibleCount} book${visibleCount === 1 ? '' : 's'} found` : '';
    }

    if (noResultsMsg) {
      noResultsMsg.style.display = (q && visibleCount === 0) ? 'block' : 'none';
    }
  }

  // Check if we are on a page with pre-rendered book cards (e.g. /books/)
  if (bookCards.length > 0 && searchInput) {
    // 1. Check for initial URL query parameter (?q=... or ?search=...)
    const urlParams = new URLSearchParams(window.location.search);
    const initialQuery = urlParams.get('q') || urlParams.get('search') || '';
    if (initialQuery) {
      searchInput.value = initialQuery;
      filterCards(initialQuery);
    }

    // 2. Filter live on typing
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.trim();
      filterCards(q);
      const newUrl = q ? `${window.location.pathname}?q=${encodeURIComponent(q)}` : window.location.pathname;
      window.history.replaceState(null, '', newUrl);
    });

    if (clearSearchBtn) {
      clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        filterCards('');
        window.history.replaceState(null, '', window.location.pathname);
        searchInput.focus();
      });
    }
  }

  // ── SEARCH AUTOCOMPLETE DROPDOWN (Homepage & Site-wide) ────────────────────
  let searchIndex = null;
  let isFetchingIndex = false;
  let selectedIndex = -1;

  async function loadSearchIndex() {
    if (searchIndex || isFetchingIndex) return searchIndex;
    isFetchingIndex = true;
    try {
      const res = await fetch('/search-index.json');
      if (res.ok) {
        searchIndex = await res.json();
      }
    } catch (err) {
      console.warn('Could not load search index:', err);
    } finally {
      isFetchingIndex = false;
    }
    return searchIndex;
  }

  // Preload search index on search bar focus or hover
  if (searchInput) {
    searchInput.addEventListener('focus', loadSearchIndex, { once: true });
    searchInput.addEventListener('mouseenter', loadSearchIndex, { once: true });
  }

  if (searchDropdown && searchInput) {
    function hideDropdown() {
      searchDropdown.style.display = 'none';
      searchDropdown.setAttribute('aria-expanded', 'false');
      selectedIndex = -1;
    }

    async function handleDropdownSearch() {
      const q = searchInput.value.toLowerCase().trim();
      if (!q || q.length < 1) {
        hideDropdown();
        return;
      }

      const index = await loadSearchIndex();
      if (!index || !index.books) {
        return;
      }

      // Find matching books
      const matchingBooks = index.books.filter(b => {
        return (b.title && b.title.toLowerCase().includes(q)) ||
               (b.author && b.author.toLowerCase().includes(q)) ||
               (b.series && b.series.toLowerCase().includes(q)) ||
               (b.primary_genre && b.primary_genre.toLowerCase().includes(q));
      });

      // Find matching series & authors
      const matchingSeries = (index.series || []).filter(s => s.name.toLowerCase().includes(q)).slice(0, 3);
      const matchingAuthors = (index.authors || []).filter(a => a.name.toLowerCase().includes(q)).slice(0, 2);

      let html = '';

      if (matchingBooks.length === 0 && matchingSeries.length === 0 && matchingAuthors.length === 0) {
        html = `
          <div class="search-dropdown-empty">
            No books matching "<strong>${escapeHtml(q)}</strong>".<br>
            <a href="/books/?q=${encodeURIComponent(q)}">Search all books catalog &rarr;</a>
          </div>
        `;
      } else {
        // Book results (top 5)
        const topBooks = matchingBooks.slice(0, 5);
        html += `<div class="search-dropdown-section-title">Matching Ebooks (${matchingBooks.length})</div>`;
        topBooks.forEach(b => {
          html += `
            <a href="/books/${b.slug}/" class="search-dropdown-item" data-type="book">
              <img src="${b.img}" alt="${escapeHtml(b.title)}" class="search-dropdown-thumb" loading="lazy">
              <div class="search-dropdown-info">
                <div class="search-dropdown-title">${escapeHtml(b.title)}</div>
                <div class="search-dropdown-author">By ${escapeHtml(b.author)}${b.series && b.series !== 'Other' ? ` &bull; ${escapeHtml(b.series)}` : ''}</div>
              </div>
              <span class="search-dropdown-badge">${escapeHtml(b.lang || 'Ebook')}</span>
            </a>
          `;
        });

        // Series / Author suggestions
        if (matchingSeries.length > 0 || matchingAuthors.length > 0) {
          html += `<div class="search-dropdown-section-title">Series &amp; Authors</div>`;
          matchingSeries.forEach(s => {
            html += `
              <a href="/series/${s.slug}/" class="search-dropdown-item" data-type="series">
                <div class="search-dropdown-info">
                  <div class="search-dropdown-title">📖 ${escapeHtml(s.name)}</div>
                  <div class="search-dropdown-author">Complete Series &bull; ${s.count} Ebooks</div>
                </div>
                <span class="search-dropdown-badge">Series</span>
              </a>
            `;
          });
          matchingAuthors.forEach(a => {
            html += `
              <a href="/authors/${a.slug}/" class="search-dropdown-item" data-type="author">
                <div class="search-dropdown-info">
                  <div class="search-dropdown-title">✍️ ${escapeHtml(a.name)}</div>
                  <div class="search-dropdown-author">Author Bibliography &bull; ${a.count} Books</div>
                </div>
                <span class="search-dropdown-badge">Author</span>
              </a>
            `;
          });
        }

        // Dropdown footer
        html += `
          <a href="/books/?q=${encodeURIComponent(q)}" class="search-dropdown-footer">
            View all ${matchingBooks.length} results in All Books &rarr;
          </a>
        `;
      }

      searchDropdown.innerHTML = html;
      searchDropdown.style.display = 'block';
      searchDropdown.setAttribute('aria-expanded', 'true');
      selectedIndex = -1;
    }

    // Event listeners for autocomplete input
    searchInput.addEventListener('input', handleDropdownSearch);
    searchInput.addEventListener('focus', () => {
      if (searchInput.value.trim()) {
        handleDropdownSearch();
      }
    });

    // Keyboard navigation in dropdown
    searchInput.addEventListener('keydown', (e) => {
      const items = searchDropdown.querySelectorAll('.search-dropdown-item, .search-dropdown-footer');
      if (searchDropdown.style.display !== 'block' || items.length === 0) {
        if (e.key === 'Enter') {
          const q = searchInput.value.trim();
          if (q) {
            window.location.href = `/books/?q=${encodeURIComponent(q)}`;
            e.preventDefault();
          }
        }
        return;
      }

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = (selectedIndex + 1) % items.length;
        updateItemSelection(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = (selectedIndex - 1 + items.length) % items.length;
        updateItemSelection(items);
      } else if (e.key === 'Enter') {
        if (selectedIndex >= 0 && items[selectedIndex]) {
          e.preventDefault();
          items[selectedIndex].click();
        } else {
          const q = searchInput.value.trim();
          if (q) {
            window.location.href = `/books/?q=${encodeURIComponent(q)}`;
            e.preventDefault();
          }
        }
      } else if (e.key === 'Escape') {
        hideDropdown();
      }
    });

    function updateItemSelection(items) {
      items.forEach((item, idx) => {
        if (idx === selectedIndex) {
          item.classList.add('is-selected');
          item.scrollIntoView({ block: 'nearest' });
        } else {
          item.classList.remove('is-selected');
        }
      });
    }

    // Close dropdown on outside click
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.pseo-search-container')) {
        hideDropdown();
      }
    });

    // Form submission
    if (searchForm) {
      searchForm.addEventListener('submit', (e) => {
        const q = searchInput.value.trim();
        if (q) {
          window.location.href = `/books/?q=${encodeURIComponent(q)}`;
          e.preventDefault();
        }
      });
    }
  }

  // ── GA4: Track Store CTA Clicks (Amazon, Kobo, etc.) ───────────────────────
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-amazon');
    if (!btn) return;

    const href = btn.getAttribute('href') || '';
    const store = href.includes('kobo.com') ? 'kobo' : (href.includes('play.google.com') ? 'google_play' : (href.includes('sqrindle.com') ? 'sqrindle' : 'amazon'));

    if (typeof gtag === 'function') {
      gtag('event', 'store_click', {
        store: store,
        book_title: btn.dataset.title || btn.getAttribute('aria-label') || '',
        author: btn.dataset.author || '',
        genre: btn.dataset.genre || '',
        target_url: btn.dataset.amazonUrl || href,
      });

      if (store === 'amazon') {
        gtag('event', 'amazon_click', {
          book_title: btn.dataset.title || btn.getAttribute('aria-label') || '',
          author: btn.dataset.author || '',
          genre: btn.dataset.genre || '',
          amazon_url: btn.dataset.amazonUrl || href,
        });
      }
    }
  });
  // ─────────────────────────────────────────────────────────────────────────
});

