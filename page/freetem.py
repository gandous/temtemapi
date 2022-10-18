from . import get_page, save, WIKI_URL
import json

def freetem():
    soup = get_page("https://temtem.wiki.gg/wiki/FreeTem!_Organization")
    table = soup.find(id="rewards-curr-table")
    row = table.find_all("tr")
    imgs = row[0].find_all("img")
    datas = row[1].find_all("td")
    rewards = []
    for i in range(0, 4):
        img = imgs[i].get("src")
        data = datas[i]
        rewards.append({
            "freedTemtem": data.find("p").text.split(" ")[0],
            "image": f"{WIKI_URL}{img}",
            "name": data.find("a").text,
            "quantity": data.text.split("x")[0]
        })
    print(rewards)
    save("freetem.json", json.dumps(rewards))
