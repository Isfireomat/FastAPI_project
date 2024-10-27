function logout() {
    fetch('/api/logout', {  
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: 'logout' }) 
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/login';  // Перенаправление после успешного выхода
        } else {
            console.error('Ошибка при выходе');
        }
    })
    .catch(error => console.error('Ошибка:', error)); 
}