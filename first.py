# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=consider-using-enumerate,invalid-name
# pylint: disable=broad-except
import os
import datetime
import re
import base64
from bs4 import BeautifulSoup
import requests
from PIL import Image
months = {'Jan,': 1, 'Feb,': 2, 'Mar,': 3, 'Apr,': 4, 'May,': 5, 'Jun,': 6,
        'Jul,': 7, 'Aug,': 8, 'Sep,': 9, 'Oct,': 10,
        'Nov,': 11, 'Dec,': 12}

def find_url(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+
            [.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+
            (?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"""
    url = re.findall(regex, string)
    return [x[0] for x in url]
def html_cleaner(string):
    ret = []
    opens = []
    closes = []
    for i in range(len(string)):

        if string[i] is not None:

            if string[i] == "<":
                opens.append(i)
            elif string[i] == ">":
                closes.append(i)

    for i in range(len(opens)):

        if i > 0:
            ret[0] = ret[-1].replace(string[opens[i]:closes[i] + 1], "")
        else:
            ret.append(string.replace(string[opens[i]:closes[i] + 1], ""))
    return ret[-1]

def quote_checker(string):
    for i in range(len(string)):

        if string[i] == "'":
            if string[i - 1] == "'":
                continue
            string = string[:i] + "'" + string[i:]

    return string

class tass:
    def __init__(self):
        self.url = "https://tass.com/"
        self.name = "TASS RUSSIAN NEWS AGENCY"
        self.all_links = self.get_all_links()
        self.categorised_urls = self.categorise_urls()
    def get_all_links(self):
        web_page = requests.get("https://tass.com/")
        soup = BeautifulSoup(web_page.content, "html.parser")
        all_urls = []
        for link in soup.find_all('a'):
            href = str(link.get('href'))
            all_urls.append(href)
        return all_urls
    def categorise_urls(self):
        all_urls = self.get_all_links()
        politics = []
        world = []
        economy = []
        defense = []
        science = []
        emergencies = []
        society = []
        sport = []
        pressreview = []
        ads = []
        contacts = []
        specialprojects = []
        for href in all_urls:
            if href.startswith("/politics/") and not href == "/politics/":
                politics.append("https://tass.com" + href)
            elif href.startswith("/world/") and not href == "/world/":
                world.append("https://tass.com" + href)
            elif href.startswith("/economy/") and not href == "/economy/":
                economy.append("https://tass.com" + href)
            elif href.startswith("/defense/") and not href == "/defense/":
                defense.append("https://tass.com" + href)
            elif href.startswith("/science/") and not href == "/science/":
                science.append("https://tass.com" + href)
            elif href.startswith("/emergencies/") and not href == "/emergencies/":
                emergencies.append("https://tass.com" + href)
            elif href.startswith("/society/") and not href == "/society/":
                society.append("https://tass.com" + href)
            elif href.startswith("/sport/") and not href == "/sport/":
                sport.append("https://tass.com" + href)
            elif href.startswith("/pressreview/") and not href == "/pressreview/":
                pressreview.append("https://tass.com" + href)
            elif href.startswith("/ads/") and not href == "/ads/":
                ads.append("https://tass.com" + href)
            elif href.startswith("/contacts/") and not href == "/contacts/":
                contacts.append("https://tass.com" + href)
            elif href.startswith("/specialprojects/") and not href == "/specialprojects/":
                specialprojects.append("https://tass.com" + href)
        ret = {"politics" : politics,"world" : world,"economy" : economy,
        "defense" : defense,"science" : science ,"emergencies" : emergencies,
        "society" : society,"sport" : sport,"pressreview" : pressreview,
        "ads" : ads ,"contacts" : contacts,"specialprojects" : specialprojects}
        return ret
class tass_news:
    def __init__(self, url, news_agency):
        try:
            self.news_agency = news_agency
            self.url = url
            self.web_page = requests.get(self.url)
            self.soup = BeautifulSoup(self.web_page.content, "html.parser")
            self.title = quote_checker( self.get_article_title() )
            self.summary = quote_checker(self.get_article_description())
            self.text = quote_checker(self.get_article_text())
            self.timestamp = self.get_article_timestamp()
            self.time_string = f'''{self.timestamp.year}-{self.timestamp.month}-{self.timestamp.day}
{self.timestamp.hour}:{self.timestamp.minute}'''
            self.img = self.get_image()
            self.subject = None
        except Exception as e:
            print("Error:", e)
    def get_article_title(self):
        result = self.soup.find("title").prettify()
        ret = html_cleaner(result)
        rev = ret[: :-1]
        if "-" in rev:
            temp = rev.find("-",8)
            return ret[:-1 * temp -1]
        else:
            return ret
    def get_article_description(self):
        try:
            result = self.soup.find(class_="news-header__lead").prettify()
            return str(html_cleaner(result))
        except Exception as e:
            print("Error:", e)
    def get_article_text(self):
        try:
            result =self. soup.find(class_="text-content")

            all_text = []

            if result is not None:

                ret = ""

                for para in result.find_all(["p","h2"]):
                    all_text.append(para.getText())
                for i in all_text:
                    ret += (i+"\n\n")
                return ret
        except Exception as e:
            print("Error:", e)
    def get_all_images(self):
        return find_url(str(self.soup.find_all("img")))
    def get_image(self):
        result =self.soup.find(class_="text-include-photo__img")
        urls = find_url(str(result))
        img_link = urls[0]
        response = requests.get("https://"+img_link[:-2])
        file = open("temp.jpg", "wb")
        file.write(response.content)
        file.close()
        #lower the quality
        img_file=Image.open("temp.jpg")
        img_file.save("temp.jpg",quality=25)
        img_file.close()

        with open("temp.jpg", "rb") as img_file:
            base64string = base64.b64encode(img_file.read())

        os.remove("temp.jpg")
        return base64string

    def get_article_timestamp(self):
        result = self.soup.find(class_ = "news-header__date")
        time = int(result.dateformat.get('time'))
        self.time_string = str(
            datetime.datetime.utcfromtimestamp(time).strftime('%Y-%m-%d s%H:%M:%S'))
        date_time = self.time_string.split(" ")
        time=date_time[1].split(":")
        date=date_time[0].split("-")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        hour = int(time[0][-2:])
        minute = int(time[1])
        timestamp = datetime.datetime(year, month, day, hour, minute)


        return  timestamp
    def get_full_article(self):
        ret = ""
        ret += self.time_string
        ret += "\n"
        ret += self.title
        ret += self.summary
        ret+= self.text
        return ret
rs=tass()
#rs.all_links
#rs.categorised_urls
print(rs.categorised_urls["politics"][1])
rs_news=tass_news( rs.categorised_urls["politics"][1] ,rs.name)
#print(len(rs_news.img))
#print(rs_news.url)
print(rs_news.get_full_article())
#print(rs_news.time_string)
