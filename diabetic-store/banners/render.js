const {chromium}=require('playwright');const fs=require('fs');
const F='/tmp/claude-0/-home-claude/762db5c8-75e2-5aae-8929-9ddca62e3623/scratchpad/node_modules/@fontsource/cairo/files/';
const ff=[400,600,700,800].map(w=>`@font-face{font-family:Cairo;font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(F+`cairo-arabic-${w}-normal.woff2`).toString('base64')})}@font-face{font-family:Cairo;font-weight:${w};unicode-range:U+0000-00FF;src:url(data:font/woff2;base64,${fs.readFileSync(F+`cairo-latin-${w}-normal.woff2`).toString('base64')})}`).join('');
const B=JSON.parse(fs.readFileSync('banners.json'));
(async()=>{const b=await chromium.launch();
for(const [k,[w,h,html]] of Object.entries(B)){const p=await b.newPage({viewport:{width:w,height:h}});
await p.setContent(`<style>${ff}body{margin:0}</style>${html}`);await p.evaluate(()=>document.fonts.ready);
const over=await p.evaluate(()=>{const r=document.body.firstElementChild;return r.scrollHeight>r.clientHeight+1||r.scrollWidth>r.clientWidth+1});
await p.screenshot({path:k+'.png'});console.log(k,over?'OVERFLOW':'ok');}
await b.close();})();
