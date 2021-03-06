import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime
import threading


# HTML data of website
def get_html_data(url):
    data = requests.get(url)
    return data


# extracting data
def get_corona_detail_of_india():
    url = "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="site-stats-count").find("ul").find_all("li")
    all_details = ""
    for block in info_div[0:4]:
        count = block.find("strong").get_text()
        text = block.find("span").get_text()
        all_details = all_details + text + " : " + count + "\n"
    return all_details


# reload the data from website
def refresh():
    newdata = get_corona_detail_of_india()
    print("Refreshing..")
    mainLabel['text'] = newdata


# for notification
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message=get_corona_detail_of_india(),
            timeout=10,
            app_icon='icon.ico'
        )
        time.sleep(30)


# GUI
root = tk.Tk()
root.geometry("650x550")
root.iconbitmap("icon.ico")
root.title("CORONA DATA TRACKER - INDIA")
root.configure(background='white')
f = ("poppins", 15, "bold")
banner = tk.PhotoImage(file="banner.png")
bannerLabel = tk.Label(root, image=banner)
bannerLabel.pack()
mainLabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, background='white')
mainLabel.pack()

reBtn = tk.Button(root, text="REFRESH", font=f, relief='solid', command=refresh)
reBtn.pack()

# new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()

root.mainloop()
