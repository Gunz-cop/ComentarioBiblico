"""Genera las páginas del prototipo UX-001 a partir de los datos importados (OSHB) y del borrador editorial.

Uso (desde prototipos/ux-001/datos): python3 -I generar.py
Produce ../genesis-1.html (interlineal compacto) y ../genesis-1-tarjetas.html (tarjetas, para comparar).
Capas: importado (texto, lema, morfología OSHB) · derivado (hebreo sin teamim, análisis legible)
· editorial en borrador (transliteración, glosa). — Claude Code
"""
import html
import json
import re
from pathlib import Path

AQUI = Path(__file__).parent
oshb = json.loads((AQUI / "oshb-gn-1.json").read_text(encoding="utf-8"))
edit = json.loads((AQUI / "editorial-borrador.json").read_text(encoding="utf-8"))

TEAMIM = re.compile("[֑-֯]")  # PEND-04: se ocultan en la vista; el dato importado los conserva

# ---------- Derivación determinística de la morfología OSHB a texto ----------
TRONCOS = {"q": "Qal", "N": "Nifal", "p": "Piel", "P": "Pual", "h": "Hifil", "H": "Hofal", "t": "Hitpael"}
TIPOS = {"p": "perfecto", "q": "perfecto consecutivo", "i": "imperfecto", "w": "imperfecto consecutivo (wayyiqtol)",
         "h": "cohortativo", "j": "yusivo", "v": "imperativo", "r": "participio activo", "s": "participio pasivo",
         "a": "infinitivo absoluto", "c": "infinitivo constructo"}
GENERO = {"m": "masculino", "f": "femenino", "c": "común", "b": "masculino o femenino"}
NUMERO = {"s": "singular", "p": "plural", "d": "dual"}
ESTADO = {"a": "absoluto", "c": "constructo", "d": "determinado"}
PERSONA = {"1": "1.ª", "2": "2.ª", "3": "3.ª"}


def gnum(c):
    return " ".join(x for x in [GENERO.get(c[0:1], ""), NUMERO.get(c[1:2], "")] if x)


def parte(p):
    k, r = p[0], p[1:]
    if k == "C":
        return "conjunción"
    if k == "R":
        return "preposición"
    if k == "D":
        return "adverbio"
    if k == "T":
        return {"d": "artículo", "o": "marca de objeto directo", "r": "partícula relativa"}.get(r, f"partícula ({r})")
    if k == "N":
        s = "sustantivo propio" if r[:1] == "p" else "sustantivo"
        return f"{s} {gnum(r[1:3])}, {ESTADO.get(r[3:4], '')}".rstrip(", ")
    if k == "S":
        return f"sufijo pronominal {PERSONA.get(r[1:2], '')} {gnum(r[2:4])}".strip()
    if k == "V":
        tronco, tipo, resto = TRONCOS.get(r[0], r[0]), r[1], r[2:]
        if tipo in "rs":
            return f"verbo {tronco}, {TIPOS[tipo]}, {gnum(resto[0:2])} {ESTADO.get(resto[2:3], '')}".strip()
        if tipo in "ac":
            return f"verbo {tronco}, {TIPOS[tipo]}"
        return f"verbo {tronco}, {TIPOS.get(tipo, tipo)}, {PERSONA.get(resto[0:1], '')} {gnum(resto[1:3])}".strip()
    return p


def analisis(morf):
    return " + ".join(parte(p) for p in morf[1:].split("/"))


def strong(lema):
    nums = [x.strip() for x in lema.split("/") if re.match(r"\d", x.strip())]
    return ", ".join("H" + n.replace(" ", "") for n in nums) or "—"


def palabras(osis):
    out = []
    for i, w in enumerate(oshb["versos"][osis], 1):
        tr, gl, *fn = edit[osis][w["id"]]
        heb = TEAMIM.sub("", w["texto"])
        segs = heb.split("/")
        visible = "".join(segs) + {"maqaf": "־", "sof_pasuq": "׃"}.get(w.get("sigue"), "")
        out.append(dict(n=i, id=w["id"], heb=visible, segs=segs, tr=tr, gl=gl, fn=fn[0] if fn else "",
                        an=analisis(w["morf"]), morf=w["morf"], lema=w["lema"], strong=strong(w["lema"])))
    return out


e = html.escape
he = lambda t: f'<span lang="he" dir="rtl">{e(t)}</span>'


def glosa_html(p):
    if p["gl"] and p["fn"]:
        return f'{e(p["gl"])} <span class="funcion">({e(p["fn"])})</span>'
    if p["fn"]:
        return f'<span class="funcion">{e(p["fn"])}</span>'
    return e(p["gl"])


def heb_linea(ps):
    s = ""
    for p in ps:
        s += p["heb"] + ("" if p["heb"].endswith("־") else " ")
    return s.strip()


