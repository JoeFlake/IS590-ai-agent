const chatContainer = document.getElementById('chatContainer');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');

let sessionId = localStorage.getItem('session_id') || crypto.randomUUID();
localStorage.setItem('session_id', sessionId);
let isStreaming = false;

function sendText(text) {
  inputEl.value = text;
  sendMessage();
}

async function sendMessage() {
  const message = inputEl.value.trim();
  if (!message || isStreaming) return;

  const welcome = chatContainer.querySelector('.welcome');
  if (welcome) welcome.remove();

  isStreaming = true;
  sendBtn.disabled = true;
  inputEl.value = '';
  inputEl.style.height = 'auto';

  appendUserMessage(message);
  const { bubble, toolArea } = appendAssistantMessage();

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, session_id: sessionId }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const data = JSON.parse(line.slice(6));
          handleEvent(data, bubble, toolArea);
        } catch (_) {}
      }
    }
  } catch (err) {
    bubble.classList.remove('cursor');
    bubble.classList.add('error-bubble');
    bubble.textContent = '🙈 Wipeout! ' + err.message;
    // swap avatar to peeking CJ on error
    const avatar = bubble.closest('.message')?.querySelector('.assistant-avatar');
    if (avatar) avatar.src = '/cj-peeking.png';
  } finally {
    bubble.classList.remove('cursor');
    isStreaming = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

function handleEvent(data, bubble, toolArea) {
  if (data.type === 'content') {
    bubble.textContent += data.content;
    scrollDown();
  } else if (data.type === 'tool_start') {
    const badge = document.createElement('span');
    badge.className = 'tool-badge';
    badge.dataset.tool = data.tool;
    badge.textContent = toolIcon(data.tool) + ' Using ' + data.tool + '…';
    toolArea.appendChild(badge);
    scrollDown();
  } else if (data.type === 'tool_end') {
    const badge = toolArea.querySelector(`[data-tool="${data.tool}"]`);
    if (badge) badge.textContent = toolIcon(data.tool) + ' ' + data.tool + ' ✓';
  } else if (data.type === 'done') {
    bubble.classList.remove('cursor');
  } else if (data.type === 'error') {
    bubble.classList.remove('cursor');
    bubble.classList.add('error-bubble');
    bubble.textContent = '🙈 Wipeout! ' + data.content;
    const avatar = bubble.closest('.message')?.querySelector('.assistant-avatar');
    if (avatar) avatar.src = '/cj-peeking.png';
  }
}

function toolIcon(name) {
  if (name === 'calculator') return '🧮';
  if (name === 'web_search') return '🌊';
  if (name === 'rag_search') return '📖';
  return '🤙';
}

function appendUserMessage(text) {
  const div = document.createElement('div');
  div.className = 'message user';
  div.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
  chatContainer.appendChild(div);
  scrollDown();
}

function appendAssistantMessage() {
  const div = document.createElement('div');
  div.className = 'message assistant';

  const toolArea = document.createElement('div');

  // Avatar + tool area row
  const headerRow = document.createElement('div');
  headerRow.className = 'assistant-header';
  const avatar = document.createElement('img');
  avatar.src = '/cj-dripping.png';
  avatar.className = 'assistant-avatar';
  avatar.alt = 'Chicken Joe';
  headerRow.appendChild(avatar);
  headerRow.appendChild(toolArea);

  const bubble = document.createElement('div');
  bubble.className = 'bubble cursor';

  div.appendChild(headerRow);
  div.appendChild(bubble);
  chatContainer.appendChild(div);
  scrollDown();
  return { bubble, toolArea };
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function scrollDown() {
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = inputEl.scrollHeight + 'px';
});

inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

sendBtn.addEventListener('click', sendMessage);

clearBtn.addEventListener('click', async () => {
  await fetch('/clear', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  });
  chatContainer.innerHTML = '';
  const welcome = document.createElement('div');
  welcome.className = 'welcome';
  welcome.innerHTML = `
    <img src="/cj-peace.png" class="welcome-img" alt="Chicken Joe peace" />
    <h2>Wiped out, dude!</h2>
    <p>Fresh waves ahead — ask me anything!</p>
    <div class="chips">
      <button class="chip" onclick="sendText('If a wave is 30 feet tall and I ride 4 waves a day for 7 days, how many total feet of wave have I ridden?')">🧮 Wave math, bro</button>
      <button class="chip" onclick="sendText('Who are the best surfers in the world right now?')">🌊 Who\'s shredding the most?</button>
      <button class="chip" onclick="sendText('What is the ReAct pattern in AI agents?')">📖 Gnarly AI knowledge</button>
    </div>`;
  chatContainer.appendChild(welcome);
});
