let toastTimeout;
function showToast(msg, type) {
  const tc = document.getElementById('toastContainer');
  const t = document.createElement('div');
  t.className = 'toast ' + type;
  const icon = type === 'success' ? '<i class="fa-solid fa-circle-check" style="color:var(--green)"></i>' : '<i class="fa-solid fa-circle-info" style="color:var(--accent)"></i>';
  t.innerHTML = icon + '<span>' + msg + '</span>';
  tc.appendChild(t);
  setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(100%)'; t.style.transition = 'all .3s'; setTimeout(() => t.remove(), 300); }, 3000);
}
