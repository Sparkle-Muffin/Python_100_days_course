from pathlib import Path
from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json

BASE_DIR = Path(__file__).parent
padlock_img_path = BASE_DIR / "logo.png"
data_file_path = BASE_DIR / "data.json"
LABEL_FONT = ("Arial", 10, "normal")
ENTRY_FONT = ("Arial", 10, "normal")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    lowercases = string.ascii_lowercase
    uppercases = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

    lowercases_list = [random.choice(lowercases) for _ in range(nr_letters)]
    uppercases_list = [random.choice(uppercases) for _ in range(nr_letters)]
    digits_list = [random.choice(digits) for _ in range(nr_numbers)]
    punctuation_list = [random.choice(punctuation) for _ in range(nr_symbols)]
        
    letters_list = lowercases_list + uppercases_list
    letters_list_new = [random.choice(letters_list) for _ in range(nr_letters)]

    password_list = letters_list_new + digits_list + punctuation_list
    random.shuffle(password_list)
        
    password = "".join(password_list)
    pyperclip.copy(password)
    
    input_pass.delete(0, END)
    input_pass.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = input_website.get()
    email = input_email.get()
    password = input_pass.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="You've left some fields empty. Please fill them.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"You've entered:\nEmail: {email}\nPassword: {password}\nIs it OK to save?")

        if is_ok == True:
            input_website.delete(0, END)
            input_pass.delete(0, END)

            try:
                with open(data_file_path, mode="r") as file:
                    data = json.load(file)
            except(FileNotFoundError):
                with open(data_file_path, mode="w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                with open(data_file_path, mode="w") as file:
                    data.update(new_data)
                    json.dump(data, file, indent=4)

# ---------------------------- SEARCH DATABASE ------------------------------- #
def search_database():
    website = input_website.get()
    if len(website) == 0:
        messagebox.showerror(title="Database", message="Please enter a website.")
    else:
        try:
            with open(data_file_path, mode="r") as file:
                data = json.load(file)
        except(FileNotFoundError):
                messagebox.showerror(title="Database", message="Database is empty.")
        else:
            try:
                website_info = data[website]
                email = website_info["email"]
                password = website_info["password"]
                messagebox.showinfo(title=website, message=f"email: {email}\n password: {password}")
            except(KeyError):
                    messagebox.showerror(title="Database", message=f"No data about {website}.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
padlock_img = PhotoImage(file=padlock_img_path)
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(column=1, row=0)

######################  Website  ######################
label_website = Label(text="Website:", font=LABEL_FONT)
label_website.grid(column=0, row=1)

input_website = Entry(font=ENTRY_FONT, width=21)
input_website.grid(column=1, row=1, sticky=W)
input_website.focus()

button_website = Button(text="Search", font=LABEL_FONT, width=15, command=search_database)
button_website.grid(column=2, row=1)

######################  Email/Username  ######################
label_email = Label(text="Email/Username:", font=LABEL_FONT)
label_email.grid(column=0, row=2)

input_email = Entry(font=ENTRY_FONT, width=41)
input_email.grid(column=1, row=2, columnspan=2, sticky=W)
input_email.insert(0, "someemail@domain.com")

######################  Password  ######################
label_pass = Label(text="Password:", font=LABEL_FONT)
label_pass.grid(column=0, row=3)

input_pass = Entry(font=ENTRY_FONT, width=21)
input_pass.grid(column=1, row=3, sticky=W)

button_pass = Button(text="Generate Password", font=LABEL_FONT, width=15, command=generate_password)
button_pass.grid(column=2, row=3)

######################  Add  ######################
button_add = Button(text="Add", font=LABEL_FONT, width=37, command=save)
button_add.grid(column=1, row=4, columnspan=2)

mainloop()
