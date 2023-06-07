# import ssl

# ssl._create_default_https_context = ssl._create_unverified_context
# import urllib.request
# import time


# # parse all heros name from url="https://pvp.qq.com/web201605/herolist.shtml", the selector is body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li > a
# def get_hero_names():
#     url = "https://pvp.qq.com/web201605/herolist.shtml"

#     headers = {
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
#     }

#     enhanced_url = urllib.request.Request(url=url, headers=headers)
#     response = urllib.request.urlopen(enhanced_url)
#     time.sleep(5)
#     html = response.read().decode("gbk")
#     print(html)
#     from bs4 import BeautifulSoup

#     soup = BeautifulSoup(html, "html.parser")
#     heros = soup.select(
#         "body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li > a"
#     )
#     h = soup.select(
#         "body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li:nth-child(1) > a"
#     )
#     print(h[0].get_text())
#     hero_names = []
#     for hero in heros:
#         hero_names.append(hero.get_text())
#     return hero_names


# herolist = get_hero_names()

# print(herolist, len(herolist))
import joblib

names = []
with open("names.txt", "r") as f:
    for line in f.readlines():
        names.append(line.split(" ")[1])
joblib.dump(names, "names.pkl")
print(len(names))
