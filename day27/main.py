from tkinter import *

PADDING_X = 10
PADDING_Y = 13
FONT = ("Arial", 25, "bold")

window = Tk()
# window.minsize(width=600, height=400)
window.title("Mile to Kilometer Converter")
window.config(padx=PADDING_X, pady=PADDING_Y)

input = Entry(width=10)
input.grid(column=1, row=0)
input.config(font=FONT)

label_miles = Label(window, text="Miles")
label_miles.grid(column=2, row=0)
label_miles.config(padx=PADDING_X, pady=PADDING_Y, font=FONT)

label_is_equal = Label(window, text="is equal to")
label_is_equal.grid(column=0, row=1)
label_is_equal.config(padx=PADDING_X, pady=PADDING_Y)
label_is_equal.config(padx=PADDING_X, pady=PADDING_Y, font=FONT)

label_result = Label(window, text="")
label_result.grid(column=1, row=1)
label_result.config(padx=PADDING_X, pady=PADDING_Y)
label_result.config(padx=PADDING_X, pady=PADDING_Y, font=FONT)

label_kilometers = Label(window, text="Kilometers")
label_kilometers.grid(column=2, row=1)
label_kilometers.config(padx=PADDING_X, pady=PADDING_Y)
label_kilometers.config(padx=PADDING_X, pady=PADDING_Y, font=FONT)

input_string = StringVar()
def button_clicked():
    label_text = input.get()
    miles = float(label_text)
    kilometers = round((miles * 1.609344), 2)
    label_result.config(text=str(kilometers))

button = Button(window, text="Calculate", command=button_clicked)
button.grid(column=1, row=2)
button.config(padx=PADDING_X, pady=PADDING_Y)
button.config(padx=PADDING_X, pady=PADDING_Y, font=FONT)


mainloop()
