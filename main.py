# -*- coding: utf-8 -*-
"""
Created on Fri May  3 22:32:13 2019

@author: m4mizery
"""

#from bs4 import BeautifulSoup #look through html
# 
#import requests #interact w http
 
import tkinter as tk

import smtplib

from threading import Timer

from parse_price_mlo import uniqlo_pp, hm_pp, madewell_pp, allsaints_pp


def pp(url):
    url_dict = {"www.uniqlo.com":uniqlo_pp, 
                "www.madewell.com":madewell_pp, 
                "www2.hm.com":hm_pp, 
                "www.us.allsaints.com":allsaints_pp
                }
    for k, v in url_dict.items():
        if k in url:
            return v(url)
       

curr_s = "store name here" 
"""FUNCTIONS FOR UI BASE SETUP"""  
def FrameWidth(event):
    canvas_width = event.width
    canvas.itemconfig(canvas_f, width = canvas_width)
    
def OnFrameConfigure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
  
def raise_frame(frame):
    global curr_s
    global curr_f
    frame.tkraise()
    curr_f = frame
    curr_s = stores[frame][0]
    store_l.config(text=curr_s)
    
    
"""UI MAIN WINDOW BASE SETUP"""    
root = tk.Tk()
root.title('lovely price tracker')
root.geometry("800x550")
menubar = tk.Menu(root)

store_l = tk.Label(root, text=curr_s, font='size, 12')
store_l.pack()

"""CREATE ARRAY TO STORE TEXTBOX ROWS & ETC"""
textbox_rows = []
on_sale = {}
on_sale_changed = False
curr_prod = []

"""REMOVE ROWS USING X BUTTON"""  
def remove_textbox(row):
    row.destroy()
    textbox_rows.remove(row)
 
"""CREATE NEW TEXTBOX ROW W/ NEW BUTTON"""
def textbox(url = 'ENTER URL'):
    #stores = {f1:("Uniqlo", "www.uniqlo.com"), f2:("Madewell", "www.madewell.com"), f3:("H&M", "www2.hm.com")}
    for k, v in stores.items():
        if v[1] in url:
            global curr_f
            curr_f = k
    f = tk.Frame(curr_f, bd=1, relief="sunken")
    f.pack_propagate()#resized if not large enough to hold all the child widgets
    f.pack(side="top", pady=5)
   
    subf2 = tk.Frame(f)
    subf2.pack(side="top")
    L4 = tk.Label(subf2, text="product")
    L4.pack(side=tk.LEFT)
    E4 = tk.Entry(subf2, bd =0, width=40)
    E4.pack(side=tk.LEFT)
    L2 = tk.Label(subf2, text="standard")
    L2.pack(side=tk.LEFT)
    E2 = tk.Entry(subf2, bd =0)
    E2.pack(side=tk.LEFT)
    L3 = tk.Label(subf2, text="sale")
    L3.pack(side=tk.LEFT)
    E3 = tk.Entry(subf2, bd =0)
    E3.pack(side=tk.LEFT)
   
    subf1 = tk.Frame(f)
    subf1.pack(fill='x', anchor="w")
    L1 = tk.Label(subf1, text="URL")
    L1.pack(side=tk.LEFT)
    entryText = tk.StringVar()
    E1 = tk.Entry(subf1, bd =3, width=70, textvariable=entryText)
    entryText.set(url)
    E1.pack(side=tk.LEFT)

    BX = tk.Button(subf1, text = "X", command = lambda: remove_textbox(f))
    BX.pack(side=tk.RIGHT)
   
    textbox_rows.append(f)

"""BUTTON FOR NEW"""
B = tk.Button(root, text = "add product", command = textbox)
B.pack(side=tk.TOP)


"""---CANVAS, SCROLLBAR, STACKED FRAMES INSIDE CANVAS---"""
# --- create canvas & scrollbar container ---
cContainer = tk.Frame(root, bg="red")
cContainer.pack(side="top", pady=10)

# --- create canvas with scrollbar ---
canvas = tk.Canvas(cContainer, width=700, height=350)
canvas.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)

