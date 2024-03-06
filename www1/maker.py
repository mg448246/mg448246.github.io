import markdownmaker.markdownmaker as mdmkr
import markdownmaker.document as mddoc
from bs4 import BeautifulSoup
import requests
import googlesearch
import duckduckgo_search
import regex

tiobe_url = "https://www.tiobe.com"
languages = []

def lang_name_to_url(name: str):
    return name.lower() \
        .replace(" ", "_") \
        .replace("+", "p") \
        .replace("#", "sharp") \
        .replace("/", "_") \
        + ".md"

# making index page:
def make_index_page():
    html = requests.get(tiobe_url + "/tiobe-index/")
    soup = BeautifulSoup(html.text, "html.parser")
    index = mddoc.Document()

    index.add(mdmkr.Header(soup.find("h1").text))
    index.add(mdmkr.Bold(soup.find("h3").text))
    index.add("""\nThe TIOBE Programming Community index is an indicator of 
            the popularity of programming languages. The index is updated 
            once a month. The ratings are based on the number of skilled 
            engineers world-wide, courses and third party vendors. 
            Popular web sites Google, Amazon, Wikipedia, Bing and more 
            than 20 other engines are used to calculate the ratings. 
            It is important to note that the TIOBE index is not about 
            the best programming language or the language in which 
            most lines of code have been written.\n""")

    table = soup.find("table").find("tbody").find_all("tr")
    for row in table:
        items = row.find_all("td")
        lang_info = {}
        lang_info["rank"] = items[0].text
        lang_info["name"] = items[4].text
        lang_info["logo_img"] = tiobe_url + items[3].find("img")["src"]
        lang_info["usage"] = items[5].text
        languages.append(lang_info)

    for lang in languages:
        index.add(lang["rank"] + ": ")
        index.add(mdmkr.Link(lang["name"], lang_name_to_url(lang["name"])))
        index.add(" (" + lang["usage"] + ")")
        index.add(mdmkr.HorizontalRule())
        index.add(mdmkr.Image(lang["logo_img"]))


    with open("index.md", "w") as file:
        file.write(index.write())

def make_lang_page(data: dict):
    page = mddoc.Document()
    page.add(mdmkr.Header(data["name"]))
    page.add(mdmkr.Bold("Tiobe index rating: " + data["rank"] + " (" + data["usage"] + ")"))
    page.add("\n")

    for logo in duckduckgo_search.DDGS().images(data["name"] + " programming language logo official",
                                                max_results=1, safesearch="on", size="medium"):
        page.add(mdmkr.Image(logo["image"]))
        

    wikipedia_url = None
    for url in duckduckgo_search.DDGS().text(data["name"] + "programming_language", max_results=10):
        if regex.match("https://en\.wikipedia\.org*.", url["href"]):
            wikipedia_url = url
            break

    if wikipedia_url != None:
        page.add(wikipedia_url["body"] + "\n")
        page.add("More at: " + wikipedia_url["href"])
    else:
        page.add("No wikipedia article found")
    

    with open(lang_name_to_url(data["name"]), "w") as file:
        file.write(page.write())

if __name__ == "__main__":
    make_index_page()

    i = 0
    print(i)
    for lang in languages:
        make_lang_page(lang)
        i += 1
        print(i)