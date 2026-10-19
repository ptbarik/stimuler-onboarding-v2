import json, html, os
A = "paper-asset:///Users/padminibarik/conductor/workspaces/engagement-conversion/bridgetown/.context/prototypes/stimuler-onboarding-v2/assets/"
GE = "font-family:Geist"
ID = "font-family:'Inter Display'"
NAME = "Naina"

def esc(t): return html.escape(t, quote=False)

def est_w(text, px=8.15, pad=36):
    return len(text)*px + pad

# ---------- chat pieces ----------
def header(label, pct, flag_on=False):
    track = 334
    fill = 12 + (track-12)*pct/100
    flag_bg = '#6C63FF' if flag_on else '#26243C'
    flag_fg = '#FFFFFF' if flag_on else '#8A85B8'
    return f'''<div layer-name="Progress header" style="position:absolute;left:0px;top:0px;width:412px;padding:10px 24px 16px 24px;display:flex;flex-direction:column;gap:10px;">
<div style="{GE};font-weight:500;font-size:13.5px;line-height:18px;color:#9D96FF;">{esc(label)}</div>
<div style="display:flex;align-items:center;gap:8px;">
<div style="position:relative;width:{track}px;height:10px;border-radius:999px;background:rgba(255,255,255,0.08);overflow:hidden;"><div layer-name="Fill" style="position:absolute;left:0px;top:0px;width:{fill:.0f}px;height:10px;border-radius:999px;background:linear-gradient(90deg,#6C63FF,#9D96FF);"></div></div>
<div style="width:22px;height:22px;border-radius:999px;background:{flag_bg};display:flex;align-items:center;justify-content:center;flex-shrink:0;"><svg width="12" height="12" viewBox="0 0 16 16"><path d="M4.5 14.5V2" stroke="{flag_fg}" stroke-width="1.6" stroke-linecap="round"/><path d="M4.5 2.6h7.2l-1.7 2.7 1.7 2.7H4.5z" fill="{flag_fg}"/></svg></div>
</div></div>'''

def avatar(size=32):
    return f'<img src="{A}sarah-chat.png" style="width:{size}px;height:{size}px;border-radius:999px;border:1px solid rgba(155,161,231,0.5);background:#1B1D3B;object-fit:cover;object-position:50% 0;flex-shrink:0;">'

def msg(text, state='normal'):
    w = est_w(text)
    width = 'width:300px;' if w > 300 else ''
    border = {'normal':'rgba(137,130,255,0.38)','dim':'rgba(137,130,255,0.22)','speaking':'rgba(187,183,255,0.9)'}[state]
    shadow = 'box-shadow:0 0 26px rgba(157,150,255,0.22);' if state=='speaking' else ''
    color = 'rgba(255,255,255,0.72)' if state=='dim' else '#FFFFFF'
    bg = 'linear-gradient(105deg,#1A1830 30%,#25224A 50%,#1A1830 70%)' if state=='speaking' else '#1A1830'
    return f'''<div layer-name="Sarah" style="display:flex;gap:10px;align-items:flex-start;">{avatar()}<div layer-name="Bubble" style="{width}padding:13px 17px;border-radius:8px 22px 22px 22px;background:{bg};border:1px solid {border};{shadow}"><div style="{GE};font-size:16.5px;line-height:25px;color:{color};">{esc(text)}</div></div></div>'''

def typing():
    dots = ''.join(f'<div style="width:7px;height:7px;border-radius:999px;background:#A9A4BC;opacity:{o};"></div>' for o in (0.35,1,0.35))
    return f'<div layer-name="Sarah · typing" style="display:flex;gap:10px;align-items:flex-start;">{avatar()}<div style="width:70px;height:51px;border-radius:8px 22px 22px 22px;background:#1A1830;border:1px solid rgba(137,130,255,0.38);display:flex;gap:5px;align-items:center;justify-content:center;">{dots}</div></div>'

def chip(text, note=None):
    n = f'<div style="{GE};font-size:12.5px;line-height:17px;color:#726D8C;text-align:right;">{esc(note)}</div>' if note else ''
    return f'<div layer-name="User reply" style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;"><div style="padding:10px 16px;border-radius:16px 6px 16px 16px;background:#6C63FF;border:1px solid #9D96FF;{ID};font-weight:500;font-size:16px;line-height:23px;color:#FFFFFF;">{esc(text)}</div>{n}</div>'

ICONS = {
 'ig':'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#BDB9D6" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/></svg>',
 'yt':'<svg width="16" height="16" viewBox="0 0 24 24" fill="#BDB9D6"><path d="M22 8.2s-.2-1.5-.8-2.1c-.8-.8-1.7-.8-2.1-.9C16.2 5 12 5 12 5s-4.2 0-7.1.2c-.4.1-1.3.1-2.1.9-.6.6-.8 2.1-.8 2.1S2 9.9 2 11.6v1.6c0 1.7.2 3.4.2 3.4s.2 1.5.8 2.1c.8.8 1.9.8 2.4.9 1.7.2 6.6.2 6.6.2s4.2 0 7.1-.2c.4-.1 1.3-.1 2.1-.9.6-.6.8-2.1.8-2.1s.2-1.7.2-3.4v-1.6c0-1.7-.2-3.4-.2-3.4zM9.9 15.1V9.2l5.4 3-5.4 2.9z"/></svg>',
 'play':'<svg width="16" height="16" viewBox="0 0 24 24" fill="#BDB9D6"><path d="M4.2 2.5c-.2.2-.3.6-.3 1v17c0 .4.1.8.3 1l9.4-9.5-9.4-9.5zm10.6 10.6 2.9 2.9-11.6 6.6 8.7-9.5zm0-2.2L6.1 1.4l11.6 6.6-2.9 2.9zm4.3-2.1 3.1 1.8c.9.5.9 1.3 0 1.8l-3.1 1.8-3.2-3.2 3.2-2.2z"/></svg>',
 'people':'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#BDB9D6" stroke-width="1.8" stroke-linecap="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.6 3.3-5.5 6.5-5.5s5.9 1.9 6.5 5.5"/></svg>',
 'fb':'<svg width="16" height="16" viewBox="0 0 24 24" fill="#BDB9D6"><path d="M14 8.5V6.7c0-.8.5-1.2 1.2-1.2H17V2h-2.6C11.6 2 10.5 4 10.5 6.4v2.1H8V12h2.5v10H14V12h2.7l.4-3.5H14z"/></svg>',
 'google':'<svg width="16" height="16" viewBox="0 0 24 24" fill="#BDB9D6"><path d="M21.6 10.2H12v3.9h5.5c-.5 2.5-2.7 3.9-5.5 3.9a6 6 0 0 1 0-12c1.5 0 2.9.6 3.9 1.5l2.9-2.9A10 10 0 1 0 12 22c5.8 0 9.8-4.1 9.8-9.9 0-.6-.1-1.3-.2-1.9z"/></svg>',
 'wa':'<svg width="16" height="16" viewBox="0 0 24 24" fill="#BDB9D6"><circle cx="12" cy="12" r="9" fill="none" stroke="#BDB9D6" stroke-width="1.8"/><path d="M8.5 9.5c.5 2.6 2.4 4.6 5 5.2l1.3-1.3 2 1-.6 1.8c-4.4.2-8.5-3.9-8.4-8.3l1.8-.6 1 2z"/></svg>',
}

