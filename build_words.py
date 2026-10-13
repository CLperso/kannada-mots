"""Génère words.json.

Progression : d'abord des mots seuls, puis des groupes de deux mots,
puis des phrases courtes, et les phrases longues seulement quand
tous leurs morceaux sont connus. Le reste du niveau 1 (data_n1.py)
suit, chaque unité triée de la plus courte à la plus longue expression.
"""
import hashlib
import json
import re

from data_n1 import NIVEAU_1

# Premier mois : 30 unités de 10, du mot seul à la phrase courte.
# Semaine 1 : mots seuls · semaine 2 : verbes, adjectifs, deux mots ·
# semaine 3 : phrases de trois mots · semaine 4 : petites conversations.
DEBUT = [
("Semaine 1 · les tout premiers mots", [
 ("bonjour", "namaskāra", "ನಮಸ್ಕಾರ", "mains jointes ; le salut respectueux, à toute heure"),
 ("oui", "haudu", "ಹೌದು", None),
 ("non / il n'y en a pas", "illa", "ಇಲ್ಲ", None),
 ("d'accord", "sari", "ಸರಿ", None),
 ("merci", "dhanyavāda", "ಧನ್ಯವಾದ", None),
 ("je veux / il faut", "bēku", "ಬೇಕು", None),
 ("je ne veux pas", "bēḍa", "ಬೇಡ", None),
 ("l'eau", "nīru", "ನೀರು", None),
 ("le repas", "ūṭa", "ಊಟ", None),
 ("venez / entrez", "banni", "ಬನ್ನಿ", None),
]),
("Semaine 1 · moi, toi, vous", [
 ("je / moi", "nānu", "ನಾನು", None),
 ("tu / toi (proches)", "nīnu", "ನೀನು", None),
 ("vous (respect)", "nīvu", "ನೀವು", "avec les parents de ton partenaire"),
 ("il / elle (respect)", "avaru", "ಅವರು", "pour parler des aînés"),
 ("il (familier)", "avanu", "ಅವನು", None),
 ("elle (familier)", "avaḷu", "ಅವಳು", None),
 ("nous", "nāvu", "ನಾವು", None),
 ("ceci / ça", "idu", "ಇದು", None),
 ("cela (là-bas)", "adu", "ಅದು", None),
 ("qui ?", "yāru?", "ಯಾರು?", None),
]),
("Semaine 1 · questions et petits mots", [
 ("quoi ?", "ēnu?", "ಏನು?", None),
 ("où ?", "elli?", "ಎಲ್ಲಿ?", None),
 ("pourquoi ?", "yāke?", "ಯಾಕೆ?", None),
 ("comment ?", "hēge?", "ಹೇಗೆ?", None),
 ("combien ?", "eṣṭu?", "ಎಷ್ಟು?", None),
 ("quand ?", "yāvāga?", "ಯಾವಾಗ?", None),
 ("ici", "illi", "ಇಲ್ಲಿ", None),
 ("là-bas", "alli", "ಅಲ್ಲಿ", None),
 ("maintenant", "īga", "ಈಗ", None),
 ("très / beaucoup", "tumbā", "ತುಂಬಾ", None),
]),
("Semaine 1 · la famille", [
 ("maman", "amma", "ಅಮ್ಮ", None),
 ("papa", "appa", "ಅಪ್ಪ", None),
 ("belle-mère (mère du partenaire)", "atte", "ಅತ್ತೆ", None),
 ("beau-père (père du partenaire)", "māva", "ಮಾವ", None),
 ("grand frère", "aṇṇa", "ಅಣ್ಣ", None),
 ("grande sœur", "akka", "ಅಕ್ಕ", None),
 ("petit frère", "tamma", "ತಮ್ಮ", None),
 ("petite sœur", "tangi", "ತಂಗಿ", None),
 ("fils", "maga", "ಮಗ", None),
 ("fille (enfant)", "magaḷu", "ಮಗಳು", None),
]),
("Semaine 1 · compter jusqu'à 10", [
 ("un (1)", "ondu", "ಒಂದು", None),
 ("deux (2)", "eraḍu", "ಎರಡು", None),
 ("trois (3)", "mūru", "ಮೂರು", None),
 ("quatre (4)", "nālku", "ನಾಲ್ಕು", None),
 ("cinq (5)", "aidu", "ಐದು", None),
 ("six (6)", "āru", "ಆರು", None),
 ("sept (7)", "ēḷu", "ಏಳು", None),
 ("huit (8)", "eṇṭu", "ಎಂಟು", None),
 ("neuf (9)", "ombattu", "ಒಂಬತ್ತು", None),
 ("dix (10)", "hattu", "ಹತ್ತು", None),
]),
("Semaine 1 · à boire, à manger", [
 ("le café", "kāphi", "ಕಾಫಿ", None),
 ("le thé", "ṭī", "ಟೀ", None),
 ("le lait", "hālu", "ಹಾಲು", None),
 ("le riz (cuit)", "anna", "ಅನ್ನ", None),
 ("la dosa", "dōse", "ದೋಸೆ", None),
 ("l'idli", "iḍli", "ಇಡ್ಲಿ", None),
 ("le fruit", "haṇṇu", "ಹಣ್ಣು", None),
 ("les légumes", "tarakāri", "ತರಕಾರಿ", None),
 ("le sucre", "sakkare", "ಸಕ್ಕರೆ", None),
 ("le sel", "uppu", "ಉಪ್ಪು", None),
]),
("Semaine 1 · la maison et la vie", [
 ("la maison", "mane", "ಮನೆ", None),
 ("le nom", "hesaru", "ಹೆಸರು", None),
 ("la ville / le village d'origine", "ūru", "ಊರು", None),
 ("l'ami", "snēhita", "ಸ್ನೇಹಿತ", None),
 ("le travail", "kelsa", "ಕೆಲಸ", None),
 ("le jour", "dina", "ದಿನ", None),
 ("l'argent", "duḍḍu", "ದುಡ್ಡು", None),
 ("la porte", "bāgilu", "ಬಾಗಿಲು", None),
 ("la chaise", "kurchi", "ಕುರ್ಚಿ", None),
 ("le lit", "hāsige", "ಹಾಸಿಗೆ", None),
]),
("Semaine 2 · verbes polis", [
 ("asseyez-vous", "kūtkoḷḷi", "ಕೂತ್ಕೊಳ್ಳಿ", None),
 ("mangez", "tinni", "ತಿನ್ನಿ", None),
 ("buvez", "kuḍiyiri", "ಕುಡಿಯಿರಿ", None),
 ("regardez", "nōḍi", "ನೋಡಿ", None),
 ("donnez", "koḍi", "ಕೊಡಿ", None),
 ("prenez", "tagoḷḷi", "ತಗೊಳ್ಳಿ", None),
 ("dites", "hēḷi", "ಹೇಳಿ", None),
 ("attendez", "kāyiri", "ಕಾಯಿರಿ", None),
 ("allez", "hōgi", "ಹೋಗಿ", None),
 ("faites", "māḍi", "ಮಾಡಿ", "la forme polie se termine en -i"),
]),
("Semaine 2 · décrire", [
 ("c'est bien / c'est bon", "chennāgide", "ಚೆನ್ನಾಗಿದೆ", None),
 ("grand", "doḍḍa", "ದೊಡ್ಡ", None),
 ("petit", "chikka", "ಚಿಕ್ಕ", None),
 ("chaud", "bisi", "ಬಿಸಿ", None),
 ("froid", "taṇṇage", "ತಣ್ಣಗೆ", None),
 ("mauvais / pas bon", "keṭṭa", "ಕೆಟ್ಟ", None),
 ("épicé", "khāra", "ಖಾರ", None),
 ("la joie", "khushi", "ಖುಷಿ", None),
 ("un peu", "svalpa", "ಸ್ವಲ್ಪ", None),
 ("ça suffit / assez", "sāku", "ಸಾಕು", None),
]),
("Semaine 2 · je veux, je ne veux pas", [
 ("je veux de l'eau", "nīru bēku", "ನೀರು ಬೇಕು", "on met juste le mot, puis bēku"),
 ("je veux du café", "kāphi bēku", "ಕಾಫಿ ಬೇಕು", None),
 ("je veux du lait", "hālu bēku", "ಹಾಲು ಬೇಕು", None),
 ("pas de thé, merci", "ṭī bēḍa", "ಟೀ ಬೇಡ", None),
 ("pas de sucre", "sakkare bēḍa", "ಸಕ್ಕರೆ ಬೇಡ", None),
 ("je veux celui-ci", "idu bēku", "ಇದು ಬೇಕು", None),
 ("je ne veux pas celui-là", "adu bēḍa", "ಅದು ಬೇಡ", None),
 ("un peu d'eau", "svalpa nīru", "ಸ್ವಲ್ಪ ನೀರು", None),
 ("encore un peu", "innu svalpa", "ಇನ್ನು ಸ್ವಲ್ಪ", None),
 ("je ne veux pas manger", "ūṭa bēḍa", "ಊಟ ಬೇಡ", None),
]),
("Semaine 2 · mon, votre", [
 ("ma maison", "nanna mane", "ನನ್ನ ಮನೆ", None),
 ("votre maison", "nimma mane", "ನಿಮ್ಮ ಮನೆ", None),
 ("ma maman", "nanna amma", "ನನ್ನ ಅಮ್ಮ", None),
 ("votre fils", "nimma maga", "ನಿಮ್ಮ ಮಗ", None),
 ("je m'appelle…", "nanna hesaru…", "ನನ್ನ ಹೆಸರು…", "« mon nom … »"),
 ("qu'est-ce que c'est ?", "idu ēnu?", "ಇದು ಏನು?", "le mot interrogatif prend la place de la réponse"),
 ("qui est-ce ?", "avaru yāru?", "ಅವರು ಯಾರು?", None),
 ("ça coûte combien ?", "idu eṣṭu?", "ಇದು ಎಷ್ಟು?", None),
 ("où est la maison ?", "mane elli?", "ಮನೆ ಎಲ್ಲಿ?", None),
 ("c'est très bien", "tumbā chennāgide", "ತುಂಬಾ ಚೆನ್ನಾಗಿದೆ", None),
]),
("Semaine 2 · il y a, il n'y a pas", [
 ("il y a / c'est là", "ide", "ಇದೆ", None),
 ("il y a du café ?", "kāphi ide?", "ಕಾಫಿ ಇದೆ?", "pour demander, on monte la voix"),
 ("il y a de l'eau", "nīru ide", "ನೀರು ಇದೆ", None),
 ("il n'y a pas de lait", "hālu illa", "ಹಾಲು ಇಲ್ಲ", None),
 ("je sais", "gottu", "ಗೊತ್ತು", None),
 ("je ne sais pas", "gottilla", "ಗೊತ್ತಿಲ್ಲ", None),
 ("ce n'est pas grave", "paravāgilla", "ಪರವಾಗಿಲ್ಲ", None),
 ("pardon / excusez-moi", "kṣamisi", "ಕ್ಷಮಿಸಿ", None),
 ("s'il vous plaît", "dayaviṭṭu", "ದಯವಿಟ್ಟು", None),
 ("une minute", "ondu nimiṣa", "ಒಂದು ನಿಮಿಷ", None),
]),
("Semaine 2 · saluer", [
 ("comment allez-vous ?", "hēgiddīra?", "ಹೇಗಿದ್ದೀರ?", None),
 ("je vais bien", "chennāgiddīni", "ಚೆನ್ನಾಗಿದ್ದೀನಿ", None),
 ("et vous ?", "nīvu?", "ನೀವು?", None),
 ("merci beaucoup", "dhanyavādagaḷu", "ಧನ್ಯವಾದಗಳು", None),
 ("bravo !", "shabhāsh!", "ಶಭಾಷ್!", None),
 ("à bientôt (« je reviens »)", "bartīni", "ಬರ್ತೀನಿ", None),
 ("au revoir (« je vais et je reviens »)", "hōgbartīni", "ಹೋಗ್ಬರ್ತೀನಿ", "on ne dit jamais « je pars »"),
 ("au revoir (réponse)", "hōgbanni", "ಹೋಗ್ಬನ್ನಿ", "« allez et revenez »"),
 ("vous avez mangé ?", "ūṭa āytā?", "ಊಟ ಆಯ್ತಾ?", "la question de tous les jours, comme « ça va ? »"),
 ("oui, j'ai mangé", "ūṭa āytu", "ಊಟ ಆಯ್ತು", None),
]),
("Semaine 2 · à table", [
 ("c'est délicieux", "tumbā ruchiyāgide", "ತುಂಬಾ ರುಚಿಯಾಗಿದೆ", None),
 ("j'ai bien mangé (« ventre plein »)", "hoṭṭe tumbitu", "ಹೊಟ್ಟೆ ತುಂಬಿತು", "très utile : on te ressert souvent"),
 ("pas trop épicé", "khāra kammi", "ಖಾರ ಕಮ್ಮಿ", None),
 ("ça suffit, merci", "sāku, dhanyavāda", "ಸಾಕು, ಧನ್ಯವಾದ", None),
 ("venez manger", "ūṭakke banni", "ಊಟಕ್ಕೆ ಬನ್ನಿ", None),
 ("buvez du café", "kāphi kuḍiyiri", "ಕಾಫಿ ಕುಡಿಯಿರಿ", None),
 ("donnez de l'eau", "nīru koḍi", "ನೀರು ಕೊಡಿ", None),
 ("donnez du riz", "anna koḍi", "ಅನ್ನ ಕೊಡಿ", None),
 ("je n'en veux plus", "innu bēḍa", "ಇನ್ನು ಬೇಡ", None),
 ("un café chaud", "bisi kāphi", "ಬಿಸಿ ಕಾಫಿ", None),
]),
("Semaine 3 · « c'est » sans verbe", [
 ("je suis étudiante", "nānu vidyārthini", "ನಾನು ವಿದ್ಯಾರ್ಥಿನಿ", "pas de verbe « être » : « moi étudiante »"),
 ("c'est ma belle-mère", "avaru nanna atte", "ಅವರು ನನ್ನ ಅತ್ತೆ", None),
 ("c'est ma maison", "idu nanna mane", "ಇದು ನನ್ನ ಮನೆ", None),
 ("c'est votre maison ?", "adu nimma mane?", "ಅದು ನಿಮ್ಮ ಮನೆ?", None),
 ("c'est mon ami", "avanu nanna snēhita", "ಅವನು ನನ್ನ ಸ್ನೇಹಿತ", None),
 ("ce n'est pas du café", "idu kāphi alla", "ಇದು ಕಾಫಿ ಅಲ್ಲ", "alla = « ce n'est pas » ; illa = « il n'y a pas »"),
 ("ce n'est pas de l'eau", "adu nīru alla", "ಅದು ನೀರು ಅಲ್ಲ", None),
 ("comment vous appelez-vous ?", "nimma hesaru ēnu?", "ನಿಮ್ಮ ಹೆಸರು ಏನು?", "« votre nom quoi ? »"),
 ("d'où êtes-vous ?", "nimma ūru yāvdu?", "ನಿಮ್ಮ ಊರು ಯಾವ್ದು?", None),
 ("je suis française", "nānu France-navaḷu", "ನಾನು ಫ್ರಾನ್ಸ್‌ನವಳು", None),
]),
("Semaine 3 · « à moi » (nanage)", [
 ("à moi / pour moi", "nanage", "ನನಗೆ", "en kannada : « à moi le café est nécessaire »"),
 ("je veux du café (« à moi café il faut »)", "nanage kāphi bēku", "ನನಗೆ ಕಾಫಿ ಬೇಕು", None),
 ("je ne sais pas (« à moi pas connu »)", "nanage gottilla", "ನನಗೆ ಗೊತ್ತಿಲ್ಲ", None),
 ("j'aime la dosa", "nanage dōse ishṭa", "ನನಗೆ ದೋಸೆ ಇಷ್ಟ", "« à moi la dosa plaît »"),
 ("je suis contente", "nanage khushi āytu", "ನನಗೆ ಖುಷಿ ಆಯ್ತು", "« à moi la joie est arrivée »"),
 ("je suis fatiguée", "nanage susthu āgide", "ನನಗೆ ಸುಸ್ತು ಆಗಿದೆ", None),
 ("j'ai faim", "nanage hasivu āgtide", "ನನಗೆ ಹಸಿವು ಆಗ್ತಿದೆ", "« à moi la faim arrive »"),
 ("je ne comprends pas", "nanage artha āgalla", "ನನಗೆ ಅರ್ಥ ಆಗಲ್ಲ", None),
 ("vous voulez du café ?", "nimage kāphi bēkā?", "ನಿಮಗೆ ಕಾಫಿ ಬೇಕಾ?", "nimage = à vous ; -ā = question"),
 ("qu'est-ce que tu veux ?", "ninage ēnu bēku?", "ನಿನಗೆ ಏನು ಬೇಕು?", None),
]),
("Semaine 3 · je fais (présent)", [
 ("je viens", "nānu bartīni", "ನಾನು ಬರ್ತೀನಿ", "-tīni = je, maintenant ou bientôt"),
 ("je vais (y aller)", "nānu hōgtīni", "ನಾನು ಹೋಗ್ತೀನಿ", None),
 ("je mange", "nānu tintīni", "ನಾನು ತಿಂತೀನಿ", None),
 ("je bois", "nānu kuḍītīni", "ನಾನು ಕುಡೀತೀನಿ", None),
 ("je fais", "nānu māḍtīni", "ನಾನು ಮಾಡ್ತೀನಿ", None),
 ("je regarde", "nānu nōḍtīni", "ನಾನು ನೋಡ್ತೀನಿ", None),
 ("je parle", "nānu mātāḍtīni", "ನಾನು ಮಾತಾಡ್ತೀನಿ", None),
 ("j'apprends", "nānu kalītīni", "ನಾನು ಕಲೀತೀನಿ", None),
 ("je dors", "nānu malagtīni", "ನಾನು ಮಲಗ್ತೀನಿ", None),
 ("je viens demain", "nāḷe bartīni", "ನಾಳೆ ಬರ್ತೀನಿ", "le même temps sert pour le futur"),
]),
("Semaine 3 · tu, vous, il (présent)", [
 ("vous venez ?", "nīvu bartīra?", "ನೀವು ಬರ್ತೀರ?", "-tīra = vous"),
 ("tu viens ?", "nīnu bartīya?", "ನೀನು ಬರ್ತೀಯ?", "-tīya = tu"),
 ("il / elle vient (respect)", "avaru bartāre", "ಅವರು ಬರ್ತಾರೆ", "-tāre = il, elle (respect), ils"),
 ("il vient", "avanu bartāne", "ಅವನು ಬರ್ತಾನೆ", "-tāne = il"),
 ("elle vient", "avaḷu bartāḷe", "ಅವಳು ಬರ್ತಾಳೆ", "-tāḷe = elle"),
 ("nous y allons", "nāvu hōgtīvi", "ನಾವು ಹೋಗ್ತೀವಿ", "-tīvi = nous"),
 ("que faites-vous ?", "nīvu ēnu māḍtīra?", "ನೀವು ಏನು ಮಾಡ್ತೀರ?", None),
 ("il boit du café (respect)", "avaru kāphi kuḍītāre", "ಅವರು ಕಾಫಿ ಕುಡೀತಾರೆ", None),
 ("maman fait la cuisine", "amma aḍige māḍtāre", "ಅಮ್ಮ ಅಡಿಗೆ ಮಾಡ್ತಾರೆ", None),
 ("je bois du café", "nānu kāphi kuḍītīni", "ನಾನು ಕಾಫಿ ಕುಡೀತೀನಿ", None),
]),
("Semaine 3 · dire non", [
 ("je ne viens pas", "nānu barolla", "ನಾನು ಬರೋಲ್ಲ", "verbe + -alla / -olla, la même forme pour tous"),
 ("je ne mange pas", "nānu tinnalla", "ನಾನು ತಿನ್ನಲ್ಲ", None),
 ("il ne vient pas", "avanu barolla", "ಅವನು ಬರೋಲ್ಲ", None),
 ("ça ne marche pas / impossible", "āgalla", "ಆಗಲ್ಲ", None),
 ("ça marche / c'est possible", "āgutte", "ಆಗುತ್ತೆ", None),
 ("je ne veux rien", "ēnū bēḍa", "ಏನೂ ಬೇಡ", None),
 ("je ne mange pas de viande", "nānu māmsa tinnalla", "ನಾನು ಮಾಂಸ ತಿನ್ನಲ್ಲ", None),
 ("je ne viens pas aujourd'hui", "ivattu barolla", "ಇವತ್ತು ಬರೋಲ್ಲ", None),
 ("ce n'est rien", "ēnū illa", "ಏನೂ ಇಲ್ಲ", None),
 ("je n'aime pas", "nanage ishṭa illa", "ನನಗೆ ಇಷ್ಟ ಇಲ್ಲ", None),
]),
("Semaine 3 · où ?", [
 ("à la maison", "maneyalli", "ಮನೆಯಲ್ಲಿ", "« dans, à » : -alli (mane → maneyalli)"),
 ("c'est ici", "illi ide", "ಇಲ್ಲಿ ಇದೆ", None),
 ("c'est là-bas", "alli ide", "ಅಲ್ಲಿ ಇದೆ", None),
 ("où allez-vous ?", "elli hōgtīra?", "ಎಲ್ಲಿ ಹೋಗ್ತೀರ?", None),
 ("où est le café ?", "kāphi elli ide?", "ಕಾಫಿ ಎಲ್ಲಿ ಇದೆ?", None),
 ("où êtes-vous ?", "nīvu elli iddīra?", "ನೀವು ಎಲ್ಲಿ ಇದ್ದೀರ?", None),
 ("je suis à la maison", "nānu maneyalli iddīni", "ನಾನು ಮನೆಯಲ್ಲಿ ಇದ್ದೀನಿ", "iddīni = je suis (quelque part)"),
 ("j'habite à Paris", "nānu Paris-alli iddīni", "ನಾನು ಪ್ಯಾರಿಸ್‌ನಲ್ಲಿ ಇದ್ದೀನಿ", None),
 ("dans la cuisine", "aḍige maneyalli", "ಅಡಿಗೆ ಮನೆಯಲ್ಲಿ", None),
 ("où sont les toilettes ?", "śaucālaya elli ide?", "ಶೌಚಾಲಯ ಎಲ್ಲಿ ಇದೆ?", None),
]),
("Semaine 3 · quand ?", [
 ("aujourd'hui", "ivattu", "ಇವತ್ತು", None),
 ("demain", "nāḷe", "ನಾಳೆ", None),
 ("hier", "ninne", "ನಿನ್ನೆ", None),
 ("le matin", "beḷigge", "ಬೆಳಿಗ್ಗೆ", None),
 ("le soir", "sanje", "ಸಂಜೆ", None),
 ("la nuit", "rātri", "ರಾತ್ರಿ", None),
 ("après / plus tard", "āmēle", "ಆಮೇಲೆ", None),
 ("vite / tôt", "bēga", "ಬೇಗ", None),
 ("ce soir", "ivattu sanje", "ಇವತ್ತು ಸಂಜೆ", None),
 ("demain matin", "nāḷe beḷigge", "ನಾಳೆ ಬೆಳಿಗ್ಗೆ", None),
]),
("Semaine 4 · le passé", [
 ("je suis venue", "nānu bande", "ನಾನು ಬಂದೆ", "passé « je » : terminaison -e"),
 ("je suis allée", "nānu hōde", "ನಾನು ಹೋದೆ", None),
 ("j'ai mangé", "nānu tinde", "ನಾನು ತಿಂದೆ", None),
 ("j'ai bu", "nānu kuḍide", "ನಾನು ಕುಡಿದೆ", None),
 ("j'ai vu", "nānu nōḍide", "ನಾನು ನೋಡಿದೆ", None),
 ("j'ai fait", "nānu māḍide", "ನಾನು ಮಾಡಿದೆ", None),
 ("j'ai parlé", "nānu mātāḍide", "ನಾನು ಮಾತಾಡಿದೆ", None),
 ("j'ai appris", "nānu kalite", "ನಾನು ಕಲಿತೆ", None),
 ("hier je suis venue", "ninne nānu bande", "ನಿನ್ನೆ ನಾನು ಬಂದೆ", None),
 ("qu'avez-vous fait ?", "nīvu ēnu māḍidri?", "ನೀವು ಏನು ಮಾಡಿದ್ರಿ?", None),
]),
("Semaine 4 · comprendre et apprendre", [
 ("j'ai compris", "artha āytu", "ಅರ್ಥ ಆಯ್ತು", None),
 ("redites-le", "matte hēḷi", "ಮತ್ತೆ ಹೇಳಿ", None),
 ("écrivez-le", "bareyiri", "ಬರೆಯಿರಿ", None),
 ("corrigez-moi (« si je me trompe, dites »)", "tappidre hēḷi", "ತಪ್ಪಿದ್ರೆ ಹೇಳಿ", None),
 ("ça veut dire quoi, … ?", "… andre ēnu?", "… ಅಂದ್ರೆ ಏನು?", None),
 ("je ne connais pas ce mot", "ī pada gottilla", "ಈ ಪದ ಗೊತ್ತಿಲ್ಲ", None),
 ("parlez un peu plus lentement", "svalpa nidhāna mātāḍi", "ಸ್ವಲ್ಪ ನಿಧಾನ ಮಾತಾಡಿ", None),
 ("comment dit-on en kannada ?", "Kannaḍadalli hēge hēḷōdu?", "ಕನ್ನಡದಲ್ಲಿ ಹೇಗೆ ಹೇಳೋದು?", None),
 ("j'apprends le kannada", "nānu Kannaḍa kalītā iddīni", "ನಾನು ಕನ್ನಡ ಕಲೀತಾ ಇದ್ದೀನಿ", "ça fait toujours plaisir à entendre"),
 ("je parle un peu kannada", "nanage svalpa Kannaḍa barutte", "ನನಗೆ ಸ್ವಲ್ಪ ಕನ್ನಡ ಬರುತ್ತೆ", "« à moi un peu de kannada vient »"),
]),
("Semaine 4 · allons-y, il faut", [
 ("allons-y", "hōgōṇa", "ಹೋಗೋಣ", "-ōṇa = « faisons »"),
 ("mangeons", "tinnōṇa", "ತಿನ್ನೋಣ", None),
 ("regardons", "nōḍōṇa", "ನೋಡೋಣ", None),
 ("parlons", "mātāḍōṇa", "ಮಾತಾಡೋಣ", None),
 ("à demain (« on se voit demain »)", "nāḷe sigōṇa", "ನಾಳೆ ಸಿಗೋಣ", None),
 ("on se parle plus tard", "āmēle mātāḍōṇa", "ಆಮೇಲೆ ಮಾತಾಡೋಣ", None),
 ("mangeons ensemble", "ūṭa māḍōṇa", "ಊಟ ಮಾಡೋಣ", None),
 ("je dois y aller", "nānu hōgbēku", "ನಾನು ಹೋಗಬೇಕು", "verbe + bēku = je dois"),
 ("nous devons y aller", "nāvu hōgbēku", "ನಾವು ಹೋಗಬೇಕು", None),
 ("je dois apprendre", "nānu kalībēku", "ನಾನು ಕಲೀಬೇಕು", None),
]),
("Semaine 4 · comment je me sens", [
 ("j'aime", "nanage ishṭa", "ನನಗೆ ಇಷ್ಟ", None),
 ("très contente", "tumbā khushi", "ತುಂಬಾ ಖುಷಿ", None),
 ("j'ai froid", "nanage chaḷi āgtide", "ನನಗೆ ಚಳಿ ಆಗ್ತಿದೆ", None),
 ("il fait chaud", "sekhe ide", "ಸೆಕೆ ಇದೆ", None),
 ("j'ai sommeil", "nanage nidde bartide", "ನನಗೆ ನಿದ್ದೆ ಬರ್ತಿದೆ", None),
 ("je ne me sens pas bien", "nanage huṣāru illa", "ನನಗೆ ಹುಷಾರು ಇಲ್ಲ", None),
 ("mal au ventre", "hoṭṭe nōvu", "ಹೊಟ್ಟೆ ನೋವು", None),
 ("j'ai soif", "nanage bāyārike āgtide", "ನನಗೆ ಬಾಯಾರಿಕೆ ಆಗ್ತಿದೆ", None),
 ("prenez soin de vous", "huṣāru", "ಹುಷಾರು", None),
 ("vous êtes très gentil·le", "nīvu tumbā oḷḷeyavru", "ನೀವು ತುಂಬಾ ಒಳ್ಳೆಯವ್ರು", None),
]),
("Semaine 4 · avec ton partenaire", [
 ("mon trésor", "chinna", "ಚಿನ್ನ", "littéralement « or »"),
 ("un bisou", "muttu", "ಮುತ್ತು", None),
 ("l'amour", "prīti", "ಪ್ರೀತಿ", None),
 ("viens ici", "illi bā", "ಇಲ್ಲಿ ಬಾ", None),
 ("avec toi", "ninna jote", "ನಿನ್ನ ಜೊತೆ", None),
 ("tu me manques", "ninna nenapāgtide", "ನಿನ್ನ ನೆನಪಾಗ್ತಿದೆ", None),
 ("dors bien", "chennāgi malkō", "ಚೆನ್ನಾಗಿ ಮಲ್ಕೊ", None),
 ("qu'est-ce que tu fais ?", "ēnu māḍtā iddīya?", "ಏನು ಮಾಡ್ತಾ ಇದ್ದೀಯ?", None),
 ("je t'aime", "nā ninna prītistīni", "ನಾ ನಿನ್ನ ಪ್ರೀತಿಸ್ತೀನಿ", "forme parlée"),
 ("tu es très beau / très belle", "nīnu tumbā chennāgiddīya", "ನೀನು ತುಂಬಾ ಚೆನ್ನಾಗಿದ್ದೀಯ", None),
]),
("Semaine 4 · relier les idées", [
 ("et", "mattu", "ಮತ್ತು", None),
 ("mais", "ādre", "ಆದ್ರೆ", None),
 ("ou", "athavā", "ಅಥವಾ", None),
 ("parce que", "yākandre", "ಯಾಕಂದ್ರೆ", None),
 ("donc / c'est pour ça", "adakke", "ಅದಕ್ಕೆ", None),
 ("avec", "jote", "ಜೊತೆ", None),
 ("sans", "illade", "ಇಲ್ಲದೆ", None),
 ("toujours", "yāvāglū", "ಯಾವಾಗ್ಲೂ", None),
 ("parfois", "kelavu sala", "ಕೆಲವು ಸಲ", None),
 ("encore / pas encore", "innū", "ಇನ್ನೂ", None),
]),
("Semaine 4 · en famille", [
 ("asseyez-vous, je vous en prie", "nīvu kūtkoḷḷi", "ನೀವು ಕೂತ್ಕೊಳ್ಳಿ", None),
 ("rien, merci", "ēnū bēḍa, dhanyavāda", "ಏನೂ ಬೇಡ, ಧನ್ಯವಾದ", None),
 ("comment va votre famille ?", "nimma kuṭumba hēgide?", "ನಿಮ್ಮ ಕುಟುಂಬ ಹೇಗಿದೆ?", None),
 ("tout le monde va bien", "ellaru chennāgiddāre", "ಎಲ್ಲರು ಚೆನ್ನಾಗಿದ್ದಾರೆ", None),
 ("je peux aider ?", "nānu sahāya māḍlā?", "ನಾನು ಸಹಾಯ ಮಾಡ್ಲಾ?", "très apprécié à la cuisine"),
 ("vous avez besoin d'aide ?", "nimage sahāya bēkā?", "ನಿಮಗೆ ಸಹಾಯ ಬೇಕಾ?", None),
 ("on fait quoi demain ?", "nāḷe ēnu māḍōṇa?", "ನಾಳೆ ಏನು ಮಾಡೋಣ?", None),
 ("le repas était délicieux", "ūṭa tumbā ruchiyāgittu", "ಊಟ ತುಂಬಾ ರುಚಿಯಾಗಿತ್ತು", None),
 ("je dois apprendre la cuisine", "nānu aḍige kalībēku", "ನಾನು ಅಡಿಗೆ ಕಲೀಬೇಕು", None),
 ("votre maison est très belle", "nimma mane tumbā chennāgide", "ನಿಮ್ಮ ಮನೆ ತುಂಬಾ ಚೆನ್ನಾಗಿದೆ", None),
]),
("Semaine 4 · parler de moi", [
 ("j'ai… ans (« mon âge… »)", "nanna vayassu…", "ನನ್ನ ವಯಸ್ಸು…", None),
 ("quel est votre travail ?", "nimma kelsa ēnu?", "ನಿಮ್ಮ ಕೆಲಸ ಏನು?", None),
 ("je donne un cours", "nānu pāṭha māḍtīni", "ನಾನು ಪಾಠ ಮಾಡ್ತೀನಿ", None),
 ("je fais de la recherche", "nānu saṁśōdhane māḍtīni", "ನಾನು ಸಂಶೋಧನೆ ಮಾಡ್ತೀನಿ", None),
 ("je suis venue de France", "nānu France-inda bande", "ನಾನು ಫ್ರಾನ್ಸ್‌ನಿಂದ ಬಂದೆ", "« depuis » : -inda"),
 ("j'aime Bangalore", "nanage Bengaḷūru ishṭa", "ನನಗೆ ಬೆಂಗಳೂರು ಇಷ್ಟ", None),
 ("j'ai une chatte", "nanna hatra bekku ide", "ನನ್ನ ಹತ್ರ ಬೆಕ್ಕು ಇದೆ", "« près de moi, un chat il y a »"),
 ("elle s'appelle Micky", "adara hesaru Micky", "ಅದರ ಹೆಸರು ಮಿಕ್ಕಿ", "pour un animal on dit adu (« ça »)"),
 ("que faites-vous comme travail ?", "nīvu ēnu kelsa māḍtīra?", "ನೀವು ಏನು ಕೆಲಸ ಮಾಡ್ತೀರ?", None),
 ("c'est ma première fois en Inde", "India-ge idu modala sala", "ಇಂಡಿಯಾಗೆ ಇದು ಮೊದಲ ಸಲ", None),
]),
("Semaine 4 · construire : ravie de vous rencontrer", [
 ("je suis contente (« la joie est arrivée »)", "khushi āytu", "ಖುಷಿ ಆಯ್ತು", None),
 ("je suis très contente", "tumbā khushi āytu", "ತುಂಬಾ ಖುಷಿ ಆಯ್ತು", None),
 ("vous (complément)", "nimmannu", "ನಿಮ್ಮನ್ನು", "nimma + -annu, la marque du complément"),
 ("en vous voyant", "nimmannu nōḍi", "ನಿಮ್ಮನ್ನು ನೋಡಿ", None),
 ("ravie de vous voir", "nimmannu nōḍi khushi āytu", "ನಿಮ್ಮನ್ನು ನೋಡಿ ಖುಷಿ ಆಯ್ತು", None),
 ("ravie de vous rencontrer", "nimmannu nōḍi tumbā khushi āytu", "ನಿಮ್ಮನ್ನು ನೋಡಿ ತುಂಬಾ ಖುಷಿ ಆಯ್ತು", "« vous voyant, très joie est arrivée »"),
]),
]

