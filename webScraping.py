from bs4 import BeautifulSoup
import requests
import pandas as pd

categories = {1: "COCUK", 3: "POLISIYE", 4: "IS KITAPLARI", 6: "KURGU DISI", 7: "BILIM KURGU & FANTASTIK", 8: "TARIH", 9: "KLASIKLER", 10: "SIIR", 11: "OYKU", 12: "KISISEL GELISIM"}       #Siteden cekilecek kategorilerin sitedeki indislerinin olusturulmasi
indexList = list(categories.keys())

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}   
linkHeader = "https://www.storytel.com"

df = pd.DataFrame(columns=["Title", "Author", "Category", "Tag0", "Tag1", "Rating", "UserRating"])                  #Kitap bilgilerinin cekecegimiz dataframe'in olusturulmasi

count = 0
for categoryNumber in indexList:
    for bound in range(0, 100, 50):                                                             #Her kategoriden 100 tane kitap bilgisinin cekilmesi
        requestLink = f"https://www.storytel.com/tr/tr/gridSmartList.action?orderBy=MOST_LISTENED&filterKeys=CATEGORY,NOT_SEASON&filterValues={categoryNumber},1,19&start={bound}&hits=50&sorting=0"        #Kategorilerin indisinin link haline getirilmesi
        r = requests.get(requestLink)                                                       #Siteye request yollanmasi
        soup = BeautifulSoup(r.content, "html.parser")

        books = soup.find_all("div", attrs={"class":"gridItem"})

        for book in books:                                                                  #Kitaplarin bilgilerinin uygun sekilde cekilmesi
            bookLink = book.find("div", attrs={"class":"gridCover"})
            linkTails = bookLink.a.get("href")
            link = linkHeader + linkTails

            details = requests.get(link, headers=header)
            detailSoup = BeautifulSoup(details.content, "html.parser")

            bookInfo = {}
            desc = detailSoup.find(attrs={"class":"book-info"})
            if desc != None:
                author = desc.a.text
                title = detailSoup.find("h1", attrs={"class":"title"}).text

                infoList = detailSoup.find("dl", attrs={"class":"info-list"})
                info_term = infoList.find_all("dt", attrs={"class":"info-term"})
                info_def = infoList.find_all("dd", attrs={"class":"info-def"})
                rate = info_def[0].text[1:-1]

                tagList = detailSoup.find("ul", attrs={"class":"tag-list"})
                if tagList != None:
                    tags = tagList.find_all("li", attrs={"class":"tag"})
                    if(len(tags) > 1):
                        tag0 = tags[0].text[:-1]
                        tag1 = tags[1].text[:-1]

                        bookInfo["Title"] = title                                                       #Cekilen bilgilerin listeye koyulmasi
                        bookInfo["Author"] = author
                        bookInfo["Category"] = categories[categoryNumber]
                        bookInfo["Tag0"] = tag0
                        bookInfo["Tag1"] = tag1
                        bookInfo["Rating"] = rate
                        bookInfo["UserRating"] = 0

                        df.loc[count] = bookInfo                        #Listenin dataframe'e eklenmesi
                        count += 1

df.to_excel("Books.csv")                                                #Olusturulan dataframe'in csv dosyasina cevrilmesi