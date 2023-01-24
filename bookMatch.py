import os
import sys
import math
from tkinter import messagebox
from tkinter import *
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from PIL import ImageTk, Image

rf = RandomForestRegressor(n_estimators=10, random_state=42)                        #RandomForestRegressor olusturulmasi

books = pd.read_csv("Books.csv")                                                    #Siteden cektigimiz kitap bilgilerini dataframe'e aktarıyoruz
books.drop("Unnamed: 0", axis=1, inplace=True)

booksDummies = pd.DataFrame(books)                                                  

userRatings = booksDummies["UserRating"]
ratings = booksDummies["Rating"]
booksDummies.drop(["Title", "Rating", "UserRating"], axis=1, inplace=True)          #Title modelde kullanilmadigi icin ve rating ve userRating'in get_dummies() ile degismesini istemedigimiz icin cikariyoruz
booksDummies = pd.get_dummies(booksDummies, drop_first=True)                        #Kitaplari tutan dataframe'i modelde kullanabilmek icin get_dummies() fonksiyonu kullanıyoruz
booksDummies["UserRating"] = userRatings                                            #Olusturulan dataframe'e rating ve userRating'leri geri ekliyoruz
booksDummies["Rating"] = ratings

modelDF = pd.DataFrame(columns=booksDummies.columns)                                #Oylanan kitaplari modelde egitebilmek icin olusturulan dataframe             

root = Tk()                                                                         #Ana Ekran
root.geometry("1000x600")                                               
root.iconbitmap(os.path.join(sys.path[0], 'bookicon.ico'))                          #Her bilgisayara uyumlu calisacak sekilde icon eklenmesi
root.title("BookMatch")
root.configure(bg = '#262423')

categoryList = ["HEPSİ", "ÇOCUK", "POLİSİYE", "İŞ KİTAPLARI", "KURGU DIŞI", "BİLİM KURGU & FANTASTİK", "TARİH", "KLASİKLER", "ŞİİR", "ÖYKÜ", "KİŞİSEL GELİŞİM"]      

titleVar = StringVar()
authorVar = StringVar()
categoryVar = StringVar()               #Label'larin guncellenebilmesi icin olusturulan degiskenler
tag0Var = StringVar()
tag1Var = StringVar()
ratingVar = StringVar()

booksList = []
predicted = []
list = []                               #Gerekli listelerin olusturulmasi
listDummies = []
suggestList = []
rateList = []

def filter():                                                                       #Kategoriye gore filtreleme yaptiginda calisan fonksiyon
    selectedCategory = clicked.get()                                                #Secilen kategorinin alinmasi
    list.clear()
    for i in range(len(books)):                                                     #Kategoriye gore kitaplarin listeye eklenmesi
        if(selectedCategory == "HEPSİ"):
            list.append(books.iloc[i])
        elif books.iloc[i]["Category"] == selectedCategory:
            list.append(books.iloc[i])

    lb.delete(first=0, last=END)                                                    #Guncellenen listeye gore ana ekranda gosterilen kitaplarin bulundugu listboxun guncellenmesi
    for i in range(len(list)):
        string1 = list[i]["Author"]
        string2 = list[i]["Title"]

        string = f"{string1:<37}{string2}"                                          
        lb.insert(END, string)      
        
def disable_event():                                                                #Acilan pencerenin X tusu ile kapatilmasinin engellenmesini saglayan fonksiyon
   pass

