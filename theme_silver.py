# Makes the Black, Silver & White edition (silver.html) from the same source as the Black & Gold app.
# Every warm gold / fire color in the page's styles and scripts becomes a silver of the same lightness,
# so glows, shimmer and depth carry over. Flags, social-network colors, error red and product photos
# keep their real colors. Crowd and crusade photos are shown in black and white.
import re

KEEP = {  # colors that must stay true (flags, social icons, warnings)
    "#feda75", "#fa7e1e", "#d62976", "#962fbf", "#4f5bd5", "#ff0000", "#0866ff",
    "#ffde00", "#de2910", "#fecb00", "#34b233", "#ea2839", "#f1bf00", "#aa151b",
    "#d52b1e", "#0039a6", "#b22234", "#3c3b6e", "#c0392b", "#a33", "#2e7d32", "#9ccc9c", "#eef7ee",
    "#d10f0f", "#ff5c5c", "#5e0606", "#ff2d2d",  # YouTube tile and the red LIVE tag
}
KEEP_RGB = {(255, 0, 0)}

def silver(r, g, b):
    if not (r > b + 25 and r >= g):          # only warm (gold / orange / red-fire) tones change
        return None
    L = 0.299 * r + 0.587 * g + 0.114 * b
    L = min(255, L * 1.04 + 6)               # a touch brighter so it reads as metal, not grey
    return tuple(max(0, min(255, round(v))) for v in (L * 0.965, L * 0.985, L * 1.03))

def map_hex(m):
    h = m.group(0)
    if h.lower() in KEEP:
        return h
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    s = silver(r, g, b)
    return h if s is None else "#%02x%02x%02x" % s

def map_rgb(m):
    fn, r, g, b, rest = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
    if (r, g, b) in KEEP_RGB:
        return m.group(0)
    s = silver(r, g, b)
    return m.group(0) if s is None else "%s(%d,%d,%d%s" % (fn, s[0], s[1], s[2], rest)

def recolor(code):
    code = re.sub(r"#[0-9a-fA-F]{6}\b", map_hex, code)
    code = re.sub(r"(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(\s*[,)])", map_rgb, code)
    code = re.sub(r"hsl\(calc\((\d+) \+ var\(--h\) \* \.0\d\),(\d+)%", lambda m: "hsl(calc(%s + var(--h) * .02),6%%" % m.group(1), code)  # course cards
    code = code.replace(',100%,75%,', ',8%,88%,').replace(',100%,55%,', ',6%,72%,').replace(',100%,45%,', ',6%,60%,')  # embers
    return code

EXTRA = """
<style>
/* Black, Silver & White edition */
.gbg,.cph img,.vimg,.evhead img,.banner,.ctiles a img{filter:grayscale(1) contrast(1.08)}
</style>
"""

def make(src):
    # recolor only <style> and <script> blocks (inline SVG flags in the page body stay true)
    out = re.sub(r"(<style>)(.*?)(</style>)", lambda m: m.group(1) + recolor(m.group(2)) + m.group(3), src, flags=re.S)
    out = re.sub(r"(<script>)(.*?)(</script>)", lambda m: m.group(1) + recolor(m.group(2)) + m.group(3), out, flags=re.S)
    out = out.replace("</head>", EXTRA + "</head>", 1)
    out = out.replace('<link rel="manifest" href="manifest.json">', '<link rel="manifest" href="manifest-silver.json">', 1)
    out = out.replace("<title>Glory App</title>", "<title>Glory App · Silver</title>", 1)
    return out
