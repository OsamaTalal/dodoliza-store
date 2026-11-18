# Builds the Dodoliza diabetic-socks store pages (HTML + Tailwind CDN). Run: python3 build.py
import json, os

SITE = "https://socks.dodoliza.com"
WA = "966500000000"  # placeholder WhatsApp number
FREE_SHIP = 150
SHIP = 25
PACKS = [
    {"pairs": 3, "price": 89},
    {"pairs": 6, "price": 159},
    {"pairs": 12, "price": 289},
]
COLORS = {
    "white": ("#FFFFFF", "أبيض", "White"),
    "black": ("#1F2523", "أسود", "Black"),
    "grey": ("#9AA5A2", "رمادي", "Grey"),
    "navy": ("#22324A", "كحلي", "Navy"),
    "beige": ("#D9CDB8", "بيج", "Beige"),
}
LENGTHS = {"ankle": ("كاحل", "Ankle"), "crew": ("متوسط", "Crew"), "knee": ("حتى الركبة", "Knee")}
SIZES = [("S", "36–39"), ("M", "40–43"), ("L", "44–47")]
PRODUCTS = [
    {"id": "comfort-crew", "nameAr": "شراب الراحة اليومية", "nameEn": "Everyday Comfort Crew", "length": "crew", "colors": ["white", "black", "grey"],
     "descAr": "الطول المتوسط اللي يناسب أغلب الأيام، بحافة واسعة ونعل مبطّن.", "descEn": "The mid-length pair for most days, with a wide top and cushioned sole."},
    {"id": "bamboo-silver", "nameAr": "شراب بامبو ونانو الفضة", "nameEn": "Bamboo Silver Crew", "length": "crew", "colors": ["navy", "grey"],
     "descAr": "ألياف بامبو مع فضة داخل الخيوط، لقدم ناشفة وريحة أقل.", "descEn": "Bamboo fibers with silver in the yarn, for drier feet and less odor."},
    {"id": "soft-ankle", "nameAr": "شراب الكاحل الناعم", "nameEn": "Soft Ankle", "length": "ankle", "colors": ["white", "black"],
     "descAr": "قصير وخفيف للبيت والمشاوير القريبة، مقدمة بدون خياطة.", "descEn": "Short and light for home and quick errands, seamless toe."},
    {"id": "home-ankle", "nameAr": "شراب البيت", "nameEn": "Home Ankle", "length": "ankle", "colors": ["beige", "grey"],
     "descAr": "نعل مبطّن ناعم للوقفة الطويلة في البيت.", "descEn": "Soft cushioned sole for long hours on your feet at home."},
    {"id": "gentle-knee", "nameAr": "شراب الركبة اللطيف", "nameEn": "Gentle Knee", "length": "knee", "colors": ["black", "navy"],
     "descAr": "طويل حتى تحت الركبة، حافته ما تشد على الساق.", "descEn": "Knee-high with a top that does not squeeze the calf."},
    {"id": "travel-knee", "nameAr": "شراب السفر", "nameEn": "Travel Knee", "length": "knee", "colors": ["grey", "black"],
     "descAr": "للرحلات الطويلة والجلوس الطويل، يتنفس ويمتص الرطوبة.", "descEn": "For long trips and long sitting; breathable and moisture-wicking."},
]
FAQ = [
    ("إيش الفرق بين هذا الشراب والشراب العادي؟", "What makes these different from regular socks?",
     "حافته واسعة ما تضغط على الساق، ومقدمته بدون خياطة، وقماشه بامبو مع فضة يتنفس ويمتص الرطوبة، ونعله مبطّن.",
     "A wide top that doesn't squeeze the leg, a seamless toe, breathable bamboo-silver fabric that absorbs moisture, and a cushioned sole."),
    ("كيف أعرف مقاسي؟", "How do I find my size?",
     "اختر حسب مقاس الحذاء: S من 36 إلى 39، وM من 40 إلى 43، وL من 44 إلى 47. لو كنت بين مقاسين، اختر الأكبر.",
     "Pick by shoe size: S 36–39, M 40–43, L 44–47. If you are between sizes, choose the larger one."),
    ("هل يناسب الاستخدام اليومي؟", "Can I wear them every day?",
     "نعم، مصمّم للبس من الصبح لآخر اليوم. وإذا كانت لديك حالة خاصة في القدم، استشر طبيبك.",
     "Yes, they are made for all-day wear. If you have a specific foot condition, consult your doctor."),
    ("كيف أغسله؟", "How do I wash them?",
     "غسيل بماء فاتر على دورة لطيفة، بدون مبيّض، وتجفيف بالهواء. الفضة داخل الخيوط وتبقى مع الغسيل.",
     "Wash warm on a gentle cycle, no bleach, air dry. The silver is in the yarn and stays through washing."),
    ("هل الدفع عند الاستلام متاح؟", "Is cash on delivery available?",
     "نعم، الدفع عند الاستلام متاح في كل مناطق المملكة، ومعه البطاقات وApple Pay.",
     "Yes, cash on delivery is available across Saudi Arabia, along with cards and Apple Pay."),
    ("إيش سياسة الاسترجاع؟", "What is the return policy?",
     "تقدر ترجع الطلب خلال 14 يوم إذا كانت العبوة مقفلة. (سياسة مبدئية للتعديل)",
     "You can return unopened packs within 14 days. (Placeholder policy, to be confirmed)"),
]

def t(ar, en):
    return f'<span data-l="ar">{ar}</span><span data-l="en" class="lat">{en}</span>'

