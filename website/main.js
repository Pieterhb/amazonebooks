// Navigation logic for sidebar layout

document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.nav-list a, .logo');
  const views = document.querySelectorAll('.view');
  const sidebar = document.getElementById('sidebar');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');

  function navigateTo(targetId) {
    // Hide all views
    views.forEach(view => {
      view.classList.remove('active');
    });
    
    // Show target view
    const targetView = document.getElementById(targetId);
    if (targetView) {
      targetView.classList.add('active');
    }

    // Update active state on nav links
    document.querySelectorAll('.nav-list a').forEach(link => {
      link.classList.remove('active');
      if (link.dataset.target === targetId) {
        link.classList.add('active');
      }
    });

    // Close sidebar on mobile after clicking a link
    if (window.innerWidth <= 1024) {
      sidebar.classList.remove('open');
    }

    window.scrollTo(0, 0);
  }

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = link.dataset.target;
      if (target) navigateTo(target);
    });
  });

  // Mobile menu toggle
  if (mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth <= 1024) {
        if (!e.target.closest('#sidebar') && !e.target.closest('#mobile-menu-btn')) {
          sidebar.classList.remove('open');
        }
      }
    });
  }
});
