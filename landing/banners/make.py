"""Generate Dodoliza banner + product-visual HTML files (rendered to PNG by render.js)."""
import pathlib

HERE = pathlib.Path(__file__).parent
FONT = pathlib.Path("/tmp/claude-0/-home-claude/762db5c8-75e2-5aae-8929-9ddca62e3623/scratchpad/node_modules/@fontsource/cairo/files")
IMG = "../assets/img/"

ICONS = {
    "stretch": '<path d="M4 12h16M7 9l-3 3 3 3M17 9l3 3-3 3"/><path d="M9 5v14M15 5v14" opacity=".45"/>',
    "leaf": '<path d="M5 19c0-8 5-13 14-14-1 9-6 14-14 14Z"/><path d="M5 19 13 11"/>',
    "air": '<path d="M7 18c-2-2 2-4 0-6s2-4 0-6M12 18c-2-2 2-4 0-6s2-4 0-6M17 18c-2-2 2-4 0-6s2-4 0-6"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
}


def icon(name, size=28):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


FEATS = [("stretch", "بدون ضغط على الساق"), ("sparkle", "خامة نانو الفضة"),
         ("air", "تهوية تقلّل الرائحة"), ("leaf", "ملمس ناعم بلا خياطة مزعجة")]

BASE = f"""
@font-face{{font-family:Cairo;font-weight:400;src:url({FONT}/cairo-arabic-400-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:600;src:url({FONT}/cairo-arabic-600-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:700;src:url({FONT}/cairo-arabic-700-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:800;src:url({FONT}/cairo-arabic-800-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:900;src:url({FONT}/cairo-arabic-900-normal.woff2)}}
@font-face{{font-family:CairoL;font-weight:700;src:url({FONT}/cairo-latin-700-normal.woff2)}}
:root{{--forest:#285429;--forest-deep:#1B3B1C;--sage:#AEC095;--sage-soft:#D9E2C9;--cream:#F3ECE1;--cream-2:#FAF6EF;
--gold:#9C7A2E;--gold-soft:#C9A95C;--rose:#C9405A;--rose-logo:#DF526A;--ink:#1F2A1F}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Cairo,CairoL,sans-serif;direction:rtl;background:#fff}}
.c{{position:relative;overflow:hidden;background:var(--cream)}}
.logo{{display:block}}
.arch{{position:absolute;background:var(--sage);border-radius:999px 999px 0 0}}
.arch.f{{background:var(--forest)}}
.ring{{position:absolute;border:2px solid var(--gold-soft);border-radius:999px 999px 0 0;opacity:.7}}
.pill{{display:inline-flex;align-items:center;gap:.5em;border:2px solid var(--gold-soft);border-radius:999px;
  background:var(--cream-2);color:var(--forest);font-weight:800;padding:.35em 1.1em;white-space:nowrap}}
.pill b{{color:var(--gold)}}
h1{{color:var(--forest);font-weight:900;line-height:1.15;letter-spacing:-.01em}}
.sub{{color:#3B4A3B;font-weight:600;line-height:1.6}}
.cta{{display:inline-flex;align-items:center;justify-content:center;gap:.5em;background:var(--forest);color:#fff;
  font-weight:800;border-radius:999px;white-space:nowrap}}
.offer{{display:flex;align-items:center;gap:.6em;color:var(--forest);font-weight:900;white-space:nowrap}}
.gift{{background:var(--rose);color:#fff;border-radius:999px;font-weight:800;padding:.15em .8em}}
.price{{display:flex;align-items:baseline;gap:.25em;color:var(--forest);font-weight:900;line-height:1}}
.price small{{font-weight:700;color:var(--gold)}}
.feats{{display:flex;gap:0;color:var(--forest)}}
.feat{{display:flex;align-items:center;gap:.55em;font-weight:700;white-space:nowrap}}
.feat i{{display:grid;place-items:center;border-radius:50%;background:var(--cream-2);border:1.5px solid var(--sage);color:var(--forest);font-style:normal}}
img.p{{position:absolute;filter:drop-shadow(0 24px 30px rgba(27,59,28,.28))}}
.dots{{position:absolute;background-image:radial-gradient(var(--gold-soft) 1.4px,transparent 1.6px);background-size:18px 18px;opacity:.55}}
"""


def page(w, h, body, extra=""):
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{BASE}{extra}</style></head>'
            f'<body><div class="c" id="b" style="width:{w}px;height:{h}px">{body}</div></body></html>')


def feats_html(fs, isz):
    return "".join(f'<div class="feat"><i style="width:{isz*1.9}px;height:{isz*1.9}px">{icon(k, isz)}</i><span>{t}</span></div>' for k, t in fs)


FILES = {}

