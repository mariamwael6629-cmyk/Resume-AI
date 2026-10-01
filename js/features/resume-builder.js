// ---------- RESUME BUILDER ----------

async function saveBuilderDraft() {
  const content = { html: document.getElementById('resumePaper').innerHTML };
  try {
    await apiFetch('/api/builder/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify({ content }),
    });
    showToast('Resume draft saved!', 'success');
  } catch (err) {
    showToast(err.status === 401 ? 'Please log in to save your draft.' : 'Could not reach server — draft not saved.', 'error');
  }
}

async function loadBuilderDraft() {
  try {
    const draft = await apiFetch('/api/builder', { headers: authHeaders() });
    if (draft && draft.content && draft.content.html) {
      document.getElementById('resumePaper').innerHTML = draft.content.html;
    }
  } catch (err) {
    // Silent — keep default preview content if no draft or backend unreachable.
  }
}
