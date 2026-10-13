# Comentario Bíblico — Documento de requisitos

| Campo | Valor |
|---|---|
| Estado | Borrador v0.1 — pendiente de auditoría independiente |
| Alcance | MVP: Génesis 1–5 (138 versículos) |
| Fase SDD | 1. Requisitos (no es plan, ni especificación técnica, ni código) |
| Fuente | Registro de decisiones aprobado tras dos auditorías |

Convenciones del documento:

- **DEBE**: requisito obligatorio del MVP.
- **DEBERÍA**: recomendado; su omisión se justifica por escrito.
- **PUEDE**: opcional.
- Cada requisito tiene un identificador (`RF-` funcional, `RNF-` no funcional, `RE-` editorial, `RL-` legal, `RD-` de datos) para poder trazarlo hasta la especificación, las tareas y las pruebas.
- **[PENDIENTE]** marca decisiones abiertas; la sección 12 las reúne y dice cuáles bloquean.

---

## 1. Visión y alcance

### 1.1 Visión

Un comentario bíblico en español, **neutral y didáctico**, que ayude a entender cada versículo a partir de:

1. El texto bíblico en español.
2. El texto en su idioma original, analizado palabra por palabra (forma, transliteración, significado y gramática).
3. Una explicación clara del contexto y del sentido literal.
4. Referencias a otros pasajes.

El proyecto se aleja de teorías sin fundamento y de la polémica. Donde existan lecturas distintas y conocidas, las menciona brevemente, atribuidas y sin tomar partido.

### 1.2 Alcance del MVP

| Incluido | Excluido (fuera del MVP) |
|---|---|
| Génesis 1–5: 31 + 25 + 24 + 26 + 32 = **138 versículos** | Resto de la Biblia |
| Home, páginas de testamento, libro y capítulo, y páginas de versículo publicadas | Búsqueda, cuentas de usuario, comentarios de lectores |
| Interlineal hebreo de Gn 1–5 | Interlineal griego (NT) |
| Léxico de glosas para los lemas de Gn 1–5 | Léxico general navegable como sección propia |
| Referencias cruzadas editoriales | Importación masiva de referencias cruzadas |
| Páginas de metodología, fuentes y "acerca de" | Clusters de personajes, lugares o temas |
| Canon de 66 libros, ampliable | Deuterocanónicos |
| Español | Otros idiomas |

**RF-001** El MVP DEBE permitir navegar desde la Home hasta cada uno de los 138 versículos de Gn 1–5 sin usar JavaScript.

**RF-002** El sistema DEBE poder incorporar nuevos capítulos y libros solo añadiendo datos y contenido, sin modificar componentes ni rutas.

---

## 2. Principios rectores

1. **Separación de capas.** El canon, los textos, el idioma original, el léxico, el comentario y la presentación son independientes. Cambiar la traducción no toca los comentarios.
2. **Procedencia explícita.** Todo dato muestra de dónde viene: corpus importado, derivado por código o redactado por el equipo editorial.
3. **Nada se publica sin revisión humana.**
4. **Las reglas editoriales se convierten en pruebas automáticas** siempre que sea posible.
5. **Profundidad variable.** Un versículo solo tiene página propia si aporta contenido propio; nunca hay páginas de relleno.
6. **HTML primero.** Todo el contenido se lee sin JavaScript.

---

## 3. Público y casos de uso

| Perfil | Caso de uso principal |
|---|---|
| Lector general | Leer Génesis 1 de corrido y desplegar explicaciones donde le interese. |
| Estudiante | Entender qué significa y cómo se conjuga cada palabra hebrea de un versículo. |
| Visitante desde buscador | Llegar desde "Génesis 1:1 significado" a una página que responde directamente. |
| Revisor editorial (el propietario) | Revisar y aprobar borradores con la seguridad de que las comprobaciones automáticas ya han filtrado los errores mecánicos. |

**Dispositivo prioritario: móvil.**

---

## 4. Arquitectura de información y URLs

### 4.1 Jerarquía

```
Home
├── Antiguo Testamento
│   └── Génesis
│       └── Capítulo 1 … 5        ← experiencia principal de lectura
│           ├── Perícopas (secciones dentro del capítulo, sin URL propia en el MVP)
│           └── Versículo n        ← página propia solo si está publicado
└── Nuevo Testamento              ← página introductoria (ver PEND-07)
Páginas institucionales: Metodología · Fuentes · Acerca de
```

### 4.2 URLs

| Página | URL | Ejemplo |
|---|---|---|
| Home | `/` | `/` |
| Testamento | `/antiguo-testamento/`, `/nuevo-testamento/` | |
| Libro | `/{libro}/` | `/genesis/` |
| Capítulo | `/{libro}/{capitulo}/` | `/genesis/1/` |
| Versículo | `/{libro}/{capitulo}/{versiculo}/` | `/genesis/1/1/` |
| Ancla de versículo en el capítulo | `/{libro}/{capitulo}/#v{n}` | `/genesis/1/#v3` |