# ordre des unités restantes du niveau 1
SUITE = [
 "Les mots essentiels", "Saluer", "Se présenter", "Les pronoms", "Oui, non, il y a",
 "La famille", "Le possessif", "Les questions", "Les nombres de 1 à 10",
 "Boire et manger", "Les plats", "« À moi » : le datif", "La maison",
 "Où ? (« dans », « à »)", "Demander : l'impératif", "Je fais : le présent",
 "Conjuguer un verbe", "Dire non au verbe", "À table", "Le temps",
 "Les jours et le calendrier", "L'heure", "Ma journée", "Le passé",
 "Comprendre et apprendre", "Sentiments et santé", "Compléments", "Avec ton partenaire",
 "Allons-y : « -ōṇa »", "Verbes courants", "Le corps", "Décrire", "Les couleurs",
 "Les nombres jusqu'à 1000", "Météo et nature", "Les gens", "Les lieux",
 "Les transports", "Les vêtements", "Loisirs", "Études et travail", "Les animaux",
 "Relier les idées", "Quantités", "Décrire (suite)", "Compter (suite)", "Fêtes",
 "Se déplacer", "Faire des courses",
]


def norm(tr):
    return re.sub(r"[^\w]", "", tr.lower())


def nwords(tr):
    return len([t for t in re.split(r"[\s/]+", tr) if t.strip("…?!.,")])


