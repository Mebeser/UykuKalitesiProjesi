![Python](https://img.shields.io/badge/Python-3.9-blue)
![Pandas](https://img.shields.io/badge/Pandas-Used%20Library-orange)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-yellow)
![MachineLearning](https://img.shields.io/badge/Machine%20Learning-Enabled-success)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)


# 🌙 Uyku Kalitesi Analiz ve Görselleştirme Aracı

Bu proje, kullanıcıların uyku alışkanlıklarını analiz etmek, istatistiksel olarak değerlendirmek ve görselleştirmek amacıyla geliştirilmiş bir **Python tabanlı analiz uygulamasıdır**.  
Proje, veri analizi, etkileşimli görselleştirme, ve simülasyon tekniklerini birleştirerek kullanıcıya akıllı bir deneyim sunar.

---

## 🧩 Özellikler

✅ **Akıllı veri girişi:**  
Kullanıcı yalnızca `Tarih`, `Uyuma Saati`, ve `Uyanma Saati` bilgilerini girer.  
Sistem otomatik olarak:
- Uyku süresini hesaplar (saat cinsinden)
- Derin uyku yüzdesini tahmin eder (matematiksel model ile)

✅ **İstatistiksel analiz (Pandas + NumPy):**
- Ortalama uyku süresi  
- Ortalama derin uyku oranı  
- Uyku düzeni (standart sapma)  
- En iyi / en kötü günler  
- Genel “Uyku Puanı” (0–100 arası)

✅ **Etkileşimli görselleştirme (Matplotlib):**
- Günlük uyku süresi çizgi grafiği  
- Derin uyku yüzdesi sütun grafiği  
- Dinamik olarak güncellenen dashboard

✅ **Görsel geri bildirim (Turtle):**
- Uyku puanına göre yüz ifadeleri (mutlu, nötr, yorgun)

✅ **Sinematik uyku simülasyonu:**
- Gerçek zamanlı uyku dalgaları  
- Gün doğumu efektiyle arka plan rengi değişimi  
- Ambiyans sesi (white noise / doğa sesi)

---

## 🧠 Uyku Puanı Hesaplama

Sistem, uyku verilerini analiz ederek kullanıcının genel puanını hesaplar:

\[
Uyku Puanı = (Ortalama Süre × 10) + (Derin Uyku × 2) - (Düzensizlik × 5)
\]

Puan aralıkları:
| Aralık | Anlamı |
|--------|--------|
| 80–100 | Mükemmel uyku düzeni 😴 |
| 50–79  | Orta kalitede uyku |
| 0–49   | Düzensiz uyku – iyileştirme önerilir |

---

## 🧮 Derin Uyku Yüzdesi Tahmini

Uyku süresine bağlı olarak sistem, derin uyku oranını otomatik tahmin eder:

| Uyku Süresi | Derin Uyku (%) |
|--------------|----------------|
| < 4 saat | 10–15% |
| 4–8 saat | 25–40% |
| > 8 saat | 25–30% |

Formül:
\[
\text{Derin Uyku} = 
\begin{cases} 
10 + s×2 & s < 4 \\
20 + (s-4)×5 & 4 ≤ s ≤ 8 \\
40 - (s-8)×3 & s > 8
\end{cases}
\]

---

## 🧱 Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|------------|----------------|
| **Python** | Ana programlama dili |
| **Tkinter** | GUI (grafik arayüz) |
| **Pandas, NumPy** | Veri analizi ve istatistik |
| **Matplotlib** | Grafik görselleştirme |
| **Turtle** | Görsel geri bildirim ve simülasyon |
| **playsound** | Ambiyans sesleri |
| **datetime** | Zaman hesaplamaları |

---

## 🚀 Kurulum

### 1️⃣ Gerekli kütüphaneleri yükle:
```bash
pip install pandas numpy matplotlib playsound
