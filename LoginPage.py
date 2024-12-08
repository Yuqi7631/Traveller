import tkinter as tk
from tkinter import messagebox, Frame
from tkinter import *
from MainPage import MainPage
from PIL import Image, ImageTk
import os
import csv
import hashlib
import binascii


class LoginPage(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("400x300")
        self.create_widgets()
        self.signup_file = "Signup.csv"
        self.init_file()

    def init_file(self):
        #Initialize the CSV file if it doesn't exist.
        if not os.path.exists(self.signup_file):
            with open(self.signup_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password"])

    def create_widgets(self):
        # Set background
        self.bg_image = Image.open("background.png")
        self.bg_image = self.bg_image.resize((400, 300), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = Canvas(self.master, width=400, height=300)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(200, 50, text="Traveller", font=("Arial", 20, "bold"), fill="white")

        self.username = StringVar()
        self.pwd = StringVar()
        
        self.canvas.create_text(80, 100, text="Username", font=("Arial", 10, "bold"), fill="black")
        self.canvas.create_text(80, 140, text="Password", font=("Arial", 10, "bold"), fill="black")
        

        self.entry1 = Entry(self.master, textvariable=self.username)
        self.entry2 = Entry(self.master, textvariable=self.pwd, show="*")
        self.canvas.create_window(230, 100, window=self.entry1, width=200, height=25)
        self.canvas.create_window(230, 140, window=self.entry2, width=200, height=25)

        self.button_login = Button(self.master, text="Login", command=self.login_check, font=("Arial", 12), relief="flat", bg="white", fg="black", highlightthickness=0, bd=0)
        self.canvas.create_window(200, 180, window=self.button_login, width=100, height=25)

        self.button_signup = Button(self.master, text="Sign up", command=self.signup, font=("Arial", 12), relief="flat", bg="white", fg="black", highlightthickness=0, bd=0)
        self.canvas.create_window(200, 220, window=self.button_signup, width=100, height=25)
        
        self.button_quit = Button(self.master, text="Quit", command=self.master.quit, font=("Arial", 12), relief="flat", bg="white", fg="black", highlightthickness=0, bd=0)
        self.canvas.create_window(200, 260, window=self.button_quit, width=100, height=25)
    
    def load_main_page(self):
        # 销毁登录窗口
        self.master.destroy()
        # 初始化 MainPage（独立窗口）
        main_page = MainPage()
        main_page.mainloop()

    def login_check(self):
        name = self.username.get()
        pwd = self.pwd.get()

        if not os.path.exists(self.signup_file):
            messagebox.showerror(title="Failed", message="Please Signup first!")
        with open(self.signup_file, mode='r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                if row[0] == name:
                        salt_store = row[1]
                        hex_salt_store = binascii.unhexlify(salt_store.encode())
                        pwd_store = row[2]
                        hashed_pwd_store = binascii.unhexlify(pwd_store.encode())
                        hashed_pwd = hashlib.pbkdf2_hmac('SHA-512', pwd.encode(), hex_salt_store, 100000)
                        if hashed_pwd == hashed_pwd_store:
                            self.master.withdraw()
                            self.load_main_page()
                        else:
                            messagebox.showerror(title="Failed", message="Wrong Password!" )
                            return
                else:
                    messagebox.showerror(title="Failed", message="Username not exists!")

    def signup(self):
        name = self.username.get().strip()
        pwd = self.pwd.get()

        with open(self.signup_file, mode='r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                if row[0] == name:
                    messagebox.showerror(title="Failed", message="Username already exists!")
                    return
        with open(self.signup_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            salt = os.urandom(16)
            salt_str = binascii.hexlify(salt).decode()
            hashed_pwd = hashlib.pbkdf2_hmac('SHA-512', pwd.encode(), salt, 100000)
            hashed_pwd_str = binascii.hexlify(hashed_pwd).decode()
            writer.writerow([name, salt_str, hashed_pwd_str])
            messagebox.showinfo(title="Congratulations!", message="Signup Successfully!")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Traveller")
    root.geometry("400x300+400+200")
    app = LoginPage(master=root)
    app.mainloop()