"""v2 — Zyros-like premium navy/white direction. Product images (4:5), hero, offer banners, social."""
import pathlib

HERE = pathlib.Path(__file__).parent / "v2"
HERE.mkdir(exist_ok=True)
FONT = pathlib.Path("/tmp/claude-0/-home-claude/762db5c8-75e2-5aae-8929-9ddca62e3623/scratchpad/node_modules/@fontsource/cairo/files")
IMG = "../../assets/img/"

BASE = f"""
@font-face{{font-family:Cairo;font-weight:400;src:url({FONT}/cairo-arabic-400-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:600;src:url({FONT}/cairo-arabic-600-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:700;src:url({FONT}/cairo-arabic-700-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:800;src:url({FONT}/cairo-arabic-800-normal.woff2)}}
@font-face{{font-family:Cairo;font-weight:900;src:url({FONT}/cairo-arabic-900-normal.woff2)}}
@font-face{{font-family:CairoL;font-weight:400;src:url({FONT}/cairo-latin-400-normal.woff2)}}
@font-face{{font-family:CairoL;font-weight:700;src:url({FONT}/cairo-latin-700-normal.woff2)}}
@font-face{{font-family:CairoL;font-weight:900;src:url({FONT}/cairo-latin-900-normal.woff2)}}
:root{{--navy:#0B1F37;--navy-2:#16304F;--white:#FFFFFF;--studio:#F3F1EE;--studio-2:#E7E3DD;--line:#E5E2DC;
--ink:#1F1E1D;--muted:#5E5A55;--sale:#B42C46;--sale-tint:#FBEAED;--rose:#DF526A;--gold:#B39457;--gold-soft:#D8C49A}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:CairoL,Cairo,sans-serif;direction:rtl;background:#fff;color:var(--ink)}}
.c{{position:relative;overflow:hidden;background:#fff}}
.studio{{background:radial-gradient(120% 90% at 50% 35%,#FBFAF8 0%,var(--studio) 55%,var(--studio-2) 100%)}}
.floor{{position:absolute;left:50%;transform:translateX(-50%);border-radius:50%;background:radial-gradient(closest-side,rgba(11,31,55,.22),rgba(11,31,55,0))}}
img.p{{position:absolute;filter:drop-shadow(0 18px 22px rgba(11,31,55,.22))}}
.cover{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.badge{{position:absolute;top:0;font-weight:800;color:#fff;line-height:1}}
.word{{font-family:CairoL;font-weight:400;letter-spacing:.42em;color:var(--navy)}}
.kicker{{font-weight:700;letter-spacing:.02em;color:var(--gold)}}
h1{{font-weight:900;line-height:1.12}}
.btn{{display:inline-flex;align-items:center;justify-content:center;font-weight:800;white-space:nowrap;border-radius:2px}}
.btn-w{{background:#fff;color:var(--navy)}}
.btn-n{{background:var(--navy);color:#fff}}
.line{{height:1px;background:currentColor;opacity:.35}}
.num{{font-family:CairoL,Cairo;font-weight:900;line-height:.9;letter-spacing:-.02em}}
s{{text-decoration-thickness:2px}}
.stamp{{position:absolute;z-index:5;width:var(--s,64px);aspect-ratio:1;transform:rotate(-14deg);filter:drop-shadow(0 6px 8px rgba(70,48,12,.35))}}
.stamp-b{{position:absolute;inset:0;clip-path:polygon(100.00% 50.00%,95.21% 55.09%,98.75% 61.13%,92.95% 65.03%,95.05% 71.69%,88.53% 74.21%,89.09% 81.17%,82.17% 82.17%,81.17% 89.09%,74.21% 88.53%,71.69% 95.05%,65.03% 92.95%,61.13% 98.75%,55.09% 95.21%,50.00% 100.00%,44.91% 95.21%,38.87% 98.75%,34.97% 92.95%,28.31% 95.05%,25.79% 88.53%,18.83% 89.09%,17.83% 82.17%,10.91% 81.17%,11.47% 74.21%,4.95% 71.69%,7.05% 65.03%,1.25% 61.13%,4.79% 55.09%,0.00% 50.00%,4.79% 44.91%,1.25% 38.87%,7.05% 34.97%,4.95% 28.31%,11.47% 25.79%,10.91% 18.83%,17.83% 17.83%,18.83% 10.91%,25.79% 11.47%,28.31% 4.95%,34.97% 7.05%,38.87% 1.25%,44.91% 4.79%,50.00% 0.00%,55.09% 4.79%,61.13% 1.25%,65.03% 7.05%,71.69% 4.95%,74.21% 11.47%,81.17% 10.91%,82.17% 17.83%,89.09% 18.83%,88.53% 25.79%,95.05% 28.31%,92.95% 34.97%,98.75% 38.87%,95.21% 44.91%);background:radial-gradient(circle at 34% 28%,#F6E7B6 0%,#D9B867 42%,#B48C3E 72%,#93702C 100%);display:grid;place-items:center;color:#0B1F37}}
.stamp-b::before{{content:"";position:absolute;inset:9%;border-radius:50%;border:2px dashed rgba(11,31,55,.6)}}
.stamp-b::after{{content:"";position:absolute;inset:15%;border-radius:50%;border:1.5px solid rgba(11,31,55,.35)}}
.stamp-t{{position:relative;display:grid;justify-items:center;line-height:1.02;text-align:center;font-family:Cairo;font-weight:900;font-size:calc(var(--s,64px) * .17)}}
.stamp-t small{{font-size:.72em;font-weight:800}}
.stamp-t i{{display:block;width:60%;height:1.5px;background:rgba(11,31,55,.5);margin:3px 0}}
"""


