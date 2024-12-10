import tkinter as tk
from tkinter import messagebox, ttk, Frame
from tkinter import *
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.cm as cm
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
        """Initialize the CSV file if it doesn't exist."""
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

        self.canvas.create_text(
            400, 100, text="Record Expense", font=("Arial", 20, "bold"), fill="white"
        )

        # Labels and Entry
        self.canvas.create_text(
            220, 200, text="Date (YYYY-MM-DD)", font=("Arial", 15, "bold"), fill="black"
        )
        self.date_entry = Entry(self)
        self.canvas.create_window(
            540, 200, window=self.date_entry, width=280, height=40
        )

        self.canvas.create_text(
            220, 280, text="Category", font=("Arial", 15, "bold"), fill="black"
        )
        self.category_entry = ttk.Combobox(
            self, values=["Food", "Transport", "Accommodation", "Tickets", "Other"]
        )
        self.canvas.create_window(
            540, 280, window=self.category_entry, width=280, height=40
        )

        self.canvas.create_text(
            220, 360, text="Amount", font=("Arial", 15, "bold"), fill="black"
        )
        self.amount_entry = Entry(self)
        self.canvas.create_window(
            540, 360, window=self.amount_entry, width=280, height=40
        )

        # Buttons
        self.add_exp_button = Button(
            self,
            text="Add Expense",
            command=self.add_expense,
            font=("Arial", 15),
            relief="flat",
            bg="white",
            fg="black",
            highlightthickness=10,
            bd=0,
        )
        self.canvas.create_window(
            400, 460, window=self.add_exp_button, width=200, height=50
        )

        self.view_sum_button = Button(
            self,
            text="View Summary",
            command=self.show_summary,
            font=("Arial", 15),
            relief="flat",
            bg="white",
            fg="black",
            highlightthickness=10,
            bd=0,
        )
        self.canvas.create_window(
            400, 540, window=self.view_sum_button, width=200, height=50
        )

        # Return to Mainpage
        self.return_mainpage_img = ImageTk.PhotoImage(
            Image.open("Return.png").resize((80, 80))
        )
        return_mainpage = self.canvas.create_image(
            700, 550, image=self.return_mainpage_img, anchor="center"
        )
        self.canvas.tag_bind(
            return_mainpage, "<Button-1>", lambda event: self.return_to_main()
        )

    def add_expense(self):
        """Save expense details to the CSV file."""
        date = self.date_entry.get().strip()
        category = self.category_entry.get().strip()
        amount = self.amount_entry.get().strip()

        # Validation
        if not date or not category or not amount:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        if len(date) != 10:
            messagebox.showerror(
                "Input Error", "Please enter the date in the correct format."
            )
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
        """Clear input fields."""
        self.category_entry.set("")
        self.amount_entry.delete(0, tk.END)

    def show_summary(self):
        """Display expense summary as a stacked bar chart."""
        data = self.read_expenses()
        if not data:
            messagebox.showinfo("No Data", "No expenses recorded yet.")
            return

        # Group data by date and category
        grouped_data = defaultdict(lambda: defaultdict(float))
        for record in data:
            date = record[0]
            category = record[1]
            amount = float(record[2])
            grouped_data[date][category] += amount

        # Prepare data for the plot
        dates = sorted(grouped_data.keys())
        categories = sorted({cat for date in grouped_data.values() for cat in date})
        amounts_by_category = {
            cat: [grouped_data[date].get(cat, 0) for date in dates]
            for cat in categories
        }

        # Create stacked bar chart
        plt.figure(figsize=(10, 6))
        # Initialize the bottom of the stack
        bottom = [0] * len(dates)
        colors = cm.Pastel1(range(len(categories)))

        for i, category in enumerate(categories):
            plt.bar(
                dates,
                amounts_by_category[category],
                bottom=bottom,
                label=category,
                color=colors[i],
            )
            bottom = [b + a for b, a in zip(bottom, amounts_by_category[category])]

        # Add labels and legend
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Expense Summary (Stacked by Category)")
        plt.xticks(rotation=45, ha="right")
        plt.legend(title="Category", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        plt.show()

    def read_expenses(self):
        """Read expenses from the CSV file."""
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
