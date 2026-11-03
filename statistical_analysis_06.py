
import numpy as np
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "micro_intracity_grid.csv"
)

OUTPUT_PATH = PROJECT_ROOT / "data" / "processed"


def load_climate_data():
    """Loads and prepares the micro-intracity climate dataset."""

    print("[INFO] Loading Micro-Intracity Climate Dataset...")

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}. Run Module 2 first."
        )

    df = pd.read_csv(DATA_PATH)

    # Open-Meteo returns the date column as 'time'
    if "time" in df.columns:
        df.rename(columns={"time": "date"}, inplace=True)

    df.columns = df.columns.str.strip().str.lower()

    required_columns = [
        "date",
        "city",
        "sub_region",
        "apparent_temperature_max"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["apparent_temperature_max"] = pd.to_numeric(
        df["apparent_temperature_max"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "date",
            "city",
            "sub_region",
            "apparent_temperature_max"
        ]
    )

    print(
        f"[SUCCESS] Loaded {len(df)} records "
        f"from {df['city'].nunique()} cities."
    )

    return df


def perform_statistical_analysis(df):
    """Performs five statistical analyses on climate data."""

    print("\n[INFO] Starting Statistical Analysis...")

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # ANALYSIS 1: DESCRIPTIVE STATISTICS

    descriptive_stats = (
        df.groupby(["city", "sub_region"])
        ["apparent_temperature_max"]
        .agg(
            Mean="mean",
            Median="median",
            Standard_Deviation="std",
            Minimum="min",
            Maximum="max"
        )
    )

    percentiles = (
        df.groupby(["city", "sub_region"])
        ["apparent_temperature_max"]
        .quantile([0.95, 0.99])
        .unstack()
    )

    percentiles.columns = [
        "95th_Percentile",
        "99th_Percentile"
    ]

    descriptive_stats = descriptive_stats.join(
        percentiles
    )

    descriptive_stats.to_csv(
        OUTPUT_PATH / "descriptive_statistics.csv"
    )

    print("[SUCCESS] Descriptive Statistics Generated.")

    # ANALYSIS 2: EXTREME HEAT ANALYSIS

    df["Extreme_Heat_Day"] = (
        df["apparent_temperature_max"] >= 45
    )

    extreme_heat = (
        df.groupby("city")
        .agg(
            Total_Observations=("Extreme_Heat_Day", "count"),
            Extreme_Heat_Days=("Extreme_Heat_Day", "sum")
        )
    )

    extreme_heat["Extreme_Heat_Percentage"] = (
        extreme_heat["Extreme_Heat_Days"]
        / extreme_heat["Total_Observations"]
    ) * 100

    extreme_heat.to_csv(
        OUTPUT_PATH / "extreme_heat_analysis.csv"
    )

    print("[SUCCESS] Extreme Heat Analysis Generated.")

    # ANALYSIS 3: CITY-WISE TEMPERATURE COMPARISON

    city_comparison = (
        df.groupby("city")
        ["apparent_temperature_max"]
        .agg(
            Average_Temperature="mean",
            Peak_Temperature="max",
            Minimum_Temperature="min"
        )
        .sort_values(
            by="Average_Temperature",
            ascending=False
        )
    )

    city_comparison.to_csv(
        OUTPUT_PATH / "city_temperature_comparison.csv"
    )

    print("[SUCCESS] City-wise Comparison Generated.")

    # ANALYSIS 4: CLIMATE VARIABLE CORRELATION

    climate_columns = [
        "temperature_2m_max",
        "apparent_temperature_max",
        "precipitation_sum",
        "wind_speed_10m_max"
    ]

    available_columns = [
        col for col in climate_columns
        if col in df.columns
    ]

    numeric_data = df[available_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    correlation_matrix = numeric_data.corr()

    correlation_matrix.to_csv(
        OUTPUT_PATH / "climate_correlation.csv"
    )

    print("[SUCCESS] Correlation Analysis Generated.")

    # ANALYSIS 5: YEARLY TEMPERATURE TREND

    df["year"] = df["date"].dt.year

    yearly_data = (
        df.groupby(["city", "year"])
        ["apparent_temperature_max"]
        .mean()
        .reset_index()
    )

    yearly_data.to_csv(
        OUTPUT_PATH / "yearly_temperature_trends.csv",
        index=False
    )

    trend_results = []

    for city, group in yearly_data.groupby("city"):

        if len(group) < 2:
            continue

        slope, intercept = np.polyfit(
            group["year"],
            group["apparent_temperature_max"],
            1
        )

        if slope > 0:
            trend = "Increasing"
        elif slope < 0:
            trend = "Decreasing"
        else:
            trend = "Stable"

        trend_results.append({
            "city": city,
            "temperature_change_per_year": slope,
            "trend": trend
        })

    trend_analysis = pd.DataFrame(trend_results)

    trend_analysis.to_csv(
        OUTPUT_PATH / "temperature_trend_analysis.csv",
        index=False
    )

    print("[SUCCESS] Yearly Trend Analysis Generated.")

    # DISPLAY RESULTS

    print("\n========== STATISTICAL ANALYSIS RESULTS ==========")

    print("\n1. Descriptive Statistics:")
    print(descriptive_stats.round(2))

    print("\n2. Extreme Heat Analysis:")
    print(extreme_heat.round(2))

    print("\n3. City-Wise Temperature Comparison:")
    print(city_comparison.round(2))

    print("\n4. Climate Correlation:")
    print(correlation_matrix.round(2))

    print("\n5. Yearly Temperature Trends:")
    print(trend_analysis.round(4))

    print("\n[COMPLETE] All Statistical Analyses Finished.")

    return {
        "descriptive_statistics": descriptive_stats,
        "extreme_heat_analysis": extreme_heat,
        "city_comparison": city_comparison,
        "correlation_matrix": correlation_matrix,
        "yearly_data": yearly_data,
        "trend_analysis": trend_analysis
    }


if __name__ == "__main__":

    climate_data = load_climate_data()

    results = perform_statistical_analysis(
        climate_data
    )