# ---------- 1. HERO 1440x640 ----------
FILES["hero-1440x640"] = (1440, 640, page(1440, 640, f"""
<div class="dots" style="left:40px;top:60px;width:180px;height:180px"></div>
<div class="arch" style="left:110px;bottom:-10px;width:470px;height:580px"></div>
<div class="ring" style="left:90px;bottom:-10px;width:510px;height:610px"></div>
<img class="p" src="{IMG}black-stretch.png" style="left:150px;bottom:20px;height:520px">
<img class="p" src="{IMG}box-open.png" style="left:430px;bottom:24px;width:300px">
<div style="position:absolute;right:96px;top:70px;width:640px">
  <img class="logo" src="{IMG}logo-rose.png" style="height:52px;margin-bottom:34px">
  <span class="pill" style="font-size:22px">مصمم خصيصًا <b>لمرضى السكري</b></span>
  <h1 style="font-size:66px;margin:22px 0 14px">راحة خاصة<br>للقدم الحساسة</h1>
  <p class="sub" style="font-size:22px;max-width:560px">شراب طبي ناعم بدون ضغط على الساق، بخامة نانو الفضة اللي تقلّل الرائحة وتخلي رجلك ناشفة طول اليوم.</p>
  <div style="display:flex;align-items:center;gap:28px;margin-top:30px">
    <span class="cta" style="font-size:24px;height:64px;padding:0 44px">اطلب الآن</span>
    <div><div class="offer" style="font-size:24px">بكج + بكج <span class="gift" style="font-size:20px">هدية</span></div>
    <div class="price" style="font-size:22px;margin-top:6px">10 أزواج بـ 149 <small style="font-size:18px">ر.س</small></div></div>
  </div>
</div>"""))

# ---------- 2. IG POST 1080 ----------
FILES["instagram-post-1080x1080"] = (1080, 1080, page(1080, 1080, f"""
<div class="arch" style="left:50%;transform:translateX(-50%);bottom:180px;width:620px;height:560px"></div>
<div class="ring" style="left:50%;transform:translateX(-50%);bottom:180px;width:670px;height:590px"></div>
<img class="p" src="{IMG}black-stretch.png" style="left:300px;bottom:190px;height:540px">
<img class="p" src="{IMG}box-open.png" style="left:560px;bottom:196px;width:330px">
<div style="position:absolute;top:56px;left:0;right:0;text-align:center">
  <img class="logo" src="{IMG}logo-rose.png" style="height:46px;margin:0 auto 22px">
  <h1 style="font-size:64px">شرابات لمرضى السكري</h1>
  <span class="pill" style="font-size:26px;margin-top:14px">بكج + بكج <b>هدية</b></span>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:180px;background:var(--forest);display:flex;align-items:center;justify-content:space-between;padding:0 70px;color:#fff">
  <div><div style="font-size:26px;font-weight:700;opacity:.9">10 أزواج بـ</div>
  <div style="font-size:64px;font-weight:900;line-height:1">149 <span style="font-size:28px;color:var(--gold-soft)">ر.س</span></div></div>
  <div class="feats" style="flex-direction:column;gap:10px;color:#fff;font-size:22px">
   <div class="feat">{icon('stretch',26)} بدون ضغط على الساق</div>
   <div class="feat">{icon('sparkle',26)} خامة نانو الفضة</div>
   <div class="feat">{icon('air',26)} تهوية تقلّل الرائحة</div></div>
</div>"""))

# ---------- 3. IG STORY 1080x1920 ----------
FILES["instagram-story-1080x1920"] = (1080, 1920, page(1080, 1920, f"""
<div class="dots" style="right:60px;top:300px;width:200px;height:200px"></div>
<div style="position:absolute;top:200px;left:0;right:0;text-align:center">
  <img class="logo" src="{IMG}logo-rose.png" style="height:60px;margin:0 auto 40px">
  <span class="pill" style="font-size:32px">مصمم خصيصًا <b>لمرضى السكري</b></span>
  <h1 style="font-size:96px;margin-top:30px">راحة خاصة<br>للقدم الحساسة</h1>
</div>
<div class="arch" style="left:50%;transform:translateX(-50%);top:720px;width:720px;height:640px;border-radius:999px 999px 48px 48px"></div>
<div class="ring" style="left:50%;transform:translateX(-50%);top:690px;width:780px;height:700px;border-radius:999px 999px 60px 60px"></div>
<img class="p" src="{IMG}black-stretch.png" style="left:230px;top:740px;height:600px">
<img class="p" src="{IMG}box-open.png" style="left:500px;top:1090px;width:400px">
<div style="position:absolute;left:0;right:0;bottom:200px;text-align:center">
  <div class="offer" style="font-size:52px;justify-content:center">بكج + بكج <span class="gift" style="font-size:44px">هدية</span></div>
  <div class="price" style="font-size:44px;justify-content:center;margin-top:16px">10 أزواج بـ 149 <small style="font-size:34px">ر.س</small></div>
  <span class="cta" style="font-size:40px;height:104px;padding:0 90px;margin-top:40px">اطلب الآن</span>
</div>""", ".c{background:linear-gradient(180deg,var(--cream) 0 82%,var(--cream-2) 82%)}"))