def make_id(tr, fr):
    return "w" + hashlib.md5(f"{norm(tr)}|{fr}".encode()).hexdigest()[:10]


# anciens identifiants, pour garder la progression déjà faite
old = json.load(open("words_previous.json"))["words"]
old_by_pair = {(norm(w["tr"]), w["fr"]): w["id"] for w in old}
old_by_tr = {}
for w in old:
    old_by_tr.setdefault(norm(w["tr"]), []).append(w["id"])

NIVEAU_1 = NIVEAU_1 + [("Compléments", [
 ("le mari", "ganḍa", "ಗಂಡ", None),
 ("l'épouse", "hendati", "ಹೆಂಡತಿ", None),
 ("je pense que… (« il me semble »)", "nanage anisutte…", "ನನಗೆ ಅನಿಸುತ್ತೆ…", None),
 ("je ne pense pas", "nanage hāge anisalla", "ನನಗೆ ಹಾಗೆ ಅನಿಸಲ್ಲ", None),
 ("comme ça / ainsi", "hāge", "ಹಾಗೆ", None),
 ("comme ceci", "hīge", "ಹೀಗೆ", None),
 ("sucré", "sihi", "ಸಿಹಿ", None),
 ("écoutez", "kēḷi", "ಕೇಳಿ", None),
 ("mal à la tête", "tale nōvu", "ತಲೆ ನೋವು", None),
])]
units = {t: items for t, items in NIVEAU_1}
assert set(SUITE) == set(units), set(units) ^ set(SUITE)

