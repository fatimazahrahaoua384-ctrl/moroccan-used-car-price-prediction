# Research notes

## A. Dataset: MUCars-2024
- Source: https://doi.org/10.17632/vjrbcb2rrt.2
- License: CC BY 4.0
- File: cars_dataframe.csv (21.8 MB)
- Rows / columns: (à compléter)
- Collection method: (à compléter)

## B. First look at the data 

Notebook: `notebooks/01_first_look.ipynb` (2026-11-22)

**Overview:** 101,896 rows × 15 columns, one CSV file (21.8 MB). No listing date column.

### Missing values
| Column | % missing |
|---|---|
| Price (target) | 25.0 |
| First Owner | 14.4 |
| Origin | 11.8 |
| Number of Doors | 11.2 |
| Condition | 3.5 |
| Fiscal Power | 0.3 |
| Sector | 0.2 |
| All others | 0.0 |

### Issues found
1. **Target missing for 25% of rows** (25,483 listings). They cannot be used to train a supervised model. Plan: remove them from training, never impute the target.
2. **Price has extreme values.** min = 1, median = 110,000, mean ≈ 498,000, max = 1.6 billion. The mean is driven by outliers, so the median is the reliable reference. Values like 1 or 1.6e9 look like errors or placeholders (hypothesis, to check).
3. **2,805 fully duplicated rows (~2.8%).** Unclear whether they are real duplicate listings or different cars with identical features (mileage is binned and there is no listing ID). To investigate before deciding.
4. **Mileage is text, in ranges of unequal width** (5,000, 10,000 and 50,000 km). The most frequent range is "200 000 - 249 999" (10,075 rows). Hypothesis: this may be a catch-all choice. To check.
5. **Year is text and contains "1980 ou plus ancien"** (307 rows), which is a category, not a number.
6. **Fiscal Power is text** (e.g. "8 CV"): the number must be extracted.
7. **Equipment is a list stored as a string**: needs parsing.
8. **Brand:** the top 24 brands look clean, but a lowercase "mini" appeared in `head()`: possible spelling variants to normalize.

### Open questions
- What is the unit of Price? The median (110,000) is consistent with MAD, but I must confirm it in the dataset description.
- Which price outliers are errors, and which are legitimate luxury cars?
- Does a missing value (First Owner, Origin) carry information?

### Next steps
- Study the price distribution (quantiles, lowest and highest values).
- Decide how to handle duplicates.
- Parse Mileage, Year, Fiscal Power and Equipment.
- Split train/test before any statistical preprocessing. 
### Update after price checks
- Brands: 81 unique values, no case variants.
- Years: last values are 2015-2024, consistent with a 2024 collection.
- Price quantiles: 1% = 10,500; 5% = 27,000; 25% = 60,000; 50% = 110,000; 75% = 170,000; 95% = 370,000; 99% = 760,000. These magnitudes look plausible for MAD, but the unit is still to be confirmed.
- 126 prices are exactly 1, and others are 2, 3 or 4: placeholders, not real prices. 557 rows are below 5,000.
- 123 prices are above 5 million (85 above 10 million). Several have repeated digits (99,999,999; 55,555,555; 33,333,333), which suggests data entry errors.
- Plan: remove clearly invalid prices with a business rule before the split. Apply any statistical clipping after the split, on the training set only. 
### décisions sur les prix

- **Seuil minimum : 5 000 MAD.** Inspection de 30 lignes entre 1 000 et 5 000 MAD :
  surtout de vieilles voitures (avant 2005) à prix plausibles, quelques erreurs
  (Audi RS3 2024 à 2024 MAD, Clio 2021 à 1 600). Aucune valeur ronde dominante.
  2 lignes avec prix égal à l'année (déjà couvertes par le seuil).
- **Seuil maximum : 1 000 000 MAD.** Au-dessus de 5 M : erreurs évidentes (Polo 2001
  à 32 M, Kangoo 2008 à 1 milliard). Entre 1 et 5 M : du luxe plausible (Cayenne,
  RS6, Q8) mais aussi des erreurs sur marques économiques (Logan, Clio, Dokker,
  Fiat 500). 111 lignes de marques économiques dépassent 1 M.
- **Lignes concernées : 966 sur 76 413 avec prix (1,26 %).** Elles sont retirées
  avant le split : ce sont des règles métier, pas des statistiques apprises.
