# Builds events.json (every event on benlimglobal.com with its real dates) for the app.
# The website's data feed has no event dates, so this reads each event page instead.
# Run: python3 update_events.py   then publish events.json with the rest of the app.
import html, json, re, time, urllib.request

SITE = "https://benlimglobal.com"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "ignore")

def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()

events, page = [], 1
while True:
    url = f"{SITE}/wp-json/wp/v2/mec-events?per_page=50&page={page}&_embed=wp:featuredmedia&_fields=title,link,excerpt,content,_links,_embedded"
    try:
        batch = json.loads(get(url))
    except Exception:
        break
    if not batch:
        break
    for p in batch:
        link = p.get("link", "")
        if not link.startswith(SITE + "/"):
            continue
        m = ((p.get("_embedded") or {}).get("wp:featuredmedia") or [{}])[0]
        sizes = (m.get("media_details") or {}).get("sizes") or {}
        ev = {
            "title": text(p["title"]["rendered"]),
            "link": link,
            "text": text(p["excerpt"]["rendered"] or p["content"]["rendered"]),
            "img": (sizes.get("medium") or sizes.get("full") or {}).get("source_url") or m.get("source_url", ""),
            "start": "", "end": "",
        }
        time.sleep(1.5)  # go slowly; the site blocks rapid requests
        try:
            page_html = get(link)
            for block in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', page_html, re.S):
                s = re.search(r'"startDate"\s*:\s*"(\d{4}-\d{2}-\d{2})', block)
                if s:
                    e = re.search(r'"endDate"\s*:\s*"(\d{4}-\d{2}-\d{2})', block)
                    ev["start"], ev["end"] = s.group(1), (e.group(1) if e else s.group(1))
                    break
        except Exception as err:
            print("  could not read", link, err)
        if len(ev["text"]) > 180:
            ev["text"] = re.sub(r"\s+\S*$", "", ev["text"][:177]) + "…"
        events.append(ev)
        print(f"  {ev['start'] or '????-??-??'}  {ev['title']}")
    page += 1

# Keep full details only for events that have not ended (the app hides any that end later on),
# plus the links of every event, so past events coming from the live website feed stay hidden too.
today = time.strftime("%Y-%m-%d")
upcoming = sorted([e for e in events if not e["start"] or e["end"] >= today], key=lambda e: e["start"] or "9999")
with open("events.json", "w", encoding="utf-8") as f:
    json.dump({"updated": today, "events": upcoming, "known": sorted(e["link"] for e in events)}, f, ensure_ascii=False, indent=1)
print(f"Saved {len(upcoming)} upcoming of {len(events)} events to events.json")
