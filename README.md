# Python_Web Scarping
I tried to get an news agency datas and it's news content.This project is simply a learning project.I used [TASS RUSSIAN NEWS AGENCY](https://tass.com/) for my project.
## What It Does:
I extract the news agency's data and also the news on the Website within the methodes I have written .

### News Agency:
By using this method `get_all_links` , You can extract all the links on the Website.
Using this methode `categorise_urls` ,You can  categorise the links based on the news category.
### News:
Within the methodes that I have Written in the `tass_news` class , You can extract the news title,summary,text and time and also You can encode the images in news for a Database.
## How It Works:
This is a OOP project and I  used specific classes for news and news agency and I've put their methodes in their classes.
## Clases:

### tass class :
##### Get links:
Firstly I downloaded  the Webpage date and loaded it into a Beautifulsoup object,then using methodes from that object I got all the links and saved it in a list.
##### Categorise links:
Using links category and list of the links , I categorised links and put them in lists named by it's category . 
### tass_news class :
##### Title:
like getting links in tass class this time by searching the tag title, I got the news title. after that by using `html_cleaner` I got the title`s content.
For every content in title element existed some extra string that I deleted them.
##### Summary:
I extracted summary`s text like title but using the proper tag.
##### Text:
I extracted text`s content with proper tag and saved it's paragraphs in a list.
then I put paragraphs in a string with two lines of space.
##### All Images:
I got all elements which have img tag and by `find_url ` method we get the images link.
##### Images:
like `get_all_images` method I can get all images link and then I download the first images. After that I saved it's content in a file and with that file I encoded the image and returned the string.

## Challenges :
##### Get Image:
The first image's link was not downloadable and was not complete.
- The issue didn't fix with cleaning the link 
- By using "http" string I could fix the link and download the image
##### Timestamp:
I couldn't get date of the news using class which contains news date:
- I searched the main class name and I added span tag but the problem didn't solve.
- By using tags I got Unix timestamp and with date time module I converted it into specific date.
## Install & Run:
```
git clone https://github.com/parniame/data-gathering.git
cd data-gathering
chmod +x first.py
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 ./first.py
```