- **Hors périmètre du modèle :** voitures à moins de 5 000 MAD ou à plus de 1 M MAD.
- **Unité du prix :** non précisée dans la description officielle (Mendeley, v2).
  Hypothèse de travail : MAD, cohérente avec la médiane de 110 000. Le prix est un
  prix annoncé, pas un prix de vente final.

## C. Lecture critique : Morocco-Used-Car-Market-Analysis

**Ce que fait le projet :** [1 à 2 phrases : analyse exploratoire, modèle ou les deux ?]

**Traitement des données**
- Colonnes utilisées ou supprimées : [...]
- Prix aberrants : [seuils choisis ou rien ? justifiés ?]
- Valeurs manquantes : [supprimées ou imputées ? avant ou après un split ?]

**Points solides :** [par exemple clarté, graphiques, taille des données]

**Limites que j'ai remarquées :** [par exemple pas de split train/test, prix non
nettoyés, pas de modèle déployé, pas de métrique d'erreur en dirhams]

**Ce que je fais différemment :**
- Nettoyage par règles métier avant le split, statistiques apprises sur le train seulement
- Pipeline scikit-learn sauvegardé, puis API FastAPI et interface Next.js
- Métrique d'erreur en dirhams (MAE) sur un test final séparé

## D. Facteurs qui influencent le prix (hypothèses à vérifier dans l'EDA voir F.EDA )

| Facteur | Colonne | Effet attendu |
|---|---|---|
| Marque et modèle | Brand, Model | Les marques premium coûtent plus cher |
| Âge | Year | Plus la voiture est récente, plus elle coûte cher |
| Kilométrage | Mileage | Plus il est élevé, plus le prix baisse |
| Carburant | Fuel | Diesel et essence se valorisent différemment |
| Puissance fiscale | Fiscal Power | Plus élevée = plus de valeur ou plus de taxes |
| Boîte de vitesses | Gearbox | Automatique souvent plus chère |
| État | Condition | Meilleur état = prix plus élevé |
| Origine | Origin | Importée ou dédouanée : effet à tester |
| Première main | First Owner | Première main = prix plus élevé |
| Équipements | Equipment | Plus d'options = prix plus élevé |
| Localisation | Location, Sector | Écarts possibles entre villes |
| Nombre de portes | Number of Doors | Effet probablement faible |

**Variables à surveiller :** Origin, First Owner, Number of Doors et Condition ont
des valeurs manquantes (3 à 14 %), à imputer dans le pipeline après le split.  

## E. Nettoyage et baseline (24/11/2026)

**Nettoyage (notebook 02)**
- 101 896 lignes au départ ; 25 483 sans prix et 966 hors de 5 000 à 1 000 000 MAD
  retirées (règles métier) ; 1 692 doublons exacts supprimés ; reste 73 755 lignes.
- Séparation 80 / 20 avec `random_state=42` : train 59 004, test 14 751.
  Le test est mis de côté jusqu'à l'évaluation finale.