def page(w, h, body, extra=""):
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{BASE}{extra}</style></head>'
            f'<body><div class="c" id="b" style="width:{w}px;height:{h}px">{body}</div></body></html>')


FILES = {}


def stamp(size, left, top):
    return (f'<span class="stamp" style="--s:{size}px;left:{left}px;top:{top}px"><span class="stamp-b"><span class="stamp-t">'
            '<small>عرض</small><i></i>الجمعة<br>البيضاء</span></span></span>')


# ---------------- Product images 1000x1250 (4:5 like Zyros cards) ----------------
def studio(key, inner):
    FILES[key] = (1000, 1250, page(1000, 1250, f'<div class="studio" style="position:absolute;inset:0"></div>{inner}'))


studio("card-black-1", f"""<div class="floor" style="bottom:120px;width:640px;height:70px"></div>
<img class="p" src="{IMG}black-stretch.png" style="left:50%;transform:translateX(-50%);bottom:140px;height:960px">""")
FILES["card-black-2"] = (1000, 1250, page(1000, 1250, f'<img class="cover" src="{IMG}black-lifestyle.jpg" style="object-position:50% 60%">'))
FILES["card-white-1"] = (1000, 1250, page(1000, 1250, f'<img class="cover" src="{IMG}white-photo.jpg" style="object-position:55% 40%;filter:sepia(.06) saturate(.9) brightness(1.04)">'))
studio("card-white-2", f"""<div class="floor" style="bottom:330px;width:820px;height:80px"></div>
<img class="p" src="{IMG}box-white.png" style="left:50%;transform:translateX(-50%);bottom:350px;width:820px">""")
studio("card-box-1", f"""<div class="floor" style="bottom:330px;width:820px;height:80px"></div>
<img class="p" src="{IMG}box-open.png" style="left:50%;transform:translateX(-50%);bottom:345px;width:860px">""")
FILES["card-box-2"] = (1000, 1250, page(1000, 1250, f'<img class="cover" src="{IMG}fabric.png" style="object-position:100% 50%">'))
studio("card-family-1", f"""<div class="floor" style="bottom:250px;width:880px;height:90px"></div>
<img class="p" src="{IMG}box-white.png" style="left:60px;bottom:560px;width:560px;opacity:.97">
<img class="p" src="{IMG}box-white.png" style="right:40px;bottom:480px;width:560px">
<img class="p" src="{IMG}box-open.png" style="left:50%;transform:translateX(-50%);bottom:260px;width:700px">""")

# ---------------- HERO desktop 1440x640 ----------------
FILES["hero-desktop-1440x640"] = (1440, 640, page(1440, 640, f"""
<div style="position:absolute;left:0;top:0;bottom:0;width:760px"><img class="cover" src="{IMG}black-lifestyle.jpg" style="object-position:50% 62%"></div>
<div style="position:absolute;right:0;top:0;bottom:0;width:680px;background:var(--navy);color:#fff;padding:78px 90px 0 70px">
  <img src="{IMG}logo-white.png" style="height:40px;display:block;margin-bottom:46px">
  <div class="kicker" style="font-size:22px;color:var(--gold-soft)">شرابات مصممة لمرضى السكري</div>
  <div style="display:flex;align-items:flex-end;gap:22px;margin:16px 0 8px">
    <span class="num" style="font-size:150px">1+1</span>
    <span style="font-size:44px;font-weight:900;padding-bottom:16px">مجانًا</span></div>
  <div style="font-size:24px;font-weight:600;opacity:.9">علبتين = 10 أزواج بـ <b style="font-size:30px">149</b> ر.س بدلًا من <s style="opacity:.75">298</s></div>
  <span class="btn btn-w" style="font-size:22px;height:62px;padding:0 54px;margin-top:40px">تسوّق الآن</span>
</div>{stamp(150, 40, 40)}"""))