def open():                                                                         #Listbox'tan kitap secilip oy ver butonuna basildiginda calisan fonksiyon
    buttonRate["state"] = DISABLED
    buttonSuggest["state"] = DISABLED                                               #Ana Ekrandaki butonlarin disabled edilmesi
    selected = lb.curselection()                                                    #Listbox'tan secilen kitabin indisinin alinmasi

    if not selected:
        messagebox.showerror("Uyarı", "Önce listeden kitap seçin!")                 #Herhangi bir kitap secmediyse uyari penceresinin acilmasi
        buttonRate["state"] = NORMAL
        buttonSuggest["state"] = NORMAL

    else:
        secondWindow = Toplevel()                                                                                       #Kitaba ait bilgilerin ve kitaba oy verilecek alanin bulundugu pencerenin olusturulmasi
        secondWindow.geometry("470x600")
        secondWindow.configure(bg = '#262423')
        secondWindow.iconbitmap(os.path.join(sys.path[0], 'bookicon.ico'))
        panel = Label(secondWindow, image = img, bg='#262423')
        panel.place(relx=0.30, rely=0.1, relwidth=0.07, relheight=0.07)
        label = Label(secondWindow, text="BookMatch", font=('Gill Sans MT' ,20, 'bold'), bg="#262423", fg="#d15802")
        label.place(relx=0.385, rely=0.1, relwidth=0.34, relheight=0.07)
        secondWindow.protocol("WM_DELETE_WINDOW", disable_event)                                                        #Acilan pencerenin X tusu ile kapatilmasinin engellenmesi
        
        titleStr = ""
        if len(books.iloc[selected[0]]["Title"]) > 33:
            titleStr += list[selected[0]]["Title"][:33] + "..."                                                         #Kitap ismi cok uzun ise ismin yarida kesilip ... ile gosterilmesi
        else:
            titleStr += list[selected[0]]["Title"]

        labelTitle1 = Label(secondWindow, text="Kitap İsmi: "+titleStr, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")                                  #Kitap bilgilerini tutan label'lar
        labelTitle1.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.05)
        labelAuthor = Label(secondWindow, text="Yazar: "+list[selected[0]]["Author"], font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
        labelAuthor.place(relx=0.1, rely=0.30, relwidth=0.8, relheight=0.05)
        labelCategory = Label(secondWindow, text="Kategori: "+list[selected[0]]["Category"], font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
        labelCategory.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.05)
        labelTag0 = Label(secondWindow, text="1. Etiket: "+list[selected[0]]["Tag0"], font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
        labelTag0.place(relx=0.1, rely=0.40, relwidth=0.8, relheight=0.05)
        labelTag1 = Label(secondWindow, text="2. Etiket: "+list[selected[0]]["Tag1"], font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
        labelTag1.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.05)
        labelRating = Label(secondWindow, text="Genel Puanlama: "+str(list[selected[0]]["Rating"]), font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
        labelRating.place(relx=0.1, rely=0.50, relwidth=0.8, relheight=0.05)

        ratingSlider = Scale(secondWindow, from_=0.00, to=5.00, orient=HORIZONTAL, resolution=0.01, highlightthickness=0, bg="#262423", fg="#ffffff", font=('Gill Sans MT' ,10, 'bold'))            #Oy verme slider
        ratingSlider.place(relx=0.2, rely=0.65, relwidth=0.6, relheight=0.08)
        buttonRate2 = Button(secondWindow, text="OY VER", command=lambda: rating(ratingSlider, secondWindow, selected), font=('Gill Sans MT' ,10, 'bold'), bg="#d15802", fg="#ffffff")              #Kitaba oy verme button'u
        buttonRate2.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.05)
        buttonCancel = Button(secondWindow, text="İPTAL ET", command=lambda: cancel(secondWindow), font=('Gill Sans MT' ,10, 'bold'), bg="#d15802", fg="#ffffff")                                   #Kitaba oy vermeyip pencereyi kapatan button
        buttonCancel.place(relx=0.4, rely=0.81, relwidth=0.2, relheight=0.05)
        label = Label(secondWindow, text="20011040 Elif Sena YILMAZ / 19011040 Engin MEMİŞ", font=('Gill Sans MT' ,10), bg="#262423", fg="#6e6965")
        label.place(relx=0.5, rely=0.99, anchor=S)

def cancel(window):                                                                          #Pencereyi kapatan fonksiyon
    buttonRate["state"] = NORMAL
    buttonSuggest["state"] = NORMAL
    window.destroy()

def rating(ratingSlider, secondWindow, selected):                                               #Kitaba ana ekrandan oy verdiğinde calisan fonksiyon
    userRating = ratingSlider.get()
    index = books[(books['Title'] == list[selected[0]]["Title"])].index                         #Kitabin listboxta bulundugu indise gore ana listede indisinin bulunmasi
    count = len(modelDF)
    modelDF.loc[count] = booksDummies.iloc[index].values[0]                                     #Egitim yapilacak dataframe'e oy verilen kitabin eklenmesi
    modelDF.at[count, "UserRating"] = userRating

    books.drop(index, inplace=True)                                                             #Oylanan kitabin tekrardan gosterilmemesi icin listeden cikarilmasi
    booksDummies.drop(index, inplace=True)

    buttonRate["state"] = NORMAL
    if len(modelDF) > 4:                                                                        #En az 5 kitaba oy vermeden kitap oner tusunun basilmasinin engellenmesi
        buttonSuggest["state"] = NORMAL
    
    list.pop(selected[0])                                                                       #Ana ekranda gosterilen listbox'tan oy verilen kitabin cikarilmasi
    lb.delete(first=0, last=END)    
    for i in range(len(list)):                                                                  #Listbox'un guncellenmesi
        string1 = list[i]["Author"]
        string2 = list[i]["Title"]

        string = f"{string1:<37}{string2}"
        lb.insert(END, string)
    secondWindow.destroy()

def suggestRating(ratingSlide, window):                                                         #Onerilen kitaba oy verildiginde calisan fonksiyon
    index = predicted.index(max(predicted))
    count = len(modelDF)
    modelDF.loc[count] = booksDummies.iloc[index].values[0]                                     #Onerilen kitabin egitilecek dataframe'e eklenmesi
    rate = ratingSlide.get()
    modelDF.at[count, "UserRating"] = rate

    i = 0
    flag = True
    while i < len(list) and flag:
        if books.iloc[index]["Title"] == list[i]["Title"]:                                      #Onerilen kitabin listbox'ta indisinin bulunmasi
            flag = False
            list.pop(i)                                                                         #Onerilen kitabin listbox'tan cikarilmasi
        i += 1

    lb.delete(first=0, last=END)    
    for i in range(len(list)):                                                                  #Listbox'un guncellenmesi
        string1 = list[i]["Author"]         
        string2 = list[i]["Title"]

        string = f"{string1:<37}{string2}"
        lb.insert(END, string)
    
    error = errorRate.get()                                                                     #Root Mean Squared Error hesaplanmasi
    if error == "":
        error = 0.0 
    else:
        splitString = error.split(': ')
        error = float(splitString[1])
    total = error * error * len(suggestList)

    total = total + (rate - predicted[index][0]) * (rate - predicted[index][0])

    errorRate.set("Hata Oranı: " + str(round(math.sqrt(total / (len(suggestList) + 1)), 2)))            #Hata oraninin ekranda gosterilmesi

    suggestList.append(predicted[index][0])
    rateList.append(rate)

    books.drop(books.index[index], inplace=True)                                                #Onerilen kitaplarin ana listeden cikarilmasi
    booksDummies.drop(booksDummies.index[index], inplace=True)
    predicted.clear()
    booksList.pop(index)
    buttonSuggest["state"] = NORMAL
    buttonRate["state"] = NORMAL
    window.destroy()

def suggest():                                                                                  #Kitap Oner butonuna basildiginda calisan fonksiyon
    buttonSuggest["state"] = DISABLED
    buttonRate["state"] = DISABLED
    predictList = booksDummies.drop("UserRating", axis=1)

    y = np.array(modelDF["UserRating"])                                                         #Egitilecek modelde tahmin edilmesini istedigimiz sutunun ayrilmasi
    x = np.array(modelDF.drop("UserRating",axis=1))                                             #Geri kalan ozelliklerin ayrilmasi

    rf.fit(x, y)                                                                                #Modelin olusturulması

    predictList = np.array(predictList)                                                         
    for i in range(len(predictList)):
        predict = rf.predict([predictList[i]])                                                  #Butun kitaplarin olusturulan modele gore puaninin tahmin edilmesi
        predicted.append(predict)
    
    for i in range(len(books)):
        booksList.append(books.iloc[i])

    index = predicted.index(max(predicted))                                                     #En yuksek puana sahip kitabin indisinin bulunmasi

    sugWindow = Toplevel()
    sugWindow.geometry("470x600")
    sugWindow.protocol("WM_DELETE_WINDOW", disable_event)                                                       #Kitap Oneri penceresinin olusturulmasi
    sugWindow.configure(bg = '#262423')
    sugWindow.iconbitmap(os.path.join(sys.path[0], 'bookicon.ico'))
    panel = Label(sugWindow, image = img, bg='#262423')
    panel.place(relx=0.30, rely=0.1, relwidth=0.07, relheight=0.07)
    label = Label(sugWindow, text="BookMatch", font=('Gill Sans MT' ,20, 'bold'), bg="#262423", fg="#d15802")
    label.place(relx=0.385, rely=0.1, relwidth=0.34, relheight=0.07)

    titleStr = ""
    if len(booksList[index]["Title"]) > 30:
        titleStr += booksList[index]["Title"][:30] + "..."
    else:
        titleStr += booksList[index]["Title"]
                                                                                                                
    titleVar.set("Kitap İsmi: " + titleStr)                                                                             #Label'larin en yuksek puana sahip kitabin bilgilerine gore guncellenmesi
    authorVar.set("Yazar: " + booksList[index]["Author"])
    categoryVar.set("Kategori: " + booksList[index]["Category"])
    tag0Var.set("1. Etiket: " + booksList[index]["Tag0"])
    tag1Var.set("2. Etiket: " + booksList[index]["Tag1"])
    ratingVar.set("Genel Puanlama: " + str(booksList[index]["Rating"]))

    labelTitle = Label(sugWindow, textvariable= titleVar, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
    labelTitle.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.05)
    labelAuthor = Label(sugWindow, textvariable=authorVar, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
    labelAuthor.place(relx=0.1, rely=0.30, relwidth=0.8, relheight=0.05)
    labelCategory = Label(sugWindow, textvariable=categoryVar, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
    labelCategory.place(relx=0.1, rely=0.35, relwidth=0.8, relheight=0.05)
    labelTag0 = Label(sugWindow, textvariable=tag0Var, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
    labelTag0.place(relx=0.1, rely=0.40, relwidth=0.8, relheight=0.05)
    labelTag1 = Label(sugWindow, textvariable=tag1Var, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
    labelTag1.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.05)
    labelRating = Label(sugWindow, textvariable=ratingVar, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
    labelRating.place(relx=0.1, rely=0.50, relwidth=0.8, relheight=0.05)

    labelRating = Label(sugWindow, text="Bu kitap önerisini nasıl buldunuz?", font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
    labelRating.place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.05)
    ratingSlide = Scale(sugWindow, from_=0.00, to=5.00, resolution=0.01, orient=HORIZONTAL, highlightthickness=0, bg="#262423", fg="#ffffff", font=('Gill Sans MT' ,10, 'bold'))
    ratingSlide.place(relx=0.2, rely=0.71, relwidth=0.6, relheight=0.08)
    label = Label(sugWindow, text="20011040 Elif Sena YILMAZ / 19011040 Engin MEMİŞ", font=('Gill Sans MT' ,10), bg="#262423", fg="#6e6965")
    label.place(relx=0.5, rely=0.99, anchor=S)

    suggestButtonRate = Button(sugWindow, text="OY VER", padx=4, pady=2, command=lambda:suggestRating(ratingSlide, sugWindow), font=('Gill Sans MT' ,10, 'bold'), bg="#d15802", fg="#ffffff")
    suggestButtonRate.place(relx=0.4, rely=0.80, relwidth=0.2, relheight=0.05)



frameUst = Frame(root, bg="#262423")                                                                    #Frame'lerin olusturulmasi
frameUst.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.08)

frameMid = Frame(root, bg="#262423")
frameMid.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.7)

clicked = StringVar()                                                                                   #Kategori menusunde varsayilan olarak hepsi ayarlanmasi
clicked.set("HEPSİ")

button = Button(frameUst, text="FİLTRELE", padx=4, pady=2, command=filter, font=('Gill Sans MT' ,10, 'bold'), bg="#d15802", fg="#ffffff")                   #Gerekli butonlarin olusturulmasi
button.pack(padx=5, pady=5, side=RIGHT)

buttonRate = Button(root, text="OY VER", padx=4, pady=2, command=open, font=('Gill Sans MT' ,10, 'bold'), bg="#d15802", fg="#ffffff")
buttonRate.place(relx=0.9, rely=0.87, anchor=SE)

buttonSuggest = Button(root, text="KİTAP ÖNER", padx=4, pady=2, command=suggest, font=('Gill Sans MT' ,10, 'bold'), bg="#d15802", fg="#ffffff")
buttonSuggest.place(relx=0.1, rely=0.87, anchor=SW)
buttonSuggest["state"] = DISABLED

category = OptionMenu(frameUst, clicked, *categoryList)                                                             #Kategori menusunun olusturulmasi
category.pack(padx = 5, pady = 5, side=RIGHT)
category.config(font=('Gill Sans MT' ,10, 'bold'), bg="#d15802", fg="#ffffff")

img = ImageTk.PhotoImage(Image.open("book.png"))                                                                            #Icon olusturulmasi
panel = Label(frameUst, image = img, bg='#262423')
panel.pack(padx = 5, pady = 5, side=LEFT)
label = Label(frameUst, text="BookMatch", font=('Gill Sans MT' ,20, 'bold'), bg="#262423", fg="#ffffff")
label.pack(padx = 5, pady = 5, side=LEFT)

errorRate = StringVar()                                                                                                 #Hata Oranini yazacak olan degiskenin olusturulmasi
errorRate.set("")

errorLabel = Label(root, textvariable=errorRate, font=('Gill Sans MT' ,12, 'bold'), bg="#262423", fg="#ffffff")
errorLabel.place(relx=0.5, rely=0.86, anchor=S)

label = Label(root, text="20011040 Elif Sena YILMAZ / 19011040 Engin MEMİŞ", font=('Gill Sans MT' ,10), bg="#262423", fg="#6e6965")
label.place(relx=0.5, rely=0.99, anchor=S)


sbb = Scrollbar(frameMid)                                                                   #Listbox'u kaydiracak scrollbar'larin eklenmesi
sbb.pack(side=RIGHT, fill=Y)

sbb2 = Scrollbar(frameMid, orient=HORIZONTAL)
sbb2.pack(side=BOTTOM, fill=X)

lb = Listbox(frameMid, width=100, height=20, yscrollcommand=sbb.set , font=('Courier New' ,10, 'bold'), bg="#383838", fg="#ffffff", selectbackground='#d15802', activestyle='none')         #Kitaplarin icinde bulundugu listbox'un olusturulmasi
lb.pack(side=LEFT, fill=BOTH, expand=True)

for i in range(len(books)):
    string1 = books.iloc[i]["Author"]
    string2 = books.iloc[i]["Title"]                                                #Listbox'un icini kitap bilgileri ile doldurulmasi

    string = f"{string1:<37}{string2}"
    lb.insert(END, string)
    list.append(books.iloc[i])

menu = frameMid.nametowidget(category.menuname) 
menu.config(font=('Gill Sans MT' ,10, 'bold'), bg="#262423", fg="#ffffff", activebackground="#d15802", activeforeground="#ffffff")
lb.config(yscrollcommand=sbb.set , xscrollcommand=sbb2.set)
sbb.config(command=lb.yview)
sbb2.config(command=lb.xview)

root.mainloop()