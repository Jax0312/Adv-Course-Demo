import datetime
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests

# Fetch weather info
try:
    url = 'https://api.open-meteo.com/v1/forecast?latitude=4.2105&longitude=101.9758&hourly=temperature_2m,weather_code&forecast_days=1'
    data = requests.get(url).json()
except:
    messagebox.Message(message="Could not fetch weather info").show()
    exit()
    

# Convert weather code to image name
def get_image_name(code):
    if 0 <= code <= 29:
        return "sunny.jpg"
    elif 30 <= code <= 39:
        return "dust.jpg"
    elif 40 <= code <= 49:
        return "fog.jpg"
    elif 50 <= code <= 69:
        return "rain.jpg"
    elif 70 <= code <= 79:
        return "snow.jpg"
    elif 80 <= code <= 89:
        return "storm.jpg"

# Handle next button event
def next_result():
    global index
    index += 1
    if index > 23:
        index = 0
    display_bg()
    display_time()

# Handle previous button event
def prev_result():
    global index
    index -= 1
    if index < 0:
        index = 23
    display_bg()
    display_time()

# Update time and temperature
def display_time():
    global index, currentTime, currentTemp
    currentTime.set("Time: "+datetime.datetime.fromisoformat(data['hourly']['time'][index]).strftime('%I:%M %p'))
    currentTemp.set(str(data['hourly']['temperature_2m'][index])+"°C")

# Load and display background image
def display_bg():
    global data, new_image
    w_code = data['hourly']['weather_code'][index]
    new_image = ImageTk.PhotoImage(Image.open('weather_bg/'+get_image_name(w_code)))
    bg_label.config(image=new_image)

# Setup window
root = Tk()
root.geometry('500x300')

# Setup variables
index = 0
new_image = None
currentTime = StringVar()
currentTemp = StringVar()

# Setup widgets
bg_label = Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
header = ttk.Frame(root, padding=10)
bottom = ttk.Frame(root)
header.grid()
bottom.grid()
ttk.Label(header, textvariable=currentTime).grid(column=1, row=0)
ttk.Label(textvariable=currentTemp, font=("Arial", 25)).place(relx=.5, rely=.5, anchor="center")
ttk.Button(bottom, text="Prev", command=prev_result).grid(column=1, row=0)
ttk.Button(bottom, text="Next", command=next_result).grid(column=2, row=0)

# Set background and time
display_bg()
display_time()

root.mainloop()