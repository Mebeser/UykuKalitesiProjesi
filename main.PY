# main.py — Uyku Kalitesi Analiz Aracı v3.1 (Yeni Gün Ekleme + Dashboard)
import tkinter as tk
from tkinter import filedialog, messagebox
from modules.analyzer import analyze_sleep_data
from modules.turtle_display import show_sleep_feedback
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import os
from modules.simulation import sleep_simulation
from modules.predictor import predict_next_score


root = tk.Tk()
root.title("🌙 Uyku Kalitesi Analiz ve Görselleştirme Aracı")
root.state('zoomed')
root.configure(bg="#f0f4f7")

# Global değişkenler
df, summary = None, None
canvas_widget = None
current_file = None

# Üst Başlık
header = tk.Label(root, text="Uyku Kalitesi Analiz Aracı 😴",
                  font=("Segoe UI", 20, "bold"), bg="#2e4053", fg="white", pady=10)
header.pack(fill="x")

# Ana çerçeve
frame = tk.Frame(root, bg="#f0f4f7", padx=30, pady=20)
frame.pack(fill="both", expand=True)

# Sol panel
left_panel = tk.Frame(frame, bg="#f0f4f7")
left_panel.pack(side="left", fill="y", padx=20)

result_text = tk.StringVar(value="Henüz veri yüklenmedi.")
btn_style = {
    "font": ("Segoe UI", 11, "bold"),
    "bg": "#3498db",
    "fg": "white",
    "activebackground": "#2e86c1",
    "activeforeground": "white",
    "relief": "flat",
    "width": 25,
    "pady": 8
}

def load_and_analyze():
    global df, summary, canvas_widget, current_file
    file_path = filedialog.askopenfilename(
        title="Uyku verisi CSV dosyasını seç",
        filetypes=[("CSV files", "*.csv")]
    )
    if not file_path:
        return
    try:
        current_file = file_path
        df, summary = analyze_sleep_data(file_path)
        update_summary_text()
        messagebox.showinfo("Başarılı", "Veri başarıyla analiz edildi.")
        draw_graph()
    except Exception as e:
        messagebox.showerror("Hata", str(e))

def update_summary_text():
    global summary
    result_text.set(
        f"📅 En iyi gün: {summary['en_iyi_gun']}\n"
        f"😴 Ortalama uyku: {summary['ortalama_uyku']} saat\n"
        f"💤 Derin uyku ort.: %{summary['ortalama_derin']}\n"
        f"📊 Uyku puanı: {summary['uyku_puani']}\n"
        f"📉 Sapma: {summary['std_sapma']}"
    )

def draw_graph():
    global df, summary, canvas_widget
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

    plt.style.use('ggplot')
    fig, axs = plt.subplots(2, 1, figsize=(8, 5))

    axs[0].plot(df['Tarih'], df['Uyku_Süresi_Saat'], marker='o', linewidth=2.5, color='#1f77b4')
    axs[0].set_title('🛌 Günlük Uyku Süresi (saat)', fontsize=12, weight='bold', color='#333')
    axs[0].axhline(df['Uyku_Süresi_Saat'].mean(), color='orange', linestyle='--', linewidth=1.5)
    axs[0].tick_params(axis='x', rotation=30)

    axs[1].bar(df['Tarih'], df['Derin_Uyku_Yüzdesi'], color='#66b3ff', edgecolor='black', linewidth=0.7)
    axs[1].set_title('💤 Derin Uyku Oranı (%)', fontsize=12, weight='bold', color='#333')
    axs[1].tick_params(axis='x', rotation=30)

    fig.suptitle(f"🌙 Genel Uyku Puanı: {summary['uyku_puani']} / 100",
                 fontsize=13, weight='bold', color='#2e4053', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92])

    canvas_widget = FigureCanvasTkAgg(fig, master=right_panel)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(fill="both", expand=True, pady=10)

def show_turtle():
    if summary is None:
        messagebox.showwarning("Uyarı", "Önce veriyi analiz edin!")
        return
    show_sleep_feedback(summary['uyku_puani'])

def start_simulation():
    if summary is None:
        messagebox.showwarning("Uyarı", "Önce veriyi analiz edin!")
        return
    sleep_simulation(summary['uyku_puani'])


# 🆕 Yeni Gün Ekle Penceresi
# --- 🆕 Yeni Gün Ekle (Akıllı Versiyon) ---
from datetime import datetime, timedelta
import pandas as pd
import os
from tkinter import messagebox

