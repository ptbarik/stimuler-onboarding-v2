
# ================= ROUND 3 OVERRIDES =================
habit = "Thanks for that! Together let's make English a daily learning habit."
daily = "Daily practice will help you achieve your goals faster."
good_hands = f"You're in good hands, {NAME}! Discover why we won Google Play’s Best AI App 2023 and hear from learners like you."

def phone_card3():
    return chat_card(
        f'<div style="display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.12);"><div style="{ID};font-weight:600;font-size:15.5px;color:#FFFFFF;">+91</div><div style="width:1px;height:20px;background:rgba(255,255,255,0.18);"></div><div style="{ID};font-size:15.5px;color:rgba(255,255,255,0.35);">Phone number</div></div>' +
        wide_cta('Continue', ready=False) + link('Skip for now'))

S['S08'] = chat([msg(ask_about, 'dim'), chip('18–24 · Female'), msg(ask_phone), phone_card3()], anchor='bottom',
                header_html=header("That helps, thank you!", 37), skip_dim=True)
S['S10'] = chat([msg(ask_phone, 'dim'), chip(PHONE), msg(ask_sit), opts([pill(x) for x in SITS])],
                anchor='bottom', header_html=header("You're all set!", 43), skip_dim=True)
S['S18'] = chat([msg(ask_lvl, 'dim'), chip('Beginner'), msg(good_hands, 'speaking'), rated_badge(), proof2(PROOF)],
                anchor='bottom', header_html=header("Almost there!", 75))
S['S09'] = chat([rated_badge(), proof2(PROOF), msg(daily, 'speaking')], anchor='bottom',
                header_html=header("75% completed", 75),
                extra=os_dialog('Allow Stimuler to send you notifications?', ['Allow', "Don't allow"]))
S['S14'] = chat([msg(daily, 'dim'), msg(habit, 'dim'), msg(ask_read), read_card(passage)], anchor='bottom', bottom=226, pills=False,
                header_html=header("87% completed", 87), extra=micbar())
S['S15'] = chat([msg(daily, 'dim'), msg(habit, 'dim'), msg(ask_read), read_card(passage)], anchor='bottom', bottom=226, pills=False,
                header_html=header("87% completed", 87), extra=micbar() + os_dialog('Allow Stimuler to record audio?', ['While using the app', 'Only this time', "Don't allow"], icon='mic'))
S['S16'] = chat([msg(daily, 'dim'), msg(habit, 'dim'), msg(ask_read), read_card(passage, lit=8, now=8)], anchor='bottom', bottom=226, pills=False,
                header_html=header("87% completed", 87), extra=micbar(rec=True))
S['S17'] = chat([msg(habit, 'dim'), msg(ask_read, 'dim'), read_card(passage, done=True), msg(f"Well done, {NAME}! You read that in one go.", 'speaking')],
                anchor='bottom', header_html=header("First speech done!", 100, flag_on=True))
S['S19'] = chat([msg(ask_read, 'dim'), read_card(passage, done=True), msg(f"Well done, {NAME}! You read that in one go.", 'dim'),
                 msg("Curious how well you spoke? Tap to see how you did!", 'speaking'), report_btn()],
                anchor='bottom', bottom=60, pills=False, header_html=header("First speech done!", 100, flag_on=True))
S['B01'] = chat([rated_badge(), proof2(PROOF), msg(daily, 'dim'), sys_pill('Notifications not allowed'), msg('No problem. You can turn reminders on later in Profile settings.', 'speaking')],
                anchor='bottom', header_html=header("75% completed", 75))
S['B02'] = chat([msg(habit, 'dim'), msg(ask_int), read_card(int_q, label='Answer out loud', question=True)], anchor='bottom', bottom=226, pills=False,
                header_html=header("87% completed", 87), extra=micbar(tip='Stuck? Tap the bulb for a model answer', hint=True))
S['B03'] = chat([msg(habit, 'dim'), msg(ask_int, 'dim'), read_card(int_q, label='Answer out loud', question=True), speech(said)], anchor='bottom', bottom=226, pills=False,
                header_html=header("87% completed", 87), extra=micbar(rec=True))
S['B07'] = chat([msg(ask_phone, 'dim'), chip('Skip for now'), msg('No problem! You can add it anytime in Profile settings.', 'speaking')],
                anchor='top', header_html=header("37% completed", 37))
