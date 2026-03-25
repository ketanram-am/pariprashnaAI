from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class VerseCard:
    reference: str
    shloka: str
    meaning: str
    word_meaning: str
    advice: str
    tags: Tuple[str, ...]


FALLBACK_VERSES = (
    VerseCard(
        reference="Bhagavad Gita 2.47",
        shloka=(
            "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। "
            "मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥"
        ),
        meaning=(
            "You have a right to your actions, but never to the fruits of those "
            "actions. Stay sincere in effort without becoming paralyzed by results."
        ),
        word_meaning=(
            "karmani: in action; eva: only; adhikarah: right; te: your; ma: never; "
            "phalesu: in the fruits; kadachana: at any time; ma: do not; "
            "karma-phala-hetuh: be motivated only by results; bhuh: become; "
            "ma: do not; te: your; sangah: attachment; astu: be; akarmani: to inaction."
        ),
        advice=(
            "Focus on the next honest step instead of mentally living in the result. "
            "If work or studies feel overwhelming, define success today as disciplined effort."
        ),
        tags=(
            "work",
            "career",
            "exam",
            "results",
            "failure",
            "performance",
            "pressure",
            "deadline",
            "ambition",
        ),
    ),
    VerseCard(
        reference="Bhagavad Gita 6.5",
        shloka=(
            "उद्धरेदात्मनाऽत्मानं नात्मानमवसादयेत्। "
            "आत्मैव ह्यात्मनो बन्धुरात्मैव रिपुरात्मनः॥"
        ),
        meaning=(
            "A person should raise oneself with one's own mind and not pull oneself down. "
            "The mind can become our closest friend or our strongest enemy."
        ),
        word_meaning=(
            "uddharet: one should uplift; atmana: by the self; atmanam: the self; "
            "na: not; atmanam: the self; avasadayet: degrade; atma eva: the self alone; "
            "hi: indeed; atmanah: for oneself; bandhu: friend; atma eva: the self alone; "
            "ripuh: enemy; atmanah: for oneself."
        ),
        advice=(
            "Speak to yourself like a guide, not a bully. Build one supportive habit that makes your mind an ally."
        ),
        tags=(
            "self-doubt",
            "confidence",
            "motivation",
            "discipline",
            "mindset",
            "inner strength",
            "low energy",
            "stuck",
        ),
    ),
    VerseCard(
        reference="Bhagavad Gita 2.14",
        shloka=(
            "मात्रास्पर्शास्तु कौन्तेय शीतोष्णसुखदुःखदाः। "
            "आगमापायिनोऽनित्यास्तांस्तितिक्षस्व भारत॥"
        ),
        meaning=(
            "Pleasure and pain, comfort and discomfort, come and go like seasons. "
            "They are temporary, so learn to endure them with steadiness."
        ),
        word_meaning=(
            "matra-sparsah: contact of the senses with objects; tu: indeed; kaunteya: O son of Kunti; "
            "sita-usna: cold and heat; sukha-duhkha-dah: givers of pleasure and pain; "
            "agama-apayinah: appearing and disappearing; anityah: temporary; "
            "tan: them; titikshasva: endure patiently; bharata: O descendant of Bharata."
        ),
        advice=(
            "What feels intense right now is real, but it is not permanent. Give yourself permission to breathe before reacting."
        ),
        tags=(
            "pain",
            "grief",
            "stress",
            "loss",
            "change",
            "hardship",
            "emotions",
            "sadness",
            "breakup",
        ),
    ),
    VerseCard(
        reference="Bhagavad Gita 6.26",
        shloka=(
            "यतो यतो निश्चरति मनश्चञ्चलमस्थिरम्। "
            "ततस्ततो नियम्यैतदात्मन्येव वशं नयेत्॥"
        ),
        meaning=(
            "Whenever the restless mind wanders, gently bring it back under your guidance. "
            "Inner steadiness grows through repeated return, not instant perfection."
        ),
        word_meaning=(
            "yatah yatah: wherever and whenever; nishcharati: wanders away; manah: the mind; "
            "chanchalam: restless; asthiram: unsteady; tatah tatah: from there and there; "
            "niyamya: restraining; etat: this; atmani eva: to the self alone; "
            "vasham nayet: bring under control."
        ),
        advice=(
            "Do not treat distraction as failure. Each time you return your attention, you are training strength."
        ),
        tags=(
            "overthinking",
            "focus",
            "mind",
            "anxiety",
            "distraction",
            "restless",
            "meditation",
            "attention",
        ),
    ),
    VerseCard(
        reference="Bhagavad Gita 12.15",
        shloka=(
            "यस्मान्नोद्विजते लोको लोकान्नोद्विजते च यः। "
            "हर्षामर्षभयोद्वेगैर्मुक्तो यः स च मे प्रियः॥"
        ),
        meaning=(
            "One who neither disturbs others nor is easily disturbed by them, "
            "and who is free from agitation, fear, and bitterness, is deeply dear."
        ),
        word_meaning=(
            "yasmat: from whom; na udvijate: does not become disturbed; lokah: the world; "
            "lokat: from the world; na udvijate: is not disturbed; cha: and; yah: who; "
            "harsha: excessive elation; amarsha: resentment; bhaya: fear; udvegaih: anxieties; "
            "muktah: free; yah: who; sah: that person; cha: and; me: to me; priyah: dear."
        ),
        advice=(
            "In conflict, aim for calm strength instead of winning every emotional battle. Protect your peace without hardening your heart."
        ),
        tags=(
            "anger",
            "relationships",
            "conflict",
            "family",
            "friendship",
            "peace",
            "resentment",
            "fear",
        ),
    ),
    VerseCard(
        reference="Bhagavad Gita 18.66",
        shloka=(
            "सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज। "
            "अहं त्वां सर्वपापेभ्यो मोक्षयिष्यामि मा शुचः॥"
        ),
        meaning=(
            "Let go of the burden of trying to control everything and take refuge in the Divine. "
            "Do not give way to despair."
        ),
        word_meaning=(
            "sarva-dharman: all limited duties or identities; parityajya: abandoning; "
            "mam: unto Me; ekam: alone; sharanam: refuge; vraja: come; aham: I; "
            "tvam: you; sarva-papebhyah: from all sin or bondage; mokshayishyami: will liberate; "
            "ma: do not; shuchah: grieve."
        ),
        advice=(
            "When life feels bigger than your plans, pause and surrender the panic first. Clarity often returns after letting go of control."
        ),
        tags=(
            "fear",
            "uncertainty",
            "guilt",
            "trust",
            "surrender",
            "hopeless",
            "lost",
            "heavy",
        ),
    ),
    VerseCard(
        reference="Bhagavad Gita 3.30",
        shloka=(
            "मयि सर्वाणि कर्माणि संन्यस्याध्यात्मचेतसा। "
            "निराशीर्निर्ममो भूत्वा युध्यस्व विगतज्वरः॥"
        ),
        meaning=(
            "Dedicate your actions to a higher purpose, act without selfish anxiety, "
            "and do your duty free from feverish tension."
        ),
        word_meaning=(
            "mayi: unto Me; sarvani karmani: all actions; sannyasya: offering or renouncing into; "
            "adhyatma-chetasa: with spiritual awareness; nirashih: free from anxious expectation; "
            "nirmamah: free from possessiveness; bhutva: becoming; yudhyasva: engage in the struggle; "
            "vigata-jvarah: without inner fever or agitation."
        ),
        advice=(
            "If responsibility is exhausting you, reconnect with why the work matters. Purpose reduces panic and helps action feel cleaner."
        ),
        tags=(
            "burnout",
            "responsibility",
            "duty",
            "service",
            "stress",
            "workload",
            "leadership",
            "pressure",
        ),
    ),
)


DEFAULT_VERSE = FALLBACK_VERSES[0]
