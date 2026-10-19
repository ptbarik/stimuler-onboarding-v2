
# ================= ROUND 2 OVERRIDES =================
ask_phone = f"Thanks, {NAME}! To make sure you get the latest lessons, can I have your phone number?"
PHONE = '+91 98765 43210'
pain_q = "Be honest. What happens when you have to speak English?"
PAINS = ["I understand but can't reply fast enough", "I translate from Hindi in my head", "I'm scared of mistakes in front of people",
         "I run out of words", "My accent", "I want to sound more polished", "Something else"]
pain_reply = "Very common! We'll help you think directly in English, one step at a time."
great = "Great job! Discover why we won Google Play’s Best AI App 2023 and hear from learners like you."

def relabel(html_, old, new):
    return html_.replace(f'>{old}<', f'>{new}<')

S['S04'] = relabel(S['S04'], '6% completed', 'Nice to meet you, Naina!')
S['S05'] = relabel(S['S05'], '12% completed', 'Got it!')
S['S07'] = relabel(S['S07'], '25% completed', 'Thanks for telling us!')
S['S08'] = chat([msg(ask_about, 'dim'), chip('18–24 · Female'), msg(ask_phone), phone_card()], anchor='bottom',
                header_html=header("That helps, thank you!", 37), skip_dim=True)
S['S09'] = chat([msg(ask_about, 'dim'), chip('18–24 · Female'), msg(ask_phone), phone_card()], anchor='bottom',
                header_html=header("37% completed", 37), skip_dim=True,
                extra=os_dialog('Allow Stimuler to send you notifications?', ['Allow', "Don't allow"]))
S['S10'] = chat([msg(ask_phone, 'dim'), chip(PHONE), msg("Done! Your daily lessons will reach you on WhatsApp.", 'dim'), msg(ask_sit),
                 opts([pill(x) for x in SITS])], anchor='bottom', header_html=header("You're all set!", 43), skip_dim=True)
S['S12b'] = chat([msg(reply, 'dim'), msg(pain_q), line_opts(PAINS)], anchor='bottom',
                 header_html=header("“Excel at my school” – Impressive!", 62), skip_dim=True)
S['S13'] = chat([msg(pain_q, 'dim'), chip(PAINS[1]), msg(pain_reply, 'dim'), msg(ask_lvl), stacked(LVLS)], anchor='bottom',
                header_html=header("You're not alone in this.", 68), skip_dim=True)
S['S14'] = relabel(S['S14'], '87% completed', 'Almost there!')
S['S17'] = chat([chip('Beginner'), msg(ask_read, 'dim'), read_card(passage, done=True), msg(f"Well done, {NAME}! You read that in one go.", 'speaking')],
                anchor='bottom', header_html=header("First speech done!", 100, flag_on=True))
S['S18'] = chat([msg(f"Well done, {NAME}! You read that in one go.", 'dim'), msg(great, 'speaking'), rated_badge(), proof2(PROOF)],
                anchor='bottom', header_html=header("First speech done!", 100, flag_on=True))
S['S19'] = chat([rated_badge(), proof2(PROOF), msg("Curious how well you spoke? Tap to see how you did!", 'speaking'), report_btn()],
                anchor='bottom', bottom=60, pills=False, header_html=header("First speech done!", 100, flag_on=True))
S['S20'] = S['S20'].replace('top:56px;', 'top:40px;').replace(cta('Continue'), '') + \
    snapshot(['Student', 'Excel at my school', 'Translating in head']) + cta('Continue')
S['S22'] = tk_head('Quick fix', [('Two words need', False), ('a little work', False)], "Let's correct them before we build your plan.") + \
    passage_card('From your reading', passage, ['project', 'thoughts']) + \
    fix_rows([('thoughts', '/θɔːts/', 'toughts', "The 'th' came out as a hard 't'.", 44),
              ('project', '/ˈprɒdʒekt/', 'pro-JECT', 'The stress fell on the second part.', 52)], 448) + cta("Let's correct them")