**RF-010** El slug del libro DEBE estar en español, en minúsculas, sin tildes ni eñes (`genesis`, `exodo`, `1-samuel`, `cantares`). La tabla de slugs de los 66 libros forma parte de los datos del canon.

**RF-011** La URL del libro NO DEBE incluir el testamento, para que sea corta y estable.

**RF-012** Una URL publicada NO DEBE cambiar. Si fuera inevitable, DEBE existir una redirección 301.

**RF-013** Internamente, toda referencia bíblica DEBE expresarse con identificadores OSIS (`Gen.1.1`, `Gen.1.1-Gen.2.3`). El slug solo se usa en presentación.

**RF-014** Los versículos sin página publicada DEBEN enlazarse a su ancla dentro del capítulo, nunca a una URL inexistente.

---

## 5. Requisitos por tipo de página

### 5.1 Home

**RF-020** DEBE incluir: presentación del proyecto, enfoque (neutral y didáctico), introducción breve a la Biblia, acceso a los dos testamentos y un acceso directo a "Empezar a leer: Génesis 1".

### 5.2 Testamento

**RF-021** DEBE incluir: introducción, contexto histórico general, organización en secciones (Pentateuco, históricos, poéticos, proféticos…) y la lista de libros.

**RF-022** Los libros sin contenido publicado DEBEN mostrarse como texto, sin enlace, y marcados como "próximamente".

### 5.3 Libro

**RF-023** DEBE incluir, cuando aporte valor: título en español y en el idioma original, autoría según la tradición y la investigación (atribuidas), fecha, propósito, estructura, temas principales y lista de capítulos.

### 5.4 Capítulo (experiencia principal)

**RF-024** DEBE mostrar el capítulo completo en la traducción base, con el número de cada versículo y un ancla `#v{n}`.

**RF-025** DEBE incluir introducción, resumen y estructura del capítulo, y DEBE mostrar los comentarios de perícopa en su sección correspondiente.

**RF-026** Cada versículo DEBE poder desplegar su comentario y su interlineal con `<details>`/`<summary>` o un equivalente que funcione sin JavaScript.

**RF-027** Los versículos con página propia DEBEN enlazar a ella ("comentario completo").

**RF-028** DEBE haber navegación al capítulo anterior y al siguiente.

### 5.5 Versículo

**RF-029** Solo existe para versículos en estado `publicado` que cumplan los criterios de contenido sustancial (RE-030).

**RF-030** Debe incluir, en este orden y omitiendo las secciones vacías:

1. Referencia y texto en la traducción base.
2. Interlineal completo (sección 6).
3. Explicación: sentido literal y contexto.
4. Notas lingüísticas.
5. Otras lecturas, si las hay (RE-012).
6. Referencias cruzadas, con las "citado en" calculadas automáticamente.
7. Fuentes.
8. Ficha editorial: estado, fecha de revisión y procedencia de los datos.

**RF-031** DEBE tener navegación al versículo anterior y al siguiente (a su página o a su ancla, según RF-014), y un enlace de vuelta al capítulo.

**RF-032** DEBE mostrar el enlace a la perícopa que lo contiene, en lugar de repetir el comentario de esa perícopa.

### 5.6 Páginas institucionales

**RF-033** **Metodología**: enfoque neutral, uso de IA con revisión humana, tipos de afirmación, cómo se tratan las lecturas distintas y significado de cada origen de datos.

**RF-034** **Fuentes**: bibliografía completa, generada a partir del registro de fuentes.

**RF-035** **Acerca de**: créditos y licencias del texto bíblico, del corpus hebreo, de las tipografías y del propio contenido.

---

## 6. Interlineal (núcleo didáctico)

### 6.1 Modelo conceptual

```
Versículo
└── Token (palabra gráfica; puede ir unida por maqaf)
    └── Segmento morfológico (prefijo · raíz/base · sufijo)
        ├── Lema
        ├── Etiqueta morfológica de origen
        └── Glosa contextual
```

Por ejemplo, `בְּרֵאשִׁית` es un token con dos segmentos: la preposición `בְּ` («en») y el sustantivo `רֵאשִׁית` («principio»).

### 6.2 Tres orígenes de datos

| Origen | Contenido | Quién lo produce | Puede editarse a mano |
|---|---|---|---|
| **Importado** | Texto hebreo, identificadores, segmentación, lema, etiqueta morfológica | Corpus académico (PEND-01) | No (las correcciones se documentan como parche) |
| **Derivado** | Descripción morfológica en español, transliteración, guía de lectura | Código determinista, a partir de lo importado | No (se corrige la regla, no el resultado) |
| **Editorial** | Glosas contextuales, notas lingüísticas, explicaciones | IA en borrador + revisión humana | Sí, mediante el flujo editorial |

