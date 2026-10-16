# Builds the app from index.src.html:
#   index.html  - Black & Gold edition (images inlined into one file)
#   silver.html - Black, Silver & White edition (same app, recolored by theme_silver.py)
import re, base64, mimetypes, json
import theme_silver
s = open('index.src.html', encoding='utf-8').read()
def inline(m):
    path = m.group(2)
    if path.startswith(('http', 'data:', '#', 'media/')): return m.group(0)  # media/ photos load as separate files
    mime = mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return f'{m.group(1)}"data:{mime};base64,' + base64.b64encode(open(path, 'rb').read()).decode() + '"'
def add_ft(src):
    en = json.load(open('i18n/en.json', encoding='utf-8'))
    ft = {l: {k: (v[3:] if v.startswith('PH:') else v) for k, v in zip(en, json.load(open(f'i18n/{l}.json', encoding='utf-8')))} for l in ('es', 'zh', 'ru', 'my')}
    src = src.replace('/*FT*/{}', json.dumps(ft, ensure_ascii=False, separators=(',', ':')), 1)
    return src.replace('/*CT*/{}', json.dumps(json.load(open('i18n/content.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':')), 1)
s = add_ft(s)
build = lambda src: re.sub(r'(src=)"([^"]+\.(?:png|jpg|jpeg))"', inline, src)
open('index.html', 'w', encoding='utf-8').write(build(s))
open('silver.html', 'w', encoding='utf-8').write(build(theme_silver.make(s)))
m = json.load(open('manifest.json'))
m.update(name="Glory App Silver", short_name="Glory App", start_url="./silver.html", background_color="#ffffff", theme_color="#ffffff",
         icons=[{"src": "icon-silver-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-silver-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}])
json.dump(m, open('manifest-silver.json', 'w'), separators=(',', ':'))
print('built')
