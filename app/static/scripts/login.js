document.getElementById('login-form').addEventListener('submit', async function(event) {
    event.preventDefault(); 
    const form = event.target;
    const formData = new FormData(form);
    const data = {
        email: formData.get('email'),
        password: formData.get('password')
    };
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            window.location.href = "/"; 
        } else {
            const error = await response.json();
            alert(error.detail || "Неверный логин или пароль. Попробуйте еще раз.");
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert("Произошла ошибка. Попробуйте еще раз.");
    }
});