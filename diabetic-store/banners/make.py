import sys; sys.path.insert(0,'..')
SOCK=open('../build.py').read()
exec(SOCK.split("NAV = [")[0].split("def t(ar, en):")[0])  # constants only
def sock(color="#FFFFFF", stroke="#123B3A"):
    return (f'<svg viewBox="0 0 200 240" style="width:100%;height:100%" aria-hidden="true"><path d="M70 20h70v110c0 10 6 18 16 24l20 12c14 9 18 26 9 40-8 13-24 17-38 10L74 186c-20-11-30-30-30-52V20z" fill="{color}" stroke="{stroke}" stroke-width="3" stroke-linejoin="round"/><path d="M70 20h70v26H70z" fill="{color}" stroke="{stroke}" stroke-width="3"/>'
      + "".join(f'<path d="M{78+i*8} 24v18" stroke="{stroke}" stroke-opacity=".35" stroke-width="2"/>' for i in range(8)) + '</svg>')
def banner(name,w,h,layout):
    s=min(w,h)/1080
    feats=["حافة ما تضغط","مقدمة بدون خياطة","بامبو مع فضة","نعل مبطّن"]
    chips="".join(f'<span style="background:#fff;border-radius:{14*s}px;padding:{8*s}px {18*s}px;font-weight:700;font-size:{30*s}px">{f}</span>' for f in feats)
    text=f'''<div style="display:flex;flex-direction:column;gap:{22*s}px;align-items:flex-start">
<div style="display:flex;align-items:center;gap:{10*s}px;font-weight:800;font-size:{40*s}px">دودليزا</div>
<div style="font-weight:800;font-size:{86*s}px;line-height:1.25">راحة تلبسها<br>من الصبح لآخر اليوم</div>
<div style="font-weight:600;font-size:{36*s}px;color:#4B5F5D">شراب مصمّم لمرضى السكري</div>
<div style="display:flex;flex-wrap:wrap;gap:{10*s}px;max-width:{720*s}px">{chips}</div>
<div style="display:flex;align-items:center;gap:{20*s}px;margin-top:{10*s}px">
<span style="background:#F2B544;color:#123B3A;border-radius:{14*s}px;padding:{18*s}px {40*s}px;font-weight:800;font-size:{40*s}px">تسوّق الآن</span>
<span style="font-weight:700;font-size:{32*s}px">يبدأ من 89 ر.س</span></div>
<div style="font-weight:600;font-size:{26*s}px;color:#4B5F5D">الدفع عند الاستلام، وشحن مجاني فوق 150 ر.س</div></div>'''
    art=f'''<div style="position:relative;background:#fff;border-radius:{40*s}px;overflow:hidden;flex:none;display:flex;align-items:center;justify-content:center;width:{layout['aw']}px;height:{layout['ah']}px">
<div style="position:absolute;inset:0 0 auto 0;height:{60*s}px;background:repeating-linear-gradient(90deg,rgba(18,59,58,.16) 0 {5*s}px,transparent {5*s}px {15*s}px),#DCE8E4"></div>
<div style="width:62%;height:78%;margin-top:{40*s}px">{sock("#FFFFFF")}</div></div>'''
    body=f'''<div dir="rtl" style="width:{w}px;height:{h}px;box-sizing:border-box;padding:{layout['pad']}px;background:#DCE8E4;color:#123B3A;font-family:Cairo;display:flex;flex-direction:{layout['dir']};gap:{48*s}px;align-items:center;justify-content:space-between">{text}{art}</div>'''
    return body
SIZES={"hero-1440x640":(1440,640,dict(dir="row",pad=72,aw=520,ah=500)),"instagram-post-1080x1080":(1080,1080,dict(dir="row",pad=64,aw=380,ah=800)),
 "instagram-story-1080x1920":(1080,1920,dict(dir="column",pad=96,aw=888,ah=820)),"facebook-ad-1200x628":(1200,628,dict(dir="row",pad=56,aw=430,ah=516))}
import json
json.dump({k:[v[0],v[1],banner(k,*v)] for k,v in SIZES.items()},open('banners.json','w'),ensure_ascii=False)