**RD-001** Cada token y cada segmento DEBEN conservar el identificador del dato de origen en el corpus.

**RD-002** El modelo DEBE registrar el origen (importado, derivado o editorial) de cada campo del interlineal.

**RF-040** La interfaz DEBE distinguir visualmente y en el texto accesible los datos editoriales de los importados. Como mínimo debe haber una leyenda, y en la ficha editorial, la procedencia de cada capa.

**RD-003** Las correcciones al corpus importado NO DEBEN modificar el archivo original. DEBEN aplicarse como parches documentados, cada uno con su motivo y una fuente.

### 6.3 Columnas visibles por token

| Campo | Ejemplo (בָּרָא) | Origen |
|---|---|---|
| Hebreo (con vocales) | בָּרָא | Importado |
| Transliteración | bārāʾ | Derivado |
| Guía de lectura (aproximada) | ba-RÁ | Derivado |
| Glosa contextual | creó | Editorial |
| Análisis | Verbo · Qal · Perfecto · 3.ª persona masculino singular | Derivado |
| Lema / raíz | ברא | Importado |

**RF-041** La transliteración y la guía de lectura son **campos distintos**. La guía se presenta siempre como aproximada y didáctica; nunca se afirma que reproduce la pronunciación del hebreo bíblico.

**RF-042** La descripción morfológica en español DEBE generarse por código a partir de las etiquetas de origen. Una etiqueta sin traducción definida DEBE hacer fallar la compilación.

**RF-043** La glosa es **contextual** (la del versículo), pero DEBE partir del léxico de glosas por lema (RD-020) para mantener la consistencia.

**RF-044** Cada término gramatical (Qal, perfecto, wayyiqtol, estado constructo…) DEBERÍA enlazar a una explicación breve en un glosario gramatical. El glosario PUEDE ser una sola página en el MVP.

### 6.4 Presentación y accesibilidad del hebreo

**RNF-001** El hebreo DEBE marcarse con `lang="he"` y `dir="rtl"`. La transliteración, con `lang="he-Latn"`.

**RNF-002** Se DEBE usar una tipografía hebrea con licencia libre (OFL), servida desde el propio sitio.

**RNF-003** Se DEBEN mostrar las vocales (niqud). Mostrar los acentos de cantilación (teamim) es [PENDIENTE] (PEND-04).

**RNF-004** El orden de lectura del interlineal DEBE ser correcto en móvil y en lectores de pantalla: los tokens siguen el orden del texto aunque la disposición visual sea de derecha a izquierda.

**RNF-005** DEBEN existir pruebas con caracteres combinados (vocales, dagesh, maqaf, sof pasuq), normalización Unicode (NFC frente al orden de marcas del corpus) y texto bidireccional mezclado (hebreo dentro de frases en español).

---

## 7. Modelo de datos conceptual

> Es un modelo **conceptual**: entidades, campos y relaciones. La definición exacta de esquemas y formatos de archivo corresponde a la especificación técnica.

### 7.1 Capas

| Capa | Entidades | Cambia… |
|---|---|---|
| Canon | Libro (id OSIS, slug, nombre, nombre original, testamento, orden, número de capítulos), Capítulo (número de versículos) | Casi nunca |
| Versificación | Esquema de versificación, mapa de equivalencias entre esquemas | Casi nunca (se implementa más adelante) |
| Textos | Edición (id, nombre, licencia, procedencia, esquema de versificación), Versículo de texto (ref OSIS, texto) | Rara vez |
| Original | Token, Segmento (sección 6) | Rara vez |
| Léxico de glosas | Entrada por lema (lema, sentidos, glosa por sentido, estado editorial) | Crece despacio |
| Comentario | Comentario (anclado a un rango OSIS) | Continuamente |
| Fuentes | Fuente (id, tipo, datos bibliográficos, URL de consulta si existe) | Crece |
| Referencias cruzadas | Referencia (origen, destino, tipo, procedencia) | Crece |

### 7.2 Requisitos de datos

**RD-010** Los comentarios NO DEBEN incrustar texto bíblico de una traducción concreta. Lo referencian por id OSIS. Citar una palabra o expresión dentro de la explicación está permitido.

**RD-011** Un comentario DEBE anclarse a un **rango** (`Gen.1.26` o `Gen.1.1-Gen.2.3`). Los tipos de comentario son: libro, capítulo, perícopa y versículo.

**RD-012** Cada comentario DEBE incluir estos metadatos editoriales:

