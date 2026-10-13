import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const root = process.argv[2];
const out = path.join(root, 'capturas');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.otf': 'font/otf', '.ttf': 'font/ttf' };
const srv = http.createServer((req, res) => {
  const f = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(root) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(0);
const url = `http://127.0.0.1:${srv.address().port}/genesis-1.html`;

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const report = [];
const views = [
  ['movil-320', 320, 720], ['movil-360', 360, 780], ['escritorio-1280', 1280, 900],
];
for (const scheme of ['light', 'dark']) {
  for (const [name, w, h] of views) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, colorScheme: scheme, javaScriptEnabled: false, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    await page.goto(url);
    await page.evaluate(() => document.fonts.ready).catch(() => {});
    await page.waitForTimeout(300);
    // abrir todos los details (sin JS en la página: lo hace el arnés de prueba)
    await page.$$eval('details', ds => ds.forEach(d => d.open = true)).catch(async () => {
      // javaScriptEnabled:false también bloquea evaluate; usar clics de teclado/ratón
    });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth).catch(() => 'n/d');
    await page.screenshot({ path: `${out}/${name}-${scheme}.png`, fullPage: true });
    report.push({ vista: name, esquema: scheme, desbordeHorizontalPx: overflow });
    await ctx.close();
  }
}

{ const ctx = await browser.newContext({ viewport: { width: 360, height: 780 }, javaScriptEnabled: false, deviceScaleFactor: 2 });
  const page = await ctx.newPage(); await page.goto(url); await page.waitForTimeout(500);
  await page.screenshot({ path: `${out}/movil-360-plegado-sin-js.png`, fullPage: true });
  report.push({ vista: 'movil-360-plegado-sin-js', bytesHTMLyCSS: fs.statSync(path.join(root,'genesis-1.html')).size + fs.statSync(path.join(root,'estilos.css')).size });
  await ctx.close(); }
// Con JS en el arnés (la página no usa JS): fuentes, axe, objetivos, teclado
for (const scheme of ['light', 'dark']) {
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 }, colorScheme: scheme });
  const page = await ctx.newPage();
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);
  await page.$$eval('details', ds => ds.forEach(d => d.open = true));
  const fonts = await page.evaluate(() => [...document.fonts].map(f => `${f.family} ${f.style} ${f.weight}: ${f.status}`));
  const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
  const targets = await page.$$eval('a, summary', els => els.filter(e => e.offsetParent).map(e => { const r = e.getBoundingClientRect(); return { t: e.textContent.trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) }; }).filter(r => r.w < 24 || r.h < 24));
  report.push({ esquema: scheme, fuentes: fonts, axeViolaciones: axe.violations.map(v => `${v.id} (${v.impact}): ${v.nodes.length} nodos`), axeAprobadas: axe.passes.length, objetivosMenoresDe24px: targets });
  await ctx.close();
}

// Reflow a 400 %: 1280 px / 4 = 320 px CSS (ya cubierto). Teclado: orden de foco.
{
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 }, javaScriptEnabled: false });
  const page = await ctx.newPage();
  await page.goto(url);
  const orden = [];
  for (let i = 0; i < 16; i++) {
    await page.keyboard.press('Tab');
    orden.push(await page.evaluate(() => { const a = document.activeElement; return `${a.tagName.toLowerCase()}: ${(a.getAttribute('aria-label') || a.textContent).trim().replace(/\s+/g, ' ').slice(0, 40)}`; }).catch(() => 'n/d'));
  }
  // abrir el interlineal con teclado y capturar foco visible
  await page.goto(url);
  for (let i = 0; i < 8; i++) await page.keyboard.press('Tab');
  await page.keyboard.press('Enter');
  await page.screenshot({ path: `${out}/teclado-foco-360.png` });
  const abierto = await page.locator('details.estudio').first().getAttribute('open');
  report.push({ tecladoOrdenFoco: orden, detailsAbiertoConEnter: abierto !== null });
  await ctx.close();
}
// Árbol de accesibilidad del interlineal (orden lógico)
{
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 } });
  const page = await ctx.newPage();
  await page.goto(url);
  await page.$$eval('details', ds => ds.forEach(d => d.open = true));
  const snap = await page.locator('ol.interlineal').ariaSnapshot();
  report.push({ arbolAccesibleInterlineal: snap.split('\n').slice(0, 40).join('\n') });
  await ctx.close();
}
await browser.close(); srv.close();
fs.writeFileSync(path.join(out, 'informe.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
