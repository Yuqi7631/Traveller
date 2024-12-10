import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
from Weather import Weather
from ExpenseTracker import ExpenseTracker
from Restaurant import Restaurant


class MainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traveller")
        self.geometry("800x600")

        self.current_page = None

        self.create_widgets()

    def create_widgets(self):
        # Set background
        self.canvas = Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = Image.open("background_blur.png")
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.logo_img = ImageTk.PhotoImage(Image.open("Logo.png").resize((200, 200)))
        self.canvas.create_image(400, 150, image=self.logo_img, anchor="center")

        self.canvas.create_text(
            400,
            280,
            text="Welcome to Traveller!",
            font=("Arial", 30, "bold"),
            fill="black",
        )

        # Images
        self.weather_img = ImageTk.PhotoImage(
            Image.open("Weather.png").resize((200, 200))
        )
        self.expense_img = ImageTk.PhotoImage(
            Image.open("Expense.png").resize((200, 200))
        )
        self.restaurant_img = ImageTk.PhotoImage(
            Image.open("Restaurant.png").resize((200, 200))
        )

        weather_btn = self.canvas.create_image(
            200, 400, image=self.weather_img, anchor="center"
        )
        expense_btn = self.canvas.create_image(
            400, 400, image=self.expense_img, anchor="center"
        )
        restaurant_btn = self.canvas.create_image(
            600, 400, image=self.restaurant_img, anchor="center"
        )

        self.canvas.tag_bind(
            weather_btn, "<Button-1>", lambda event: self.show_weather()
        )
        self.canvas.tag_bind(
            expense_btn, "<Button-1>", lambda event: self.show_expense()
        )
        self.canvas.tag_bind(
            restaurant_btn, "<Button-1>", lambda event: self.show_restaurant()
        )

        self.canvas.create_text(
            400, 470, text="Record Expense", font=("Arial", 18, "bold"), fill="black"
        )
        self.canvas.create_text(
            200, 470, text="Weather", font=("Arial", 18, "bold"), fill="black"
        )
        self.canvas.create_text(
            600, 470, text="Restaurant", font=("Arial", 18, "bold"), fill="black"
        )

    def show_weather(self):
        """Show Weather page"""
        self.destroy_current_page()
        self.current_page = Weather(master=self)
        self.current_page.place(x=0, y=0, width=800, height=600)

    def show_expense(self):
        """Show Expense page"""
        self.destroy_current_page()
        self.current_page = ExpenseTracker(master=self)
        self.current_page.place(x=0, y=0, width=800, height=600)

    def show_restaurant(self):
        """Show Restaurant page"""
        self.destroy_current_page()
        self.current_page = Restaurant(master=self)
        self.current_page.place(x=0, y=0, width=800, height=600)

    def destroy_current_page(self):
        """Destroy current page to a show new page"""
        if self.current_page:
            self.current_page.destroy()
            self.current_page = None

    def show_main_page(self):
        """Show a new page"""
        self.destroy_current_page()
        self.canvas.pack()


if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
