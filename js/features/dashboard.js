// ---------- DASHBOARD ----------

async function loadDashboardOverview() {
  try {
    const data = await apiFetch('/api/dashboard/overview', { headers: authHeaders() });
    document.getElementById('metricAtsScore').textContent = data.ats_score;
    document.getElementById('metricAtsBar').style.width = data.ats_score + '%';
    document.getElementById('metricJobMatches').textContent = data.job_matches;
    document.getElementById('metricApplicationsSent').textContent = data.applications_sent;
    document.getElementById('metricInterviews').textContent = data.interviews_scheduled;
  } catch (err) {
    showToast('Could not reach server — showing cached dashboard data.', 'error');
  }
}
