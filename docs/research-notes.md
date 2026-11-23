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

## D. Facteurs qui influencent le prix (hypothèses à vérifier dans l'EDA)

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