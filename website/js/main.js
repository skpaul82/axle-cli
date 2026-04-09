// Navigation Toggle
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add active class to current page
const currentPage = window.location.pathname.split('/').pop() || 'index.html';
navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
        link.classList.add('active');
    } else {
        link.classList.remove('active');
    }
});

// Copy to clipboard functionality for code blocks
function copyToClipboard(button) {
    const codeBlock = button.parentElement.querySelector('code');
    const text = codeBlock.textContent;

    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = '✓ Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

// Add copy buttons to code blocks
document.addEventListener('DOMContentLoaded', function() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.onclick = function() { copyToClipboard(this); };

        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);
    });
});

// FAQ Search Functionality
function searchFAQ(query) {
    const faqItems = document.querySelectorAll('.faq-item');
    const lowerQuery = query.toLowerCase();

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question').textContent.toLowerCase();
        const answer = item.querySelector('.faq-answer').textContent.toLowerCase();
        const category = item.querySelector('.faq-category')?.textContent.toLowerCase() || '';

        const matches = question.includes(lowerQuery) ||
                       answer.includes(lowerQuery) ||
                       category.includes(lowerQuery);

        if (matches || query === '') {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// FAQ Category Filter
function filterByCategory(category) {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const itemCategory = item.querySelector('.faq-category')?.textContent.toLowerCase();

        if (category === 'all' || itemCategory === category.toLowerCase()) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

// FAQ Toggle
function toggleFAQ(button) {
    const item = button.closest('.faq-item');
    const answer = item.querySelector('.faq-answer');
    const icon = button.querySelector('.faq-icon');

    answer.classList.toggle('active');
    icon.classList.toggle('active');
}

// Newsletter form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Zoho Campaigns form handling
function setupZF_Optin() {
    try {
        const zf_Form = document.getElementById('zf_optin_form');
        if (zf_Form) {
            zf_Form.addEventListener('submit', function(e) {
                const email = document.getElementById('CONTACT_EMAIL').value;
                if (!validateEmail(email)) {
                    e.preventDefault();
                    alert('Please enter a valid email address.');
                    return false;
                }
                return true;
            });
        }
    } catch (e) {
        console.error('Zoho Optin setup error:', e);
    }
}

// Analytics placeholder (replace with your analytics code)
function trackEvent(eventName, properties) {
    console.log('Event:', eventName, properties);
    // Add your analytics tracking here
    // Example: gtag('event', eventName, properties);
}

// Track button clicks
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            trackEvent('button_click', {
                button_text: buttonText,
                page: window.location.pathname
            });
        });
    });

    // Track external links
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    externalLinks.forEach(link => {
        link.addEventListener('click', function() {
            trackEvent('external_link_click', {
                url: this.href,
                page: window.location.pathname
            });
        });
    });
});

// Add loading animation
window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// Console welcome message
console.log('%c⚙️ Axle CLI', 'font-size: 24px; font-weight: bold; color: #2563eb;');
console.log('%cA modular platform for Python microtools', 'font-size: 14px; color: #64748b;');
console.log('%chttps://www.axle.sanjoypaul.com', 'font-size: 12px; color: #64748b;');