**Conversions (src/features.py)**
- `Mileage` : tranche texte vers milieu de tranche.
- `Year` : texte vers nombre ; « 1980 ou plus ancien » devient 1980
  (approximation : l'âge de ces voitures est sous-estimé).
- `Fiscal Power` : « 8 CV » vers 8.
- `Number of Doors` : déjà numérique (3.0 ou 5.0, 5 729 manquants).

**Baseline (notebook 03)**
- Pipeline scikit-learn : imputation + one-hot dans un `ColumnTransformer`.
- MAE en validation croisée à 5 plis sur le train :
  - dummy (médiane) : 74 979 MAD
  - régression linéaire : 44 905 MAD (plis entre 44 500 et 45 419)
- Interprétation : la baseline bat nettement le dummy mais reste imprécise.
  Elle sert de référence pour les modèles suivants.

**Limites connues**
- Unité du prix : hypothèse MAD (non précisée par les auteurs).
- Prix annoncé, pas prix de vente final.
- Doublons : pas d'identifiant d'annonce, donc des annonces réellement
  distinctes mais identiques ont pu être supprimées.
- `Equipment` pas encore exploité.

**Prochaines étapes :** EDA sur le train, `Equipment`, décision sur l'écrêtage
de la cible ou le log du prix, puis Random Forest et XGBoost. 
## F. EDA : session du 25/11/2026 (notebook 04_eda.ipynb, train.csv uniquement)

### Prix (cible)
- Train : 59 004 lignes. Médiane 109 000, moyenne 136 700. Percentiles : 1 % = 15 000, 5 % = 28 000, 25 % = 60 000, 75 % = 168 000, 95 % = 350 000, 99 % = 625 000, max = 1 000 000.
- Skew du prix = 2,57 ; skew de log(1 + prix) = -0,13. L'histogramme du log est une cloche presque symétrique.
- **Décision : entraîner sur le log du prix**, avec TransformedTargetRegressor (log1p / expm1) pour garder la MAE en MAD.
- **Décision : pas d'écrêtage de la cible pour l'instant.** La queue est progressive et les erreurs absurdes sont déjà retirées par les seuils 5 000 et 1 000 000. À reconsidérer après l'analyse des erreurs (calcul sur le train).

### Marques
- Les plus fréquentes : Renault (7 319), Volkswagen (7 069), Peugeot (5 483), Dacia (4 950), Mercedes-Benz (4 153).
- Médianes : de 58 000 (Fiat) à 280 000 (Land Rover). Audi 225 000, BMW 210 000, Kia 74 000, Peugeot 70 000.
- Limite : la médiane d'une marque mélange l'effet marque et l'effet âge. À recroiser avec l'âge avant de conclure sur une marque.

### Corrélations de Spearman avec le prix
- car_age : -0,79 (de loin la variable la plus forte).
- mileage_num : -0,16 (faible).
- fiscal_power_num : +0,17 ; Number of Doors : +0,07.
- Entre kilométrage et âge : seulement +0,31, alors qu'on attendait bien plus fort.

### Prix médian selon l'âge (âges avec au moins 30 annonces)
- Baisse régulière : 230 000 à 0 an, 195 000 à 2 ans, 100 000 à 12 ans, 55 000 à 20 ans, puis un plateau entre 22 000 et 40 000 de 27 à 42 ans.
- La courbe est convexe : forte décote les premières années, puis ralentissement. La relation prix/âge n'est donc pas une droite. C'est un argument de plus pour le log, et pour des modèles non linéaires (Random Forest, XGBoost).
- Remontée à 44 ans (50 000, 139 annonces) : cette tranche correspond à « 1980 ou plus ancien » converti en 1980 (REF_YEAR 2024 - 1980). Elle regroupe aussi des voitures de collection. Limite à noter.
- Petit pic à 29 ans (40 000) : probablement du bruit ou un effet de modèles précis, à ne pas sur-interpréter.

### Kilométrage
- Aucune valeur manquante après conversion (part de NaN = 0,0).
- Les tranches n'ont pas toutes la même largeur (« 0 - 4 999 », « 100 000 - 109 999 », « 200 000 - 249 999 »). Le milieu de tranche est donc plus ou moins précis selon la tranche.
- Tranches dominantes : 200 000 - 249 999 (6 523), 250 000 - 299 999 (3 340), 190 000 - 199 999 (2 893), 100 000 - 109 999 (2 616), 0 - 4 999 (2 549).
- Corrélations de Spearman avant correction : kilométrage/âge = +0,31 ; kilométrage/prix = -0,16. C'est faible, alors qu'on attendait bien plus fort.

**Constat (cellule 7) : la tranche « 0 - 4 999 » est suspecte**
- Elle compte 2 549 annonces, mais leur âge médian est de 16 ans (moyenne 16,6 ; 25 % ≤ 7 ans ; 75 % ≤ 25 ans ; max 44).
- Seules 210 annonces ont 0 an (environ 8 %), puis 99 à 1 an et 78 à 2 ans.
- De 4 à 14 ans, on trouve entre 41 et 79 annonces par âge, sans décroissance. Un vrai faible kilométrage devrait devenir de plus en plus rare avec l'âge.
- Conclusion : cette tranche mélange de vraies voitures neuves ou quasi neuves et beaucoup de valeurs par défaut (kilométrage non renseigné).
- Hypothèse (non vérifiée) : valeur par défaut du formulaire d'annonce. Elle expliquerait en partie la faible corrélation avec l'âge et le prix.

**Décision (à valider par le score)**
- Règle métier déterministe dans src/features.py : si Mileage = « 0 - 4 999 » et car_age >= 3, alors mileage_num = NaN (imputé ensuite par la médiane apprise sur le train) et mileage_suspect = 1.
- Seuil de 3 ans : les âges 0, 1, 2 (210, 99, 78 annonces) restent plausibles.
- Nombre de lignes concernées attendu : 2 549 - (210 + 99 + 78) = 2 162.
- Pas de fuite de données : la règle ne dépend que de la ligne elle-même.
**Vérification (25/11/2026)**
- Lignes suspectes obtenues : 2 162 (attendu 2 162, conforme).
- Corrélation de Spearman kilométrage/âge : +0,39 après correction (avant : +0,31).
- Corrélation de Spearman kilométrage/prix : -0,23 après correction (avant : -0,16).
- Corrélation âge/prix : -0,79, inchangée.
- Lecture : la règle améliore la cohérence du kilométrage, mais l'amélioration est modérée. Le kilométrage reste une variable faible (tranches larges, valeurs déclarées bruitées).
- MAE baseline (CV 5 plis) après correction : 44 882 MAD (avant : 44 905 MAD). Plis : 45 101, 45 421, 44 887, 44 474, 44 525.
- Verdict : gain de 23 MAD (0,05 %), dans le bruit entre plis (écart d'environ 950 MAD). Effet neutre sur la régression linéaire. Règle gardée car justifiée par les données et sans effet négatif ; à retester avec Random Forest et XGBoost, et à retirer si elle n'apporte rien là non plus. 
### Conséquences pour la suite
- Passer à la modélisation avec log du prix, car_age et Brand/Model comme variables centrales.
- Garder mileage_num, mais vérifier le pic 0 - 4 999 (cellule 7) avant de décider d'un traitement.
- Tester plus tard un indicateur « âge ≥ 44 » ou laisser les arbres gérer la cassure.
- Prochaines étapes de l'EDA : prix selon le kilométrage à âge fixé, marque × âge, colonne Equipment. 
### Prix selon le kilométrage à âge fixé (cellules 8 et 9, train, hors lignes suspectes)
- Âge 8, médiane par tranche (au moins 30 annonces, 34 à 264 par tranche) : 102 100 à 20 000 - 24 999 km, 162 500 à 80 000 - 84 999 km, puis 146 500 à 162 000 jusqu'à 250 000 km. Pas de baisse du prix quand le kilométrage monte.
- Corrélation de Spearman km/prix par âge : 3 ans -0,04 ; 4 : 0,08 ; 5 : 0,03 ; 6 : 0,02 ; 7 : 0,12 ; 8 : 0,10 ; 9 : 0,09 ; 10 : 0,08 ; 11 : 0,18 ; 12 : 0,20 ; 13 : 0,23 ; 14 : 0,23 ; 15 : 0,24.
- Constat : de 3 à 10 ans, le lien km/prix est proche de zéro ; à partir de 11 ans, il est positif (+0,18 à +0,24). La corrélation globale négative (-0,23) vient donc surtout de l'âge (variable de confusion).
- Carburant à 8 ans : Diesel 2 875 annonces, prix médian 155 000, km médian 144 999,5 ; Petrol 229, 93 000 et 104 999,5 ; Hybrid 8 et Electrique 3 (trop rares). Le diesel est plus cher et plus roulé : effet de composition.
- Corrélation km/prix à l'intérieur du carburant (âge 8) : Diesel +0,06 (2 875 lignes), Petrol -0,13 (229 lignes), contre +0,10 tous carburants confondus.
- Conclusion : le carburant explique une partie de l'effet positif, mais pas tout. Le reste (marque, modèle, kilométrage déclaré peu fiable) n'est pas vérifié.
- Décision : garder mileage_num et mileage_suspect ; ne pas tirer de conclusion sur le kilométrage avec la régression linéaire, qui ne capte pas les interactions ; tester avec Random Forest et XGBoost. Idée à tester à l'étape features : kilométrage par an (mileage_num / car_age). 
### Variables catégorielles (cellule 10, train)
- Fuel (aucun NaN) : Diesel 46 952, médiane 120 000 ; Petrol 11 362, 55 000 ; Hybrid 489, 250 000 ; Electrique 157, 223 600 ; LPG 44, 88 500. Diesel et Petrol = 98 % des lignes ; les trois autres sont rares.
- Gearbox (aucun NaN) : Automatic 17 449, médiane 210 000 ; Manual 41 555, 82 000.
- Condition : New 2 012, 160 000 ; Excellent 24 919, 140 000 ; Very Good 20 962, 96 000 ; Good 8 042, 55 000 ; Fair 1 251, 37 000 ; Damaged 54, 31 000 ; For Parts 38, 28 500 ; NaN 1 726 (2,9 %), 79 000. Médianes monotones : variable ordinale.
- Limite : ces médianes mélangent l'effet de la variable avec celui de l'âge et de la marque (ex. diesel/essence : rapport 2,2 au global, 1,7 à 8 ans). Elles montrent qu'une variable est informative, pas qu'elle explique le prix.
- Cardinalité : Model 916, Location 360, Sector 805 valeurs distinctes (environ 2 080 colonnes en one-hot).
- Origin : WW in Morocco 38 648, médiane 117 000 ; Customs-cleared car 10 705, 78 000 ; NaN 6 620 (11,2 %), 76 000 ; Imported New 2 605, 155 000 ; Car not yet customs-cleared 426, 134 000.
- First Owner : No 33 480, 85 000 ; Yes 18 230, 155 000 ; NaN 7 294, 95 000.
- Constat : les NaN de Origin (76 000) ressemblent à « Customs-cleared » (78 000) et non à la valeur la plus fréquente (117 000) ; imputer par most_frequent les classe donc dans la mauvaise catégorie. Même logique que Condition.
- Décision : pour Condition, Origin et First Owner, traiter les NaN comme une catégorie « Inconnu » (SimpleImputer(strategy="constant", fill_value="Inconnu")). Hypothèse à valider par la MAE, comparée à la baseline 44 882.
- Cardinalité (cellule 11, train) : Model 916 valeurs, dont 632 avec moins de 30 annonces (7,5 % des lignes) ; les 50 plus fréquentes couvrent 52,1 %. Location 360 valeurs, 270 rares (2,2 % des lignes) ; top 50 = 93,7 %. Sector 805 valeurs, 552 rares (7,9 % des lignes) ; top 50 = 66,4 %.
- Lecture : les valeurs rares représentent environ 69 à 75 % des colonnes mais seulement 2 à 8 % des lignes. Les regrouper supprime environ 1 450 colonnes de one-hot pour un faible coût.
- Décision : OneHotEncoder(handle_unknown="ignore", min_frequency=30) pour Model, Location et Sector. Seuil de 30 à ajuster selon la MAE. Règle apprise sur le train, donc sans fuite.
- Décisions : garder Fuel et Gearbox ; garder Condition en traitant les NaN comme catégorie « Inconnu » (hypothèse : leur médiane 79 000 est loin de la valeur la plus fréquente, Excellent à 140 000 ; à valider par la MAE) ; tester aussi un encodage ordinal pour les arbres. Pour Model, Location et Sector : décider après mesure des valeurs rares ; piste OneHotEncoder(min_frequency=30), à tester à l'étape modèles. 
### Test « Inconnu » et regroupement des rares (baseline, notebook 03, 25/11/2026)
- Référence (NaN imputés par most_frequent, sans regroupement) : MAE CV 44 882 MAD.
- Test A (NaN de Condition, Origin, First Owner, etc. = catégorie « Inconnu », sans regroupement) : 45 014 MAD. Plis : 45 142, 45 477, 45 132, 44 611, 44 706. Durée 17,1 s.
- Test B (« Inconnu » + OneHotEncoder min_frequency=30 sur Brand, Model, Location, Sector) : 45 005 MAD. Plis : 45 114, 45 463, 45 124, 44 612, 44 715. Durée 2,9 s.
- Lecture : écart de +130 MAD (environ 0,3 %) avec la référence, dans le bruit entre plis (environ 950 MAD d'écart). Effet neutre de « Inconnu » sur la régression linéaire.
- Le regroupement des rares ne change pas le score (A contre B : 9 MAD) mais divise le temps de calcul par environ 6 (environ 1 450 colonnes en moins).
- Hypothèse écartée : « les NaN de Origin/Condition ressemblent à une autre catégorie » reposait sur des médianes qui mélangent l'âge et la marque ; le test ne la confirme pas.
- Décision : garder min_frequency=30 (même score, plus rapide). Garder « Inconnu » provisoirement (un NaN n'est pas une valeur réelle) ; à retester avec Random Forest et XGBoost, et retirer s'il n'apporte rien.  
### Equipment (cellule 12, train)
- Format : texte qui ressemble à une liste Python (ex. "['ABS', 'Airbags']"), à convertir avec ast.literal_eval. Doublons possibles dans une même annonce (ex. 'Electric Windows' répété) : dédoublonner avec set().
- 8 208 combinaisons distinctes, mais seulement 16 équipements distincts. Aucun NaN, aucun texte illisible, aucune liste vide (min = 1).
- Part des annonces ayant l'équipement : Electric Windows 60,6 % ; CD/MP3/Bluetooth 56,1 % ; Alloy Wheels 53,3 % ; Air Conditioning 47,2 % ; Airbags 43,8 % ; Central Locking 43,8 % ; Rear Camera 39,7 % ; ABS 39,5 % ; Leather Seats 33,9 % ; Speed Limiter 33,9 % ; Cruise Control 33,7 % ; Parking Sensors 32,4 % ; Onboard Computer 31,1 % ; ESP 29,8 % ; Navigation System/GPS 26,2 % ; Sunroof 11,3 %.
- n_equipment (nombre d'équipements distincts) : moyenne 6,2 ; écart-type 4,9 ; min 1 ; 25 % = 2 ; max 15.
- Spearman n_equipment/prix = +0,42 ; n_equipment/âge = -0,33. Plus fort que le kilométrage (-0,23) et la puissance fiscale (+0,17), derrière l'âge (-0,79).
- Limite : le +0,42 mélange l'effet de l'équipement avec celui de la marque et de l'âge. Piste prometteuse, non démontrée.
- Décision : créer n_equipment et 16 indicateurs eq_<nom> dans src/features.py (vocabulaire fixe de 16 noms). Les tester séparément en régression linéaire (n_equipment = somme des indicateurs : multicolinéarité exacte). Comparer à 45 005 MAD (test B). Avec Random Forest et XGBoost, on pourra garder les deux.
- Résultats MAE (CV 5 plis, notebook 03, référence test B = 45 005 MAD) :
  - Test C (n_equipment) : 44 971 MAD, plis 45 125, 45 388, 45 083, 44 595, 44 667. Gain de 34 MAD (0,08 %) : négligeable.
  - Test D (16 indicateurs eq_*) : 44 634 MAD, plis 44 747, 45 043, 44 708, 44 242, 44 433. Gain de 371 MAD (0,8 %), meilleur que B sur les 5 plis (de 282 à 420 MAD).
- Lecture : les 16 indicateurs apportent un gain modeste mais régulier ; n_equipment seul n'apporte rien en régression linéaire. Hypothèse (non vérifiée) : les indicateurs laissent le modèle pondérer chaque équipement séparément.
- Remarque méthodologique : les plis sont identiques d'un test à l'autre (KFold sans mélange), donc la comparaison pli par pli est plus informative que celle des moyennes.
- Décision : garder les 16 indicateurs pour la baseline linéaire. n_equipment reste dans features.py ; à retester avec Random Forest et XGBoost (les deux ensemble sont possibles avec des arbres).  
### Marque × âge (cellule 13, train, 10 marques les plus fréquentes, groupes d'au moins 30 annonces)
- Âge 3, médiane (annonces) : Fiat 124 500 (146) ; Dacia 132 000 (399) ; Citroen 147 000 (161) ; Renault 153 000 (438) ; Peugeot 169 000 (244) ; Ford 222 500 (98) ; Hyundai 235 000 (236) ; Volkswagen 354 000 (281) ; Audi 424 500 (128) ; Mercedes-Benz 470 000 (91).
- Âge 8 (sortie partielle), médiane (annonces) : Fiat 85 000 (134) ; Dacia 99 000 (281) ; Citroen 105 000 (86) ; Peugeot 109 000 (178) ; Renault 115 000 (274) ; Ford 144 000 (304) ; Hyundai 145 000 (163) ; Volkswagen 173 000 (443). Audi et Mercedes-Benz à 8 ans non visibles (sortie tronquée). Âge 12 : sortie tronquée, seules Volkswagen 125 000 (312), Audi 150 000 et Mercedes-Benz 155 000 sont visibles.
- Constat : l'effet marque persiste à âge fixé. Groupe économique (Fiat, Dacia, Citroen, Renault, Peugeot) contre groupe premium (Volkswagen, Audi, Mercedes-Benz) ; à 3 ans, Mercedes-Benz vaut environ 3,8 fois Fiat.
- Dacia (médiane globale 110 000) est bien dans le groupe économique à âge fixé : l'écart global venait de l'âge du parc. Kia : non vérifiée (hors top 10).
- Lecture pour le modèle : l'effet marque est multiplicatif, ce qui renforce le choix du log du prix ; les interactions marque × âge sont à confier aux arbres (Random Forest, XGBoost). 