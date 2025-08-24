// HackHub - Advanced Dynamic Effects & Animations

class DynamicEffects {
    constructor() {
        this.init();
    }

    init() {
        this.createParticleSystem();
        this.initializeScrollAnimations();
        this.setupMagneticElements();
        this.createFloatingShapes();
        this.initializeTypingEffect();
        this.setupInteractiveElements();
        this.initializeCounters();
        this.createMatrixRain();
        this.setupParallaxEffects();
        this.initializeMorphingElements();
    }

    // ===============================
    // PARTICLE SYSTEM
    // ===============================
    createParticleSystem() {
        const container = document.createElement('div');
        container.className = 'particle-container';
        document.body.appendChild(container);

        // Create particles
        for (let i = 0; i < 15; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Randomize particle properties
            const size = Math.random() * 8 + 2;
            const animationDuration = Math.random() * 10 + 5;
            const animationDelay = Math.random() * 5;
            const leftPosition = Math.random() * 100;
            
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = leftPosition + '%';
            particle.style.animationDuration = animationDuration + 's';
            particle.style.animationDelay = animationDelay + 's';
            
            // Random colors
            const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#43e97b'];
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];
            
            container.appendChild(particle);
        }
    }

    // ===============================
    // SCROLL ANIMATIONS
    // ===============================
    initializeScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    
                    // Add staggered animation for children
                    const children = entry.target.querySelectorAll('.stagger-child');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('revealed');
                        }, index * 100);
                    });
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '-50px 0px'
        });

        // Observe all elements with scroll-reveal class
        document.querySelectorAll('.scroll-reveal').forEach(el => {
            observer.observe(el);
        });

        // Add scroll-reveal class to cards and sections
        this.addScrollRevealClasses();
    }

    addScrollRevealClasses() {
        const selectors = [
            '.card', '.feature-card', '.participant-card', 
            '.team-card', '.stat-card', '.portal-card'
        ];
        
        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(el => {
                el.classList.add('scroll-reveal');
            });
        });
    }

    // ===============================
    // MAGNETIC ELEMENTS
    // ===============================
    setupMagneticElements() {
        const magneticElements = document.querySelectorAll('.btn, .card, .nav-link');
        
        magneticElements.forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                const moveX = x * 0.1;
                const moveY = y * 0.1;
                
                element.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'translate(0px, 0px)';
            });
        });
    }

    // ===============================
    // FLOATING SHAPES
    // ===============================
    createFloatingShapes() {
        const shapes = [
            { type: 'circle', size: 40, top: '10%', left: '80%' },
            { type: 'square', size: 30, top: '20%', left: '10%' },
            { type: 'triangle', size: 35, top: '60%', left: '85%' },
            { type: 'circle', size: 25, top: '80%', left: '5%' },
            { type: 'square', size: 20, top: '40%', left: '90%' }
        ];

        shapes.forEach((shapeConfig, index) => {
            const shape = document.createElement('div');
            shape.className = `floating-shape ${shapeConfig.type}`;
            shape.style.width = shapeConfig.size + 'px';
            shape.style.height = shapeConfig.size + 'px';
            shape.style.top = shapeConfig.top;
            shape.style.left = shapeConfig.left;
            shape.style.animationDelay = index * 2 + 's';
            
            document.body.appendChild(shape);
        });
    }

    // ===============================
    // TYPING EFFECT
    // ===============================
    initializeTypingEffect() {
        const typingElements = document.querySelectorAll('.typing-text');
        
        typingElements.forEach(element => {
            const text = element.textContent;
            element.textContent = '';
            element.classList.add('typing-active');
            
            let index = 0;
            const typeWriter = () => {
                if (index < text.length) {
                    element.textContent += text.charAt(index);
                    index++;
                    setTimeout(typeWriter, 100);
                } else {
                    setTimeout(() => {
                        element.textContent = '';
                        index = 0;
                        typeWriter();
                    }, 3000);
                }
            };
            
            setTimeout(typeWriter, 1000);
        });
    }

    // ===============================
    // INTERACTIVE ELEMENTS
    // ===============================
    setupInteractiveElements() {
        // Add hover effects to icons
        const icons = document.querySelectorAll('i[class*="fa"]');
        icons.forEach(icon => {
            icon.classList.add('interactive-icon');
        });

        // Add 3D card effects
        const cards = document.querySelectorAll('.card, .feature-card, .participant-card, .team-card');
        cards.forEach(card => {
            card.classList.add('card-3d', 'hover-lift');
        });

        // Add animated buttons
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.classList.add('btn-animated', 'gpu-acceleration');
        });

        // Add glowing effects to important elements
        const primaryButtons = document.querySelectorAll('.btn-primary');
        primaryButtons.forEach(btn => {
            btn.classList.add('btn-pulse');
        });
    }

    // ===============================
    // ANIMATED COUNTERS
    // ===============================
    initializeCounters() {
        const counters = document.querySelectorAll('.stat-number, .score-value');
        
        const animateCounter = (element) => {
            const target = parseInt(element.textContent) || 0;
            const duration = 2000;
            const start = performance.now();
            
            const animate = (currentTime) => {
                const elapsed = currentTime - start;
                const progress = Math.min(elapsed / duration, 1);
                
                // Easing function for smooth animation
                const easeOutCubic = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(easeOutCubic * target);
                
                element.textContent = current;
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    element.textContent = target;
                }
            };
            
            requestAnimationFrame(animate);
        };

        // Animate counters when they come into view
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        });

        counters.forEach(counter => {
            counterObserver.observe(counter);
        });
    }

    // ===============================
    // MATRIX RAIN EFFECT
    // ===============================
    createMatrixRain() {
        const container = document.createElement('div');
        container.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -3;
            overflow: hidden;
        `;
        
        document.body.appendChild(container);

        // Create matrix rain columns
        for (let i = 0; i < 20; i++) {
            const column = document.createElement('div');
            column.style.cssText = `
                position: absolute;
                top: -100px;
                left: ${i * 5}%;
                width: 2px;
                height: 100px;
                background: linear-gradient(transparent, #667eea, transparent);
                animation: matrix-rain ${5 + Math.random() * 10}s linear infinite;
                animation-delay: ${Math.random() * 10}s;
                opacity: 0.3;
            `;
            
            container.appendChild(column);
        }
    }

    // ===============================
    // PARALLAX EFFECTS
    // ===============================
    setupParallaxEffects() {
        const parallaxElements = document.querySelectorAll('.parallax-element');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            
            parallaxElements.forEach(element => {
                element.style.transform = `translateY(${parallax}px)`;
            });
        });

        // Add parallax class to background elements
        document.querySelectorAll('.floating-shape').forEach(shape => {
            shape.classList.add('parallax-element');
        });
    }

    // ===============================
    // MORPHING ELEMENTS
    // ===============================
    initializeMorphingElements() {
        const morphElements = document.querySelectorAll('.hero-section, .features-section');
        morphElements.forEach(element => {
            element.classList.add('morphing-bg');
        });

        // Add morphing animation to cards
        const cards = document.querySelectorAll('.portal-card');
        cards.forEach((card, index) => {
            if (index % 3 === 0) {
                card.classList.add('card-morphing');
            }
        });
    }

    // ===============================
    // TEXT EFFECTS
    // ===============================
    createBouncingText(element) {
        const text = element.textContent;
        const chars = text.split('').map(char => 
            char === ' ' ? '&nbsp;' : `<span class="char">${char}</span>`
        ).join('');
        
        element.innerHTML = chars;
        element.classList.add('text-bouncing');
    }

    // ===============================
    // INTERACTIVE CURSOR
    // ===============================
    initializeCustomCursor() {
        const cursor = document.createElement('div');
        cursor.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            background: var(--primary-gradient);
            border-radius: 50%;
            pointer-events: none;
            z-index: 10000;
            opacity: 0.7;
            transition: all 0.1s ease;
            mix-blend-mode: difference;
        `;
        
        document.body.appendChild(cursor);
        
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX - 10 + 'px';
            cursor.style.top = e.clientY - 10 + 'px';
        });
        
        // Grow cursor on hover
        const hoverElements = document.querySelectorAll('button, a, .card');
        hoverElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                cursor.style.transform = 'scale(2)';
            });
            
            element.addEventListener('mouseleave', () => {
                cursor.style.transform = 'scale(1)';
            });
        });
    }

    // ===============================
    // DYNAMIC GRADIENTS
    // ===============================
    animateGradients() {
        const gradientElements = document.querySelectorAll('.gradient-text, .hero-section');
        gradientElements.forEach(element => {
            element.classList.add('dynamic-gradient');
        });
    }

    // ===============================
    // PERFORMANCE OPTIMIZATION
    // ===============================
    optimizeAnimations() {
        // Use Intersection Observer to pause animations when not visible
        const animatedElements = document.querySelectorAll('[class*="animation"], .particle');
        
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                } else {
                    entry.target.style.animationPlayState = 'paused';
                }
            });
        });

        animatedElements.forEach(element => {
            animationObserver.observe(element);
        });
    }

    // ===============================
    // CLEANUP AND DESTROY
    // ===============================
    destroy() {
        // Remove all dynamic elements
        document.querySelectorAll('.particle-container, .floating-shape').forEach(el => el.remove());
        
        // Remove all event listeners
        window.removeEventListener('scroll', this.scrollHandler);
        window.removeEventListener('mousemove', this.mouseMoveHandler);
    }
}

// ===============================
// UTILITY FUNCTIONS
// ===============================

function addStaggeredAnimation(container, delay = 100) {
    const children = container.children;
    Array.from(children).forEach((child, index) => {
        child.style.animationDelay = index * delay + 'ms';
        child.classList.add('scroll-reveal');
    });
}

function createRippleEffect(element, event) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    `;
    
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

// Add ripple effect styles
const rippleStyles = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;

const rippleStyleSheet = document.createElement('style');
rippleStyleSheet.textContent = rippleStyles;
document.head.appendChild(rippleStyleSheet);

// ===============================
// INITIALIZATION
// ===============================

let dynamicEffects;

document.addEventListener('DOMContentLoaded', () => {
    dynamicEffects = new DynamicEffects();
    
    // Add ripple effects to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        
        button.addEventListener('click', (e) => {
            createRippleEffect(button, e);
        });
    });
    
    // Enhanced page load animation
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 100);
});

// ===============================
// EXPORT FOR EXTERNAL USE
// ===============================

window.DynamicEffects = DynamicEffects;
window.addStaggeredAnimation = addStaggeredAnimation;
window.createRippleEffect = createRippleEffect;