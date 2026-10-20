# Cahier des charges — niveaux 2, 3, 4 du cours de kannada

Public : une Française qui apprend le **kannada parlé de Bangalore** pour parler
avec les parents de son partenaire (registre respectueux, `nīvu` / `-i`) et avec
son partenaire (`nīnu`). Elle ne lit pas l'écriture kannada : la translittération
est ce qu'elle voit ; l'écriture sert à la synthèse vocale et doit être exacte.

## Format du fichier (Python)

```python
NIVEAU_2 = [
("Titre de l'unité", [
 ("français", "translittération", "ಕನ್ನಡ", "note facultative ou None"),
 ...
]),
...
]
```

- Une unité = un thème + un point de grammaire, **10 à 12 entrées**.
- Le **premier item** d'une unité à point de grammaire explique la règle dans sa
  note (une phrase simple, en français).
- Progression **dans** l'unité : du plus court au plus long.
- Progression **entre** unités : grammaire introduite une fois, puis réutilisée.
- Le français est naturel et bref ; le sens littéral va dans la note quand il
  aide (« à moi la faim arrive »).
- Pas d'anglais dans le kannada sauf mots sans équivalent courant (bus, phone,
  ticket, PhD…) ; dans ce cas, kannada dans l'écriture (ಬಸ್).
- Pas de doublon avec le niveau 1 (liste des translittérations déjà prises dans
  `n1_tr.txt`) ni entre unités.

## Translittération (identique au niveau 1)

Voyelles longues avec macron : ā ī ū ē ō. Rétroflexes : ṭ ḍ ṇ ḷ ṣ. Palatales :
ch, j, sh (ಶ), ñ. Aspirées : kh gh chh jh ṭh ḍh th dh ph bh. Anusvara devant
p/b/m → m, sinon n. `v` pour ವ. Pas de `w`, pas de `z`.

Kannada **parlé** : formes contractées de Bangalore (`bartīni`, `māḍtā iddīni`,
`hōgbēku`, `gottilla`, `āytu`), pas les formes littéraires (`baruttēne`).
L'écriture kannada doit refléter exactement la forme parlée translittérée
(ex. ಬರ್ತೀನಿ pour `bartīni`), car un script vérifie la correspondance :

    python3 check_kn.py data_n2.py    # doit afficher « 0 écarts »

Lance-le et corrige jusqu'à 0 écart avant de rendre le fichier.

## Niveau 2 (A2) — ~45 unités, ~500 entrées — `data_n2.py`

Grammaire à couvrir, dans cet ordre : passé pour toutes les personnes (-de, -di,
-dri, -da, -ḷu, -ru, -vi, -tu) · progressif « en train de » (-tā iddīni) ·
futur/intention (-tīni déjà vu → « je vais » + hōgtā iddīni) · négation au
passé (-illa : barlilla) · « il y avait » (ittu / iralilla) · « pouvoir »
(-bahudu, āgutte/āgalla, nanage … barutte) · « il faut / devoir » (-bēku, -bāradu
= il ne faut pas) · conditionnel « si » (-dre) · « quand » (-dāga) · « avant /
après » (-mod(a)lu, -mēle) · comparaison (-ginta, tumbā, svalpa) · superlatif
(ellakkinta) · objet direct (-annu / -na) · instrumental « avec, par » (-inda) ·
« pour » (-ge, -gōskara) · « chez » (hatra) · pluriels (-galu, -ru) · quantité et
fréquence · démonstratifs ī / ā (ce… -ci / ce… -là) · adjectifs de ce qui est à
moi (nannadu) · « vouloir faire » (-bēku anta ide) · « aimer faire » (-ōdu ishṭa).

Thèmes A2 : raconter sa journée et son week-end · projets et rendez-vous ·
la cuisine (recettes, ustensiles, goûts, « comment on fait ») · courses et
marché · santé et pharmacie · transports et directions détaillées · maison et
tâches ménagères · vêtements et achats · fêtes (Dīpāvaḷi, Ugādi, mariage) ·
météo et saisons · corps et sport · téléphone et messages · se plaindre
poliment, s'excuser, remercier · opinions simples (j'aime, je préfère, je pense) ·
nombres : heures précises, prix, dates, âges · le temps qui passe (depuis,
pendant, il y a).

## Niveau 3 (B1) — ~50 unités, ~600 entrées — `data_n3.py`

Grammaire : propositions relatives (verbe en -ō / -ida + nom : « le livre que
j'ai lu ») · discours rapporté (anta : « il a dit que… ») · cause et but
(-dakke, yākandre, -ōdakke) · concession (-drū : « même si ») · « pendant que »
(-tā) · « avant que / après que » avec verbe · habitude passée (-tā idde) ·
plus-que-parfait (-idde) · obligation et permission (-bēkāgutte, -bahudu, -bāradu)
· souhait et regret (-bēkittu : « j'aurais dû ») · passif rare, impersonnel (ide,
āgutte) · verbes composés (māḍkoḷḷu, hōgbiḍu, kuḍidbiḍu : nuances d'achèvement) ·
réfléchi -koḷḷu · gérondif -tā · participes adverbiaux (-i : « après avoir… ») ·
interrogatives indirectes (ēnu anta gottilla) · « soit… soit », « ni… ni » ·
quantifieurs (ellā, kelavu, yāvdū, ēnādru) · degrés (innū, tumbānē, svalpanē,
-ē emphatique) · politesse avancée (-ri, dayaviṭṭu + -bahudā?).

Thèmes B1 : raconter une histoire ou un souvenir · décrire une personne
(caractère, apparence) · le travail et les études en détail (recherche,
enseignement, réunion, thèse) · la santé et les émotions nuancées · la
famille élargie et les traditions · l'Inde et la France : comparer, expliquer
sa culture · actualités simples, environnement · donner son avis et nuancer ·
résoudre un problème (réclamation, rendez-vous raté) · humour et petites
expressions idiomatiques de Bangalore · proverbes très courants.

## Niveau 4 (B2) — ~40 unités, ~500 entrées — `data_n4.py`

Grammaire : hypothèses irréelles (-iddre … -tidde) · conditionnel négatif
(-dillāndre) · nominalisations (-uvudu, -ike, -ṇa) · voix causative (-isu :
māḍisu, kalisu) · formes honorifiques et formes très familières · discours
indirect complexe · connecteurs de texte (ādarindā, hāgāgi, allade, matte,
koneyadāgi) · registre écrit vs parlé (quelques formes littéraires à
reconnaître : baruttēne, iddēne, māḍuttāre) · expressions figées avec « dire /
faire / mettre » (hēḷu, māḍu, hāku) · sandhi courants à l'oral.

Thèmes B2 : débattre et argumenter · exprimer des sentiments complexes ·
l'ironie, l'humour, taquiner gentiment · administration, banque, logement ·
cinéma kannada et chansons (vocabulaire pour en parler) · histoire et culture du
Karnataka (quelques mots) · psychologie et science vulgarisées (son domaine) ·
cuisine avancée et vocabulaire d'une recette complète · relations : amitié,
couple, belle-famille, conflits et réconciliation · idiomes et proverbes
courants (15–20) avec sens littéral en note.
