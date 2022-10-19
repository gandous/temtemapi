from . import get_page, save, WIKI_URL
import json

def get_value(table, index):
    return table[index * 3 + 2].text.removesuffix("\n")

def parse_table(table):
    bottom_table = table.find("table").find_all("td")
    left_table = bottom_table[0]
    right_table = bottom_table[1]
    value = right_table.find_all("td")
    img = left_table.find("img").get("src")
    return {
        "img": f"{WIKI_URL}{img}",
        "temtem": left_table.find("p").text,
        "area": table.find("td").find("p").text,
        "rate": get_value(value, 0),
        "lumaRate": get_value(value, 1),
        "minSvs": get_value(value, 2),
        "eggMoves": get_value(value, 3)
    }

def saipark():
    soup = get_page("https://temtem.wiki.gg/wiki/Saipark")
    tables = soup.find(id="mw-content-text").find("div").find_all("table", recursive=False)
    table1 = parse_table(tables[1])
    table2 = parse_table(tables[2])
    save("saipark.json", json.dumps([table1, table2]))
