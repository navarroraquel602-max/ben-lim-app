# Builds shop.json: the products shown on the benlimglobal.com store, for the app's "Music & More" shelf.
# Mirrors the store's own listing (2 pages), skipping mission trips (shown in Missions & Crusades)
# and free virtual events. Buying still happens on the website's own checkout.
# Run: python3 update_shop.py   then publish shop.json with the rest of the app.
import html, json, re, time, urllib.request

SITE = "https://benlimglobal.com"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"}
SKIP_CATEGORIES = {"Missions", "Virtual Free Event"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

# 1. Which products the store page actually lists (single tracks inside bundles are hidden there)
listed = []
for page in ("/shop/", "/shop/?product-page=2", "/shop/?product-page=3"):
    try:
        h = get(SITE + page)
    except Exception:
        break
    for pid in re.findall(r'class="[^"]*\bpost-(\d+)\b[^"]*\bproduct\b', h):
        if pid not in listed:
            listed.append(pid)
    time.sleep(1.5)

# 2. Names, prices, images and links from the store's data feed
data = json.loads(get(SITE + "/wp-json/wc/store/v1/products?per_page=100"))
by_id = {str(p["id"]): p for p in data}
items = []
for pid in listed:
    p = by_id.get(pid)
    if not p or {c["name"] for c in p.get("categories", [])} & SKIP_CATEGORIES:
        continue
    pr = p["prices"]; unit = 10 ** pr.get("currency_minor_unit", 2)
    rng = pr.get("price_range")
    price = (int(rng["min_amount"]) if rng else int(pr["price"] or 0)) / unit
    img = p["images"][0] if p.get("images") else {}
    items.append({
        "id": p["id"], "name": html.unescape(p["name"]), "link": p["permalink"],
        "price": price, "from": bool(rng) or p["type"] == "grouped",
        "kind": p["type"],  # simple / grouped (choose tracks) / external
        "img": img.get("thumbnail") or img.get("src", ""),
    })
    print(f"  {pid}  {items[-1]['name']}  ${price:.2f}  {p['type']}")

with open("shop.json", "w", encoding="utf-8") as f:
    json.dump({"updated": time.strftime("%Y-%m-%d"), "items": items}, f, ensure_ascii=False, indent=1)
print(f"Saved {len(items)} products to shop.json")