def pill(label, sel=False, nat=None, icon=None, small=False):
    bg = '#6C63FF' if sel else '#211F38'
    bd = '#9D96FF' if sel else 'rgba(255,255,255,0.09)'
    pad = '9px 14px' if small else '10px 15px'
    fs = '15px' if small else '15.5px'
    ic = ICONS.get(icon,'') if icon else ''
    if sel and ic: ic = ic.replace('#BDB9D6','#FFFFFF')
    nt = f'<div style="{ID};font-size:14px;line-height:20px;color:{"rgba(255,255,255,0.75)" if sel else "#726D8C"};">{esc(nat)}</div>' if nat else ''
    return f'<div layer-name="Chip" style="display:flex;align-items:center;gap:8px;padding:{pad};border-radius:999px;background:{bg};border:1px solid {bd};flex-shrink:0;">{ic}<div style="{ID};font-weight:500;font-size:{fs};line-height:20px;color:{"#FFFFFF" if sel else "#EDEBF5"};white-space:nowrap;">{esc(label)}</div>{nt}</div>'

def opts(pills, head='Select an option'):
    return f'<div layer-name="Options" style="display:flex;flex-direction:column;align-items:flex-end;gap:10px;"><div style="{ID};font-weight:500;font-size:14.5px;line-height:20px;color:#A9A4BC;">{esc(head)}</div><div style="width:356px;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px;">{"".join(pills)}</div></div>'

def stacked(items, sel=None):
    out = []
    for ic, lab, desc in items:
        s = lab == sel
        out.append(f'<div layer-name="Option" style="width:300px;display:flex;flex-direction:column;gap:6px;padding:13px 17px;border-radius:16px;background:{"#6C63FF" if s else "#211F38"};border:1px solid {"#9D96FF" if s else "rgba(255,255,255,0.08)"};"><div style="display:flex;align-items:center;gap:10px;"><div style="font-size:17px;line-height:22px;">{ic}</div><div style="{ID};font-weight:600;font-size:16.5px;line-height:22px;color:#FFFFFF;">{esc(lab)}</div></div><div style="{GE};font-size:14.5px;line-height:20px;color:{"rgba(255,255,255,0.82)" if s else "#A9A4BC"};">{esc(desc)}</div></div>')
    return f'<div layer-name="Options" style="display:flex;flex-direction:column;align-items:flex-end;gap:10px;"><div style="{ID};font-weight:500;font-size:14.5px;line-height:20px;color:#A9A4BC;">Select an option</div>{"".join(out)}</div>'

def inset(inner, name='Card'):
    return f'<div layer-name="{name}" style="display:flex;padding-left:42px;">{inner}</div>'

def chat_card(inner):
    return inset(f'<div style="width:328px;padding:18px;border-radius:22px;background:rgba(24,22,45,0.92);border:1px solid rgba(255,255,255,0.08);display:flex;flex-direction:column;gap:14px;">{inner}</div>', 'Chat card')

def cap(t): return f'<div style="{ID};font-weight:500;font-size:14px;line-height:18px;color:#A9A4BC;">{esc(t)}</div>'
def wrapchips(pills): return f'<div style="display:flex;flex-wrap:wrap;gap:8px;">{"".join(pills)}</div>'
def wide_cta(t, ready=True): return f'<div layer-name="CTA" style="height:50px;border-radius:999px;background:{"#FFFFFF" if ready else "rgba(255,255,255,0.08)"};display:flex;align-items:center;justify-content:center;"><div style="{ID};font-weight:600;font-size:16px;color:{"#14121A" if ready else "rgba(255,255,255,0.4)"};">{esc(t)}</div></div>'
def link(t): return f'<div style="{ID};font-size:14px;line-height:20px;color:#726D8C;text-decoration:underline;text-align:center;">{esc(t)}</div>'

def sticker(src, w=140):
    sp = lambda l,t,s,c: f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" style="position:absolute;left:{l}px;top:{t}px;"><path d="M12 0c.7 5.9 5.4 10.6 12 12-6.6 1.4-11.3 6.1-12 12-.7-5.9-5.4-10.6-12-12C6.6 10.6 11.3 5.9 12 0Z" fill="{c}"/></svg>'
    return f'<div layer-name="Sticker" style="display:flex;padding-left:40px;"><div style="position:relative;width:{w}px;"><img src="{A}{src}" style="width:{w}px;height:{w}px;display:block;">{sp(-10,22,15,"#BBB7FF")}{sp(w+4,10,10,"#BBB7FF")}</div></div>'

def words(text, lit=0, now=-1, done=False, color_rest='rgba(255,255,255,0.36)', size=21, lh=31, weight=600, gap=6):
    ws = text.split(' ')
    out=[]
    for i,w in enumerate(ws):
        if done: c='#63E39B'
        elif i==now: c='#FFFFFF'
        elif i<lit: c='#BBB7FF'
        else: c=color_rest
        out.append(f'<div style="{ID};font-weight:{weight};font-size:{size}px;line-height:{lh}px;color:{c};">{esc(w)}</div>')
    return f'<div layer-name="Text" style="display:flex;flex-wrap:wrap;column-gap:{gap}px;">{"".join(out)}</div>'

SPK = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg>'
MICI = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>'

def read_card(text, label='Read it out loud', lit=0, now=-1, done=False, question=False):
    if done:
        bg='linear-gradient(180deg,rgba(50,225,141,0.10),rgba(50,225,141,0.03))'; bd='rgba(50,225,141,0.3)'; lc='#BFF6DC'; ic='#BFF6DC'; ib='rgba(126,255,184,0.08)'
    else:
        bg='linear-gradient(180deg,rgba(108,99,255,0.10),rgba(108,99,255,0.03))'; bd='rgba(157,150,255,0.24)'; lc='#A9A4BC'; ic='#D7D4EC'; ib='rgba(255,255,255,0.06)'
    lab = f'<div style="display:flex;align-items:center;gap:8px;">{MICI.format(s=15,c=lc) if question else ""}<div style="{ID};font-weight:500;font-size:14px;line-height:18px;color:{lc};">{esc(label)}</div></div>'
    body = words(text, lit, now, done) if not question else f'<div style="{ID};font-weight:600;font-size:21px;line-height:31px;color:#FFFFFF;">“{esc(text)}”</div>'
    icons = f'<div style="width:34px;height:34px;border-radius:999px;background:{ib};border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;">{SPK.format(c=ic)}</div>'
    return inset(f'<div style="width:328px;padding:18px 18px 16px 18px;border-radius:22px;background:{bg};border:1px solid {bd};box-shadow:inset 0 0 60px rgba(108,99,255,0.12);display:flex;flex-direction:column;gap:12px;">{lab}{body}{icons}</div>', 'Question card' if question else 'Read-aloud card')

def speech(text, final=False, caret=True):
    st = 'background:#6C63FF;border:1px solid #9D96FF;color:#FFFFFF;' if final else 'background:rgba(108,99,255,0.12);border:1px dashed rgba(157,150,255,0.55);color:#E4E1FA;'
    w = 'width:300px;' if est_w(text, 7.9, 34) > 300 else ''
    car = '<div style="width:2px;height:16px;background:#BBB7FF;"></div>' if caret and not final else ''
    tc = '#FFFFFF' if final else '#E4E1FA'
    return f'<div layer-name="Live answer" style="display:flex;justify-content:flex-end;"><div style="{w}padding:12px 16px;border-radius:18px 6px 18px 18px;{st}display:flex;align-items:flex-end;gap:2px;"><div style="{ID};font-weight:500;font-size:15.5px;line-height:23px;color:{tc};">{esc(text)}</div>{car}</div></div>'

def sys_pill(t):
    return f'<div layer-name="System note" style="display:flex;justify-content:center;"><div style="display:flex;align-items:center;gap:7px;padding:7px 13px;border-radius:999px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#A9A4BC" stroke-width="2" stroke-linecap="round"><path d="M13.7 21a2 2 0 0 1-3.4 0M18 8a6 6 0 0 0-9.3-5M6 8c0 7-3 9-3 9h14M3 3l18 18"/></svg><div style="{GE};font-size:12.5px;line-height:16px;color:#A9A4BC;">{esc(t)}</div></div></div>'

def award(): return f'<div layer-name="Award" style="display:flex;justify-content:center;"><img src="{A}best-app.png" style="width:230px;display:block;"></div>'