fscrollbar = tk.Scrollbar(cContainer, orient = "vertical", command=canvas.yview)
fscrollbar.pack(side=tk.RIGHT, fill='y')

canvas.config(yscrollcommand = fscrollbar.set)

# --- initialize frame in canvas ---
fContainer = tk.Frame(canvas)
fContainer.grid_rowconfigure(0, weight=1)
fContainer.grid_columnconfigure(0, weight=1)
canvas_f = canvas.create_window((0,0), window=fContainer, anchor='nw')

# --- put working frames in canvas frame ---
f1 = tk.Frame(fContainer)
f2 = tk.Frame(fContainer)
f3 = tk.Frame(fContainer)
f4 = tk.Frame(fContainer)

stores = {f1:("Uniqlo", "www.uniqlo.com"), 
          f2:("Madewell", "www.madewell.com"), 
          f3:("H&M", "www2.hm.com"), 
          f4:("All Saints", "www.us.allsaints.com")
          }
 
for f in (f1, f2, f3, f4):
    f.grid(row=0, column=0, sticky="nsew")
    
# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
fContainer.bind("<Configure>", OnFrameConfigure)
canvas.bind("<Configure>", FrameWidth)

""" --- MENU CONFIGURATION --- """
# --- add commands to the menu buttons ---
menubar.add_command(label=stores[f1][0], command=lambda:raise_frame(f1))
menubar.add_command(label=stores[f2][0], command=lambda:raise_frame(f2))
menubar.add_command(label=stores[f3][0], command=lambda:raise_frame(f3))
menubar.add_command(label=stores[f4][0], command=lambda:raise_frame(f4))

# display the menu & top frame
root.config(menu=menubar)
raise_frame(f1)


"""LOAD FILE AT START"""
try:
    with open('price.txt', 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]    
    for c in content[2:]:
        if c[0:4] == "http":
            textbox(c)
        else:
            on_sale.update({c:0})
    print("load on_sale", on_sale)
except FileNotFoundError:
    content = []
    

"""GET INFO FROM ENTRY BOXES"""
def gettext():
    global on_sale_changed
    global curr_prod
    for row in textbox_rows:
        URLentry = row.winfo_children()[1].winfo_children()[1]
        getURL = URLentry.get() 
        try:
            parsed_price = pp(getURL)
            product = row.winfo_children()[0].winfo_children()[1]
            productName = parsed_price[2]
            product.delete(0, tk.END)
            product.insert(0, productName)
            curr_prod.append(productName)
            
            standard = row.winfo_children()[0].winfo_children()[3]
            sale = row.winfo_children()[0].winfo_children()[5]
            if parsed_price[1] == False:
                standardPrice = parsed_price[0]
                standard.delete(0, tk.END)
                standard.insert(0, standardPrice)
                sale.delete(0, tk.END)
                sale.insert(0, "--")
                if productName in on_sale:
                    on_sale.pop(productName)
            else:                
                salePrice = parsed_price[0]
                sale.delete(0, tk.END)
                sale.insert(0, salePrice)
                standardPrice = parsed_price[3]
                standard.delete(0, tk.END)
                standard.insert(0, standardPrice)
                if productName not in on_sale:
                    on_sale.update({productName:salePrice})
                    on_sale_changed = True
                #for products that are already on sale and becomes even lower priced
                if productName in on_sale and on_sale[productName] > salePrice:
                    on_sale.update({productName:salePrice})
                    on_sale_changed = True
        except Exception:
            product = row.winfo_children()[0].winfo_children()[1]
            productName = "???"
            product.delete(0, tk.END)
            product.insert(0, productName)

            
"""EMAIL FRAME"""
ef = tk.Frame(root)
ef.pack(side="bottom", anchor="w", padx=5, pady=10)
ef.pack_propagate()
L1 = tk.Label(ef, text="e-mail")
L1.pack(side=tk.LEFT)
def emailbox(eetext = "ENTER EMAIL"):

    eeText = tk.StringVar()
    E1 = tk.Entry(ef, bd =5, textvariable = eeText)
    if content and '@' in content[1]:
        eeText.set(content[1])#from save file
    else:
        eeText.set(eetext)
    E1.pack(side=tk.LEFT)

