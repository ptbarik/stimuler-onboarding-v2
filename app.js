/* ============================================================
   Stimuler · India onboarding v2 — flow engine
   One async script walks the user's sequence (Paper frame
   "USER ONBOARDING FLOW"). Voice and mic are mocked.
   Deep links: ?goal=&sit=&lvl=&step=&name=
   ============================================================ */
'use strict';

const C  = window.CONTENT;
const $  = (id) => document.getElementById(id);
const QP = new URLSearchParams(location.search);

/* ---------- pathway state ---------- */
const S = {
  goal: C.GOALS.some(g => g.key === QP.get('goal')) ? QP.get('goal') : 'school',
  sit:  C.SITUATIONS.some(s => s.key === QP.get('sit')) ? QP.get('sit') : 'student',
  lvl:  ['beginner', 'intermediate', 'advanced'].includes(QP.get('lvl')) ? QP.get('lvl') : 'beginner',
  name: QP.get('name') || '',
  lang: 'Hindi',
  usedHint: false,
  skippedSpeaking: false,
  pain: QP.get('pain') || 'translate',
  painText: '',
};
const STEPS = [
  ['signup', 'Sign up'], ['hello', 'Sarah says hi'], ['name', 'Name'], ['language', 'Native language'],
  ['applang', 'App language'], ['source', 'Heard from'], ['about', 'Age + gender'], ['reminders', 'Phone number'],
  ['situation', 'Situation'], ['goal', 'Goal'], ['pain', 'Pain point'], ['level', 'Level'], ['proof', 'Social proof'], ['notify', 'Notifications'], ['test', 'Speaking test'],
  ['report', 'Analysing'], ['result', 'Your level'], ['fix', 'Errors'],
  ['practice', 'Practice'], ['win', 'Quick win'], ['plan', 'Plan'], ['paywall', 'Paywall'],
];
const TARGET = STEPS.some(s => s[0] === QP.get('step')) ? QP.get('step') : 'signup';
let FF = TARGET !== 'signup';           // fast-forward to a deep-linked step
function reach(key){
  window.__step = key;
  document.querySelectorAll('#dpStep button').forEach(b => b.classList.toggle('active', b.dataset.v === key));
  if (FF && key === TARGET) FF = false;
}

const goalObj = () => C.GOALS.find(g => g.key === S.goal);
const sitObj  = () => C.SITUATIONS.find(s => s.key === S.sit);
const test    = () => C.TEST[S.testGoal || S.goal];
const isRead  = () => S.lvl === 'beginner' || S.usedHint;
const fixes   = () => (S.lvl === 'beginner' ? test().fix : test().fixInt);
const nm      = () => S.name || 'Naina';

/* ---------- device fit (like the activation-funnel prototype) ---------- */
let SCALE = 1;
function fitPhone(){
  const m = $('mockup');
  if (innerWidth <= 480){
    const k = Math.min(innerWidth / 412, innerHeight / 917);
    m.style.transform = `scale(${k})`; SCALE = k; return;
  }
  const panel = innerWidth > 1100 ? 270 : 0;
  const s = Math.min(1, (innerWidth - 48 - panel) / (412 + 24), (innerHeight - 40) / (917 + 24));
  m.style.transform = `scale(${s})`; SCALE = s;
}
addEventListener('resize', fitPhone); fitPhone();

/* ---------- status bars ---------- */
document.querySelectorAll('.statusbar').forEach(sb => {
  sb.innerHTML = `<span>3:15</span><span class="sb-r"><span class="sb-bars"><i style="height:4px"></i><i style="height:6px"></i><i style="height:9px"></i><i style="height:11px"></i></span><span class="sb-batt"><i></i></span><span>47%</span></span>`;
});

/* ---------- timing ---------- */
let rushing = false;
const wait = (ms) => new Promise(r => setTimeout(r, (FF || rushing) ? 0 : ms));
const raf2 = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
function waitTap(el){
  if (FF) return Promise.resolve();
  return new Promise(r => el.addEventListener('click', () => r(), { once: true }));
}
function el(html){ const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; }

/* ---------- screens ---------- */
const SCREENS = ['sSignup', 'sChat', 'sReport', 'sLevel', 'sFix', 'sPractice', 'sWin', 'sPlan', 'sPaywall'];
function show(id){ SCREENS.forEach(s => $(s).classList.toggle('is-hidden', s !== id)); }

/* ---------- chat refs ---------- */
const chatScroll = $('chatScroll'), stream = $('chatStream');
const bottomBar = $('bottomBar'), skipBtn = $('skipBtn'), muteBtn = $('muteBtn');
let muted = false;
muteBtn.addEventListener('click', () => {
  muted = !muted; muteBtn.classList.toggle('muted', muted);
  muteBtn.querySelector('span').textContent = muted ? 'Unmute' : 'Mute';
  if (muted && 'speechSynthesis' in window) speechSynthesis.cancel();
});
function armSkip(){ skipBtn.classList.add('dimmed'); }
function disarmSkip(){ rushing = false; skipBtn.classList.remove('dimmed'); }
skipBtn.addEventListener('click', () => { if (!skipBtn.classList.contains('dimmed')) rushing = true; });
function toEnd(smooth = true){ chatScroll.scrollTo({ top: chatScroll.scrollHeight, behavior: (smooth && !FF) ? 'smooth' : 'auto' }); }

