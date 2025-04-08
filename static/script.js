document.addEventListener("DOMContentLoaded", function () {
    const scrollContainer = document.querySelector(".reasons-container");
    let scrollInterval;
    let isScrolling = false;
    let scrollAmount = 0;
    const cardWidth = 305; // Width of card + gap

    // Function to scroll left
    window.scrollLeft = function() {
        scrollContainer.scrollBy({
            left: -cardWidth,
            behavior: "smooth"
        });
    };

    // Function to scroll right
    window.scrollRight = function() {
        scrollContainer.scrollBy({
            left: cardWidth,
            behavior: "smooth"
        });
    };

    function startScrolling(direction) {
        if (isScrolling) return;
        
        isScrolling = true;
        stopScrolling(); // Clear any existing interval
        
        scrollInterval = setInterval(() => {
            scrollAmount += 2;
            scrollContainer.scrollBy({
                left: direction * 5, // Adjust speed here
                behavior: "auto",
            });
            
            // Add easing effect
            if (scrollAmount > 60) {
                clearInterval(scrollInterval);
                scrollAmount = 0;
                isScrolling = false;
            }
        }, 10); // Frequency of scrolling
    }

    function stopScrolling() {
        clearInterval(scrollInterval);
        scrollAmount = 0;
    }

    // Auto-scroll on edge hover
    document.addEventListener("mousemove", (event) => {
        const screenWidth = window.innerWidth;
        const edgeThreshold = 50; // How close to the edge the hover effect starts
        const reasonsSection = document.querySelector(".reasons");
        const reasonsRect = reasonsSection.getBoundingClientRect();
        
        // Only activate auto-scroll when mouse is within the reasons section
        if (event.clientY >= reasonsRect.top && event.clientY <= reasonsRect.bottom) {
            if (event.clientX < edgeThreshold) {
                startScrolling(-1); // Scroll left
            } else if (event.clientX > screenWidth - edgeThreshold) {
                startScrolling(1); // Scroll right
            } else {
                if (isScrolling) {
                    stopScrolling(); // Stop when not near edges
                    isScrolling = false;
                }
            }
        }
    });

    document.addEventListener("mouseleave", () => {
        stopScrolling(); // Stops scrolling when the mouse leaves
        isScrolling = false;
    });

    // Add animation to hero section
    const heroContent = document.querySelector('.hero-content');
    
    if (heroContent) {
        setTimeout(() => {
            heroContent.style.opacity = '1';
            heroContent.style.transform = 'translateY(0)';
        }, 300);
    }

    // Add animation to reasons cards on scroll
    const reasons = document.querySelectorAll('.reason');
    const features = document.querySelectorAll('.feature-container');
    
    function checkScroll() {
        // Animate reasons
        reasons.forEach(reason => {
            const rect = reason.getBoundingClientRect();
            const isVisible = (rect.top <= window.innerHeight * 0.8);
            
            if (isVisible) {
                reason.classList.add('animate-in');
            }
        });
        
        // Animate features
        features.forEach(feature => {
            const rect = feature.getBoundingClientRect();
            const isVisible = (rect.top <= window.innerHeight * 0.8);
            
            if (isVisible) {
                feature.classList.add('animate-in');
            }
        });
    }
    
    // Initial check
    checkScroll();
    
    // Check on scroll
    window.addEventListener('scroll', checkScroll);
});

// Add this CSS rule dynamically
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .hero-content {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }
        
        .reason {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
        
        .reason.animate-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        .feature-container {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }
        
        .feature-container.animate-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
});