emailbox()


"""SEND AN EMAIL"""
def sendemail():
    global on_sale_changed
    if on_sale_changed:
        ee = ef.winfo_children()[1].get()
        gmail_user = 'add email here'  
        gmail_password = 'add password here'
    
        sent_from = gmail_user  
        to = ee 
        
        s = ''
        for k, v in on_sale.items():
#            if v == 0: #does not notify in new email if something else is already on sale
#                continue
            temp = k + " on sale -> " + str(v)
            s += temp + '\n'
            
        subject = 'something is on sale'  
        body = s
        
        email_text = 'Subject: {}\n\n{}'.format(subject, body)
        header = 'To:' + to + '\n' + 'From: ' + sent_from + '\n'        
        email_text = header + email_text
        
        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()
            
            print('Email sent!')
            vis=tk.Label(root, text='Email sent!', font=("Arial", 12))
            vis.place(x=250,y=510)
            vis.after(3000, lambda: vis.destroy())
            on_sale_changed = False
            print(on_sale)                        
        except:  
            print('Something went wrong...')
            vis=tk.Label(root, text='Something went wrong...', font=("Arial", 12))
            vis.place(x=250,y=510)
            vis.after(3000, lambda: vis.destroy())
                    
    else:
        print('nothing on sale')
        vis=tk.Label(root, text='nothing on sale', font=("Arial", 12))
        vis.place(x=250,y=510)
        vis.after(3000, lambda: vis.destroy())

        
def sendnow():
    global on_sale_changed
    if on_sale == {}:
        on_sale_changed = False
    else:
        on_sale_changed = True
    sendemail()

sendB = tk.Button(ef, text = "send", command = sendnow)
sendB.pack(padx=5)


"""OPTION MENU FOR TIMED REFRESH"""
sf = tk.Frame(root)
sf.pack(side="bottom", anchor="e", padx=5, pady=10)
sf.pack_propagate()

OPTIONS = ["03 hr","06 hr","12 hr","24 hr"] #etc

hr = tk.StringVar(sf)
if content:
    hr.set(content[0]) #from save file
else:
    hr.set(OPTIONS[0]) # default value

hrM = tk.OptionMenu(sf, hr, *OPTIONS)
hrM.pack(side=tk.RIGHT)
hrL = tk.Label(sf, text="refresh")
hrL.pack(side=tk.RIGHT)

"""SET TIMER INTERVAL"""
def interval(email = True):
    global t 
    ti = int(hr.get()[:2])
    t = Timer(ti * 60 * 60, interval)
    t.start() # called every minute
    gettext()
    if email:
        sendemail()

interval(False)

"""SUBMIT BUTTON"""
def updateT():
    global t
    #If the interval changes, stop the timer, change sleep, and then start a new thread. This would be attached to an event on the text box.
    t.cancel()    
    interval(False)
    save()

submit = tk.Button(sf, text="submit", command=updateT)
submit.pack(side=tk.RIGHT)

def cleansave(): #deletes missing products from save file
    on_sale_k = list(on_sale.keys())
    miss_prod = [i for i in on_sale_k if i not in curr_prod]
    #print(miss_prod)
    for miss in miss_prod:
        on_sale.pop(miss)

def save():
    print("don't look for me")
    cleansave()
    file = open('price.txt', 'w') #write permission
    savetxt = ''
    savetxt += str(hr.get()) + "\n" #save optionmenu
    savetxt += str(ef.winfo_children()[1].get()) + "\n" #save email 
    for row in textbox_rows:
        URLentry = row.winfo_children()[1].winfo_children()[1]
        getURL = URLentry.get()
        if getURL[0:4] == "http":
            savetxt += getURL + '\n'
    for k in on_sale.keys():
        savetxt += str(k) + '\n'
    file.write(savetxt)
    file.close()
        
def on_closing():
    save()
    print("GOOD BYE WORLD")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


# --- start program (puts above script into a loop) ---
root.mainloop()
