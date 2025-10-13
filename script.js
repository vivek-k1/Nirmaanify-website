document.addEventListener('DOMContentLoaded', function() {
    console.log('Nirmaanify website loaded successfully! 🚀');
    initializeMobileMenu();
    initializeForms();
    initializeSmoothScrolling();
    initializeAnimations();
});

function initializeMobileMenu() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            nav.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
            
            const spans = mobileMenuBtn.querySelectorAll('span');
            if (mobileMenuBtn.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        document.addEventListener('click', function(e) {
            if (!mobileMenuBtn.contains(e.target) && !nav.contains(e.target)) {
                nav.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                
                const spans = mobileMenuBtn.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        
    }
}

function initializeForms() {
    const supportForm = document.getElementById('supportForm');
    if (supportForm) {
        supportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleSupportFormSubmission(this);
        });
    }
    
    const internshipForm = document.getElementById('internshipForm');
    if (internshipForm) {
        internshipForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleInternshipFormSubmission(this);
        });
    }
    
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleContactFormSubmission(this);
        });
    }
}

async function handleSupportFormSubmission(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    try {
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        if (!data.name || !data.email || !data.service || !data['project-details']) {
            showNotification('Please fill in all required fields.', 'error');
            return;
        }
        
        const response = await fetch('/api/services', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            form.reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            showNotification(result.error || 'Failed to submit form', 'error');
        }
        
    } catch (error) {
        console.error('Error submitting form:', error);
        showNotification('Network error. Please try again.', 'error');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

async function handleInternshipFormSubmission(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    try {
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        if (!data.name || !data.email || !data.phone || !data.area || !data.skills || !data.duration || !data.motivation) {
            showNotification('Please fill in all required fields.', 'error');
            return;
        }
        
        const response = await fetch('/api/training', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            form.reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            showNotification(result.error || 'Failed to submit form', 'error');
        }
        
    } catch (error) {
        console.error('Error submitting form:', error);
        showNotification('Network error. Please try again.', 'error');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

async function handleContactFormSubmission(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    try {
        submitBtn.textContent = 'Submitting...';
        submitBtn.disabled = true;
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        if (!data.name || !data.email || !data.subject || !data.message) {
            showNotification('Please fill in all required fields.', 'error');
            return;
        }
        
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification(result.message, 'success');
            form.reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            showNotification(result.error || 'Failed to submit form', 'error');
        }
        
    } catch (error) {
        console.error('Error submitting form:', error);
        showNotification('Network error. Please try again.', 'error');
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
}

function initializeSmoothScrolling() {
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

function initializeAnimations() {
    const sections = document.querySelectorAll('section');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const sectionObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        sectionObserver.observe(section);
    });
    
    const serviceCards = document.querySelectorAll('.service-card, .service-detailed-card, .benefit-card, .area-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 8px 25px rgba(106, 62, 232, 0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        });
    });
}

function enhanceFormFields() {
    const formFields = document.querySelectorAll('.form-group input, .form-group textarea, .form-group select');
    
    formFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        field.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        if (field.tagName === 'TEXTAREA') {
            const counter = document.createElement('div');
            counter.className = 'char-counter';
            counter.style.fontSize = '0.8rem';
            counter.style.color = '#888';
            counter.style.textAlign = 'right';
            counter.style.marginTop = '0.5rem';
            
            field.parentElement.appendChild(counter);
            
            field.addEventListener('input', function() {
                const remaining = 1000 - this.value.length;
                counter.textContent = `${remaining} characters remaining`;
                
                if (remaining < 100) {
                    counter.style.color = '#e74c3c';
                } else if (remaining < 200) {
                    counter.style.color = '#f39c12';
                } else {
                    counter.style.color = '#888';
                }
            });
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    enhanceFormFields();
});

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;
    
    if (type === 'success') {
        notification.style.backgroundColor = '#6A3EE8';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#e74c3c';
    } else if (type === 'warning') {
        notification.style.backgroundColor = '#f39c12';
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.parentElement.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function addScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: #6A3EE8;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 1.5rem;
        box-shadow: 0 4px 12px rgba(106, 62, 232, 0.3);
        transition: all 0.3s ease;
        opacity: 0;
        visibility: hidden;
        z-index: 1000;
    `;
    
    document.body.appendChild(scrollBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.style.opacity = '1';
            scrollBtn.style.visibility = 'visible';
        } else {
            scrollBtn.style.opacity = '0';
            scrollBtn.style.visibility = 'hidden';
        }
    });
    
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    scrollBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
        this.style.backgroundColor = '#5A2ED8';
    });
    
    scrollBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
        this.style.backgroundColor = '#6A3EE8';
    });
}

document.addEventListener('DOMContentLoaded', function() {
    addScrollToTop();
});

console.log(`
%cWelcome to Nirmaanify! 🚀
%c
%cWe're excited to have you here! This website now includes:
%c• Responsive design for all devices
%c• Interactive forms with Flask backend
%c• Smooth animations and transitions
%c• Mobile-friendly navigation
%c• Real form submissions and data storage
%c
%cBackend API endpoints:
%c• POST /api/contact - Contact form
%c• POST /api/services - Service requests
%c• POST /api/training - Internship applications
%c• GET /api/submissions - View all submissions
%c
%cFeel free to explore the code and customize it for your needs!
%c
%cFor support or questions, contact us at contact@nirmaanify.com
`,
'color: #6A3EE8; font-size: 20px; font-weight: bold;',
'',
'color: #333; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'',
'color: #6A3EE8; font-size: 14px; font-weight: bold;',
'color: #6A3EE8; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'color: #6A3EE8; font-size: 14px;',
'',
'color: #666; font-size: 12px; font-style: italic;'
);