# ---------------- HERO mobile 750x1000 ----------------
FILES["hero-mobile-750x1000"] = (750, 1000, page(750, 1000, f"""
<div style="position:absolute;inset:0 0 430px 0"><img class="cover" src="{IMG}black-lifestyle.jpg" style="object-position:50% 62%"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:430px;background:var(--navy);color:#fff;text-align:center;padding-top:44px">
  <div class="kicker" style="font-size:28px;color:var(--gold-soft)">شرابات مصممة لمرضى السكري</div>
  <div style="display:flex;align-items:flex-end;justify-content:center;gap:18px;margin:6px 0">
    <span class="num" style="font-size:150px">1+1</span><span style="font-size:48px;font-weight:900;padding-bottom:14px">مجانًا</span></div>
  <div style="font-size:28px;font-weight:600;opacity:.92">10 أزواج بـ <b style="font-size:34px">149</b> ر.س بدلًا من <s style="opacity:.75">298</s></div>
  <span class="btn btn-w" style="font-size:30px;height:84px;width:620px;margin-top:34px">تسوّق الآن</span>
</div>{stamp(150, 30, 30)}"""))

# ---------------- Offer banners (mid-page) 1200x500 ----------------
FILES["offer-1plus1-1200x500"] = (1200, 500, page(1200, 500, f"""
<div class="studio" style="position:absolute;inset:0"></div>
<div class="floor" style="left:330px;bottom:70px;width:520px;height:60px"></div>
<img class="p" src="{IMG}box-open.png" style="left:110px;bottom:82px;width:480px">
<img class="p" src="{IMG}box-white.png" style="left:40px;bottom:250px;width:300px;opacity:.96">
<div style="position:absolute;right:90px;top:70px;color:var(--navy)">
  <div class="kicker" style="font-size:22px">عرض لفترة محدودة</div>
  <div style="display:flex;align-items:flex-end;gap:18px"><span class="num" style="font-size:170px">1+1</span>
  <span style="font-size:48px;font-weight:900;padding-bottom:18px;color:var(--sale)">مجانًا</span></div>
  <div style="font-size:24px;font-weight:700;margin-top:6px">اشترِ علبة، والثانية علينا</div>
  <span class="btn btn-n" style="font-size:20px;height:56px;padding:0 44px;margin-top:26px">تسوّق الآن</span>
</div>{stamp(120, 30, 26)}"""))

FILES["offer-50off-1200x500"] = (1200, 500, page(1200, 500, f"""
<div style="position:absolute;inset:0;background:var(--navy)"></div>
<div style="position:absolute;left:0;top:0;bottom:0;width:520px"><img class="cover" src="{IMG}fabric.png"></div>
<div style="position:absolute;left:520px;top:0;bottom:0;width:6px;background:var(--gold)"></div>
<div style="position:absolute;right:90px;top:64px;color:#fff;width:520px">
  <div style="font-size:30px;font-weight:800">خصم يصل إلى</div>
  <div style="display:flex;align-items:flex-start;gap:6px;margin-top:-6px">
    <span class="num" style="font-size:220px">50</span><span class="num" style="font-size:90px;margin-top:30px;color:var(--rose)">%</span></div>
  <span class="btn btn-w" style="font-size:20px;height:56px;padding:0 44px;margin-top:4px">اطلب الحين</span>
</div>{stamp(120, 30, 26)}"""))

FILES["offer-bundle-1200x500"] = (1200, 500, page(1200, 500, f"""
<div style="position:absolute;inset:0;background:#fff"></div>
<div class="studio" style="position:absolute;left:0;top:0;bottom:0;width:560px"></div>
<div class="floor" style="left:280px;bottom:60px;width:500px;height:60px"></div>
<img class="p" src="{IMG}box-white.png" style="left:40px;bottom:230px;width:290px">
<img class="p" src="{IMG}box-white.png" style="left:250px;bottom:200px;width:290px">
<img class="p" src="{IMG}box-open.png" style="left:70px;bottom:70px;width:420px">
<div style="position:absolute;right:80px;top:70px;color:var(--navy);width:540px">
  <div class="kicker" style="font-size:22px">باكدج العائلة</div>
  <h1 style="font-size:64px;margin:8px 0 10px">3 علب بسعر 2</h1>
  <div style="font-size:22px;font-weight:700;color:var(--muted)">15 زوج · أسود وأبيض</div>
  <div style="display:flex;align-items:baseline;gap:16px;margin-top:18px">
    <span style="font-size:46px;font-weight:900;color:var(--sale)">219 ر.س</span><s style="font-size:26px;color:var(--muted)">447 ر.س</s></div>
  <span class="btn btn-n" style="font-size:20px;height:56px;padding:0 40px;margin-top:22px">أضف الباكدج</span>
</div>{stamp(120, 30, 26)}"""))

