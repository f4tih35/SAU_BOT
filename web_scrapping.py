import requests
from bs4 import BeautifulSoup

class MainScript:
    def __init__(self):
        self.ogr_url="http://ogrisl.sakarya.edu.tr"
        self.cs_url="http://cs.sakarya.edu.tr"

# verilen sayfa linkindeki haber başlıklarını ve linklerini alır.
    def script(self,link):
        url=requests.get(link).content
        datas=BeautifulSoup(url,"html.parser")
        text=datas.find_all("div",{"class":"widget-main"},limit=5)
        for data in text:
            blog_list=data.find_all("div",{"class":"blog-list-post"})
            for titles in blog_list:
                title=titles.find("h5").text
                temp_url=titles.find("a",href=True)
                # bota eklenirken değişiklik yapılması gereken yer
                print(f"Haber : {title}  URL : {temp_url['href']}")

data=MainScript()
data.script("http://cs.sakarya.edu.tr")