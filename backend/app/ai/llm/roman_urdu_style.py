"""
=========================================================
Roman Urdu Style Constants
Project : AI Mental Health Chatbot (FYP)

Purpose:
    Central vocabulary reference for Roman Urdu quality
    control.  Used by both the prompt templates (as
    guidance) and the validator (for automated checking).

    APPROVED_WORDS  — natural Pakistani Roman Urdu words
                      the LLM should prefer.
    FORBIDDEN_WORDS — formal Hindi/Sanskrit words that
                      sound unnatural in Pakistani speech.
=========================================================
"""

# =====================================================
# Approved Pakistani Roman Urdu vocabulary
# =====================================================

APPROVED_WORDS: list[str] = [
    # Pronouns
    "aap", "mujhe", "mujhy", "aapko", "main", "hum",
    "mera", "meri", "mere", "apna", "apni", "apne",

    # Common verbs / verb forms
    "hai", "hain", "hon", "tha", "thi", "the",
    "hona", "ho", "kar", "karo", "karna",
    "bata", "batao", "bata sakti hain", "bata sakte hain",
    "suno", "sunna", "samjho", "samajh",
    "jana", "jao", "aa", "aao",
    "raha", "rahi", "rahe",
    "hua", "hui", "hue",
    "lagta", "lagti", "chahein", "sakti hain", "sakte hain",
    "mehsoos karna", "mehsoos kar rahi", "mehsoos kar rahe",

    # Feelings / emotions
    "udaas", "udas", "pareshan", "takleef", "dard",
    "dukh", "khushi", "fikr", "ghabrana", "dara hua",
    "akela", "akeli", "thaka hua", "thaki hui",
    "tension", "stress", "anxiety", "okay",

    # Descriptors
    "bohat", "bht", "bahut", "zyada", "thora",
    "bilkul", "sirf", "bas", "acha", "achha", "bura",
    "theek", "mushkil", "asaan",

    # Time / place
    "aaj", "aj", "kal", "abhi", "phir", "kab",
    "ghar", "bahar", "yahan", "wahan",

    # Question words
    "kya", "kyun", "kahan", "kaisa", "kaisi", "kaise",
    "kon", "kaun",

    # Connectors
    "aur", "lekin", "ya", "jo", "ke", "ka", "ki",
    "ko", "se", "ne", "par", "bhi", "nahi", "nhi",
    "agar", "toh", "to",

    # Supportive phrases
    "madad", "saath", "baat", "dil",
    "zindagi", "waqt", "log", "kuch", "sab",
    "samajh", "sunna", "yahan hoon", "aapke saath hoon",
    "mujhe afsos hai", "mujhe khushi hai",
]

# =====================================================
# Forbidden — formal Hindi / Sanskrit vocabulary
# that sounds unnatural in Pakistani Roman Urdu
# =====================================================

FORBIDDEN_WORDS: list[str] = [
    # Formal Hindi problem / solution words
    "samasya",
    "sujhav",
    "nivaran",
    "upay",
    "samadhan",

    # Formal Hindi emotional / abstract words
    "peeda",
    "anand",
    "vyakti",
    "vartamaan",
    "vishay",
    "prashn",
    "prashna",

    # Medical / clinical Hindi — with all common spelling variants
    "chikitsa",
    "aavashyakta",   # double-a spelling
    "avashyakta",    # single-a spelling — LLM commonly uses this
    "avashyak",      # shortened single-a
    "aavashyak",     # shortened double-a
    "samarth",
    "samagri",

    # Other unnatural Hindi
    "pratyek",
    "avastha",
    "karya",
    "sthiti",
    "nirdesh",
    "nirdeshit",
    "prakriya",
    "sambandh",
    "sthaan",
    "sthan",
    "vastu",
    "uttar",

    # Additional formal Hindi words LLMs commonly produce
    "sahayata",      # help — say "madad"
    "margdarshan",   # guidance
    "unnati",        # progress
    "samvad",        # conversation
    "spasht",        # clear
    "swasth",        # healthy
    "prayas",        # effort — say "koshish"
    "avsar",         # opportunity
    "vichar",        # thought — say "soch"
    "sthir",         # stable
    "samay",         # time — say "waqt"
    "vyavhar",       # behaviour
    "suvidhaa",      # convenience
    "suvidha",       # same word, different spelling
    "stithi",        # situation variant
    "astitva",       # existence
    "anubhav",       # experience — say "tajurba"
    "mahatva",       # importance
    "mahatvapoorn",  # important

    # Family / social words that LLMs often say in formal Hindi style
    "parivaar",      # family — say "family" or "ghar waale"
    "parivajan",     # family members (very formal)
    "samaj",         # society (formal context)
    "saksham",       # capable — say "capable" or "kaam kar sakne waala"
    "yogya",         # worthy/capable (formal Hindi)
    "nischit",       # certain (formal)
    "nischay",       # determination (formal)
    "uttardayi",     # responsible (formal)
    "kartavya",      # duty (formal)
    "seva",          # service (formal — acceptable in religious context but LLMs overuse)
    "prabandh",      # management (formal)
    "nirman",        # construction/building (formal)
    "siddh",         # proven/established (formal)
    "labh",          # benefit (formal — say "faida")
    "prabhav",       # effect/influence (formal — say "asar")
    "drishtikon",    # perspective (very formal)
    "parishram",     # hard work (formal — say "mehnat")
    "sweekar",       # acceptance (formal)
    "tyag",          # sacrifice (formal)
    "nirnay",        # decision (formal — say "faisla")
]

# =====================================================
# Max retry attempts for regeneration
# =====================================================

MAX_REGENERATE_ATTEMPTS: int = 2