def report_btn(): return f'<div layer-name="See detailed report" style="display:flex;justify-content:center;"><div style="width:300px;height:54px;border-radius:999px;background:#FFFFFF;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(255,255,255,0.08);"><div style="{ID};font-weight:600;font-size:17px;color:#14121A;">See detailed report</div></div></div>'

STAR = '<svg width="14" height="14" viewBox="0 0 24 24" fill="#FFC94D"><path d="M12 2.5l2.9 6.2 6.6.7-4.9 4.5 1.4 6.6L12 17.2l-5.9 3.3 1.4-6.6L2.6 9.4l6.6-.7z"/></svg>'
def proof(cards):
    cs = ''.join(f'''<div layer-name="Testimonial" style="width:282px;flex-shrink:0;border-radius:20px;padding:18px;display:flex;flex-direction:column;gap:14px;background:linear-gradient(180deg,rgba(108,99,255,0.12),rgba(255,255,255,0.02));border:1px solid rgba(255,255,255,0.12);"><div style="display:flex;gap:2px;">{STAR*5}</div><div style="{ID};font-weight:500;font-size:16.5px;line-height:24px;color:#FFFFFF;">“{esc(q)}”</div><div style="display:flex;align-items:center;gap:10px;"><div style="width:34px;height:34px;border-radius:999px;background:linear-gradient(135deg,#8982FF,#3B368C);display:flex;align-items:center;justify-content:center;"><div style="{ID};font-weight:600;font-size:13px;color:#FFFFFF;">{n[0]}</div></div><div style="display:flex;flex-direction:column;"><div style="{GE};font-weight:600;font-size:14px;line-height:19px;color:#FFFFFF;">{esc(n)}</div><div style="{GE};font-size:12.5px;line-height:17px;color:#A9A4BC;">{esc(m)}</div></div></div></div>''' for q,n,m in cards)
    dots = '<div style="width:16px;height:5px;border-radius:3px;background:#9D96FF;"></div><div style="width:5px;height:5px;border-radius:3px;background:rgba(255,255,255,0.2);"></div><div style="width:5px;height:5px;border-radius:3px;background:rgba(255,255,255,0.2);"></div>'
    return f'''<div layer-name="Social proof" style="display:flex;flex-direction:column;gap:12px;padding-left:42px;"><div style="display:flex;align-items:baseline;gap:8px;"><div style="{ID};font-weight:700;font-size:22px;line-height:28px;color:#FFFFFF;">1,133,400+</div><div style="{ID};font-size:14px;line-height:20px;color:#A9A4BC;">learners in India chose us</div></div><div style="display:flex;gap:12px;width:400px;overflow:hidden;">{cs}</div><div style="display:flex;gap:5px;justify-content:center;">{dots}</div></div>'''

def chat(items, anchor='top', bottom=110, pills=True, skip_dim=False, header_html='', extra=''):
    pos = 'top:0px;' if anchor=='top' else f'bottom:{bottom}px;'
    stream = f'<div layer-name="Chat" style="position:absolute;left:0px;top:66px;width:412px;height:817px;overflow:hidden;"><div layer-name="Stream" style="position:absolute;left:0px;{pos}width:412px;padding:14px 18px 0px 18px;display:flex;flex-direction:column;gap:20px;">{"".join(items)}</div></div>'
    pl = ''
    if pills:
        pl = f'''<div layer-name="Bottom bar" style="position:absolute;left:24px;bottom:40px;width:364px;display:flex;align-items:center;justify-content:space-between;"><div style="display:flex;align-items:center;gap:7px;height:38px;padding:0px 16px;border-radius:999px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.1);"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(233,230,242,0.6)" stroke-width="2" stroke-linecap="round"><path d="M9 9v3a3 3 0 0 0 5.1 2.1M15 9.3V5a3 3 0 0 0-5.9-.8"/><path d="M19 11a7 7 0 0 1-1.1 3.8M5 11a7 7 0 0 0 10.6 6M12 18v3"/><path d="M3 3l18 18"/></svg><div style="{ID};font-weight:600;font-size:14px;color:rgba(233,230,242,0.6);">Mute</div></div><div style="display:flex;align-items:center;gap:4px;height:38px;padding:0px 18px;border-radius:999px;background:#6C63FF;border:1px solid #8982FF;opacity:{0.35 if skip_dim else 1};"><div style="{ID};font-weight:600;font-size:14px;color:#FFFFFF;">Skip</div><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7l5 5-5 5M13 7l5 5-5 5"/></svg></div></div>'''
    return header_html + stream + pl + extra

def micbar(tip='Tap the mic and read', hint=False, rec=False):
    if rec:
        bars = ''.join(f'<div style="width:3px;height:{h}px;border-radius:2px;background:#8982FF;"></div>' for h in (10,18,26,14,30,22,12,28,20,10,24,30,16,22,12,26))
        return f'''<div layer-name="Mic · recording" style="position:absolute;left:58px;bottom:56px;width:296px;height:76px;border-radius:999px;border:1.5px solid rgba(124,92,255,0.6);background:linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.015));box-shadow:0 12px 36px rgba(108,99,255,0.25);display:flex;align-items:center;gap:8px;padding:0px 12px;"><div style="width:42px;height:42px;border-radius:999px;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;flex-shrink:0;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></div><div style="flex-grow:1;display:flex;align-items:center;justify-content:center;gap:3px;height:34px;">{bars}</div><div style="width:50px;height:50px;border-radius:999px;background:#6C63FF;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 4px 14px rgba(108,99,255,0.45);"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg></div></div>'''
    bulb = f'<div layer-name="Hint" style="width:48px;height:48px;border-radius:999px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 6px rgba(157,150,255,0.12),0 0 22px rgba(157,150,255,0.4);"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.6.5 1.1 1.3 1.1 2.2h5c0-.9.5-1.7 1.1-2.2A6 6 0 0 0 12 3z"/></svg></div>' if hint else '<div style="width:48px;height:48px;"></div>'
    return f'''<div layer-name="Mic" style="position:absolute;left:0px;bottom:30px;width:412px;display:flex;flex-direction:column;align-items:center;gap:12px;">
<div style="display:flex;flex-direction:column;align-items:center;"><div style="padding:8px 15px;border-radius:999px;background:#25233B;border:1px solid rgba(255,255,255,0.1);"><div style="{ID};font-weight:500;font-size:13.5px;line-height:18px;color:#E9E6F2;">{esc(tip)}</div></div><svg width="12" height="6" viewBox="0 0 12 6"><path d="M0 0h12L6 6z" fill="#25233B"/></svg></div>
<div style="display:flex;align-items:center;gap:22px;">{bulb}<div layer-name="Mic orb" style="width:76px;height:76px;border-radius:999px;background:radial-gradient(circle at 50% 30%,#B09CFF 0%,#8B71FF 30%,#6A4FF0 66%,#4A2EE0 100%);box-shadow:0 0 0 10px rgba(124,92,255,0.12),0 14px 38px rgba(108,99,255,0.55);display:flex;align-items:center;justify-content:center;">{MICI.format(s=28,c="#FFFFFF")}</div><div style="width:48px;height:48px;"></div></div>
<div style="{ID};font-size:13.5px;line-height:18px;color:#726D8C;text-decoration:underline;">I can't speak right now</div></div>'''

