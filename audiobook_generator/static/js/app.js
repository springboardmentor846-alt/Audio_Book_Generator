
const S = {
  file:        null,
  text:        '',
  script:      '',
  lang:        'English',
  summary:     null,
  quiz:        null,
  quizAnswers: [],
  evaluation:  null,
  bookmarks:   JSON.parse(localStorage.getItem('am_bm') || '[]'),
  speaking:    false,
  muted:       false,
  ttsUtt:      null
};

window.addEventListener('DOMContentLoaded', () => {
  renderBookmarks();
});

/*FILE HANDLING */
function handleDragOver(e) {
  e.preventDefault();
  document.getElementById('dropzone').classList.add('drag-over');
}
function handleDragLeave() {
  document.getElementById('dropzone').classList.remove('drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('dropzone').classList.remove('drag-over');
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
}
function handleFileSelect(e) {
  if (e.target.files[0]) setFile(e.target.files[0]);
}

function setFile(file) {
  const ext = file.name.split('.').pop().toLowerCase();
  if (!['pdf', 'txt', 'docx', 'doc'].includes(ext)) {
    showToast('Only PDF, DOCX or TXT allowed', 'error');
    return;
  }
  S.file = file;
  document.getElementById('selectedName').textContent = file.name;
  document.getElementById('fileSelected').classList.remove('d-none');
  showToast('File ready: ' + file.name, 'success');
}

function clearFile(e) {
  e.stopPropagation();
  S.file = null;
  document.getElementById('fileInput').value = '';
  document.getElementById('fileSelected').classList.add('d-none');
}

/* GENERATE AUDIOBOOK*/
async function generateAudiobook() {
  if (!S.file) { showToast('Upload a file first', 'error'); return; }

  S.lang = document.getElementById('languageSelect').value;
  S.summary = null; S.quiz = null; S.evaluation = null; S.quizAnswers = [];

  const btn = document.getElementById('generateBtn');
  btn.disabled = true;
  btn.textContent = 'Generating…';
  showProg('Uploading file…', 15);

  const fd = new FormData();
  fd.append('file', S.file);
  fd.append('language', S.lang);

  try {
    setProg(40, 'Sending to Groq AI…');
    const res  = await fetch('/api/generate-audiobook', { method: 'POST', body: fd });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Generation failed');

    S.script = data.script;
    S.text   = data.original_text;

    setProg(100, 'Done!');
    setTimeout(hideProg, 600);
    renderPlayer();
    showToast('Audiobook generated!', 'success');

  } catch (err) {
    hideProg();
    showToast('Error: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate Podcast Audiobook';
  }
}

function showProg(msg, pct) {
  document.getElementById('genProg').classList.remove('d-none');
  setProg(pct, msg);
}
function setProg(pct, msg) {
  document.getElementById('genProgBar').style.width   = pct + '%';
  if (msg) document.getElementById('genProgLabel').textContent = msg;
}
function hideProg() {
  document.getElementById('genProg').classList.add('d-none');
  document.getElementById('genProgBar').style.width = '0%';
}

/* RENDER PLAYER */
function renderPlayer() {
  document.getElementById('abEmpty').classList.add('d-none');
  document.getElementById('abPlayer').classList.remove('d-none');
  document.getElementById('scriptText').textContent = S.script;

  // Unlock Q&A
  document.getElementById('qaEmpty').classList.add('d-none');
  document.getElementById('qaContent').classList.remove('d-none');

  initTTS();
}

/* TEXT-TO-SPEECH */
function initTTS() {
  window.speechSynthesis.cancel();
  S.speaking = false;
  updatePlayIcon(false);
  document.getElementById('pbFilled').style.width = '0%';
  document.getElementById('pbThumb').style.left   = '0%';
  document.getElementById('curTime').textContent  = '00:00';
  const mins = Math.max(1, Math.round(S.script.split(' ').length / 140));
  document.getElementById('totTime').textContent  = pad(mins) + ':00';
}

function pad(n) { return n < 10 ? '0' + n : '' + n; }

function togglePlay() {
  if (S.speaking) {
    window.speechSynthesis.pause();
    S.speaking = false;
    updatePlayIcon(false);
  } else {
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
      S.speaking = true;
      updatePlayIcon(true);
    } else {
      startTTS();
    }
  }
}

function startTTS() {
  window.speechSynthesis.cancel();
  const clean = S.script
    .replace(/\[PAUSE\]/g, '… ')
    .replace(/\[EMPHASIS\]/g, '')
    .replace(/\[TRANSITION\]/g, '… ');

  S.ttsUtt = new SpeechSynthesisUtterance(clean);
  S.ttsUtt.lang   = langCode(S.lang);
  S.ttsUtt.rate   = parseFloat(document.querySelector('.pb-speed-sel')?.value || 1);
  S.ttsUtt.volume = S.muted ? 0 : 1;

  const totalWords = clean.split(' ').length;
  let wordsDone = 0;

  S.ttsUtt.onboundary = (e) => {
    if (e.name !== 'word') return;
    wordsDone++;
    const pct = Math.min(100, wordsDone / totalWords * 100);
    document.getElementById('pbFilled').style.width = pct + '%';
    document.getElementById('pbThumb').style.left   = pct + '%';
    const secs = Math.round(wordsDone / 140 * 60);
    document.getElementById('curTime').textContent =
      pad(Math.floor(secs / 60)) + ':' + pad(secs % 60);
  };

  S.ttsUtt.onend = () => {
    S.speaking = false;
    updatePlayIcon(false);
    document.getElementById('pbFilled').style.width = '100%';
  };

  S.ttsUtt.onerror = () => { S.speaking = false; updatePlayIcon(false); };

  window.speechSynthesis.speak(S.ttsUtt);
  S.speaking = true;
  updatePlayIcon(true);
}

function updatePlayIcon(playing) {
  document.getElementById('playIcon').className =
    playing ? 'bi bi-pause-fill' : 'bi bi-play-fill';
}

function seekAudio(e) {
  const track = document.getElementById('pbTrack');
  const pct = Math.max(0, Math.min(1,
    (e.clientX - track.getBoundingClientRect().left) / track.offsetWidth));
  document.getElementById('pbFilled').style.width = (pct * 100) + '%';
  document.getElementById('pbThumb').style.left   = (pct * 100) + '%';
}

function toggleMute() {
  S.muted = !S.muted;
  if (S.ttsUtt) S.ttsUtt.volume = S.muted ? 0 : 1;
  document.getElementById('volIcon').className =
    S.muted ? 'bi bi-volume-mute-fill' : 'bi bi-volume-up-fill';
}

function langCode(l) {
  return { English:'en-US', Spanish:'es-ES', French:'fr-FR', German:'de-DE',
           Hindi:'hi-IN', Portuguese:'pt-BR', Arabic:'ar-SA',
           Japanese:'ja-JP', Chinese:'zh-CN', Italian:'it-IT' }[l] || 'en-US';
}

/*DOWNLOAD / COPY */
function downloadScript() {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([S.script], { type: 'text/plain' }));
  a.download = 'audiobook-script.txt';
  a.click();
  showToast('Downloaded!', 'success');
}

