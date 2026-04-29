"""
datamarts.py
------------
Construction des 8 datamarts analytiques.
"""

import pandas as pd


def _add_market_share(df: pd.DataFrame, value_col: str = "total_revenue") -> pd.DataFrame:
    """Ajoute une colonne market_share_pct calculée sur value_col."""
    total = df[value_col].sum()
    df = df.copy()
    df["market_share_pct"] = (100 * df[value_col] / total).round(2)
    return df


def build_global_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """KPIs globaux (1 ligne) — pour scorecards."""
    return pd.DataFrame([{
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
        "first_sale_date":     str(pd.to_datetime(df["Date"]).min().date()),
        "last_sale_date":      str(pd.to_datetime(df["Date"]).max().date()),
    }])


def build_brand_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Performance par marque + market share."""
    out = df.groupby("Brand", observed=True).agg(
        sales=("Sale_ID", "count"),
        total_revenue=("Revenue_USD", "sum"),
        total_units=("Units_Sold", "sum"),
        avg_price=("Price_USD", "mean"),
        avg_order_value=("Revenue_USD", "mean"),
    ).round(2).reset_index().sort_values("total_revenue", ascending=False)
    return _add_market_share(out)


def build_country_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Performance par pays + market share."""
    out = df.groupby("Country", observed=True).agg(
        sales=("Sale_ID", "count"),
        total_revenue=("Revenue_USD", "sum"),
        total_units=("Units_Sold", "sum"),
        avg_price=("Price_USD", "mean"),
        avg_order_value=("Revenue_USD", "mean"),
    ).round(2).reset_index().sort_values("total_revenue", ascending=False)
    return _add_market_share(out)


def build_channel_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Performance par canal de vente."""
    out = df.groupby("Sales_Channel", observed=True).agg(
        sales=("Sale_ID", "count"),
        total_revenue=("Revenue_USD", "sum"),
        total_units=("Units_Sold", "sum"),
        avg_order_value=("Revenue_USD", "mean"),
        avg_price=("Price_USD", "mean"),
    ).round(2).reset_index().sort_values("total_revenue", ascending=False)
    return _add_market_share(out)


def build_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Évolution mensuelle (saisonnalité)."""
    return df.groupby("YearMonth", observed=True).agg(
        sales=("Sale_ID", "count"),
        total_revenue=("Revenue_USD", "sum"),
        total_units=("Units_Sold", "sum"),
        avg_order_value=("Revenue_USD", "mean"),
    ).round(2).reset_index().sort_values("YearMonth")


def build_shoe_type_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Performance par type de chaussure."""
    out = df.groupby("Shoe_Type", observed=True).agg(
        sales=("Sale_ID", "count"),
        total_revenue=("Revenue_USD", "sum"),
        total_units=("Units_Sold", "sum"),
        avg_price=("Price_USD", "mean"),
    ).round(2).reset_index().sort_values("total_revenue", ascending=False)
    return _add_market_share(out)


def build_brand_country_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Matrice marque × pays pour heatmap."""
    return df.groupby(["Brand", "Country"], observed=True).agg(
        sales=("Sale_ID", "count"),
        total_revenue=("Revenue_USD", "sum"),
        total_units=("Units_Sold", "sum"),
    ).round(2).reset_index()


def build_color_type_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Matrice couleur × type pour analyse mix produit."""
    return df.groupby(["Color", "Shoe_Type"], observed=True).agg(
        sales=("Sale_ID", "count"),
        total_revenue=("Revenue_USD", "sum"),
        avg_price=("Price_USD", "mean"),
    ).round(2).reset_index()


def build_all(df: pd.DataFrame) -> dict:
    """Construit les 8 datamarts d'un coup."""
    return {
        "global_kpis":           build_global_kpis(df),
        "brand_performance":     build_brand_performance(df),
        "country_performance":   build_country_performance(df),
        "channel_performance":   build_channel_performance(df),
        "monthly_trend":         build_monthly_trend(df),
        "shoe_type_performance": build_shoe_type_performance(df),
        "brand_country_matrix":  build_brand_country_matrix(df),
        "color_type_matrix":     build_color_type_matrix(df),
    }