# ---------------- Social ----------------
FILES["instagram-post-1080x1080"] = (1080, 1080, page(1080, 1080, f"""
<div style="position:absolute;inset:0 0 380px 0"><img class="cover" src="{IMG}black-lifestyle.jpg" style="object-position:50% 64%"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:380px;background:var(--navy);color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 80px">
  <div><div class="kicker" style="font-size:26px;color:var(--gold-soft)">شرابات لمرضى السكري</div>
  <div style="display:flex;align-items:flex-end;gap:16px"><span class="num" style="font-size:160px">1+1</span><span style="font-size:48px;font-weight:900;padding-bottom:16px">مجانًا</span></div></div>
  <div style="text-align:left"><div style="font-size:28px;font-weight:700;opacity:.9">10 أزواج</div>
  <div style="font-size:84px;font-weight:900;line-height:1">149</div><div style="font-size:26px;font-weight:700;color:var(--gold-soft)">ر.س بدلًا من <s>298</s></div></div>
</div>
<img src="{IMG}logo-white.png" style="position:absolute;top:44px;right:56px;height:44px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.35))">{stamp(170, 40, 40)}"""))

FILES["instagram-story-1080x1920"] = (1080, 1920, page(1080, 1920, f"""
<div style="position:absolute;inset:0 0 820px 0"><img class="cover" src="{IMG}black-lifestyle.jpg" style="object-position:50% 60%"></div>
<img src="{IMG}logo-white.png" style="position:absolute;top:150px;left:50%;transform:translateX(-50%);height:58px;filter:drop-shadow(0 2px 10px rgba(0,0,0,.35))">
<div style="position:absolute;left:0;right:0;bottom:0;height:820px;background:var(--navy);color:#fff;text-align:center;padding-top:70px">
  <div class="kicker" style="font-size:38px;color:var(--gold-soft)">شرابات مصممة لمرضى السكري</div>
  <div style="display:flex;align-items:flex-end;justify-content:center;gap:22px"><span class="num" style="font-size:230px">1+1</span>
  <span style="font-size:68px;font-weight:900;padding-bottom:26px">مجانًا</span></div>
  <div style="font-size:42px;font-weight:700;opacity:.92;margin-top:6px">10 أزواج بـ <b style="font-size:52px">149</b> ر.س بدلًا من <s style="opacity:.75">298</s></div>
  <span class="btn btn-w" style="font-size:44px;height:120px;width:760px;margin-top:70px">اطلب الحين</span>
</div>{stamp(220, 50, 250)}"""))

FILES["facebook-ad-1200x628"] = (1200, 628, page(1200, 628, f"""
<div style="position:absolute;left:0;top:0;bottom:0;width:640px"><img class="cover" src="{IMG}black-lifestyle.jpg" style="object-position:50% 62%"></div>
<div style="position:absolute;right:0;top:0;bottom:0;width:560px;background:var(--navy);color:#fff;padding:60px 64px 0 50px">
  <img src="{IMG}logo-white.png" style="height:36px;display:block;margin-bottom:34px">
  <div class="kicker" style="font-size:22px;color:var(--gold-soft)">شرابات لمرضى السكري</div>
  <div style="display:flex;align-items:flex-end;gap:14px"><span class="num" style="font-size:130px">1+1</span><span style="font-size:40px;font-weight:900;padding-bottom:12px">مجانًا</span></div>
  <div style="font-size:22px;font-weight:600;opacity:.92">10 أزواج بـ <b style="font-size:28px">149</b> ر.س بدلًا من <s style="opacity:.75">298</s></div>
  <span class="btn btn-w" style="font-size:22px;height:58px;padding:0 46px;margin-top:30px">تسوّق الآن</span>
</div>{stamp(130, 30, 30)}"""))

for name, (w, h, html) in FILES.items():
    (HERE / f"{name}.html").write_text(html, encoding="utf-8")
(HERE / "list.txt").write_text("\n".join(f"{n} {w} {h}" for n, (w, h, _) in FILES.items()))
print(len(FILES))
