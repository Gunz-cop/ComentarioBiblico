// Arnés de verificación del prototipo UX-001 (no forma parte del prototipo; la página no usa JS).
// Uso: npm ci && npm run verificar   (ver README de esta carpeta)
// Navegador: el que instala Playwright (`npx playwright install chromium`) o PW_CHROMIUM_PATH si se define.
// — Claude Code
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '..');
const out = path.join(root, 'capturas');
fs.mkdirSync(out, { recursive: true });

// Servidor estático mínimo
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.otf': 'font/otf', '.ttf': 'font/ttf' };
const srv = http.createServer((req, res) => {
  const f = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(0);
const url = `http://127.0.0.1:${srv.address().port}/genesis-1.html`;

const launch = process.env.PW_CHROMIUM_PATH ? { executablePath: process.env.PW_CHROMIUM_PATH } : {};
const browser = await chromium.launch(launch);
const runId = new Date().toISOString();
const meta = {
  ejecucion: runId,
  playwright: require('playwright/package.json').version,
  axeCore: require('axe-core/package.json').version,
  navegador: `${browser.browserType().name()} ${browser.version()}`,
  ejecutable: process.env.PW_CHROMIUM_PATH || 'navegador gestionado por Playwright',
  node: process.version,
};
const capturas = [];
const shot = async (page, name, opts = {}) => {
  const file = `${name}.png`;
  await page.screenshot({ path: path.join(out, file), fullPage: true, ...opts });
  capturas.push(file);
};
// Abre los <details> con clics reales: funciona con JS de página desactivado (comportamiento nativo)
const abrirTodos = async page => {
  // los <details> anidados (análisis por palabra) solo son visibles al abrir su contenedor
  const pendiente = page.locator('details:not([open]) > summary:visible');
  for (let i = 0; i < 100 && await pendiente.count(); i++) await pendiente.first().click();
};
const listo = async page => { await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(200); };

const VISTAS = [['movil-320', 320, 720], ['movil-360', 360, 780], ['escritorio-1280', 1280, 900]];
const ESQUEMAS = ['light', 'dark'];

// 1. Capturas: JS de la página DESACTIVADO (demuestra que no depende de JS).
for (const scheme of ESQUEMAS) for (const [name, width, height] of VISTAS) {
  const ctx = await browser.newContext({ viewport: { width, height }, colorScheme: scheme, javaScriptEnabled: false, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(url); await page.waitForTimeout(400);
  await shot(page, `${name}-${scheme}-plegado`);
  await abrirTodos(page); await page.waitForTimeout(200);
  await shot(page, `${name}-${scheme}-desplegado`);
  await ctx.close();
}

// 2. Reflow: medición con JS habilitado SOLO en el arnés; mismos tamaños, esquemas y estados.
const reflow = [];
for (const scheme of ESQUEMAS) for (const [name, width, height] of VISTAS) for (const estado of ['plegado', 'desplegado']) {
  const ctx = await browser.newContext({ viewport: { width, height }, colorScheme: scheme });
  const page = await ctx.newPage();
  await page.goto(url); await listo(page);
  if (estado === 'desplegado') { await abrirTodos(page); await listo(page); }
  const m = await page.evaluate(() => {
    const de = document.documentElement;
    const desbordan = [...document.querySelectorAll('body *')]
      .filter(e => e.getBoundingClientRect().right > de.clientWidth + 0.5 && !e.closest('.tabla-scroll, .oculto, .saltar'))
      .slice(0, 5).map(e => e.tagName.toLowerCase() + (e.className ? '.' + e.className : ''));
    return { desbordeHorizontalPx: de.scrollWidth - de.clientWidth, elementosQueDesbordan: desbordan };
  });
  reflow.push({ vista: name, esquema: scheme, estado, ...m });
  await ctx.close();
}

// 3. axe y objetivos táctiles, por esquema y estado
const auditoria = [];
for (const scheme of ESQUEMAS) for (const estado of ['plegado', 'desplegado']) {
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 }, colorScheme: scheme });
  const page = await ctx.newPage();
  await page.goto(url); await listo(page);
  if (estado === 'desplegado') { await abrirTodos(page); await listo(page); }
  const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze();
  const pequenos = await page.$$eval('a, summary', els => els.filter(e => e.offsetParent)
    .map(e => { const r = e.getBoundingClientRect(); return { t: e.textContent.trim().slice(0, 30), w: Math.round(r.width), h: Math.round(r.height) }; })
    .filter(r => r.w < 24 || r.h < 24));
  const fuentes = await page.evaluate(() => [...document.fonts].map(f => `${f.family} ${f.style} ${f.weight}: ${f.status}`));
  auditoria.push({ esquema: scheme, estado, axeViolaciones: axe.violations.map(v => `${v.id} (${v.impact}): ${v.nodes.length}`), axeIncompletas: axe.incomplete.map(v => v.id), axeAprobadas: axe.passes.length, objetivosMenoresDe24px: pequenos, fuentes });
  await ctx.close();
}

// 4. Teclado (JS de página desactivado): orden de foco, apertura/cierre con Enter, foco visible
const teclado = {};
{
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 }, javaScriptEnabled: false, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto(url);
  const activo = () => page.evaluate(() => { const a = document.activeElement; return `${a.tagName.toLowerCase()}: ${(a.getAttribute('aria-label') || a.textContent).trim().replace(/\s+/g, ' ').slice(0, 40)}`; });
  teclado.ordenFoco = [];
  for (let i = 0; i < 16; i++) { await page.keyboard.press('Tab'); teclado.ordenFoco.push(await activo()); }
  await page.goto(url);
  let n = 0;
  while (!(await activo()).startsWith('summary: Hebreo') && n++ < 30) await page.keyboard.press('Tab');
  const det = page.locator('details.estudio').first();
  await page.keyboard.press('Enter');
  teclado.abiertoTrasEnter = (await det.getAttribute('open')) !== null;
  await page.screenshot({ path: path.join(out, 'teclado-foco-360.png') }); capturas.push('teclado-foco-360.png');
  teclado.focoTrasAbrir = await activo();
  await page.keyboard.press('Enter');
  teclado.cerradoTrasSegundoEnter = (await det.getAttribute('open')) === null;
  teclado.focoVisible = await page.evaluate(() => getComputedStyle(document.activeElement).outlineStyle !== 'none');
  await ctx.close();
}