def os_dialog(title_parts, buttons, icon='bell'):
    ic = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A8C7FA" stroke-width="1.8" stroke-linecap="round"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0"/></svg>' if icon=='bell' else MICI.format(s=24,c='#A8C7FA')
    bt = ''.join(f'<div style="width:260px;height:46px;border-radius:22px;background:#D3E3FD;display:flex;align-items:center;justify-content:center;"><div style="font-family:Roboto;font-weight:500;font-size:14.5px;color:#0B1D3A;">{esc(b)}</div></div>' for b in buttons)
    return f'''<div layer-name="OS dialog" style="position:absolute;left:0px;top:-34px;width:412px;height:917px;background:rgba(5,4,12,0.62);display:flex;align-items:center;justify-content:center;"><div style="width:300px;padding:24px 20px 20px 20px;border-radius:28px;background:#2B2A33;display:flex;flex-direction:column;align-items:center;gap:8px;">{ic}<div style="font-family:Roboto;font-size:19px;line-height:26px;color:#E3E3E8;text-align:center;padding:6px 0px 12px 0px;">{esc(title_parts)}</div>{bt}</div></div>'''

# ---------- takeover pieces ----------
def tk_head(kicker, title_parts, sub=None, extra=''):
    t = ''.join(f'<div style="{ID};font-weight:700;font-size:28px;line-height:34px;letter-spacing:-0.02em;color:{"#9D96FF" if hl else "#FFFFFF"};">{esc(x)}</div>' for x,hl in title_parts)
    s = f'<div style="{GE};font-size:16px;line-height:24px;color:#B4B0C8;">{esc(sub)}</div>' if sub else ''
    return f'<div layer-name="Header" style="position:absolute;left:24px;top:28px;width:364px;display:flex;flex-direction:column;gap:10px;"><div style="{GE};font-weight:600;font-size:12px;letter-spacing:0.16em;line-height:16px;color:#8F8AB3;">{esc(kicker.upper())}</div><div style="display:flex;flex-wrap:wrap;column-gap:8px;">{t}</div>{s}{extra}</div>'

def cta(t): return f'<div layer-name="CTA" style="position:absolute;left:24px;bottom:40px;width:364px;height:54px;border-radius:999px;background:#FFFFFF;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,0.25);"><div style="{ID};font-weight:600;font-size:17px;color:#14121A;">{esc(t)}</div></div>'

CHECK = '<svg width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="10" fill="rgba(79,209,165,0.16)"/><path d="M6 10.3l2.7 2.7 5.3-5.8" fill="none" stroke="#4FD1A5" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
TICK = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'

def marked(text, errs, state={}, size=21, lh=38, rest='rgba(255,255,255,0.55)'):
    out=[]
    for w in text.split(' '):
        core = w.rstrip('.,!?'); punct = w[len(core):]
        k = next((i for i,e in enumerate(errs) if e.lower()==core.lower()), None)
        if k is None:
            out.append(f'<div style="{ID};font-weight:500;font-size:{size}px;line-height:{lh}px;color:{rest};">{esc(w)}</div>')
        else:
            stt = state.get(k,'err')
            if stt=='fixed': bg,bd,c='rgba(50,225,141,0.16)','rgba(50,225,141,0.55)','#63E39B'
            elif stt=='focus': bg,bd,c='#6C63FF','#BBB7FF','#FFFFFF'
            else: bg,bd,c='rgba(108,99,255,0.26)','rgba(157,150,255,0.6)','#FFFFFF'
            pdiv = f'<div style="{ID};font-weight:500;font-size:{size}px;line-height:{lh}px;color:{rest};">{esc(punct)}</div>' if punct else ''
            out.append(f'<div style="display:flex;align-items:center;gap:1px;"><div style="padding:0px 8px;border-radius:9px;background:{bg};border:1px solid {bd};"><div style="{ID};font-weight:600;font-size:{size}px;line-height:{lh-8}px;color:{c};">{esc(core)}</div></div>{pdiv}</div>')
    return f'<div layer-name="Text" style="display:flex;flex-wrap:wrap;column-gap:6px;row-gap:4px;align-items:center;">{"".join(out)}</div>'

def glass(inner, top, pad='26px 22px', name='Card'):
    return f'<div layer-name="{name}" style="position:absolute;left:24px;top:{top}px;width:364px;padding:{pad};border-radius:24px;overflow:hidden;background:linear-gradient(180deg,rgba(108,99,255,0.10),rgba(24,22,45,0.6));border:1px solid rgba(157,150,255,0.22);display:flex;flex-direction:column;gap:12px;"><div style="position:absolute;left:42px;top:-60px;width:280px;height:160px;border-radius:999px;background:radial-gradient(closest-side,rgba(137,130,255,0.32),rgba(137,130,255,0));"></div>{inner}</div>'

exec(open('/tmp/paper/helpers2.py').read())
S = {}; NOTES = {}

# ================= MAIN PATH =================
first = "Hi! I'm Sarah, your personal English speaking partner."
ask_name = "Let's get to know each other! What should I call you?"
ask_lang = f"Lovely to meet you, {NAME}! What's your native language?"
ask_app = "Do you want to change the app language to Hindi?"
ask_src = f"Quick one, {NAME}. Where did you hear about us?"
ask_about = "Let's get to know more about you! What's your age and gender?"
ask_rem = f"Thanks, {NAME}! Want me to remind you once a day so your practice stays on track?"
ask_sit = "What best describes you right now?"
ask_goal = f"I'm glad we met, {NAME}. What's your main goal for learning English?"
reply = "Love that! Speaking up in class gets so much easier once English stops feeling like a test. We'll practise the real moments: answering your teacher, presentations and group work."
ask_lvl = "What would you say is your current English level?"
ask_read = "We're almost done! As a last step, read this out loud for me."
passage = "I enjoy my classes. Today I will present my project and share my thoughts with the class."
LANGS = [('Hindi','हिन्दी'),('Tamil','தமிழ்'),('Telugu','తెలుగు'),('Marathi','मराठी'),('Bengali','বাংলা'),('Kannada','ಕನ್ನಡ'),('Malayalam','മലയാളം'),('Gujarati','ગુજરાતી'),('Punjabi','ਪੰਜਾਬੀ'),('Odia','ଓଡ଼ିଆ'),('Other',None)]
SRC = [('Instagram','ig'),('YouTube','yt'),('Play Store search','play'),('Friends or family','people'),('Facebook','fb'),('Google','google'),('WhatsApp','wa'),('Other',None)]
SITS = ['Student','Working professional','Self-employed / Freelancer','Business owner','Looking for work','Homemaker','Career break','Parent']
GOALS = ['IELTS','Grow in my career','Personal growth','Travel confidently','Excel at my school','Other']
LVLS = [('🌱','Beginner',"I know a few words, but I can't make sentences."),('🌿','Intermediate','I can make short sentences about simple things.'),('🌳','Advanced','I can have short conversations and understand others.')]

# S01 hello
S['S01'] = f'''<div layer-name="Glow" style="position:absolute;left:-4px;top:110px;width:420px;height:420px;border-radius:999px;background:radial-gradient(circle,rgba(108,99,255,0.22),rgba(108,99,255,0.06) 45%,rgba(108,99,255,0) 70%);"></div>
<img layer-name="Sarah" src="{A}sarah-hi.png" style="position:absolute;left:174px;top:214px;width:150px;height:406px;object-fit:cover;">
<div layer-name="Bubble · shining" style="position:absolute;left:58px;top:228px;padding:11px 16px;border-radius:18px 18px 6px 18px;background:#1A1830;border:1.5px solid rgba(187,183,255,0.9);box-shadow:0 0 26px rgba(157,150,255,0.3);"><div style="{GE};font-size:16px;line-height:22px;color:#FFFFFF;white-space:nowrap;">Hi, I'm Sarah 👋</div></div>'''
NOTES['S01'] = ("Sarah says hi", "Sarah springs up (spring ease, 0.9s), the bubble pops in 0.5s later. Its border shines: a light sweeps around the edge while Sarah speaks.")

S['S02'] = chat([msg(first,'speaking')], header_html=header("Let's get started!",0))
NOTES['S02'] = ("Into the chat", "Sarah's photo shrinks into the avatar circle and the bubble slides up into the first chat message (0.8s, ease in-out). The text cross-fades. The progress header and Mute / Skip fade in.")