function copyScript() {
  navigator.clipboard.writeText(S.script)
    .then(() => showToast('Copied!', 'success'))
    .catch(() => showToast('Copy failed', 'error'));
}

/* SUMMARY*/
async function loadSummary(force = false) {
  if (!S.text) return;
  if (S.summary && !force) { showSummary(); return; }

  document.getElementById('sumEmpty').classList.add('d-none');
  document.getElementById('sumContent').classList.remove('d-none');
  document.getElementById('sumBody').innerHTML = '<div class="shimmer"></div>';

  try {
    const res  = await fetch('/api/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: S.text, language: S.lang })
    });
    const d = await res.json();
    if (!res.ok) throw new Error(d.error);
    S.summary = d.summary;
    showSummary();
  } catch (err) {
    document.getElementById('sumBody').innerHTML =
      `<p style="color:#ef4444;text-align: left" >Error: ${err.message}</p>`;
  }
}

function showSummary() {
  document.getElementById('sumEmpty').classList.add('d-none');
  document.getElementById('sumContent').classList.remove('d-none');
  document.getElementById('sumBody').innerHTML = mdToHtml(S.summary);
}

function mdToHtml(t) {
  return t
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm,  '<h2>$1</h2>')
    .replace(/^# (.+)$/gm,   '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,     '<em>$1</em>')
    .replace(/^[-•] (.+)$/gm,  '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)+/g, m => '<ul>' + m + '</ul>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(?!<)/gm, '<p>')
    .replace(/$(?!>)/gm, '</p>')
    .replace(/<p><\/p>/g, '');
}