def open_add_entry_window():
    if not current_file:
        messagebox.showwarning("Uyarı", "Önce bir CSV dosyası yükleyin!")
        return

    add_win = tk.Toplevel(root)
    add_win.title("🆕 Yeni Gün Ekle (Akıllı Giriş)")
    add_win.geometry("400x380")
    add_win.config(bg="#ecf0f1")

    tk.Label(add_win, text="Yeni Uyku Verisi Ekle", font=("Segoe UI", 14, "bold"), bg="#ecf0f1").pack(pady=10)

    entries = {}
    fields = ["Tarih (YYYY-MM-DD)", "Uyuma Saati (HH:MM)", "Uyanma Saati (HH:MM)"]
    for f in fields:
        tk.Label(add_win, text=f, bg="#ecf0f1", font=("Segoe UI", 10, "bold")).pack(pady=5)
        e = tk.Entry(add_win, width=25, font=("Consolas", 10))
        e.pack()
        entries[f] = e

    def save_entry():
        try:
            tarih = entries[fields[0]].get().strip()
            uyuma_saati = entries[fields[1]].get().strip()
            uyanma_saati = entries[fields[2]].get().strip()

            # 🕒 Uyku süresini hesapla
            fmt = "%H:%M"
            uyuma = datetime.strptime(uyuma_saati, fmt)
            uyanma = datetime.strptime(uyanma_saati, fmt)
            if uyanma < uyuma:
                uyanma += timedelta(days=1)
            uyku_suresi = round((uyanma - uyuma).total_seconds() / 3600, 2)

            # 💡 Derin uyku yüzdesini otomatik tahmin et
            if uyku_suresi < 4:
                derin_yuzde = 10 + uyku_suresi * 2
            elif uyku_suresi <= 8:
                derin_yuzde = 20 + (uyku_suresi - 4) * 5
            else:
                derin_yuzde = 40 - (uyku_suresi - 8) * 3
            derin_yuzde = max(5, min(derin_yuzde, 45))

            new_data = {
                "Tarih": tarih,
                "Uyku_Süresi_Saat": uyku_suresi,
                "Derin_Uyku_Yüzdesi": round(derin_yuzde, 1),
                "Uyuma_Saati": uyuma_saati,
                "Uyanma_Saati": uyanma_saati
            }

            # CSV’ye ekle
            if os.path.exists(current_file):
                df_existing = pd.read_csv(current_file)
                df_updated = pd.concat([df_existing, pd.DataFrame([new_data])], ignore_index=True)
                df_updated.to_csv(current_file, index=False)
            else:
                pd.DataFrame([new_data]).to_csv(current_file, index=False)

            messagebox.showinfo("Başarılı", f"Yeni veri eklendi!\nUyku Süresi: {uyku_suresi} saat\nDerin Uyku: %{round(derin_yuzde,1)}")
            add_win.destroy()

            # Yeniden analiz ve grafik güncelle
            global df, summary
            df, summary = analyze_sleep_data(current_file)
            update_summary_text()
            draw_graph()

        except Exception as e:
            messagebox.showerror("Hata", f"Veri eklenemedi: {str(e)}")




    tk.Button(
        add_win,
        text="💾 Kaydet",
        command=save_entry,
        bg="#27ae60",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        pady=5,
        width=15
    ).pack(pady=15)

def show_prediction():
    if not current_file:
        messagebox.showwarning("Uyarı", "Önce bir CSV yükleyin!")
        return
    result = predict_next_score(current_file)
    if "Yeterli veri" in result or "hata" in result:
        messagebox.showwarning("Makine Öğrenmesi", result)
    else:
        messagebox.showinfo("Makine Öğrenmesi Tahmini", result)

# --- Butonlar ---
tk.Button(left_panel, text="📂 Veriyi Yükle ve Analiz Et", command=load_and_analyze, **btn_style).pack(pady=10)
tk.Button(left_panel, text="📈 Grafiği Göster", command=draw_graph, **btn_style).pack(pady=10)
tk.Button(left_panel, text="🆕 Yeni Gün Ekle", command=open_add_entry_window, **btn_style).pack(pady=10)
tk.Button(left_panel, text="🐢 Turtle İfadesi", command=show_turtle, **btn_style).pack(pady=10)
tk.Button(left_panel, text="🌙 Uyku Simülasyonu", command=start_simulation, **btn_style).pack(pady=10)
tk.Button(left_panel, text="🧠 ML Tahmini", command=lambda: show_prediction(), **btn_style).pack(pady=10)


# Sonuç etiketi
tk.Label(left_panel, textvariable=result_text, justify="left", bg="#f0f4f7", font=("Consolas", 10)).pack(pady=30)

# Sağ panel (grafik alanı)
right_panel = tk.Frame(frame, bg="white", relief="groove", bd=2)
right_panel.pack(side="right", fill="both", expand=True, padx=10)

footer = tk.Label(root, text="© 2025 Uyku Analiz Projesi | Profesyonel Sürüm",
                  bg="#2e4053", fg="white", font=("Segoe UI", 9))
footer.pack(fill="x", side="bottom")

import sys

def on_close():
    root.destroy()
    sys.exit()  # Python işlemini tamamen sonlandır

root.protocol("WM_DELETE_WINDOW", on_close)



root.mainloop()
