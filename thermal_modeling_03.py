import os
import numpy as np
import pandas as pd


def compute_thermal_stress_analytics(
    macro_df: pd.DataFrame,
    micro_csv_path: str = "data/processed/micro_intracity_grid.csv",
) -> pd.DataFrame:
    """Processes Macro city baseline and Micro coordinate grid data to derive

    peak heat index metrics, 99th percentile extreme stress, and heatwave durations.
    """
    print("[INFO] Executing Thermal Stress & Heat Index Analytics Engine...")

    if os.path.exists(micro_csv_path):
        grid_df = pd.read_csv(micro_csv_path)
        group_cols = ["city", "sub_region"]
    else:
        print(
            "[NOTICE] Micro-grid CSV not found. Running thermal analytics on Macro Dataset."
        )
        grid_df = macro_df.copy()
        grid_df["sub_region"] = "Central"
        group_cols = ["city", "sub_region"]

    analytics_summary = (
        grid_df.groupby(group_cols)
        .agg(
            avg_max_temp=("temperature_2m_max", "mean"),
            max_temp_recorded=("temperature_2m_max", "max"),
            avg_apparent_max_temp=("apparent_temperature_max", "mean"),
            max_heat_index=("apparent_temperature_max", "max"),
            p99_heat_index=(
                "apparent_temperature_max",
                lambda x: np.percentile(x, 99),
            ),
            heatwave_days_above_40c=(
                "temperature_2m_max",
                lambda x: (x >= 40).sum(),
            ),
            extreme_hi_days_above_45c=(
                "apparent_temperature_max",
                lambda x: (x >= 45).sum(),
            ),
        )
        .reset_index()
    )

    return analytics_summary


if __name__ == "__main__":
    from data_ingestion_01 import load_macro_baseline

    macro_data = load_macro_baseline()
    results = compute_thermal_stress_analytics(macro_data)
    print(results.head(10))