| Campo | Contenido |
|---|---|
| `estado` | `borrador`, `aprobado` o `publicado` |
| `revisadoPor` y `fechaRevision` | Quién lo revisó y cuándo |
| `versionEsquema` | Versión del esquema editorial |
| `asistidoPorIA` | Si la IA participó en la redacción |
| `fuentes` | Lista de ids de fuentes |

**RD-013** Toda referencia (OSIS, id de fuente, id de lema) DEBE resolverse a algo existente. Si no, la compilación falla.

**RD-014** Una referencia cruzada DEBE tener un tipo (`cita`, `alusión`, `paralelo`, `temática`) y una procedencia. Las referencias inversas ("citado en") DEBEN calcularse al compilar, nunca escribirse a mano.

**RD-015** El esquema DEBE prever que una edición use un esquema de versificación distinto y que exista una tabla de equivalencias, sin alterar las URLs canónicas. La implementación del mapeo se pospone. En el MVP basta con que la edición declare su esquema.

**RD-016** Los datos del canon DEBEN incluir los 66 libros desde el MVP (sirven para la navegación y la validación). El modelo DEBE permitir añadir libros deuterocanónicos sin cambiar las URLs existentes.

**RD-020** El léxico de glosas DEBE organizarse por lema y sentido, y reutilizarse entre versículos. Una glosa contextual que se aparte del léxico DEBE quedar marcada y justificada.

**RD-021** Las fuentes DEBEN clasificarse por tipo (léxico, gramática, comentario académico, comentario clásico, fuente primaria antigua, edición del texto) y DEBERÍAN incluir un enlace de consulta pública cuando exista.

---

## 8. Política editorial

### 8.1 Enfoque

**RE-001** El comentario es **neutral y didáctico**: explica qué dice el texto, en qué contexto y con qué lenguaje. No defiende posiciones doctrinales.

**RE-002** Prioriza el sentido literal y el contexto. Excluye lecturas devocionales, alegóricas o aplicaciones personales, salvo cuando se mencionen de forma descriptiva y atribuida.

**RE-003** NO DEBE incluir teorías sin fundamento, especulaciones ni conexiones científicas o arqueológicas forzadas.

### 8.2 Tipos de afirmación

**RE-010** Toda afirmación especializada DEBE clasificarse en uno de estos tipos:

| Tipo | Ejemplo | Evidencia exigida |
|---|---|---|
| Lingüística | «en Qal, *bārāʾ* tiene siempre a Dios como sujeto» | Léxico o gramática |
| Histórica / cultural | «Los relatos de creación eran comunes en el antiguo Oriente Próximo» | Estudio académico o fuente primaria |
| Literaria | «Gn 1 se organiza en seis días con un patrón repetido» | Estudio o análisis del propio texto (referencias OSIS) |
| Interpretativa | «La tradición judía lee… ; muchos intérpretes cristianos leen…» | Fuentes que la sostienen, atribuidas |

**RE-011** Una afirmación lingüística, histórica o interpretativa sin fuente DEBE hacer fallar la validación. Las afirmaciones literarias pueden apoyarse solo en referencias del propio texto.

**RE-012** Lecturas distintas: cuando haya interpretaciones diferentes conocidas, se mencionan **brevemente** (orientación: una o dos frases cada una), atribuidas a quien las sostiene, sin argumentar ni concluir cuál es la correcta. La orientación de extensión puede superarse cuando simplificar daría una idea falsa (por ejemplo, Gn 1:1, 1:26 o 2:4).

**RE-013** Las expresiones atribuidas DEBEN identificar al sujeto: "la tradición rabínica", "los Padres de la Iglesia", "parte de la crítica académica". Fórmulas vagas como "algunos dicen" están prohibidas.

### 8.3 Fuentes

**RE-020** Se DEBEN priorizar fuentes que el revisor pueda consultar: léxicos y comentarios de dominio público (por ejemplo Gesenius, Brown-Driver-Briggs, Keil-Delitzsch) y obras académicas citables.

**RE-021** Una fuente citada DEBE existir en el registro de fuentes con datos bibliográficos verificables. La IA NO DEBE introducir fuentes nuevas sin que el revisor las confirme.

**RE-022** Las citas DEBERÍAN incluir localizador (página, entrada o sección) cuando la fuente lo permita.

### 8.4 Uso de IA

**RE-030** Criterios de **contenido sustancial**. Un versículo tiene página propia solo si cumple todos estos:

1. Su comentario tiene una explicación propia (no solo remite a la perícopa).
2. Tiene al menos una nota lingüística pertinente o un análisis de contexto específico del versículo.
3. Está en estado `publicado`.
4. No duplica el comentario de la perícopa.

El punto 4 lo verifica el revisor; los puntos 1 a 3 son automatizables.

