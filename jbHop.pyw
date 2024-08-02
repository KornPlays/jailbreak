page = 1 #number of the page from the top/bottom (0 is the minimum)
sort = 1 #sorting of the server, 1 is lowest, 2 is highest
hopKey = ["F1"] #keybind to server hop
rejoinKey = ["F2"] #keybind to rejoin server
serverAddress = "http://127.0.0.1" #server address where the cloud requests will go, the server needs to save data sent by POST request to a string and via a GET request give it back to the user
#REQUIREMENTS:requests,keyboard,orjson,pillow

import threading, time, requests, os, keyboard, base64, io
from PIL import Image, ImageTk
import orjson as json
import tkinter as tk

window = tk.Tk()
window.title("JB Server hop")
window.geometry("290x100")
window.resizable(False, False)
window.configure(bg="#101010")

frame = tk.Frame(window, bg="#101010")
frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

btn_options = {
    "bg": "#101010",
    "fg": "white",
    "relief": "flat",
    "activebackground": "#101010",
    "borderwidth": 0
}

def getImage(base):
    data = base64.b64decode(base)
    image = Image.open(io.BytesIO(data))
    photo = ImageTk.PhotoImage(image)
    return photo

nextImg = getImage('''
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
''')
localImg = getImage('''
iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAMAAAAPdrEwAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAI0UExURRAQECAgIHR0dLe3t+Tk5Pz8/P///xcXF4qKivT09IuLixgYGC8vL9TU1P7+/sDAwHBwcDw8PCIiIh4eHr+/v9XV1ebm5tvb21BQUE9PTzAwMMbGxikpKcXFxdnZ2YyMjE5OTvX19b29vXZ2dm1tbbm5uTo6OuXl5SEhITQ0NFNTU1lZWVhYWDExMUtLS7S0tPDw8O7u7klJSYCAgPr6+vf393p6evv7+8PDw8TExNHR0f39/cnJyUpKStDQ0Dg4OKysrNLS0icnJyoqKmFhYVRUVFtbW9PT07Ozs83NzX19fTk5OUFBQfPz83l5eevr64mJienp6aCgoN/f31JSUmBgYGVlZcfHx7i4uL6+vvn5+UNDQ0xMTGtray0tLZaWlpycnODg4CsrK+Pj4ywsLOfn50dHR2xsbHJycry8vB8fH8vLy19fXyUlJd3d3aKioqWlpdfX1+zs7Dc3NzU1NYWFhfHx8Xx8fISEhLCwsFpaWlVVVVdXV6GhoampqczMzK+vr8rKyjIyMqenp5ubm8jIyHd3d01NTcHBwWJiYqurq6ampo6OjpKSknV1daqqqq6urm9vb11dXUVFRSMjI9zc3FFRUSgoKO/v7zMzMyYmJvj4+D8/P3h4eEJCQiQkJM7OzpCQkLa2tmpqaoaGhoKCgnNzc5OTk5GRkY+Pj0BAQLKysoeHh5iYmIODg52dnX9/f+Hh4V5eXujo6Lq6ukZGRo2NjYiIiPb29js7O9jY2BkZGRGSxfYAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARMSURBVGhD7Zn7XxRVGIcPl/0KCgPLxIJkiyuCqIWXMDe7kaSWdsOoFAkj020pLIjMlFIrU1MsC6Xbdr/fKaLUf673nH1nd2YY3J2d42/7/HK+58zM89mdOTvn3RmRpqS0rDwEDYTKy0pLWCpZUFHJW7RQuXARi0VVNYya2nCdqYG6cO0NBuqr2BxBQyNv0cLiBkSapHlBNW5cwoOaWHIT6uU5qUCDZjO5o2imuVFpaD0baZYasTpRihruamUZWkQZarmnleVoFeUIc08rbVghQtAyn920IyQA7mgGKKodFNUuimoX11CvXLX65tysXnUL7+9mXnXHmrW8huZi3Zr1fIyT+dS3dvKB+bChhY9yMI/6NjpgY3X89tzEN91B+3rd8b3VYapK7ryLO7lYfDew9h7u2PBWdwH3buacm+56oIuzDU/1ffQVt3DOh620/1bOWbzUdds8P8U1uB94gGMWL/V2Onc7OOfHgw8BD3PO4KFe+QjwKOd8qQB63D8dD/VOoKGbc750Pwbs5GwxV91LVfbjnPPnCSqsOzgzc9VPArs4+mE3EOfIzFGXAn17OPuhfyPwFOc0bvVAObCXsz+eBgaf4axwq2mHfc9y9kfTfteHcqkP9AEJzn55DojZT6VLnZxzMfJn6HmglbPEqU7QFOrn7J9GmrYvcCYc6uGDwIucC+ElYGSYs0vdDIy+zLkQxkaBVzg71TsOAa9yLozDtFJmFgW7+jVgUzvnwhgesd2ObeojdEM/mo4FIx3jnLPqElriXlcpCG8Ax0rSMaumBQDxruPB6DpBFl4UMuqxdTSoh543neq3eFwHbzvUvTRysiWxPCiJd47RL/qUXU2n/7TsB2foNK9llpqmxxHZ1wBNQFU5WOptMLzrTf90UOklW0tN38J20wrEGWCZbC31u4BnJVsAVOWela2lPgdMyL4G9gILZWupzwPvyb4G3gcuyNZSfxBg5XJBhYwqWy31hyFE9TwWmbyITrX6WuqxQ+gZkAM+GVp/6ZKateHexsYpGapG8dHHMljqTwbx6WdywCd0jYCUae6hFQrH5cjnfTj4hQyW2vwS6JWtT76S6nOmOS7bk3LkKHBCbcqovwa+USP+GPh2YuI7+QDy+x9+/OlnOXIB+EW2WTVVZIfVSFB+BX5TIaP+HfhDjQSFipE/VcioqfaOqrMfkO5p4C+VMuqBv4GZfzYPB+RADbAi/fA3ozZTdIk79w1OB2FwmipdORclWbU5K+ePBv5N6+xqczy5P7YhGP9FWq0Kx6Gma3A5HIzLtmfsTrVWimoXRbWL66sOIdgfmHmQryGu28uTiNiVrkh0k8CMOI/d3NNKEinRXmks5a5G+o3YpBDNiKriRCdTUcwKIRaNIK7ZPRXHlavyNWlTBFH1z0YX/VF+AUvuERjJRJuW+d3elkgauMJmIa7Oxnhl00JsVp0NZjI1E9Hzij4yk6K5IYQQ/wMoDfGIX9OlqQAAAABJRU5ErkJggg==
''')
onlineImg = getImage('''
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
''')
offlineImg = getImage('''
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
''')
rejoinImg = getImage('''
iVBORw0KGgoAAAANSUhEUgAAAFoAAABaCAMAAAAPdrEwAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJAUExURRAQECAgIHR0dLe3t+Tk5Pz8/P///xcXF4qKivT09IuLixgYGC8vL9TU1P7+/sDAwHBwcDw8PCIiIh4eHr+/v9XV1ebm5tvb21BQUE9PTzAwMMbGxikpKcXFxdnZ2YyMjE5OTvX19b29vXZ2dm1tbbm5uT4+PltbW3JycoGBgY6Ojjo6OuXl5TU1NXFxcaenp9bW1vr6+iEhITg4OIeHh9LS0lpaWru7u62trZ2dnZKSkry8vF9fX/j4+MPDw1RUVMLCwmBgYENDQ/39/cHBwW5ubioqKsTExCMjI4+Pj/b29p6enpGRkdPT0/v7+6CgoDMzMzIyMp+fnz8/P2JiYvLy8snJycjIyGRkZIKCgvf394CAgB8fH39/f4ODg5aWluHh4UlJSUdHR+Dg4JeXly4uLi0tLcfHx4iIiCUlJbi4uImJiWlpaba2tmtra0VFRSQkJCYmJtra2isrK9zc3CcnJ0JCQkBAQPPz86GhoVFRUVJSUjc3N3Nzc+Li4m9vb+3t7SgoKOvr69DQ0EpKSkxMTJubm6ysrKqqqlhYWOfn5+/v70tLS7CwsIaGhl1dXT09PSwsLNfX12VlZampqXl5eaWlpezs7I2NjcrKympqavHx8WZmZrq6unV1dYWFha+vr1lZWaurqzQ0NKSkpNjY2N7e3mxsbLS0tLOzs7W1tZqampycnJiYmEZGRkRERH19fXt7e0FBQWdnZ/n5+ZSUlJWVlb6+vmNjY4SEhF5eXjs7Ozk5OXh4eBkZGU1NTRhI0/IAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAWwSURBVGhDrZn/XxRFGMcX4R4B5YBbPBDh8EIQAZGvKoKHoSIB0hcjixCQjMKyoAQRRcWCysyMvhEJFQVYmpV9USvtX+uZ2w/c7t7u3e3dvn96ntnZ9+tudmZ2ZlZSiFsTn+AgG3AkxK+Jg1SwNjEJV2whKXkdxNL6FHKmpqW7ZBtwpadlOGnDepjdlJmFK7awMZPc2cK8NoU25aDQJnJyaYNok0TKtNnMbg/lcd9IctraGgqbnV6XtIZSkdrKY5QvxVMaMlvZQgVSAqUjC4GrcGvRtuTi5G1FWwsj66MlVCo5KEzd7WU7yiswGAQV5TuKtuOaOZXkkIiQGFJVXQOjlprqKtQwgyikeucuzCvOhNzdtXuK99Tuzk1wKkWOuq2oZUxIdb3yg/f6qhvUHT+noXrfXv+VmsdRZEQIdaNP3L3/wMEmFKhpOnhgv7h8qBEFwZiqm58QT66l1bz3pNe2cI2KtmbkeszUhYf5tvYnn0JqzNPPtHOtw0eQ6jBRP9vB9zxn/mdXaDzK9TqeR6bFWP0Ct2Pni13IQtF1rJOfRzcyDYbqHv4pvceRhKPvJa7dg0SNkfoE1z36MpLw9L/C9U8gUWGgfpVrFgwgiYSBk3zHa0gCBKtf58F20tpb0nWKh+sbSFYJUr/p5XEwiCRSmnl0tfQhWUGvHnqLKPNtJJHT5CE6PYwE6NWtRN4RxFY4M0p0FjHQqce4QxchtkYaN/c5xApadRcP712IrVJAlBKH2I9WXcbNEW6GN+M8L+3GEfvRqCt7iYoRWyeZ6IK602rUF4kuTSC2zvBlojLEAo36HaJEhNHAw7gGoUCtfpenu8injmD6+dUwiZhRq6eI3kMYHe8TtSJk1OpSop0Io+MDoisIGZW6j+jDSiWMkrhLRFcRa9TdRB8pUdTsJrqGUKPmWTdfiaJmXD2YVWpu6vDvWVM+vsLvgxVKr3NJQP0Jdz3NHGCJ69qNoXhXBtRXiab9QVRshBOI5UNA/Wn0k57gM0h56YDhEVB/TvSFP4iO5kMwM73+VWJAfc3wjR85/fzqU2hXdl0BdXEsE6og/UuoZ5TcRrWcxWs07ihfoZ8F1NUxNggzK/YLX5cgs+0x+qll9epfD6hvEM35gxhI30/O1aVGQM1DptwfxMLVHqOZrz+mgW5AQC27Y5qeglGpeY0yr0T2oFJ/Q/StEtmDSn2cVyF2NrZKLRr7O4R2oFZzh19AaAdqNffsln7ENqBWy7zbD97tWKFLvdXUqHn5fVm3a4gBjdp1gSgPsXX0yyONWqwjks4jtsr3viztzlurjkvh3Shiq5yi0WMIFbRq+RxP5tEdzW3hbVIDYgWdWj5LNHoGsRUKO4h+QAz06uHTRB6jE6HQNC0SLen2Knq13MfvTp/Vg2xXKk/2+lOOILW8zM1909o6u/JHbuiDSFYJVsuJ/O78ycoBwOBNviN4PBio5Vtcc1Pkk0l/Lte/jUSFkVr+mesu3UESjl+WuPYtJGoM1fI1bu/OX5GE5jd+7M5qJBqM1fKNUdEod5GZc0Q0RtLvyLSYqOW7G/ieitpspMZk3/6Da02b/AIztTz4pzh59E6trOCCKbklPhO1/2XWmUzVsnxHHLKR496s0RQ+PHvPv3s5qj9xChBCLcv3eSJkOjMejA2hSDA09iCDHx6Tch9FRoRUy/LfGf6jZN6g9PoWptqK26YWfL0rRan1qGVMGDW3aLJ4oMGUJ/+DGmaw2kFhZoyq+QWPelvo8Czk/4tr5ojPEBF9PBkYqR/vzivO6x6vH4nsULSE3NJJuojMVpZpTpqne8hspY4eSpVJzs1IbWTS6W2WpDzyRH9OZsKEh2YkSVo3TT6b3RM+WnwkPpNmu8nzHwptYdKDD7DsniZn3XJJbCdPoLJkuc5JizBL0qMZL8aDLXhn/K0Bmh/OubUnMVHicM895L4hSZL0P2RArZzo0DYZAAAAAElFTkSuQmCC
''')

