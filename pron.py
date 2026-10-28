"""Prononciation « à la française » d'une translittération kannada."""
import re

_MAP = [
    ("chh", "tch"), ("ch", "tch"), ("jh", "dj"), ("j", "dj"),
    ("sh", "ch"), ("ṣ", "ch"), ("ś", "ch"),
    ("kh", "k"), ("gh", "g"), ("ṭh", "t"), ("ḍh", "d"), ("th", "t"), ("dh", "d"),
    ("ph", "f"), ("bh", "b"),
    ("ṭ", "t"), ("ḍ", "d"), ("ṇ", "n"), ("ḷ", "l"), ("ñ", "gn"), ("ṅ", "ng"), ("ṛ", "ri"),
    ("ai", "aï"), ("au", "aou"),
    ("ā", "aa"), ("ī", "ii"), ("ū", "ou"), ("ē", "éé"), ("ō", "ô"),
    ("u", "ou"), ("e", "é"),
]
_VOW = set("aeiouéèôïaā")


def _word(w):
    if not w or w[0].isupper():  # nom propre : laissé tel quel
        return w
    t = w.lower()
    out = ""
    i = 0
    while i < len(t):
        for src, dst in _MAP:
            if t.startswith(src, i):
                out += dst
                i += len(src)
                break
        else:
            out += t[i]
            i += 1
    # « g » dur devant é / i → gu
    out = re.sub(r"g(?=[éi])", "gu", out)
    # « s » entre voyelles → ss (sinon lu « z »)
    out = re.sub(r"(?<=[aeiouéôï])s(?=[aeiouéôï])", "ss", out)
    # « y » après voyelle et avant consonne ou en fin de mot → « ï » (āytu → aaï-tou)
    out = re.sub(r"(?<=[aeiouéôï])y(?=$|[^aeiouéôï])", "ï", out)
    # découpage en syllabes : on coupe avant chaque groupe de consonnes suivi d'une voyelle
    # (« anna » → a-nna, pour éviter la lecture nasale « an-na »)
    units = re.findall(r"(?:aou|aï|aa|ii|ou|éé|tch|dj|gu|gn|ng|ch|[a-zéèôï])", out)
    syl, cur = [], ""
    vow = {"a", "i", "ou", "é", "éé", "ô", "o", "aa", "ii", "aï", "aou", "è", "ï"}
    k = 0
    while k < len(units):
        u = units[k]
        cur += u
        if u in vow:
            rest = units[k + 1:]
            cons = []
            for r in rest:
                if r in vow:
                    break
                cons.append(r)
            if cons and len(cons) < len(rest):
                # groupe de consonnes avant la voyelle suivante
                first = cons[0]
                glide = len(cons) > 1 and cons[1] in ("y", "r", "l", "v")
                if len(cons) >= 2 and cons[0] != cons[1] and first not in ("n", "m") and not glide \
                        and first not in ("tch", "dj", "gu", "gn", "ng", "ch"):
                    cur += first  # la première consonne ferme la syllabe (bar-tii)
                    k += 1
                syl.append(cur)
                cur = ""
        k += 1
    if cur:
        syl.append(cur)
    return "-".join(syl)


def pron(tr):
    tr = re.sub(r"[?!…]", "", tr).strip()
    parts = []
    for tok in re.split(r"(\s+|/|,)", tr):
        if tok is None or tok == "":
            continue
        if re.fullmatch(r"\s+|/|,", tok):
            parts.append(tok)
        else:
            parts.append(_word(tok))
    return "".join(parts).replace("  ", " ").strip()


if __name__ == "__main__":
    for t in ["ēḷu", "nīru", "kāphi", "chennāgide", "anna", "haudu", "namaskāra", "ūṭa āytā?",
              "nimmannu nōḍi tumbā khushi āytu", "hōgbartīni", "dhanyavāda", "sakkare", "hesaru",
              "gottilla", "ombattu", "kṣamisi", "vidyārthini", "maneyalli", "ondu", "sanje", "nīvu bartīra?"]:
        print(f"{t:35} {pron(t)}")
