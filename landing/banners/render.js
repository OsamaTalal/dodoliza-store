const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch();
  const list = fs.readFileSync(path.join(__dirname, 'list.txt'), 'utf8').trim().split('\n');
  for (const line of list) {
    const [n, w, h] = line.split(' ');
    const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.join(__dirname, n + '.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    await (await p.$('#b')).screenshot({ path: path.join(__dirname, n + '.png') });
    await p.close();
  }
  await b.close();
})();