**RE-031** La IA redacta borradores (comentarios, glosas, notas). **Nunca** genera los datos importados ni los derivados.

**RE-032** La página de Metodología DEBE declarar el uso de IA con revisión humana. Cada comentario DEBE indicar `asistidoPorIA`.

### 8.5 Estilo

**RE-040** Debe existir una guía de estilo (documento aparte, previo a la redacción masiva) que defina:

- El tono y la persona gramatical.
- Cómo se citan versículos.
- Cómo se escribe el hebreo dentro del texto en español.
- La terminología gramatical.
- La extensión orientativa de cada sección.

---

## 9. Flujo editorial y estados

### 9.1 Estados

```
borrador ──(revisión humana)──▶ aprobado ──(despliegue)──▶ publicado
    ▲                               │                          │
    └──────── cambio sustancial ────┴──────────────────────────┘
```

| Estado | Visible en el sitio | Ruta propia | Sitemap |
|---|---|---|---|
| `borrador` | No | No | No |
| `aprobado` | No (preparado para publicar) | No | No |
| `publicado` | Sí | Sí, si cumple RE-030 | Sí, si tiene ruta |

**RE-050** Un comentario en `borrador` NO DEBE aparecer en el HTML compilado. Ni siquiera dentro de la página de capítulo.

**RE-051** **Regla de transición:** cualquier cambio sustancial (de contenido, no tipográfico) en un comentario `aprobado` o `publicado` DEBE devolverlo a `borrador` y exigir una nueva aprobación antes del despliegue. Se controla con pull requests y metadatos, sin sistema de permisos.

**RE-052** Pasar a `publicado` requiere que `revisadoPor` y `fechaRevision` estén completos y que la fecha sea posterior al último cambio sustancial.

### 9.2 Flujo

1. **Borrador.** La IA genera el comentario y las glosas usando solo fuentes del registro.
2. **Verificación automática:** esquema, referencias, fuentes, tipos de afirmación y enlaces.
3. **Revisión humana.** El propietario revisa en el pull request.
4. **Aprobación:** cambio de estado y metadatos.
5. **Fusión y despliegue.**

**RE-053** La auditoría editorial (contenido) y la técnica (código) son procesos separados. Las auditorías editoriales independientes PUEDEN hacerse por muestreo, por capítulo.

---

## 10. Requisitos no funcionales

### 10.1 Accesibilidad

**RNF-010** Se DEBE cumplir WCAG 2.2 nivel AA.

**RNF-011** Todo el contenido y la navegación DEBEN funcionar sin JavaScript.

**RNF-012** Se DEBE usar HTML semántico: `nav` con migas de pan, `main`, `article` y encabezados jerárquicos sin saltos.

**RNF-013** El sitio DEBE pasar sin errores una auditoría automática de accesibilidad (por ejemplo, axe) en todas las páginas generadas.

### 10.2 SEO

**RNF-020** Cada página DEBE tener `title`, meta descripción, URL canónica, `lang="es"` y Open Graph básico.

**RNF-021** Se DEBEN incluir datos estructurados `BreadcrumbList` en todas las páginas, y `Article` (con fecha de revisión) en libro, capítulo y versículo.

**RNF-022** El sitemap DEBE incluir solo las páginas publicadas. Ninguna página en `borrador` o `aprobado` puede ser accesible.

**RNF-023** Los enlaces internos DEBEN funcionar al 100 % (verificado al compilar).

### 10.3 Rendimiento y despliegue

**RNF-030** El sitio DEBE generarse de forma estática y desplegarse en Cloudflare.

**RNF-031** La arquitectura DEBE ser compatible con el límite de archivos por despliegue de la plataforma, que hay que verificar. RE-030 (páginas solo cuando son sustanciales) es la primera mitigación.

**RNF-032** Las páginas DEBERÍAN funcionar bien sin JavaScript; se fija como objetivo que un capítulo con interlineal plegado pese menos de 200 KB transferidos (excluidas las tipografías en caché).

### 10.4 Mantenibilidad

**RNF-040** Los datos, el contenido y la presentación DEBEN vivir en ubicaciones separadas del repositorio.

**RNF-041** Toda regla de validación de esta especificación DEBE ejecutarse en la integración continua (CI) y bloquear la fusión si falla.

---

## 11. Licencias y procedencia

**RL-001** Para cada recurso externo (traducción, corpus hebreo, morfología, léxicos, tipografías, referencias cruzadas importadas) se DEBE registrar:

- Nombre.
- Edición o versión exacta.
- URL de origen.
- Licencia.
- Fecha de obtención.
- Atribución exigida.

