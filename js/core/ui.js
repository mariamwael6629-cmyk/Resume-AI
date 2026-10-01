function goTo(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(page).classList.add('active');
  currentPage = page;
  window.scrollTo(0,0);
  // Update nav visibility
  const showNav = ['dashboard','analyzer','jobs','builder','admin'].includes(page);
  document.getElementById('navLinks').style.display = showNav ? 'flex' : '';
  // Close notif
  document.getElementById('notifDropdown').style.display = 'none';

  if (page === 'jobs') loadJobs();
  if (page === 'dashboard') loadDashboardOverview();
  if (page === 'builder') loadBuilderDraft();
  if (page === 'admin') loadAdminUsers();
}

async function loadAdminUsers() {
  const body = document.getElementById('adminUsersBody');
  try {
    const users = await apiFetch('/api/admin/users');
    if (!users.length) {
      body.innerHTML = '<tr><td colspan="5" class="text-dim text-center">No users yet</td></tr>';
      return;
    }
    body.innerHTML = users.map(u => `
      <tr>
        <td><div class="fw-600">${u.first_name || u.last_name ? (u.first_name + ' ' + u.last_name).trim() : 'Unnamed User'}</div></td>
        <td class="text-dim">${u.email}</td>
        <td class="text-dim">${u.resume_count}</td>
        <td class="text-dim">${new Date(u.created_at).toLocaleDateString()}</td>
        <td><span class="status-badge ${u.is_admin ? 'status-pending' : 'status-active'}">${u.is_admin ? 'Admin' : 'Active'}</span></td>
      </tr>
    `).join('');
  } catch (err) {
    body.innerHTML = '<tr><td colspan="5" class="text-dim text-center">Could not load users</td></tr>';
  }
}

function toggleTheme() {
  isLight = !isLight;
  document.body.classList.toggle('light', isLight);
  document.getElementById('themeIcon').className = isLight ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
}

function toggleLang() {
  currentLang = currentLang === 'EN' ? 'عربي' : 'EN';
  document.querySelector('.lang-badge').textContent = currentLang;
  showToast(currentLang === 'EN' ? 'Switched to English' : 'تم التبديل إلى العربية', 'success');
}

function toggleNotif() {
  const d = document.getElementById('notifDropdown');
  d.style.display = d.style.display === 'block' ? 'none' : 'block';
}

document.addEventListener('click', (e) => {
  if (!document.getElementById('notifBtn').contains(e.target)) {
    document.getElementById('notifDropdown').style.display = 'none';
  }
});

function toggleFaq(el) {
  el.classList.toggle('open');
}

function switchDash(view, el) {
  ['overview','analytics','applications','skills'].forEach(v => {
    const el2 = document.getElementById('dash-'+v);
    if(el2) el2.style.display = 'none';
  });
  document.getElementById('dash-'+view).style.display = 'block';
  document.querySelectorAll('#dashboard .sidebar-item').forEach(i => i.classList.remove('active'));
  el.classList.add('active');
}

function switchAdmin(view, el) {
  ['overview','users','resumes','jobs-admin','subs'].forEach(v => {
    const el2 = document.getElementById('admin-'+v);
    if(el2) el2.style.display = 'none';
  });
  document.getElementById('admin-'+view).style.display = 'block';
  document.querySelectorAll('#admin .sidebar-item').forEach(i => i.classList.remove('active'));
  el.classList.add('active');
}

function setFilter(el) {
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
}

function saveJob(btn, jobId) {
  const icon = btn.querySelector('i');
  if(icon.classList.contains('fa-regular')) {
    icon.className = 'fa-solid fa-bookmark';
    icon.style.color = 'var(--accent)';
    showToast('Job saved!', 'success');
    if (jobId !== undefined) saveJobToServer(jobId);
  } else {
    icon.className = 'fa-regular fa-bookmark';
    icon.style.color = '';
    showToast('Job removed from saved', '');
  }
}