# ---------- Patrón compacto ----------
def compacto(v, ps):
    items = "\n".join(
        f'''      <li id="p-{v}-{p["n"]}"><a class="palabra" href="#a-{v}-{p["n"]}"><span class="oculto">Palabra {p["n"]}: </span><span class="c-heb" lang="he" dir="rtl">{e(p["heb"])}</span> <span class="c-tr" lang="he-Latn" dir="ltr">{e(p["tr"])}</span> <span class="c-gl" dir="ltr">{glosa_html(p)}</span></a></li>'''
        for p in ps)
    filas = "\n".join(
        f'''          <tr id="a-{v}-{p["n"]}"><th scope="row"><a href="#p-{v}-{p["n"]}" aria-label="Volver a la palabra {p["n"]}">{p["n"]}</a></th><td>{" + ".join(he(s) for s in p["segs"])}</td><td>{e(p["an"])}<br><span class="morf-cod"><code>{e(p["morf"])}</code> · {e(p["strong"])}</span></td></tr>'''
        for p in ps)
    return f'''    <ol class="compacto" dir="rtl" aria-label="Interlineal compacto de {v}, {len(ps)} palabras en el orden del texto hebreo">
{items}
    </ol>
    <p class="afirmacion">Toca una palabra para ver su análisis gramatical.</p>
    <details class="analisis" id="analisis-{v}">
      <summary>Análisis gramatical de {v} ({len(ps)} palabras)</summary>
      <div class="tabla-scroll" role="region" aria-label="Tabla de análisis de {v}" tabindex="0">
      <table class="tabla-analisis">
        <thead><tr><th scope="col">N.º</th><th scope="col">Segmentos</th><th scope="col">Análisis <span class="etiqueta derivado">Derivado</span> · morfología y Strong <span class="etiqueta importado">Importado</span></th></tr></thead>
        <tbody>
{filas}
        </tbody>
      </table>
      </div>
    </details>'''


# ---------- Patrón tarjetas (comparación) ----------
def tarjetas(v, ps):
    items = "\n".join(
        f'''      <li class="token"><dl>
        <dt>Palabra</dt><dd class="t-n">{p["n"]}</dd>
        <dt>Hebreo</dt><dd class="t-heb" lang="he" dir="rtl">{e(p["heb"])}</dd>
        <dt>Transliteración</dt><dd class="t-tr" lang="he-Latn">{e(p["tr"])}</dd>
        <dt>Glosa</dt><dd class="t-gl">{glosa_html(p)}</dd>
      </dl>
      <details><summary>Análisis<span class="oculto"> de la palabra {p["n"]}</span></summary>
        <div class="t-morf">{e(p["an"])} <span class="etiqueta derivado">Derivado</span><br>
        Segmentos {" + ".join(he(s) for s in p["segs"])}<br><code>{e(p["morf"])}</code> · {e(p["strong"])} <span class="etiqueta importado">Importado</span></div>
      </details></li>''' for p in ps)
    return f'''    <ol class="interlineal" dir="rtl" aria-label="Interlineal de {v}, {len(ps)} palabras en el orden del texto hebreo">
{items}
    </ol>'''


LEYENDA = '''    <ul class="leyenda" aria-label="Leyenda de procedencia">
      <li><span class="etiqueta importado">Importado</span> borde continuo: hebreo, lema, morfología (OSHB)</li>
      <li><span class="etiqueta derivado">Derivado</span> borde doble: análisis legible y hebreo sin teamim</li>
      <li><span class="etiqueta editorial">Borrador</span> borde discontinuo: transliteración y glosa sin revisar</li>
    </ul>'''


def estudio(v, ps, patron):
    cuerpo = compacto(v, ps) if patron == "compacto" else tarjetas(v, ps)
    return f'''<details class="estudio">
  <summary>Hebreo e interlineal de {v}</summary>
  <div class="estudio-cuerpo">
    <p class="linea-hebrea" lang="he" dir="rtl">{e(heb_linea(ps))}</p>
{LEYENDA}
{cuerpo}
  </div>
</details>'''


def pagina(patron):
    p1, p11 = palabras("Gen.1.1"), palabras("Gen.1.11")
    otro = ("genesis-1-tarjetas.html", "Ver variante en tarjetas") if patron == "compacto" else ("genesis-1.html", "Ver variante compacta")
    titulo = "compacto" if patron == "compacto" else "tarjetas"
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Génesis 1 ({titulo}) — Prototipo UX-001</title>
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Prototipo aislado de la página de capítulo con interlineal ({titulo}) de Gn 1:1 y Gn 1:11. No es contenido aprobado.">
<link rel="stylesheet" href="estilos.css">
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<!-- Generado por datos/generar.py: no editar a mano. -->
<header class="sitio">
  <div class="contenedor">
    <a class="marca" href="#">Comentario Bíblico <span class="oculto">(nombre provisional, PEND-10)</span></a>
    <nav class="migas" aria-label="Migas de pan">
      <ol>
        <li><a href="#">Inicio</a></li>
        <li><a href="#">Antiguo Testamento</a></li>
        <li><a href="#">Génesis</a></li>
        <li><a href="#contenido" aria-current="page">Capítulo 1</a></li>
      </ol>
    </nav>
  </div>
