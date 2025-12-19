# modules/simulation.py — Sinematik Uyku Simülasyonu (ışık + ses efektli)
import turtle
import time
import math
import colorsys
from threading import Thread
from playsound import playsound

def play_ambient_sound():
    try:
        playsound("sounds/ambient.mp3")
    except Exception as e:
        print("Ses çalma hatası:", e)

def sleep_simulation(sleep_score):
    turtle.clearscreen()
    screen = turtle.Screen()
    screen.title("🌙 Uyku Derinliği Simülasyonu")

    wave = turtle.Turtle()
    wave.hideturtle()
    wave.speed(0)
    wave.pensize(3)

    # Uyku kalitesine göre parametreler
    if sleep_score >= 80:
        mood = "Derin ve dinlendirici uyku"
        hue_speed = 0.002
        amplitude = 50
        delay = 0.02
    elif sleep_score >= 50:
        mood = "Orta kalitede uyku"
        hue_speed = 0.004
        amplitude = 70
        delay = 0.015
    else:
        mood = "Düzensiz uyku"
        hue_speed = 0.006
        amplitude = 90
        delay = 0.01

    # Başlık
    title = turtle.Turtle()
    title.hideturtle()
    title.color("white")
    title.penup()
    title.goto(0, 230)
    title.write(f"{mood} ({sleep_score}/100)", align="center", font=("Arial", 16, "bold"))

    screen.tracer(0)
    hue = 0

    # 🔊 Arka planda ses başlat (thread)
    Thread(target=play_ambient_sound, daemon=True).start()

    for frame in range(300):
        # 🔸 Arka plan: gece → sabah geçişi
        r = int(5 + frame * 0.6)
        g = int(5 + frame * 0.4)
        b = int(15 + frame * 0.25)
        r, g, b = min(r, 255), min(g, 180), min(b, 160)
        screen.bgcolor(r / 255, g / 255, b / 255)

        # 🔹 Dalga çizimi
        wave.clear()
        wave.penup()
        wave.goto(-300, 0)
        wave.pendown()

        hue += hue_speed
        if hue > 1:
            hue = 0
        col = colorsys.hsv_to_rgb(hue, 0.8, 1)
        wave.pencolor(col)

        for x in range(-300, 300):
            y = math.sin((x + frame * 4) * math.pi / 90) * amplitude
            wave.goto(x, y)

        screen.update()
        time.sleep(delay)

    # 🌅 Gün doğumu sahnesi
    wave.clear()
    title.clear()
    screen.bgcolor("#ffcf88")
    title.color("#2e4053")
    title.goto(0, 0)
    title.write("🌞 Yeni bir güne uyanma zamanı", align="center", font=("Arial", 18, "bold"))
    time.sleep(3)
    turtle.done()