**RL-002** Se DEBE verificar la licencia de la **edición digital concreta** (texto, notas, correcciones y morfología), no solo la de la obra. Que una obra esté en dominio público no implica que lo esté su digitalización.

**RL-003** Traducción base: **Reina-Valera 1909**. Se DEBE documentar la edición digital usada y cotejar Gn 1–5 con una edición impresa o escaneada antes de publicar.

**RL-004** Las atribuciones exigidas por las licencias (por ejemplo, CC BY) DEBEN aparecer en "Acerca de" y, si la licencia lo pide, junto al dato.

**RL-005** La licencia del contenido propio del sitio es [PENDIENTE] (PEND-06).

**RL-006** El cambio futuro a una traducción con licencia (por ejemplo, la RVR1960) DEBE requerir solo añadir una edición y cambiar la edición por defecto. Si esa licencia impone límites de uso, se añadirá una validación de conteo de versículos.

---

## 12. Decisiones pendientes

| ID | Decisión | Bloquea | Cuándo resolver |
|---|---|---|---|
| PEND-01 | **Fuente hebrea**: comparar OSHB (WLC + morfología), los datos de STEPBible (TAHOT) y otras opciones por licencia de la edición digital, segmentación, calidad de la morfología y facilidad de importación | **Sí**: el esquema del interlineal y la importación | Antes de la especificación técnica |
| PEND-02 | **Transliteración**: SBL académica, SBL general u otra; reglas para shewa, dagesh, matres lectionis y el nombre divino | **Sí**: el generador de transliteración | Antes de la especificación técnica |
| PEND-03 | **Guía de lectura**: convención didáctica (sílabas, acento, pronunciación sefardí o israelí moderna como base) | No (puede cerrarse en paralelo) | Antes de implementar el interlineal |
| PEND-04 | Mostrar o no los acentos de cantilación (teamim) | No | Antes del diseño visual |
| PEND-05 | **Ortografía de la RV1909**: tal cual (por ejemplo, «crió», «fué») o actualizada sin cambiar palabras | **Sí**: la importación del texto | Antes de la especificación técnica |
| PEND-06 | Licencia del contenido propio (CC BY-SA, CC BY-NC, todos los derechos reservados…) | No | Antes de publicar |
| PEND-07 | Contenido de la página del Nuevo Testamento en el MVP: introducción completa o mínima | No | Durante la redacción |
| PEND-08 | **Delimitación de perícopas** de Gn 1–5, especialmente la frontera de Gn 2:4 | No | Antes de redactar los comentarios |
| PEND-09 | Límite exacto de archivos por despliegue de Cloudflare (Pages o Workers) | No en el MVP | Antes de pasar de unos pocos libros |
| PEND-10 | Nombre del sitio y dominio | No | Antes de publicar |

---

## 13. Criterios de aceptación del MVP

Cada criterio debe poder comprobarse con una prueba automática (**A**) o con una revisión manual documentada (**M**).

| # | Criterio | Tipo |
|---|---|---|
| CA-01 | Existen 138 entradas de texto RV1909 para Gn 1–5 y coinciden con el número de versículos del canon | A |
| CA-02 | Los 138 versículos tienen interlineal completo; todo token tiene origen, lema, etiqueta, transliteración y glosa aprobada | A |
| CA-03 | Ninguna etiqueta morfológica de Gn 1–5 carece de traducción al español | A |
| CA-04 | Toda referencia OSIS, id de fuente e id de lema se resuelve | A |
| CA-05 | Ningún comentario en `borrador` o `aprobado` aparece en el HTML ni en el sitemap | A |
| CA-06 | Toda afirmación lingüística, histórica o interpretativa tiene al menos una fuente | A |
| CA-07 | Las referencias inversas ("citado en") coinciden con las directas | A |
| CA-08 | No hay enlaces internos rotos | A |
| CA-09 | Todas las páginas pasan la auditoría automática de accesibilidad sin errores | A |
| CA-10 | Toda la navegación de la Home a cada versículo funciona con JavaScript desactivado | A |
| CA-11 | Cada página tiene title, descripción, URL canónica y migas de pan con datos estructurados válidos | A |
| CA-12 | El texto de Gn 1–5 ha sido cotejado con una edición de referencia de la RV1909 | M |
| CA-13 | Cada comentario publicado tiene la revisión humana registrada | A (metadatos) + M |
| CA-14 | Las licencias y atribuciones de todos los recursos externos están documentadas y visibles | M |
| CA-15 | Los ejemplos de los Anexos A y B se pueden representar con el modelo de datos sin excepciones ni campos ad hoc | M |

---

## 14. Glosario

