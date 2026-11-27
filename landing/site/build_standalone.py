import re,base64,sys
src="/home/claude/dodoliza-store/landing/site/"
s=open(src+"luxury.html",encoding="utf8").read()
head='<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="theme-color" content="#285429">\n'
body_open=s  # title/meta/link/style stay in head; rest follows
# close head before first body element (<div class="ann")
i=s.index('<div class="ann"')
out=head+s[:i]+'</head>\n<body>\n'+s[i:]+'\n</body>\n</html>\n'
if len(sys.argv)>1 and sys.argv[1]=="inline":
    out=re.sub(r'(?<=["\(])(img/[a-z0-9-]+\.webp)',lambda m:"data:image/webp;base64,"+base64.b64encode(open(src+m.group(1),"rb").read()).decode(),out)
    open("/tmp/ghp/index.html","w",encoding="utf8").write(out)
else:
    open(src+"standalone.html","w",encoding="utf8").write(out)
