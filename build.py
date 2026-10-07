# Builds index.html (one self-contained file) from index.src.html by inlining images.
import re, base64, mimetypes
s=open('index.src.html',encoding='utf-8').read()
def inline(m):
    path=m.group(2)
    if path.startswith(('http','data:','#')): return m.group(0)
    mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'
    return f'{m.group(1)}"data:{mime};base64,'+base64.b64encode(open(path,'rb').read()).decode()+'"'
open('index.html','w',encoding='utf-8').write(re.sub(r'(src=)"([^"]+\.(?:png|jpg|jpeg))"',inline,s))
print('built')