</header>

<main id="contenido" class="contenedor">
  <article>
    <header class="capitulo-cab">
      <p class="antetitulo">Génesis · Antiguo Testamento</p>
      <h1>Génesis <span class="num">1</span></h1>
      <div class="aviso" role="note">
        <p><strong>Prototipo UX-001 — variante «{titulo}».</strong> <a href="{otro[0]}">{otro[1]}</a>.</p>
        <p>Texto RV1909 provisional (RL-003, PEND-05). Hebreo, lemas y morfología: OSHB, candidata en PEND-01 (WLC de dominio público; morfología CC BY 4.0, Open Scriptures Hebrew Bible Project). <strong>Transliteración y glosas: borrador editorial sin revisar</strong> (PEND-02, DEC-007). Sin teamim (PEND-04). Se muestran solo los vv. 1–5 y 11; no es el capítulo íntegro.</p>
      </div>
    </header>

    <section class="texto" aria-labelledby="per-1">
      <h2 id="per-1" class="pericopa">La creación <span class="oculto">— perícopa provisional</span>(1:1–2:3)</h2>

      <p><span class="versiculo" id="v1" data-osis="Gen.1.1"><a class="vnum" href="#v1" aria-label="Versículo 1">1</a>En el principio crió Dios los cielos y la tierra.</span></p>

{estudio("1:1", p1, patron)}

      <details class="estudio">
        <summary>Comentario de 1:1 <span class="etiqueta editorial">Borrador ilustrativo</span></summary>
        <div class="estudio-cuerpo">
          <p>El versículo abre el relato de la creación con una afirmación general: Dios es el sujeto de la acción y «los cielos y la tierra» abarca la totalidad de lo creado. <span class="afirmacion">[Literaria; ref. Gn 1:1, 2:1]</span></p>
          <h3>Notas lingüísticas</h3>
          <ul>
            <li>En la forma Qal, el verbo <i lang="he-Latn">bārāʾ</i> («crear») tiene en la Biblia hebrea siempre a Dios como sujeto. <span class="afirmacion">[Lingüística; fuente: léxico BDB, s.v. <span lang="he" dir="rtl">ברא</span>]</span></li>
            <li><i lang="he-Latn">ʾĕlōhîm</i> (<span lang="he" dir="rtl">אֱלֹהִים</span>) tiene forma plural, pero aquí va con un verbo en singular (<i lang="he-Latn">bārāʾ</i>). <span class="afirmacion">[Lingüística; fuente: Gesenius §124g]</span></li>
          </ul>
          <p class="afirmacion">Reproduce el borrador del anexo A de <code>docs/requisitos.md</code>; no aprobado.</p>
        </div>
      </details>

      <p>
        <span class="versiculo" id="v2" data-osis="Gen.1.2"><a class="vnum" href="#v2" aria-label="Versículo 2">2</a>Y la tierra estaba desordenada y vacía, y las tinieblas estaban sobre la haz del abismo, y el Espíritu de Dios se movía sobre la haz de las aguas.</span>
        <span class="versiculo" id="v3" data-osis="Gen.1.3"><a class="vnum" href="#v3" aria-label="Versículo 3">3</a>Y dijo Dios: Sea la luz: y fué la luz.</span>
        <span class="versiculo" id="v4" data-osis="Gen.1.4"><a class="vnum" href="#v4" aria-label="Versículo 4">4</a>Y vió Dios que la luz era buena: y apartó Dios la luz de las tinieblas.</span>
        <span class="versiculo" id="v5" data-osis="Gen.1.5"><a class="vnum" href="#v5" aria-label="Versículo 5">5</a>Y llamó Dios á la luz Día, y á las tinieblas llamó Noche: y fué la tarde y la mañana un día.</span>
      </p>
      <p class="afirmacion">[Versículos 6–10 omitidos en el prototipo.]</p>

      <p><span class="versiculo" id="v11" data-osis="Gen.1.11"><a class="vnum" href="#v11" aria-label="Versículo 11">11</a>Después dijo Dios: Produzca la tierra hierba verde, hierba que dé simiente; árbol de fruto que dé fruto según su género, que su simiente esté en él, sobre la tierra: y fué así.</span></p>

