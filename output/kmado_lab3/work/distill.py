from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import json
from docx import Document
B=Path(__file__).resolve().parent
p=Path('C:/Users/ПК/Downloads/2026_titul_lr (2).docx')
z=ZipFile(p)
parts={n:{'size':len(z.read(n)),'sha256':sha256(z.read(n)).hexdigest()} for n in z.namelist()}
(B/'template-parts.json').write_text(json.dumps(parts,indent=2),encoding='utf8')
text=f'''# Laboratory report template contract
Reference: {p}
SHA256: {sha256(p.read_bytes()).hexdigest()}
Evidence: template.pdf; template_render/page-1.png and page-2.png; template-style-evidence.json; template-parts.json.
Reference has 2 pages and 1 portrait A4 section. Body is expandable per user's lab completion request.
Page size 21.000861 × 29.700361 cm; margins T/B 2.00025 cm, L 2.501194 cm, R 1.501069 cm.
Different first page header; retain original header and PAGE field on subsequent pages, top right.
Typography: Times New Roman 14 pt; line spacing 1.5; body justified with 1.25 cm first-line indent; no paragraph-after space.
Cover: ministry/university/department paragraphs 0–3 centered 14 pt; blank paragraphs 4–8 retain vertical position; report paragraphs 9–10 bold centered; title paragraphs 11–12 centered; course paragraph 13 centered.
Identity block paragraphs 15–25: Times New Roman 10 pt, left indent 9.000 cm, line 1.5. Signature underline tab stops retained.
Committee rows 27–32 retain signature lines and compact 7 pt sublabels. City/year paragraph 34 centered 14 pt; existing page break retained.
Editable slots in word/document.xml w:body/w:p (zero-based): p10 lab number -> 3; p11–12 subject -> trigger study on logic elements; p15 group -> ІПЗ–11 (03); p19 name -> Сепан РИЧІХІН, preserving underline/tab runs. All other cover paragraphs preserved.
Body p35 onward is placeholder laboratory-1 content and must be replaced with laboratory-3 content: purpose, theory, 13 schemes/tables, Boolean checks, timing diagrams, Karnaugh minimization, 26 answers, conclusions and sources.
Body headings clone source centered bold 14 pt role with keep-next. New table role uses 11.5–12 pt Times New Roman, single spacing, repeating header and light-gray visible borders; figures center within 17 cm content width with 12 pt captions. This is an added role needed by the requested lab, not a change to cover style.
Use one full page per investigated circuit, with table, equation and four computed state examples. Insert explicit breaks between coherent sections.
Figures: deterministic IEC-like editable draw.io symbols; slash denotes inversion. No claimed Multisim captures; outputs labeled logical verification.
Package preserve-only parts: every original package member except word/document.xml and word/_rels/document.xml.rels and [Content_Types].xml. Existing relationships retained. Any added relationships only link new figure media.
Use python-docx to create body objects, then merge document.xml/new image parts and appended relationships into original ZIP so preserve-only parts remain byte-identical. Do not alter existing styles, headers, numbering, theme, or metadata.
Title paragraph uses Title style but explicit source formatting retained. New heading roles may use existing heading styles with direct source-derived formatting.
Fidelity gate: visually inspect every final page, compare original cover outside the five replacement slots; validate all preserve-only part hashes; verify reference hash unchanged; confirm no old placeholder lab text remains.
Renderer: packaged render_docx.py failed because bundled Windows LibreOffice is absent. Microsoft Word COM read-only ExportAsFixedFormat succeeded; bundled Poppler rasterizes PDFs. Use this verified native Word rendering fallback for final QA.
'''
(B/'artifact.md').write_text(text,encoding='utf8')
print('Template contract written')
