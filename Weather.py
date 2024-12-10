import tkinter as tk
from tkinter import messagebox, Frame
from tkinter import *
from PIL import Image, ImageTk
import API


class Weather(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.weather_result = tk.StringVar()  # Define as instance variable
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
            400, 100, text="Today's weather", font=("Arial", 20, "bold"), fill="white"
        )

        # Labels and Entry
        self.canvas.create_text(
            280, 170, text="City Name", font=("Arial", 15, "bold"), fill="black"
        )
        self.city_entry = Entry(self, width=30)
        self.canvas.create_window(
            520, 170, window=self.city_entry, width=200, height=40
        )

        self.canvas.create_text(
            280, 220, text="Country Name", font=("Arial", 15, "bold"), fill="black"
        )
        self.country_entry = Entry(self, width=30)
        self.canvas.create_window(
            520, 220, window=self.country_entry, width=200, height=40
        )

        self.search_button = Button(
            self,
            text="Query Weather",
            command=lambda: self.fetch_weather(
                self.city_entry.get().strip(), self.country_entry.get().strip()
            ),
        )
        self.canvas.create_window(
            400, 290, window=self.search_button, width=200, height=40
        )

        self.location_button = Button(
            self,
            text="Get Weather for Current Location",
            command=lambda: self.fetch_weather(),
        )
        self.canvas.create_window(
            400, 350, window=self.location_button, width=200, height=40
        )

        self.weather_label = Label(
            self,
            textvariable=self.weather_result,
            justify="left",
            anchor="w",
            bg="white",
        )
        self.canvas.create_window(
            400, 480, window=self.weather_label, width=500, height=180
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

    def fetch_weather(self, city=None, country=None):
        """Fetch weather data for the user's input or current location"""
        if city is None:
            city, country = API.get_location()
            if country in ["United States", "USA"]:
                country = "United States of America"
            if city is None:
                messagebox.showerror("Error", "Unable to detect location.")
                return
            messagebox.showinfo(
                "Location Detected", f"Detected location: {city}, {country}"
            )
        try:
            self.display_weather(city, country)
        except Exception as e:
            messagebox.showerror("Query Failed", f"Unable to fetch weather data: {e}")

    def display_weather(self, city, country):
        """Fetch weather data from API and display it in the GUI"""
        # Fetch data from API
        location = f"{city},{country}"
        data = API.fetch_weather_data(location)

        # Parse data
        city = data["location"]["name"]
        country = data["location"]["country"]
        localtime = data["location"]["localtime"]
        condition = data["current"]["condition"]["text"]
        temp_c = data["current"]["temp_c"]
        feelslike_c = data["current"]["feelslike_c"]
        wind_kph = data["current"]["wind_kph"]
        humidity = data["current"]["humidity"]

        # Update the result display
        self.weather_result.set(
            f"City: {city}, {country}\n"
            f"Local Time: {localtime}\n"
            f"Condition: {condition}\n"
            f"Temperature: {temp_c}°C\n"
            f"Feels Like: {feelslike_c}°C\n"
            f"Wind Speed: {wind_kph} km/h\n"
            f"Humidity: {humidity}%"
        )

    def return_to_main(self):
        self.master.show_main_page()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Traveller")
    root.geometry("800x600+400+200")
    app = Weather(master=root)
    app.pack(fill="both", expand=True)  # Pack Weather into the root
    root.mainloop()
