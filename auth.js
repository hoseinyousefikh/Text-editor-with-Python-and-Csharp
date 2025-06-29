// 1. استفاده از HTTP در محیط توسعه
const AUTH_API_URL = "http://localhost:5000";

// 2. تابع مشترک برای مدیریت فرم‌ها
async function handleForm(endpoint, formData) {
    try {
        const response = await fetch(`${AUTH_API_URL}/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        // بررسی وضعیت HTTP
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `خطای سرور: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`${endpoint} error:`, error);
        throw error;
    }
}

// 3. مدیریت ثبت نام
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorElement = document.getElementById('error');
    errorElement.textContent = '';

    try {
        const formData = {
            first_name: document.getElementById('firstName').value,
            last_name: document.getElementById('lastName').value,
            age: parseInt(document.getElementById('age').value),
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            confirm_password: document.getElementById('confirmPassword').value
        };

        await handleForm('register', formData);
        alert('ثبت نام با موفقیت انجام شد! لطفاً وارد شوید.');
        window.location.href = 'login.html';

    } catch (error) {
        errorElement.textContent = error.message;
    }
});

// 4. مدیریت ورود
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const errorElement = document.getElementById('error');
    errorElement.textContent = '';

    try {
        const formData = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };

        const result = await handleForm('login', formData);
        localStorage.setItem('authToken', result.token);
        window.location.href = 'text-editor.html';

    } catch (error) {
        errorElement.textContent = error.message;
    }
});