function say(text){
  if (muted || !('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'en-IN'; u.rate = .9;
  speechSynthesis.speak(u);
}

/* ---------- progress ---------- */
const pFill = $('progressFill'), pLabel = $('progressLabel');
function setProgress(pct, label){
  pFill.style.width = pct <= 0 ? '12px' : `calc((100% - 12px) * ${pct / 100} + 12px)`;
  document.querySelector('#sChat .progress-flag').classList.toggle('on', pct >= 100);
  if (label !== undefined && label !== pLabel.textContent){
    pLabel.textContent = label;
    pLabel.classList.remove('swap'); void pLabel.offsetWidth; pLabel.classList.add('swap');
  }
}
let held = null;
/* earn(pct, ack): progress lands with the answer; an optional ack
   ("Nice to meet you, Naina!") shows first, then settles to "NN% completed" */
let ackTimer = null;
const earn = (pct, ack = null) => { held = [pct, `${pct}% completed`, ack]; };
function release(){
  if (!held) return;
  const [pct, label, ack] = held; held = null;
  clearTimeout(ackTimer);
  if (ack && !FF){
    setProgress(pct, ack);
    pLabel.classList.add('ack');
    ackTimer = setTimeout(() => { pLabel.classList.remove('ack'); setProgress(pct, label); }, 2600);
  } else { pLabel.classList.remove('ack'); setProgress(pct, label); }
}

/* ---------- juice: pips fly from the answer to the bar ---------- */
function rel(r){
  const p = $('phone').getBoundingClientRect();
  return { x: (r.left - p.left) / SCALE, y: (r.top - p.top) / SCALE, w: r.width / SCALE, h: r.height / SCALE };
}
function pips(fromEl){
  if (FF) return;
  const a = rel(fromEl.getBoundingClientRect()), b = rel(pFill.getBoundingClientRect());
  const sx = a.x + a.w / 2, sy = a.y + a.h / 2, tx = b.x + b.w, ty = b.y + b.h / 2;
  for (let i = 0; i < 6; i++){
    const p = el('<i class="pip"></i>');
    $('phone').appendChild(p);
    const mx = sx + (Math.random() - .5) * 120, my = sy - 60 - Math.random() * 80;
    p.animate([
      { transform: `translate(${sx}px,${sy}px) scale(.6)`, opacity: 0 },
      { transform: `translate(${mx}px,${my}px) scale(1.15)`, opacity: 1, offset: .35 },
      { transform: `translate(${tx}px,${ty}px) scale(.5)`, opacity: .9 },
    ], { duration: 720 + i * 60, easing: 'cubic-bezier(.5,0,.3,1)', fill: 'forwards' }).onfinish = () => p.remove();
  }
}

function confetti(fromEl){
  const box = el('<div class="confetti"></div>');
  $('phone').appendChild(box);
  const a = rel(fromEl.getBoundingClientRect());
  const cols = ['#9D96FF', '#6C63FF', '#FFFFFF', '#63E39B', '#BBB7FF', '#FFC94D'];
  for (let i = 0; i < 46; i++){
    const c = el(`<i style="background:${cols[i % cols.length]}"></i>`);
    box.appendChild(c);
    const sx = a.x + a.w / 2, sy = a.y + a.h / 2;
    const ang = -Math.PI / 2 + (Math.random() - .5) * 2.4, v = 160 + Math.random() * 220;
    const ex = sx + Math.cos(ang) * v, ey = sy + Math.sin(ang) * v;
    c.animate([
      { transform: `translate(${sx}px,${sy}px) rotate(0deg)`, opacity: 1 },
      { transform: `translate(${ex}px,${ey}px) rotate(${Math.random() * 540}deg)`, opacity: 1, offset: .55 },
      { transform: `translate(${ex + (Math.random() - .5) * 60}px,${ey + 260}px) rotate(${Math.random() * 900}deg)`, opacity: 0 },
    ], { duration: 1300 + Math.random() * 500, easing: 'cubic-bezier(.2,.7,.3,1)', fill: 'forwards' });
  }
  setTimeout(() => box.remove(), 2000);
}

/* ---------- chat primitives ---------- */
function dimPrev(){ stream.querySelectorAll('.msg:not(.dim)').forEach(m => m.classList.add('dim')); }

async function sarah(text, { quick = false } = {}){
  dimPrev();
  if (FF || rushing){
    stream.appendChild(el(`<div class="msg dim"><div class="dp"><img src="assets/sarah-chat.png" alt=""></div><div class="bubble"><p>${text}</p></div></div>`));
    toEnd(false); return;
  }
  const row = el(`<div class="msg"><div class="dp"><img src="assets/sarah-chat.png" alt=""></div><div class="bubble typing"><i></i><i></i><i></i></div></div>`);
  stream.appendChild(row); toEnd();
  await wait(quick ? 420 : 640);
  const b = row.querySelector('.bubble');
  b.classList.remove('typing'); b.innerHTML = `<p>${text}</p>`;
  row.classList.add('speaking'); toEnd();
  await wait(Math.max(1100, text.split(' ').length * (quick ? 80 : 115)));
  row.classList.remove('speaking');
  await wait(quick ? 160 : 300);
}

function userChip(text){
  release();
  const row = el(`<div class="chip-row"><div class="chip">${text}</div></div>`);
  stream.appendChild(row); toEnd();
  return row;
}
function sysNote(row, text){ row.appendChild(el(`<p class="sys-note">${text}</p>`)); toEnd(); }
function sysPill(text){
  stream.appendChild(el(`<div class="sys-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M13.7 21a2 2 0 0 1-3.4 0M18 8a6 6 0 0 0-9.3-5M6 8c0 7-3 9-3 9h14M3 3l18 18"/></svg>${text}</div>`));
  toEnd();
}

const SPARK = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c.7 5.9 5.4 10.6 12 12-6.6 1.4-11.3 6.1-12 12-.7-5.9-5.4-10.6-12-12C6.6 10.6 11.3 5.9 12 0Z"/></svg>';
async function sticker(src, into = stream){
  into.appendChild(el(`<div class="sticker"><i class="spark s1">${SPARK}</i><i class="spark s2">${SPARK}</i><i class="spark s3">${SPARK}</i><img src="${src}" alt=""></div>`));
  if (into === stream) toEnd();
  await wait(700);
}

/* answer chips that wrap (Gift Sense pattern) */
const ICON = {
  ig: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".9" fill="currentColor"/></svg>',
  yt: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 8.2s-.2-1.5-.8-2.1c-.8-.8-1.7-.8-2.1-.9C16.2 5 12 5 12 5s-4.2 0-7.1.2c-.4.1-1.3.1-2.1.9-.6.6-.8 2.1-.8 2.1S2 9.9 2 11.6v1.6c0 1.7.2 3.4.2 3.4s.2 1.5.8 2.1c.8.8 1.9.8 2.4.9 1.7.2 6.6.2 6.6.2s4.2 0 7.1-.2c.4-.1 1.3-.1 2.1-.9.6-.6.8-2.1.8-2.1s.2-1.7.2-3.4v-1.6c0-1.7-.2-3.4-.2-3.4zM9.9 15.1V9.2l5.4 3-5.4 2.9z"/></svg>',
  play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.2 2.5c-.2.2-.3.6-.3 1v17c0 .4.1.8.3 1l9.4-9.5-9.4-9.5zm10.6 10.6 2.9 2.9-11.6 6.6 8.7-9.5zm0-2.2L6.1 1.4l11.6 6.6-2.9 2.9zm4.3-2.1 3.1 1.8c.9.5.9 1.3 0 1.8l-3.1 1.8-3.2-3.2 3.2-2.2z"/></svg>',
  people: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.3-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18.5 14.8c1.7.7 2.8 2.5 3 5.2"/></svg>',
  fb: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8.5V6.7c0-.8.5-1.2 1.2-1.2H17V2h-2.6C11.6 2 10.5 4 10.5 6.4v2.1H8V12h2.5v10H14V12h2.7l.4-3.5H14z"/></svg>',
  google: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.6 10.2H12v3.9h5.5c-.5 2.5-2.7 3.9-5.5 3.9a6 6 0 0 1 0-12c1.5 0 2.9.6 3.9 1.5l2.9-2.9A10 10 0 1 0 12 22c5.8 0 9.8-4.1 9.8-9.9 0-.6-.1-1.3-.2-1.9z"/></svg>',
  wa: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 13.9c-.2.6-1.3 1.2-1.8 1.3-.5.1-1 .1-1.7-.1a15 15 0 0 1-1.5-.6 12 12 0 0 1-4.6-4c-.6-.8-1.2-1.9-1.2-3s.6-1.7.8-2c.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.7 1.2 1.6 1.9 1.1 1 2 1.3 2.3 1.4.3.1.4.1.6-.1l.8-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.2z"/></svg>',
};
function chipsQ(items, { head = 'Select an option', forced } = {}){
  if (FF){
    const it = items.find(i => i.value === forced) || items[0];
    const row = userChip(it.chip || it.label);
    return Promise.resolve({ value: it.value, row });
  }
  return new Promise(resolve => {
    const wrap = el(`<div class="opts"><p class="opt-head">${head}</p><div class="chips"></div></div>`);
    const list = wrap.querySelector('.chips');
    items.forEach((it, i) => {
      const b = el(`<button class="pchip${it.more ? ' more' : ''}">${it.icon ? `<span class="pico">${ICON[it.icon] || ''}</span>` : ''}<span>${it.label}</span>${it.nat ? `<span class="nat">${it.nat}</span>` : ''}</button>`);
      b.style.animationDelay = `${i * 35}ms`;
      b.addEventListener('click', () => {
        if (wrap.dataset.done) return;
        wrap.dataset.done = 1;
        b.classList.add('sel'); pips(b);
        setTimeout(() => {
          disarmSkip(); wrap.remove();
          const row = userChip(it.chip || it.label);
          resolve({ value: it.value, row });
        }, 380);
      });
      list.appendChild(b);
    });
    stream.appendChild(wrap); toEnd(); armSkip();
  });
}

function stackedQ(items, forced){
  if (FF){ const it = items.find(i => i.value === forced) || items[0]; userChip(it.label); return Promise.resolve(it.value); }
  return new Promise(resolve => {
    const wrap = el(`<div class="opts"><p class="opt-head">Select an option</p><div class="opt-list"></div></div>`);
    items.forEach((it, i) => {
      const b = el(`<button class="opt"><span class="o-top"><span class="o-ico">${it.icon}</span>${it.label}</span><span class="o-desc">${it.desc}</span></button>`);
      b.style.animationDelay = `${i * 50}ms`;
      b.addEventListener('click', () => {
        if (wrap.dataset.done) return; wrap.dataset.done = 1;
        b.classList.add('sel'); pips(b);
        setTimeout(() => { disarmSkip(); wrap.remove(); userChip(it.label); resolve(it.value); }, 420);
      });
      wrap.querySelector('.opt-list').appendChild(b);
    });
    stream.appendChild(wrap); toEnd(); armSkip();
  });
}

function nameInput(){
  if (FF){ userChip(nm()); return Promise.resolve(nm()); }
  return new Promise(resolve => {
    const wrap = el(`<div class="input-block"><input class="field" maxlength="30" placeholder="Type your name" autocomplete="given-name"><button class="mini-cta">Continue</button></div>`);
    const inp = wrap.querySelector('input'), btn = wrap.querySelector('button');
    inp.addEventListener('input', () => btn.classList.toggle('ready', inp.value.trim().length > 1));
    const go = () => {
      const v = inp.value.trim(); if (v.length < 2) return;
      const n = v.split(' ')[0]; const nice = n.charAt(0).toUpperCase() + n.slice(1);
      if (held) held[2] = `Nice to meet you, ${nice}!`;
      pips(btn); disarmSkip(); wrap.remove(); userChip(v); resolve(nice);
    };
    btn.addEventListener('click', go);
    inp.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
    stream.appendChild(wrap); toEnd(); armSkip();
    setTimeout(() => inp.focus({ preventScroll: true }), 350);
  });
}

/* frames 7 + 8 merged: one card, two chip rows, one Done */
function aboutCard(){
  if (FF){ userChip('18–24 · Female'); return Promise.resolve(); }
  return new Promise(resolve => {
    const card = el(`<div class="chat-card">
      <p class="cc-cap">Age</p><div class="chips" data-k="age"></div>
      <p class="cc-cap">Gender</p><div class="chips" data-k="gender"></div>
      <button class="wide-cta">Done</button></div>`);
    const pick = { age: null, gender: null };
    const done = card.querySelector('.wide-cta');
    [['age', C.AGES], ['gender', C.GENDERS]].forEach(([k, arr]) => {
      const box = card.querySelector(`[data-k="${k}"]`);
      arr.forEach(v => {
        const b = el(`<button class="pchip">${v}</button>`);
        b.addEventListener('click', () => {
          box.querySelectorAll('.pchip').forEach(x => x.classList.remove('sel'));
          b.classList.add('sel'); pick[k] = v;
          done.classList.toggle('ready', !!(pick.age && pick.gender));
        });
        box.appendChild(b);
      });
    });
    done.addEventListener('click', () => {
      pips(done); disarmSkip(); card.remove();
      userChip(`${pick.age} · ${pick.gender}`); resolve();
    });
    stream.appendChild(card); toEnd(); armSkip();
  });
}

/* frame 9 (JHU-0): ask for the number, low barrier. "Skip for now" is always there.
   Notifications are asked later, the way the live app does it. */
function phoneCard(){
  if (FF) return Promise.resolve({ on: true, phone: '98765 43210' });
  return new Promise(resolve => {
    const card = el(`<div class="chat-card">
      <label class="phone-field"><span class="cc">+91</span><input inputmode="numeric" maxlength="11" placeholder="Phone number"></label>
      <button class="wide-cta">Continue</button>
      <button class="text-link">Skip for now</button></div>`);
    const inp = card.querySelector('input'), cta = card.querySelector('.wide-cta');
    inp.addEventListener('input', () => {
      const d = inp.value.replace(/\D/g, '').slice(0, 10);
      inp.value = d.length > 5 ? `${d.slice(0, 5)} ${d.slice(5)}` : d;
      cta.classList.toggle('ready', d.length === 10);
    });
    inp.addEventListener('keydown', e => { if (e.key === 'Enter' && cta.classList.contains('ready')) cta.click(); });
    cta.addEventListener('click', e => {
      pips(e.currentTarget); disarmSkip(); card.remove();
      resolve({ on: true, phone: inp.value.trim() });
    });
    card.querySelector('.text-link').addEventListener('click', () => { disarmSkip(); card.remove(); resolve({ on: false }); });
    stream.appendChild(card); toEnd(); armSkip();
    setTimeout(() => inp.focus({ preventScroll: true }), 350);
  });
}

/* single-line stacked options (pain question) */
function listQ(items, forced){
  if (FF){ const it = items.find(i => i.value === forced) || items[0]; userChip(it.label); return Promise.resolve(it.value); }
  return new Promise(resolve => {
    const wrap = el(`<div class="opts"><p class="opt-head">Select an option</p><div class="opt-list"></div></div>`);
    items.forEach((it, i) => {
      const b = el(`<button class="opt line"><span class="o-label">${it.label}</span></button>`);
      b.style.animationDelay = `${i * 45}ms`;
      b.addEventListener('click', () => {
        if (wrap.dataset.done) return; wrap.dataset.done = 1;
        b.classList.add('sel'); pips(b);
        setTimeout(() => { disarmSkip(); wrap.remove(); if (it.value !== 'other') userChip(it.label); resolve(it.value); }, 420);
      });
      wrap.querySelector('.opt-list').appendChild(b);
    });
    stream.appendChild(wrap); toEnd(); armSkip();
  });
}

/* free text (used for "Something else") */
function freeText(placeholder){
  if (FF){ userChip('I lose confidence midway'); return Promise.resolve('I lose confidence midway'); }
  return new Promise(resolve => {
    const wrap = el(`<div class="input-block"><input class="field" maxlength="60" placeholder="${placeholder}"><button class="mini-cta">Continue</button></div>`);
    const inp = wrap.querySelector('input'), btn = wrap.querySelector('button');
    inp.addEventListener('input', () => btn.classList.toggle('ready', inp.value.trim().length > 2));
    const go = () => { const v = inp.value.trim(); if (v.length < 3) return; pips(btn); disarmSkip(); wrap.remove(); userChip(v); resolve(v); };
    btn.addEventListener('click', go);
    inp.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
    stream.appendChild(wrap); toEnd(); armSkip();
    setTimeout(() => inp.focus({ preventScroll: true }), 350);
  });
}

/* ---------- OS dialogs ---------- */
function osDialog({ icon, title, buttons }){
  if (FF) return Promise.resolve(0);
  return new Promise(resolve => {
    const d = $('osDialog');
    d.innerHTML = `<span class="os-ico">${icon}</span><h4>${title}</h4>`;
    buttons.forEach((t, i) => {
      const b = el(`<button>${t}</button>`);
      b.addEventListener('click', () => { $('osScrim').classList.remove('show'); setTimeout(() => resolve(i), 260); });
      d.appendChild(b);
    });
    $('osScrim').classList.add('show');
  });
}
const BELL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0"/></svg>';
const MIC  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>';

/* ============================================================
   FRAMES 1 → 2 · Sarah says hi, then becomes the first message
   ============================================================ */
async function hello(){
  const H = $('hello'), sarahBox = $('helloSarah'), bub = $('helloBubble');
  const first = "Hi! I'm Sarah, your personal English speaking partner.";
  const finish = () => {
    H.classList.add('gone');
    $('topbar').classList.remove('gone');
    bottomBar.classList.remove('gone');
  };
  if (FF){
    stream.appendChild(el(`<div class="msg dim"><div class="dp"><img src="assets/sarah-chat.png" alt=""></div><div class="bubble"><p>${first}</p></div></div>`));
    finish(); return;
  }
  $('topbar').classList.add('gone');
  await wait(1150);
  bub.classList.add('shine');
  await wait(2000);

  /* measure where the first chat message will sit */
  const row = el(`<div class="msg" style="animation:none;opacity:0"><div class="dp"><img src="assets/sarah-chat.png" alt=""></div><div class="bubble"><p>${first}</p></div></div>`);
  stream.appendChild(row);
  $('topbar').classList.remove('gone');
  await raf2();
  const hr = rel(H.getBoundingClientRect());
  const dp = rel(row.querySelector('.dp').getBoundingClientRect());
  const bb = rel(row.querySelector('.bubble').getBoundingClientRect());
  const sb = rel(sarahBox.getBoundingClientRect());
  const hb = rel(bub.getBoundingClientRect());

  H.classList.add('morphing');
  bub.classList.remove('shine');
  const dur = 820, ease = 'cubic-bezier(.65,0,.25,1)';
  sarahBox.style.animation = 'none';
  sarahBox.animate([
    { left: `${sb.x - hr.x}px`, top: `${sb.y - hr.y}px`, width: `${sb.w}px`, height: `${sb.h}px`, borderRadius: '0px', borderColor: 'transparent', backgroundColor: 'transparent' },
    { left: `${dp.x - hr.x}px`, top: `${dp.y - hr.y}px`, width: `${dp.w}px`, height: `${dp.h}px`, borderRadius: '50%', borderColor: 'rgba(155,161,231,.5)', backgroundColor: '#1B1D3B' },
  ], { duration: dur, easing: ease, fill: 'forwards' });
  bub.style.animation = 'none';
  const bp = bub.querySelector('p');
  bp.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 200, fill: 'forwards' }).onfinish = () => {
    bp.textContent = first;
    Object.assign(bp.style, { whiteSpace: 'normal', width: `${bb.w - 36}px`, fontSize: '16.5px', lineHeight: '25px' });
    bp.animate([{ opacity: 0 }, { opacity: 0, offset: .35 }, { opacity: 1 }], { duration: dur - 200, fill: 'forwards' });
  };
  bub.animate([
    { left: `${hb.x - hr.x}px`, top: `${hb.y - hr.y}px`, width: `${hb.w}px`, height: `${hb.h}px`, borderRadius: '18px 18px 6px 18px', padding: '11px 16px' },
    { left: `${bb.x - hr.x}px`, top: `${bb.y - hr.y}px`, width: `${bb.w}px`, height: `${bb.h}px`, borderRadius: '8px 22px 22px 22px', padding: '13px 17px' },
  ], { duration: dur, easing: ease, fill: 'forwards' });
  await wait(dur);
  row.style.opacity = 1; row.classList.add('speaking');
  finish();
  await wait(2000);
  row.classList.remove('speaking');
}

