const description = document.getElementById('description');
const wordCount = document.getElementById('word-count');
const generateBtn = document.getElementById('generate-btn');
const canvas = document.getElementById('diagram-canvas');
const sourceCode = document.getElementById('source-code');
const resultState = document.getElementById('result-state');
const diagramTitles = {class:'Class diagram',usecase:'Use-case diagram',sequence:'Sequence diagram',activity:'Activity diagram',state:'State diagram'};
let diagramData = null;
let activeTab = 'class';
let toastTimer;

function updateWords() {
  const words = description.value.trim() ? description.value.trim().split(/\s+/).length : 0;
  wordCount.textContent = `${words} word${words === 1 ? '' : 's'}`;
}
description.addEventListener('input', updateWords);
updateWords();

document.getElementById('clear-btn').addEventListener('click', () => {
  description.value = ''; updateWords(); description.focus();
});
document.querySelectorAll('.example-chip').forEach(btn => btn.addEventListener('click', () => {
  description.value = btn.dataset.example; updateWords(); description.focus();
}));

function toast(message) {
  const el = document.getElementById('toast');
  el.textContent = message; el.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 2400);
}
function renderSource() {
  if (!diagramData) return;
  sourceCode.textContent = diagramData.diagrams[activeTab];
}
async function renderDiagram() {
  if (!diagramData) return;
  document.getElementById('diagram-title').textContent = diagramTitles[activeTab];
  renderSource();
  canvas.innerHTML = '<div class="empty-state"><div class="empty-icon">✦</div><h3>Rendering diagram…</h3><p>Arranging your diagram elements.</p></div>';
  try {
    if (!window.mermaid) await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('Diagram library did not load. Check your internet connection.')), 9000);
      window.addEventListener('mermaid-ready', () => { clearTimeout(timeout); resolve(); }, {once:true});
    });
    const id = 'diagram-' + activeTab + '-' + Date.now();
    const rendered = await window.mermaid.render(id, diagramData.diagrams[activeTab]);
    canvas.innerHTML = rendered.svg;
    const svg = canvas.querySelector('svg');
    if (svg) { svg.removeAttribute('height'); svg.style.maxWidth = '100%'; svg.style.height = 'auto'; }
    resultState.textContent = 'DIAGRAM READY';
  } catch (error) {
    canvas.innerHTML = `<div class="error-box">${escapeHtml(error.message || 'Unable to render this diagram.')}</div>`;
  }
}
function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
generateBtn.addEventListener('click', async () => {
  const text = description.value.trim();
  if (text.length < 20) { toast('Please enter at least 20 characters.'); description.focus(); return; }
  generateBtn.disabled = true; generateBtn.innerHTML = '<span>✦</span> Analysing requirements…';
  resultState.textContent = 'ANALYSING TEXT';
  try {
    const response = await fetch('/generate', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({description:text})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Generation failed.');
    diagramData = data;
    document.getElementById('class-count').textContent = data.summary.classes;
    document.getElementById('method-count').textContent = data.summary.methods;
    document.getElementById('rel-count').textContent = data.summary.relationships;
    document.querySelectorAll('.tab').forEach(tab => tab.classList.toggle('active', tab.dataset.tab === activeTab));
    await renderDiagram();
    toast('UML diagrams generated successfully.');
  } catch (error) {
    resultState.textContent = 'GENERATION FAILED';
    canvas.innerHTML = `<div class="error-box">${escapeHtml(error.message || 'Could not generate diagrams.')}</div>`;
  } finally {
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<span>✦</span> Generate UML diagrams <span class="button-arrow">→</span>';
  }
});
document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => {
  activeTab = tab.dataset.tab;
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t === tab));
  if (diagramData) renderDiagram();
}));
document.getElementById('source-toggle').addEventListener('click', () => {
  sourceCode.classList.toggle('hidden');
  document.getElementById('source-toggle').textContent = sourceCode.classList.contains('hidden') ? '⌄ View generated Mermaid source' : '⌃ Hide generated Mermaid source';
});
document.getElementById('copy-btn').addEventListener('click', async () => {
  if (!diagramData) return toast('Generate a diagram first.');
  try { await navigator.clipboard.writeText(diagramData.diagrams[activeTab]); toast('Mermaid source copied.'); }
  catch { toast('Clipboard access unavailable. Open the source panel to copy manually.'); }
});
document.getElementById('download-btn').addEventListener('click', () => {
  const svg = canvas.querySelector('svg');
  if (!svg) return toast('Generate a diagram first.');
  const clone = svg.cloneNode(true);
  clone.setAttribute('xmlns','http://www.w3.org/2000/svg');
  const blob = new Blob([new XMLSerializer().serializeToString(clone)], {type:'image/svg+xml;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = `uml-${activeTab}.svg`; a.click();
  URL.revokeObjectURL(url); toast('SVG download started.');
});
document.getElementById('zoom-btn').addEventListener('click', () => {
  canvas.scrollTo({top:0,left:0,behavior:'smooth'}); toast('Diagram view reset.');
});