# ---------- 4. FB AD 1200x628 ----------
FILES["facebook-ad-1200x628"] = (1200, 628, page(1200, 628, f"""
<div style="position:absolute;inset:0 0 0 auto;width:470px;background:var(--forest)"></div>
<div class="arch" style="left:90px;bottom:0;width:400px;height:520px;background:var(--sage)"></div>
<img class="p" src="{IMG}black-pair.png" style="left:70px;bottom:40px;width:460px">
<img class="p" src="{IMG}box-white.png" style="left:420px;bottom:30px;width:260px">
<div style="position:absolute;right:60px;top:56px;width:370px;color:#fff">
  <img class="logo" src="{IMG}logo-white.png" style="height:40px;margin-bottom:26px">
  <h1 style="font-size:46px;color:#fff">شرابات<br>لمرضى السكري</h1>
  <p style="font-size:21px;font-weight:600;margin:14px 0 22px;opacity:.92;line-height:1.6">بدون ضغط على الساق · خامة نانو الفضة</p>
  <div style="font-size:30px;font-weight:900">بكج + بكج <span class="gift" style="font-size:24px">هدية</span></div>
  <div style="font-size:24px;font-weight:700;margin-top:8px">10 أزواج بـ 149 <span style="color:var(--gold-soft)">ر.س</span></div>
  <span class="cta" style="background:var(--cream);color:var(--forest);font-size:22px;height:58px;padding:0 40px;margin-top:26px">اطلب الآن</span>
</div>"""))


# ---------- Product visuals (canvas-design) 1080 ----------
def product_visual(key, img, title, line, bg_arch, img_style, extra_img=""):
    FILES[key] = (1080, 1080, page(1080, 1080, f"""
<div class="arch {bg_arch}" style="left:50%;transform:translateX(-50%);bottom:0;width:700px;height:820px"></div>
<div class="ring" style="left:50%;transform:translateX(-50%);bottom:0;width:760px;height:860px"></div>
<img class="p" src="{IMG}{img}" style="{img_style}">{extra_img}
<img class="logo" src="{IMG}logo-rose.png" style="position:absolute;top:44px;right:56px;height:40px">
<div style="position:absolute;top:44px;left:56px;text-align:left"><span class="pill" style="font-size:22px">{title}</span></div>
<div style="position:absolute;bottom:44px;left:0;right:0;text-align:center"><span class="pill" style="font-size:24px;background:#fffdf8">{line}</span></div>
"""))


product_visual("product-black-1080", "black-stretch.png", "شراب دودليزا · أسود", "حافة واسعة بدون ضغط على الساق", "",
               "left:50%;transform:translateX(-50%);bottom:110px;height:760px")
FILES["product-white-1080"] = (1080, 1080, page(1080, 1080, f"""
<div class="ring" style="left:50%;transform:translateX(-50%);bottom:0;width:760px;height:900px"></div>
<div style="position:absolute;left:50%;transform:translateX(-50%);bottom:0;width:700px;height:860px;border-radius:999px 999px 0 0;overflow:hidden;box-shadow:0 30px 60px rgba(27,59,28,.18)">
<img src="{IMG}white-photo.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%"></div>
<img class="logo" src="{IMG}logo-rose.png" style="position:absolute;top:44px;right:56px;height:40px">
<div style="position:absolute;top:44px;left:56px"><span class="pill" style="font-size:22px">شراب دودليزا · أبيض</span></div>
<div style="position:absolute;bottom:44px;left:0;right:0;text-align:center"><span class="pill" style="font-size:24px;background:#fffdf8">ملمس ناعم وتهوية طول اليوم</span></div>"""))
product_visual("product-box-1080", "box-open.png", "العلبة · 5 أزواج", "بكج + بكج هدية = 10 أزواج", "",
               "left:50%;transform:translateX(-50%);bottom:150px;width:760px")

# fabric close-up framed
FILES["product-fabric-1080"] = (1080, 1080, page(1080, 1080, f"""
<div style="position:absolute;inset:70px 70px 150px;border-radius:44px;overflow:hidden;box-shadow:0 30px 60px rgba(27,59,28,.25)">
<img src="{IMG}fabric.png" style="width:100%;height:100%;object-fit:cover"></div>
<div style="position:absolute;inset:56px 56px 136px;border:2px solid var(--gold-soft);border-radius:56px"></div>
<div style="position:absolute;bottom:44px;left:0;right:0;display:flex;justify-content:center;gap:16px">
<span class="pill" style="font-size:24px">{icon('sparkle',24)} خيوط نانو الفضة</span>
<span class="pill" style="font-size:24px">{icon('air',24)} نسيج مسامي يتنفس</span></div>"""))

for name, (w, h, html) in FILES.items():
    (HERE / f"{name}.html").write_text(html, encoding="utf-8")
(HERE / "list.txt").write_text("\n".join(f"{n} {w} {h}" for n, (w, h, _) in FILES.items()))
print("\n".join(FILES))
