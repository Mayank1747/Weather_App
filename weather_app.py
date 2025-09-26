import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk

API_KEY = "c5e9ad18b58ff0f45a317c88bd648618"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        city_name = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['main'].lower()
        
        # Show text
        result_label.config(text=f"Weather in {city_name}\n"
                                 f"Temperature: {temperature}°C\n"
                                 f"Humidity: {humidity}%\n"
                                 f"Condition: {description.capitalize()}")
        
        # Only check for known icons
        supported_icons = ["clear", "clouds", "rain", "snow"]
        if description in supported_icons:
            icon_file = f"icons/{description}.png"
            try:
                icon_img = Image.open(icon_file).resize((80, 80))
                icon_tk = ImageTk.PhotoImage(icon_img)
                icon_label.config(image=icon_tk, text="")
                icon_label.image = icon_tk
            except:
                icon_label.config(image="", text="No icon available")
        else:
            icon_label.config(image="", text="No icon for this condition")
    else:
        messagebox.showerror("Error", "City not found or API error.")

# main window
root = tk.Tk()
root.title("Weather App")
root.geometry("350x350")
root.config(bg="#1e1e1e")

# Style settings
fg_color = "#ffffff"
btn_color = "#44475a"
entry_bg = "#2e2e2e"
font_style = ("Arial", 12)

# Input field
city_entry = tk.Entry(root, font=("Arial", 14), bg=entry_bg, fg=fg_color, insertbackground=fg_color)
city_entry.pack(pady=10)

# Button
get_weather_btn = tk.Button(root, text="Get Weather", font=font_style,
                            bg=btn_color, fg=fg_color, activebackground="#6272a4", command=get_weather)
get_weather_btn.pack(pady=5)

# Icon placeholder
icon_label = tk.Label(root, bg="#1e1e1e", fg=fg_color, font=font_style)
icon_label.pack(pady=10)

# Result label
result_label = tk.Label(root, font=font_style, justify="left", bg="#1e1e1e", fg=fg_color)
result_label.pack(pady=20)

root.mainloop()