// 5. Árbol de accesibilidad del interlineal (Chromium; NO sustituye a VoiceOver/TalkBack)
let arbol;
{
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 } });
  const page = await ctx.newPage();
  await page.goto(url); await abrirTodos(page);
  arbol = (await page.locator('ol.interlineal').ariaSnapshot()).split('\n').slice(0, 30).join('\n');
  await ctx.close();
}

// 6. Peso transferido en primera visita (sin caché)
let peso;
{
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 } });
  const page = await ctx.newPage();
  const recursos = [];
  page.on('response', async r => { try { recursos.push({ url: r.url().replace(/^.*\//, ''), bytes: (await r.body()).length }); } catch {} });
  await page.goto(url); await listo(page); await page.waitForLoadState('networkidle');
  const total = recursos.reduce((s, r) => s + r.bytes, 0);
  peso = { recursos, totalBytes: total, sinFuentesBytes: recursos.filter(r => !/\.(otf|ttf|woff2?)$/.test(r.url)).reduce((s, r) => s + r.bytes, 0) };
  await ctx.close();
}

await browser.close(); srv.close();
const informe = { meta, capturas, reflow, auditoria, teclado, arbolAccesibleInterlineal: arbol, pesoPrimeraVisita: peso };
fs.writeFileSync(path.join(out, 'informe.json'), JSON.stringify(informe, null, 2));
const maxDesborde = Math.max(...reflow.map(r => r.desbordeHorizontalPx));
const violaciones = auditoria.reduce((s, a) => s + a.axeViolaciones.length, 0);
console.log(JSON.stringify({ meta, maxDesborde, violaciones, teclado, peso: { total: peso.totalBytes, sinFuentes: peso.sinFuentesBytes } }, null, 2));
process.exitCode = maxDesborde > 0 || violaciones > 0 ? 1 : 0;
