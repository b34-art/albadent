// Reemplaza TODO el event listener del formulario con esto:
document.getElementById('login-form')?.addEventListener('submit', (e) => {
  e.preventDefault();
  
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  // Demo credentials (solo para pruebas)
  if (email === 'admin@albadent.com' && password === 'admin123') {
    localStorage.setItem('demoToken', 'demo-only-not-secure');
    alert('✅ Login exitoso (modo demo)');
    window.location.href = './dashboard/index.html';
  } else if (email === 'recepcion@albadent.com' && password === 'recep123') {
    localStorage.setItem('demoToken', 'demo-only-not-secure');
    alert('✅ Login exitoso (modo demo)');
    window.location.href = './dashboard/index.html';
  } else {
    alert('❌ Credenciales incorrectas');
  }
});
const res = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
