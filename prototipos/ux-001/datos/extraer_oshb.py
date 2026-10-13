"""Extrae Gn 1:1 y Gn 1:11 de OSHB (morphhb/wlc/Gen.xml) a JSON, sin editar los datos importados.

Uso: python3 extraer_oshb.py ruta/a/Gen.xml > oshb-gn-1.json
Fuente: https://github.com/openscriptures/morphhb (texto WLC: dominio público;
lemas y morfología: CC BY 4.0, Open Scriptures Hebrew Bible Project).
Candidata en PEND-01: su uso aquí no decide la fuente definitiva. — Claude Code
"""
import json
import re
import sys
import xml.etree.ElementTree as ET

NS = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
VERSOS = ["Gen.1.1", "Gen.1.11"]

root = ET.parse(sys.argv[1]).getroot()
salida = {"fuente": "OSHB morphhb wlc/Gen.xml", "versos": {}}
for v in root.iterfind(".//o:verse", NS):
    osis = v.get("osisID")
    if osis not in VERSOS:
        continue
    palabras = []
    for el in v:
        tag = el.tag.split("}")[1]
        if tag == "w":
            palabras.append({"id": el.get("id"), "texto": el.text, "lema": el.get("lemma"), "morf": el.get("morph")})
        elif tag == "seg":
            # maqaf o sof pasuq: se adjunta a la palabra anterior
            palabras[-1]["sigue"] = {"x-maqqef": "maqaf", "x-sof-pasuq": "sof_pasuq"}.get(el.get("type"), el.get("type"))
    salida["versos"][osis] = palabras
json.dump(salida, sys.stdout, ensure_ascii=False, indent=1)
