function getToken() {
  return localStorage.getItem('resumeai_token');
}

function setToken(token) {
  localStorage.setItem('resumeai_token', token);
}

function clearToken() {
  localStorage.removeItem('resumeai_token');
}

function authHeaders() {
  const token = getToken();
  return token ? { 'Authorization': 'Bearer ' + token } : {};
}

async function apiFetch(path, options = {}) {
  const res = await fetch(API_BASE + path, options);
  if (!res.ok) {
    let detail = res.statusText;
    try { const body = await res.json(); detail = body.detail || detail; } catch (e) {}
    const err = new Error(detail || ('Request failed: ' + res.status));
    err.status = res.status;
    throw err;
  }
  return res.json();
}