/* ============================================================
   FRAMES 15 – 17 · the speaking test
   ============================================================ */
const micBar = $('micBar'), convMic = $('convMic'), micTip = $('micTip'), hintBtn = $('hintBtn'), micSkip = $('micSkip');
let micAllowed = false;

function words(text){
  return text.split(' ').map(w => `<span class="w">${w}</span>`).join(' ');
}
function readCard(text, label = 'Read it out loud'){
  const card = el(`<div class="read-card"><p class="rc-label">${label}</p><p class="rc-text">${words(text)}</p>
    <div class="rc-icons"><span class="rc-listen" title="Listen"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg></span></div></div>`);
  card.querySelector('.rc-listen').addEventListener('click', () => say(text));
  stream.appendChild(card); toEnd();
  return card;
}
function questionCard(q){
  const card = el(`<div class="q-card"><p class="rc-label">${MIC.replace('<svg', '<svg width="15" height="15"')} Answer out loud</p><p class="rc-text">“${q}”</p>
    <div class="rc-icons"><span class="rc-listen" title="Listen"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg></span></div></div>`);
  card.querySelector('.rc-listen').addEventListener('click', () => say(q));
  stream.appendChild(card); toEnd();
  return card;
}

/* returns 'done' | 'skip' | 'hint' */
function micTurn({ mode, card, hint }){
  if (FF){
    if (mode === 'read') card.querySelectorAll('.w').forEach(w => w.classList.add('said'));
    else stream.appendChild(el(`<div class="speech final">${test().said}</div>`));
    return Promise.resolve('done');
  }
  return new Promise(resolve => {
    bottomBar.classList.add('gone');
    micBar.classList.remove('gone');
    $('sChat').classList.add('mic-on'); setTimeout(() => toEnd(), 60);
    const tips = mode === 'read' ? ['Tap the mic and read'] : ['Tap the mic and answer', 'Stuck? Tap the bulb for a model answer'];
    let ti = 0; micTip.textContent = tips[0];
    const tipIv = setInterval(() => {
      if (tips.length < 2 || convMic.classList.contains('rec')) return;
      ti = (ti + 1) % tips.length;
      micTip.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 180 }).onfinish = () => {
        micTip.textContent = tips[ti]; micTip.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 220 });
      };
    }, 3600);
    micTip.classList.remove('hide'); micSkip.classList.remove('hide');
    hintBtn.classList.toggle('gone', !hint);
    hintBtn.classList.toggle('glow', !!hint);
    $('micSpacer').style.display = '';

    let timer = null, live = null, idx = 0;
    const wave = $('micWave');
    wave.innerHTML = Array.from({ length: 22 }, (_, i) => `<i style="height:${8 + Math.round(Math.abs(Math.sin(i * 1.7)) * 24)}px;animation-delay:${(i % 6) * .08}s"></i>`).join('');

    const cleanup = () => {
      clearInterval(timer); clearInterval(tipIv);
      $('sChat').classList.remove('mic-on');
      $('micOrb').onclick = null; $('micCancel').onclick = null; $('micDone').onclick = null; hintBtn.onclick = null; micSkip.onclick = null;
    };
    const reset = () => {
      clearInterval(timer);
      convMic.classList.remove('rec');
      micTip.classList.remove('hide'); micSkip.classList.remove('hide');
      if (hint) hintBtn.classList.remove('gone');
      if (mode === 'read') card.querySelectorAll('.w').forEach(w => w.classList.remove('said', 'now'));
      if (live){ live.remove(); live = null; }
      idx = 0;
    };
    const complete = async () => {
      clearInterval(timer);
      if (mode === 'read') card.querySelectorAll('.w').forEach(w => { w.classList.remove('now'); w.classList.add('said'); });
      else if (live){ live.innerHTML = test().said; live.classList.add('final'); }
      convMic.classList.remove('rec'); convMic.classList.add('busy');
      await wait(900);
      convMic.classList.remove('busy');
      micBar.classList.add('gone');
      cleanup(); resolve('done');
    };
    const record = () => {
      convMic.classList.add('rec');
      micTip.classList.add('hide'); micSkip.classList.add('hide'); hintBtn.classList.add('gone');
      if (mode === 'read'){
        const ws = [...card.querySelectorAll('.w')];
        timer = setInterval(() => {
          if (idx > 0) { ws[idx - 1].classList.remove('now'); ws[idx - 1].classList.add('said'); }
          if (idx >= ws.length){ clearInterval(timer); setTimeout(complete, 450); return; }
          ws[idx].classList.add('now'); idx++;
        }, 300);
      } else {
        const ws = test().said.split(' ');
        live = el(`<div class="speech"><span class="t"></span><span class="caret"></span></div>`);
        stream.appendChild(live); toEnd();
        timer = setInterval(() => {
          if (idx >= ws.length){ clearInterval(timer); setTimeout(complete, 600); return; }
          live.querySelector('.t').textContent += (idx ? ' ' : '') + ws[idx]; idx++;
          if (idx % 4 === 0) toEnd();
        }, 230);
      }
    };
    $('micOrb').onclick = async () => {
      if (!micAllowed){
        const r = await osDialog({ icon: MIC, title: 'Allow <b>Stimuler</b> to record audio?', buttons: ['While using the app', 'Only this time', "Don't allow"] });
        if (r === 2){
          await sarah("I'll need your mic to hear you. Tap it again whenever you're ready.", { quick: true });
          return;
        }
        micAllowed = true;
      }
      record();
    };
    $('micCancel').onclick = reset;
    $('micDone').onclick = () => { if (idx > 2) complete(); };
    hintBtn.onclick = () => { cleanup(); micBar.classList.add('gone'); resolve('hint'); };
    micSkip.onclick = () => { cleanup(); micBar.classList.add('gone'); resolve('skip'); };
  });
}