syncMode = 1 #1 for local, 2 for offline, 3 for online

def sync():
    global syncMode
    if syncMode == 1:
        sync_button.config(image=offlineImg)
        syncMode = 2
    else:
        sync_button.config(image=localImg)
        syncMode = 1

hopBtnPressed = False
rejoinBtnPressed = False

def hopPress():
    global hopBtnPressed
    hopBtnPressed = True

def rejoinPress():
    global rejoinBtnPressed
    rejoinBtnPressed = True

next_button = tk.Button(frame, **btn_options, image=nextImg, command=hopPress)
next_button.grid(row=0, column=0, padx=1)

sync_button = tk.Button(frame, **btn_options, image=localImg, command=sync)
sync_button.grid(row=0, column=1, padx=1)

rejoin_button = tk.Button(frame, **btn_options, image=rejoinImg, command=rejoinPress)
rejoin_button.grid(row=0, column=2, padx=1)

currentServer = ""
stop_thread = False

def loop():
    global stop_thread
    global syncMode
    while not stop_thread:
        if syncMode == 1:
            time.sleep(0.2)
        else:
            get = requests.get(serverAddress)
            try:
                if syncMode == 2:
                    sync_button.config(image=onlineImg)
                    syncMode = 3
                get = get.content.decode('utf-8')
                if len(get) != 0:
                    join(get)
            except Exception:
                if syncMode == 3:
                    sync_button.config(image=offlineImg)
                    syncMode = 2
            for i in range(0,15):
                if stop_thread:
                    break
                time.sleep(0.2)

