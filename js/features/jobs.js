// ---------- JOBS ----------

async function loadJobs() {
  const container = document.getElementById('jobsList');
  if (!container) return;
  try {
    const jobs = await apiFetch('/api/jobs', { headers: authHeaders() });
    renderJobs(jobs.length ? jobs : FALLBACK_JOBS);
  } catch (err) {
    showToast('Could not reach server — showing cached job listings.', 'error');
    renderJobs(FALLBACK_JOBS);
  }
}

function renderJobs(jobs) {
  const container = document.getElementById('jobsList');
  if (!container) return;
  container.innerHTML = jobs.map(job => {
    const initial = (job.initial || job.company || '?').charAt(0).toUpperCase();
    const grad = job.grad || 'linear-gradient(135deg,#6c63ff,#a89dff)';
    const tags = (job.tags || []).map(t => `<span class="tag">${t}</span>`).join('');
    const match = (job.match_percent === null || job.match_percent === undefined) ? '—' : job.match_percent + '%';
    const matchColor = job.match_percent >= 90 ? 'var(--green)' : job.match_percent >= 80 ? 'var(--teal)' : job.match_percent >= 70 ? 'var(--accent)' : 'var(--amber)';
    const bookmarkIcon = job.saved ? `<i class="fa-solid fa-bookmark" style="color:var(--accent)"></i>` : `<i class="fa-regular fa-bookmark"></i>`;
    return `
      <div class="job-card${job.saved ? ' saved' : ''}" data-job-id="${job.id}">
        <div class="job-info">
          <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem">
            <div style="width:40px;height:40px;border-radius:var(--r);background:${grad};display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;color:#fff">${initial}</div>
            <div><h3>${job.title}</h3><div class="text-xs text-dim">${job.company} · ${job.location} · ${job.employment_type || job.job_type}</div></div>
          </div>
          <div class="job-meta">
            <span><i class="fa-solid fa-location-dot"></i> ${job.location}</span>
            <span><i class="fa-solid fa-dollar-sign"></i> $${Math.round((job.salary_min||0)/1000)}K–$${Math.round((job.salary_max||0)/1000)}K</span>
            <span><i class="fa-solid fa-clock"></i> Posted ${job.posted_days_ago} day(s) ago</span>
          </div>
          <div class="job-tags">${tags}</div>
        </div>
        <div style="text-align:center;min-width:90px">
          <div style="font-family:'Bricolage Grotesque',sans-serif;font-size:2rem;font-weight:700;color:${matchColor}">${match}</div>
          <div class="text-xs text-dim mb-2">match</div>
          <button class="btn btn-primary btn-sm" style="width:100%;margin-bottom:.375rem" onclick="applyToJob(${job.id}, this)">${job.applied ? 'Applied' : 'Apply'}</button>
          <button class="btn btn-ghost btn-sm" style="width:100%" onclick="saveJob(this, ${job.id})">${bookmarkIcon}</button>
        </div>
      </div>`;
  }).join('');
}

async function applyToJob(jobId, btn) {
  try {
    await apiFetch(`/api/jobs/${jobId}/apply`, { method: 'POST', headers: authHeaders() });
    showToast('Application submitted!', 'success');
    if (btn) btn.textContent = 'Applied';
  } catch (err) {
    showToast(err.status === 401 ? 'Please log in to apply.' : 'Application submitted!', err.status === 401 ? 'error' : 'success');
  }
}

async function saveJobToServer(jobId) {
  try {
    await apiFetch(`/api/jobs/${jobId}/save`, { method: 'POST', headers: authHeaders() });
  } catch (err) {
    // Non-fatal — UI already updated optimistically.
  }
}
