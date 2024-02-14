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
    global currentTime
    currentTime.set(datetime.datetime.fromisoformat(data['hourly']['time'][index]).strftime('%I:%M'))
    global currentTemp
    currentTemp.set(data['hourly']['temperature_2m'][index])


def prev_result():
    global index
    index = max(index - 1, 0)
    global currentTime
    currentTime.set(datetime.datetime.fromisoformat(data['hourly']['time'][index]).strftime('%I:%M'))
    global currentTemp
    currentTemp.set(data['hourly']['temperature_2m'][index])

# Define a function to change the background image
def change_bg():
    new_image = ImageTk.PhotoImage(Image.open("bg2.jpg"))  # Replace with the new image path
    bg_label.config(image=new_image)
    bg_label.image = new_image  # Keep a reference to the image to prevent garbage collection


index = 0
root = Tk()
root.geometry('500x300')

bg_image = ImageTk.PhotoImage(Image.open("bg1.jpg"))  # Replace with your initial image path
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

change_button = Button(root, text="Change Background", command=change_bg)
change_button.pack()


# currentTime = StringVar()
# currentTemp = StringVar()
# currentTime.set(datetime.datetime.fromisoformat(data['hourly']['time'][index]).strftime('%I:%M'))
# currentTemp.set(data['hourly']['temperature_2m'][index])
# header = ttk.Frame(root, padding=10)
# bottom = ttk.Frame(root)
# header.grid()
# bottom.grid()
# ttk.Label(header, text="Time").grid(column=0, row=0)
# ttk.Label(header, textvariable=currentTime).grid(column=1,
#                                                                                                           row=0)
#
# ttk.Label(textvariable=currentTemp).place(relx=.5, rely=.5, anchor="center")
# ttk.Button(bottom, text="Prev", command=prev_result).grid(column=1, row=0)
# ttk.Button(bottom, text="Next", command=next_result).grid(column=2, row=0)

root.mainloop()
