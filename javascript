// Solo para demo - NO usar en producción
document.getElementById('login-form')?.addEventListener('submit', (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  // Demo credentials
  if (email === 'admin@albadent.com' && password === 'admin123') {
    localStorage.setItem('demoToken', 'demo-only');
    window.location.href = '/dashboard/index.html';
  } else {
    alert('Credenciales incorrectas');
  }
});
const res = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
