// Authentication Pages JavaScript

// Password Toggle Function
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(inputId + '-toggle-icon');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
    }
}

// Form Validation and Animations
document.addEventListener('DOMContentLoaded', function() {
    // Add input animations
    const inputs = document.querySelectorAll('.form-control-auth');
    inputs.forEach(input => {
        // Focus animation
        input.addEventListener('focus', function() {
            this.parentElement.parentElement.classList.add('focused');
            this.style.transform = 'scale(1.02)';
        });
        
        // Blur animation
        input.addEventListener('blur', function() {
            this.parentElement.parentElement.classList.remove('focused');
            this.style.transform = 'scale(1)';
            validateField(this);
        });
        
        // Input animation
        input.addEventListener('input', function() {
            if (this.value) {
                this.parentElement.parentElement.classList.add('has-value');
            } else {
                this.parentElement.parentElement.classList.remove('has-value');
            }
        });
    });
    
    // Form submission loading state
    const forms = document.querySelectorAll('.auth-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('.btn-auth-submit');
            const btnText = submitBtn.querySelector('.btn-text');
            
            // Add loading state
            submitBtn.classList.add('loading');
            btnText.textContent = 'Processing...';
            submitBtn.disabled = true;
            
            // Validate form before submit
            let isValid = true;
            const requiredInputs = form.querySelectorAll('[required]');
            requiredInputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                submitBtn.classList.remove('loading');
                btnText.textContent = submitBtn.closest('form').id === 'register-form' ? 'Create Account' : 'Login';
                submitBtn.disabled = false;
            }
        });
    });
    
    // Real-time password strength checker for registration
    const password1Input = document.getElementById('password1');
    const password2Input = document.getElementById('password2');
    
    if (password1Input) {
        password1Input.addEventListener('input', function() {
            checkPasswordStrength(this.value);
        });
    }
    
    if (password2Input && password1Input) {
        password2Input.addEventListener('input', function() {
            checkPasswordMatch(password1Input.value, this.value);
        });
    }
    
    // Animate form fields on page load
    const formGroups = document.querySelectorAll('.form-group-auth');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        setTimeout(() => {
            group.style.transition = 'all 0.5s ease';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn-auth-submit');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Validate individual field
function validateField(input) {
    const formGroup = input.parentElement.parentElement;
    const value = input.value.trim();
    
    // Remove previous error states
    formGroup.classList.remove('error', 'success');
    const existingError = formGroup.querySelector('.error-message');
    if (existingError && existingError.parentElement === formGroup) {
        existingError.remove();
    }
    
    // Check if required field is empty
    if (input.hasAttribute('required') && !value) {
        formGroup.classList.add('error');
        showFieldError(formGroup, 'This field is required');
        return false;
    }
    
    // Email validation
    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            formGroup.classList.add('error');
            showFieldError(formGroup, 'Please enter a valid email address');
            return false;
        }
    }
    
    // Phone validation
    if (input.type === 'tel' && value) {
        const phoneRegex = /^[\d\s\-\+\(\)]+$/;
        if (!phoneRegex.test(value) || value.length < 10) {
            formGroup.classList.add('error');
            showFieldError(formGroup, 'Please enter a valid phone number');
            return false;
        }
    }
    
    // Username validation
    if (input.name === 'username' && value) {
        if (value.length < 3) {
            formGroup.classList.add('error');
            showFieldError(formGroup, 'Username must be at least 3 characters');
            return false;
        }
        if (!/^[a-zA-Z0-9_]+$/.test(value)) {
            formGroup.classList.add('error');
            showFieldError(formGroup, 'Username can only contain letters, numbers, and underscores');
            return false;
        }
    }
    
    // Success state
    if (value) {
        formGroup.classList.add('success');
    }
    
    return true;
}

// Show field error message
function showFieldError(formGroup, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `<i class="bi bi-exclamation-circle"></i> ${message}`;
    formGroup.appendChild(errorDiv);
}

// Check password strength
function checkPasswordStrength(password) {
    const formGroup = document.getElementById('password1').parentElement.parentElement;
    let strength = 0;
    let feedback = [];
    
    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');
    
    if (/[a-z]/.test(password)) strength++;
    else feedback.push('lowercase letter');
    
    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('uppercase letter');
    
    if (/[0-9]/.test(password)) strength++;
    else feedback.push('number');
    
    if (/[^a-zA-Z0-9]/.test(password)) strength++;
    else feedback.push('special character');
    
    // Remove existing strength indicator
    const existingIndicator = formGroup.querySelector('.password-strength');
    if (existingIndicator) {
        existingIndicator.remove();
    }
    
    if (password && feedback.length > 0) {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength';
        indicator.style.marginTop = '8px';
        indicator.style.fontSize = '0.85rem';
        indicator.style.color = '#666';
        indicator.innerHTML = `<i class="bi bi-info-circle"></i> Password should contain: ${feedback.join(', ')}`;
        formGroup.appendChild(indicator);
    }
}

// Check if passwords match
function checkPasswordMatch(password1, password2) {
    const formGroup = document.getElementById('password2').parentElement.parentElement;
    
    if (password2 && password1 !== password2) {
        formGroup.classList.add('error');
        if (!formGroup.querySelector('.error-message')) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.innerHTML = '<i class="bi bi-exclamation-circle"></i> Passwords do not match';
            formGroup.appendChild(errorDiv);
        }
        return false;
    } else if (password2 && password1 === password2) {
        formGroup.classList.remove('error');
        formGroup.classList.add('success');
        const errorMsg = formGroup.querySelector('.error-message');
        if (errorMsg) {
            errorMsg.remove();
        }
        return true;
    }
    
    return true;
}

// Add smooth scroll to form errors
function scrollToFirstError() {
    const firstError = document.querySelector('.form-group-auth.error');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        const input = firstError.querySelector('.form-control-auth');
        if (input) {
            input.focus();
        }
    }
}

// Check for existing errors on page load and scroll to them
window.addEventListener('load', function() {
    setTimeout(scrollToFirstError, 500);
});

