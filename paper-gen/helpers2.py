
def phone_card():
    wa = ICONS["wa"].replace("#BDB9D6","#5FD38B")
    return chat_card(f'<div style="display:flex;align-items:center;gap:7px;">{wa}<div style="{ID};font-weight:500;font-size:14px;line-height:18px;color:#A9A4BC;">Get reminders on WhatsApp</div></div>' +
      f'<div style="display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);"><div style="{ID};font-weight:600;font-size:15.5px;color:#FFFFFF;">+91</div><div style="width:1px;height:20px;background:rgba(255,255,255,0.18);"></div><div style="{ID};font-size:15.5px;color:rgba(255,255,255,0.35);">Phone number (optional)</div></div>' +
      wide_cta('Turn on reminders', ready=False) + link('Skip for now'))

def line_opts(labels, sel=None):
    out = ''
    for l in labels:
        s_ = (l == sel)
        bg = 'linear-gradient(90deg,#4A46B8,#3A2580)' if s_ else '#211F38'
        bd = '#8982FF' if s_ else 'rgba(255,255,255,0.08)'
        c = '#FFFFFF' if s_ else '#EDEBF5'
        out += f'<div layer-name="Option" style="width:300px;padding:14px 18px;border-radius:16px;background:{bg};border:1px solid {bd};"><div style="{ID};font-weight:500;font-size:16px;line-height:22px;color:{c};">{esc(l)}</div></div>'
    return f'<div layer-name="Options" style="display:flex;flex-direction:column;align-items:flex-end;gap:10px;"><div style="{ID};font-weight:500;font-size:14.5px;line-height:20px;color:#A9A4BC;">Select an option</div>{out}</div>'

def rated_badge():
    return f'<div layer-name="Rated #1 badge" style="display:flex;justify-content:center;"><img src="{A}rated-badge.png" style="width:341px;height:171px;display:block;"></div>'

def proof2(cards):
    stat = f'<div style="display:flex;align-items:baseline;gap:8px;"><div style="{ID};font-weight:700;font-size:22px;line-height:28px;color:#FFFFFF;">1,133,400+</div><div style="{ID};font-size:14px;line-height:20px;color:#A9A4BC;">learners in India chose us</div></div>'
    return proof(cards).replace(stat, '')

def yellow_marked(text, errs, state={}, size=21, lh=40):
    out = []
    plain = lambda t: f'<div style="{ID};font-weight:500;font-size:{size}px;line-height:{lh}px;color:rgba(255,255,255,0.55);">{esc(t)}</div>'
    for w in text.split(' '):
        core = w.rstrip('.,!?'); punct = w[len(core):]
        k = next((i for i, e in enumerate(errs) if e.lower() == core.lower()), None)
        if k is None:
            out.append(plain(w)); continue
        stt = state.get(k, 'err')
        if stt == 'fixed': bg, bd, c = 'rgba(50,225,141,0.14)', 'rgba(50,225,141,0.55)', '#63E39B'
        elif stt == 'focus': bg, bd, c = 'rgba(245,196,81,0.24)', '#F5C451', '#FFF1CC'
        else: bg, bd, c = 'rgba(245,196,81,0.13)', 'rgba(245,196,81,0.45)', '#FFE3A3'
        pdiv = plain(punct) if punct else ''
        out.append(f'<div style="display:flex;align-items:center;gap:1px;"><div style="height:31px;padding:0px 9px;border-radius:9px;background:{bg};border:1px solid {bd};display:flex;align-items:center;justify-content:center;"><div style="{ID};font-weight:600;font-size:{size}px;line-height:28px;color:{c};text-align:center;">{esc(core)}</div></div>{pdiv}</div>')
    return f'<div layer-name="Text" style="display:flex;flex-wrap:wrap;column-gap:6px;align-items:center;">{"".join(out)}</div>'

def passage_card(label, text, errs, state={}):
    inner = f'<div style="position:relative;{ID};font-weight:500;font-size:13.5px;color:#A9A4BC;">{esc(label)}</div><div style="position:relative;">{yellow_marked(text, errs, state)}</div>'
    return glass(inner, 200, '26px 22px', 'Passage')

def ring(p):
    import math
    r = 25; c = 2 * math.pi * r; d = c * p / 100
    return (f'<div style="position:relative;width:58px;height:58px;flex-shrink:0;">'
            f'<svg width="58" height="58" viewBox="0 0 58 58" style="position:absolute;left:0px;top:0px;"><circle cx="29" cy="29" r="{r}" fill="#16142A" stroke="rgba(255,255,255,0.08)" stroke-width="4.5"/>'
            f'<circle cx="29" cy="29" r="{r}" fill="none" stroke="#F5C451" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="{d:.1f} {c:.1f}" transform="rotate(-90 29 29)"/></svg>'
            f'<div style="position:absolute;left:0px;top:0px;width:58px;height:58px;display:flex;align-items:center;justify-content:center;"><div style="{ID};font-weight:700;font-size:14px;color:#FFE3A3;">{p}%</div></div></div>')

