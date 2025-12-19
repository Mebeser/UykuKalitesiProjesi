# modules/visualizer.py
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def visualize_sleep(df, summary):
    plt.style.use('ggplot')
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))

    # --- 1️⃣ Günlük Uyku Süresi ---
    axs[0].plot(df['Tarih'], df['Uyku_Süresi_Saat'], 
                marker='o', linewidth=2.5, color='#1f77b4')
    axs[0].set_title('🛌 Günlük Uyku Süresi (saat)', fontsize=13, weight='bold', color='#333')
    axs[0].set_ylabel('Saat', fontsize=11)
    axs[0].grid(True, alpha=0.3)
    axs[0].tick_params(axis='x', rotation=30)

    # Ortalama çizgisi
    avg_sleep = df['Uyku_Süresi_Saat'].mean()
    axs[0].axhline(avg_sleep, color='orange', linestyle='--', linewidth=1.5, label=f'Ortalama: {avg_sleep:.1f} saat')
    axs[0].legend()

    # --- 2️⃣ Derin Uyku Oranı ---
    axs[1].bar(df['Tarih'], df['Derin_Uyku_Yüzdesi'], 
               color='#66b3ff', edgecolor='black', linewidth=0.7)
    axs[1].set_title('💤 Derin Uyku Oranı (%)', fontsize=13, weight='bold', color='#333')
    axs[1].set_ylabel('Yüzde (%)', fontsize=11)
    axs[1].yaxis.set_major_formatter(mtick.PercentFormatter())
    axs[1].tick_params(axis='x', rotation=30)

    # --- Genel başlık ---
    fig.suptitle(
        f"🌙 Genel Uyku Puanı: {summary['uyku_puani']} / 100\n"
        f"En iyi gün: {summary['en_iyi_gun']} | En kötü gün: {summary['en_kotu_gun']}",
        fontsize=14, weight='bold', color='#2e4053', y=0.98
    )

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.show()
