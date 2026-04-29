"""
visualizations.py
-----------------
Fonctions de plot réutilisables.
"""

import matplotlib.pyplot as plt
import seaborn as sns


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
SEASON_COLORS = {
    "Winter": "#3498db",
    "Spring": "#2ecc71",
    "Summer": "#f39c12",
    "Autumn": "#e67e22",
}


def set_style():
    """Style cohérent."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 140,
        "savefig.bbox": "tight",
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
    })


def plot_revenue_by_brand(dm_brand, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(11, 6))
    data = dm_brand.sort_values("total_revenue")
    colors = [BRAND_COLORS.get(b, "#888") for b in data["Brand"]]
    bars = ax.barh(data["Brand"], data["total_revenue"], color=colors, edgecolor="black")
    for bar, val in zip(bars, data["total_revenue"]):
        ax.text(val + 5000, bar.get_y() + bar.get_height()/2,
                f"${val:,.0f}", va="center", fontweight="bold", fontsize=9)
    ax.set_title("Revenus totaux par marque")
    ax.set_xlabel("Revenus (USD)")
    return ax


def plot_monthly_trend(dm_monthly, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(13, 6))
    ax.plot(dm_monthly["YearMonth"], dm_monthly["total_revenue"],
            marker="o", linewidth=2.5, color="#2c3e50", markersize=8)
    ax.fill_between(dm_monthly["YearMonth"], dm_monthly["total_revenue"], alpha=0.2, color="#3498db")
    ax.set_title("Évolution mensuelle des revenus")
    ax.set_xlabel("Mois"); ax.set_ylabel("Revenus (USD)")
    plt.setp(ax.get_xticklabels(), rotation=45)
    return ax


def plot_brand_country_heatmap(df, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))
    pivot = df.pivot_table(values="Revenue_USD", index="Brand",
                           columns="Country", aggfunc="sum", fill_value=0)
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu",
                cbar_kws={"label": "Revenus (USD)"}, ax=ax, linewidths=0.5)
    ax.set_title("Revenus par marque et par pays")
    return ax


def plot_channel_donut(dm_channel, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(9, 7))
    colors = [CHANNEL_COLORS.get(c, "#888") for c in dm_channel["Sales_Channel"]]
    ax.pie(dm_channel["total_revenue"], labels=dm_channel["Sales_Channel"],
           autopct="%.1f%%", colors=colors, startangle=90,
           wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
           textprops={"fontweight": "bold"})
    ax.set_title("Répartition des revenus par canal")
    return ax


def plot_seasonality(df, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))
    season_order = ["Winter", "Spring", "Summer", "Autumn"]
    data = df.groupby("Season", observed=True)["Revenue_USD"].sum().reindex(season_order)
    colors = [SEASON_COLORS[s] for s in data.index]
    bars = ax.bar(data.index, data.values, color=colors, edgecolor="black")
    for bar, val in zip(bars, data.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f"${val/1000:.1f}k", ha="center", fontweight="bold")
    ax.set_title("Revenus par saison")
    ax.set_ylabel("Revenus (USD)")
    return ax