def fix_rows(rows, top):
    items = ''
    for w, ipa, h, why, p in rows:
        items += (f'<div layer-name="Word to fix" style="display:flex;align-items:center;gap:16px;padding:18px 18px;border-radius:18px;background:linear-gradient(90deg,rgba(245,196,81,0.07),rgba(24,22,45,0.85) 45%);border:1px solid rgba(245,196,81,0.18);">{ring(p)}'
                  f'<div style="flex-grow:1;display:flex;flex-direction:column;gap:3px;"><div style="display:flex;align-items:baseline;gap:8px;"><div style="{ID};font-weight:700;font-size:17px;color:#FFFFFF;">{esc(w)}</div><div style="{GE};font-size:13px;color:#A9A4BC;">{esc(ipa)}</div></div>'
                  f'<div style="{GE};font-size:13.5px;line-height:19px;color:#F2D08A;">We heard “{esc(h)}”</div><div style="{GE};font-size:13.5px;line-height:19px;color:#A9A4BC;">{esc(why)}</div></div></div>')
    return f'<div layer-name="What to fix" style="position:absolute;left:24px;top:{top}px;width:364px;display:flex;flex-direction:column;gap:12px;"><div style="{GE};font-weight:600;font-size:11px;letter-spacing:0.16em;color:#8F8AB3;">WHAT TO FIX</div>{items}</div>'

def snapshot(chips):
    pen = '<div style="width:32px;height:32px;border-radius:999px;border:1.5px solid #434BA9;display:flex;align-items:center;justify-content:center;flex-shrink:0;"><svg width="14" height="14" viewBox="0 0 14 14"><path d="M9.5 1.8l2.7 2.7L4.7 12H2v-2.7z" fill="none" stroke="#C9C8FF" stroke-width="1.4" stroke-linejoin="round"/></svg></div>'
    cs = ''.join(f'<div style="padding:7px 12px;border-radius:999px;background:#16142A;border:1px solid #434BA9;flex-shrink:0;"><div style="{GE};font-weight:500;font-size:13px;line-height:16px;color:#E4E3EC;white-space:nowrap;">{esc(c)}</div></div>' for c in chips)
    return f'<div layer-name="Snapshot" style="position:absolute;left:24px;bottom:118px;width:364px;display:flex;flex-direction:column;gap:10px;"><div style="{GE};font-weight:500;font-size:13px;line-height:16px;color:#9C9AAF;">Built from your answers. Tap one to change it.</div><div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">{pen}{cs}</div></div>'

def ba_card(word, ipa, b, a):
    def bar(lab, pct, after):
        fill = 'linear-gradient(90deg,#2DCB7F,#7EFFB8)' if after else '#5A5675'
        vc = '#63E39B' if after else '#A9A4BC'
        return (f'<div style="display:flex;align-items:center;gap:10px;"><div style="width:50px;{GE};font-size:13px;color:#A9A4BC;">{lab}</div>'
                f'<div style="flex-grow:1;height:8px;border-radius:999px;background:rgba(255,255,255,0.07);overflow:hidden;position:relative;"><div style="position:absolute;left:0px;top:0px;height:8px;width:{pct}%;border-radius:999px;background:{fill};"></div></div>'
                f'<div style="width:40px;text-align:right;{ID};font-weight:600;font-size:14px;color:{vc};">{pct}%</div></div>')
    head = (f'<div style="display:flex;justify-content:space-between;align-items:flex-start;"><div style="display:flex;flex-direction:column;"><div style="{ID};font-weight:700;font-size:26px;line-height:30px;letter-spacing:-0.02em;color:#FFFFFF;">{esc(word)}</div><div style="{GE};font-size:13.5px;color:#A9A4BC;">{esc(ipa)}</div></div>'
            f'<div style="display:flex;flex-direction:column;align-items:flex-end;padding:8px 12px;border-radius:14px;background:rgba(50,225,141,0.12);border:1px solid rgba(50,225,141,0.3);"><div style="{ID};font-weight:700;font-size:22px;line-height:24px;color:#63E39B;">+{a-b}</div><div style="{GE};font-size:11.5px;color:#9FE8C2;">points in one try</div></div></div>')
    bars = f'<div style="display:flex;flex-direction:column;gap:10px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.08);">{bar("Before", b, False)}{bar("After", a, True)}</div>'
    return f'<div layer-name="Before / after" style="display:flex;padding-left:42px;"><div style="width:328px;padding:18px;border-radius:22px;background:rgba(24,22,45,0.9);border:1px solid rgba(50,225,141,0.28);display:flex;flex-direction:column;gap:16px;">{head}{bars}</div></div>'