S['S03'] = chat([msg(first,'dim'), sticker('st-hi.png'), msg(ask_name),
  f'<div layer-name="Name input" style="display:flex;flex-direction:column;align-items:flex-end;gap:10px;"><div style="width:260px;padding:13px 16px;border-radius:16px;background:rgba(255,255,255,0.05);border:1px solid #8982FF;box-shadow:0 0 0 4px rgba(108,99,255,0.14);display:flex;align-items:center;gap:1px;"><div style="{ID};font-weight:500;font-size:16.5px;line-height:22px;color:#FFFFFF;">Naina</div><div style="width:2px;height:20px;background:#8982FF;"></div></div><div style="padding:12px 26px;border-radius:999px;background:#FFFFFF;"><div style="{ID};font-weight:600;font-size:15.5px;color:#14121A;">Continue</div></div></div>'],
  header_html=header("Let's get started!",0), skip_dim=True)
NOTES['S03'] = ("Name", "\"Let's get to know each other\" and the name question are one message. Continue turns white once 2+ letters are typed. Skip dims while a question is waiting.")

S['S04'] = chat([msg(ask_name,'dim'), chip(NAME), msg(ask_lang), opts([pill(l, nat=n) for l,n in LANGS])],
  anchor='bottom', header_html=header("6% completed",6), skip_dim=True)
NOTES['S04'] = ("Native language", "Pill chips wrap right-aligned (Gift Sense pattern) with the language in its own script. Tap: the chip fills indigo, sparks fly to the progress bar, the answer drops into the chat.")

S['S05'] = chat([msg(ask_lang,'dim'), chip('Hindi'), msg(ask_app), opts([pill('Switch to Hindi'), pill('Keep it in English')])],
  anchor='bottom', header_html=header("12% completed",12), skip_dim=True)
NOTES['S05'] = ("App language", "Two chips. If she keeps English, a grey line appears under her answer: \"You can always change this from Settings.\" (see next screen).")

S['S06'] = chat([msg(ask_app,'dim'), chip('Keep it in English', 'You can always change this from Settings.'), msg(ask_src), opts([pill(l, icon=i) for l,i in SRC])],
  anchor='bottom', header_html=header("18% completed",18), skip_dim=True)
NOTES['S06'] = ("Heard from", "Same chip style as languages, with a small source icon.")

S['S07'] = chat([msg(ask_src,'dim'), chip('Instagram'), msg(ask_about),
  chat_card(cap('Age') + wrapchips([pill(a, sel=(a=='18–24'), small=True) for a in ['Under 18','18–24','25–34','35–44','45+']]) + cap('Gender') + wrapchips([pill(g, sel=(g=='Female'), small=True) for g in ['Male','Female','Non-binary','Prefer not to say']]) + wide_cta('Done'))],
  anchor='bottom', header_html=header("25% completed",25), skip_dim=True)
NOTES['S07'] = ("Age + gender", "Frames 7 and 8 merged into one card. Done turns white once both rows have an answer; her reply reads \"18–24 · Female\".")

remcard = chat_card(cap('Remind me at') + wrapchips([pill(t, sel=(t=='8:30 PM'), small=True) for t in ['7:30 AM','1:00 PM','8:30 PM']]) +
  f'<div style="display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);"><div style="{ID};font-weight:600;font-size:15.5px;color:#FFFFFF;">+91</div><div style="width:1px;height:20px;background:rgba(255,255,255,0.18);"></div><div style="flex-grow:1;{ID};font-size:15.5px;color:rgba(255,255,255,0.35);">WhatsApp no. (optional)</div>{ICONS["wa"].replace("#BDB9D6","#5FD38B")}</div>' +
  wide_cta('Turn on reminders') + link('Not now'))
S['S08'] = chat([msg(ask_about,'dim'), chip('18–24 · Female'), msg(ask_rem), remcard], anchor='bottom', header_html=header("37% completed",37), skip_dim=True)
NOTES['S08'] = ("Reminders", "Frames 9 + 10: time chips (8:30 PM pre-selected), optional WhatsApp number with +91, a white \"Turn on reminders\" and a quiet \"Not now\".")

S['S09'] = chat([msg(ask_about,'dim'), chip('18–24 · Female'), msg(ask_rem), remcard], anchor='bottom', header_html=header("37% completed",37), skip_dim=True,
  extra=os_dialog('Allow Stimuler to send you notifications?', ['Allow',"Don't allow"]))
NOTES['S09'] = ("Notification permission", "The Android prompt appears over the chat. Allow → \"Done! I'll nudge you at 8:30 PM.\" Don't allow → see branch B01.")

S['S10'] = chat([msg(ask_rem,'dim'), chip('Remind me at 8:30 PM'), msg("Done! I'll nudge you at 8:30 PM.",'dim'), msg(ask_sit), opts([pill(s) for s in SITS])],
  anchor='bottom', header_html=header("43% completed",43), skip_dim=True)
NOTES['S10'] = ("Situation", "8 chips: Student, Working professional, Self-employed / Freelancer, Business owner, Looking for work, Homemaker, Career break, Parent.")

S['S11'] = chat([msg(ask_sit,'dim'), chip('Student'), msg(ask_goal), opts([pill(g) for g in GOALS])],
  anchor='bottom', header_html=header("50% completed",50), skip_dim=True)
NOTES['S11'] = ("Goal", "Same chip style. Once she picks, the header label changes to her goal with a cheer, e.g. \"Excel at my school\" – Impressive!")

S['S12'] = chat([msg(ask_goal,'dim'), chip('Excel at my school'), msg(reply,'speaking')],
  anchor='bottom', header_html=header("“Excel at my school” – Impressive!",62))
NOTES['S12'] = ("Personalised reply", "Sarah's reply is written for each goal × situation (48 versions in content.js). Shown: Excel at my school × Student.")

S['S13'] = chat([msg(reply,'dim'), msg(ask_lvl), stacked(LVLS)],
  anchor='bottom', header_html=header("“Excel at my school” – Impressive!",62), skip_dim=True)
NOTES['S13'] = ("Self-rated level", "Stacked cards with a short description. Beginner reads a passage; Intermediate and Advanced answer a question (branch B02).")

S['S14'] = chat([msg(ask_lvl,'dim'), chip('Beginner'), msg(ask_read), read_card(passage)], anchor='bottom', bottom=226, pills=False,
  header_html=header("87% completed",87), extra=micbar())
NOTES['S14'] = ("Read it out loud", "The read card slides in, Mute / Skip slide away and the mic orb rises with a soft pulse and a floating \"Tap the mic and read\" tip.")

S['S15'] = chat([msg(ask_lvl,'dim'), chip('Beginner'), msg(ask_read), read_card(passage)], anchor='bottom', bottom=226, pills=False,
  header_html=header("87% completed",87), extra=micbar() + os_dialog('Allow Stimuler to record audio?', ['While using the app','Only this time',"Don't allow"], icon='mic'))
NOTES['S15'] = ("Mic permission", "First tap on the mic asks for audio. Don't allow → Sarah: \"I'll need your mic to hear you. Tap it again whenever you're ready.\"")

S['S16'] = chat([msg(ask_lvl,'dim'), chip('Beginner'), msg(ask_read), read_card(passage, lit=8, now=8)], anchor='bottom', bottom=226, pills=False,
  header_html=header("87% completed",87), extra=micbar(rec=True))
NOTES['S16'] = ("Recording", "The orb stretches into a pill (× · waveform · ✓). Words light up as they're heard: the current word glows white, read words turn lavender.")

S['S17'] = chat([chip('Beginner'), msg(ask_read,'dim'), read_card(passage, done=True), msg(f"Well done, {NAME}! You read that in one go.",'dim'),
  msg("That was great! Now it's time for you to experience why we won Google Play's Best AI App 2023.",'speaking'), award()],
  anchor='bottom', header_html=header("First speech done!",100, flag_on=True))
