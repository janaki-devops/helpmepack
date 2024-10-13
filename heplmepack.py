import tkinter as tk
from tkinter import ttk
import requests
import csv
import urllib.request
import math
from PIL import Image, ImageTk


root = tk.Tk()
root.title("HelpMePack")
root.configure(bg="#5DC1F2")
root.geometry("750x650")


def get_weather():
    city = city_var.get()
    country = country_var.get()
    if city and country:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid=3f75a000df4eaf2eccf4c5bfb86e943e&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:

            icon_id = data["weather"][0]["icon"]
            condition = data["weather"][0]["main"]
            temp = int(data["main"]["temp"])
            pressure = data["main"]["pressure"]
            description = data["weather"][0]["description"]
            icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
            im = Image.open(requests.get(icon_url, stream=True).raw)
            weather_icon = ImageTk.PhotoImage(im)
            icon_label.configure(image=weather_icon)
            icon_label.image = weather_icon
            final_info = condition + "\n" + str(temp) + "°c"
            final_data = "\n" + "pressure: " + str(pressure) + "\n" + "description: " + str(description)

            packing_suggestions = suggest_packing(data['weather'][0]['main'], data['main']['temp'])
            info_text.set(f"Packing Suggestions:\n{packing_suggestions}")

            label1.config(text=final_info)
            label2.config(text=final_data)

        else:
            info_text.set("City not found")
    else:
        city_var.set("None Selected")
        info_text.set("Please select both city and country")



def suggest_packing(weather_condition, temperature):
    packing_url = 'https://raw.githubusercontent.com/evapchiri/HelpMePack/main/packlist.csv'
    response = urllib.request.urlopen(packing_url)
    csv_data = response.read().decode('utf-8')
    data_rows = csv.reader(csv_data.splitlines())

    pack = []
    for row in data_rows:
        if row[0] == weather_condition:
            pack.append(row[1])

    rounded_temperature = str(math.ceil(temperature / 5.0) * 5)

    for row in data_rows:
        if row[2] == rounded_temperature:
            pack.append(row[3])

    pack = list(set(pack))
    return "\n".join(pack)


def update_cities(event):
    selected_country = country_var.get()
    cities_for_country = cities.get(selected_country, [])
    city_dropdown['values'] = cities_for_country
    city_dropdown.current(0)

countries = ["None Selected", "USA", "UK", "Canada", "Germany", "France", "Italy", "Spain", "Australia", "Japan",
             "China", "India"]
cities = {
    "None Selected": [],
    "USA": ["None Selected", "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
            "San Diego", "Dallas", "San Jose"],
    "UK": ["None Selected", "London", "Manchester", "Birmingham", "Glasgow", "Liverpool", "Bristol", "Leeds",
           "Sheffield", "Edinburgh", "Cardiff"],
    "Canada": ["None Selected", "Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg",
               "Quebec City", "Hamilton", "Kitchener"],
    "Germany": ["None Selected", "Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf",
                "Dortmund", "Essen", "Leipzig"],
    "France": ["None Selected", "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier",
               "Bordeaux", "Lille"],
    "Italy": ["None Selected", "Rome", "Milan", "Naples", "Turin", "Palermo", "Genoa", "Bologna", "Florence", "Bari",
              "Catania"],
    "Spain": ["None Selected", "Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Málaga", "Murcia", "Palma",
              "Las Palmas de Gran Canaria", "Bilbao"],
    "Australia": ["None Selected", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle",
                  "Canberra", "Sunshine Coast", "Wollongong"],
    "Japan": ["None Selected", "Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto",
              "Kawasaki", "Saitama"],
    "China": ["None Selected", "Shanghai", "Beijing", "Guangzhou", "Shenzhen", "Tianjin", "Chongqing", "Hong Kong",
              "Wuhan", "Dongguan", "Chengdu"],
    "India": ["None Selected", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad", "Pune",
              "Surat", "Jaipur"]
}


tk.Label(root,
         text="Welcome to HelpMePack!\n\nThis little app will help you decide what to pack depending on the weather of your destination!"
              "\n\n Tell us where are you travelling to:", fg="black",bg="#5DC1F2",
         font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5, columnspan=2)
tk.Label(root, text="Country:", fg="white", bg="#4169E1", font=("Arial", 12,"bold")).grid(row=1, column=0,
                                                                         padx=5, pady=5, sticky="e")
tk.Label(root, text="City:", fg="white", bg="#4169E1",  font=("Arial", 12,"bold")).grid(row=2, column=0, padx=5,
                                                                      pady=5, sticky="e")

country_var = tk.StringVar(root)
country_dropdown = ttk.Combobox(root, textvariable=country_var, values=countries)
country_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
country_dropdown.current(0)

city_var = tk.StringVar(root)
city_dropdown = ttk.Combobox(root, textvariable=city_var)
city_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")

f = ("verdana", 12, "bold")
t = ("poppins", 18, "bold")
k = ("verdana", 9, "bold")


icon_label = tk.Label(root, bg="#5DC1F2")
icon_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
label1 = tk.Label(root, font=t, fg="#44387D", bg="#5DC1F2", )
label1.grid(row=4, column=0, columnspan=2, padx=2, pady=2)
label2 = tk.Label(root, font=f, fg="#44387D", bg="#5DC1F2")
label2.grid(row=5, column=0, columnspan=2, padx=2, pady=2)
info_text = tk.StringVar()
label3 = tk.Label(root, font=k, fg="#44387D", bg="#5DC1F2", textvariable=info_text, wraplength=1000)
label3.grid(row=6, column=0, columnspan=2, padx=2, pady=2)


country_dropdown.bind("<<ComboboxSelected>>",update_cities)

submit_button = tk.Button(root, text="Suggest me what to pack", command=get_weather, fg="white", bg="#4169E1",
                          font=("Arial", 12, "bold"))
submit_button.grid(row=7, column=0, columnspan=2, pady=40)

root.mainloop()