| Término | Definición |
|---|---|
| OSIS | Estándar de referencias bíblicas (`Gen.1.1`). |
| Perícopa | Unidad de texto con sentido completo (por ejemplo, Gn 1:1–2:3). |
| Token | Palabra gráfica del texto hebreo, separada por espacios o unida por maqaf. |
| Segmento | Parte morfológica de un token (prefijo, base, sufijo). |
| Lema | Forma de diccionario de una palabra. |
| Glosa | Traducción breve de una palabra en su contexto. |
| Wayyiqtol | Forma verbal hebrea con *waw* consecutiva, típica de la narración. |
| Maqaf | Guion hebreo (־) que une palabras en una unidad de acentuación. |
| Niqud / teamim | Signos vocálicos / acentos de cantilación del texto masorético. |

---

## Anexo A — Ejemplo vertical: Génesis 1:1

> **Propósito:** comprobar que el modelo representa un caso real completo.
> **Advertencia:** los datos son **ilustrativos**. Las etiquetas morfológicas siguen el estilo de OSHB y DEBEN contrastarse con la fuente elegida (PEND-01). La transliteración sigue provisionalmente un estilo SBL académico (PEND-02). El texto RV1909 está pendiente de cotejo (RL-003). El comentario es un borrador de ejemplo, no contenido aprobado.

### A.1 Texto

- **RV1909:** «EN el principio crió Dios los cielos y la tierra.» *(ortografía original; véase PEND-05)*
- **Hebreo:** בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ׃

### A.2 Interlineal

| # | Hebreo | Segmentos | Translit. | Guía | Glosa | Análisis (derivado) | Lema | Etiqueta (import.) |
|---|---|---|---|---|---|---|---|---|
| 1 | בְּרֵאשִׁית | בְּ + רֵאשִׁית | bərēʾšît | be-re-SHIT | en (el) principio | Preposición + sustantivo femenino singular | רֵאשִׁית | `HR/Ncfsa` |
| 2 | בָּרָא | בָּרָא | bārāʾ | ba-RÁ | creó | Verbo Qal perfecto, 3.ª m. sg. | ברא | `HVqp3ms` |
| 3 | אֱלֹהִים | אֱלֹהִים | ʾĕlōhîm | e-lo-HIM | Dios | Sustantivo masculino plural | אֱלֹהִים | `HNcmpa` |
| 4 | אֵת | אֵת | ʾēt | et | — (marca de objeto directo) | Partícula de objeto directo | אֵת | `HTo` |
| 5 | הַשָּׁמַיִם | הַ + שָּׁמַיִם | haššāmayim | ha-sha-MA-yim | los cielos | Artículo + sustantivo masculino plural | שָׁמַיִם | `HTd/Ncmpa` |
| 6 | וְאֵת | וְ + אֵת | wəʾēt | ve-ET | y — | Conjunción + partícula de objeto directo | אֵת | `HC/To` |
| 7 | הָאָרֶץ | הָ + אָרֶץ | hāʾāreṣ | ha-A-rets | la tierra | Artículo + sustantivo singular | אֶרֶץ | `HTd/Ncbsa` |

Casos del modelo que valida este ejemplo:

- Un token con varios segmentos (1, 5, 6, 7).
- Una palabra sin glosa traducible (4): la glosa debe admitir una «función» en lugar de una traducción.
- Un lema con género común o ambiguo (7).

### A.3 Comentario (borrador ilustrativo)

**Explicación.** El versículo abre el relato de la creación con una afirmación general: Dios es el sujeto de la acción y «los cielos y la tierra» abarca la totalidad de lo creado. *[Literaria; ref. Gen.1.1, Gen.2.1]*

**Notas lingüísticas.**

- En la forma Qal, el verbo *bārāʾ* («crear») tiene en la Biblia hebrea siempre a Dios como sujeto. *[Lingüística; fuente: léxico BDB, s.v. ברא]*
- *ʾĕlōhîm* tiene forma plural, pero aquí va con un verbo en singular (*bārāʾ*), lo que indica que se refiere a un único sujeto. *[Lingüística; fuente: gramática de Gesenius §124g]*
- «Los cielos y la tierra» es un merismo: dos extremos que expresan la totalidad. *[Lingüística/literaria; fuente: por asignar]*

**Otras lecturas.** La primera palabra, *bərēʾšît*, no lleva artículo. Por eso, una parte de la tradición judía (Rashi) y algunas traducciones modernas leen el versículo como una oración subordinada: «Cuando Dios comenzó a crear…». La lectura tradicional, reflejada en la RV1909 y en la mayoría de las traducciones, lo entiende como una afirmación independiente: «En el principio creó Dios…». *[Interpretativa; fuentes: Rashi sobre Gn 1:1; por asignar]*

**Referencias cruzadas.**

| Destino | Tipo |
|---|---|
| Jn 1:1 | Alusión |
| Sal 33:6 | Temática |
| Heb 11:3 | Temática |
| Gn 2:4 | Paralelo |

