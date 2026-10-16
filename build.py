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
build = lambda src: re.sub(r'(src=)"([^"]+\.(?:png|jpg|jpeg))"', inline, src)
open('index.html', 'w', encoding='utf-8').write(build(s))
open('silver.html', 'w', encoding='utf-8').write(build(theme_silver.make(s)))
m = json.load(open('manifest.json'))
m.update(name="Glory App Silver", short_name="Glory App", start_url="./silver.html")
json.dump(m, open('manifest-silver.json', 'w'), separators=(',', ':'))
print('built')
