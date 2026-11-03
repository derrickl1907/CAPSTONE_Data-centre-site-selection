
import os
import pandas as pd
from pathlib import Path


def load_macro_baseline(
    file_path: str = "data/raw/DOC-20260922-WA0000.csv",
) -> pd.DataFrame:
    """Loads and validates the original multi-decade macro climate dataset (2000-2024).

    Cleans data types, checks integrity, and maps baseline centroid coordinates.
    """

    # Resolve dataset path relative to the project root
    if not os.path.isabs(file_path):
        project_root = Path(__file__).resolve().parent.parent
        file_path = str(project_root / file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Original dataset '{file_path}' not found."
        )

    print("[INFO] Loading Macro City Baseline Dataset...")
    df = pd.read_csv(file_path)

    # Convert date and extract temporal attributes
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # Map baseline centroid coordinates for each metro area
    city_centroids = {
        "Delhi": {"lat": 28.6139, "lon": 77.2090},
        "Mumbai": {"lat": 19.0760, "lon": 72.8777},
        "Kolkata": {"lat": 22.5726, "lon": 88.3639},
        "Chennai": {"lat": 13.0827, "lon": 80.2707},
        "Bangalore": {"lat": 12.9716, "lon": 77.5946},
        "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
        "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
        "Pune": {"lat": 18.5204, "lon": 73.8567},
        "Jaipur": {"lat": 26.9124, "lon": 75.7877},
        "Lucknow": {"lat": 26.8467, "lon": 80.9462},
    }

    df["centroid_lat"] = df["city"].map(
        lambda c: city_centroids.get(c, {}).get("lat")
    )
    df["centroid_lon"] = df["city"].map(
        lambda c: city_centroids.get(c, {}).get("lon")
    )

    print(
        f"[SUCCESS] Macro dataset successfully loaded: "
        f"{df.shape[0]} rows across {df['city'].nunique()} cities."
    )

    return df


if __name__ == "__main__":
    df_macro = load_macro_baseline()
    print(df_macro.head(3))