NOTES['S17'] = ("Well done + award", "The card turns green, the bar fills and the flag lights up. Sarah's congratulation lands in a bubble at the bottom, then the Best AI App 2023 badge pops in.")

PROOF = [("I used to stay quiet in class. Now I'm usually the first one to answer.","Ananya S.","Class 11 · Pune"),
         ("My viva went so well. I didn't freeze even once.","Rohit K.","B.Com student · Delhi")]
S['S18'] = chat([msg("That was great! Now it's time for you to experience why we won Google Play's Best AI App 2023.",'dim'), award(), msg("Here’s what learners like you are saying:"), proof(PROOF)],
  anchor='bottom', header_html=header("First speech done!",100, flag_on=True))
NOTES['S18'] = ("Social proof", "Carousel of reviews matched to her goal. Auto-slides every 3s, swipe to browse, dots follow. Reviews are placeholders.")

S['S19'] = chat([msg("Here’s what learners like you are saying:",'dim'), proof(PROOF), msg("Curious how well you spoke? Tap to see how you did!",'speaking'), report_btn()],
  anchor='bottom', bottom=60, pills=False, header_html=header("First speech done!",100, flag_on=True))
NOTES['S19'] = ("See detailed report", "White CTA with a slow sheen. Tap: a confetti burst, then the report screen.")

# S20 analysing
ticks = ['Checking pronunciation','Checking fluency and pauses','Checking grammar','Matching this to your goal: Excel at my school']
tk = ''.join(f'<div style="display:flex;align-items:flex-start;gap:12px;"><div style="width:22px;height:22px;border-radius:999px;background:#6C63FF;display:flex;align-items:center;justify-content:center;flex-shrink:0;">{TICK}</div><div style="{GE};font-size:15.5px;line-height:22px;color:#E9E6F2;">{esc(t)}</div></div>' for t in ticks)
S['S20'] = f'''<div layer-name="Report" style="position:absolute;left:32px;top:56px;width:348px;display:flex;flex-direction:column;align-items:center;">
<div style="position:relative;width:156px;height:156px;"><div style="position:absolute;left:-8px;top:-8px;width:172px;height:172px;border-radius:999px;border:2px solid rgba(157,150,255,0.35);"></div><img src="{A}sarah-report.png" style="width:156px;height:156px;border-radius:999px;border:1px solid rgba(255,255,255,0.12);"></div>
<div style="padding-top:30px;{ID};font-weight:600;font-size:24px;line-height:31px;text-align:center;color:#FFFFFF;">Putting your report<br>together…</div>
<div style="padding-top:26px;width:348px;"><div style="padding:18px;border-radius:20px;background:rgba(24,22,45,0.75);border:1px solid rgba(255,255,255,0.08);display:flex;flex-direction:column;gap:14px;">{tk}</div></div>
<div style="padding-top:18px;{GE};font-size:13.5px;color:#726D8C;">Takes about 5 seconds, yep we're that fast!</div></div>''' + cta('Continue')
NOTES['S20'] = ("Analysing", "A ring spins around Sarah. Each line gets a spinner, then a tick (0.85s each). The last line names her goal. Continue rises when all four are done.")

# S21 level
lad = [('Native','C2','future'),('Proficient','C1','future'),('Advanced','B2','future'),('Intermediate','B1','next'),('Beginner','A2','here'),('Novice','A1','past')]
rows=[]
for name,cefr,st in lad:
    if st=='here': rb='background:linear-gradient(90deg,#625AE8,#8982FF);border:1px solid #BBB7FF;box-shadow:0 0 0 4px rgba(108,99,255,0.18),0 8px 26px rgba(108,99,255,0.45);'; rc='#FFFFFF'; nc='#FFFFFF'; nw=600
    elif st=='next': rb='background:rgba(108,99,255,0.08);border:1.5px dashed #9D96FF;'; rc='#BBB7FF'; nc='#BBB7FF'; nw=500
    elif st=='past': rb='background:#34306A;border:1px solid rgba(157,150,255,0.15);'; rc='#C9C5FF'; nc='#A9A4BC'; nw=500
    else: rb='background:#24223A;border:1px solid rgba(255,255,255,0.05);'; rc='#5E5A7A'; nc='#726D8C'; nw=500
    ann=''
    if st=='here': ann=f'<div style="display:flex;flex-direction:column;"><div style="{ID};font-weight:600;font-size:15px;line-height:20px;color:#FFFFFF;">You\'re here</div><div style="{GE};font-size:12.5px;line-height:16px;color:#A9A4BC;">“Short sentences”</div></div>'
    if st=='next': ann=f'<div style="display:flex;flex-direction:column;"><div style="{ID};font-weight:600;font-size:15px;line-height:20px;color:#BBB7FF;">Next stop</div><div style="{GE};font-size:12.5px;line-height:16px;color:#A9A4BC;">Fewer pauses</div></div>'
    rows.append(f'<div layer-name="{name}" style="display:flex;align-items:center;gap:10px;height:50px;"><div style="width:96px;{ID};font-weight:{nw};font-size:14px;text-align:right;color:{nc};">{name}</div><div style="width:76px;height:50px;border-radius:14px;{rb}display:flex;align-items:center;justify-content:center;"><div style="{ID};font-weight:600;font-size:13px;color:{rc};">{cefr}</div></div><div style="width:30px;"></div>{ann}</div>')
arrow = '<svg layer-name="Curved arrow" width="30" height="62" viewBox="0 -2 30 62" style="position:absolute;left:192px;top:205px;overflow:visible;"><path d="M0 60 C 28 60 28 0 3 0" fill="none" stroke="#9D96FF" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 5"/><path d="M9 -5 L3 0 L9 5" fill="none" stroke="#9D96FF" stroke-width="2" stroke-linecap="round"/></svg>'
well = ''.join(f'<div style="display:flex;gap:10px;align-items:flex-start;">{CHECK}<div style="{GE};font-size:15px;line-height:21px;color:#F2F1F7;">{esc(t)}</div></div>' for t in ["You read the whole passage without stopping.","'classes' and 'today' were clear."])
S['S21'] = tk_head('Your level', [("You're a",False),("Beginner",True)], 'You can say simple sentences, but you slow down on longer words.') + \
  f'<div layer-name="Ladder" style="position:absolute;left:24px;top:192px;width:364px;display:flex;flex-direction:column;gap:10px;">{"".join(rows)}{arrow}</div>' + \
  f'<div layer-name="What you did well" style="position:absolute;left:24px;bottom:118px;width:364px;display:flex;flex-direction:column;gap:10px;"><div style="{GE};font-weight:600;font-size:11px;letter-spacing:0.16em;color:#8F8AB3;">WHAT YOU DID WELL</div>{well}</div>' + cta('Continue')
NOTES['S21'] = ("Your level", "Rungs fill bottom-up to her level, which pops with a glow and \"You're here\". A dashed curved arrow draws up to \"Next stop\". \"What you did well\" quotes what she actually said.")

ERRS = ['project','thoughts']
fx_list = ''.join(f'<div style="display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:16px;background:rgba(24,22,45,0.8);border:1px solid rgba(255,255,255,0.08);"><div style="width:88px;{ID};font-weight:600;font-size:16px;color:#FFFFFF;">{w}</div><div style="flex-grow:1;{GE};font-size:14px;line-height:19px;color:#A9A4BC;">{why}</div><div style="padding:5px 10px;border-radius:999px;background:rgba(108,99,255,0.16);"><div style="{ID};font-weight:600;font-size:14px;color:#C9C5FF;">{sc}%</div></div></div>' for w,why,sc in [('thoughts',"The 'th' sound was unclear",44),('project','Stress on the wrong part',52)])
S['S22'] = tk_head('Quick fix', [('Two words need',False),('a little work',False)], "Let's correct them before we build your plan.") + \
  glass(f'<div style="position:relative;{ID};font-weight:500;font-size:13.5px;color:#A9A4BC;">From your reading</div><div style="position:relative;">{marked(passage, ERRS)}</div>', 200, '30px 24px', 'Passage') + \
  f'<div layer-name="Words to fix" style="position:absolute;left:24px;top:470px;width:364px;display:flex;flex-direction:column;gap:10px;">{fx_list}</div>' + cta("Let's correct them")
