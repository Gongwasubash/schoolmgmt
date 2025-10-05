// AGGRESSIVE MOBILE FIX - FORCE ALL ELEMENTS TO BE CLICKABLE
(function() {
    function forceMobileInteraction() {
        if (window.innerWidth <= 768) {
            // Force main content to be interactive
            const mainContent = document.querySelector('.main-content');
            if (mainContent) {
                mainContent.style.pointerEvents = 'auto !important';
                mainContent.style.touchAction = 'auto !important';
            }
            
            // Force all interactive elements to be clickable (except overlay)
            document.querySelectorAll('button, select, input, a, .btn, [onclick], .profile-btn, .menu-toggle').forEach(el => {
                if (!el.classList.contains('mobile-overlay')) {
                    el.style.pointerEvents = 'auto !important';
                    el.style.touchAction = 'manipulation !important';
                    el.style.webkitTapHighlightColor = 'rgba(0,0,0,0.3) !important';
                    el.style.position = 'relative !important';
                    el.style.zIndex = '999 !important';
                    el.style.minHeight = '48px !important';
                    el.style.minWidth = '48px !important';
                    el.style.cursor = 'pointer !important';
                }
            });
            
            // Special fix for content area
            document.querySelectorAll('.content, .container, main').forEach(el => {
                el.style.pointerEvents = 'auto !important';
                el.style.touchAction = 'auto !important';
            });
        }
    }
    
    // Run on load
    document.addEventListener('DOMContentLoaded', forceMobileInteraction);
    
    // Run continuously every 200ms for aggressive fixing
    setInterval(forceMobileInteraction, 200);
    
    // Run on resize
    window.addEventListener('resize', forceMobileInteraction);
    
    // Run on any click to ensure elements stay clickable
    document.addEventListener('click', function() {
        setTimeout(forceMobileInteraction, 50);
    });
    
    // Run on touch events
    document.addEventListener('touchstart', function() {
        setTimeout(forceMobileInteraction, 50);
    });
})();

// SIDEBAR SPECIFIC FIX
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.mobile-overlay');
    
    if (sidebar && overlay) {
        // Watch for sidebar state changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    // If sidebar is closing, force everything clickable
                    if (!sidebar.classList.contains('open') && window.innerWidth <= 768) {
                        setTimeout(() => {
                            document.querySelectorAll('button, select, input, a, .btn, [onclick]').forEach(el => {
                                if (!el.classList.contains('mobile-overlay')) {
                                    el.style.pointerEvents = 'auto !important';
                                    el.style.touchAction = 'manipulation !important';
                                }
                            });
                        }, 100);
                    }
                }
            });
        });
        
        observer.observe(sidebar, { attributes: true });
    }
});