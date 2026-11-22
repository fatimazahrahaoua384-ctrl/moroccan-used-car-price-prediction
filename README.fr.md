[🇬🇧 English](README.md) | 🇫🇷 Français 
# Moroccan Used Car Price Prediction

Projet de machine learning de bout en bout : prédire le prix d'une voiture d'occasion au Maroc, de la collecte des données jusqu'à une application déployée.

## 1. Problème

Au Maroc, il est difficile de savoir si le prix d'une voiture d'occasion est juste. Les acheteurs risquent de payer trop cher, et les vendeurs de fixer un prix mal adapté au marché. Ce projet s'adresse aux **deux** : l'acheteur qui veut vérifier une annonce, et le vendeur qui veut estimer le prix de sa voiture.

## 2. Objectif

Une application web où l'utilisateur saisit les caractéristiques d'une voiture et obtient une estimation de son prix en dirhams, grâce à un modèle entraîné sur des annonces réelles du marché marocain.

## 3. Variable à prédire

Le **prix de vente** de la voiture, en dirhams marocains (MAD).

## 4. Variables d'entrée espérées

- Marque et modèle
- Année de mise en circulation
- Kilométrage
- Type de carburant (essence, diesel, hybride…)
- Boîte de vitesses (manuelle, automatique)
- Puissance fiscale (CV)
- Ville
- Nombre de portes (si disponible)

## 5. Métrique de succès (hypothèse initiale)

Je mesurerai la **MAE** (erreur absolue moyenne), car elle est facile à interpréter : en moyenne, le modèle se trompe de X dirhams.
Objectif initial : **MAE inférieure à 10 % du prix médian** des voitures du jeu de données. Cet objectif sera révisé après l'analyse exploratoire.
Le modèle devra aussi battre une baseline simple (régression linéaire).

## 6. Hors périmètre (version 1)

- Les autres véhicules (motos, utilitaires, camions)
- L'analyse des photos des annonces
- La prédiction des prix de voitures neuves

## Stack prévue

Python, pandas, scikit-learn, XGBoost, FastAPI, Next.js, Docker.

## Données

Jeu de données : **Moroccan Used Cars Dataset (MUCars-2024)**, version 2.
Auteurs : Tabarnoust, E., Mghari, M., Zaz, Y. (2024). Mendeley Data. DOI : [10.17632/vjrbcb2rrt.2](https://doi.org/10.17632/vjrbcb2rrt.2)
Licence : CC BY 4.0.

Le fichier brut n'est pas inclus dans ce dépôt. Télécharge `cars_dataframe.csv` depuis le lien ci-dessus et place-le dans `data/raw/`. 
## Statut

En cours de développement.  