**Ficha editorial.** Estado: `borrador` · asistidoPorIA: sí · revisadoPor: — · versionEsquema: 0.1

> Lo que el ejemplo pone a prueba: la afirmación marcada «fuente: por asignar» haría fallar la validación (RE-011). Es el comportamiento esperado: el borrador no puede aprobarse así.

---

## Anexo B — Ejemplo vertical: Génesis 1:3

> Mismas advertencias que el Anexo A. Este ejemplo se incluye porque contiene el *wayyiqtol*, la forma narrativa dominante en Génesis, y una forma yusiva.

### B.1 Texto

- **RV1909:** «Y dijo Dios: Sea la luz: y fué la luz.» *(pendiente de cotejo; ortografía original)*
- **Hebreo:** וַיֹּאמֶר אֱלֹהִים יְהִי אוֹר וַיְהִי־אוֹר׃

### B.2 Interlineal

| # | Hebreo | Segmentos | Translit. | Guía | Glosa | Análisis (derivado) | Lema | Etiqueta (import.) |
|---|---|---|---|---|---|---|---|---|
| 1 | וַיֹּאמֶר | וַ + יֹּאמֶר | wayyōʾmer | va-YÓ-mer | y dijo | Conjunción (waw consecutiva) + verbo Qal wayyiqtol, 3.ª m. sg. | אמר | `HC/Vqw3ms` |
| 2 | אֱלֹהִים | אֱלֹהִים | ʾĕlōhîm | e-lo-HIM | Dios | Sustantivo masculino plural | אֱלֹהִים | `HNcmpa` |
| 3 | יְהִי | יְהִי | yəhî | ye-HÍ | sea / haya | Verbo Qal yusivo, 3.ª m. sg. | היה | `HVqj3ms` |
| 4 | אוֹר | אוֹר | ʾôr | or | luz | Sustantivo singular | אוֹר | `HNcbsa` |
| 5 | וַיְהִי־ | וַ + יְהִי | wayəhî | va-ye-HÍ | y fue / y hubo | Conjunción (waw consecutiva) + verbo Qal wayyiqtol, 3.ª m. sg. | היה | `HC/Vqw3ms` |
| 6 | אוֹר | אוֹר | ʾôr | or | luz | Sustantivo singular | אוֹר | `HNcbsa` |

Casos del modelo que valida este ejemplo:

- Maqaf entre los tokens 5 y 6: unidad gráfica y prosódica, pero dos tokens.
- Un mismo lema (היה) en dos formas distintas (yusivo y wayyiqtol), con glosas contextuales diferentes que salen de la misma entrada del léxico.
- El término gramatical «wayyiqtol» necesita su entrada en el glosario (RF-044).
- La guía de lectura debe tratar el dagesh de יֹּ en *wayyōʾmer* (consonante doble).

### B.3 Comentario (borrador ilustrativo)

**Explicación.** Es el primer acto de habla divino del relato. La estructura «Y dijo Dios… y fue…» se repite a lo largo del capítulo y marca el ritmo de los días. *[Literaria; refs. Gen.1.6, Gen.1.9, Gen.1.14]*

**Notas lingüísticas.**

- *wayyōʾmer* es un **wayyiqtol**: la forma con la que la narración hebrea encadena hechos sucesivos («y dijo… y fue…»). Se traduce normalmente con un pasado en español. *[Lingüística; fuente: gramática de referencia, por asignar]*
- *yəhî* es un **yusivo** («sea», «haya»): expresa una orden o un deseo en tercera persona. El versículo pasa de la orden (*yəhî ʾôr*) a su cumplimiento (*wayəhî ʾôr*) con el mismo verbo. *[Lingüística; fuente: por asignar]*

**Otras lecturas.** La luz aparece antes que el sol, que se crea en el día cuarto (Gn 1:14–19). La tradición interpretativa ha propuesto varias explicaciones; el comentario las mencionaría atribuidas, sin desarrollarlas. *[Interpretativa; fuentes: por asignar]*

**Referencias cruzadas.**

| Destino | Tipo |
|---|---|
| 2 Co 4:6 | Alusión |
| Sal 33:9 | Temática |
| Gn 1:14–18 | Paralelo |

**Ficha editorial.** Estado: `borrador` · asistidoPorIA: sí · revisadoPor: — · versionEsquema: 0.1

---

## Siguientes pasos

1. Auditoría independiente de este documento: requisitos ambiguos, inconsistentes o no verificables.
2. Resolver los pendientes bloqueantes: PEND-01, PEND-02 y PEND-05.
3. Redactar la guía de estilo editorial (RE-040).
4. Plan de implementación, especificación técnica (SDD), auditoría de la especificación y tareas.
