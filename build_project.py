"""
build_project.py
----------------
Pipeline complet : nettoyage → datamarts → exports Looker → 10 figures PNG.

Usage :
    python build_project.py
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# Configuration
# ============================================================
ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "shoes_sales.csv"
PROCESSED = ROOT / "data" / "processed"
DATAMARTS = ROOT / "data" / "datamarts"
EXPORTS = ROOT / "data" / "exports"
FIGURES = ROOT / "images" / "figures"

for d in [PROCESSED, DATAMARTS, EXPORTS, FIGURES]:
    d.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 140,
    "savefig.bbox": "tight",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
})

BRAND_COLORS = {
    "Nike":        "#FA5400",
    "Adidas":      "#000000",
    "Puma":        "#0066B3",
    "Reebok":      "#D81E05",
    "Skechers":    "#1B3D6E",
    "New Balance": "#CE0E2D",
}
CHANNEL_COLORS = {
    "Online":       "#3498db",
    "Mall":         "#9b59b6",
    "Retail Store": "#e67e22",
}

# ============================================================
# 1. CHARGEMENT + NETTOYAGE + FEATURES
# ============================================================
print("▶ [1/4] Chargement et nettoyage…")
df = pd.read_csv(RAW)

# --- Conversions ---
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["MonthName"] = df["Date"].dt.strftime("%b")
df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")
df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
df["DayOfWeek"] = df["Date"].dt.day_name()
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
df["Season"] = df["Month"].apply(
    lambda m: "Winter" if m in [12, 1, 2] else
              "Spring" if m in [3, 4, 5] else
              "Summer" if m in [6, 7, 8] else "Autumn"
)

# --- Features dérivées business ---
df["Price_Bucket"] = pd.cut(
    df["Price_USD"], bins=[0, 75, 150, 250],
    labels=["Budget (<75$)", "Mid-range (75-150$)", "Premium (>150$)"]
)
df["Revenue_Bucket"] = pd.cut(
    df["Revenue_USD"], bins=[0, 500, 1500, 3000, 5000],
    labels=["Small", "Medium", "Large", "XLarge"]
)
# Vérification cohérence Revenue = Price × Units
df["Revenue_Check_Diff"] = (df["Revenue_USD"] - df["Price_USD"] * df["Units_Sold"]).round(2)

df.to_csv(PROCESSED / "shoes_sales_clean.csv", index=False)
print(f"   ✓ {len(df)} ventes nettoyées — {PROCESSED / 'shoes_sales_clean.csv'}")

# ============================================================
# 2. DATAMARTS
# ============================================================
print("▶ [2/4] Construction des datamarts…")

# DM 1 : KPIs globaux
dm_kpi = pd.DataFrame([{
    "total_sales":         len(df),
    "total_revenue_usd":   round(df["Revenue_USD"].sum(), 2),
    "total_units_sold":    int(df["Units_Sold"].sum()),
    "avg_order_value":     round(df["Revenue_USD"].mean(), 2),
    "avg_price_usd":       round(df["Price_USD"].mean(), 2),
    "avg_units_per_sale":  round(df["Units_Sold"].mean(), 2),
    "unique_brands":       df["Brand"].nunique(),
    "unique_countries":    df["Country"].nunique(),
    "unique_shoe_types":   df["Shoe_Type"].nunique(),
    "unique_channels":     df["Sales_Channel"].nunique(),
    "first_sale_date":     str(df["Date"].min().date()),
    "last_sale_date":      str(df["Date"].max().date()),
}])
dm_kpi.to_csv(DATAMARTS / "dm_global_kpis.csv", index=False)

# DM 2 : Performance par marque
dm_brand = df.groupby("Brand", observed=True).agg(
    sales=("Sale_ID", "count"),
    total_revenue=("Revenue_USD", "sum"),
    total_units=("Units_Sold", "sum"),
    avg_price=("Price_USD", "mean"),
    avg_order_value=("Revenue_USD", "mean"),
).round(2).reset_index().sort_values("total_revenue", ascending=False)
dm_brand["market_share_pct"] = (100 * dm_brand["total_revenue"] /
                                 dm_brand["total_revenue"].sum()).round(2)
dm_brand.to_csv(DATAMARTS / "dm_brand_performance.csv", index=False)

# DM 3 : Performance par pays
dm_country = df.groupby("Country", observed=True).agg(
    sales=("Sale_ID", "count"),
    total_revenue=("Revenue_USD", "sum"),
    total_units=("Units_Sold", "sum"),
    avg_price=("Price_USD", "mean"),
    avg_order_value=("Revenue_USD", "mean"),
).round(2).reset_index().sort_values("total_revenue", ascending=False)
dm_country["market_share_pct"] = (100 * dm_country["total_revenue"] /
                                   dm_country["total_revenue"].sum()).round(2)
dm_country.to_csv(DATAMARTS / "dm_country_performance.csv", index=False)

# DM 4 : Performance par canal
dm_channel = df.groupby("Sales_Channel", observed=True).agg(
    sales=("Sale_ID", "count"),
    total_revenue=("Revenue_USD", "sum"),
    total_units=("Units_Sold", "sum"),
    avg_order_value=("Revenue_USD", "mean"),
    avg_price=("Price_USD", "mean"),
).round(2).reset_index().sort_values("total_revenue", ascending=False)
dm_channel["market_share_pct"] = (100 * dm_channel["total_revenue"] /
                                   dm_channel["total_revenue"].sum()).round(2)
dm_channel.to_csv(DATAMARTS / "dm_channel_performance.csv", index=False)

# DM 5 : Évolution mensuelle
dm_monthly = df.groupby("YearMonth", observed=True).agg(
    sales=("Sale_ID", "count"),
    total_revenue=("Revenue_USD", "sum"),
    total_units=("Units_Sold", "sum"),
    avg_order_value=("Revenue_USD", "mean"),
).round(2).reset_index().sort_values("YearMonth")
dm_monthly.to_csv(DATAMARTS / "dm_monthly_trend.csv", index=False)

# DM 6 : Performance par type de chaussure
dm_type = df.groupby("Shoe_Type", observed=True).agg(
    sales=("Sale_ID", "count"),
    total_revenue=("Revenue_USD", "sum"),
    total_units=("Units_Sold", "sum"),
    avg_price=("Price_USD", "mean"),
).round(2).reset_index().sort_values("total_revenue", ascending=False)
dm_type["market_share_pct"] = (100 * dm_type["total_revenue"] /
                                dm_type["total_revenue"].sum()).round(2)
dm_type.to_csv(DATAMARTS / "dm_shoe_type_performance.csv", index=False)

# DM 7 : Matrice marque × pays (pour heatmap)
dm_brand_country = df.groupby(["Brand", "Country"], observed=True).agg(
    sales=("Sale_ID", "count"),
    total_revenue=("Revenue_USD", "sum"),
    total_units=("Units_Sold", "sum"),
).round(2).reset_index()
dm_brand_country.to_csv(DATAMARTS / "dm_brand_country_matrix.csv", index=False)

# DM 8 : Mix produit (couleur × type)
dm_color_type = df.groupby(["Color", "Shoe_Type"], observed=True).agg(
    sales=("Sale_ID", "count"),
    total_revenue=("Revenue_USD", "sum"),
    avg_price=("Price_USD", "mean"),
).round(2).reset_index()
dm_color_type.to_csv(DATAMARTS / "dm_color_type_matrix.csv", index=False)

print(f"   ✓ 8 datamarts dans {DATAMARTS}/")

# Exports Looker
df.to_csv(EXPORTS / "main_dataset.csv", index=False)
dm_brand.to_csv(EXPORTS / "by_brand.csv", index=False)
dm_country.to_csv(EXPORTS / "by_country.csv", index=False)
dm_channel.to_csv(EXPORTS / "by_channel.csv", index=False)
dm_monthly.to_csv(EXPORTS / "monthly_trend.csv", index=False)
dm_type.to_csv(EXPORTS / "by_shoe_type.csv", index=False)
dm_kpi.to_csv(EXPORTS / "global_kpis.csv", index=False)

# ============================================================
# 3. FIGURES
# ============================================================
print("▶ [3/4] Génération des figures…")

# Fig 1 : Revenus par marque
fig, ax = plt.subplots(figsize=(11, 6))
data = dm_brand.sort_values("total_revenue")
colors = [BRAND_COLORS.get(b, "#888") for b in data["Brand"]]
bars = ax.barh(data["Brand"], data["total_revenue"], color=colors, edgecolor="black")
for bar, val, share in zip(bars, data["total_revenue"], data["market_share_pct"]):
    ax.text(val + 5000, bar.get_y() + bar.get_height()/2,
            f"${val:,.0f}\n({share:.1f}%)", va="center", fontweight="bold", fontsize=9)
ax.set_title("Revenus totaux par marque (2025)")
ax.set_xlabel("Revenus (USD)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
plt.savefig(FIGURES / "01_revenue_by_brand.png")
plt.close()

# Fig 2 : Évolution mensuelle des ventes
fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(dm_monthly["YearMonth"], dm_monthly["total_revenue"],
        marker="o", linewidth=2.5, color="#2c3e50", markersize=8)
ax.fill_between(dm_monthly["YearMonth"], dm_monthly["total_revenue"], alpha=0.2, color="#3498db")
for i, (m, r) in enumerate(zip(dm_monthly["YearMonth"], dm_monthly["total_revenue"])):
    ax.text(i, r + 4000, f"${r/1000:.0f}k", ha="center", fontsize=9, fontweight="bold")
ax.set_title("Évolution mensuelle des revenus (2025)")
ax.set_xlabel("Mois"); ax.set_ylabel("Revenus (USD)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
plt.xticks(rotation=45)
plt.savefig(FIGURES / "02_monthly_revenue_trend.png")
plt.close()

# Fig 3 : Top pays
fig, ax = plt.subplots(figsize=(10, 6))
data = dm_country.sort_values("total_revenue")
bars = ax.barh(data["Country"], data["total_revenue"],
               color=sns.color_palette("viridis", len(data)), edgecolor="black")
for bar, val, share in zip(bars, data["total_revenue"], data["market_share_pct"]):
    ax.text(val + 3000, bar.get_y() + bar.get_height()/2,
            f"${val/1000:.1f}k ({share:.1f}%)", va="center", fontweight="bold", fontsize=9)
ax.set_title("Top pays par revenus")
ax.set_xlabel("Revenus (USD)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
plt.savefig(FIGURES / "03_revenue_by_country.png")
plt.close()

# Fig 4 : Répartition par canal de vente (donut)
fig, ax = plt.subplots(figsize=(9, 7))
colors_c = [CHANNEL_COLORS.get(c, "#888") for c in dm_channel["Sales_Channel"]]
wedges, texts, autotexts = ax.pie(
    dm_channel["total_revenue"], labels=dm_channel["Sales_Channel"],
    autopct=lambda p: f"{p:.1f}%\n(${p*dm_channel['total_revenue'].sum()/100/1000:.1f}k)",
    colors=colors_c, startangle=90, wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
    textprops={"fontweight": "bold", "fontsize": 11}
)
ax.set_title("Répartition des revenus par canal de vente")
plt.savefig(FIGURES / "04_revenue_by_channel.png")
plt.close()

# Fig 5 : Performance par type de chaussure
fig, ax = plt.subplots(figsize=(11, 6))
data = dm_type.sort_values("total_revenue")
bars = ax.barh(data["Shoe_Type"], data["total_revenue"],
               color=sns.color_palette("rocket_r", len(data)), edgecolor="black")
for bar, val, units in zip(bars, data["total_revenue"], data["total_units"]):
    ax.text(val + 3000, bar.get_y() + bar.get_height()/2,
            f"${val/1000:.1f}k\n({int(units)} unités)", va="center", fontweight="bold", fontsize=9)
ax.set_title("Revenus par type de chaussure")
ax.set_xlabel("Revenus (USD)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
plt.savefig(FIGURES / "05_revenue_by_shoe_type.png")
plt.close()

# Fig 6 : Heatmap marque × pays (revenus)
fig, ax = plt.subplots(figsize=(10, 6))
pivot = df.pivot_table(values="Revenue_USD", index="Brand",
                       columns="Country", aggfunc="sum", fill_value=0).round(0)
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu",
            cbar_kws={"label": "Revenus (USD)"}, ax=ax, linewidths=0.5)
ax.set_title("Revenus par marque et par pays")
ax.set_xlabel("Pays"); ax.set_ylabel("Marque")
plt.savefig(FIGURES / "06_brand_country_heatmap.png")
plt.close()

# Fig 7 : Distribution des prix
fig, ax = plt.subplots(figsize=(11, 6))
for brand in df["Brand"].unique():
    data = df.loc[df["Brand"] == brand, "Price_USD"]
    ax.hist(data, bins=20, alpha=0.45, label=brand,
            color=BRAND_COLORS.get(brand, "#888"), edgecolor="black", linewidth=0.5)
ax.set_title("Distribution des prix par marque")
ax.set_xlabel("Prix (USD)"); ax.set_ylabel("Nombre de ventes")
ax.legend(title="Marque", loc="upper right")
plt.savefig(FIGURES / "07_price_distribution_by_brand.png")
plt.close()

# Fig 8 : Saisonnalité
fig, ax = plt.subplots(figsize=(10, 6))
season_order = ["Winter", "Spring", "Summer", "Autumn"]
season_data = df.groupby("Season", observed=True)["Revenue_USD"].sum().reindex(season_order)
season_colors = ["#3498db", "#2ecc71", "#f39c12", "#e67e22"]
bars = ax.bar(season_data.index, season_data.values, color=season_colors, edgecolor="black")
for bar, val in zip(bars, season_data.values):
    pct = 100 * val / season_data.sum()
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
            f"${val/1000:.1f}k\n({pct:.1f}%)", ha="center", fontweight="bold")
ax.set_title("Revenus par saison")
ax.set_ylabel("Revenus (USD)")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
plt.savefig(FIGURES / "08_revenue_by_season.png")
plt.close()

# Fig 9 : Top 10 ventes (plus grosses transactions)
fig, ax = plt.subplots(figsize=(11, 6))
top10 = df.nlargest(10, "Revenue_USD").sort_values("Revenue_USD")
labels = [f"{r['Brand']} {r['Shoe_Type']} ({r['Country']})" for _, r in top10.iterrows()]
bars = ax.barh(labels, top10["Revenue_USD"],
               color=sns.color_palette("magma_r", 10), edgecolor="black")
for bar, val, units in zip(bars, top10["Revenue_USD"], top10["Units_Sold"]):
    ax.text(val + 50, bar.get_y() + bar.get_height()/2,
            f"${val:,.0f} ({int(units)} u.)", va="center", fontweight="bold", fontsize=9)
ax.set_title("Top 10 des plus grosses transactions")
ax.set_xlabel("Revenus (USD)")
plt.savefig(FIGURES / "09_top10_transactions.png")
plt.close()

# Fig 10 : Couleur × type (heatmap mix produit)
fig, ax = plt.subplots(figsize=(10, 6))
color_type_pivot = df.pivot_table(values="Sale_ID", index="Color",
                                   columns="Shoe_Type", aggfunc="count", fill_value=0)
sns.heatmap(color_type_pivot, annot=True, fmt="d", cmap="Purples",
            cbar_kws={"label": "Nombre de ventes"}, ax=ax, linewidths=0.5)
ax.set_title("Mix produit : ventes par couleur et type de chaussure")
plt.savefig(FIGURES / "10_color_type_heatmap.png")
plt.close()

print(f"   ✓ 10 figures dans {FIGURES}/")
print("▶ [4/4] Terminé ✨")
