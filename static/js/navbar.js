// Navbar JavaScript for enhanced interactions

document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.main-navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    // Add scrolled class on scroll
    let lastScroll = 0;
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
    
    // Set active link based on current URL
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath || 
            (currentPath === '/' && linkPath === '/') ||
            (currentPath !== '/' && currentPath.startsWith(linkPath) && linkPath !== '/')) {
            link.classList.add('active');
        }
    });
    
    // Smooth scroll for anchor links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
    
    // Mobile menu close on link click
    const navbarCollapse = document.querySelector('.navbar-collapse');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            }
        });
    });
    
    // Add hover effect to navbar brand
    const brandWrapper = document.querySelector('.brand-wrapper');
    if (brandWrapper) {
        brandWrapper.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        brandWrapper.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    }
    
    // Dropdown animation
    const dropdownToggle = document.querySelector('.user-dropdown');
    if (dropdownToggle) {
        dropdownToggle.addEventListener('shown.bs.dropdown', function() {
            const dropdown = this.nextElementSibling;
            dropdown.style.animation = 'dropdownFadeIn 0.3s ease';
        });
    }
    
    // Navbar color change on scroll (subtle)
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.5;
        
        if (scrolled > 100) {
            navbar.style.background = `linear-gradient(135deg, 
                rgba(102, 126, 234, ${0.95 - rate * 0.001}) 0%, 
                rgba(118, 75, 162, ${0.95 - rate * 0.001}) 100%)`;
        } else {
            navbar.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    });
});

