/* ============================================================
   Stimuler · India onboarding v2 — all copy lives here.
   Goal-specific and situation-specific lines are keyed so the
   review panel can switch pathways without touching app.js.
   ============================================================ */
window.CONTENT = (() => {

  const LANGS = [
    { value: 'Hindi',     native: 'हिन्दी' },
    { value: 'Tamil',     native: 'தமிழ்' },
    { value: 'Telugu',    native: 'తెలుగు' },
    { value: 'Marathi',   native: 'मराठी' },
    { value: 'Bengali',   native: 'বাংলা' },
    { value: 'Kannada',   native: 'ಕನ್ನಡ' },
    { value: 'Malayalam', native: 'മലയാളം' },
    { value: 'Gujarati',  native: 'ગુજરાતી' },
    { value: 'Punjabi',   native: 'ਪੰਜਾਬੀ' },
    { value: 'Odia',      native: 'ଓଡ଼ିଆ' },
    { value: 'Other',     native: '' },
  ];

  const SOURCES = [
    { value: 'Instagram',        icon: 'ig' },
    { value: 'YouTube',          icon: 'yt' },
    { value: 'Play Store search', icon: 'play' },
    { value: 'Friends or family', icon: 'people' },
    { value: 'Facebook',         icon: 'fb' },
    { value: 'Google',           icon: 'google' },
    { value: 'WhatsApp',         icon: 'wa' },
    { value: 'Other',            icon: '' },
  ];

  /* the pain question (asked after the goal) */
  const PAINS = [
    { key: 'slow',      label: "I understand but can't reply fast enough", short: 'Slow replies',
      reply: "That gap between understanding and replying closes fast with practice. We'll train quick replies." },
    { key: 'translate', label: 'I translate from {lang} in my head', short: 'Translating in head',
      reply: "Very common! We'll help you think directly in English, one step at a time." },
    { key: 'mistakes',  label: "I'm scared of mistakes in front of people", short: 'Fear of mistakes',
      reply: "Mistakes are how we learn. Here it's just you and me, no judgement." },
    { key: 'words',     label: 'I run out of words', short: 'Running out of words',
      reply: "We'll build the words you need for the moments that matter to you." },
    { key: 'accent',    label: 'My accent', short: 'Accent',
      reply: "Being clear matters more than any accent. We'll work on the sounds that trip you up." },
    { key: 'polished',  label: 'I want to sound more polished', short: 'Sounding polished',
      reply: "Love that. We'll sharpen your fluency and range so you sound natural." },
    { key: 'other',     label: 'Something else', short: 'Something else',
      reply: "Thanks for telling me. I'll keep that in mind as we practise." },
  ];

  const AGES    = ['Under 18', '18–24', '25–34', '35–44', '45+'];
  const GENDERS = ['Male', 'Female', 'Non-binary', 'Prefer not to say'];
  const TIMES   = ['7:30 AM', '1:00 PM', '8:30 PM'];

  const SITUATIONS = [
    { key: 'student',     label: 'Student' },
    { key: 'professional',label: 'Working professional' },
    { key: 'freelancer',  label: 'Self-employed / Freelancer' },
    { key: 'business',    label: 'Business owner' },
    { key: 'jobseeker',   label: 'Looking for work' },
    { key: 'homemaker',   label: 'Homemaker' },
    { key: 'careerbreak', label: 'Career break' },
    { key: 'parent',      label: 'Parent' },
  ];

  const GOALS = [
    { key: 'ielts',    label: 'IELTS',              short: 'IELTS' },
    { key: 'career',   label: 'Grow in my career',  short: 'Career' },
    { key: 'personal', label: 'Personal growth',    short: 'Personal' },
    { key: 'travel',   label: 'Travel confidently', short: 'Travel' },
    { key: 'school',   label: 'Excel at my school', short: 'School' },
    { key: 'other',    label: 'Other',              short: 'Other' },
  ];

  /* the header flourish right after the goal is picked (as in frame 13) */
  const GOAL_CHEER = {
    ielts: 'Great choice!', career: 'Impressive!', personal: 'Love that!',
    travel: 'How exciting!', school: 'Impressive!', other: 'Got it!',
  };

  /* Sarah's reply: goal × situation, so it never reads like a template */
  const GOAL_REPLY = {
    school: {
      student:     "Love that! Speaking up in class gets so much easier once English stops feeling like a test. We'll practise the real moments: answering your teacher, presentations and group work.",
      professional:"Studying while you work takes grit. We'll make sure you can speak up in lectures and present with confidence.",
      freelancer:  "Great choice. Courses move faster when you can discuss ideas out loud, so that's exactly what we'll practise.",
      business:    "Smart move. Learning while running a business is hard work, so we'll keep it short and focused on speaking up in class.",
      jobseeker:   "Good thinking. A course plus confident English is a strong mix for later interviews. We'll start with class discussions.",
      homemaker:   "That's wonderful! Going back to learning takes courage. We'll help you speak up in class without second-guessing yourself.",
      careerbreak: "A great way to use your break. We'll get you comfortable speaking in class, so the course feels easy from day one.",
      parent:      "Lovely! Whether it's your own classes or helping your child with school, we'll build the confidence to speak clearly.",
    },
    career: {
      student:     "Smart to start early! Placements reward people who speak clearly. We'll practise introductions, HR questions and group discussions.",
      professional:"Love it. Clear English shows up in every meeting, review and promotion talk. We'll practise the conversations you actually have at work.",
      freelancer:  "Great! Clients trust people who explain clearly. We'll practise pitching, negotiating and client calls.",
      business:    "Brilliant. Confident English helps you win clients and lead your team. We'll practise pitches, meetings and negotiations.",
      jobseeker:   "You've got this! Confident English can change how an interview goes. We'll practise the questions you're most likely to hear.",
      homemaker:   "That's exciting! Restarting a career is a big step. We'll practise interviews and introductions so you walk in confident.",
      careerbreak: "Welcome back! We'll help you walk into interviews sounding like you never left, gap questions and all.",
      parent:      "Great goal! You're balancing a lot, so we'll keep practice short and focused on the conversations that move you forward.",
    },
    ielts: {
      student:     "Great! Speaking is the part most students fear, and the one you can improve fastest. We'll practise all three parts of the test.",
      professional:"Smart! Whether it's for work abroad or PR, we'll lift your speaking band with practice that fits around your job.",
      freelancer:  "Good plan. We'll practise each IELTS speaking part in short daily sessions that fit around your client work.",
      business:    "Great! We'll build the fluency and range examiners look for, in 10 minutes a day.",
      jobseeker:   "A strong move. A good band opens doors. We'll practise the speaking test until it feels routine.",
      homemaker:   "That's a big goal, and a great one. We'll practise the speaking test step by step, at your pace.",
      careerbreak: "Good use of the time! We'll get you exam-ready on speaking with steady daily practice.",
      parent:      "Wonderful! We'll fit IELTS speaking practice into short sessions around family time.",
    },
    travel: {
      student:     "How exciting! We'll practise airports, hostels and making friends abroad, so you enjoy the trip instead of worrying.",
      professional:"Nice! Work trips and holidays both go better when you can just talk. We'll practise check-ins, directions and small talk.",
      freelancer:  "Love it. Client visit or workcation, we'll make everyday travel conversations feel easy.",
      business:    "Great! From client visits to trade fairs, we'll practise the conversations you'll have on the road.",
      jobseeker:   "Lovely! We'll practise the everyday English that makes travel easy: airports, hotels and asking for help.",
      homemaker:   "How wonderful! We'll practise ordering food, asking for directions and chatting with people, so you can travel with ease.",
      careerbreak: "Perfect time for it! We'll get you comfortable with airports, hotels and new people, so you enjoy every trip.",
      parent:      "Family trips are the best! We'll practise what you'll actually face, from the check-in counter to the hotel desk.",
    },
    personal: {
      student:     "Love that! Confidence in English spills into everything: friendships, classes, even your reels. We'll start with everyday conversations.",
      professional:"Great! Speaking freely, without rehearsing every sentence in your head, is something we can build together.",
      freelancer:  "Nice! We'll practise everyday conversations so English feels natural, not like work.",
      business:    "Wonderful. We'll build easy, everyday confidence, the kind that shows in every conversation.",
      jobseeker:   "Great choice. Confidence built now helps everywhere, including your next interview. We'll start with everyday talk.",
      homemaker:   "That's lovely! We'll practise the everyday conversations that matter to you, at your own pace.",
      careerbreak: "A great way to use this time! We'll make speaking English feel natural, one short session a day.",
      parent:      "Wonderful! Kids pick up on confidence. We'll practise everyday English you can use with them and everyone else.",
    },
    other: {
      student:     "Got it! We'll build confidence for the conversations you have every day, in class and out of it.",
      professional:"Got it! We'll focus on clear, confident speaking you can use at work and beyond.",
      freelancer:  "Got it! We'll build the confident English that helps with clients and everyday life.",
      business:    "Got it! We'll build confident English for customers, partners and everyday life.",
      jobseeker:   "Got it! We'll build speaking confidence that helps in interviews and beyond.",
      homemaker:   "Got it! We'll build everyday speaking confidence at your own pace.",
      careerbreak: "Got it! We'll use this time to make speaking English feel natural.",
      parent:      "Got it! We'll build everyday confidence you can use with your kids and everyone else.",
    },
  };

  /*
    Speaking test per goal.
    passage  — Beginner reads this aloud
    question — Intermediate / Advanced answer this
    model    — the hint: a model answer they can read instead
    said     — simulated transcript of their own answer (int/adv)
    fix      — the two words we flag; [0] is practised on screen 23
    good     — two words that came out clear (for "What you did well")
  */
  const TEST = {
    school: {
      passage:  "I enjoy my classes. Today I will present my project and share my thoughts with the class.",
      question: "Tell me about your favourite subject and why you like it.",
      context:  "to a new classmate",
      model:    "My favourite subject is biology, because I love learning how the human body works. Our teacher makes every chapter feel like a story.",
      said:     "My favourite subject is history. I like it because I enjoy learning about the past and our teacher explains each chapter like a story.",
      fix: [
        { word: 'thoughts', heard: 'toughts', issue: 'The \'th\' came out as a hard \'t\'.', ipa: '/θɔːts/', hint: "Tongue between your teeth for 'th', then 'awts'", focus: "'th'", before: 44, after: 81 },
        { word: 'project', heard: 'pro-JECT', issue: 'The stress fell on the second part.',  ipa: '/ˈprɒdʒekt/', hint: "Stress the first part: PRO-ject", focus: 'stress', before: 52, after: 84 },
      ],
      fixInt: [
        { word: 'favourite', heard: 'fa-VOU-rite', issue: 'The stress fell in the middle.', ipa: '/ˈfeɪvərɪt/', hint: "Three quick beats: FAY-vuh-rit", focus: "'ay'", before: 48, after: 83 },
        { word: 'chapter', heard: 'shapter', issue: 'The \'ch\' sounded like \'sh\'.',   ipa: '/ˈtʃæptə/',  hint: "Start with a crisp 'ch'", focus: "'ch'", before: 55, after: 86 },
      ],
      good: ['classes', 'today'],
    },
    career: {
      passage:  "I am ready for this interview. I have worked on many projects with my team.",
      question: "Tell me about yourself, like you would in an interview.",
      context:  "in an interview",
      model:    "I'm a software engineer with two years of experience. I enjoy solving problems with my team, and I'm looking for a role where I can keep learning.",
      said:     "I am working as a software engineer since two years. I like solving problems with my team and now I am looking for a role where I can grow.",
      fix: [
        { word: 'interview', heard: 'inter-VIEW', issue: 'The stress moved to the end.', ipa: '/ˈɪntəvjuː/', hint: "Stress the start: IN-ter-view", focus: 'stress', before: 46, after: 82 },
        { word: 'worked', heard: 'vorked', issue: 'The \'w\' sounded like a \'v\'.',    ipa: '/wɜːkt/',     hint: "Round your lips for 'w', end with a soft 't'", focus: "'w'", before: 51, after: 85 },
      ],
      fixInt: [
        { word: 'engineer', heard: 'EN-gineer', issue: 'The stress fell on the first part.', ipa: '/ˌendʒɪˈnɪə/', hint: "Stress the end: en-ji-NEER", focus: 'stress', before: 49, after: 84 },
        { word: 'role', heard: 'rol', issue: 'The \'oh\' sound was too short.',     ipa: '/rəʊl/',       hint: "One smooth sound: 'rohl'", focus: "'oh'", before: 56, after: 87 },
      ],
      good: ['ready', 'team'],
    },
    ielts: {
      passage:  "Many people believe that technology has changed the way we learn and work.",
      question: "Describe a skill you would like to learn, and say why.",
      context:  "in the speaking test",
      model:    "I'd really like to learn photography. I've always admired how a single picture can tell a whole story, and I think it would help me notice small details.",
      said:     "I would like to learn photography because I always liked how one picture can tell a full story, and I think it will help me notice small details.",
      fix: [
        { word: 'technology', heard: 'TEK-nology', issue: 'The stress fell on the first part.', ipa: '/tekˈnɒlədʒi/', hint: "Stress the second part: tek-NOL-uh-jee", focus: 'stress', before: 45, after: 80 },
        { word: 'believe', heard: 'beleew', issue: 'The \'v\' at the end sounded like a \'w\'.',    ipa: '/bɪˈliːv/',     hint: "End on a buzzing 'v', not 'w'", focus: "'v'", before: 53, after: 86 },
      ],
      fixInt: [
        { word: 'photography', heard: 'PHO-tography', issue: 'The stress fell on the first part.', ipa: '/fəˈtɒɡrəfi/', hint: "Stress the second part: fuh-TOG-ruh-fee", focus: 'stress', before: 47, after: 82 },
        { word: 'details', heard: 'de-TAILS', issue: 'The stress moved to the end.',     ipa: '/ˈdiːteɪlz/',  hint: "Stress the start: DEE-tails", focus: 'stress', before: 57, after: 86 },
      ],
      good: ['people', 'learn'],
    },
    travel: {
      passage:  "Hello, I would like to check in. Could you please tell me where my room is?",
      question: "Your hotel room isn't ready yet. What would you say at the front desk?",
      context:  "at a hotel",
      model:    "Hi, I have a booking for tonight, but my room isn't ready yet. Could I leave my bags here and come back in an hour?",
      said:     "Hello, I have booking for tonight but they said room is not ready. Can I keep my bags here and come back after one hour?",
      fix: [
        { word: 'would', heard: 'wuld', issue: 'The \'l\' should be silent.',  ipa: '/wʊd/', hint: "The 'l' is silent: say 'wood'", focus: "silent 'l'", before: 43, after: 82 },
        { word: 'please', heard: 'pliss', issue: 'The \'ee\' sound was too short.', ipa: '/pliːz/', hint: "Hold the long 'ee', end with a 'z'", focus: "'ee'", before: 54, after: 85 },
      ],
      fixInt: [
        { word: 'booking', heard: 'boo-king-g', issue: 'The \'ng\' ended with a hard \'g\'.', ipa: '/ˈbʊkɪŋ/', hint: "Short 'oo' like 'book', soft 'ng' at the end", focus: "'ng'", before: 50, after: 84 },
        { word: 'ready', heard: 'raydee', issue: 'The \'e\' sounded like \'ay\'.',   ipa: '/ˈredi/',  hint: "Two quick beats: RED-ee", focus: "'e'", before: 58, after: 87 },
      ],
      good: ['hello', 'room'],
    },
    personal: {
      passage:  "I love to paint in my free time. It helps me relax and be creative.",
      question: "What do you like to do on weekends, and why?",
      context:  "to a new friend",
      model:    "On weekends I like to go for long walks and try new cafés with my friends. It helps me switch off after a busy week.",
      said:     "On weekends I like going for walks and trying new cafés with my friends. It helps me to relax after the busy week.",
      fix: [
        { word: 'paint', heard: 'pent', issue: 'The \'ai\' sounded like a short \'e\'.',    ipa: '/peɪnt/',    hint: "Say it like 'pay' + 'nt'", focus: "'ai'", before: 44, after: 81 },
        { word: 'creative', heard: 'CREE-ative', issue: 'The stress fell on the first part.', ipa: '/kriˈeɪtɪv/', hint: "Three beats: kree-AY-tiv", focus: 'stress', before: 52, after: 84 },
      ],
      fixInt: [
        { word: 'weekends', heard: 'veekends', issue: 'The \'w\' sounded like a \'v\'.', ipa: '/ˌwiːkˈendz/', hint: "Round your lips for 'w', end with 'dz'", focus: "'w'", before: 49, after: 83 },
        { word: 'cafés', heard: 'ka-FAYS', issue: 'The stress moved to the end.',    ipa: '/ˈkæfeɪz/',    hint: "Two beats: KA-fays", focus: "'ay'", before: 57, after: 86 },
      ],
      good: ['love', 'free time'],
    },
  };
  TEST.other = TEST.personal;

  /* measured level: what the report says back to them */
  const LEVELS = {
    beginner:     { label: 'Beginner',     cefr: 'A2', rung: 1, line: 'You can say simple sentences, but you slow down on longer words.', next: 'Intermediate', nextCefr: 'B1' },
    intermediate: { label: 'Intermediate', cefr: 'B1', rung: 2, line: 'People understand you well, but you pause to find the right words.', next: 'Advanced', nextCefr: 'B2' },
    advanced:     { label: 'Advanced',     cefr: 'B2', rung: 3, line: 'You speak with ease. A few sounds and longer answers need polish.', next: 'Proficient', nextCefr: 'C1' },
  };
  const LADDER = [
    { label: 'Novice', cefr: 'A1' }, { label: 'Beginner', cefr: 'A2' },
    { label: 'Intermediate', cefr: 'B1' }, { label: 'Advanced', cefr: 'B2' },
    { label: 'Proficient', cefr: 'C1' }, { label: 'Native', cefr: 'C2' },
  ];

  /* plan: header + three dated milestones, per goal */
  const PLAN = {
    school:   { title: 'Speak up in class with confidence', end: 'Class-ready',
                m: ['Introduce yourself in class without pausing', 'Answer your teacher in full sentences', 'Give a 2-minute class presentation'] },
    career:   { title: 'Walk into your next interview ready', end: 'Interview-ready',
                m: ['Introduce yourself without pausing', "Answer 'Tell me about yourself' in one minute", 'Handle a full mock HR round'] },
    ielts:    { title: 'Get closer to your target band', end: 'Test-ready',
                m: ['Answer Part 1 questions without long pauses', 'Speak for 2 full minutes on a Part 2 cue card', 'Take a full speaking mock test'] },
    travel:   { title: 'Travel without the language worry', end: 'Trip-ready',
                m: ['Get through airport and hotel check-in', 'Order food and ask locals for directions', 'Chat comfortably with locals'] },
    personal: { title: 'Speak English with everyday confidence', end: 'Confident',
                m: ['Talk about your day without pausing', 'Hold a 5-minute conversation', 'Share your opinion clearly in a group'] },
  };
  PLAN.other = PLAN.personal;

  /* social proof — placeholders, swap for real reviews before testing */
  const PROOF = {
    school: [
      { name: 'Ananya S.', meta: 'Class 11 · Pune', quote: "I used to stay quiet in class. Now I'm usually the first one to answer.", src: 'play' },
      { name: 'Rohit K.',  meta: 'B.Com student · Delhi', quote: "My viva went so well. I didn't freeze even once.", src: 'play' },
      { name: 'Fatima N.', meta: 'Class 12 · Hyderabad', quote: 'Presentations don’t scare me anymore. Ten minutes a day really works.', src: 'app' },
    ],
    career: [
      { name: 'Arjun M.', meta: 'Software engineer · Bengaluru', quote: 'Cleared my HR round after three weeks of mock interviews with Sarah.', src: 'play' },
      { name: 'Sneha P.', meta: 'Analyst · Mumbai', quote: 'I speak up on client calls now instead of staying on mute.', src: 'play' },
      { name: 'Vikram R.', meta: 'Sales lead · Chennai', quote: 'Did my whole appraisal talk in English, without notes.', src: 'app' },
    ],
    ielts: [
      { name: 'Harpreet K.', meta: 'IELTS · Ludhiana', quote: 'Went from 6.0 to 7.0 in speaking. The Part 2 practice is gold.', src: 'play' },
      { name: 'Nikhil J.', meta: 'IELTS · Ahmedabad', quote: 'The real test felt familiar because I had done it so many times here.', src: 'play' },
      { name: 'Aisha F.', meta: 'IELTS · Kochi', quote: 'Daily practice fixed my long pauses. My examiner said I was fluent.', src: 'app' },
    ],
    travel: [
      { name: 'Meera T.', meta: 'Traveller · Jaipur', quote: 'Checked in, ordered food and made friends in Dubai. All in English!', src: 'play' },
      { name: 'Kunal D.', meta: 'Traveller · Kolkata', quote: 'My first solo trip abroad, and I didn’t panic once.', src: 'play' },
      { name: 'Divya R.', meta: 'Traveller · Coimbatore', quote: 'Airport announcements and hotel desks finally make sense.', src: 'app' },
    ],
    personal: [
      { name: 'Pooja G.', meta: 'Homemaker · Indore', quote: 'I finally think in English instead of translating in my head.', src: 'play' },
      { name: 'Sunita R.', meta: 'Parent · Lucknow', quote: "I talk to my kids' teachers confidently now.", src: 'play' },
      { name: 'Rahul V.', meta: 'Student · Patna', quote: 'Speaking English feels normal now, not scary.', src: 'app' },
    ],
  };
  PROOF.other = PROOF.personal;

  return { PAINS, LANGS, SOURCES, AGES, GENDERS, TIMES, SITUATIONS, GOALS, GOAL_CHEER, GOAL_REPLY, TEST, LEVELS, LADDER, PLAN, PROOF,
           LEARNERS: '1,133,400+' };
})();