NOTES['S22'] = ("Errors", "Indigo glass card (no yellow). The two words light up one after another with a soft glow; the rows below say what was off and today's score.")

def practice(after=False):
    head = tk_head('Practice', [("Let's improve the 'th' sound",False),("in 'thoughts'",True)])
    st = {0:'fixed' if after else 'focus', 1:'err'}
    errs = ['thoughts','project']
    psg = glass(f'<div style="position:relative;">{marked(passage, errs, st, size=17, lh=31)}</div>', 150, '18px 20px', 'Passage')
    cue = f'<div style="position:absolute;left:24px;top:336px;width:364px;display:flex;justify-content:center;gap:5px;"><div style="{GE};font-weight:600;font-size:12px;letter-spacing:0.16em;color:#8F8AB3;">READ THE WORD</div><div style="{GE};font-weight:600;font-size:12px;letter-spacing:0.16em;color:#FFFFFF;">OUT LOUD</div></div>'
    if after:
        score = f'<div style="display:flex;flex-direction:column;"><div style="display:flex;align-items:baseline;gap:8px;"><div style="{ID};font-weight:700;font-size:32px;line-height:36px;color:#63E39B;">81%</div><div style="{ID};font-weight:600;font-size:15px;color:#63E39B;">+37</div></div><div style="{GE};font-size:12.5px;color:#A9A4BC;">New score</div></div>'
        btn = f'<div style="height:50px;min-width:170px;padding:0px 20px;border-radius:999px;background:rgba(50,225,141,0.14);border:1px solid rgba(50,225,141,0.45);display:flex;align-items:center;justify-content:center;gap:8px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#63E39B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg><div style="{ID};font-weight:600;font-size:15.5px;color:#63E39B;">Sounds clear</div></div>'
        cardst = 'border:1px solid rgba(50,225,141,0.35);background:linear-gradient(180deg,rgba(50,225,141,0.08),rgba(24,22,45,0.85));'
    else:
        score = f'<div style="display:flex;flex-direction:column;"><div style="{ID};font-weight:700;font-size:32px;line-height:36px;color:#FFFFFF;">44%</div><div style="{GE};font-size:12.5px;color:#A9A4BC;">Current score</div></div>'
        btn = f'<div style="height:50px;min-width:170px;padding:0px 20px;border-radius:999px;background:linear-gradient(180deg,#8982FF,#625AE8);box-shadow:0 8px 24px rgba(108,99,255,0.45);display:flex;align-items:center;justify-content:center;gap:8px;">{MICI.format(s=18,c="#FFFFFF")}<div style="{ID};font-weight:600;font-size:15.5px;color:#FFFFFF;">Tap to speak</div></div>'
        cardst = 'border:1px solid rgba(255,255,255,0.08);background:rgba(24,22,45,0.85);'
    card = f'''<div layer-name="Word card" style="position:absolute;left:24px;top:366px;width:364px;padding:20px;border-radius:24px;{cardst}display:flex;flex-direction:column;gap:12px;">
<div style="display:flex;justify-content:space-between;align-items:flex-start;"><div style="display:flex;flex-direction:column;gap:2px;"><div style="{ID};font-weight:700;font-size:34px;line-height:40px;letter-spacing:-0.02em;color:#FFFFFF;">thoughts</div><div style="{GE};font-size:14px;color:#A9A4BC;">/θɔːts/</div></div><div style="width:40px;height:40px;border-radius:999px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;">{SPK.format(c="#E6E3F7")}</div></div>
<div style="padding:10px 12px;border-radius:12px;background:rgba(255,255,255,0.04);"><div style="{GE};font-size:14.5px;line-height:20px;color:#C9C5DD;">Tongue between your teeth for 'th', then 'awts'</div></div>
<div style="display:flex;align-items:flex-end;justify-content:space-between;">{score}{btn}</div></div>'''
    return head + psg + cue + card + (cta('Continue') if after else '')
S['S23'] = practice(False)
NOTES['S23'] = ("Practice the word", "The word she's fixing is filled indigo in the passage. Listen plays the word. Tap to speak → the button becomes a live waveform for ~1.7s.")
S['S24'] = practice(True)
NOTES['S24'] = ("Improved score", "The score counts up 44 → 81% (+37) and turns green, the word in the passage turns green, and Continue rises.")

ba = f'''<div layer-name="Before / after" style="display:flex;padding-left:42px;"><div style="width:328px;padding:18px;border-radius:22px;background:rgba(24,22,45,0.9);border:1px solid rgba(50,225,141,0.28);display:flex;flex-direction:column;gap:14px;"><div style="display:flex;flex-direction:column;"><div style="{ID};font-weight:700;font-size:28px;line-height:34px;color:#FFFFFF;">thoughts</div><div style="{GE};font-size:13.5px;color:#A9A4BC;">/θɔːts/</div></div><div style="height:1px;background:rgba(255,255,255,0.08);"></div><div style="display:flex;align-items:center;gap:10px;"><div style="padding:7px 12px;border-radius:10px;background:rgba(255,255,255,0.06);"><div style="{ID};font-weight:600;font-size:14px;color:#A9A4BC;">Before 44</div></div><div style="{GE};color:#726D8C;">→</div><div style="padding:7px 12px;border-radius:10px;background:rgba(50,225,141,0.14);"><div style="{ID};font-weight:600;font-size:14px;color:#63E39B;">After 81</div></div><div style="flex-grow:1;text-align:right;{ID};font-weight:700;font-size:18px;color:#63E39B;">+37</div></div></div></div>'''
S['S25'] = header("Nice work!",100,flag_on=True) + f'<div layer-name="Chat" style="position:absolute;left:0px;bottom:120px;width:412px;padding:0px 18px;display:flex;flex-direction:column;gap:16px;">{msg(f"Look at that, {NAME}! One try and ‘thoughts’ already sounds clearer.","dim")}{ba}{msg("That’s what 10 minutes a day does. ‘project’ is waiting for you in your Day 1 plan.")}{sticker("st-sarah_cheer_thumbs_up.png")}</div>' + cta('Start my plan')
NOTES['S25'] = ("Quick win", "Sarah congratulates her in the chat, shows before → after, and points to the second word in Day 1. \"Start my plan\" rises last.")

pts=[(16,330),(104,284),(222,196),(342,84)]
def seg(a,b,p0,p3):
    c1=(a[0]+(b[0]-p0[0])/6, a[1]+(b[1]-p0[1])/6); c2=(b[0]-(p3[0]-a[0])/6, b[1]-(p3[1]-a[1])/6)
    return c1,c2
allp=[(pts[0][0]-60,pts[0][1]+20)]+pts+[(pts[3][0]+60,pts[3][1]-50)]
d=f"M{pts[0][0]} {pts[0][1]}"
for i in range(3):
    c1,c2=seg(allp[i+1],allp[i+2],allp[i],allp[i+3]); d+=f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {allp[i+2][0]} {allp[i+2][1]}"
