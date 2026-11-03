
import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "micro_intracity_grid.csv"
GRAPHICS_PATH = PROJECT_ROOT / "graphics"


def generate_publication_graphics(report_df, climate_df):
    """Generates four climate and data-centre risk visualizations."""

    print("[INFO] Generating Climate and Infrastructure Graphs...")

    GRAPHICS_PATH.mkdir(parents=True, exist_ok=True)

    # GRAPH 1: Intra-City Thermal Risk Heatmap

    if "sub_region" in report_df.columns:

        pivot_data = report_df.pivot(
            index="city",
            columns="sub_region",
            values="max_heat_index"
        )

        plt.figure(figsize=(10, 7))

        sns.heatmap(
            pivot_data,
            annot=True,
            fmt=".1f",
            cmap="YlOrRd",
            linewidths=0.5,
            cbar_kws={"label": "Apparent Temperature (°C)"}
        )

        plt.title("Intra-City Thermal Risk Heatmap")
        plt.xlabel("Sub-Region")
        plt.ylabel("City")
        plt.tight_layout()

        plt.savefig(
            GRAPHICS_PATH / "intracity_thermal_heatmap.png",
            dpi=300
        )
        plt.close()

    # GRAPH 2: Estimated PUE by Sub-Region

    sorted_report = report_df.sort_values(
        "Est_PUE",
        ascending=True
    )

    labels = (
        sorted_report["city"].astype(str)
        + " - "
        + sorted_report["sub_region"].astype(str)
    )

    plt.figure(figsize=(11, 8))

    plt.barh(
        labels,
        sorted_report["Est_PUE"]
    )

    plt.xlabel("Estimated PUE")
    plt.ylabel("Location")
    plt.title("Estimated Data Centre Energy Overhead by Location")
    plt.tight_layout()

    plt.savefig(
        GRAPHICS_PATH / "pue_energy_overhead.png",
        dpi=300
    )
    plt.close()

    # GRAPH 3: Climate Variable Correlation Heatmap

    climate_columns = [
        "temperature_2m_max",
        "apparent_temperature_max",
        "precipitation_sum",
        "wind_speed_10m_max"
    ]

    available_columns = [
        col for col in climate_columns
        if col in climate_df.columns
    ]

    correlation_data = climate_df[available_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    correlation_matrix = correlation_data.corr()

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        vmin=-1,
        vmax=1
    )

    plt.title("Correlation Between Climate Variables")
    plt.tight_layout()

    plt.savefig(
        GRAPHICS_PATH / "climate_correlation_heatmap.png",
        dpi=300
    )
    plt.close()

    # GRAPH 4: City-Wise Estimated PUE Comparison

    city_pue = (
        report_df.groupby("city")["Est_PUE"]
        .mean()
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    plt.bar(
        city_pue.index,
        city_pue.values
    )

    plt.xlabel("City")
    plt.ylabel("Average Estimated PUE")
    plt.title("City-Wise Data Centre PUE Comparison")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        GRAPHICS_PATH / "city_wise_pue_comparison.png",
        dpi=300
    )
    plt.close()

    print("[SUCCESS] All four graphs generated in the graphics folder.")


if __name__ == "__main__":

    from modules.data_ingestion_01 import load_macro_baseline
    from modules.thermal_modeling_03 import compute_thermal_stress_analytics
    from modules.risk_assessment_04 import evaluate_infrastructure_risk

    macro_data = load_macro_baseline()

    analytics = compute_thermal_stress_analytics(macro_data)

    report = evaluate_infrastructure_risk(analytics)

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Micro-grid dataset not found. Run Module 2 first."
        )

    climate_data = pd.read_csv(DATA_PATH)

    generate_publication_graphics(report, climate_data)
