# 📖 Data Dictionary

## Dataset principal : `shoes_sales.csv`

**1 000 lignes × 10 colonnes** — un record = une transaction.

### Colonnes originales

| Variable | Type | Domaine | Description |
|----------|------|---------|-------------|
| `Sale_ID` | string | S1, S2, … | Identifiant unique de la transaction |
| `Date` | date | 2025-01-03 → 2025-12-31 | Date de la vente |
| `Brand` | string | 6 modalités | Adidas, New Balance, Nike, Puma, Reebok, Skechers |
| `Shoe_Type` | string | 6 modalités | Boots, Casual, Formal, Running, Sneakers, Sports |
| `Color` | string | 6 modalités | Black, Blue, Green, Grey, Red, White |
| `Country` | string | 7 modalités | France, Germany, India, Saudi Arabia, UAE, UK, USA |
| `Sales_Channel` | string | 3 modalités | Online, Mall, Retail Store |
| `Price_USD` | float | 31 → 250 | Prix unitaire en USD |
| `Units_Sold` | int | 1 → 20 | Quantité vendue dans la transaction |
| `Revenue_USD` | float | calculé | `Price_USD × Units_Sold` (vérifié dans le pipeline) |

---

## Variables dérivées (générées par `src/preprocessing.py`)

### Features temporelles

| Variable | Calcul | Description |
|----------|--------|-------------|
| `Year` | `Date.dt.year` | Année (toutes 2025 ici) |
| `Month` | `Date.dt.month` | Mois (1-12) |
| `MonthName` | `Date.dt.strftime("%b")` | Jan, Feb, Mar… |
| `YearMonth` | `Date.dt.strftime("%Y-%m")` | Pour les agrégations mensuelles (2025-01) |
| `Quarter` | `Date.dt.to_period("Q")` | Q1-Q4 |
| `DayOfWeek` | `Date.dt.day_name()` | Monday, Tuesday… |
| `WeekOfYear` | `Date.dt.isocalendar().week` | 1-52 |
| `Season` | mapping mois → saison | Winter (Dec-Fév) / Spring / Summer / Autumn |

### Features business

| Variable | Bins | Description |
|----------|------|-------------|
| `Price_Bucket` | <75, 75-150, >150 | Budget / Mid-range / Premium |
| `Revenue_Bucket` | <500, 500-1500, 1500-3000, >3000 | Small / Medium / Large / XLarge |

### Contrôle qualité

| Variable | Description |
|----------|-------------|
| `Revenue_Check_Diff` | `Revenue_USD - (Price_USD × Units_Sold)`. Devrait être proche de 0 (juste arrondis flottants). |

---

## Notes méthodologiques

- **Valeurs manquantes** : aucune
- **Doublons** : aucun (`Sale_ID` est unique)
- **Cohérence Revenue** : vérifiée — l'écart max est < 0.01 (pure imprécision flottante)
- **Distribution prix** : équilibrée — moyenne $138, médiane $139
- **Couverture temporelle** : année 2025 complète, ~83 ventes par mois en moyenne

## Encodage des catégories pour Looker / SQL

Si tu charges en BigQuery, pas besoin d'encoder, les `STRING` natives suffisent. Pour du ML par contre, prévoir un `LabelEncoder` ou `OneHotEncoder` sur :
- `Brand`, `Shoe_Type`, `Color`, `Country`, `Sales_Channel` (catégorielles nominales)
- `Price_Bucket`, `Season` (catégorielles ordinales)