/* ============================================================
   FRAME 18 · social proof rail (auto-sliding)
   ============================================================ */
const STAR = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5l2.9 6.2 6.6.7-4.9 4.5 1.4 6.6L12 17.2l-5.9 3.3 1.4-6.6L2.6 9.4l6.6-.7z"/></svg>';
function proofRail(){
  const list = C.PROOF[S.goal];
  const wrap = el(`<div class="rail-wrap"><div class="rail"></div><div class="rail-dots"></div></div>`);
  const rail = wrap.querySelector('.rail'), dots = wrap.querySelector('.rail-dots');
  list.forEach((t, i) => {
    rail.appendChild(el(`<div class="t-card"><div class="t-stars">${STAR.repeat(5)}</div><p class="t-quote">“${t.quote}”</p>
      <div class="t-who"><span class="t-av">${t.name[0]}</span><span><p class="t-name">${t.name}</p><p class="t-meta">${t.meta}</p></span>
      <span class="t-src">${t.src === 'play' ? ICON.play.replace('<svg', '<svg style="color:#9D96FF"') : '<svg viewBox="0 0 24 24" fill="#9D96FF"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm-3.6 15.5-1.2-.7 1.4-2.4H6v-1.5h3.4l2.4-4.1-1-1.7 1.3-.8.6 1.1.6-1.1 1.3.8-3.7 6.3h2.3l.9 1.5H9.3l-.9 1.5zm9.6-1.6h-2.1l1.1 1.9-1.3.8-3.6-6.2.9-1.5 1.7 3h3.3v1.5z"/></svg>'}</span></div></div>`));
    dots.appendChild(el(`<i class="${i === 0 ? 'on' : ''}"></i>`));
  });
  stream.appendChild(wrap); toEnd();
  let i = 0;
  const go = () => {
    if (!document.body.contains(rail)) return clearInterval(iv);
    i = (i + 1) % list.length;
    rail.scrollTo({ left: rail.children[i].offsetLeft - 60, behavior: 'smooth' });
  };
  const iv = setInterval(go, 3000);
  rail.addEventListener('scroll', () => {
    const k = Math.round(rail.scrollLeft / 294);
    [...dots.children].forEach((d, j) => d.classList.toggle('on', j === Math.min(k, list.length - 1)));
  }, { passive: true });
  rail.addEventListener('pointerdown', () => clearInterval(iv), { once: true });
}

