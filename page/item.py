from . import get_page, save, WIKI_URL
import json
from urllib.parse import urljoin
import traceback

def clean_text(text):
    return text.removesuffix("\n")


def get_big_img_url(url):
    return "/".join(url.split("/")[:-1]).replace("/thumb", "")


def parse_table(table, category):
    out = []
    head = table.find_all("tr")[0]
    item_col_idx = -1
    effect_col_idx = -1
    buy_price_col_idx = -1
    sell_price_col_idx = -1
    capture_bonus_col_idx = -1
    source_col_idx = -1
    quest_col_idx = -1
    location_col_idx = -1
    head_tds = head.find_all("th")
    for i in range(0, len(head_tds)):
        text = clean_text( head_tds[i].text)
        match text:
            case ("Name"|"Item"):
                item_col_idx = i
            case ("Effect"|"Description"):
                effect_col_idx = i
            case ("Buy price"|"Buy Price"):
                buy_price_col_idx = i
            case "Sell price":
                sell_price_col_idx = i
            case "Source":
                source_col_idx = i
            case "Quest":
                quest_col_idx = i
            case "Capture Bonus":
                capture_bonus_col_idx = i
            case "Location":
                location_col_idx = i
            case other:
                print(other)

    for row in table.find_all("tr")[1:]:
        tds = row.find_all("td")
        img_src = tds[item_col_idx].find("img").get("src")
        img_big_src = get_big_img_url(img_src)

        data = {
            "name": clean_text(tds[item_col_idx].text),
            "description": clean_text(tds[effect_col_idx].text),
            "category": category,
            "buyPrice": clean_text(tds[buy_price_col_idx].text) if buy_price_col_idx != -1 else None,
            "sellPrice": clean_text(tds[sell_price_col_idx].text) if sell_price_col_idx != -1 else None,
            "smallImg": urljoin(WIKI_URL, img_src),
            "img": urljoin(WIKI_URL, img_big_src)
        }
        if capture_bonus_col_idx != -1:
            data["captureBonus"] = clean_text(tds[capture_bonus_col_idx].text)
        if source_col_idx != -1:
            data["source"] = clean_text(tds[source_col_idx].text)
        if quest_col_idx != -1:
            data["quest"] = clean_text(tds[quest_col_idx].text)
        if location_col_idx != -1:
            data["location"] = clean_text(tds[location_col_idx].text)
        if row.find(alt="Pansuns.png") != None:
            data["money"] = "pansuns"
            data["moneyImg"] = urljoin(WIKI_URL, get_big_img_url(row.find(alt="Pansuns.png").get("src")))
        elif row.find(alt="Feathers.png") != None:
            data["money"] = "feathers"
            data["moneyImg"] = urljoin(WIKI_URL, get_big_img_url(row.find(alt="Feathers.png").get("src")))
        else:
            data["money"] = None
        out.append(data)
    return out


def parse_items():
    soup = get_page("https://temtem.wiki.gg/wiki/Items")
    content = soup.find(class_="mw-body-content")
    titles = content.find_all("h3")
    tables = content.find_all("table")
    categories = [title.text.removesuffix("[edit]") for title in titles]
    out = []
    for i in range(0, len(categories)):
        try:
            out.extend(parse_table(tables[i], categories[i]))
        except Exception as e:
            traceback.print_exception(e)
    return out


def parse_etc():
    soup = get_page("https://temtem.wiki.gg/wiki/Category:Techniques_learned_by_Breeding")
    etcs = []
    content = soup.find(id="mw-pages")
    for li in content.find_all("li"):
        link = li.find("a")
        etcs.append({
            "name": clean_text(link.text),
            "description": "",
            "category": "ETC",
            "buyPrice": None,
            "sellPrice": None,
            "smallImg": "https://temtem.wiki.gg/images/7/7e/ETC.png",
            "img": "https://temtem.wiki.gg/images/7/7e/ETC.png"
        })
    return etcs


def item():
    out = parse_items()
    out.extend(parse_etc())
    #print(out)
    save("item.json", json.dumps(out))