/* Q&A */
async function askQuestion() {
  const inp = document.getElementById('qaInput');
  const q   = inp.value.trim();
  if (!q || !S.text) return;
  inp.value = '';

  addBubble('user', escHtml(q));
  const thinkEl = addBubble('ai', '<em style="color:#9ca3af">Thinking…</em>');

  try {
    const res = await fetch('/api/generate-qa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: S.text, question: q, language: S.lang })
    });
    const d = await res.json();
    if (!res.ok) throw new Error(d.error);
    thinkEl.querySelector('.qa-txt').innerHTML = d.answer.replace(/\n/g, '<br>');
  } catch (err) {
    thinkEl.querySelector('.qa-txt').innerHTML =
      `<span style="color:#ef4444">Error: ${err.message}</span>`;
  }

  const chat = document.getElementById('qaChat');
  chat.scrollTop = chat.scrollHeight;
}

function quickAsk(q) {
  document.getElementById('qaInput').value = q;
  askQuestion();
}

function addBubble(role, html) {
  const chat = document.getElementById('qaChat');
  const div  = document.createElement('div');
  div.className = 'qa-bubble ' + role;
  div.innerHTML = `
    <div class="qa-av">
      <i class="bi bi-${role === 'user' ? 'person-fill' : 'cpu-fill'}"></i>
    </div>
    <div class="qa-txt">${html}</div>`;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

/* QUIZ*/
async function loadQuiz(force = false) {
  if (!S.text) return;
  if (S.quiz && !force) { renderQuiz(); return; }

  document.getElementById('quizEmpty').classList.add('d-none');
  document.getElementById('quizContent').classList.remove('d-none');
  document.getElementById('quizBody').innerHTML =
    '<div class="shimmer" style="height:200px"></div>';
  document.getElementById('quizScore').classList.add('d-none');

  try {
    const res = await fetch('/api/generate-quiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: S.text, language: S.lang })
    });
    const d = await res.json();
    if (!res.ok) throw new Error(d.error);
    S.quiz = d.quiz;
    S.quizAnswers = new Array(S.quiz.length).fill(null);
    renderQuiz();
  } catch (err) {
    document.getElementById('quizBody').innerHTML =
      `<p style="color:#ef4444">Error: ${err.message}</p>`;
  }
}

function renderQuiz() {
  document.getElementById('quizEmpty').classList.add('d-none');
  document.getElementById('quizContent').classList.remove('d-none');
  document.getElementById('quizScore').classList.add('d-none');
  S.quizAnswers = new Array(S.quiz.length).fill(null);

  const letters = ['A','B','C','D'];
  let html = S.quiz.map((q, qi) => `
    <div class="quiz-qcard" id="qqc${qi}">
      <div class="quiz-qnum">Question ${qi + 1} of ${S.quiz.length}</div>
      <div class="quiz-qtext">${escHtml(q.question)}</div>
      <div class="quiz-opts">
        ${q.options.map((opt, oi) => `
          <button class="quiz-opt" onclick="pickAnswer(${qi},${oi})" id="qo${qi}-${oi}">
            <span class="qletter">${letters[oi]}</span>
            ${escHtml(opt)}
          </button>`).join('')}
      </div>
      <div class="quiz-exp" id="qex${qi}">${escHtml(q.explanation)}</div>
    </div>`).join('');

  html += `<button class="quiz-submit" onclick="submitQuiz()">
             <i class="bi bi-check-circle-fill me-2"></i>Submit Answers
           </button>`;
  document.getElementById('quizBody').innerHTML = html;
}