/* ============================================================
   TAKEOVER SCREENS (frames 20 – 25)
   ============================================================ */
const TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>';
const UPI = '<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" fill="rgba(245,196,81,.16)"/><path d="M10 14V6.5M6.8 9.4 10 6.2l3.2 3.2" fill="none" stroke="#F5C451" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const CHECK = '<svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" fill="rgba(79,209,165,.16)"/><path d="M6 10.3l2.7 2.7 5.3-5.8" fill="none" stroke="#4FD1A5" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

const PENCIL = '<svg viewBox="0 0 14 14"><path d="M9.5 1.8l2.7 2.7L4.7 12H2v-2.7z" fill="none" stroke="#C9C8FF" stroke-width="1.4" stroke-linejoin="round"/></svg>';
const painShort = () => S.pain === 'other' && S.painText ? S.painText : (C.PAINS.find(p => p.key === S.pain) || C.PAINS[1]).short;

/* bottom sheet: pick a new value for one of her answers */
function sheet(title, items, current){
  return new Promise(resolve => {
    const sh = $('sheet');
    sh.innerHTML = `<div class="sh-grab"></div><p class="sh-title">${title}</p><div class="sh-list"></div>`;
    items.forEach(it => {
      const b = el(`<button class="pchip${it.value === current ? ' sel' : ''}">${it.label}</button>`);
      b.addEventListener('click', () => { b.classList.add('sel'); setTimeout(() => close(it.value), 220); });
      sh.querySelector('.sh-list').appendChild(b);
    });
    const close = (v) => { $('sheetScrim').classList.remove('show'); setTimeout(() => resolve(v), 280); };
    $('sheetScrim').onclick = (e) => { if (e.target.id === 'sheetScrim') close(null); };
    $('sheetScrim').classList.add('show');
  });
}

function renderSnapshot(){
  const box = $('rpSnapChips');
  const chips = [
    { k: 'sit',  label: sitObj().label },
    { k: 'goal', label: goalObj().label },
    { k: 'pain', label: painShort() },
  ];
  box.innerHTML = chips.map((c, i) => `<button class="snap-chip" data-k="${c.k}" style="animation-delay:${.15 + i * .12}s">${c.label}</button>`).join('');
  box.querySelectorAll('.snap-chip').forEach(b => b.addEventListener('click', async () => {
    const k = b.dataset.k;
    let v = null;
    if (k === 'sit')  v = await sheet('What best describes you?', C.SITUATIONS.map(x => ({ value: x.key, label: x.label })), S.sit);
    if (k === 'goal') v = await sheet('Your main goal', C.GOALS.map(x => ({ value: x.key, label: x.label })), S.goal);
    if (k === 'pain') v = await sheet('What gets in the way?', C.PAINS.filter(x => x.key !== 'other').map(x => ({ value: x.key, label: x.short })), S.pain);
    if (v === null) return;
    if (k === 'sit') S.sit = v; else if (k === 'goal') S.goal = v; else { S.pain = v; S.painText = ''; }
    renderSnapshot();
    const nb = box.querySelector(`[data-k="${k}"]`); nb.classList.add('changed');
  }));
}

async function report(){
  reach('report');
  show('sReport');
  const items = ['Checking pronunciation', 'Checking fluency and pauses', 'Checking grammar', `Matching this to your goal: ${goalObj().label}`];
  const ul = $('rpTicks');
  ul.innerHTML = items.map(t => `<li><span class="tk">${TICK}</span><span>${t}</span></li>`).join('');
  const cta = $('rpCta'); cta.classList.add('cta-hidden');
  $('rpSnap').classList.remove('show');
  renderSnapshot();
  const lis = [...ul.children];
  for (const li of lis){
    li.classList.add('active'); await wait(850);
    li.classList.remove('active'); li.classList.add('ok');
  }
  document.querySelector('.rp-avatar').classList.add('done');
  $('rpSnap').classList.add('show');
  await wait(500);
  cta.classList.remove('cta-hidden');
  await waitTap(cta);
}

