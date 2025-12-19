# modules/turtle_display.py
import turtle

def show_sleep_feedback(score):
    turtle.clearscreen()
    t = turtle.Turtle()
    t.speed(0)
    t.width(5)
    
    # Renk ve ifade seçimi
    if score >= 80:
        color, mood = "green", "mutlu"
    elif score >= 50:
        color, mood = "orange", "normal"
    else:
        color, mood = "red", "yorgun"
    
    t.color(color)
    t.penup()
    t.goto(0, -100)
    t.pendown()
    
    # Yüz çemberi
    t.circle(100)
    
    # Gözler
    for x in [-35, 35]:
        t.penup()
        t.goto(x, 30)
        t.pendown()
        t.circle(10)
    
    # Ağız (ifade)
    t.penup()
    t.goto(-40, -30)
    t.pendown()
    if mood == "mutlu":
        t.setheading(-60)
        t.circle(50, 120)
    elif mood == "normal":
        t.forward(80)
    else:
        t.setheading(60)
        t.circle(-50, 120)
    
    t.hideturtle()
    turtle.done()
