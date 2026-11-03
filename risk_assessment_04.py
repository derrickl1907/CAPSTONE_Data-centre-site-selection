import pandas as pd


def evaluate_infrastructure_risk(analytics_df: pd.DataFrame) -> pd.DataFrame:
    """Evaluates data center siting suitability, estimates operational PUE / WUE penalties,

    and maps engineered cooling mitigations based on local thermal risk tiers.
    """
    print("[INFO] Mapping Infrastructure Risk Tiers & Cooling Mitigations...")

    def assign_datacenter_specs(row):
        hi = row["max_heat_index"]
        p99 = row["p99_heat_index"]

        if hi >= 50 or p99 >= 46:
            tier = "CRITICAL / SEVERE RISK"
            pue = 1.48
            wue = "High (>2.2 L/kWh)"
            cooling_tech = "Direct-to-Chip Liquid Cooling (DLC) or Immersion Cooling"
            mitigation = (
                "Direct air evaporative cooling prohibited due to severe wet-bulb spikes. "
                "Requires N+2 HVAC redundancy, closed-loop DLC, and secondary condenser scaling protection."
            )
        elif 45 <= hi < 50:
            tier = "HIGH RISK"
            pue = 1.34
            wue = "Moderate-High (1.5-2.0 L/kWh)"
            cooling_tech = "Hybrid Air-Water Economizers & Chilled Water Loops"
            mitigation = (
                "Restricted direct evaporative cooling during summer monsoons. Deploy dual-mode "
                "chilled water plants with dynamic variable-frequency drive (VFD) chillers."
            )
        elif 40 <= hi < 45:
            tier = "MODERATE RISK"
            pue = 1.21
            wue = "Low (0.8-1.2 L/kWh)"
            cooling_tech = "Standard Air-Side Economizers & Mechanical Chillers"
            mitigation = (
                "Standard operational climate. Seasonal free-cooling economizers operate efficiently "
                "for ~6-8 months per year."
            )
        else:
            tier = "LOW RISK"
            pue = 1.12
            wue = "Minimal (<0.5 L/kWh)"
            cooling_tech = "Direct Ambient Air Free-Cooling"
            mitigation = (
                "Optimal thermal profile. Maximize direct ambient air economization to achieve lowest "
                "operational PUE (<1.15) and minimize water footprint."
            )

        return pd.Series(
            [tier, pue, wue, cooling_tech, mitigation],
            index=[
                "Risk_Tier",
                "Est_PUE",
                "Est_WUE",
                "Recommended_Cooling",
                "Mitigation_Strategy",
            ],
        )

    eval_specs = analytics_df.apply(assign_datacenter_specs, axis=1)
    report_df = pd.concat([analytics_df, eval_specs], axis=1)
    return report_df.sort_values(
        by="max_heat_index", ascending=False
    ).reset_index(drop=True)


if __name__ == "__main__":
    from data_ingestion_01 import load_macro_baseline
    from thermal_modeling_03 import compute_thermal_stress_analytics

    macro_data = load_macro_baseline()
    analytics = compute_thermal_stress_analytics(macro_data)
    final_report = evaluate_infrastructure_risk(analytics)
    print(
        final_report[
            [
                "city",
                "sub_region",
                "max_heat_index",
                "Risk_Tier",
                "Est_PUE",
                "Recommended_Cooling",
            ]
        ].head(10)
    )