function pickAnswer(qi, oi) {
  if (S.quizAnswers[qi] !== null) return;
  S.quizAnswers[qi] = oi;
  const correct = S.quiz[qi].correct;
  for (let i = 0; i < 4; i++) {
    const btn = document.getElementById(`qo${qi}-${i}`);
    if (!btn) continue;
    btn.disabled = true;
    if (i === correct)         btn.classList.add('correct');
    else if (i === oi)         btn.classList.add('wrong');
  }
  document.getElementById('qex' + qi).classList.add('show');
}

function submitQuiz() {
  S.quiz.forEach((_, qi) => {
    if (S.quizAnswers[qi] === null) { S.quizAnswers[qi] = -1; pickAnswer(qi, -1); }
  });

  const got   = S.quizAnswers.filter((a, i) => a === S.quiz[i].correct).length;
  const total = S.quiz.length;
  const pct   = Math.round(got / total * 100);

  const box = document.getElementById('quizScore');
  box.classList.remove('d-none');
  box.innerHTML = `
    <div class="quiz-score-num">${got}/${total}</div>
    <div class="quiz-score-lbl">Your Score — ${pct}%</div>
    <div class="quiz-score-fb">
      ${pct >= 80 ? '🎉 Excellent comprehension!'
        : pct >= 60 ? '👍 Good — review the explanations.'
        : '📚 Keep reading to improve your score.'}
    </div>`;

  document.querySelector('.quiz-submit').remove();
  box.scrollIntoView({ behavior: 'smooth' });

  S.quizAnswers = S.quizAnswers.map((a, i) => ({ correct: a === S.quiz[i].correct }));
}

/*BOOKMARKS */
function addBookmark() {
  if (!S.script) { showToast('No content to bookmark', 'error'); return; }
  const sel  = window.getSelection()?.toString().trim();
  const text = sel || S.script.substring(0, 200) + '…';
  const bm   = { id: Date.now(), text, time: new Date().toLocaleString(), file: S.file?.name || '—' };
  S.bookmarks.unshift(bm);
  localStorage.setItem('am_bm', JSON.stringify(S.bookmarks));
  renderBookmarks();
  showToast('Bookmark saved!', 'success');
}

function deleteBookmark(id) {
  S.bookmarks = S.bookmarks.filter(b => b.id !== id);
  localStorage.setItem('am_bm', JSON.stringify(S.bookmarks));
  renderBookmarks();
}

function clearBookmarks() {
  S.bookmarks = [];
  localStorage.setItem('am_bm', '[]');
  renderBookmarks();
  showToast('Bookmarks cleared', 'info');
}

function renderBookmarks() {
  const list = document.getElementById('bkList');
  if (!S.bookmarks.length) {
    list.innerHTML = `
      <div class="empty-state">
        <i class="bi bi-bookmark empty-ico"></i>
        <p>No bookmarks yet. Select text in the Audiobook tab and click <strong>Bookmark</strong>.</p>
      </div>`;
    return;
  }
  list.innerHTML = S.bookmarks.map(b => `
    <div class="bk-item">
      <div class="bk-meta"><i class="bi bi-clock me-1"></i>${b.time} &nbsp;·&nbsp; ${escHtml(b.file)}</div>
      <div class="bk-text">${escHtml(b.text)}</div>
      <button class="bk-del" onclick="deleteBookmark(${b.id})"><i class="bi bi-x-lg"></i></button>
    </div>`).join('');
}

/* EVALUATION */
async function loadEvaluation(force = false) {
  if (!S.text || !S.script) {
    showToast('Generate audiobook first', 'error');
    return;
  }

  if (S.evaluation && !force) {
    renderEval();
    return;
  }

  document.getElementById('evalEmpty').classList.add('d-none');
  document.getElementById('evalContent').classList.remove('d-none');
  document.getElementById('evalBody').innerHTML =
    '<div class="shimmer" style="height:280px"></div>';

  try {
    const res = await fetch('/api/evaluate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        original_text: S.text,   
        script: S.script,        
        language: S.lang
      })
    });

    const d = await res.json();
    if (!res.ok) throw new Error(d.error);

    S.evaluation = d.evaluation;
    renderEval();

  } catch (err) {
    document.getElementById('evalBody').innerHTML =
      `<p style="color:#ef4444">Error: ${err.message}</p>`;
  }
}

