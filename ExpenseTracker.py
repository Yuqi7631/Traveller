import tkinter as tk
from tkinter import messagebox, ttk, Frame
from tkinter import *
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import csv
import os


class ExpenseTracker(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.expenses_file = "expenses.csv"
        self.init_file()
        self.create_widgets()

    def init_file(self):
        #Initialize the CSV file if it doesn't exist.
        if not os.path.exists(self.expenses_file):
            with open(self.expenses_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount"])
    
    def create_widgets(self):
        # Set background
        self.canvas = Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = Image.open("background_blur.png")
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(400, 100, text="Record Expense", font=("Arial", 20, "bold"), fill="white")

        # Labels and Entry
        self.canvas.create_text(220, 200, text="Date (YYYY-MM-DD)", font=("Arial", 15, "bold"), fill="black")
        self.date_entry = Entry(self)
        self.canvas.create_window(540, 200, window=self.date_entry, width=280, height=40)
        

        self.canvas.create_text(220, 280, text="Category", font=("Arial", 15, "bold"), fill="black")
        self.category_entry = ttk.Combobox(self, values=["Food", "Transport", "Accommodation", "Tickets", "Other"])
        self.canvas.create_window(540, 280, window=self.category_entry, width=280, height=40)

        self.canvas.create_text(220, 360, text="Amount", font=("Arial", 15, "bold"), fill="black")
        self.amount_entry = Entry(self)
        self.canvas.create_window(540, 360, window=self.amount_entry, width=280, height=40)
        
        # Buttons
        self.add_exp_button = Button(self, text="Add Expense", command=self.add_expense, font=("Arial", 15), relief="flat", bg="white", fg="black", highlightthickness=10, bd=0)
        self.canvas.create_window(400, 460, window=self.add_exp_button, width=200, height=50)

        self.view_sum_button = Button(self, text="View Summary", command=self.show_summary, font=("Arial", 15), relief="flat", bg="white", fg="black", highlightthickness=10, bd=0)
        self.canvas.create_window(400, 540, window=self.view_sum_button, width=200, height=50)
        
        # Return to Mainpage
        self.return_mainpage_img = ImageTk.PhotoImage(Image.open("Return.png").resize((80, 80)))
        return_mainpage = self.canvas.create_image(700, 550, image=self.return_mainpage_img, anchor="center")
        self.canvas.tag_bind(return_mainpage, "<Button-1>", lambda event: self.return_to_main())


    def add_expense(self):
        # Save expense details to the CSV file.
        date = self.date_entry.get().strip()
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()

        # Validation
        if not date or not category or not amount:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        if not amount.isdigit():
            messagebox.showerror("Input Error", "Amount must be a number.")
            return
        
        # Save to file
        with open(self.expenses_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, float(amount)])
        
        messagebox.showinfo("Success", "Expense added successfully!")
        self.clear_entries()

    def clear_entries(self):
        # Clear input fields.
        self.date_entry.delete(0, tk.END)
        self.category_entry.set("")
        self.amount_entry.delete(0, tk.END)

    def show_summary(self):
        # Display expense summary as a bar chart.
        data = self.read_expenses()
        if not data:
            messagebox.showinfo("No Data", "No expenses recorded yet.")
            return
        
        # Group by category
        category_totals = {}
        for record in data:
            category = record[1]
            amount = float(record[2])
            category_totals[category] = category_totals.get(category, 0) + amount
        
        # Plot bar chart
        categories = list(category_totals.keys())
        totals = list(category_totals.values())
        
        plt.figure(figsize=(8, 6))
        plt.bar(categories, totals, color='skyblue')
        plt.xlabel("Category")
        plt.ylabel("Total Amount")
        plt.title("Expense Summary")
        plt.show()

    def read_expenses(self):
        #Read expenses from the CSV file.
        if not os.path.exists(self.expenses_file):
            return []
        with open(self.expenses_file, "r") as file:
            reader = csv.reader(file)
            next(reader)  
            return list(reader)
    
    def return_to_main(self):
        self.master.show_main_page()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Daily Expense Tracker")
    root.geometry("800x600")
    app = ExpenseTracker(master=root)
    app.pack(fill="both", expand=True)
    app.mainloop()
