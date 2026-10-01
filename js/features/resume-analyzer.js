// ---------- RESUME ANALYZER ----------

function handleResumeFileSelected(event) {
  const file = event.target.files && event.target.files[0];
  if (file) runResumeAnalysis(file);
}

function handleResumeDrop(event) {
  event.preventDefault();
  event.currentTarget.classList.remove('drag');
  const file = event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0];
  if (file) runResumeAnalysis(file);
}

function startAnalysis() {
  // "Demo" button — generates a small sample text file and runs it through
  // the real analysis endpoint instead of faking results client-side.
  const sampleText = 'Experienced software engineer skilled in React, JavaScript, Node.js, REST API, Git, CSS. ' +
    'Led development of scalable web applications. Improved performance by 35%. Bachelor degree in Computer Science.';
  const file = new File([sampleText], 'sample_resume.txt', { type: 'text/plain' });
  runResumeAnalysis(file);
}

async function runResumeAnalysis(file) {
  document.getElementById('analyzerUpload').style.display = 'none';
  document.getElementById('analyzerLoading').style.display = 'block';
  document.getElementById('analyzerResult').style.display = 'none';

  try {
    const formData = new FormData();
    formData.append('file', file);
    const result = await apiFetch('/api/resumes/upload', {
      method: 'POST',
      headers: authHeaders(),
      body: formData,
    });
    renderAnalysisResult(result);
  } catch (err) {
    showToast(err.message === 'Could not validate credentials' || err.status === 401
      ? 'Please log in to analyze your resume.'
      : 'Could not reach server — showing sample analysis instead.', 'error');
    renderAnalysisResult({
      ats_score: 87, formatting_score: 91, keywords_score: 74, experience_score: 88, education_score: 95,
      found_keywords: ['React','JavaScript','Node.js','REST API','Git','CSS'],
      missing_keywords: ['TypeScript','Docker','GraphQL','AWS','CI/CD'],
      suggestions: [
        'Add quantified achievements (e.g., "Reduced load time by 40%") to 3 bullet points.',
        'Your summary is too generic. Tailor it to target role using keywords from job descriptions.',
        'Great use of action verbs! Keep using "developed", "implemented", "led".',
      ],
    });
  } finally {
    document.getElementById('analyzerLoading').style.display = 'none';
    document.getElementById('analyzerResult').style.display = 'block';
  }
}

function renderAnalysisResult(result) {
  document.getElementById('scoreFormatting').textContent = result.formatting_score;
  document.getElementById('scoreKeywords').textContent = result.keywords_score;
  document.getElementById('scoreExperience').textContent = result.experience_score;
  document.getElementById('scoreEducation').textContent = result.education_score;
  document.getElementById('scoreOverallText').textContent = result.ats_score;

  const circumference = 408.4;
  const offset = circumference - (circumference * result.ats_score / 100);
  document.getElementById('scoreRingFill').setAttribute('stroke-dashoffset', offset);

  const foundEl = document.getElementById('foundKeywordsCloud');
  foundEl.innerHTML = (result.found_keywords || []).map(k => `<span class="keyword found">${k}</span>`).join('') || '<span class="text-xs text-dim">None found</span>';

  const missingEl = document.getElementById('missingKeywordsCloud');
  missingEl.innerHTML = (result.missing_keywords || []).map(k => `<span class="keyword missing">${k}</span>`).join('') || '<span class="text-xs text-dim">None missing</span>';

  const suggestionsEl = document.getElementById('suggestionsList');
  suggestionsEl.innerHTML = (result.suggestions || []).map(s =>
    `<div class="suggestion"><i class="fa-solid fa-lightbulb color-amber"></i><p>${s}</p></div>`
  ).join('');
}

function resetAnalyzer() {
  document.getElementById('analyzerResult').style.display = 'none';
  document.getElementById('analyzerUpload').style.display = 'block';
}
