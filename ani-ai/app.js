const KEY = 'ani.ai.writing_events.v1';
const entry = document.querySelector('#entry');
const photo = document.querySelector('#photo');

function load() {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]'); }
  catch { return []; }
}
function save(events) { localStorage.setItem(KEY, JSON.stringify(events)); render(); }
function id() { return crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`; }

function addEvent(event) {
  const events = load();
  events.unshift({ id: id(), created_at: new Date().toISOString(), ...event });
  save(events);
}

document.querySelector('#saveText').onclick = () => {
  const text = entry.value.trim();
  if (!text) return;
  addEvent({ type: 'text', text, source: 'mobile_text' });
  entry.value = '';
};

photo.onchange = async () => {
  const file = photo.files?.[0];
  if (!file) return;
  const data_url = await fileToDataURL(file);
  addEvent({ type: 'image', text: '', source: 'mobile_camera', mime_type: file.type, data_url });
  photo.value = '';
};

function fileToDataURL(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function metrics(events) {
  const textEvents = events.filter(e => e.type === 'text');
  const days = new Set(textEvents.map(e => e.created_at.slice(0,10))).size;
  const totalWords = textEvents.reduce((n,e) => n + (e.text.match(/\b\w+\b/g)||[]).length, 0);
  const completionSignals = textEvents.filter(e => /\b(done|completed|shipped|finished|built|sent|launched|closed)\b/i.test(e.text)).length;
  const actionable = textEvents.filter(e => /\b(todo|next|will|must|ship|build|call|send|finish)\b/i.test(e.text)).length;
  const score = textEvents.length ? Math.round(
    Math.min(100, days * 8) * .35 +
    Math.min(100, actionable / Math.max(1,textEvents.length) * 100) * .20 +
    Math.min(100, completionSignals / Math.max(1,textEvents.length) * 100) * .25 +
    Math.min(100, totalWords / Math.max(1,textEvents.length) * 2) * .20
  ) : 0;
  return { days, score, actionable, completionSignals, totalWords };
}

function render() {
  const events = load();
  const m = metrics(events);
  document.querySelector('#count').textContent = events.length;
  document.querySelector('#cadence').textContent = `${m.days} day${m.days === 1 ? '' : 's'}`;
  document.querySelector('#score').textContent = events.length ? m.score : '—';
  document.querySelector('#progress').textContent = m.completionSignals ? `${m.completionSignals} completion signals` : 'Baseline';
  const timeline = document.querySelector('#timeline');
  timeline.innerHTML = events.slice(0,12).map(e => `
    <article class="event">
      <time>${new Date(e.created_at).toLocaleString()}</time>
      <div><b>${e.type === 'image' ? 'Handwritten capture' : 'Writing capture'}</b></div>
      <p>${e.type === 'image' ? 'Image stored locally. OCR/stroke extraction is the next adapter.' : escapeHtml(e.text)}</p>
    </article>`).join('') || '<p class="muted">No captures yet.</p>';

  if (!events.length) return;
  document.querySelector('#insightTitle').textContent = m.score >= 70 ? 'Your baseline is forming.' : 'Your archive is still building the baseline.';
  document.querySelector('#insightBody').textContent = `Across ${m.days} active writing day${m.days===1?'':'s'}, Ani.ai found ${m.actionable} actionable writing signals and ${m.completionSignals} completion signals. This is a transparent prototype metric, not a psychological diagnosis.`;
}

function escapeHtml(s) { return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

document.querySelector('#export').onclick = () => {
  const blob = new Blob([JSON.stringify({ exported_at:new Date().toISOString(), events:load() }, null, 2)], {type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href=url; a.download='ani-ai-writing-archive.json'; a.click(); URL.revokeObjectURL(url);
};

if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js').catch(()=>{});
render();
