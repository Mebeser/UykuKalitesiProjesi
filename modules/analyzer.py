# modules/analyzer.py
# import os
# os.environ["PANDAS_NO_BOTTLENECK"] = "1"

import pandas as pd
import numpy as np

def analyze_sleep_data(csv_path):
    # CSV dosyasını oku
    df = pd.read_csv(csv_path)

    # Gerekli kolonlar kontrolü
    required_cols = ['Tarih', 'Uyku_Süresi_Saat', 'Derin_Uyku_Yüzdesi']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"'{col}' kolonu eksik!")

    # Ortalama değerler
    avg_sleep = df['Uyku_Süresi_Saat'].mean()
    avg_deep = df['Derin_Uyku_Yüzdesi'].mean()

    # Uyku düzeni (standart sapma)
    std_dev = np.std(df['Uyku_Süresi_Saat'])

    # En iyi ve en kötü günler
    best_day = df.loc[df['Uyku_Süresi_Saat'].idxmax(), 'Tarih']
    worst_day = df.loc[df['Uyku_Süresi_Saat'].idxmin(), 'Tarih']

    # Uyku puanı hesapla
    sleep_score = (avg_sleep * 10) + (avg_deep * 2) - (std_dev * 5)
    sleep_score = max(0, min(100, round(sleep_score, 2)))

    summary = {
        "ortalama_uyku": round(avg_sleep, 2),
        "ortalama_derin": round(avg_deep, 2),
        "std_sapma": round(std_dev, 2),
        "en_iyi_gun": best_day,
        "en_kotu_gun": worst_day,
        "uyku_puani": sleep_score
    }

    return df, summary