loop_thread = threading.Thread(target=loop)
loop_thread.start()

def join(jobid):
    global currentServer
    if currentServer != jobid:
        print(jobid)
        os.startfile('roblox://experiences/start?placeId=606849621&gameInstanceId='+jobid)
        currentServer = jobid

url = "https://games.roblox.com/v1/games/606849621/servers/0?excludeFullGames=true&limit=100&sortOrder="+str(sort)

def getList():
    response = requests.get(url)
    for i in range(0,page):
        response = json.loads(response.content)
        response = requests.get(url+"&cursor="+response["nextPageCursor"])
    return json.loads(response.content)["data"]

def hopPressed():
    pressed = True
    for key in hopKey:
        if not keyboard.is_pressed(key):
            pressed = False
            break
    return pressed

def rejoinPressed():
    pressed = True
    for key in rejoinKey:
        if not keyboard.is_pressed(key):
            pressed = False
            break
    return pressed

pressedHop = False
pressedRejoin = False

def main():
    global rejoinBtnPressed
    global hopBtnPressed
    global syncMode
    global stop_thread
    while not stop_thread:
        servers = getList()
        finish = False
        for server in servers:
            while not stop_thread:
                if rejoinBtnPressed:
                    rejoinBtnPressed = False
                    os.startfile('roblox://experiences/start?placeId=606849621&gameInstanceId='+currentServer)
                elif hopBtnPressed:
                    hopBtnPressed = False
                    break
                elif rejoinPressed():
                    if not pressedRejoin:
                        pressedRejoin = True
                        os.startfile('roblox://experiences/start?placeId=606849621&gameInstanceId='+currentServer)
                elif hopPressed():
                    if not pressedHop:
                        pressedHop = True
                        break
                else:
                    pressedHop = False
                    pressedRejoin = False
                time.sleep(0.05)
            if not stop_thread:
                if syncMode == 3:
                    try:
                        requests.post(serverAddress,server['id'])
                    except Exception:
                        sync_button.config(image=offlineImg)
                        syncMode = 2
                join(server['id'])

main_thread = threading.Thread(target=main)
main_thread.start()

def on_close(event):
    global stop_thread
    stop_thread = True
    loop_thread.join()
    main_thread.join()
    exit()

window.bind("<Destroy>", on_close)

window.wm_attributes("-topmost", True)

window.mainloop()