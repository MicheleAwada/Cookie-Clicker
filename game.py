import json
import tkinter as tk
from tkscrolledframe import ScrolledFrame
from tkinter import messagebox
from datetime import datetime
from PIL import ImageTk
from timeit import timeit
from random import randint
import os
from os import path
from math import log10
from playsound import playsound
from pyaudio import PyAudio, paContinue
import wave
import ctypes
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, paContinue)
def start_count():
    global count
    if mmuted and not no_current_music:
        count += 1
        root.after(1000,start_count)
def music(ref=False):
    global stream
    global wf
    global no_current_music
    if ref is False:
        global count
        if mmuted is False and count>0:
            countt=count*1000+1
            count=0
            root.after(countt, music)
            return
        if mmuted:
            no_current_music=True
            count=0
            return
        stream.stop_stream()
        stream.close()
        wf.close()
    # random_music = randint(1,3)
    # wf = wave.open(resource_path('music1.wav') if random_music==1 else resource_path("music2.wav") if random_music==2 else resource_path("music3.wav"), 'rb')
    wf = wave.open(resource_path('music.wav'), 'rb')
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    stream.start_stream()
    if mmuted:
        stream.stop_stream()
        start_count()
    frames = wf.getnframes()
    framespersecond = wf.getframerate()
    len_of_music = int(frames/framespersecond*1000)
    root.after(len_of_music, music)
def motion_def(e):
    global motion
    if motion:
        motion=False
        pplaysound(click_audio, False)
        save_settings(muted,mmuted,motion)
        canvas_menu.itemconfig(cookiemotion, image=no_motion_cookie)
        cookiemotionlbl["text"] = "Cookie\nMotion:Off"
        cookiemotionlbl.place(x=245,y=65,anchor=tk.W)
    else:
        motion=True
        pplaysound(click_audio, False)
        save_settings(muted, mmuted, motion)
        canvas_menu.itemconfig(cookiemotion, image=motion_cookie)
        cookiemotionlbl["text"] = "Cookie\nMotion:On"
        cookiemotionlbl.place(x=270, y=65, anchor=tk.W)
def mmuted_def(e):
    global mmuted
    global no_current_music
    if mmuted is True:
        mmuted=False
        if no_current_music:
            no_current_music=False
            music()
        else:
            stream.start_stream()
        pplaysound(click_audio, False)
        save_settings(muted, mmuted, motion)
        canvas_menu.itemconfig(music_canvas, image=mmuted_off_png)
        mmute_label['text']= "Music Is On"
    elif mmuted is False:
        mmuted=True
        start_count()
        stream.stop_stream()
        pplaysound(click_audio, False)
        save_settings(muted, mmuted, motion)
        canvas_menu.itemconfig(music_canvas, image=mmuted_on_png)
        mmute_label['text'] = "Music Is Off"
def muted_def(e):
    global muted
    if muted is True:
        muted=False
        pplaysound(click_audio, False)
        save_settings(muted, mmuted, motion)
        canvas_menu.itemconfig(muted_canvas, image=muted_off_png)
        mute_label['text']= "Sound Effects On"
    elif muted is False:
        pplaysound(click_audio, False)
        save_settings(muted, mmuted, motion)
        muted=True
        canvas_menu.itemconfig(muted_canvas, image=muted_on_png)
        mute_label['text'] = "Sound Effects Off"
def menu_ingame_def_e(e,in_menu_for_menu):
    global in_menu,canvas_menu,close_btn_menu
    global muted_canvas,mute_label
    global music_canvas,mmute_label
    global cookiemotion,cookiemotionlbl
    if in_menu is False:
        in_menu=True
        canvas_menu = tk.Canvas(canvas if in_menu_for_menu else canvas2, height=175, width=350, relief=tk.RAISED, bg=cookiecolor)
        canvas_menu.place(x=270 if in_menu_for_menu else 250, y=270 if in_menu_for_menu else 137, anchor=tk.CENTER)

        close_btn_menu = canvas_menu.create_image(335,15,image= close_btn,anchor=tk.NE)
        canvas_menu.tag_bind(close_btn_menu,"<Button-1>",lambda e: menu_ingame_def_e(e,in_menu_for_menu))
        canvas_menu.tag_bind(close_btn_menu, "<Enter>", muted_canvas_def_enter)
        canvas_menu.tag_bind(close_btn_menu, "<Leave>", muted_canvas_def_leave)

        muted_canvas = canvas_menu.create_image(15, 40, image=muted_on_png if muted is True else muted_off_png,anchor=tk.NW)
        canvas_menu.tag_bind(muted_canvas,"<Button-1>",muted_def)
        canvas_menu.tag_bind(muted_canvas, "<Enter>", muted_canvas_def_enter)
        canvas_menu.tag_bind(muted_canvas, "<Leave>", muted_canvas_def_leave)
        mute_label = tk.Label(canvas_menu, text="Sound Effects Off" if muted is True else "Sound Effects On", bg=cookiecolor)
        mute_label.place(x=80,y=65,anchor=tk.W)

        music_canvas = canvas_menu.create_image(15, 160, image=mmuted_on_png if mmuted is True else mmuted_off_png,
                                                anchor=tk.SW)
        canvas_menu.tag_bind(music_canvas,"<Button-1>",mmuted_def)
        canvas_menu.tag_bind(music_canvas, "<Enter>", muted_canvas_def_enter)
        canvas_menu.tag_bind(music_canvas, "<Leave>", muted_canvas_def_leave)
        mmute_label = tk.Label(canvas_menu, text="Music Is Off" if mmuted is True else "Music Is On", bg=cookiecolor)
        mmute_label.place(x=80,y=135,anchor=tk.W)

        back_to_main_menu = canvas_menu.create_image(220,135,anchor=tk.CENTER, image=menu_ingame_img)
        canvas_menu.tag_bind(back_to_main_menu,"<Button-1>",lambda e: main_menu(e,in_menu_for_menu))
        canvas_menu.tag_bind(back_to_main_menu, "<Enter>", muted_canvas_def_enter)
        canvas_menu.tag_bind(back_to_main_menu, "<Leave>", muted_canvas_def_leave)

        label_to_main_menu = tk.Label(canvas_menu, text="Go to Main Menu",bg=cookiecolor)
        label_to_main_menu.place(x=250,y=135,anchor=tk.W)

        cookiemotion = canvas_menu.create_image(195,40,anchor=tk.NW,image=motion_cookie if motion else no_motion_cookie)
        canvas_menu.tag_bind(cookiemotion,"<Button-1>", motion_def)
        canvas_menu.tag_bind(cookiemotion, "<Enter>", muted_canvas_def_enter)
        canvas_menu.tag_bind(cookiemotion, "<Leave>", muted_canvas_def_leave)
        cookiemotionlbl = tk.Label(canvas_menu,text="Cookie\nMotion:On" if motion else "Cookie\nMotion:Off",bg=cookiecolor)
        cookiemotionlbl.place(x=270 if motion else 245,y=65,anchor=tk.W)
    elif in_menu is True:
        in_menu=False
        canvas_menu.destroy()