ICONS = {
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "bag": '<path d="M6 7h12l-1 13H7z"/><path d="M9 7a3 3 0 0 1 6 0"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "top": '<path d="M4 7h16"/><path d="M6 7v3M10 7v3M14 7v3M18 7v3"/><path d="M7 14c2 3 8 3 10 0"/>',
    "toe": '<path d="M5 15c0-5 3-8 7-8s7 3 7 8"/><path d="M5 15h14"/>',
    "leaf": '<path d="M5 19c0-8 6-14 14-14 0 8-6 14-14 14z"/><path d="M5 19L14 10"/>',
    "sole": '<path d="M4 17h16"/><path d="M6 17c0-3 2-5 6-5s6 2 6 5"/><path d="M8 20h8"/>',
    "truck": '<path d="M3 7h11v9H3z"/><path d="M14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',
    "return": '<path d="M9 14L4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/>',
    "cash": '<rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "check": '<path d="M5 12l5 5 9-10"/>',
    "wa": '<path d="M4 20l1.4-4A8 8 0 1 1 8 18.6z"/><path d="M9 9.5c.5 2 2.5 4 4.5 4.5l1.2-1.2 2 1-.6 1.6c-3.5 0-7-3.5-7-7l1.6-.6 1 2z"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
}
def icon(name, cls="icon", extra=""):
    return f'<svg class="{cls} {extra}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def sock(color="#FFFFFF", stroke="#123B3A"):
    # original flat sock illustration used as a placeholder product image
    return (f'<svg class="sock" viewBox="0 0 200 240" aria-hidden="true">'
            f'<path d="M70 20h70v110c0 10 6 18 16 24l20 12c14 9 18 26 9 40-8 13-24 17-38 10L74 186c-20-11-30-30-30-52V20z" '
            f'fill="{color}" stroke="{stroke}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M70 20h70v26H70z" fill="{color}" stroke="{stroke}" stroke-width="3"/>'
            + "".join(f'<path d="M{78+i*8} 24v18" stroke="{stroke}" stroke-opacity=".35" stroke-width="2"/>' for i in range(8))
            + f'<path d="M150 176c10 6 22 4 28-4" fill="none" stroke="{stroke}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="0"/>'
            f'<path d="M58 160c18 14 40 20 58 18" fill="none" stroke="{stroke}" stroke-opacity=".25" stroke-width="2"/></svg>')

def ph(color, note_ar, note_en, cls=""):
    return f'<div class="ph {cls}">{sock(COLORS[color][0])}<span class="ph-note">{t(note_ar, note_en)}</span></div>'

NAV = [("index.html", "الرئيسية", "Home"), ("shop.html", "المتجر", "Shop"), ("about.html", "قصتنا", "Our story"), ("contact.html", "تواصل معنا", "Contact")]

def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t(a, e)}</a>' for h, a, e in NAV)
    return f'''<header class="site-header"><div class="wrap"><div class="bar">
<a class="logo" href="index.html" aria-label="دودليزا">{icon("leaf")}{t("دودليزا", "Dodoliza")}</a>
<nav class="nav nav-desktop" aria-label="Main">{links}</nav>
<div style="display:flex;align-items:center;gap:6px">
<button type="button" class="tool" data-lang-toggle data-aria-ar="Switch to English" data-aria-en="التبديل إلى العربية">{icon("globe")}<span data-l="ar" class="lat">EN</span><span data-l="en">عربي</span></button>
<a class="tool" href="cart.html" data-aria-ar="السلة" data-aria-en="Cart">{icon("bag")}<span class="badge" data-cart-count hidden>0</span></a>
</div></div></div>
<div class="subnav"><div class="wrap"><nav class="nav" aria-label="Main mobile">{links}</nav></div></div></header>'''

FOOTER = f'''<footer class="site-footer"><div class="wrap section" style="display:grid;gap:32px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">
<div style="display:flex;flex-direction:column;gap:10px"><div class="logo" style="color:#fff">{icon("leaf")}{t("دودليزا", "Dodoliza")}</div>
<p>{t("شراب مصمّم لراحة مرضى السكري، من الصبح لآخر اليوم.", "Socks designed for comfort for people with diabetes, morning to night.")}</p></div>
<div style="display:flex;flex-direction:column;gap:6px"><strong>{t("المتجر", "Shop")}</strong>
<a href="shop.html">{t("كل الشرابات", "All socks")}</a><a href="product.html">{t("شراب الراحة اليومية", "Everyday Comfort Crew")}</a><a href="cart.html">{t("السلة", "Cart")}</a></div>
<div style="display:flex;flex-direction:column;gap:6px"><strong>{t("الشركة", "Company")}</strong>
<a href="about.html">{t("قصتنا", "Our story")}</a><a href="contact.html">{t("تواصل معنا", "Contact")}</a></div>
<div style="display:flex;flex-direction:column;gap:6px"><strong>{t("الدفع", "Payment")}</strong>
<span>{t("الدفع عند الاستلام، مدى، فيزا، Apple Pay", "Cash on delivery, mada, Visa, Apple Pay")}</span></div>
</div><div class="wrap" style="padding-block:18px;border-top:1px solid rgba(255,255,255,.15)"><span class="small">© 2026 {t("دودليزا", "Dodoliza")}</span></div></footer>
<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" data-aria-ar="تواصل معنا على واتساب" data-aria-en="Chat with us on WhatsApp">{icon("wa", extra="", cls="icon")}</a>'''

def page(fname, title_ar, desc_ar, title_en, body, active="", schema=None, noindex=False, body_cls=""):
    data = json.dumps({"products": PRODUCTS, "packs": PACKS, "freeShipping": FREE_SHIP, "shipping": SHIP}, ensure_ascii=False)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    canon = SITE + "/" + ("" if fname == "index.html" else fname)
    head = f'''<title>{title_ar}</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc_ar}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="ar-SA" href="{canon}"><link rel="alternate" hreflang="en" href="{canon}?lang=en">
<meta property="og:type" content="{'product' if fname == 'product.html' else 'website'}"><meta property="og:title" content="{title_ar}">
<meta property="og:description" content="{desc_ar}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="ar_SA">
<meta name="twitter:card" content="summary_large_image">
{'<meta name="robots" content="noindex, nofollow">' if noindex else '<meta name="robots" content="index, follow">'}
<meta name="theme-color" content="#FFFFFF">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap">
<script src="https://cdn.tailwindcss.com/3.4.17"></script>
<script>window.tailwind&&(tailwind.config={{corePlugins:{{preflight:false}},theme:{{extend:{{colors:{{ink:"var(--color-text)",teal:"var(--color-primary)",tint:"var(--color-tint)",cta:"var(--color-cta)"}}}}}}}})</script>
<link rel="stylesheet" href="assets/tokens.css"><link rel="stylesheet" href="assets/app.css">
{ld}'''
    content = f'''<a href="#main" class="sr-only focus:not-sr-only">تخطي إلى المحتوى</a>
{header(active)}
<main id="main">{body}</main>
{FOOTER}
<script src="assets/data.js"></script>
<script src="assets/app.js"></script>'''
    if fname == "index.html":
        os.makedirs("_artifact", exist_ok=True)
        open("_artifact/index.html", "w").write(f'{head}\n<div class="{body_cls}">{content}</div>')
    if True:
        html = f'<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n{head}\n</head>\n<body class="{body_cls}">\n{content}\n</body>\n</html>'
    open(fname, "w").write(html)
    open("assets/data.js", "w").write("window.DODO=" + data + ";")