{estudio("1:11", p11, patron)}

      <p class="afirmacion">[Versículos 12–31 omitidos en el prototipo.]</p>
    </section>

    <section aria-labelledby="pruebas-tit">
      <h2 id="pruebas-tit">Banco de pruebas tipográficas (RNF-005)</h2>
      <p>Casos representativos de marcas para comprobar el renderizado de Ezra SIL. Cada fila combina hebreo dentro de una frase en español para comprobar el bidi: la palabra <span lang="he" dir="rtl">בָּרָא</span> («creó») no altera el orden de la frase.</p>
      <div class="tabla-scroll" role="region" aria-labelledby="pruebas-tit" tabindex="0">
      <table class="pruebas">
        <thead><tr><th scope="col">Caso</th><th scope="col">Muestra</th><th scope="col">Marcas</th></tr></thead>
        <tbody>
          <tr><th scope="row">Dagesh + qamets</th><td lang="he" dir="rtl">בָּרָא</td><td>U+05BC, U+05B8</td></tr>
          <tr><th scope="row">Shin con punto y shewa</th><td lang="he" dir="rtl">בְּרֵאשִׁית</td><td>U+05C1, U+05B0</td></tr>
          <tr><th scope="row">Sin con punto</th><td lang="he" dir="rtl">עֵשֶׂב</td><td>U+05C2</td></tr>
          <tr><th scope="row">Ḥatef segol</th><td lang="he" dir="rtl">אֱלֹהִים</td><td>U+05B1, U+05B9</td></tr>
          <tr><th scope="row">Maqaf</th><td lang="he" dir="rtl">וַיְהִי־כֵן</td><td>U+05BE</td></tr>
          <tr><th scope="row">Ḥolam sobre vav (ḥolam male)</th><td lang="he" dir="rtl">אוֹר</td><td>U+05D5 + U+05B9</td></tr>
          <tr><th scope="row">Pataḥ furtivo</th><td lang="he" dir="rtl">מַזְרִיעַ</td><td>U+05E2 + U+05B7</td></tr>
          <tr><th scope="row">Sof pasuq</th><td lang="he" dir="rtl">הָאָרֶץ׃</td><td>U+05C3</td></tr>
          <tr><th scope="row">Meteg</th><td lang="he" dir="rtl">וַֽיְהִי</td><td>U+05BD</td></tr>
        </tbody>
      </table>
      </div>
    </section>
  </article>

  <aside class="lateral" aria-labelledby="lat-tit">
    <h2 id="lat-tit">En este capítulo</h2>
    <ul>
      <li><a href="#v1">1:1 Hebreo y comentario</a></li>
      <li><a href="#v11">1:11 Prueba de estrés del interlineal</a></li>
      <li><a href="#pruebas-tit">Pruebas tipográficas</a></li>
    </ul>
  </aside>

  <nav class="nav-cap" aria-label="Capítulos de Génesis">
    <div class="prev-next">
      <span></span>
      <a href="#" rel="next">Génesis 2 ›</a>
    </div>
    <ol class="capitulos">
      <li><span aria-current="page"><span class="oculto">Capítulo </span>1</span></li>
      <li><a href="#"><span class="oculto">Capítulo </span>2</a></li>
      <li><a href="#"><span class="oculto">Capítulo </span>3</a></li>
      <li><a href="#"><span class="oculto">Capítulo </span>4</a></li>
      <li><a href="#"><span class="oculto">Capítulo </span>5</a></li>
    </ol>
  </nav>
</main>

<footer>
  <div class="contenedor">Prototipo aislado UX-001 (#8). Tipografías: Source Serif 4 (OFL 1.1, Adobe) y Ezra SIL 2.51 (OFL 1.1 + MIT, SIL International). Datos hebreos: OSHB (WLC dominio público; morfología CC BY 4.0). — Claude Code</div>
</footer>
<!-- Mejora progresiva opcional: al seguir un enlace a una fila de análisis, abre su <details>. Sin JS, el resumen sigue siendo operable. -->
<script>
  function abrirDestino() {{
    var t = location.hash && document.getElementById(location.hash.slice(1));
    for (var d = t; d; d = d.parentElement) if (d.tagName === 'DETAILS') d.open = true;
    if (t) t.scrollIntoView();
  }}
  addEventListener('hashchange', abrirDestino); abrirDestino();
</script>
</body>
</html>
'''


(AQUI.parent / "genesis-1.html").write_text(pagina("compacto"), encoding="utf-8")
(AQUI.parent / "genesis-1-tarjetas.html").write_text(pagina("tarjetas"), encoding="utf-8")
for v in ("Gen.1.1", "Gen.1.11"):
    for p in palabras(v):
        print(v, p["n"], p["heb"], p["morf"], "→", p["an"], p["strong"])