def muted_canvas_def_enter(e):
    canvas_menu['cursor']="hand2"
def muted_canvas_def_leave(e):
    canvas_menu['cursor']=""
def cookie_enter(e):
    canvas2.config(cursor="hand2")
def cookie_leave(e):
    canvas2.config(cursor="")
def new_load_enter(e):
    canvas.config(cursor="hand2")
def new_load_leave(e):
    canvas.config(cursor="")
def dev_delete_prof():
    path_to_dir = resource_path("profiles")
    files_in_dir = os.listdir(path_to_dir)  # get list of files in the directory
    print(f"{files_in_dir} all have been deleted")
    for file in files_in_dir:  # loop to delete each file in folder
        os.remove(f'{path_to_dir}/{file}')
def pplaysound(name,T_or_F):
    if muted is False:
        playsound(name, T_or_F)
def wtf_def(randomizer_for_move, mookie=1):
    if cps_number!=8:
        x = 1 if 5>=randomizer_for_move>=3 else 0 if randomizer_for_move==6 or randomizer_for_move==2 else -1
        y = 1 if 3>=randomizer_for_move>=1 else 0 if randomizer_for_move==4 or randomizer_for_move==8 else -1
        if 2>=mookie>0:
            canvas2.move(cookieclick,x,y)
        elif 6>=mookie>2:
            canvas2.move(cookieclick,x,y)
        elif 8>=mookie>6:
            canvas2.move(cookieclick,x,y)
        else:
            return
        mookie+=1
        root.after(20, lambda: wtf_def(randomizer_for_move,mookie))
def move_cookie(randomizer_for_move, mookie=1):
    if cps_number!=8:
        x = 1 if 5>=randomizer_for_move>=3 else 0 if randomizer_for_move==6 or randomizer_for_move==2 else -1
        y = 1 if 3>=randomizer_for_move>=1 else 0 if randomizer_for_move==4 or randomizer_for_move==8 else -1
        if 2>=mookie>0:
            canvas2.move(cookieclick,x,y)
        elif 6>=mookie>2:
            canvas2.move(cookieclick,-x,-y)
        elif 8>=mookie>6:
            canvas2.move(cookieclick,x,y)
        else:
            return
        mookie+=1
        root.after(20, lambda: move_cookie(randomizer_for_move,mookie))
def resource_path(relative_path):
    baseDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(baseDir, "extras", relative_path)
def timeit_def(time):
    if 0.07>time:
        cps_number=20
        print("fast pc")
    elif 0.12>time>=0.07:
        cps_number=10
        print("meh pc")
    else:
        cps_number=8
        print("slow pc")
    time_wait = int(1000 / cps_number)
    return cps_number, time_wait
def autosave(start=False):
    try:
        save()
        if start is False:
            print("auto saving")
    except:
        print("error saving")
    root.after(60000, autosave)
def state():
    for v,butt in zip(price_per_type, buttons):
        if cookie < price_per_type[v]:
            butt["state"] = tk.DISABLED
        else:
            if butt["state"] == tk.DISABLED:
                butt["state"] = tk.NORMAL
def passivecookie():
    if in_game:
        global cookie
        global nwcookie
        nwcookie += cps_x_th
        cookie += cps_x_th
        labelcookienumber['text'] = f"{cookie_emoji}{abbreviate_numbers(cookie)}"
        state()
        achie()
        root.after(time_wait, passivecookie)
def cookieincrimental(click,start):
    def change_image():
        canvas2.itemconfig(cookieclick, image=donutimg)
        root.after(250, revert_image)
    def revert_image():
        canvas2.itemconfig(cookieclick, image=cookiepng)
    def infolbl_donut(all):
        global achie_present
        global cookiecolor
        if achie_present is False:
            achie_present=True
            if infolbl["state"] == tk.DISABLED:
                infolbl["state"] = tk.NORMAL
            if all is True:
                cookiecolor = "#F59CA9"
                root["bg"] = cookiecolor
                lbls = [bakerycookieprofilename, labelcookienumber, cookieclick, shoptxt, infolbl]
                for lbl in lbls:
                    lbl["bg"] = cookiecolor
                    lbl["fg"] = "white"
                first=True
                for lbl2 in buttons:
                    if first is True:
                        first=False
                    else:
                        lbl2["bg"] = cookiecolor
                        lbl2["activebackground"] = aacookiecolor
                        lbl2["fg"] = "white"
            infolbl["text"] = f"DONUTS"
            infolbl["bg"] = "#F59CA9"
            infolbl["fg"] = "white"
            root.after(2000, lambda: infolbl_donut_revert(all))
    def infolbl_donut_revert(all):
        global achie_present
        global cookiecolor
        achie_present = False
        if all is True:
            cookiecolor = '#E6CEA0'
            root["bg"] = cookiecolor
            lbls = [bakerycookieprofilename, labelcookienumber, cookieclick, shoptxt, infolbl]
            for lbl in lbls:
                lbl["bg"] = cookiecolor
                lbl["fg"] = "black"
            first = True
            for lbl2 in buttons:
                if first is True:
                    first = False
                else:
                    lbl2["bg"] = cookiecolor
                    lbl2["activebackground"] = aacookiecolor
                    lbl2["fg"] = "black"
        infolbl["text"] = ""
        infolbl["bg"] = '#E6CEA0'
        infolbl["fg"] = "black"
    if click is True:
        randomizer = randint(1, 2048)
        if randomizer == 1:
            change_image()
    else:
        randomizer = randint(1, 64)
        if randomizer <= 2 and start is False:
            infolbl_donut(False)
        if randomizer == 3 and start is False:
            infolbl_donut(True)
        root.after(15000, lambda: cookieincrimental(False,False))