def price_from():
    return PACKS[0]["price"]

def pcard(p, link="product.html", pack_dynamic=False):
    sw = "".join(f'<span class="sw" style="background:{COLORS[c][0]}" title="{COLORS[c][1]}"></span>' for c in p["colors"])
    lab = t(LENGTHS[p["length"]][0], LENGTHS[p["length"]][1])
    price_attr = ' data-pack-price' if pack_dynamic else ''
    return f'''<a class="pcard" href="{link}">
{ph(p["colors"][0], "صورة المنتج (مؤقتة)", "Product photo (placeholder)")}
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><span class="muted small">{lab}</span><span class="swatches">{sw}</span></div>
<h3>{t(p["nameAr"], p["nameEn"])}</h3>
<div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap"><span class="muted small">{t("يبدأ من", "From")}</span><span class="price"{price_attr}>{price_from()} ر.س</span><span class="muted small" data-pack-label>{t("3 أزواج", "3 pairs")}</span></div>
</a>'''

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Dodoliza دودليزا", "url": SITE,
       "contactPoint": {"@type": "ContactPoint", "telephone": "+" + WA, "contactType": "customer service", "areaServed": "SA", "availableLanguage": ["ar", "en"]}}
def faq_schema():
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, _, a, _ in FAQ]}
def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (n, u) in enumerate(items)]}

def faq_html(items):
    return "".join(f'''<details class="faq"><summary>{t(qa, qe)}{icon("chev", extra="chev")}</summary><div class="a">{t(aa, ae)}</div></details>''' for qa, qe, aa, ae in items)

TRUST = f'''<div class="trust">
<div>{icon("truck")}<div><strong>{t("شحن مجاني", "Free shipping")}</strong><p class="muted small">{t(f"للطلبات فوق {FREE_SHIP} ر.س", f"On orders over SAR {FREE_SHIP}")}</p></div></div>
<div>{icon("return")}<div><strong>{t("استرجاع سهل", "Easy returns")}</strong><p class="muted small">{t("خلال 14 يوم للعبوات المقفلة", "Within 14 days, unopened")}</p></div></div>
<div>{icon("cash")}<div><strong>{t("الدفع عند الاستلام", "Cash on delivery")}</strong><p class="muted small">{t("في كل مناطق المملكة", "Across Saudi Arabia")}</p></div></div>
<div>{icon("lock")}<div><strong>{t("دفع آمن", "Secure payment")}</strong><p class="muted small">{t("مدى، فيزا، Apple Pay", "mada, Visa, Apple Pay")}</p></div></div>
</div>'''

BENEFITS = [
    ("top", "حافة ما تضغط", "Non-binding top", "تمسك الشراب بدون ما تشد أو تعلّم على الساق.", "Stays up without squeezing or leaving marks on the leg."),
    ("toe", "مقدمة بدون خياطة", "Seamless toe", "ما فيه خياطة بارزة تحتك بالأصابع.", "No raised seam rubbing against the toes."),
    ("leaf", "بامبو مع فضة", "Bamboo and silver", "يتنفس ويمتص الرطوبة ويقلل الريحة طول اليوم.", "Breathes, absorbs moisture and keeps odor down all day."),
    ("sole", "نعل مبطّن", "Cushioned sole", "راحة إضافية للمشي والوقفة الطويلة.", "Extra comfort for walking and long hours standing."),
]

# ---------------- HOME ----------------
lineup = "".join(pcard(p) for p in PRODUCTS)
benefits = "".join(f'''<div class="card" style="padding:24px;display:flex;flex-direction:column;gap:10px">
<span style="width:56px;height:56px;border-radius:14px;background:var(--color-tint);display:flex;align-items:center;justify-content:center">{icon(i)}</span>
<h3 style="font-size:var(--text-h3)">{t(a, e)}</h3><p class="muted">{t(da, de)}</p></div>''' for i, a, e, da, de in BENEFITS)
sizes_rows = "".join(f'''<div class="card" style="padding:20px;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center">
<span class="num" style="font-size:2.25rem;font-weight:700">{s}</span><span class="muted">{t("مقاس الحذاء", "Shoe size")}</span><span class="num" style="font-weight:700;font-size:1.25rem">{r}</span></div>''' for s, r in SIZES)
testis = "".join(f'''<figure class="card" style="margin:0;padding:24px;display:flex;flex-direction:column;gap:12px;border:2px dashed var(--color-border)">
<span class="small" style="align-self:flex-start;background:var(--color-tint);padding:2px 10px;border-radius:6px">{t("مكان مؤقت لرأي عميل", "Placeholder testimonial")}</span>
<blockquote style="margin:0;font-size:1.25rem;line-height:1.7">{t("هنا يُكتب رأي عميل حقيقي بعد التجربة.", "A real customer review goes here.")}</blockquote>
<figcaption class="muted">{t(f"اسم العميل {n}، المدينة", f"Customer name {n}, city")}</figcaption></figure>''' for n in (1, 2, 3))

