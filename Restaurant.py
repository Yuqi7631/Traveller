import tkinter as tk
from tkinter import Frame
from tkinter import *
from PIL import Image, ImageTk
import API


class Restaurant(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.restaurant_result = tk.StringVar()  # Define as instance variable
        self.bg_photo = None
        self.create_widgets()

    def create_widgets(self):
        # Set background
        self.canvas = Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = Image.open("background_blur.png")
        self.bg_image = self.bg_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(
            400, 100, text="Restaurants", font=("Arial", 20, "bold"), fill="white"
        )

        # Show restaurants result
        self.restaurant_frame = Frame(self)
        self.restaurant_frame.place(x=150, y=150, width=500, height=300)

        self.result_text = Text(
            self.restaurant_frame,
            wrap=tk.WORD,
            bg="white",
            font=("Arial", 12),
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(
            self.restaurant_frame, orient=tk.VERTICAL, command=self.result_text.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind scrollbar to text widget
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        self.search_button = Button(
            self, text="Find Restaurants", command=self.fetch_restaurant
        )
        self.canvas.create_window(
            400, 530, window=self.search_button, width=200, height=40
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

    def fetch_restaurant(self):
        """Get current location to find near restaurants"""
        self.search_button.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, "Searching for restaurants...\n")
        self.update_idletasks()

        try:
            lat, lon = API.get_user_location()
            if lat is None or lon is None:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(
                    tk.END, "Error: Could not determine your location.\n"
                )
                return
            restaurants = API.find_restaurants(lat, lon)
            if not restaurants:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "No restaurants found nearby.\n")
            else:
                self.result_text.delete(1.0, tk.END)
                for i, (name, address, rating) in enumerate(restaurants):
                    self.result_text.insert(
                        tk.END, f"{i + 1}. {name}\n   {address} (Rating: {rating})\n\n"
                    )

        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Query Failed: {e}\n")
        finally:
            self.search_button.config(state=tk.NORMAL)

    def return_to_main(self):
        """Return to the MainPage"""
        self.master.show_main_page()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Traveller")
    root.geometry("800x600+400+200")
    app = Restaurant(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()
