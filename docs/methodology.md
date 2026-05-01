# 🔬 Méthodologie

## 1. Exploration (EDA)

- Vérification des dimensions, types et valeurs manquantes (aucune)
- Statistiques descriptives sur les variables numériques (`Price_USD`, `Units_Sold`, `Revenue_USD`)
- Inventaire des modalités catégorielles
- Vérification de la **cohérence Revenue = Price × Units** (écart < 0.01, OK)

## 2. Nettoyage et feature engineering

Pipeline implémenté dans `src/preprocessing.py` :

1. **Dédoublonnage** par `Sale_ID`
2. **Conversion de `Date`** en datetime
3. **Features temporelles** : Year, Month, Quarter, YearMonth, DayOfWeek, WeekOfYear
4. **Saison** dérivée du mois (hémisphère nord)
5. **Buckets de prix** : Budget (<$75) / Mid-range ($75-150) / Premium (>$150)
6. **Buckets de revenus** : Small / Medium / Large / XLarge
7. **Vérification de cohérence** : `Revenue_Check_Diff` doit être proche de 0

## 3. Construction des datamarts

8 datamarts implémentés dans `src/datamarts.py`. Chaque datamart :
- répond à **une question business précise**
- est directement exploitable dans Looker Studio sans jointure
- inclut systématiquement un compte (`sales`) pour pouvoir pondérer

## 4. Visualisations

**Choix design :**
- **Couleurs des marques** = couleurs officielles (Nike orange, Adidas noir, Reebok rouge…)
- **Couleurs des canaux** = palette distinctive
- **Annotations directes** sur chaque barre (valeurs + %)
- Format des montants : `$Xk` ou `$X,XXX` selon la magnitude
- DPI=140 pour rendu propre sur GitHub

**Outils :**
- Matplotlib + Seaborn pour les figures statiques (intégration README)
- Looker Studio pour le dashboard interactif final

## 5. Export pour Looker Studio

Deux options :

**Option A — Upload CSV direct** : les fichiers de `data/exports/` sont uploadés un par un. Rapide mais demande une mise à jour manuelle.

**Option B — BigQuery** : charger via `sql/create_tables.sql` (avec partition par date pour optimiser les coûts), brancher Looker en mode live. Préférable en prod.

## 6. Limitations

- **1 année de données seulement** (2025) → pas de comparaison year-over-year possible
- **Dataset synthétique probable** : les revenus sont parfaitement cohérents avec Price × Units, ce qui est rare en vraies données (où on a des promotions, frais de port, taxes…)
- **Pas d'identifiant client** → impossible de calculer la LTV ou le taux de réachat
- **Pas de dimension produit fine** (taille, modèle exact) → analyse limitée à la combinaison marque × type × couleur
- **Pas de coût d'acquisition** → impossible de calculer la marge ou le ROI marketing

## 7. Pistes d'amélioration

- **Forecasting** : modèle ARIMA ou Prophet sur la saisonnalité pour prévoir 2026
- **Segmentation client** si on récupère des `customer_id`
- **Analyse de panier** : quels types de chaussures se vendent ensemble ?
- **A/B test** entre canaux : Online performe-t-il vraiment mieux que Retail ?
- **Pricing optimization** : quel est le prix optimal par segment ?