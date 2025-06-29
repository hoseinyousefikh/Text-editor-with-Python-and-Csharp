// ثابت‌ها
const TEXT_API_URL = "https://localhost:7044/api/texts";

// پس از بارگیری صفحه
document.addEventListener('DOMContentLoaded', () => {
    const saveBtn = document.getElementById('saveBtn');
    const messageDiv = document.getElementById('message');

    if (saveBtn) {
        saveBtn.addEventListener('click', saveText);
    }
});

// ذخیره متن
async function saveText() {
    const content = document.getElementById('content').value;
    const token = localStorage.getItem('authToken');
    const messageDiv = document.getElementById('message');

    if (!token) {
        messageDiv.textContent = 'لطفاً ابتدا وارد شوید';
        messageDiv.className = 'message error';
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);
        return;
    }

    if (!content.trim()) {
        messageDiv.textContent = 'لطفاً متنی برای ذخیره وارد کنید';
        messageDiv.className = 'message error';
        return;
    }

    try {
        const response = await fetch(TEXT_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ content })
        });

        const result = await response.json();

        if (response.ok) {
            messageDiv.textContent = 'متن با موفقیت ذخیره شد!';
            messageDiv.className = 'message success';
            document.getElementById('content').value = '';
        } else {
            messageDiv.textContent = result.error || 'خطا در ذخیره متن';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'خطا در ارتباط با سرور';
        messageDiv.className = 'message error';
        console.error('Save text error:', error);
    }
}