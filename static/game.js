/* ================================================================
   Juego de Viaje — Logica del frontend
   ================================================================ */

const ICONS = { start: "I", village: "A", market: "M", temple: "T", inn: "P", end: "F" };
const TYPE_ES = { start: "Inicio", village: "Aldea", market: "Mercado", temple: "Templo", inn: "Posada", end: "Fin" };
const TYPE_COLORS = {
  start: "var(--neutral)", village: "var(--village)", market: "var(--market)",
  temple: "var(--temple)", inn: "var(--inn)", end: "var(--neutral)"
};

let state = null;

/* ─── API ──────────────────────────────────────────── */

async function api(url, method = "GET", body = null) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  return res.json();
}

async function startGame() {
  state = await api("/api/nuevo", "POST");
  document.getElementById("start-screen").style.display = "none";
  document.getElementById("game-screen").style.display = "block";
  render();
}

async function makeMove(position) {
  state = await api("/api/mover", "POST", { position });
  render();
}

async function doContinue() {
  state = await api("/api/continuar", "POST");
  render();
}

/* ─── Renderizado principal ────────────────────────── */

function render() {
  if (!state) return;
  renderTitleBar();
  renderBoard();
  renderPlayers();
  renderAction();
  renderLog();
}

/* ─── Barra de titulo ──────────────────────────────── */

function renderTitleBar() {
  document.getElementById("turn-info").textContent = `Turno ${state.turn}`;
  document.getElementById("score-info").textContent =
    `Tu: ${state.human.score}  —  Rival: ${state.ai.score}`;
}

/* ─── Tablero ──────────────────────────────────────── */

function renderBoard() {
  const spacesEl = document.getElementById("board-spaces");
  const markersEl = document.getElementById("board-markers");
  spacesEl.innerHTML = "";
  markersEl.innerHTML = "";

  state.board.forEach((sp, i) => {
    // Casilla
    const el = document.createElement("div");
    el.className = `space space-${sp.type}`;
    if (state.phase === "movimiento" && state.legal_moves.includes(i)) {
      el.classList.add("legal");
      el.onclick = () => makeMove(i);
    }
    el.innerHTML = `<span class="space-num">${i}</span><span class="space-letter">${ICONS[sp.type] || "?"}</span>`;
    spacesEl.appendChild(el);

    // Slot de marcador
    const slot = document.createElement("div");
    slot.className = "marker-slot";

    if (state.human.position === i && !state.human.finished) {
      slot.innerHTML += `<div style="text-align:center"><div class="marker marker-human"></div><div class="marker-label human-color">Tu</div></div>`;
    }
    if (state.ai.position === i && !state.ai.finished) {
      slot.innerHTML += `<div style="text-align:center"><div class="marker marker-ai"></div><div class="marker-label ai-color">IA</div></div>`;
    }
    markersEl.appendChild(slot);
  });
}

/* ─── Paneles de jugador ───────────────────────────── */

function renderPlayers() {
  const h = state.human, a = state.ai;

  document.getElementById("human-pos").textContent = h.finished ? "Finalizado" : `Casilla ${h.position}`;
  document.getElementById("h-coins").textContent = h.coins;
  document.getElementById("h-points").textContent = h.points;
  document.getElementById("h-bless").textContent = h.blessings;
  document.getElementById("h-score").textContent = h.score;

  document.getElementById("ai-pos").textContent = a.finished ? "Finalizado" : `Casilla ${a.position}`;
  document.getElementById("a-coins").textContent = a.coins;
  document.getElementById("a-points").textContent = a.points;
  document.getElementById("a-bless").textContent = a.blessings;
  document.getElementById("a-score").textContent = a.score;
}

/* ─── Area de accion ───────────────────────────────── */

function renderAction() {
  const content = document.getElementById("action-content");
  const btn = document.getElementById("btn-continue");

  if (state.phase === "movimiento") {
    btn.style.display = "none";
    let html = `<div class="action-title">Elige tu movimiento</div>`;
    html += `<div class="action-subtitle">Haz clic en una casilla resaltada o selecciona abajo</div>`;

    state.legal_moves.forEach(move => {
      const sp = state.board[move];
      const steps = move - state.human.position;
      const tipo = TYPE_ES[sp.type] || sp.type;
      const color = TYPE_COLORS[sp.type] || "var(--dim)";
      html += `<div class="move-option" onclick="makeMove(${move})">`;
      html += `<div class="move-dot" style="background:${color}"></div>`;
      html += `<div><div class="move-text">${steps} casilla${steps > 1 ? "s" : ""} → ${sp.name}</div>`;
      html += `<div class="move-type">${tipo}</div></div></div>`;
    });

    content.innerHTML = html;

  } else if (state.phase === "efecto" || state.phase === "templo") {
    btn.style.display = "inline-block";
    let html = "";
    state.effect_text.forEach((line, i) => {
      let cls = "effect-line";
      if (i === 0) cls += " title-line";
      if (line.includes("+")) cls += " reward";
      html += `<div class="${cls}">${line}</div>`;
    });
    content.innerHTML = html;

  } else if (state.phase === "fin_del_juego") {
    btn.style.display = "none";
    let html = "";
    state.effect_text.forEach(line => {
      let cls = "effect-line";
      if (line.includes("GANASTE") || line.includes("Rival gana") || line.includes("empate")) cls += " winner";
      else if (line.includes("COMPLETADO")) cls += " title-line";
      else if (line.includes("pts")) cls += " reward";
      html += `<div class="${cls}">${line}</div>`;
    });
    content.innerHTML = html;
  }
}

/* ─── Registro ─────────────────────────────────────── */

function renderLog() {
  const el = document.getElementById("log-content");
  el.innerHTML = state.log.map(line => `<div class="log-line">${line}</div>`).join("");
  el.scrollTop = el.scrollHeight;
}
