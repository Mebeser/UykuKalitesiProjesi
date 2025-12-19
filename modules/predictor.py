# modules/predictor.py — Smart Prediction Engine v3.0
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np

def predict_next_score(csv_path):
    try:
        df = pd.read_csv(csv_path)

        # Yeterli veri kontrolü
        if len(df) < 5:
            return "Yeterli veri yok. En az 5 günlük kayıt girin."

        # Özellikler (X) ve hedef değişken (y)
        X = df[['Uyku_Süresi_Saat', 'Derin_Uyku_Yüzdesi']]
        y = (df['Uyku_Süresi_Saat'] * 10 + df['Derin_Uyku_Yüzdesi'] * 2).clip(0, 100)

        # Modeli eğit
        model = LinearRegression()
        model.fit(X, y)

        # Tahminler ve R² skoru
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        confidence = round(r2 * 100, 1)

        # Son veriye göre yarın tahmini
        last_row = X.iloc[-1].to_numpy().reshape(1, -1)
        prediction = model.predict(last_row)[0]
        prediction = float(np.clip(prediction, 0, 100))

        # Trend analizi (son 3 günün puan ortalaması farkı)
        last3 = y.tail(3).mean()
        prev3 = y.tail(6).head(3).mean() if len(y) >= 6 else y.head(3).mean()
        trend = "🔼 Eğilim Yükseliyor" if last3 > prev3 else "🔽 Eğilim Düşüyor"

        # 🔹 Grafik
        plt.style.use("ggplot")
        plt.figure(figsize=(6, 4))
        days = list(range(1, len(y) + 1))
        plt.plot(days, y, marker='o', label="Gerçek Uyku Puanı", linewidth=2)
        plt.scatter(len(y) + 1, prediction, color='orange', s=100, label=f"Tahmin: {prediction:.2f}")
        plt.title("🧠 Uyku Puanı Tahmin Eğrisi", fontsize=13, weight="bold")
        plt.xlabel("Gün")
        plt.ylabel("Puan (0–100)")
        plt.ylim(0, 110)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Rapor metni döndür
        report = (
            f"Yarınki Tahmini Uyku Puanı: {round(prediction, 2)} / 100\n"
            f"Model Güven Seviyesi (R²): %{confidence}\n"
            f"{trend}"
        )
        return report

    except Exception as e:
        return f"Tahmin hatası: {e}"