area=d+f" L{pts[3][0]} 350 L{pts[0][0]} 350 Z"
grid=''.join(f'<line x1="0" x2="364" y1="{y}" y2="{y}" stroke="rgba(255,255,255,0.06)"/>' for y in (90,170,250,330))
vl=''.join(f'<line x1="{x}" x2="{x}" y1="{y+8}" y2="350" stroke="rgba(157,150,255,0.28)" stroke-dasharray="2 4"/>' for x,y in pts[1:])
dots=''.join(f'<circle cx="{x}" cy="{y}" r="{9 if i==3 else 7}" fill="{"#6C63FF" if i==3 else "#0F0D25"}" stroke="{"#8A85B8" if i==0 else "#BBB7FF"}" stroke-width="2.5"/>' for i,(x,y) in enumerate(pts)) + f'<circle cx="{pts[3][0]}" cy="{pts[3][1]}" r="3.5" fill="#FFFFFF"/>'
svg=f'<svg layer-name="Graph" width="364" height="372" viewBox="0 0 364 372" style="position:absolute;left:0px;top:0px;"><defs><linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="#6C63FF"/><stop offset="1" stop-color="#BBB7FF"/></linearGradient><linearGradient id="g2" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6C63FF" stop-opacity="0.35"/><stop offset="1" stop-color="#6C63FF" stop-opacity="0"/></linearGradient></defs>{grid}<line x1="0" x2="364" y1="350" y2="350" stroke="rgba(255,255,255,0.12)"/><path d="{area}" fill="url(#g2)"/><path d="{d}" fill="none" stroke="url(#g1)" stroke-width="3.5" stroke-linecap="round"/>{vl}{dots}</svg>'
xl=''.join(f'<div style="position:absolute;left:{x-30}px;top:356px;width:60px;text-align:center;{GE};font-size:12.5px;font-weight:{600 if i==3 else 400};color:{"#FFFFFF" if i==3 else "#726D8C"};">{t}</div>' for i,((x,y),t) in enumerate(zip(pts,['Today','Week 1','Week 4','Week 8'])))
cards=[(40,196,'WEEK 1','Introduce yourself in class without pausing'),(120,108,'WEEK 4','Answer your teacher in full sentences'),(190,0,'WEEK 8','Give a 2-minute class presentation')]
cs=''.join(f'<div layer-name="{k.title()}" style="position:absolute;left:{x}px;top:{y}px;width:150px;padding:10px 12px;border-radius:14px;background:{"linear-gradient(180deg,rgba(108,99,255,0.3),rgba(24,22,45,0.95))" if i==2 else "rgba(24,22,45,0.92)"};border:1px solid {"#9D96FF" if i==2 else "rgba(157,150,255,0.25)"};display:flex;flex-direction:column;gap:3px;"><div style="{GE};font-weight:600;font-size:10.5px;letter-spacing:0.14em;color:#9D96FF;">{k}</div><div style="{ID};font-weight:500;font-size:13.5px;line-height:18px;color:#FFFFFF;">{esc(t)}</div></div>' for i,(x,y,k,t) in enumerate(cards))
social=f'<div style="display:flex;align-items:center;gap:10px;"><div style="display:flex;">' + ''.join(f'<div style="width:24px;height:24px;border-radius:999px;border:2px solid #0F0D25;background:{bg};display:flex;align-items:center;justify-content:center;"><div style="{GE};font-weight:600;font-size:10.5px;color:#FFFFFF;">{l}</div></div>' for l,bg in [('A','linear-gradient(135deg,#F28B9B,#8E4A9E)'),('R','linear-gradient(135deg,#8982FF,#3B368C)'),('S','linear-gradient(135deg,#6FD3C0,#2F6E8E)')]) + f'</div><div style="{GE};font-size:13.5px;color:#A9A4BC;">1,133,400+ learners are on this journey with you</div></div>'
S['S26'] = tk_head('Your plan', [('Speak up in class with confidence',False)], None, social) + f'<div layer-name="Plan chart" style="position:absolute;left:24px;top:176px;width:364px;height:372px;">{svg}{xl}{cs}</div>' + \
  f'<div layer-name="Body" style="position:absolute;left:32px;bottom:116px;width:348px;text-align:center;{GE};font-size:15px;line-height:22px;color:#B4B0C8;">With your current level (A2), here’s what 10 min of daily practice can do.</div>' + cta('Start my plan')
NOTES['S26'] = ("Your plan", "Headline is goal-specific. The line draws one step at a time: Today → Week 1 → Week 4 → Week 8; each dot pops and its milestone card rises. The week labels light up as the line passes. Then the area fills, the body fades in and the CTA rises.")

# ================= BRANCHES =================
S['B01'] = chat([msg(ask_rem,'dim'), chip('Remind me at 8:30 PM'), sys_pill('Notifications not allowed'), msg('No problem. You can switch reminders on later from Profile.','speaking')],
  anchor='top', header_html=header("43% completed",43))
NOTES['B01'] = ("Notifications denied", "Her choice still shows, a quiet system pill notes the OS answer, and Sarah reassures her. Same for \"Not now\".")

int_q = "Tell me about your favourite subject and why you like it."
ask_int = "We're almost done! Last step: answer this like you would to a new classmate."
S['B02'] = chat([msg(ask_lvl,'dim'), chip('Intermediate'), msg(ask_int), read_card(int_q, label='Answer out loud', question=True)], anchor='bottom', bottom=226, pills=False,
  header_html=header("87% completed",87), extra=micbar(tip='Stuck? Tap the bulb for a model answer', hint=True))
NOTES['B02'] = ("Intermediate / Advanced · question", "A goal-specific question instead of a passage. The bulb glows; the tip alternates between \"Tap the mic and answer\" and \"Stuck? Tap the bulb for a model answer\".")

said = "My favourite subject is history. I like it because I enjoy learning about the past and our teacher"
S['B03'] = chat([chip('Intermediate'), msg(ask_int,'dim'), read_card(int_q, label='Answer out loud', question=True), speech(said)], anchor='bottom', bottom=226, pills=False,
  header_html=header("87% completed",87), extra=micbar(rec=True))
NOTES['B03'] = ("Answering", "Her answer appears word by word in a dashed bubble with a caret while she speaks. ✓ ends it; the bubble turns into a solid reply.")

model = "My favourite subject is biology, because I love learning how the human body works. Our teacher makes every chapter feel like a story."
S['B04'] = chat([read_card(int_q, label='Answer out loud', question=True), chip('Show me a model answer'), msg("Here's one way to say it. Read it out loud:"), read_card(model, label='Model answer')], anchor='bottom', bottom=226, pills=False,
  header_html=header("87% completed",87), extra=micbar())
NOTES['B04'] = ("Model answer (hint)", "Tapping the bulb drops in a model answer to read aloud. From here it works like the Beginner read-aloud, and \"What you did well\" adapts.")

said_full = "My favourite subject is history. I like it because I enjoy learning about the past and our teacher explains each chapter like a story."
S['B05'] = tk_head('Quick fix', [('Two words need',False),('a little work',False)], "Let's correct them before we build your plan.") + \
  glass(f'<div style="position:relative;{ID};font-weight:500;font-size:13.5px;color:#A9A4BC;">From your answer</div><div style="position:relative;">{marked(said_full, ["favourite","chapter"], size=19, lh=34)}</div>', 200, '28px 22px', 'Passage') + cta("Let's correct them")
NOTES['B05'] = ("Errors · from her answer", "For Intermediate / Advanced the card shows what she said, with the two words to fix.")

S['B06'] = chat([msg(ask_read,'dim'), read_card(passage), chip("I can't speak right now"), msg("No worries! I'll build your plan from your answers, and we'll do your first speaking task together later.",'speaking')],
  anchor='bottom', header_html=header("87% completed",87))
NOTES['B06'] = ("Can't speak right now", "Skips the report screens and goes straight to the plan, which says \"Based on your level (Beginner)\".")

exec(open('/tmp/paper/override2.py').read())
os.makedirs('/tmp/paper/out', exist_ok=True)
for k,v in S.items():
    open(f'/tmp/paper/out/{k}.html','w').write(v)
json.dump(NOTES, open('/tmp/paper/out/notes.json','w'), ensure_ascii=False, indent=1)
print(len(S), sum(len(v) for v in S.values()))
