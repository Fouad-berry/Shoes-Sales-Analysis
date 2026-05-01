# 📊 Guide Looker Studio

## 🔗 Lien du dashboard

> **[👉 Ouvrir le dashboard](https://lookerstudio.google.com/)** *(à remplacer par ton lien publié)*

---

## 🚀 Connexion des données

### Option A — Upload CSV (rapide, recommandé)

1. [lookerstudio.google.com](https://lookerstudio.google.com/) → **Créer** → **Source de données** → **File Upload**
2. Uploader depuis `data/exports/` :
   - `main_dataset.csv` (1 000 transactions, source principale)
   - `by_brand.csv`
   - `by_country.csv`
   - `by_channel.csv`
   - `by_shoe_type.csv`
   - `monthly_trend.csv`
   - `global_kpis.csv`
3. Pour chaque source : **Créer un rapport**

### Option B — BigQuery (option pro)

1. Exécuter `sql/create_tables.sql` dans BigQuery
2. Charger les CSV via l'UI BigQuery ou `bq load`
3. Dans Looker : **Ajouter une source** → **BigQuery** → choisir la table

---

## 🎨 Structure recommandée — 5 pages

### 📄 Page 1 — Executive Overview

Source : `global_kpis.csv` + `main_dataset.csv`

- **6 scorecards** : total_sales, total_revenue, total_units, avg_order_value, avg_price, unique_brands
- **Line chart** : évolution mensuelle des revenus
- **Donut** : répartition par canal de vente
- **Bar chart horizontal** : top marques

### 📄 Page 2 — Brands

Source : `by_brand.csv` + `main_dataset.csv`

- **Bar chart horizontal** : revenus par marque (avec couleurs officielles)
- **Pie chart** : market share
- **Box plot** : distribution des prix par marque
- **Table** : tous les KPIs comparatifs

### 📄 Page 3 — Geography

Source : `by_country.csv` + `main_dataset.csv`

- **Geo map** : revenus par pays (utiliser la carte mondiale Looker)
- **Bar chart horizontal** : top 7 pays
- **Heatmap** : marque × pays (revenus)
- **Table** : tous les KPIs par pays

### 📄 Page 4 — Channels

Source : `by_channel.csv` + `main_dataset.csv`

- **Donut** : Online vs Mall vs Retail Store
- **Bar chart** : panier moyen (AOV) par canal
- **Stacked bar** : répartition canal × marque
- **Filtres** : pays, type de chaussure

### 📄 Page 5 — Products

Source : `by_shoe_type.csv` + `dm_color_type_matrix.csv`

- **Bar chart** : revenus par type de chaussure
- **Heatmap** : couleur × type (mix produit)
- **Bar chart** : prix moyen par type
- **Top 10 transactions** : table filtrable

---

## 🎛️ Filtres globaux (haut de page)

- `Brand` (dropdown multiple)
- `Country` (dropdown)
- `Sales_Channel` (boutons : Online / Mall / Retail Store)
- `Shoe_Type` (dropdown)
- `Date` (range picker)
- `Season` (boutons)

---

## 🎨 Palette des couleurs

Pour cohérence avec les figures Python, utilise dans Looker :

**Marques :**
- Nike : `#FA5400` (orange)
- Adidas : `#000000` (noir)
- Puma : `#0066B3` (bleu)
- Reebok : `#D81E05` (rouge)
- Skechers : `#1B3D6E` (bleu marine)
- New Balance : `#CE0E2D` (rouge brique)

**Canaux :**
- Online : `#3498db` (bleu)
- Mall : `#9b59b6` (violet)
- Retail Store : `#e67e22` (orange foncé)

---

## 💡 Champs calculés utiles

Dans Looker, tu peux ajouter :

- `Margin_per_Unit = Revenue_USD / Units_Sold` (= Price_USD vérification)
- `Is_Premium = IF(Price_USD > 150, "Premium", "Mass-market")`
- `Quarter_label = CONCAT("Q", QUARTER(Date))`

---

## 📸 Captures d'écran

Place tes captures dans `images/` et référence-les ici :

```markdown
![Page 1 — Overview](../images/dashboard_01_overview.png)
![Page 2 — Brands](../images/dashboard_02_brands.png)
![Page 3 — Geography](../images/dashboard_03_geography.png)
![Page 4 — Channels](../images/dashboard_04_channels.png)
![Page 5 — Products](../images/dashboard_05_products.png)
```