function renderEval() {
  const e = S.evaluation;
  document.getElementById('evalEmpty').classList.add('d-none');
  document.getElementById('evalContent').classList.remove('d-none');

  const acc  = e.accuracy_score;
  const comp = e.comprehension_score;
  const diff = e.difficulty_score    || 5;

  const c = (v) => v >= 70 ? '#22c55e' : v >= 50 ? '#eab308' : '#ef4444';

  document.getElementById('evalBody').innerHTML = `
    <div class="eval-grid">
      <div class="eval-metric">
        <div class="eval-val" style="color:${c(acc)}">${acc}%</div>
        <div class="eval-lbl">Accuracy</div>
        <div class="eval-sub">${e.topic_coverage || 'Good'}</div>
      </div>
      <div class="eval-metric">
        <div class="eval-val" style="color:${c(comp)}">${comp}%</div>
        <div class="eval-lbl">Comprehension</div>
        <div class="eval-sub">${e.readability || 'General'}</div>
      </div>
      <div class="eval-metric">
        <div class="eval-val" style="color:#1a6fd4;font-size:1.3rem;margin-top:6px">${e.difficulty_level || 'Intermediate'}</div>
        <div class="eval-lbl" style="margin-top:4px">Difficulty</div>
        <div class="diff-bar"><div class="diff-fill" style="width:${diff * 10}%"></div></div>
        <div class="eval-sub">${diff}/10</div>
      </div>
      <div class="eval-metric">
        <div class="eval-val" style="color:#64748b;font-size:1.2rem;margin-top:6px">${e.vocabulary_complexity || 'Moderate'}</div>
        <div class="eval-lbl" style="margin-top:4px">Vocabulary</div>
        <div class="eval-sub">${e.readability || ''}</div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-4">
        <div class="eval-sec">
          <div class="eval-sec-title">
            <i class="bi bi-lightbulb-fill text-warning me-1"></i>Recommendations
          </div>
          ${(e.recommendations || []).map(r => `
            <div class="eval-row">
              <i class="bi bi-arrow-right-circle-fill text-primary"></i>
              <span>${escHtml(r)}</span>
            </div>`).join('')}
        </div>
      </div>
      <div class="col-md-4">
        <div class="eval-sec">
          <div class="eval-sec-title">
            <i class="bi bi-check-circle-fill text-success me-1"></i>Strengths
          </div>
          ${(e.strengths || []).map(s => `
            <div class="eval-row">
              <i class="bi bi-check-lg text-success"></i>
              <span>${escHtml(s)}</span>
            </div>`).join('')}
        </div>
      </div>
      <div class="col-md-4">
        <div class="eval-sec">
          <div class="eval-sec-title">
            <i class="bi bi-exclamation-circle-fill text-danger me-1"></i>Areas to Improve
          </div>
          ${(e.areas_for_improvement || []).map(a => `
            <div class="eval-row">
              <i class="bi bi-arrow-up-circle-fill text-danger"></i>
              <span>${escHtml(a)}</span>
            </div>`).join('')}
        </div>
      </div>
    </div>`;
}

/*  TOAST */
let toastTimer;
function showToast(msg, type = 'info') {
  const el  = document.getElementById('amToast');
  const ico = { success: 'bi-check-circle-fill', error: 'bi-x-circle-fill', info: 'bi-info-circle-fill' };
  el.className = `am-toast ${type}`;
  document.getElementById('toastIcon').className = `bi ${ico[type]}`;
  document.getElementById('toastMsg').textContent = msg;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add('d-none'), 3200);
}

/*  UTILS*/
function escHtml(str) {
  return String(str)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
