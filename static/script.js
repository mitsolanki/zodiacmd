// AI Horoscope Generator - JavaScript Functionality
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const zodiacCards = document.querySelectorAll('.zodiac-card');
    const horoscopeSection = document.getElementById('horoscopeSection');
    const selectedSign = document.getElementById('selectedSign');
    const loading = document.getElementById('loading');
    const horoscopeContent = document.getElementById('horoscopeContent');
    const horoscopeText = document.getElementById('horoscopeText');
    const luckyNumber = document.getElementById('luckyNumber');
    const luckyColor = document.getElementById('luckyColor');
    const mood = document.getElementById('mood');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const refreshBtn = document.getElementById('refreshBtn');
    const themeToggle = document.getElementById('themeToggle');

    // Global variables
    let currentZodiacSign = '';
    let isLoading = false;

    // Theme Toggle Functionality
    function initTheme() {
        const savedTheme = localStorage.getItem('horoscope-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    }

    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        if (theme === 'light') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }

    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('horoscope-theme', newTheme);
        updateThemeIcon(newTheme);
        
        // Add ripple effect
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });

    // Zodiac Card Click Handlers
    zodiacCards.forEach(card => {
        card.addEventListener('click', function() {
            if (isLoading) return;

            const sign = this.getAttribute('data-sign');
            const signName = this.querySelector('.zodiac-name').textContent;
            const signSymbol = this.querySelector('.zodiac-symbol').textContent;
            
            currentZodiacSign = sign;
            
            // Update selected sign display
            selectedSign.textContent = `${signSymbol} ${signName}`;
            
            // Add selection animation
            zodiacCards.forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            
            // Show horoscope section and get horoscope
            showHoroscopeSection();
            getHoroscope(sign);
        });

        // Add hover sound effect (optional)
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Refresh Button Handler
    refreshBtn.addEventListener('click', function() {
        if (isLoading || !currentZodiacSign) return;
        
        getHoroscope(currentZodiacSign);
        
        // Add click animation
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });

    // Show horoscope section with animation
    function showHoroscopeSection() {
        horoscopeSection.style.display = 'block';
        horoscopeSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'nearest' 
        });
    }

    // Hide error and content sections
    function resetHoroscopeDisplay() {
        errorMessage.style.display = 'none';
        horoscopeContent.style.display = 'none';
        loading.style.display = 'block';
    }

    // Show error message
    function showError(message) {
        loading.style.display = 'none';
        horoscopeContent.style.display = 'none';
        errorMessage.style.display = 'block';
        errorText.textContent = message;
    }

    // Show horoscope content with typing effect
    function showHoroscopeContent(data) {
        loading.style.display = 'none';
        errorMessage.style.display = 'none';
        horoscopeContent.style.display = 'block';
        
        // Update extra information immediately
        luckyNumber.textContent = data.lucky_number;
        luckyColor.textContent = data.lucky_color;
        mood.textContent = data.mood;
        
        // Add typing effect to horoscope text
        typeWriter(horoscopeText, data.horoscope, 50);
        
        // Animate extra items
        animateExtraItems();
    }

    // Typing effect function
    function typeWriter(element, text, speed = 50) {
        element.textContent = '';
        let i = 0;
        
        function typing() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typing, speed);
            } else {
                // Add breathing animation when typing is complete
                element.classList.add('breathing-text');
                setTimeout(() => {
                    element.classList.remove('breathing-text');
                }, 2000);
            }
        }
        
        typing();
    }

    // Animate extra items
    function animateExtraItems() {
        const extraItems = document.querySelectorAll('.extra-item');
        extraItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                item.style.transition = 'all 0.5s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, 500 + (index * 200));
        });
    }

    // Main function to get horoscope from API
    async function getHoroscope(zodiacSign) {
        if (isLoading) return;
        
        isLoading = true;
        resetHoroscopeDisplay();
        
        try {
            const response = await fetch('/get_horoscope', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    zodiac_sign: zodiacSign
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Simulate a minimum loading time for better UX
                setTimeout(() => {
                    showHoroscopeContent(data);
                    isLoading = false;
                }, 1500);
            } else {
                setTimeout(() => {
                    showError(data.error || 'Failed to generate horoscope');
                    isLoading = false;
                }, 1000);
            }
            
        } catch (error) {
            console.error('Error fetching horoscope:', error);
            setTimeout(() => {
                showError('Network error. Please check your connection and try again.');
                isLoading = false;
            }, 1000);
        }
    }

    // Add keyboard support for accessibility
    document.addEventListener('keydown', function(e) {
        // Press 'R' to refresh current horoscope
        if (e.key === 'r' || e.key === 'R') {
            if (currentZodiacSign && !isLoading) {
                refreshBtn.click();
            }
        }
        
        // Press Escape to go back to zodiac selection
        if (e.key === 'Escape') {
            if (horoscopeSection.style.display !== 'none') {
                horoscopeSection.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }
        }
    });

    // Add particle effect on zodiac card click
    function createParticles(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        for (let i = 0; i < 6; i++) {
            createParticle(centerX, centerY);
        }
    }

    function createParticle(x, y) {
        const particle = document.createElement('div');
        particle.innerHTML = '✨';
        particle.style.position = 'fixed';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.fontSize = '20px';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '9999';
        particle.style.color = '#ffd700';
        
        document.body.appendChild(particle);
        
        // Animate particle
        const angle = Math.random() * Math.PI * 2;
        const distance = 100 + Math.random() * 100;
        const endX = x + Math.cos(angle) * distance;
        const endY = y + Math.sin(angle) * distance;
        
        particle.animate([
            { 
                transform: 'translate(0, 0) scale(1)', 
                opacity: 1 
            },
            { 
                transform: `translate(${endX - x}px, ${endY - y}px) scale(0)`, 
                opacity: 0 
            }
        ], {
            duration: 1000,
            easing: 'cubic-bezier(0.4, 0.0, 0.2, 1)'
        }).onfinish = () => {
            document.body.removeChild(particle);
        };
    }

    // Enhanced zodiac card click with particles
    zodiacCards.forEach(card => {
        const originalClickHandler = card.onclick;
        card.addEventListener('click', function(e) {
            createParticles(this);
        });
    });

    // Add floating animation to zodiac cards
    function addFloatingAnimation() {
        zodiacCards.forEach((card, index) => {
            card.style.animation = `floating 3s ease-in-out infinite`;
            card.style.animationDelay = `${index * 0.2}s`;
        });
    }

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.zodiac-card, .header, .footer').forEach(el => {
        observer.observe(el);
    });

    // Add CSS for additional animations
    const additionalStyles = `
        <style>
        .selected {
            border: 2px solid var(--accent-color) !important;
            box-shadow: 0 0 30px var(--hover-glow) !important;
        }
        
        .breathing-text {
            animation: breathe 2s ease-in-out infinite;
        }
        
        @keyframes breathe {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes floating {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .fade-in-up {
            animation: fadeInUp 0.8s ease-out forwards;
        }
        
        .extra-item {
            transition: all 0.3s ease;
        }
        
        .loading-spinner {
            animation: spin 1s linear infinite, pulse 2s ease-in-out infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    `;
    
    document.head.insertAdjacentHTML('beforeend', additionalStyles);

    // Initialize theme and floating animations
    initTheme();
    setTimeout(addFloatingAnimation, 1000);

    // Add smooth scrolling behavior
    document.documentElement.style.scrollBehavior = 'smooth';

    // Console welcome message
    console.log('%c🌟 AI Horoscope Generator Ready! 🌟', 
        'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px; border-radius: 5px; font-size: 16px;');
    console.log('%cPress "R" to refresh horoscope, "Escape" to scroll to top', 
        'color: #ffd700; font-size: 12px;');
});

// PWA Service Worker Registration (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment if you want to add PWA functionality
        // navigator.serviceWorker.register('/service-worker.js');
    });
}

// Export functions for testing (if needed)
window.HoroscopeApp = {
    version: '1.0.0',
    author: 'AI Horoscope Generator',
    features: ['Dark/Light Theme', 'Typing Animation', 'Particle Effects', 'Responsive Design']
};