seen = set()
words = []


def add(cat, item):
    fr, tr, kn, note = item
    key = norm(tr)
    if key in seen:
        return
    seen.add(key)
    w = {"id": make_id(tr, fr), "cat": cat, "fr": fr, "tr": tr, "kn": kn}
    if note:
        w["note"] = note
    aka = []
    if (key, fr) in old_by_pair:
        aka.append(old_by_pair[(key, fr)])
    elif len(old_by_tr.get(key, [])) == 1:
        aka.extend(old_by_tr[key])
    if aka:
        w["aka"] = aka
    words.append(w)


for title, items in DEBUT:
    for it in items:
        add(f"Niveau 1 · {title}", it)

# les unités dont il ne reste que quelques expressions sont regroupées
pending, titles = [], []


def flush():
    global pending, titles
    if not pending:
        return
    label = " · ".join(titles[:2]) + (" …" if len(titles) > 2 else "")
    for it in pending:
        add(f"Niveau 1 · {label}", it)
    pending, titles = [], []


for title in SUITE:
    items = sorted(units[title], key=lambda it: nwords(it[1]))  # tri stable
    fresh = [it for it in items if norm(it[1]) not in seen
             and norm(it[1]) not in {norm(p[1]) for p in pending}]
    if not fresh:
        continue
    pending += fresh
    titles.append(title)
    if len(pending) >= 8:
        flush()
flush()

# progressivité du premier mois : longueur maximale selon la position
LIMITS = [(70, 1), (140, 2), (210, 3), (290, 4), (310, 6)]
for i, w in enumerate(words[:310]):
    lim = next(m for p, m in LIMITS if i < p)
    assert nwords(w["tr"]) <= lim, (i, w["tr"], lim)

ids = [w["id"] for w in words]
assert len(ids) == len(set(ids)), "identifiants en double"
json.dump({"version": 6, "updated": "2026-10-13", "words": words},
          open("words.json", "w"), ensure_ascii=False, indent=1)
print(len(words), "expressions ;", sum(1 for w in words if "aka" in w), "reliées à l'ancienne liste")
