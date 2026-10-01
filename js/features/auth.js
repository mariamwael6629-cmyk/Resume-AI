// ---------- AUTH ----------

async function doLogin() {
  const email = (document.getElementById('loginEmail').value || '').trim();
  const password = document.getElementById('loginPassword').value || '';

  if (!email || !password) {
    showToast('Please enter both email and password.', 'error');
    return;
  }

  showToast('Signing in...', 'success');
  try {
    const result = await apiFetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    setToken(result.access_token);
    showToast('Welcome back!', 'success');
    goTo('dashboard');
  } catch (err) {
    showToast('Login failed: ' + (err.message || 'Could not reach server.'), 'error');
  }
}

async function doRegister() {
  const firstName = (document.getElementById('registerFirstName').value || '').trim();
  const lastName = (document.getElementById('registerLastName').value || '').trim();
  const email = (document.getElementById('registerEmail').value || '').trim();
  const password = document.getElementById('registerPassword').value || '';

  if (!email || !password) {
    showToast('Please enter both email and password.', 'error');
    return;
  }
  if (password.length < 6) {
    showToast('Password must be at least 6 characters.', 'error');
    return;
  }

  showToast('Creating your account...', 'success');
  try {
    const result = await apiFetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, first_name: firstName, last_name: lastName }),
    });
    setToken(result.access_token);
    showToast('Account created!', 'success');
    goTo('dashboard');
  } catch (err) {
    showToast('Registration failed: ' + (err.message || 'Could not reach server.'), 'error');
  }
}