def practice2(after=False):
    head = tk_head('Practice', [("Let's improve the 'th' sound", False), ("in 'thoughts'", True)])
    psg = passage_card('From your reading', passage, ['thoughts', 'project'], {0: 'fixed' if after else 'focus', 1: 'err'})
    if after:
        score = (f'<div style="display:flex;flex-direction:column;"><div style="display:flex;align-items:baseline;gap:8px;"><div style="{ID};font-weight:700;font-size:32px;line-height:36px;color:#63E39B;">81%</div>'
                 f'<div style="{ID};font-weight:600;font-size:15px;color:#63E39B;">+37</div></div><div style="{GE};font-size:12.5px;color:#A9A4BC;">New score</div></div>')
        btn = (f'<div style="height:50px;padding:0px 20px;border-radius:999px;background:rgba(50,225,141,0.14);border:1px solid rgba(50,225,141,0.45);display:flex;align-items:center;justify-content:center;gap:8px;">'
               f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#63E39B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
               f'<div style="{ID};font-weight:600;font-size:15.5px;color:#63E39B;">Sounds clear</div></div>')
        cardst = 'border:1px solid rgba(50,225,141,0.35);background:linear-gradient(180deg,rgba(50,225,141,0.08),rgba(24,22,45,0.85));'
    else:
        score = f'<div style="display:flex;flex-direction:column;"><div style="{ID};font-weight:700;font-size:32px;line-height:36px;color:#FFFFFF;">44%</div><div style="{GE};font-size:12.5px;color:#A9A4BC;">Current score</div></div>'
        btn = (f'<div style="height:50px;padding:0px 20px;border-radius:999px;background:linear-gradient(180deg,#8982FF,#625AE8);box-shadow:0 8px 24px rgba(108,99,255,0.45);display:flex;align-items:center;justify-content:center;gap:8px;">'
               f'{MICI.format(s=18, c="#FFFFFF")}<div style="{ID};font-weight:600;font-size:15.5px;color:#FFFFFF;">Tap to speak</div></div>')
        cardst = 'border:1px solid rgba(255,255,255,0.08);background:rgba(24,22,45,0.85);'
    cue = (f'<div style="display:flex;justify-content:center;gap:5px;"><div style="{GE};font-weight:600;font-size:12px;letter-spacing:0.16em;color:#8F8AB3;">READ THE WORD</div>'
           f'<div style="{GE};font-weight:600;font-size:12px;letter-spacing:0.16em;color:#FFFFFF;">OUT LOUD</div></div>')
    top = (f'<div style="display:flex;justify-content:space-between;align-items:flex-start;"><div style="display:flex;flex-direction:column;gap:2px;"><div style="{ID};font-weight:700;font-size:34px;line-height:40px;letter-spacing:-0.02em;color:#FFFFFF;">thoughts</div>'
           f'<div style="{GE};font-size:14px;color:#A9A4BC;">/θɔːts/</div></div><div style="width:40px;height:40px;border-radius:999px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;">{SPK.format(c="#E6E3F7")}</div></div>')
    hint = f'<div style="padding:10px 12px;border-radius:12px;background:rgba(255,255,255,0.04);"><div style="{GE};font-size:14.5px;line-height:20px;color:#C9C5DD;">Tongue between your teeth for \'th\', then \'awts\'</div></div>'
    card = f'<div layer-name="Word card" style="padding:20px;border-radius:24px;{cardst}display:flex;flex-direction:column;gap:12px;">{top}{hint}<div style="display:flex;align-items:flex-end;justify-content:space-between;">{score}{btn}</div></div>'
    bottom = f'<div layer-name="Read the word" style="position:absolute;left:24px;bottom:118px;width:364px;display:flex;flex-direction:column;gap:12px;">{cue}{card}</div>'
    return head + psg + bottom + (cta('Continue') if after else '')

S['S23'] = practice2(False)
S['S24'] = practice2(True)
S['S25'] = header("Nice work!", 100, flag_on=True) + \
    f'<div layer-name="Chat" style="position:absolute;left:0px;bottom:120px;width:412px;padding:0px 18px;display:flex;flex-direction:column;gap:16px;">' + \
    msg(f"Look at that, {NAME}! One try and ‘thoughts’ already sounds clearer.", "dim") + ba_card("thoughts", "/θɔːts/", 44, 81) + \
    msg("That’s what 10 minutes a day does. ‘project’ is waiting for you in your Day 1 plan.") + sticker("st-sarah_cheer_thumbs_up.png") + '</div>' + cta('Start my plan')
S['B01'] = chat([msg(ask_phone, 'dim'), chip(PHONE), sys_pill('Notifications not allowed'), msg('No problem. You can turn reminders on later in Profile settings.', 'speaking')],
                anchor='top', header_html=header("43% completed", 43))
S['B05'] = tk_head('Quick fix', [('Two words need', False), ('a little work', False)], "Let's correct them before we build your plan.") + \
    passage_card('From your answer', said_full, ['favourite', 'chapter']) + \
    fix_rows([('favourite', '/ˈfeɪvərɪt/', 'fa-VOU-rite', 'The stress fell in the middle.', 48),
              ('chapter', '/ˈtʃæptə/', 'shapter', "The 'ch' sounded like 'sh'.", 55)], 520) + cta("Let's correct them")
S['B07'] = chat([msg(ask_phone, 'dim'), chip('Skip for now'), msg('No problem! You can turn reminders on anytime in Profile settings.', 'speaking')],
                anchor='top', header_html=header("37% completed", 37))
