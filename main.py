import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests

# Maybe error handling when response fails, add message on screen with option to retry
# Maybe Async
data = requests.get(
    'https://api.open-meteo.com/v1/forecast?latitude=4.2105&longitude=101.9758&hourly=temperature_2m,weather_code&forecast_days=1').json()


def next_result():
    global index
    index = index + 1
    if index >= len(data['hourly']['temperature_2m']):
        index = 0
    global currentTime
    currentTime.set(datetime.datetime.fromisoformat(data['hourly']['time'][index]).strftime('%I:%M'))
    global currentTemp
    currentTemp.set(data['hourly']['temperature_2m'][index])
    change_bg()


def prev_result():
    global index
    index = max(index - 1, 0)
    global currentTime
    currentTime.set(datetime.datetime.fromisoformat(data['hourly']['time'][index]).strftime('%I:%M'))
    global currentTemp
    currentTemp.set(data['hourly']['temperature_2m'][index])


def change_bg():
    global data
    w_code = str(data['hourly']['weather_code'][index])[0]
    if w_code == '1' or w_code == '2' or w_code == '3':
        image_path = "1.jpg"
    else:
        # God bless a valid image is found
        image_path = w_code+".jpg"
    new_image = ImageTk.PhotoImage(Image.open('weather_bg/'+image_path))  # Replace with the new image path
    bg_label.config(image=new_image)
    bg_label.image = new_image  # Keep a reference to the image to prevent garbage collection


index = 0
root = Tk()
root.geometry('500x300')
bg_label = Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# Set initial bg
change_bg()

currentTime = StringVar()
currentTemp = StringVar()
currentTime.set(datetime.datetime.fromisoformat(data['hourly']['time'][index]).strftime('%I:%M'))
currentTemp.set(data['hourly']['temperature_2m'][index])
header = ttk.Frame(root, padding=10)
bottom = ttk.Frame(root)
header.grid()
bottom.grid()
ttk.Label(header, text="Time").grid(column=0, row=0)
ttk.Label(header, textvariable=currentTime).grid(column=1,
                                                                                                          row=0)

ttk.Label(textvariable=currentTemp).place(relx=.5, rely=.5, anchor="center")
ttk.Button(bottom, text="Prev", command=prev_result).grid(column=1, row=0)
ttk.Button(bottom, text="Next", command=next_result).grid(column=2, row=0)

root.mainloop()
