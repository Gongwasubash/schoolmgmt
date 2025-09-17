// Smooth scrolling for navigation links
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

// Show login modal
function showLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

// Close login modal
function closeLogin() {
    document.getElementById('loginModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('loginModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Handle login form submission
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const userType = document.getElementById('userType').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Simple validation
    if (!username || !password) {
        alert('Please fill in all fields');
        return;
    }
    
    // Simulate login process
    showLoadingState();
    
    setTimeout(() => {
        hideLoadingState();
        alert(`Login successful! Welcome ${username} (${userType})`);
        closeLogin();
        
        // Redirect based on user type
        redirectUser(userType);
    }, 1500);
});

// Show demo functionality
function showDemo() {
    alert('Demo feature coming soon! This will showcase the system capabilities.');
}

// Scroll to features section
function scrollToFeatures() {
    document.getElementById('features').scrollIntoView({
        behavior: 'smooth'
    });
}

// Loading state for login
function showLoadingState() {
    const submitBtn = document.querySelector('#loginForm button[type="submit"]');
    submitBtn.textContent = 'Logging in...';
    submitBtn.disabled = true;
}

function hideLoadingState() {
    const submitBtn = document.querySelector('#loginForm button[type="submit"]');
    submitBtn.textContent = 'Login';
    submitBtn.disabled = false;
}

// Redirect user based on type
function redirectUser(userType) {
    const dashboards = {
        admin: 'admin-dashboard.html',
        teacher: 'teacher-dashboard.html',
        student: 'student-dashboard.html',
        parent: 'parent-dashboard.html'
    };
    
    console.log(`Redirecting to ${dashboards[userType]}`);
    // In a real application, you would redirect to the appropriate dashboard
    // window.location.href = dashboards[userType];
}

// Animate feature cards on scroll
function animateOnScroll() {
    const cards = document.querySelectorAll('.feature-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s, transform 0.6s';
        observer.observe(card);
    });
}

// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    animateOnScroll();
    
    // Add active class to navbar on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(44, 62, 80, 0.95)';
        } else {
            navbar.style.background = '#2c3e50';
        }
    });
});