async function result(){
  reach('result');
  const L = C.LEVELS[S.lvl];
  $('lvTitle').innerHTML = S.lvl === 'beginner' ? `You're a <em>${L.label}</em>` : `You're <em>${L.label}</em>`;
  $('lvLine').textContent = '';
  const HERE = { beginner: '“Short sentences”', intermediate: '“Everyday talk”', advanced: '“Fluent, with polish”' };
  const NEXT = { beginner: 'Fewer pauses', intermediate: 'Quicker replies', advanced: 'Natural, precise' };
  const lad = $('lvLadder');
  lad.innerHTML = C.LADDER.map((r, i) => `<div class="lv-row" data-i="${i}"><span class="lv-name">${r.label}</span><span class="lv-rung">${r.cefr}</span>
    <span class="lv-ann">${i === L.rung ? `<b>You're here</b><span>${HERE[S.lvl]}</span>` : i === L.rung + 1 ? `<b>Next stop</b><span>${NEXT[S.lvl]}</span>` : ''}</span></div>`).join('')
    + `<svg class="lv-arrow" id="lvArrow" width="30" height="62" viewBox="0 -2 30 62"><path id="lvArrowPath" d="M0 60 C 28 60 28 0 3 0"/><path class="head" d="M9 -5 L3 0 L9 5"/></svg>`;
  const well = S.skippedSpeaking ? [] : (S.lvl === 'beginner'
    ? ['You read the whole passage without stopping.', `'${test().good[0]}' and '${test().good[1]}' were clear.`]
    : S.usedHint ? ['You read the model answer smoothly.', 'Your pace was steady and easy to follow.']
    : ['You answered in full sentences.', 'You kept going without long pauses.']);
  $('lvWell').innerHTML = well.map(t => `<li>${CHECK}<span>${t}</span></li>`).join('');
  const FX = fixes();
  $('lvImprove').innerHTML = `<li>${UPI}<span>'${FX[0].word}' and '${FX[1].word}' need a little work. We'll fix them next.</span></li>`;
  const cta = $('lvCta'); cta.classList.add('cta-hidden');
  show('sLevel');
  await raf2();
  const rows = [...lad.querySelectorAll('.lv-row')];
  /* place the curved arrow between "here" and "next" */
  const here = rows[L.rung], next = rows[L.rung + 1], arrow = $('lvArrow');
  arrow.style.top = `${next.offsetTop + 17}px`;
  const ap = $('lvArrowPath'), len = ap.getTotalLength();
  ap.style.strokeDasharray = `${len}`; ap.style.strokeDashoffset = `${len}`; arrow.style.opacity = 0;

  await wait(350);
  for (let i = 0; i < L.rung; i++){ rows[i].classList.add('past'); await wait(140); }
  here.classList.add('here');
  await wait(380);
  here.querySelector('.lv-ann').classList.add('show');
  await wait(550);
  next.classList.add('next');
  arrow.style.opacity = 1;
  ap.style.transition = FF ? 'none' : 'stroke-dashoffset .8s cubic-bezier(.65,0,.35,1)';
  ap.style.strokeDashoffset = 0;
  setTimeout(() => { ap.style.strokeDasharray = '4 5'; }, FF ? 0 : 820);
  await wait(700);
  next.querySelector('.lv-ann').classList.add('show');
  await wait(300);
  for (const li of [...$('lvWell').children, ...$('lvImprove').children]){ li.classList.add('show'); await wait(220); }
  cta.classList.remove('cta-hidden');
  await waitTap(cta);
}

function markText(text, list, { focus = -1 } = {}){
  const norm = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z']/g, '');
  return text.split(' ').map(w => {
    const k = list.findIndex(f => norm(w) === norm(f.word));
    if (k === -1) return w;
    const m = w.match(/^(.*?)([.,!?]*)$/);
    return `<span class="err${k === focus ? ' focus' : ''}" data-k="${k}">${m[1]}</span>${m[2]}`;
  }).join(' ');
}
const spokenText = () => S.lvl === 'beginner' ? test().passage : (S.usedHint ? test().model : test().said);

async function fix(){
  reach('fix');
  const F = fixes();
  $('fxLabel').textContent = S.lvl === 'beginner' || S.usedHint ? 'From your reading' : 'From your answer';
  $('fxText').innerHTML = markText(spokenText(), F);
  $('fxText').querySelectorAll('.err').forEach((e, i) => e.style.animationDelay = `${.5 + i * .35}s`);
  $('fxList').innerHTML = F.map((f, i) => `<li class="fx-item" style="animation-delay:${.9 + i * .18}s">
      <span class="fx-ring" style="--p:${f.before}"><span>${f.before}%</span></span>
      <div class="fx-main"><div class="fx-top"><b>${f.word}</b><span>${f.ipa}</span></div>
      <p class="fx-heard">We heard <q>${f.heard}</q></p><p class="fx-why">${f.issue}</p></div></li>`).join('');
  show('sFix');
  await waitTap($('fxCta'));
}

async function practice(){
  reach('practice');
  const F = fixes(), f = F[0];
  const focusLabel = f.focus === 'stress' ? 'the stress' : `the ${f.focus} sound`;
  $('prTitle').innerHTML = `Let's improve ${focusLabel} in <em>'${f.word}'</em>`;
  $('prText').innerHTML = markText(spokenText(), F, { focus: 0 });
  $('prLabel').textContent = S.lvl === 'beginner' || S.usedHint ? 'From your reading' : 'From your answer';
  $('pwWord').textContent = f.word; $('pwIpa').textContent = f.ipa; $('pwHint').textContent = f.hint;
  $('pwNum').innerHTML = `${f.before}%`; $('pwCap').textContent = 'Current score';
  const card = $('prWord'), btn = $('pwSpeak'), cta = $('prCta');
  card.classList.remove('won'); btn.classList.remove('rec', 'won'); cta.classList.add('cta-hidden');
  $('pwListen').onclick = () => { say(f.word); $('pwListen').classList.add('playing'); setTimeout(() => $('pwListen').classList.remove('playing'), 900); };
  show('sPractice');

  if (!FF){
    await waitTap(btn);
    btn.classList.add('rec');
    await wait(1700);
  }
  btn.classList.remove('rec'); btn.classList.add('won'); card.classList.add('won');
  $('pwCap').textContent = 'New score';
  /* count the score up */
  const num = $('pwNum'), t0 = performance.now(), d = FF ? 1 : 900;
  await new Promise(r => {
    const tick = (now) => {
      const k = Math.min(1, (now - t0) / d), e = 1 - Math.pow(1 - k, 3);
      num.innerHTML = `${Math.round(f.before + (f.after - f.before) * e)}%<span class="pw-delta">+${f.after - f.before}</span>`;
      k < 1 ? requestAnimationFrame(tick) : r();
    };
    requestAnimationFrame(tick);
  });
  const e0 = $('prText').querySelector('.err[data-k="0"]');
  if (e0){ e0.classList.remove('focus'); e0.classList.add('fixed'); }
  await wait(500);
  cta.classList.remove('cta-hidden');
  await waitTap(cta);
}

async function win(){
  reach('win');
  const F = fixes(), f = F[0], s = $('winStream'), cta = $('winCta');
  s.innerHTML = ''; cta.classList.add('cta-hidden');
  show('sWin');
  const talk = async (t) => {
    s.querySelectorAll('.msg').forEach(m => m.classList.add('dim'));
    const row = el(`<div class="msg speaking"><div class="dp"><img src="assets/sarah-chat.png" alt=""></div><div class="bubble"><p>${t}</p></div></div>`);
    s.appendChild(row); await wait(Math.max(1200, t.split(' ').length * 110)); row.classList.remove('speaking');
  };
  await wait(400);
  await talk(`Look at that, ${nm()}! One try and '${f.word}' already sounds clearer.`);
  const ba = el(`<div class="ba-card">
      <div class="ba-head"><div class="ba-w"><b>${f.word}</b><span>${f.ipa}</span></div><div class="ba-gain"><b>+${f.after - f.before}</b><span>points in one try</span></div></div>
      <div class="ba-bars">
        <div class="ba-bar"><span class="l">Before</span><div class="t"><i style="width:${f.before}%"></i></div><span class="v">${f.before}%</span></div>
        <div class="ba-bar after"><span class="l">After</span><div class="t"><i style="width:${f.before}%"></i></div><span class="v">${f.after}%</span></div>
      </div></div>`);
  s.appendChild(ba);
  setTimeout(() => { ba.querySelector('.after i').style.width = `${f.after}%`; }, FF ? 0 : 450);
  await wait(900);
  await talk("That's what 10 minutes a day does. Your first lesson is ready and waiting for you.");
  await sticker('assets/st-sarah_cheer_thumbs_up.png', s);
  cta.classList.remove('cta-hidden');
  await waitTap(cta);
}

async function plan(){
  reach('plan');
  const P = C.PLAN[S.goal], L = C.LEVELS[S.lvl];
  $('plTitle').textContent = P.title;
  $('plSocial').textContent = `${C.LEARNERS} learners are on this journey with you`;
  $('plBody').innerHTML = S.skippedSpeaking
    ? `Based on your level (<b>${L.label}</b>), here's what 10 min of daily practice can do.`
    : `With your current level (<b>${L.cefr}</b>), here’s what<br>10 min of daily practice can do.`;
  $('plBody').classList.remove('show');
  const pts = [[16, 330], [104, 284], [222, 196], [342, 84]];
  const xl = ['Today', 'Week 1', 'Week 4', 'Week 8'];
  const cards = [[-3, 104, 168], [89, 192, 144], [207, 305, 144]];   /* designer's x/width (Paper LKT-0); [1] = bottom offset, ~16px above each dot */
  const seg = (a, b, p0, p3) => {          /* catmull-rom → bezier */
    const c1 = [a[0] + (b[0] - p0[0]) / 6, a[1] + (b[1] - p0[1]) / 6];
    const c2 = [b[0] - (p3[0] - a[0]) / 6, b[1] - (p3[1] - a[1]) / 6];
    return `M${a} C${c1} ${c2} ${b}`;
  };
  const P0 = [pts[0][0] - 60, pts[0][1] + 20], P4 = [pts[3][0] + 60, pts[3][1] - 50];
  const all = [P0, ...pts, P4];
  const segs = [0, 1, 2].map(i => seg(all[i + 1], all[i + 2], all[i], all[i + 3]));
  const area = `M${pts[0]} ` + segs.map(s => s.replace(/^M[^C]+/, '')).join(' ') + ` L${pts[3][0]},350 L${pts[0][0]},350 Z`;
  $('plChart').innerHTML = `<svg viewBox="0 0 364 372" preserveAspectRatio="none">
      <defs><linearGradient id="plGrad" x1="0" x2="1"><stop offset="0" stop-color="#6C63FF"/><stop offset="1" stop-color="#BBB7FF"/></linearGradient>
      <linearGradient id="plFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6C63FF" stop-opacity=".35"/><stop offset="1" stop-color="#6C63FF" stop-opacity="0"/></linearGradient></defs>
      ${[90, 170, 250, 330].map(y => `<line class="pl-grid" x1="0" x2="364" y1="${y}" y2="${y}"/>`).join('')}
      <line x1="0" x2="364" y1="350" y2="350" stroke="rgba(255,255,255,.12)"/>
      <path class="pl-area" d="${area}" fill="url(#plFill)"/>
      ${segs.map((d, i) => `<path class="pl-line" data-i="${i}" d="${d}"/>`).join('')}
      ${pts.map(([x, y], i) => i ? `<line x1="${x}" x2="${x}" y1="${y + 8}" y2="350" stroke="rgba(157,150,255,.28)" stroke-dasharray="2 4"/>` : '').join('')}
      ${pts.map(([x, y], i) => `<g class="pl-dot" data-i="${i}"><circle cx="${x}" cy="${y}" r="${i === 3 ? 9 : 7}" fill="${i === 3 ? '#6C63FF' : '#0F0D25'}" stroke="${i === 0 ? '#8A85B8' : '#BBB7FF'}" stroke-width="2.5"/>${i === 3 ? `<circle cx="${x}" cy="${y}" r="3.5" fill="#fff"/>` : ''}</g>`).join('')}
    </svg>
    ${xl.map((t, i) => `<span class="pl-xl" data-i="${i}" style="left:${pts[i][0]}px">${t}</span>`).join('')}
    ${P.m.map((t, i) => `<div class="pl-card${i === 2 ? ' end' : ''}" data-i="${i}" style="left:${cards[i][0]}px;bottom:${cards[i][1]}px;width:${cards[i][2]}px"><span class="k">${xl[i + 1].toUpperCase()}</span><p>${t}</p></div>`).join('')}`;
  const cta = $('plCta'); cta.classList.add('cta-hidden');
  show('sPlan');
  const lines = [...$('plChart').querySelectorAll('.pl-line')];
  lines.forEach(l => { const n = l.getTotalLength(); l.style.strokeDasharray = n; l.style.strokeDashoffset = n; });
  const q = (sel, i) => $('plChart').querySelector(`${sel}[data-i="${i}"]`);
  await wait(500);
  q('.pl-dot', 0).classList.add('show'); q('.pl-xl', 0).classList.add('on');
  await wait(350);
  for (let i = 0; i < 3; i++){
    const l = lines[i];
    l.style.transition = FF ? 'none' : 'stroke-dashoffset .75s cubic-bezier(.45,0,.25,1)';
    l.style.strokeDashoffset = 0;
    await wait(700);
    q('.pl-dot', i + 1).classList.add('show');
    q('.pl-xl', i).classList.remove('on'); q('.pl-xl', i + 1).classList.add('on');
    await wait(160);
    q('.pl-card', i).classList.add('show');
    await wait(520);
  }
  $('plChart').querySelector('.pl-area').classList.add('show');
  $('plBody').classList.add('show');
  await wait(300);
  cta.classList.remove('cta-hidden');
  await waitTap(cta);
}

/* ============================================================
   THE FLOW
   ============================================================ */
async function run(){
  /* 0 · sign up */
  reach('signup');
  show('sSignup');
  if (!FF) await new Promise(r => document.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', r, { once: true })));

  /* 1 – 2 · hello */
  show('sChat');
  reach('hello');
  setProgress(0, "Let's get started!");
  await hello();

  /* 3 · name (merged with "let's get to know each other") */
  reach('name');
  await sticker('assets/st-hi.png');
  await sarah("Let's get to know each other! What should I call you?");
  earn(6, null);
  S.name = await nameInput();

  /* 4 · native language */
  reach('language');
  await sarah(`Lovely to meet you, ${nm()}! What's your native language?`);
  earn(12, 'Got it!');
  const lang = await chipsQ(C.LANGS.map(l => ({ value: l.value, label: l.value, nat: l.native })), { forced: 'Hindi' });
  S.lang = lang.value;

  /* 5 · app language */
  reach('applang');
  if (S.lang !== 'Other'){
    await sarah(`Do you want to change the app language to ${S.lang}?`, { quick: true });
    earn(18);
    const a = await chipsQ([{ value: 'switch', label: `Switch to ${S.lang}` }, { value: 'en', label: 'Keep it in English' }], { forced: 'en' });
    if (a.value === 'en') sysNote(a.row, 'You can always change this from Settings.');
    else sysNote(a.row, `Done. Sarah will explain in ${S.lang} where it helps.`);
    await wait(500);
  }

  /* 6 · heard from */
  reach('source');
  await sarah(`Quick one, ${nm()}. Where did you hear about us?`, { quick: true });
  earn(25, 'Thanks for telling us!');
  await chipsQ(C.SOURCES.map(s => ({ value: s.value, label: s.value, icon: s.icon })), { forced: 'Instagram' });

  /* 7 + 8 · age and gender, one card */
  reach('about');
  await sarah("Let's get to know more about you! What's your age and gender?");
  earn(37, 'That helps, thank you!');
  await aboutCard();

  /* 9 · phone number (low barrier, Skip for now) */
  reach('reminders');
  await sarah(`Thanks, ${nm()}! To make sure you get the latest lessons, can I have your phone number?`);
  earn(43, "You're all set!");
  const rem = await phoneCard();
  if (rem.on) userChip(`+91 ${rem.phone}`);
  else {
    held = held ? [held[0], held[1], null] : held;
    userChip('Skip for now');
    await sarah('No problem! You can add it anytime in Profile settings.', { quick: true });
  }

  /* 11 · situation */
  reach('situation');
  await sarah('What best describes you right now?');
  earn(50);
  const sit = await chipsQ(C.SITUATIONS.map(s => ({ value: s.key, label: s.label })), { forced: S.sit });
  S.sit = sit.value;

  /* 12 · goal */
  reach('goal');
  await sarah(`I'm glad we met, ${nm()}. What's your main goal for learning English?`);
  const g = await chipsQ(C.GOALS.map(x => ({ value: x.key, label: x.label })), { forced: S.goal });
  S.goal = g.value;
  setProgress(62, `“${goalObj().label}” – ${C.GOAL_CHEER[S.goal]}`);

  /* 13 · personalised reply: goal × situation */
  await sarah(C.GOAL_REPLY[S.goal][S.sit]);

  /* 13b · the pain question */
  reach('pain');
  await sarah('Be honest. What happens when you have to speak English?');
  earn(68, "You're not alone in this.");
  const langName = S.lang === 'Other' ? 'my language' : S.lang;
  const pv = await listQ(C.PAINS.map(p => ({ value: p.key, label: p.label.replace('{lang}', langName) })), S.pain);
  S.pain = pv;
  if (pv === 'other'){
    await sarah('Tell me in a few words. It helps me plan your practice.', { quick: true });
    S.painText = await freeText('e.g. I lose confidence midway');
  }
  await sarah(C.PAINS.find(p => p.key === pv).reply, { quick: true });

  /* 14 · self-rated level */
  reach('level');
  await sarah('What would you say is your current English level?');
  earn(75, 'Almost there!');
  S.lvl = await stackedQ([
    { value: 'beginner',     icon: '🌱', label: 'Beginner',     desc: "I know a few words, but I can't make sentences." },
    { value: 'intermediate', icon: '🌿', label: 'Intermediate', desc: 'I can make short sentences about simple things.' },
    { value: 'advanced',     icon: '🌳', label: 'Advanced',     desc: 'I can have short conversations and understand others.' },
  ], S.lvl);

  /* 14b · social proof, right after the level */
  reach('proof');
  await sarah(`You're in good hands, ${nm()}! Discover why we won Google Play’s Best AI App 2023 and hear from learners like you.`);
  stream.appendChild(el(`<div class="award rated"><img src="assets/rated-badge.png" alt="Rated #1 App in Play Store India"></div>`));
  toEnd(); await wait(700);
  proofRail();
  await wait(3400);

  /* 14c · notifications, asked the way the live app does */
  reach('notify');
  await sarah('Daily practice will help you achieve your goals faster.');
  const nr = await osDialog({ icon: BELL, title: 'Allow <b>Stimuler</b> to send you notifications?', buttons: ['Allow', "Don't allow"] });
  if (nr === 0) await sarah("Thanks for that! Together let's make English a daily learning habit.", { quick: true });
  else { sysPill('Notifications not allowed'); await wait(300); await sarah('No problem. You can turn reminders on later in Profile settings.', { quick: true }); }

  /* 15 – 17 · speaking test */
  reach('test');
  S.testGoal = S.goal;
  setProgress(87, '87% completed');
  let outcome;
  if (S.lvl === 'beginner'){
    await sarah(`We're almost done! As a last step, read this out loud for me.`);
    const card = readCard(test().passage);
    await wait(500);
    outcome = await micTurn({ mode: 'read', card });
    if (outcome === 'done') card.classList.add('done');
  } else {
    await sarah(`We're almost done! Last step: answer this like you would ${test().context}.`);
    const q = questionCard(test().question);
    await wait(500);
    outcome = await micTurn({ mode: 'answer', card: q, hint: true });
    if (outcome === 'hint'){
      S.usedHint = true;
      q.classList.add('dim');
      userChip('Show me a model answer');
      await sarah("Here's one way to say it. Read it out loud:", { quick: true });
      const card = readCard(test().model, 'Model answer');
      await wait(400);
      outcome = await micTurn({ mode: 'read', card });
      if (outcome === 'done') card.classList.add('done');
    }
  }

  if (outcome === 'skip'){
    S.skippedSpeaking = true;
    userChip("I can't speak right now");
    await sarah("No worries! I'll build your plan from your answers, and we'll do your first speaking task together later.");
    bottomBar.classList.remove('gone');
    await wait(600);
    await plan();
    reach('paywall'); show('sPaywall'); return;
  }

  /* 17b · Sarah acknowledges, then the award */
  setProgress(100, 'First speech done!');
  bottomBar.classList.remove('gone');
  await sarah(S.lvl === 'beginner' || S.usedHint
    ? `Well done, ${nm()}! You read that in one go.`
    : `Well done, ${nm()}! You answered in full sentences.`);

  /* 19 · curious? see detailed report */
  await sarah('Curious how well you spoke? Tap to see how you did!');
  const rb = el(`<button class="btn-report">See detailed report</button>`);
  stream.appendChild(rb); toEnd();
  bottomBar.classList.add('gone');
  await waitTap(rb);
  if (!FF){ confetti(rb); await wait(900); }

  /* 20 – 25 */
  await report();
  await result();
  await fix();
  await practice();
  await win();
  await plan();

  /* 26 · paywall (designer-owned) */
  reach('paywall');
  show('sPaywall');
  $('sPaywall').querySelector('.pw-scroll').scrollTop = 0;
}

/* ---------- review panel ---------- */
function panel(){
  const go = (patch) => {
    const p = new URLSearchParams({ goal: S.goal, sit: S.sit, lvl: S.lvl, step: window.__step || 'signup', ...patch });
    if (S.name) p.set('name', S.name);
    location.search = p.toString();
  };
  const chips = (box, arr, cur, key) => {
    $(box).innerHTML = arr.map(([v, t]) => `<button data-v="${v}" class="${v === cur ? 'active' : ''}">${t}</button>`).join('');
    $(box).querySelectorAll('button').forEach(b => b.addEventListener('click', () => go({ [key]: b.dataset.v })));
  };
  chips('dpGoal', C.GOALS.map(g => [g.key, g.short]), S.goal, 'goal');
  chips('dpSit', C.SITUATIONS.map(s => [s.key, s.label.replace(' / Freelancer', '')]), S.sit, 'sit');
  chips('dpLvl', [['beginner', 'Beginner'], ['intermediate', 'Intermediate'], ['advanced', 'Advanced']], S.lvl, 'lvl');
  chips('dpStep', STEPS, TARGET, 'step');
  $('restart').addEventListener('click', () => go({ step: 'signup' }));
}
panel();
run();
