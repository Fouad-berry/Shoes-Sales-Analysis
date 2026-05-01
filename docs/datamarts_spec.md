# 🧱 Spécification des datamarts

## 1. `dm_global_kpis.csv`

**Grain** : 1 ligne · **Usage** : scorecards en haut du dashboard

| Colonne | Description |
|---------|-------------|
| `total_sales` | Nombre de transactions |
| `total_revenue_usd` | Revenus totaux |
| `total_units_sold` | Unités totales vendues |
| `avg_order_value` | Panier moyen (AOV) |
| `avg_price_usd` | Prix unitaire moyen |
| `avg_units_per_sale` | Moyenne d'unités par transaction |
| `unique_brands`, `unique_countries`, `unique_shoe_types`, `unique_channels` | Diversité |
| `first_sale_date`, `last_sale_date` | Couverture temporelle |

---

## 2. `dm_brand_performance.csv`

**Grain** : 1 ligne par marque (6 lignes) · **Usage** : page "Brands"

Colonnes : `Brand`, `sales`, `total_revenue`, `total_units`, `avg_price`, `avg_order_value`, `market_share_pct`.

Tri : par revenus décroissants.

---

## 3. `dm_country_performance.csv`

**Grain** : 1 ligne par pays (7 lignes) · **Usage** : page "Geography"

Colonnes : `Country`, `sales`, `total_revenue`, `total_units`, `avg_price`, `avg_order_value`, `market_share_pct`.

---

## 4. `dm_channel_performance.csv`

**Grain** : 1 ligne par canal (3 lignes) · **Usage** : page "Channels"

Colonnes : `Sales_Channel`, `sales`, `total_revenue`, `total_units`, `avg_order_value`, `avg_price`, `market_share_pct`.

---

## 5. `dm_monthly_trend.csv`

**Grain** : 1 ligne par mois (12 lignes) · **Usage** : line chart de saisonnalité

Colonnes : `YearMonth`, `sales`, `total_revenue`, `total_units`, `avg_order_value`.

Tri : chronologique.

---

## 6. `dm_shoe_type_performance.csv`

**Grain** : 1 ligne par type (6 lignes) · **Usage** : page "Products"

Colonnes : `Shoe_Type`, `sales`, `total_revenue`, `total_units`, `avg_price`, `market_share_pct`.

---

## 7. `dm_brand_country_matrix.csv`

**Grain** : marque × pays (~42 lignes) · **Usage** : heatmap croisée

Colonnes : `Brand`, `Country`, `sales`, `total_revenue`, `total_units`.

---

## 8. `dm_color_type_matrix.csv`

**Grain** : couleur × type (~36 lignes) · **Usage** : analyse mix produit

Colonnes : `Color`, `Shoe_Type`, `sales`, `total_revenue`, `avg_price`.

---

## Règles de construction

- Tous les arrondis à **2 décimales**
- `market_share_pct` toujours en base 100 (pas 0.XX)
- Source unique : `data/processed/shoes_sales_clean.csv`
- Régénérés à chaque exécution de `build_project.py`
- Format CSV pour compatibilité maximale (Looker, Excel, Sheets)