document.getElementById('registration-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Отключаем стандартную отправку формы

    const form = event.target;
    const formData = new FormData(form);

    // Преобразуем данные формы в объект
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        password: formData.get('password')
    };

    try {
        const response = await fetch('/api/register/', {
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
            console.error('Ошибка регистрации:', error);
            alert(error.detail || "Ошибка регистрации. Попробуйте еще раз.");
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert("Произошла ошибка. Попробуйте еще раз.");
    }
});