home = f'''
<section class="surface"><div class="wrap section" style="display:grid;gap:40px;align-items:center;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
<div style="display:flex;flex-direction:column;gap:20px;min-width:0">
<h1 style="font-size:clamp(2.25rem,5vw,3.5rem)">{t("راحة تلبسها<br>من الصبح لآخر اليوم", "Comfort you wear<br>from morning to night")}</h1>
<p class="muted" style="font-size:1.25rem;max-width:34ch">{t("شراب مصمّم لمرضى السكري: حافة واسعة ما تضغط، مقدمة بدون خياطة، وألياف بامبو مع فضة تحمي القدم من الرطوبة.", "Socks designed for people with diabetes: a wide top that doesn't squeeze, a seamless toe, and bamboo-silver fibers that keep feet dry.")}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-cta" href="shop.html">{t("تسوّق الآن", "Shop now")}{icon("arrow", extra="flip")}</a><a class="btn btn-ghost" href="#why">{t("ليش شراب مخصّص؟", "Why diabetic socks?")}</a></div>
<p class="small muted" style="display:flex;gap:8px;align-items:center">{icon("cash")}{t("الدفع عند الاستلام متاح، وشحن مجاني فوق 150 ر.س", "Cash on delivery available, free shipping over SAR 150")}</p>
</div>
<div class="rib-frame card" style="aspect-ratio:4/5;max-width:100%">{ph("white", "صورة: الشراب على القدم (مؤقتة)", "Photo: sock on foot (placeholder)", "fill")}</div>
</div></section>

<section class="wrap section" id="why" style="display:flex;flex-direction:column;gap:28px">
<div style="display:flex;flex-direction:column;gap:10px;max-width:60ch"><span class="eyebrow-rule"></span><h2 style="font-size:var(--text-h2)">{t("ليش شراب مخصّص لمرضى السكري؟", "Why diabetic socks?")}</h2>
<p class="muted">{t("القدم مع السكري تحتاج عناية أكثر. كل تفصيلة في الشراب مصمّمة عشان الراحة والحماية اليومية.", "Feet need extra care with diabetes. Every detail of these socks is made for everyday comfort and protection.")}</p></div>
<div style="display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{benefits}</div>
</section>

<section class="surface"><div class="wrap section" style="display:flex;flex-direction:column;gap:28px">
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap"><h2 style="font-size:var(--text-h2)">{t("كل الشرابات", "All our socks")}</h2><a href="shop.html" class="btn btn-ghost">{t("عرض المتجر", "View shop")}</a></div>
<div style="display:grid;gap:24px;grid-template-columns:repeat(auto-fill,minmax(min(100%,160px),1fr))">{lineup}</div>
</div></section>

<section class="wrap section" style="display:grid;gap:32px;align-items:center;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
<div style="display:flex;flex-direction:column;gap:14px;min-width:0"><span class="eyebrow-rule"></span><h2 style="font-size:var(--text-h2)">{t("كيف تختار مقاسك", "How to choose your size")}</h2>
<p class="muted">{t("اختر حسب مقاس حذائك. لو كنت بين مقاسين، اختر المقاس الأكبر عشان الحافة تبقى مريحة.", "Choose by your shoe size. If you are between two sizes, pick the larger one so the top stays comfortable.")}</p>
<a href="product.html#size-group" class="btn btn-ghost" style="align-self:flex-start">{icon("ruler")}{t("جدول المقاسات الكامل", "Full size chart")}</a></div>
<div style="display:grid;gap:12px;grid-template-columns:repeat(3,minmax(0,1fr))">{sizes_rows}</div>
</section>

<section class="tint"><div class="wrap section" style="display:flex;flex-direction:column;gap:24px">
<h2 style="font-size:var(--text-h2)">{t("آراء عملائنا", "What customers say")}</h2>
<div style="display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">{testis}</div></div></section>

<section class="surface"><div class="wrap" style="padding-block:40px">{TRUST}</div></section>

<section class="wrap section" style="display:flex;flex-direction:column;gap:16px;max-width:860px">
<h2 style="font-size:var(--text-h2)">{t("أسئلة شائعة", "Frequently asked questions")}</h2>{faq_html(FAQ)}</section>
'''
page("index.html", "دودليزا | شراب مرضى السكري المريح", "شراب مصمّم لراحة مرضى السكري: حافة لا تضغط، مقدمة بدون خياطة، بامبو مع فضة، ونعل مبطّن. شحن مجاني والدفع عند الاستلام في السعودية.",
     "Dodoliza | Comfortable diabetic socks", home, "index.html",
     [ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": "دودليزا", "url": SITE, "inLanguage": ["ar-SA", "en"]}, faq_schema()])

# ---------------- SHOP ----------------
def chips(key, opts):
    allb = f'<button type="button" class="chip" data-filter="{key}" data-value="all" aria-pressed="true">{t("الكل", "All")}</button>'
    return allb + "".join(f'<button type="button" class="chip" data-filter="{key}" data-value="{v}" aria-pressed="false">{lab}</button>' for v, lab in opts)
len_opts = [(k, t(a, e)) for k, (a, e) in LENGTHS.items()]
col_opts = [(k, f'<span class="sw" style="background:{h}"></span>{t(a, e)}') for k, (h, a, e) in COLORS.items()]
size_opts = [(s, f'<span class="num">{s}</span> <span class="muted small num">{r}</span>') for s, r in SIZES]
pack_opts = [(str(p["pairs"]), t(f'{p["pairs"]} أزواج', f'{p["pairs"]} pairs')) for p in PACKS]
cards = "".join(f'<div class="pcard-wrap" data-length="{p["length"]}" data-colors="{",".join(p["colors"])}" data-sizes="S,M,L">{pcard(p, pack_dynamic=True)}</div>' for p in PRODUCTS)
shop = f'''
<section class="surface"><div class="wrap" style="padding-block:40px;display:flex;flex-direction:column;gap:10px">
<nav aria-label="breadcrumb" class="small muted"><a href="index.html">{t("الرئيسية", "Home")}</a> / {t("المتجر", "Shop")}</nav>
<h1 style="font-size:var(--text-h1)">{t("شرابات مرضى السكري", "Diabetic socks")}</h1>
<p class="muted" style="max-width:60ch">{t("كل الشرابات بنفس التفاصيل: حافة ما تضغط، مقدمة بدون خياطة، وبامبو مع فضة. اختر الطول واللون اللي يناسبك.", "Every pair shares the same details: a non-binding top, seamless toe, and bamboo-silver fabric. Choose the length and color you like.")}</p>
</div></section>
<section class="wrap section" style="display:grid;gap:32px;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));align-items:start">
<aside aria-label="Filters" style="display:flex;flex-direction:column;gap:22px">
<div style="display:flex;flex-direction:column;gap:10px"><h2 style="font-size:1.25rem">{t("الطول", "Length")}</h2><div style="display:flex;gap:8px;flex-wrap:wrap">{chips("length", len_opts)}</div></div>
<div style="display:flex;flex-direction:column;gap:10px"><h2 style="font-size:1.25rem">{t("اللون", "Color")}</h2><div style="display:flex;gap:8px;flex-wrap:wrap">{chips("color", col_opts)}</div></div>
<div style="display:flex;flex-direction:column;gap:10px"><h2 style="font-size:1.25rem">{t("المقاس", "Size")}</h2><div style="display:flex;gap:8px;flex-wrap:wrap">{chips("size", size_opts)}</div></div>
<div style="display:flex;flex-direction:column;gap:10px"><h2 style="font-size:1.25rem">{t("عدد الأزواج", "Pack size")}</h2><div style="display:flex;gap:8px;flex-wrap:wrap">{chips("pack", pack_opts)}</div></div>
<button type="button" class="btn btn-ghost" data-filter-reset>{t("مسح الفلاتر", "Clear filters")}</button>
</aside>
<div style="grid-column:span 2 / span 2;min-width:0;display:flex;flex-direction:column;gap:18px" class="shop-results">
<p class="muted" aria-live="polite"><span class="num" data-shop-count>6</span> {t("منتجات", "products")}</p>
<div data-shop-grid style="display:grid;gap:24px;grid-template-columns:repeat(auto-fill,minmax(min(100%,160px),1fr))">{cards}</div>
<div data-shop-empty hidden class="card" style="padding:28px;display:flex;flex-direction:column;gap:12px;align-items:flex-start">
<strong>{t("ما فيه شراب بهذي الاختيارات", "No socks match these filters")}</strong><p class="muted">{t("جرّب لون أو طول ثاني، أو امسح الفلاتر.", "Try another color or length, or clear the filters.")}</p>
<button type="button" class="btn btn-primary" data-filter-reset>{t("مسح الفلاتر", "Clear filters")}</button></div>
</div></section>
<style>@media (max-width:899px){{.shop-results{{grid-column:auto !important}}}}</style>
'''
page("shop.html", "متجر شرابات مرضى السكري | دودليزا", "تسوّق شرابات دودليزا لمرضى السكري بطول الكاحل والمتوسط وحتى الركبة، بعبوات 3 و6 و12 زوج. شحن مجاني فوق 150 ر.س.",
     "Shop diabetic socks | Dodoliza", shop, "shop.html",
     [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "شرابات مرضى السكري", "url": SITE + "/shop.html",
       "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + "/product.html#" + p["id"], "name": p["nameAr"]} for i, p in enumerate(PRODUCTS)]}},
      crumbs([("الرئيسية", ""), ("المتجر", "shop.html")])])

# ---------------- PRODUCT ----------------
P = PRODUCTS[0]
slides = [("white", "الشراب كامل", "Full sock"), ("grey", "لقطة قريبة للقماش", "Fabric close-up"), ("black", "المقدمة بدون خياطة", "Seamless toe"), ("white", "النعل المبطّن", "Cushioned sole")]
gal = "".join(f'''<div data-slide="{i}" {"hidden" if i else ""}><button type="button" class="zoom ph card" aria-pressed="false" style="width:100%;aspect-ratio:1;border:0;padding:0" data-aria-ar="تكبير الصورة" data-aria-en="Zoom image">{sock(COLORS[c][0])}<span class="ph-note">{t(a + " (مؤقتة)", e + " (placeholder)")}</span></button></div>''' for i, (c, a, e) in enumerate(slides))
thumbs = "".join(f'<button type="button" class="thumb ph" data-thumb="{i}" aria-current="{"true" if i == 0 else "false"}" data-aria-ar="{a}" data-aria-en="{e}">{sock(COLORS[c][0])}</button>' for i, (c, a, e) in enumerate(slides))
size_btns = "".join(f'<button type="button" class="chip" role="radio" aria-checked="false" data-pick="size" data-value="{s}"><span class="num" style="font-weight:700">{s}</span><span class="muted small num">{r}</span></button>' for s, r in SIZES)
color_btns = "".join(f'<button type="button" class="chip" role="radio" aria-checked="{"true" if i == 0 else "false"}" data-pick="color" data-value="{COLORS[c][1]}"><span class="sw" style="background:{COLORS[c][0]}"></span>{t(COLORS[c][1], COLORS[c][2])}</button>' for i, c in enumerate(P["colors"]))
base = PACKS[0]["price"] / PACKS[0]["pairs"]
def pack_btn(pk):
    per = pk["price"] / pk["pairs"]; save = round((base - per) * pk["pairs"])
    sv = f'<span class="save">{t(f"توفّر {save} ر.س", f"Save SAR {save}")}</span>' if save > 0 else f'<span class="muted small">{t("السعر الأساسي", "Base price")}</span>'
    return f'''<button type="button" class="pack-opt" role="radio" aria-checked="{"true" if pk["pairs"] == 6 else "false"}" data-pick="pack" data-value="{pk["pairs"]}">
<span style="display:flex;flex-direction:column;gap:2px"><strong>{t(f'{pk["pairs"]} أزواج', f'{pk["pairs"]} pairs')}</strong><span class="muted small">{t(f"{per:.1f} ر.س للزوج", f"SAR {per:.1f} per pair")}</span></span>
<span style="display:flex;flex-direction:column;align-items:flex-end;gap:2px"><span class="price num" style="font-size:1.375rem">{t(f'{pk["price"]} ر.س', f'SAR {pk["price"]}')}</span>{sv}</span></button>'''
packs_html = "".join(pack_btn(pk) for pk in PACKS)
chart_rows = "".join(f'<tr><td class="num" style="font-weight:700">{s}</td><td class="num">{r}</td><td class="num">{["22–24", "25–27", "28–30"][i]}</td></tr>' for i, (s, r) in enumerate(SIZES))
product_body = f'''
<div data-product="{P["id"]}">
<section class="wrap" style="padding-block:28px 64px;display:grid;gap:40px;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));align-items:start">
<div style="display:flex;flex-direction:column;gap:12px;min-width:0">
<nav aria-label="breadcrumb" class="small muted"><a href="index.html">{t("الرئيسية", "Home")}</a> / <a href="shop.html">{t("المتجر", "Shop")}</a> / {t(P["nameAr"], P["nameEn"])}</nav>
{gal}
<div style="display:grid;gap:10px;grid-template-columns:repeat(4,minmax(0,1fr))">{thumbs}</div>
<p class="small muted">{t("اضغط على الصورة للتكبير", "Tap the image to zoom")}</p>
</div>
<div style="display:flex;flex-direction:column;gap:22px;min-width:0">
<div style="display:flex;flex-direction:column;gap:8px"><span class="muted">{t("طول متوسط", "Crew length")}</span>
<h1 style="font-size:clamp(2rem,4vw,2.75rem)">{t(P["nameAr"], P["nameEn"])}</h1>
<p class="muted">{t(P["descAr"], P["descEn"])}</p>
<div style="display:flex;align-items:baseline;gap:10px"><span class="price num" data-pp-price>159 ر.س</span><span class="muted" data-pp-pairs>6 أزواج</span></div></div>

<div id="size-group" style="display:flex;flex-direction:column;gap:10px" role="radiogroup" aria-labelledby="size-label">
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><strong id="size-label">{t("المقاس", "Size")}</strong>
<button type="button" class="tool" style="color:var(--color-primary);padding:0 8px" data-open-chart>{icon("ruler")}{t("جدول المقاسات", "Size chart")}</button></div>
<div style="display:flex;gap:8px;flex-wrap:wrap">{size_btns}</div><p class="err" data-size-err hidden role="alert">{t("اختر المقاس قبل الإضافة للسلة.", "Choose a size before adding to cart.")}</p></div>

<div style="display:flex;flex-direction:column;gap:10px" role="radiogroup" aria-labelledby="color-label"><strong id="color-label">{t("اللون", "Color")}: <span data-color-name></span></strong><div style="display:flex;gap:8px;flex-wrap:wrap">{color_btns}</div></div>

<div style="display:flex;flex-direction:column;gap:10px" role="radiogroup" aria-labelledby="pack-label"><strong id="pack-label">{t("عدد الأزواج", "Pack size")}</strong><div class="pack">{packs_html}</div></div>

<button type="button" class="btn btn-cta btn-block" data-add style="min-height:60px;font-size:1.25rem">{icon("bag")}{t("أضف إلى السلة", "Add to cart")}</button>
<p class="small muted" style="display:flex;gap:8px;align-items:center">{icon("truck")}{t("شحن مجاني فوق 150 ر.س، والدفع عند الاستلام متاح", "Free shipping over SAR 150, cash on delivery available")}</p>
<p class="card small" style="padding:14px 16px;display:flex;gap:10px;align-items:flex-start;border:1px solid var(--color-border)">{icon("heart")}{t("إذا كانت لديك حالة خاصة في القدم، استشر طبيبك قبل الاستخدام.", "If you have a specific foot condition, consult your doctor.")}</p>

<div>
<details class="faq" open><summary>{t("المميزات", "Features")}{icon("chev", extra="chev")}</summary><div class="a"><ul style="margin:0;padding-inline-start:20px;display:flex;flex-direction:column;gap:6px">
{"".join(f"<li>{t(a + ': ' + da, e + ': ' + de)}</li>" for _, a, e, da, de in BENEFITS)}</ul></div></details>
<details class="faq"><summary>{t("الخامة", "Material")}{icon("chev", extra="chev")}</summary><div class="a">{t("ألياف بامبو 80%، بوليامايد 17%، إيلاستين 3%، مع خيوط فضة. (نسب مؤقتة للتأكيد)", "80% bamboo viscose, 17% polyamide, 3% elastane, with silver-infused yarn. (Placeholder composition)")}</div></details>
<details class="faq"><summary>{t("طريقة العناية", "Care")}{icon("chev", extra="chev")}</summary><div class="a">{t("غسيل بماء فاتر حتى 40 درجة على دورة لطيفة. بدون مبيّض. تجفيف بالهواء.", "Wash up to 40°C on a gentle cycle. No bleach. Air dry.")}</div></details>
</div>
</div></section>

<section class="surface"><div class="wrap section" style="display:flex;flex-direction:column;gap:16px;max-width:860px">
<h2 style="font-size:var(--text-h2)">{t("أسئلة عن المنتج", "Product questions")}</h2>{faq_html(FAQ[:4])}</div></section>

<dialog id="size-chart" aria-labelledby="chart-title"><div style="padding:24px;display:flex;flex-direction:column;gap:16px">
<div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><h2 id="chart-title" style="font-size:1.5rem">{t("جدول المقاسات", "Size chart")}</h2>
<button type="button" class="tool" data-close-chart data-aria-ar="إغلاق" data-aria-en="Close">{icon("x")}</button></div>
<div class="table-wrap"><table class="chart"><thead><tr><th>{t("المقاس", "Size")}</th><th>{t("مقاس الحذاء", "Shoe size")}</th><th>{t("طول القدم (سم)", "Foot length (cm)")}</th></tr></thead><tbody>{chart_rows}</tbody></table></div>
<p class="muted small">{t("لو كنت بين مقاسين، اختر الأكبر.", "If you are between sizes, choose the larger one.")}</p>
<button type="button" class="btn btn-primary" data-close-chart>{t("تمام", "Done")}</button></div></dialog>

<div class="sticky-cart"><div style="display:flex;flex-direction:column"><span class="price num" style="font-size:1.25rem" data-pp-price>159 ر.س</span><span class="muted small" data-pp-pairs>6 أزواج</span></div>
<button type="button" class="btn btn-cta" style="flex:1" data-add>{t("أضف إلى السلة", "Add to cart")}</button></div>
</div>'''
product_schema = {"@context": "https://schema.org", "@type": "Product", "name": P["nameAr"], "alternateName": P["nameEn"], "description": P["descAr"],
    "brand": {"@type": "Brand", "name": "Dodoliza"}, "sku": "DDZ-" + P["id"].upper(), "image": [SITE + "/images/comfort-crew-1.jpg"],
    "material": "Bamboo viscose, polyamide, elastane, silver-infused yarn",
    "offers": {"@type": "AggregateOffer", "priceCurrency": "SAR", "lowPrice": PACKS[0]["price"], "highPrice": PACKS[-1]["price"], "offerCount": len(PACKS),
               "availability": "https://schema.org/InStock", "url": SITE + "/product.html"}}
page("product.html", "شراب الراحة اليومية لمرضى السكري | دودليزا", "شراب بطول متوسط لمرضى السكري بحافة لا تضغط ومقدمة بدون خياطة ونعل مبطّن. عبوات 3 و6 و12 زوج، من 89 ر.س.",
     "Everyday Comfort Crew | Dodoliza", product_body, "shop.html",
     [product_schema, {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, _, a, _ in FAQ[:4]]},
      crumbs([("الرئيسية", ""), ("المتجر", "shop.html"), (P["nameAr"], "product.html")])], body_cls="has-sticky")

# ---------------- CART ----------------
cart_body = f'''
<section class="wrap section" style="display:flex;flex-direction:column;gap:24px;max-width:960px">
<h1 style="font-size:var(--text-h1)">{t("السلة", "Your cart")}</h1>
<div data-cart-empty class="card" style="padding:32px;display:flex;flex-direction:column;gap:14px;align-items:flex-start" hidden>
<strong style="font-size:1.25rem">{t("سلتك فاضية", "Your cart is empty")}</strong><p class="muted">{t("اختر الشراب والمقاس وعدد الأزواج، وبيظهر هنا.", "Pick a sock, size and pack, and it will show here.")}</p>
<a class="btn btn-cta" href="shop.html">{t("تسوّق الآن", "Shop now")}</a></div>
<div data-cart-full style="display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));align-items:start">
<ul data-cart-list style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px;min-width:0"></ul>
<div class="card" style="padding:24px;display:flex;flex-direction:column;gap:12px">
<div style="display:flex;justify-content:space-between"><span>{t("المجموع", "Subtotal")}</span><span class="num" data-sub></span></div>
<div style="display:flex;justify-content:space-between"><span>{t("الشحن", "Shipping")}</span><span class="num" data-ship></span></div>
<p class="small" style="color:var(--color-success)" data-free-left></p>
<div style="display:flex;justify-content:space-between;font-weight:700;font-size:1.25rem;border-top:1px solid var(--color-border);padding-top:12px"><span>{t("الإجمالي", "Total")}</span><span class="num" data-total></span></div>
<a class="btn btn-cta btn-block" href="checkout.html">{t("إتمام الطلب", "Checkout")}</a>
<p class="small muted" style="text-align:center">{t("بدون تسجيل حساب، والدفع عند الاستلام متاح", "No account needed, cash on delivery available")}</p></div></div>
</section>'''
page("cart.html", "السلة | دودليزا", "سلة مشترياتك في دودليزا.", "Cart | Dodoliza", cart_body, noindex=True)

# ---------------- CHECKOUT ----------------
def field(id_, ar, en, typ="text", ph_ar="", ph_en="", req=True, err_ar="", err_en="", auto=""):
    return f'''<div class="field"><label for="{id_}">{t(ar, en)}</label><input class="input" id="{id_}" name="{id_}" type="{typ}" {"required" if req else ""} autocomplete="{auto}" data-ph-ar="{ph_ar}" data-ph-en="{ph_en}" placeholder="{ph_ar}">
<span class="err" data-err-for="{id_}" hidden>{t(err_ar, err_en)}</span></div>'''
regions = ["الرياض", "مكة المكرمة", "المنطقة الشرقية", "المدينة المنورة", "القصيم", "عسير", "تبوك", "حائل", "الحدود الشمالية", "جازان", "نجران", "الباحة", "الجوف"]
checkout_body = f'''
<section class="wrap section" style="display:flex;flex-direction:column;gap:24px;max-width:960px">
<div class="steps" aria-label="Checkout steps"><span class="step"><b>1</b>{t("السلة", "Cart")}</span><span class="step" aria-current="step"><b>2</b>{t("بيانات التوصيل والدفع", "Delivery and payment")}</span><span class="step"><b>3</b>{t("تأكيد", "Confirmation")}</span></div>
<h1 style="font-size:var(--text-h1)">{t("إتمام الطلب", "Checkout")}</h1>
<div style="display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));align-items:start">
<form data-checkout novalidate class="card" style="padding:24px;display:flex;flex-direction:column;gap:16px;min-width:0">
<p class="muted">{t("بدون تسجيل حساب. نحتاج بس بيانات التوصيل.", "No account needed. We just need delivery details.")}</p>
{field("name", "الاسم الكامل", "Full name", ph_ar="مثال: محمد العتيبي", ph_en="e.g. Mohammed Alotaibi", err_ar="اكتب الاسم الكامل.", err_en="Enter your full name.", auto="name")}
{field("phone", "رقم الجوال", "Mobile number", "tel", "05XXXXXXXX", "05XXXXXXXX", err_ar="اكتب رقم جوال سعودي من 10 أرقام يبدأ بـ 05.", err_en="Enter a 10-digit Saudi number starting with 05.", auto="tel")}
<div class="field"><label for="region">{t("المنطقة", "Region")}</label><select class="input" id="region" name="region" required>{"".join(f"<option>{r}</option>" for r in regions)}</select></div>
{field("city", "المدينة والحي", "City and district", ph_ar="مثال: الرياض، حي النرجس", ph_en="e.g. Riyadh, Al Narjis", err_ar="اكتب المدينة والحي.", err_en="Enter your city and district.", auto="address-level2")}
{field("address", "العنوان الوطني أو وصف العنوان", "National address or directions", req=False, ph_ar="اختياري", ph_en="Optional", auto="street-address")}
<fieldset style="border:0;padding:0;margin:0;display:flex;flex-direction:column;gap:10px"><legend style="font-weight:600;margin-bottom:8px">{t("طريقة الدفع", "Payment method")}</legend>
<label class="pack-opt" style="cursor:pointer"><span style="display:flex;gap:12px;align-items:center"><input type="radio" name="pay" id="pay-cod" value="cod" checked style="width:22px;height:22px">{t("الدفع عند الاستلام", "Cash on delivery")}</span>{icon("cash")}</label>
<label class="pack-opt" style="cursor:pointer"><span style="display:flex;gap:12px;align-items:center"><input type="radio" name="pay" id="pay-card" value="card" style="width:22px;height:22px">{t("مدى / فيزا / Apple Pay", "mada / Visa / Apple Pay")}</span>{icon("lock")}</label></fieldset>
<button type="submit" class="btn btn-cta btn-block" style="min-height:60px;font-size:1.25rem">{t("تأكيد الطلب", "Place order")}</button>
</form>
<div style="display:flex;flex-direction:column;gap:16px">
<div class="card" style="padding:24px;display:flex;flex-direction:column;gap:12px"><strong>{t("ملخص الطلب", "Order summary")}</strong>
<div style="display:flex;justify-content:space-between"><span>{t("المجموع", "Subtotal")}</span><span class="num" data-sub></span></div>
<div style="display:flex;justify-content:space-between"><span>{t("الشحن", "Shipping")}</span><span class="num" data-ship></span></div>
<div style="display:flex;justify-content:space-between;font-weight:700;font-size:1.25rem;border-top:1px solid var(--color-border);padding-top:12px"><span>{t("الإجمالي", "Total")}</span><span class="num" data-total></span></div>
<a href="cart.html" class="small">{t("تعديل السلة", "Edit cart")}</a></div>
<div data-done hidden tabindex="-1" class="card" style="padding:24px;display:flex;flex-direction:column;gap:10px;border:2px solid var(--color-success)" role="status">
<strong style="font-size:1.25rem;display:flex;gap:8px;align-items:center;color:var(--color-success)">{icon("check")}{t("تم استلام طلبك", "Order placed")}</strong>
<p>{t("بنتواصل معك على الجوال لتأكيد الطلب خلال ساعات.", "We will call your mobile to confirm the order within a few hours.")}</p>
<a class="btn btn-ghost" href="shop.html">{t("رجوع للمتجر", "Back to shop")}</a></div>
</div></div></section>'''
page("checkout.html", "إتمام الطلب | دودليزا", "إتمام الطلب في دودليزا بدون تسجيل حساب، مع الدفع عند الاستلام.", "Checkout | Dodoliza", checkout_body, noindex=True)

# ---------------- ABOUT ----------------
about_body = f'''
<section class="surface"><div class="wrap section" style="display:grid;gap:40px;align-items:center;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
<div style="display:flex;flex-direction:column;gap:18px;min-width:0"><span class="eyebrow-rule"></span>
<h1 style="font-size:var(--text-h1)">{t("بدأنا بسؤال بسيط", "We started with a simple question")}</h1>
<p style="font-size:1.25rem;max-width:44ch">{t("ليش الشراب اللي يلبسه مريض السكري يكون نفس الشراب العادي؟ القدم تحتاج عناية أكثر، والراحة اليومية تفرق.", "Why should someone with diabetes wear the same socks as everyone else? Their feet need more care, and everyday comfort matters.")}</p>
<p class="muted" style="max-width:60ch">{t("عشان كذا صمّمنا شراب واحد بتفاصيل مدروسة: حافة واسعة، مقدمة بدون خياطة، بامبو مع فضة، ونعل مبطّن. ما نبيع غيره، ونركّز إنه يكون أريح شراب تلبسه. (نص مؤقت للتعديل)", "So we made one sock with considered details: a wide top, seamless toe, bamboo with silver, and a cushioned sole. It is all we sell, and we focus on making it the most comfortable pair you own. (Placeholder copy)")}</p></div>
<div class="rib-frame card" style="aspect-ratio:4/3">{ph("grey", "صورة: كبار سن يمشون براحة (مؤقتة)", "Photo: older adults walking comfortably (placeholder)", "fill")}</div>
</div></section>
<section class="wrap section" style="display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
<div class="card" style="padding:24px;display:flex;flex-direction:column;gap:8px">{icon("heart")}<h2 style="font-size:1.375rem">{t("نهتم بالتفاصيل", "We care about details")}</h2><p class="muted">{t("كل خياطة وكل خيط مختار عشان الراحة.", "Every seam and every thread is chosen for comfort.")}</p></div>
<div class="card" style="padding:24px;display:flex;flex-direction:column;gap:8px">{icon("leaf")}<h2 style="font-size:1.375rem">{t("خامات طبيعية", "Natural fibers")}</h2><p class="muted">{t("ألياف بامبو ناعمة تتنفس.", "Soft, breathable bamboo fibers.")}</p></div>
<div class="card" style="padding:24px;display:flex;flex-direction:column;gap:8px">{icon("truck")}<h2 style="font-size:1.375rem">{t("قريبين منك", "Close to you")}</h2><p class="muted">{t("توصيل لكل المملكة ودفع عند الاستلام.", "Delivery across Saudi Arabia, with cash on delivery.")}</p></div>
</section>'''
page("about.html", "قصتنا | دودليزا", "قصة دودليزا: شراب واحد مصمّم بعناية لراحة مرضى السكري في السعودية، بحافة لا تضغط ومقدمة بدون خياطة وألياف بامبو مع فضة.", "Our story | Dodoliza", about_body, "about.html",
     [{"@context": "https://schema.org", "@type": "AboutPage", "name": "قصتنا", "url": SITE + "/about.html", "about": ORG}, crumbs([("الرئيسية", ""), ("قصتنا", "about.html")])])

# ---------------- CONTACT ----------------
contact_body = f'''
<section class="wrap section" style="display:grid;gap:32px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));align-items:start">
<div style="display:flex;flex-direction:column;gap:18px;min-width:0"><h1 style="font-size:var(--text-h1)">{t("تواصل معنا", "Contact us")}</h1>
<p class="muted" style="max-width:48ch">{t("عندك سؤال عن المقاس أو الطلب؟ أسرع طريقة هي واتساب، ونرد خلال ساعات العمل.", "Questions about sizing or your order? WhatsApp is the fastest way; we reply during working hours.")}</p>
<a class="btn btn-primary" href="https://wa.me/{WA}" target="_blank" rel="noopener" style="align-self:flex-start">{icon("wa")}{t("راسلنا على واتساب", "Message us on WhatsApp")}</a>
<div class="card" style="padding:20px;display:flex;flex-direction:column;gap:12px">
<div style="display:flex;gap:10px;align-items:center">{icon("phone")}<span class="num" style="user-select:all" dir="ltr">+{WA}</span></div>
<div style="display:flex;gap:10px;align-items:center">{icon("mail")}<span class="lat" style="user-select:all">care@dodoliza.com</span></div>
<p class="muted small">{t("الأحد إلى الخميس، 9 صباحًا إلى 9 مساءً (مؤقت)", "Sunday to Thursday, 9am to 9pm (placeholder)")}</p></div></div>
<form class="card" style="padding:24px;display:flex;flex-direction:column;gap:16px" onsubmit="event.preventDefault();this.hidden=true;document.getElementById('sent').hidden=false;document.getElementById('sent').focus()">
<div class="field"><label for="c-name">{t("الاسم", "Name")}</label><input class="input" id="c-name" required autocomplete="name"></div>
<div class="field"><label for="c-phone">{t("رقم الجوال", "Mobile number")}</label><input class="input" id="c-phone" type="tel" required autocomplete="tel" placeholder="05XXXXXXXX"></div>
<div class="field"><label for="c-msg">{t("رسالتك", "Your message")}</label><textarea class="input" id="c-msg" required></textarea></div>
<button type="submit" class="btn btn-primary">{t("أرسل الرسالة", "Send message")}</button></form>
<div id="sent" hidden tabindex="-1" class="card" role="status" style="padding:24px;border:2px solid var(--color-success)"><strong style="color:var(--color-success)">{t("وصلتنا رسالتك، بنرد عليك قريب.", "Message received. We will reply soon.")}</strong></div>
</section>'''
page("contact.html", "تواصل معنا | دودليزا", "تواصل مع دودليزا على واتساب أو البريد لأي سؤال عن المقاسات أو الطلبات أو الشحن والدفع عند الاستلام داخل السعودية.", "Contact | Dodoliza", contact_body, "contact.html",
     [{"@context": "https://schema.org", "@type": "ContactPage", "name": "تواصل معنا", "url": SITE + "/contact.html", "about": ORG}, crumbs([("الرئيسية", ""), ("تواصل معنا", "contact.html")])])
print("built")