def abbreviate_numbers(numinp,dec=1):
    exp = max(0,min(100,int(0 if numinp == 0 else log10(abs(numinp))//3)))
    num = numinp * 10**3 // 10 ** (exp * 3) / 10**3 if exp>0 else numinp * dec // 1 / dec
    return f'{int(num) if exp==0 and dec==1 else num} {Big_Names[exp].capitalize()}'
def price(name, price_constant):
    price = round(price_constant * 1.15 ** amount_per_type[name])
    return price
def shopdef():
    def create_button(cps_constant, name, desc):
        def update_values(refresh):
            global cpsall
            global cookie
            global cps_x_th
            global buttons
            global unlocked_buttons
            global click_cookie_amount, click_cookie_amount1, click_cookie_amount10
            if refresh is False:
                pplaysound(click_audio, False)
                cookie -= price_per_type[name]
                labelcookienumber['text'] = f"{cookie_emoji}{abbreviate_numbers(cookie)}"
                amount_per_type[name] += buy
                price_per_type[name] = round(price_per_type[name] * 1.15) if buy==1 else round(price_per_type[iii]*20.303718) if buy==10 else round(price_per_type[iii]*7828749.6713352) if buy==100 else print("wtf")
                cpsall = round(cpsall + cps_constant*buy, 1)
                cps_x_th = cpsall / cps_number
                click_cookie_amount = cpsall * amount_per_type[initial_cookie_name] / 100 + 1
                click_cookie_amount1 = cpsall * (amount_per_type[initial_cookie_name]+1) / 100 + 1
                click_cookie_amount10 = cpsall * (amount_per_type[initial_cookie_name] + 10) / 100 + 1
                if unlocked_buttons+2 < len(buttons):
                    if amount_per_type[name]==1:
                        unlocked_buttons+=1
                        buttons[unlocked_buttons+1].pack()
                shoptxt["text"] = f"↓Shop↓, {abbreviate_numbers(cpsall,10)} c/s"
                state()
                on_leave("_")
                on_enter("_")
                achie()
            else:
                cpsall= round(cpsall+cps_constant*amount_per_type[name],1)
                if amount_per_type[name]>0:
                    unlocked_buttons+=1
            button["text"] = f"{name}\n{cookie_emoji}{abbreviate_numbers(price_per_type[name])}"
        def on_enter(e):
            global active,backed_text,active_disabled
            active=True
            active_disabled=False if button["state"] == tk.NORMAL else True
            backed_text = f"Buy a {name} {cookie_emoji}{abbreviate_numbers(price_per_type[name])}" \
                                  f"\n{desc}" \
                                  f"\nAmount: {amount_per_type[name]}, {initial_cookie_name}: {abbreviate_numbers(amount_per_type[name] * cps_constant,10)}" \
                                  f"\nEach {name} gives {abbreviate_numbers(cps_constant,10)}c/s"
            if button["state"] == tk.NORMAL:
                button['background'] = acookiecolor
            if achie_present is False:
                if button["state"] == tk.DISABLED:
                    infolbl["state"] = tk.DISABLED
                infolbl["text"] = backed_text
        def on_leave(e):
            global active,active_disabled
            active_disabled = False
            active = False
            button['background'] = cookiecolor
            if achie_present is False:
                infolbl["state"] = tk.NORMAL
                infolbl['text'] = ''
        button = tk.Button(inframe, command=lambda: update_values(False), bg=cookiecolor, activebackground=aacookiecolor, width=32, cursor="hand2")
        if player_name=="donut" or player_name=="donuts":
            button["fg"] = "white"
        update_values(True)
        button.bind("<Leave>", on_leave)
        button.bind("<Enter>", on_enter)
        return button
    def create_button_cpspercent_add(cre):
        def cps_on_enter(e):
            global active,backed_text,active_disabled
            active_disabled = False if cps_percent_bn["state"] == tk.NORMAL else True
            active=True
            backed_text = f'Gain {amount_per_type[initial_cookie_name]}% of {long_initial_cookie_name if amount_per_type[initial_cookie_name]==0 else initial_cookie_name} on {cookie_name.capitalize()} Clicks' \
                                  f"\nYou're currently getting {abbreviate_numbers(click_cookie_amount,10)} on each {cookie_name.capitalize()} Click" \
                                  f'\nAnd will get {abbreviate_numbers(click_cookie_amount1 if buy1 else abbreviate_numbers(click_cookie_amount10) if buy10 else 1,10)} if you buy me'
            if cps_percent_bn["state"] == tk.NORMAL:
                cps_percent_bn["bg"] = "#7DF9FF"
            if achie_present is False:
                if cps_percent_bn["state"] == tk.DISABLED:
                    infolbl["state"] = tk.DISABLED
                infolbl["text"] = backed_text
        def cps_on_leave(e):
            global active,active_disabled
            active=False
            active_disabled = False
            cps_percent_bn["bg"] = "#15F4EE"
            if achie_present is False:
                infolbl["text"] = ""
                infolbl["state"] = tk.NORMAL
        def cpspercent_add(refresh):
            global click_cookie_amount, click_cookie_amount1, click_cookie_amount10
            global cookie
            if refresh is False:
                pplaysound(click_audio, False)
                cookie-= price_per_type[initial_cookie_name]
                labelcookienumber['text'] = f"{cookie_emoji}{abbreviate_numbers(cookie)}"
                amount_per_type[initial_cookie_name] += 1
                price_per_type[initial_cookie_name] *= 100
                state()
            click_cookie_amount = cpsall * amount_per_type[initial_cookie_name] / 100 + 1
            click_cookie_amount1 = cpsall * (amount_per_type[initial_cookie_name] + 1) / 100 + 1
            click_cookie_amount10 = cpsall * (amount_per_type[initial_cookie_name] + 10) / 100 + 1
            print(click_cookie_amount10)
            cps_percent_bn["text"] = f"Buy {initial_cookie_name} on Cookie Click" \
                                 f'\n{cookie_emoji}{abbreviate_numbers(price_per_type[initial_cookie_name])}'
        if cre is True:
            global cps_percent_bn
            cps_percent_bn = tk.Button(inframe, height=2, width=32, command=lambda: cpspercent_add(False), bg="#15F4EE", activebackground="#B2FFFF", cursor="hand2")
            cps_percent_bn.bind("<Enter>", cps_on_enter)
            cps_percent_bn.bind("<Leave>", cps_on_leave)
            return cps_percent_bn
        else:
            cpspercent_add(True)
    global cookie
    global cpsall
    global buttons
    global price_per_type
    global cps_x_th
    global unlocked_buttons
    unlocked_buttons=0
    cpsall=0
    buttons = [
        create_button_cpspercent_add(True),
        create_button(0.1, "Clicker", f"Click {cookie_name}s for you"),
        create_button(1, "Grandma", f"Bakes {cookie_name}s with the sweetest smell"),
        create_button(5, f"{cookie_name.capitalize()} Chef", f"Bakes {cookie_name}s with the best texture"),
        create_button(20, f"{cookie_name.capitalize()} Tree", f"Grows {cookie_name}s no matter the season"),
        create_button(50, f"{cookie_name.capitalize()} Machine", f"Creates {cookie_name}s with crazy speed"),
        create_button(100, "Bakery", f"Makes {cookie_name}s from scratch"),
        create_button(250, "Factory", f"Creates {cookie_name}s using of {cookie_name.capitalize()} Machines"),
        create_button(500, "Farm", f"Farms {cookie_name}s from the soil"),
        create_button(1_250, "Bank", f"Local banks use {cookie_name}s as the new currency"),
        create_button(3_000, f"{cookie_name.capitalize()} Forest", f"Hundreds of {cookie_name.capitalize()} trees"),
        create_button(5_000, "Auto Clicker", f"New advanced Clickers click {cookie_name}s super fast"),
        create_button(10_000, "International Factories", "Factories start opening all around the world"),
        create_button(25_000, "International Banks", "Banks start opening all around the world"),
        create_button(45_000, "Crypto Currency", f"BitCookies start create {cookie_name}s from the blockchain"),
        create_button(500_000, f"{cookie_name.capitalize()} Machine 2.0", f"Only Possible using Element 115")
    ]
    create_button_cpspercent_add(False)
    cps_x_th = cpsall/cps_number
    if unlocked_buttons+1==len(buttons):
        unlocked_buttons-=1
    for buttonz in range(unlocked_buttons+2):
        buttons[buttonz].pack()
    shoptxt["text"] = f"↓Shop↓, {abbreviate_numbers(cpsall,10)} {initial_cookie_name}"
    state()
    passivecookie()
def on_enter_buy(e, buy_num):
    if buy_num==1:
        if buy1["state"] == tk.NORMAL:
            buy1["bg"] = acookiecolor
    if buy_num==10:
        if buy10["state"] == tk.NORMAL:
            buy10["bg"] = acookiecolor
    if buy_num==100:
        if buy100["state"] == tk.NORMAL:
            buy100["bg"] = acookiecolor
def on_leave_buy(e, buy_num):
    if buy_num==1:
        buy1["bg"] = cookiecolor
    if buy_num==10:
        buy10["bg"] = cookiecolor
    if buy_num==100:
        buy100["bg"] = cookiecolor
def price_per_type_refresh():
    global price_per_type
    price_per_type = {
        f"{initial_cookie_name}": 100 ** (amount_per_type[f"{initial_cookie_name}"] + 1),
        "Clicker": price("Clicker", 5),
        "Grandma": price("Grandma", 75),
        f"{cookie_name.capitalize()} Chef": price(f"{cookie_name.capitalize()} Chef", 5_00),
        f"{cookie_name.capitalize()} Tree": price(f"{cookie_name.capitalize()} Tree", 2_500),
        f"{cookie_name.capitalize()} Machine": price(f"{cookie_name.capitalize()} Machine", 8_500),
        "Bakery": price("Bakery", 22_500),
        "Factory": price("Factory", 75_000),
        "Farm": price("Farm", 200_000),
        "Bank": price("Bank", 667_500),
        f"{cookie_name.capitalize()} Forest": price(f"{cookie_name.capitalize()} Forest", 2_160_000),
        "Auto Clicker": price("Auto Clicker", 4_800_000),
        "International Factories": price("International Factories", 12_800_000),
        "International Banks": price("International Banks", 39_260_000),
        "Crypto Currency": price("International Banks", 100_000_000),
        f"{cookie_name.capitalize()} Machine 2.0": price(f"{cookie_name.capitalize()} Machine 2.0", 1_000_000_000),
    }
def buy_def(buy_num,ref=False):
    global buy,buybef
    global price_per_type
    buybef = buy
    calm_down_jamal = False
    if buy_num==1:
        buy=1
        buy1["bg"] = cookiecolor
        for something in buyboutins:
            something["state"] = tk.NORMAL
            something["relief"] = tk.GROOVE
        buy1["relief"] =  tk.SUNKEN
        buy1["state"] = tk.DISABLED
        price_per_type_refresh()
    if buy_num == 10:
        buy=10
        buy10["bg"] = cookiecolor
        for something in buyboutins:
            something["state"] = tk.NORMAL
            something["relief"] = tk.GROOVE
        buy10["relief"] = tk.SUNKEN
        buy10["state"] = tk.DISABLED
        price_per_type_refresh()
        for iii in price_per_type:
            if iii == f"{initial_cookie_name}":
                for factorial_exponential in range(11):
                    if factorial_exponential>0:
                        price_per_type[iii] += 100**factorial_exponential
                        price_per_type[iii] = round(price_per_type[iii])
            else:
                price_per_type[iii] = round(price_per_type[iii]*20.303718)
    if buy_num == 100:
        buy=100
        buy100["bg"] = cookiecolor
        for something in buyboutins:
            something["state"] = tk.NORMAL
            something["relief"] = tk.GROOVE
        buy100["relief"] = tk.SUNKEN
        buy100["state"] = tk.DISABLED
        price_per_type_refresh()
        for iii in price_per_type:
            if iii == f"{initial_cookie_name}":
                calm_down_jamal=True
                price_per_type[iii]=price_per_type[iii]*1.0101010101010101010101010102e29
            else:
                price_per_type[iii]=round(price_per_type[iii]*7828749.6713352)
    if ref is not True:
        pplaysound(click_audio, False)
        state()
        for key, key2 in zip(price_per_type, buttons):
            if calm_down_jamal is True:
                if key == f"{initial_cookie_name}":
                    key2["text"] = f"Buy {initial_cookie_name} on Cookie Click\nCalm down jamal"
                    key2["state"] = tk.DISABLED

                    calm_down_jamal=False
            else:
                key2['text'] = f"{key}\n{cookie_emoji}{abbreviate_numbers(price_per_type[key])}"
    return
def clickcookielbls():
    global canvas2
    global in_game
    global player_name_canvas
    global new_canvas
    global load_canvas
    global labelcookienumber
    global errorpresent
    global cookiecolor
    global cookie_emoji, cookie_name, long_initial_cookie_name, initial_cookie_name
    global inframe
    global cookiecolor, cookieclick, acookiecolor, aacookiecolor, cookie_emoji, ee
    global infolbl, shoptxt
    global donutimg, cookiepng
    global buy1, buy10, buy100, buy, buyboutins
    global wtf
    if errorpresent is True:
        canvas.delete(error_canvas)
        errorpresent = False
    canvas.destroy()
    root.geometry("500x300")
    root.config(bg=cookiecolor)

    wtf=False
    if player_name=="wtf":
        wtf=True

    canvas2 = tk.Canvas(root, bg=cookiecolor, width=500, height=300)
    canvas2.pack()

    donutimg = ImageTk.PhotoImage(file=resource_path('cookie2.png'))
    cookiepng = ImageTk.PhotoImage(file=resource_path('cookieclr.png'))
    if used:
        200, 200 == cookiepng.height(), cookiepng.width()
        200, 200 == donutimg.height(), donutimg.width()
    cookieclick = canvas2.create_image(100,160, image=cookiepng, anchor=tk.CENTER)
    canvas2.tag_bind(cookieclick, '<Button-1>', clickcookie)
    canvas2.tag_bind(cookieclick, '<Enter>', cookie_enter)
    canvas2.tag_bind(cookieclick, '<Leave>', cookie_leave)

    bakerycookieprofilename = tk.Label(canvas2, height=1, bg=cookiecolor)
    labelcookienumber = tk.Label(canvas2, height=1, bg=cookiecolor)
    shoptxt = tk.Label(canvas2, height=1, bg=cookiecolor)
    infolbl = tk.Label(canvas2, height=4, bg=cookiecolor, borderwidth=2, relief=tk.GROOVE)
    sf = ScrolledFrame(canvas2, bg=cookiecolor, scrollbars="vertical", height=128, width=250)

    buy1 = tk.Button(canvas2, relief=tk.GROOVE, height=1, bg=cookiecolor, activebackground=aacookiecolor, command=lambda: buy_def(1), text="Buy 1", state=tk.DISABLED, cursor="hand2")
    buy10 = tk.Button(canvas2, relief=tk.GROOVE, height=1, bg=cookiecolor, activebackground=aacookiecolor, command=lambda: buy_def(10), text="Buy 10", cursor="hand2")
    buy100 = tk.Button(canvas2, relief=tk.GROOVE, height=1, bg=cookiecolor, activebackground=aacookiecolor, command=lambda: buy_def(100), text="Buy 100", cursor="hand2")
    buy1.bind('<Enter>', lambda e: on_enter_buy(e,1))
    buy10.bind('<Enter>', lambda e: on_enter_buy(e,10))
    buy100.bind('<Enter>', lambda e: on_enter_buy(e,100))
    buy1.bind('<Leave>', lambda e: on_leave_buy(e,1))
    buy10.bind('<Leave>', lambda e: on_leave_buy(e,10))
    buy100.bind('<Leave>', lambda e: on_leave_buy(e,100))
    buyboutins = [buy1,buy10,buy100]
    buy=1

    if cookie_name_def(player_name) is True:
        ee = True
        canvas2.itemconfig(cookieclick, image=donutimg)
        cookiecolor="#F6828C"
        acookiecolor="#F59CA9"
        aacookiecolor="#F9C7CF"

        cookie_name="donut"
        cookie_emoji = "🍩"
        initial_cookie_name = "DPS"
        long_initial_cookie_name = "Donuts Per Second"
        lbls = [bakerycookieprofilename, labelcookienumber, shoptxt, infolbl, buy1, buy10, buy100]
        root.config(bg=cookiecolor)
        canvas2.config(bg=cookiecolor)
        for lbl in lbls:
            lbl["bg"] = cookiecolor
            lbl["fg"] = "white"
        for buybtns in buyboutins:
            buybtns['activebackground']=aacookiecolor
    else:
        ee=False
    buy_def(1, True)

    bakerycookieprofilename["text"] = f"{player_name.capitalize()}'s Bakery"
    labelcookienumber['text'] = f"{cookie_emoji}{abbreviate_numbers(cookie)}"

    bakerycookieprofilename.place(x=100, y=15, width=100, anchor=tk.CENTER)
    labelcookienumber.place(x=100, y=35, width=100, anchor=tk.CENTER)
    shoptxt.place(x=350, y=50, width=180, anchor=tk.CENTER)
    infolbl.place(x=350, y=97, width=300, anchor=tk.CENTER)
    sf.place(x=350, y=230, width=300, height=150, anchor=tk.CENTER)

    buy1.place(x=200,y=130, width=100, anchor=tk.NW)
    buy10.place(x=350, y=143, width=100, anchor=tk.CENTER)
    buy100.place(x=500, y=130, width=100, anchor=tk.NE)

    menu_ingame = canvas2.create_image(495, 5, image=menu_ingame_img, anchor=tk.NE)
    canvas2.tag_bind(menu_ingame, "<Enter>", cookie_enter)
    canvas2.tag_bind(menu_ingame, "<Leave>", cookie_leave)
    canvas2.tag_bind(menu_ingame, "<Button-1>", lambda e: menu_ingame_def_e(e, False))

    inframe = sf.display_widget(tk.Frame)
    sf.bind_arrow_keys(root)
    sf.bind_scroll_wheel(root)



    in_game = True
    shopdef()
    achie()
def cookie_name_def(name):
    if name=="donut" or name=="donuts" or name == "dougnuts" or name == "dougnut":
        return True
    return False
def clickcookie(e):
    global cookie
    global nwcookie
    pplaysound(crunch_audio, False)
    cookie += 1
    nwcookie += 1
    labelcookienumber['text'] = f"{cookie_emoji}{abbreviate_numbers(cookie)}"
    achie()
    state()
    random=randint(1,8)
    if motion:
        if wtf is False:
            move_cookie(random)
        else:
            wtf_def(random)
    if ee is False:
        cookieincrimental(True,False)
def achiestart():
    global achie_present,backed_text
    achie_present = True
    infolbl["state"] = tk.NORMAL
    infolbl["text"] = f'Congrats you got the achievement:\n{infolbltxt}'
    infolbl["bg"] = "orange"
    infolbl["fg"] = "white"
def achlblreset():
    global achie_present
    achie_present = False
    infolbl['text'] = "" if active is False else f"{backed_text}"
    infolbl['state'] = tk.NORMAL if active_disabled is False else tk.DISABLED
    infolbl["bg"] = cookiecolor
    infolbl["fg"] = "black"
    achie()
def achie():
    global infolbltxt
    global ach
    if achie_present is False:
        if 'ach1k' not in ach and cookie >= 1000:
            ach.append('ach1k')
            infolbltxt = '1 Thousand Cookies Obtained'
            achiestart()
            root.after(5000, achlblreset)
        elif 'ach1m' not in ach and cookie >= 1000000:
            ach.append('ach1m')
            infolbltxt = '1 Million Cookies Obtained'
            achiestart()
            root.after(5000, achlblreset)
        if 'grandma10' not in ach and amount_per_type["Grandma"] >= 10:
            ach.append('grandma10')
            infolbltxt= "10 Grandma's in a Party"
            achiestart()
            root.after(5000, achlblreset)
        if 'clicker20' not in ach and amount_per_type["Clicker"] >= 20:
            ach.append('clicker20')
            infolbltxt= 'Auto Clicker'
            achiestart()
            root.after(5000, achlblreset)
def reserrorlabel():
    global errorpresent
    global cagain
    if errorpresent is True:
        global error_canvas
        cagain=0
        errorpresent=False
        canvas.delete(error_canvas)
def newe(e):
    newatm()
def new():
    global shopdic
    global cookie
    global ach
    global player_name
    global datecreated
    global amount_per_type
    global nwcookie
    global cookie_name
    global initial_cookie_name
    global long_initial_cookie_name
    global mlt_cps_per_type
    cookie = cookies_in_menu
    nwcookie = cookies_in_menu
    if cookie_name_def(player_name) is True:
        cookie_name = "donut"
        initial_cookie_name = "DPS"
    amount_per_type = {
        f"{initial_cookie_name}": 0,
        "Clicker": 0,
        "Grandma": 0,
        f"{cookie_name.capitalize()} Chef": 0,
        f"{cookie_name.capitalize()} Tree": 0,
        f"{cookie_name.capitalize()} Machine": 0,
        "Bakery": 0,
        "Factory": 0,
        "Farm": 0,
        "Bank": 0,
        f"{cookie_name.capitalize()} Forest": 0,
        "Auto Clicker": 0,
        "International Factories": 0,
        "International Banks": 0,
        "Crypto Currency": 0,
        f"{cookie_name.capitalize()} Machine 2.0":0
    }
    mlt_cps_per_type = {
        f"{initial_cookie_name}": 1,
        "Clicker": 1,
        "Grandma": 1,
        f"{cookie_name.capitalize()} Chef": 1,
        f"{cookie_name.capitalize()} Tree": 1,
        f"{cookie_name.capitalize()} Machine": 1,
        "Bakery": 1,
        "Factory": 1,
        "Farm": 1,
        "Bank": 1,
        f"{cookie_name.capitalize()} Forest": 1,
        "Auto Clicker": 1,
        "International Factories": 1,
        "International Banks": 1,
        "Crypto Currency": 1,
        f"{cookie_name.capitalize()} Machine 2.0":1
    }
    ach = []
    datecreated = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    clickcookielbls()
    autosave(True)
def newatm():
    global player_name
    global cagain
    global entpname
    if entpname.get() == "":
        return
    player_name = entpname.get().lower()
    exists = path.exists(f'extras\\profiles\\{player_name}.json')
    if exists is False:
        new()
    else:
        global error_canvas
        global errorpresent
        if errorpresent is True and cagain==0:
            canvas.delete(error_canvas)
        elif cagain==0:
            errorpresent = True
        error_canvas = canvas.create_image(270, 266, image=profilealrexistz, anchor=tk.CENTER)
        cagain +=1
        if cagain==1:
            root.after(3000, reserrorlabel)
        elif cagain==2:
            cagain=0
            new()
def save():
    if in_game is True:
        last_open = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        dictionary = dict(net_player_points=round(nwcookie), player_points=round(cookie), player_achievement=ach, shop_amount=amount_per_type, date_diff=str(last_open))
        with open(resource_path(f"extras/profiles/{player_name}.json"), 'w') as f:
            json.dump(dictionary, f)
def loade(e):
    load()
def load():
    global cookie
    global nwcookie
    global amount_per_type
    global player_name
    global ach
    global entpname
    global unlocked_buttons
    global cookie_name
    global initial_cookie_name
    global long_initial_cookie_name
    player_name = entpname.get().lower()
    if player_name=="":
        global dev_delete,dev_mode
        dev_delete+= 1 if dev_mode is False else 0
        if dev_delete==5:
            dev_mode=True
            dev_delete_bn = tk.Button(canvas, cursor="hand2", text="Delete ALL\nProfiles", command=dev_delete_prof, relief=tk.GROOVE,width=10,height=2)
            dev_delete_bn.place(x=270,y=450,anchor=tk.CENTER)
    else:
        exists = path.exists(f'profiles/{player_name}.json')
        if exists is True:
            with open(resource_path(f"profiles/{player_name}.json"), 'r') as f:
                dictionary = json.load(f)
            cookie = dictionary['player_points']
            nwcookie = dictionary['net_player_points']
            ach = dictionary['player_achievement']
            last_open = dictionary['date_diff']
            last_open = datetime.strptime(last_open, "%y-%m-%d %H:%M:%S")
            today = datetime.now()
            datediff = today - last_open
            datediffd = datediff.days
            datediffs = datediff.seconds
            diffs = datediffd*86400+datediffs
            amount_per_type = dictionary['shop_amount']
            clickcookielbls()
            cookie+=cookies_in_menu
            offlinecookies = cpsall * diffs/6
            if offlinecookies!=0:
                cookie = round(cookie + offlinecookies)
                pplaysound(message_audio,False)
                messagebox.showinfo(title=f"Congrats",message=f"You got {abbreviate_numbers(offlinecookies)} Cookies While you were away")
            root.after(60000, autosave)
        else:
            global error_canvas
            global errorpresent
            global cagain
            if cagain>0 or errorpresent is True:
                canvas.delete(error_canvas)
                cagain=0
            else:
                errorpresent = True
            error_canvas = canvas.create_image(270, 266, image=profilenotfoundpng, anchor=tk.CENTER)
            root.after(3000, reserrorlabel)
            return
def move_cookkie_note():
    global amount_cookie_move
    amount_cookie_move+=1
    canvas.move(canvas_image_cookie_menu,8,0)
    canvas.move(canvas_image_begin_button,0,-8)
    if amount_cookie_move>=45:
        global entpname
        global player_name_canvas
        global new_canvas
        global load_canvas,dev_delete,dev_mode
        dev_mode=False
        dev_delete=0
        canvas.delete(canvas_image_cookie_menu)
        canvas.delete(canvas_image_begin_button)
        player_name_canvas = canvas.create_image(270, 130, image=transparentbutton, anchor=tk.CENTER)
        new_canvas = canvas.create_image(195, 198, image=newbtnpng, anchor=tk.CENTER)
        load_canvas = canvas.create_image(345, 198, image=loadbtnpng, anchor=tk.CENTER)
        entpname = tk.Entry(canvas, width=30, borderwidth=0)
        entpname.place(x=270,y=140, anchor=tk.CENTER)
        canvas.config(cursor="")
        canvas.tag_bind(new_canvas, "<Button-1>", newe)
        canvas.tag_bind(load_canvas, "<Button-1>", loade)
        canvas.tag_bind(new_canvas, "<Enter>", new_load_enter)
        canvas.tag_bind(load_canvas, "<Enter>", new_load_enter)
        canvas.tag_bind(new_canvas, "<Leave>", new_load_leave)
        canvas.tag_bind(load_canvas, "<Leave>", new_load_leave)
    else:
        root.after(5, move_cookkie_note)
def move_cookkie(e):
    global clickedbeggin
    if clickedbeggin is False:
        move_cookkie_note()
    clickedbeggin=True
def jiggle_cookie():
    global jiggle_cookie_amount
    global cookies_in_menu
    if jiggle_cookie_amount<=8:
        canvas.move(canvas_image_cookie_menu,1,0)
    elif jiggle_cookie_amount<=24:
        canvas.move(canvas_image_cookie_menu, -1, 0)
    elif jiggle_cookie_amount<=32:
        canvas.move(canvas_image_cookie_menu, 1, 0)
    if jiggle_cookie_amount!=33:
        jiggle_cookie_amount+=1
        root.after(6, jiggle_cookie)
    else:
        jiggle_cookie_amount=1
        cookies_in_menu+=1
def jiggle_cookiee(e):
    global jiggle_cookie_amount
    pplaysound(crunch_audio,False)
    jiggle_cookie()
def folders_check():
    path_to_profile = resource_path("profiles")
    exists_profile = path.exists(path_to_profile)
    if exists_profile is False:
        os.mkdir(path_to_profile)

    path_to_settings = resource_path("user-settings.json")
    exists_settings = path.exists(path_to_settings)
    if exists_settings is False:
        save_settings(False,False,True)
def save_settings(music,sound,motion):
    dictionary = dict(music_mute=music,sounds_mute=sound,mootion=motion)
    with open(resource_path("user-settings.json"), 'w') as f:
        json.dump(dictionary, f)
def load_settings():
    global muted,mmuted,motion
    with open(resource_path("user-settings.json"), 'r') as f:
        dictionary = json.load(f)
    muted = dictionary["music_mute"]
    mmuted = dictionary["sounds_mute"]
    motion = dictionary["mootion"]
def close():
    try:
        save()
        print("saving..")
    finally:
        root.after(1000, root.destroy())
def main_menu(e, inmenu_or_no):
    if inmenu_or_no:
        canvas.destroy()
        main()
    else:
        global in_game
        canvas2.destroy()
        save()
        in_game=False
        main()
def main():
    global cookiecolor, acookiecolor, aacookiecolor, cookie_name, initial_cookie_name, long_initial_cookie_name, cookie_emoji
    global in_menu, in_game, errorpresent, achie_present,cookies_in_menu,cagain,jiggle_cookie_amount,amount_cookie_move
    root.geometry("540x540")

    cookiecolor = '#E6CEA0'
    acookiecolor = '#FDE2B0'
    aacookiecolor = '#FEEDCD'

    cookie_name = "cookie"
    initial_cookie_name = "CPS"
    long_initial_cookie_name = "Cookie Per Second"
    cookie_emoji = "🍪"

    in_menu = False
    in_game = False
    errorpresent = False
    achie_present = False
    cookies_in_menu = 0
    cagain = 0
    jiggle_cookie_amount = 1
    amount_cookie_move = 0

    global canvas, clickedbeggin, canvas_image_cookie_menu,canvas_image_begin_button
    canvas = tk.Canvas(root, bg=cookiecolor, width=540, height=540)
    canvas.pack()
    canvas_image_menu = canvas.create_image(270, 270, image=menu_start_image, anchor=tk.CENTER)
    canvas_image_cookie_menu = canvas.create_image(270, 270, image=cookie_menu_image, anchor=tk.CENTER)
    canvas_image_begin_button = canvas.create_image(270, 490, image=beginbutton, anchor=tk.CENTER)
    menu_ingame = canvas.create_image(530, 10, image=menu_ingame_img, anchor=tk.NE)

    canvas.tag_bind(menu_ingame, "<Button-1>", lambda e: menu_ingame_def_e(e, True))
    canvas.tag_bind(canvas_image_begin_button, "<Button-1>", move_cookkie)
    canvas.tag_bind(canvas_image_cookie_menu, "<Button-1>", jiggle_cookiee)
    canvas.tag_bind(canvas_image_begin_button, "<Enter>", new_load_enter)
    canvas.tag_bind(canvas_image_cookie_menu, "<Enter>", new_load_enter)
    canvas.tag_bind(menu_ingame, "<Enter>", new_load_enter)
    canvas.tag_bind(canvas_image_begin_button, "<Leave>", new_load_leave)
    canvas.tag_bind(canvas_image_cookie_menu, "<Leave>", new_load_leave)
    canvas.tag_bind(menu_ingame, "<Leave>", new_load_leave)
    clickedbeggin = False
if __name__ == "__main__":
    folders_check()
    load_settings()
    root = tk.Tk()

    WM_SETICON = 0x80
    ICON_SMALL = 0
    LR_LOADFROMFILE = 0x10  # Load the image from a file
    baseDir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(baseDir, "cookieclr.ico")
    root.iconbitmap(icon_path)

    def set_taskbar_icon(window_handle, icon_path):
        icon = ctypes.windll.user32.LoadImageW(
            None,
            ctypes.c_wchar_p(icon_path),
            ctypes.c_uint(1),  # IMAGE_ICON
            ctypes.c_int(16),  # Width
            ctypes.c_int(16),  # Height
            ctypes.c_uint(0x10)  # LR_LOADFROMFILE
        )
        ctypes.windll.user32.SendMessageW(
            window_handle,
            WM_SETICON,
            ICON_SMALL,
            icon
        )
    set_taskbar_icon(root.winfo_id(), icon_path)



    root.title("Cookie Clicker")
    root.resizable(tk.FALSE, tk.FALSE)
    root.protocol("WM_DELETE_WINDOW", close)

    timeit_time = timeit(stmt="a=27;b=8;c=a+b")
    print(timeit_time)
    cps_number, time_wait = timeit_def(timeit_time)

    Big_Names = [
        "",
        "thousand",
        "million",
        "billion",
        "trillion",
        "quadrillion",
        "quintillion",
        "sex-tillion",
        "septillion",
        "octillion",
        "nonillion",
        "decillion",
        "undecillion",
        "duodecillion",
        "tredecillion",
        "quattuordecillion",
        "quindecillion",
        "sex-decillion",
        "septendecillion",
        "sctodecillion",
        "novemdecillion",
        "vigintillion",
        "unvigintillion",
        "duovigintillion",
        "trevigintillion",
        "quattuorvigintillion",
        "quinvigintillion",
        "sexvigintillion",
        "septvigintillion",
        "octovigintillion",
        "nonvigintillion",
        "trigintillion",
        "untrigintillion",
        "duotrigintillion",
    ]

    click_audio = resource_path('Click_sound.wav')
    crunch_audio = resource_path('Crunch.wav')
    message_audio = resource_path('Message.wav')

    no_motion_cookie = ImageTk.PhotoImage(file=resource_path('cookie no motion.png'))
    motion_cookie = ImageTk.PhotoImage(file=resource_path('cookie motion.png'))
    close_btn = ImageTk.PhotoImage(file=resource_path('close btn mini.png'))
    mmuted_on_png = ImageTk.PhotoImage(file=resource_path('music muted on mini.png'))
    mmuted_off_png = ImageTk.PhotoImage(file=resource_path('music muted off mini.png'))
    muted_on_png = ImageTk.PhotoImage(file=resource_path('muted on mini.png'))
    muted_off_png = ImageTk.PhotoImage(file=resource_path('muted off mini.png'))
    menu_ingame_img = ImageTk.PhotoImage(file=resource_path('house.png'))
    menu_start_image = ImageTk.PhotoImage(file=resource_path("cookestartscreennocookienobegin.png"))
    cookie_menu_image = ImageTk.PhotoImage(file=resource_path("cookemenu450.png"))
    beginbutton = ImageTk.PhotoImage(file=resource_path("beginbutton.png"))
    transparentbutton = ImageTk.PhotoImage(file=resource_path("transparent rounded button.png"))
    loadbtnpng = ImageTk.PhotoImage(file=resource_path("loadbtn.png"))
    newbtnpng = ImageTk.PhotoImage(file=resource_path("newbtn.png"))
    profilenotfoundpng = ImageTk.PhotoImage(file=resource_path("profile not found.png"))
    profilealrexistz = ImageTk.PhotoImage(file=resource_path("profile alr existz.png"))

    used = False
    if used:
        50, 50 == close_btn.height(), close_btn.width()
        50, 50 == mmuted_off_png.height(), muted_off_png.width()
        50, 50 == mmuted_on_png.height(), muted_on_png.width()
        50, 50 == muted_off_png.height(), muted_off_png.width()
        50, 50 == muted_on_png.height(), muted_on_png.width()
        40, 40 == menu_ingame_img.height(), menu_ingame_img.width()
        540, 540 == menu_start_image.width(), menu_start_image.height()
        450, 450 == cookie_menu_image.width(), cookie_menu_image.height()
        300, 63 == beginbutton.width(), beginbutton.height()
        300, 63 == transparentbutton.width(), transparentbutton.height()
        125, 63 == loadbtnpng.width(), loadbtnpng.height()
        125, 63 == newbtnpng.width(), newbtnpng.height()
    main()
    p = PyAudio()
    count = 0
    no_current_music = False
    music(True)

    root.mainloop()