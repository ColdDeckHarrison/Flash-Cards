from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
current_card = {}


def new_word():
    seen_cards = []
    global current_card, flip_timer, to_learn
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(new_title, text="French", fill="black")
    canvas.itemconfig(current_word, text=current_card["French"], fill="black")
    canvas.itemconfig(background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)
    seen_cards += current_card


def flip_card():
    global current_card
    canvas.itemconfig(background, image=card_back)
    canvas.itemconfig(new_title, text="English", fill="white")
    canvas.itemconfig(current_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    new_word()


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("French Flash Cards")
flip_timer = window.after(3000, func=flip_card)


wrong = PhotoImage(file="./images/wrong.png")
correct = PhotoImage(file="./images/right.png")

canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_back = PhotoImage(file="./images/card_back.png")
card_front = PhotoImage(file="./images/card_front.png")
background = canvas.create_image(417, 280, image=card_front)
new_title = canvas.create_text(415, 175, text="", fill="black", font=("ariel", 40, "italic"))
current_word = word_in_french = canvas.create_text(415, 275, text="", fill="black", font=("ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_button = Button(image=wrong, bg=BACKGROUND_COLOR, highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=0)

correct_button = Button(image=correct, bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)
correct_button.grid(row=1, column=1)

new_word()

window.mainloop()
