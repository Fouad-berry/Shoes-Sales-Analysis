"""
preprocessing.py
----------------
Nettoyage et feature engineering.
"""

import pandas as pd
import numpy as np


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute toutes les features dérivées de la date."""
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%b")
    df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")
    df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
    return df


def add_season(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute la saison à partir du mois (hémisphère nord)."""
    df = df.copy()
    df["Season"] = df["Month"].apply(
        lambda m: "Winter" if m in [12, 1, 2] else
                  "Spring" if m in [3, 4, 5] else
                  "Summer" if m in [6, 7, 8] else "Autumn"
    )
    return df


def add_price_buckets(df: pd.DataFrame) -> pd.DataFrame:
    """Catégorise les prix en buckets business."""
    df = df.copy()
    df["Price_Bucket"] = pd.cut(
        df["Price_USD"], bins=[0, 75, 150, 250],
        labels=["Budget (<75$)", "Mid-range (75-150$)", "Premium (>150$)"]
    )
    return df


def add_revenue_buckets(df: pd.DataFrame) -> pd.DataFrame:
    """Catégorise les revenus par taille de transaction."""
    df = df.copy()
    df["Revenue_Bucket"] = pd.cut(
        df["Revenue_USD"], bins=[0, 500, 1500, 3000, 5000],
        labels=["Small", "Medium", "Large", "XLarge"]
    )
    return df


def add_consistency_check(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie la cohérence Revenue = Price × Units.
    Ajoute une colonne avec l'écart (devrait être ~0).
    """
    df = df.copy()
    df["Revenue_Check_Diff"] = (df["Revenue_USD"] - df["Price_USD"] * df["Units_Sold"]).round(2)
    return df


def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline complet de nettoyage + features."""
    df = df.drop_duplicates().reset_index(drop=True)
    df = add_date_features(df)
    df = add_season(df)
    df = add_price_buckets(df)
    df = add_revenue_buckets(df)
    df = add_consistency_check(df)
    return df