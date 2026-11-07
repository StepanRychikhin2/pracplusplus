from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile, ZIP_DEFLATED
from hashlib import sha256
from itertools import product
from lxml import etree
import json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import assets as A

B=Path(__file__).resolve().parent;OUT=B.parent
SRC=Path('C:/Users/ПК/Downloads/2026_titul_lr (2).docx')
FINAL=OUT/'ЛР3_КМАДО_Ричіхін.docx'
doc=Document(SRC)
body=doc._element.body
original_hash=sha256(SRC.read_bytes()).hexdigest()
assert original_hash in (B/'artifact.md').read_text(encoding='utf8')
for name in ['Title','Heading 1','Heading 2']:
    if name not in doc.styles:
        st=doc.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
        st.base_style=doc.styles['Normal']

def replace_text(p,text):
    # Only replace visible text; cover paragraph properties are retained.
    first=p.runs[0]
    first.text=text
    for r in p.runs[1:]:r.text=''

replace_text(doc.paragraphs[10],'з лабораторної роботи № 3')
replace_text(doc.paragraphs[11],'на тему «Дослідження тригерів')
replace_text(doc.paragraphs[12],'на логічних елементах»')
for r in doc.paragraphs[15].runs:
    if r.text=='01':r.text='03'
for r in doc.paragraphs[19].runs:
    if r.text=='Ім’я':r.text='Сепан'
    elif r.text=='ПРІЗВИЩЕ':r.text='РИЧІХІН'
doc.paragraphs[9].style='Title'
for r in doc.paragraphs[9].runs:r.font.color.rgb=RGBColor(0,0,0)
for p in list(doc.paragraphs)[35:]:p._element.getparent().remove(p._element)

def fmt(p,size=14,bold=False,align=WD_ALIGN_PARAGRAPH.JUSTIFY,indent=1.25,line=1.5,after=0,before=0):
    p.alignment=align
    pf=p.paragraph_format;pf.first_line_indent=Cm(indent);pf.left_indent=Cm(0);pf.right_indent=Cm(0)
    pf.line_spacing=line;pf.space_after=Pt(after);pf.space_before=Pt(before);pf.widow_control=True
    for r in p.runs:
        r.font.name='Times New Roman';r.font.size=Pt(size);r.bold=bold;r.font.color.rgb=RGBColor(0,0,0)
        r._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Times New Roman')
    return p
def p(text='',size=14,**kw):return fmt(doc.add_paragraph(text),size=size,**kw)
def heading(text,level=1):
    pp=doc.add_paragraph(text,style='Heading 1' if level==1 else 'Heading 2')
    fmt(pp,bold=True,align=WD_ALIGN_PARAGRAPH.CENTER if level==1 else WD_ALIGN_PARAGRAPH.LEFT,indent=0,line=1.2,after=7,before=0)
    pp.paragraph_format.keep_with_next=True
    return pp
def page(title):
    pp=heading(title);pp.paragraph_format.page_break_before=True
def caption(text):return p(text,size=12,align=WD_ALIGN_PARAGRAPH.CENTER,indent=0,line=1.0,after=7)
def fig(path,width=16,cap=None):
    pp=p('',indent=0,align=WD_ALIGN_PARAGRAPH.CENTER,line=1.0,after=3)
    shape=pp.add_run().add_picture(str(path),width=Cm(width))
    shape._inline.docPr.set('descr',cap or Path(path).stem)
    if cap:pp.paragraph_format.keep_with_next=True;caption(cap)
def eq(text):
    pp=p('',indent=0,align=WD_ALIGN_PARAGRAPH.CENTER,line=1.15,after=6,before=4)
    math=OxmlElement('m:oMath');r=OxmlElement('m:r');t=OxmlElement('m:t');t.text=text;r.append(t);math.append(r);pp._p.append(math)
    return pp
def table(headers,rows,widths=None,size=11.5,padding=45):
    tab=doc.add_table(rows=1,cols=len(headers));tab.alignment=WD_TABLE_ALIGNMENT.CENTER;tab.autofit=False
    if widths is None:widths=[17/len(headers)]*len(headers)
    for c,w in zip(tab.columns,widths):c.width=Cm(w)
    pr=tab._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'6');el.set(qn('w:color'),'D9D9D9');borders.append(el)
    pr.append(borders)
    margins=OxmlElement('w:tblCellMar')
    for k,v in [('top',padding),('bottom',padding),('left',65),('right',65)]:
        e=OxmlElement('w:'+k);e.set(qn('w:w'),str(v));e.set(qn('w:type'),'dxa');margins.append(e)
    pr.append(margins)
    for i,row in enumerate([headers]+rows):
        cells=tab.rows[0].cells if i==0 else tab.add_row().cells
        trpr=tab.rows[i]._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
        if i==0:trpr.append(OxmlElement('w:tblHeader'))
        for j,(c,txt) in enumerate(zip(cells,row)):
            c.width=Cm(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            c.text=str(txt);fmt(c.paragraphs[0],size=size,bold=i==0,indent=0,align=WD_ALIGN_PARAGRAPH.CENTER,line=1.0)
            if i==0:
                sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'EFEFEF');c._tc.get_or_add_tcPr().append(sh)
    p('',size=3,indent=0,line=1,after=2)
    return tab

heading('Мета роботи')
p('Ознайомитися з принципом дії, основними параметрами та характеристиками тригерів на логічних елементах і в інтегральному виконанні; дослідити таблиці станів, побудувати часові діаграми та отримати логічні рівняння їх роботи.')
heading('Теоретичні відомості',2)
p('Тригер зберігає один біт інформації. Його стан визначають прямий вихід Q та інверсний вихід /Q. У допустимому усталеному стані /Q = ¬Q. Перехресний зворотний зв’язок забезпечує збереження стану після зняття вхідного сигналу.')
p('RS-тригер має входи встановлення S і скидання R; D-тригер записує значення D; T-тригер перемикає стан; JK-тригер поєднує зберігання, встановлення, скидання й перемикання. Засувка реагує протягом активного рівня дозволу, а тригер із динамічним входом — лише на відповідний фронт такту.')
heading('Позначення та спосіб перевірки',2)
p('Qₙ — попередній стан; Qₙ₊₁ — наступний стан; ¬ — заперечення; ∧ — І; ∨ — АБО; ⊕ — виключне АБО. Запис /S, /R, /C на схемах позначає інверсний сигнал або вхід з активним нулем. X — довільне значення; * — заборонена комбінація.')
p('Для інтегральних моделей E↑ = 1 означає подію C: 0 → 1, E↓ = 1 — подію C: 1 → 0; E = 0 означає відсутність активного фронту. У таблицях методички ця умова спрощено позначена C = 1. Тут рівень C і подію E розрізнено, щоб правильно відобразити роботу пам’яті.')
p('Схеми відтворено у draw.io. Таблиці й ілюстрації перевірки отримано програмним перебором двійкових входів: для вентильних схем розв’язано рівняння зворотного зв’язку, для інтегральних — застосовано модель переходів. Це ідеальне логічне моделювання без затримок поширення, а не електрична симуляція Multisim.',size=13,line=1.25)

TITLES={1:'Асинхронний RS на АБО–НІ',2:'Асинхронний RS на І–НІ',3:'Інтегральний асинхронний RS',4:'Синхронний RS на АБО–НІ',5:'Синхронний RS на І–НІ',6:'Синхронний D на АБО–НІ',7:'Синхронний D на І–НІ',8:'Інтегральний D-тригер',9:'Асинхронний T на базі D',10:'Інтегральний JK-тригер',11:'Асинхронний T на базі JK',12:'Синхронний T на базі JK',13:'D-тригер на базі JK'}
EXPL={
1:'Два елементи АБО–НІ з’єднано перехресним зворотним зв’язком. Входи R і S активні одиницею. За R = S = 0 тригер зберігає попередній стан; за R = S = 1 обидва виходи дорівнюють нулю.',
2:'Два елементи І–НІ мають перехресний зворотний зв’язок. Входи /S і /R активні нулем. Комбінація 11 зберігає стан, а комбінація 00 є забороненою та примусово дає Q = /Q = 1.',
3:'Умовне позначення інтегрального RS містить асинхронні входи /R та /S. Функціонально це RS-засувка з активним нулем. Порядок входів у таблиці збережено як у табл. 3.3 методички: спочатку /R, потім /S.',
4:'У схемі з методички всі чотири елементи — АБО–НІ. Дозвіл /C активний нулем: за /C = 1 вузли Ra і Sa дорівнюють 0 та стан зберігається. За /C = 0 входи /R та /S керують засувкою.',
5:'Перші два елементи І–НІ формують /Sa = ¬(S ∧ C) і /Ra = ¬(R ∧ C). За C = 0 обидва проміжні сигнали дорівнюють 1, тому стан зберігається. За C = 1 входи S і R активні одиницею.',
6:'У схемі з методички R = ¬(D ∨ /C), S = ¬(R ∨ /C). За /C = 0 вихід Q повторює D; за /C = 1 — зберігається. Це засувка, прозора за низького рівня дозволу, а не тригер за фронтом.',
7:'Схема містить чотири елементи І–НІ: /S = ¬(D ∧ C), /R = ¬(/S ∧ C). За C = 1 вихід Q повторює D, за C = 0 — зберігається. У сталих допустимих режимах заборонена комбінація не виникає.',
8:'Модель D-тригера записує D на наростальному фронті C. Асинхронні входи /S і /R мають пріоритет над D та C. Такий принцип відповідає SN74LS74A; таблицю виробника наведено в джерелі [2].',
9:'Інверсний вихід /Q під’єднано до D, а імпульси T подано на тактовий вхід C. На кожному наростальному фронті T записується ¬Q. Назва «асинхронний T» тут означає відсутність окремого входу синхронізації.',
10:'JK за C↓: 00 — пам’ять, 01 — скидання, 10 — встановлення, 11 — перемикання. Асинхронні /S і /R мають пріоритет. Приклад — SN74LS112A [3].',
11:'На входи J і K подано логічну 1, а імпульси T — на C. Кожний спадний фронт T інвертує Q. Тривале утримання T = 1 не викликає повторних перемикань у тригері з динамічним входом.',
12:'Входи J і K об’єднано та під’єднано до T. На спадному фронті C за T = 0 стан зберігається, а за T = 1 — інвертується. Між активними фронтами вихід не змінюється.',
13:'На J подано D, а на K — ¬D через інвертор. Тоді на спадному фронті C вихід приймає D. Для інвертора в базисі І–НІ можна об’єднати два входи одного NAND; на схемі показано його функціональний символ.'}
FORM={1:'Qₙ₊₁ = S ∨ (¬R ∧ Qₙ),   R ∧ S = 0',2:'Qₙ₊₁ = ¬s̄ ∨ (r̄ ∧ Qₙ),   (s̄, r̄) ≠ (0, 0)',3:'Qₙ₊₁ = ¬s̄ ∨ (r̄ ∧ Qₙ),   (r̄, s̄) ≠ (0, 0)',4:'Qₙ₊₁ = c̄Qₙ ∨ ¬c̄(¬s̄ ∨ r̄Qₙ)',5:'Qₙ₊₁ = ¬C Qₙ ∨ C(S ∨ ¬R Qₙ)',6:'Qₙ₊₁ = c̄Qₙ ∨ ¬c̄D',7:'Qₙ₊₁ = ¬C Qₙ ∨ CD',8:'Qₙ₊₁ = ¬E↑ Qₙ ∨ E↑ D',9:'Qₙ₊₁ = Qₙ ⊕ EТ↑',10:'Qₙ₊₁ = ¬E↓ Qₙ ∨ E↓(J¬Qₙ ∨ ¬K Qₙ)',11:'Qₙ₊₁ = Qₙ ⊕ EТ↓',12:'Qₙ₊₁ = Qₙ ⊕ (E↓ ∧ T)',13:'Qₙ₊₁ = ¬E↓ Qₙ ∨ E↓ D'}

def build_rows(n):
    rows=[]
    if n<=3:
        heads=(['R','S'] if n==1 else ['/S','/R'] if n==2 else ['/R','/S'])+['Qₙ','Qₙ₊₁','/Qₙ₊₁','Режим']
        for q in [0,1]:
            for u,v in product([0,1],repeat=2):
                out=A.actual(n,(u,v),q);bad=out[0]==out[1]
                s,r=(v,u) if n==1 else ((u,v) if n==2 else (v,u))
                hold=(u==v==(0 if n==1 else 1))
                mode='заборонено' if bad else 'зберігання' if hold else 'встановлення' if out[0] else 'скидання'
                rows.append([u,v,q,str(out[0])+('*' if bad else ''),str(out[1])+('*' if bad else ''),mode])
        return heads,rows,[1.5,1.5,1.7,2,2.2,8.1]
    if n in [4,5]:
        heads=(['/C','/R','/S','Ra','Sa'] if n==4 else ['C','S','R','/Sa','/Ra'])+['Qₙ','Qₙ₊₁','/Qₙ₊₁']
        for c in ([1,0] if n==4 else [0,1]):
            for q in [0,1]:
                for u,v in product([0,1],repeat=2):
                    a,b=(1-(u|c),1-(v|c)) if n==4 else (1-(u&c),1-(v&c))
                    val,bar=A.actual(n,(c,u,v),q);star='*' if val==bar else ''
                    rows.append([c,u,v,a,b,q,str(val)+star,str(bar)+star])
        return heads,rows,None
    if n in [6,7]:
        heads=(['/C','D','R','S'] if n==6 else ['C','D','/S','/R'])+['Qₙ','Qₙ₊₁','/Qₙ₊₁']
        for q in [0,1]:
            for c in ([1,0] if n==6 else [0,1]):
                for d in [0,1]:
                    a=1-(d|c) if n==6 else 1-(d&c);b=1-(a|c) if n==6 else 1-(a&c)
                    val,bar=A.actual(n,(c,d),q);rows.append([c,d,a,b,q,val,bar])
        return heads,rows,None
    dataheads=['E↑','D'] if n==8 else ['EТ↑'] if n==9 else ['E↓','J','K'] if n==10 else ['EТ↓'] if n==11 else ['E↓','T'] if n==12 else ['E↓','D']
    heads=['/S','/R']+dataheads+['Qₙ','Qₙ₊₁','/Qₙ₊₁']
    for s,r,val,bar in [(0,0,'1*','1*'),(0,1,1,0),(1,0,0,1)]:rows.append([s,r]+['X']*len(dataheads)+['X',val,bar])
    for q in [0,1]:
        for data in product([0,1],repeat=len(dataheads)):
            val,bar=A.actual(n,(1,1)+data,q);rows.append([1,1]+list(data)+[q,val,bar])
    return heads,rows,None

for n in range(1,14):
    page(f'3.{n} {TITLES[n]}')
    p(EXPL[n],size=13,line=1.15,after=5)
    fig(A.SCHEMES[n],width=12.3 if n==10 else 13.2 if n in [4,5] else 14.8,cap=f'Рисунок 3.{n} — {TITLES[n]}')
    cap=p(f'Таблиця 3.{n} — Стани та переходи',size=12,indent=0,line=1,after=4);cap.paragraph_format.keep_with_next=True
    heads,rows,widths=build_rows(n);table(heads,rows,widths,size=11 if n==10 else 11.5,padding=25 if n==10 else 35 if n in [4,5] else 45)
    eq(FORM[n])
    if n in [2,3,4,6]:
        note='У рівнянні c̄ — значення входу /C.' if n==6 else 'У рівнянні s̄ і r̄ — значення входів /S та /R.' if n in [2,3] else 'У рівнянні s̄, r̄, c̄ — значення входів /S, /R, /C відповідно.'
        p(note,size=11.5,indent=0,line=1,after=4)
    if n>=8:p('Рівняння діє за /S = /R = 1; інші режими визначає верхня частина таблиці.',size=11.5,indent=0,line=1,after=4)
    fig(A.ASSETS/f'check_{n:02}.png',width=16.6)
    p(f'Перевірено {A.CHECKS[n]} комбінацій входів і попереднього стану; розбіжностей між моделлю та рівняннями немає. Приклади вище — незалежні випробування.',size=11.5,indent=0,line=1.0)

page('Часові діаграми асинхронних RS-тригерів')
p('Початковий стан Q = 0. Кожний інтервал між вертикальними лініями — одна умовна одиниця часу; числа внизу — номери інтервалів. Реальні затримки вентилів не враховано. Заборонені комбінації не подаються.')
fig(A.ASSETS/'time_1.png',16.8,'Рисунок 3.14 — RS на АБО–НІ з активними одиницею входами')
fig(A.ASSETS/'time_2.png',16.8,'Рисунок 3.15 — RS на І–НІ з активними нулем входами')
p('На інтервалі 1 команда встановлення переводить Q у 1. На інтервалі 3 команда скидання повертає Q у 0. За пасивних входів вихід зберігає попереднє значення. Інверсія обох керувальних сигналів дає однакову послідовність Q для двох базисів.')

page('Часові діаграми синхронних RS-тригерів')
p('Початковий стан Q = 0. На діаграмах подано еквівалентні команди; у схемі АБО–НІ дозвіл і керувальні входи інверсні. Зміна входу під час заборони запису не впливає на Q.')
fig(A.ASSETS/'time_3.png',16.8,'Рисунок 3.16 — RS на АБО–НІ відкритий за /C = 0')
fig(A.ASSETS/'time_4.png',16.8,'Рисунок 3.17 — RS на І–НІ відкритий за C = 1')
p('Команда встановлення на інтервалі 1 ігнорується, бо запис закрито; на інтервалі 2 вона виконується. Команда скидання на інтервалі 4 виконується лише після дозволу на інтервалі 5. Обидві схеми формують однаковий вихід Q.')

page('Часові діаграми D- і T-тригерів')
p('Для D початковий стан Q = 0. На одному рисунку порівняно D-засувку на І–НІ та інтегральний D-тригер за C↑. Для засувки на АБО–НІ достатньо замінити C на /C = ¬C.')
fig(A.ASSETS/'time_5.png',16.8,'Рисунок 3.18 — Запис D за рівнем і за наростальним фронтом')
p('На інтервалах 3, 7 і 11 D змінюється при C = 1: засувка реагує, а тригер за фронтом утримує записане значення. Перед активними фронтами дані стабільні.',size=13,line=1.2)
fig(A.ASSETS/'time_6.png',16.8,'Рисунок 3.19 — Синхронний T з дозволом перемикання T')
p('На спадному фронті C вихід змінюється лише за T = 1. За T = 0, а також між фронтами, стан зберігається. Асинхронні входи /S і /R неактивні та дорівнюють 1.',size=13,line=1.2)

page('Часові діаграми JK та лічильних T-тригерів')
fig(A.ASSETS/'time_7.png',16.8,'Рисунок 3.20 — Послідовність режимів JK 00, 10, 01, 11, 11')
p('На спадних фронтах C (інтервали 3, 7, 11, 15, 19) отримано Q = 0, 1, 0, 1, 0. Отже, послідовно перевірено зберігання, встановлення, скидання та два перемикання. Початковий стан Q = 0.',size=13,line=1.2)
fig(A.ASSETS/'time_8.png',16.8,'Рисунок 3.21 — T на D реагує на T↑, а T на JK — на T↓')
p('Кожний активний фронт вхідних імпульсів змінює стан один раз. Період Q удвічі більший за період T, тому частота виходу fQ = fT / 2. Зсув діаграм зумовлений різними активними фронтами.',size=13,line=1.2)

page('Отримання логічних рівнянь RS-тригерів')
p('Для мінімізації використано таблицю 3.1. Заборонені набори R = S = 1 позначено знаком * і використано як невизначені значення лише під час мінімізації функції. Робоче рівняння застосовне за умови R ∧ S = 0.')
caption('Таблиця 3.14 — Скорочена таблиця асинхронного RS')
table(['R','S','Qₙ','Qₙ₊₁'],[[r,s,q,'*' if r&s else s|((1-r)&q)] for r,s,q in product([0,1],repeat=3)],size=12)
caption('Таблиця 3.15 — Карта Карно для RS у коді Грея')
table(['Qₙ \\ RS','00','01','11','10'],[['0','0','1','*','0'],['1','1','1','*','0']],size=12)
p('Одиниці у стовпці RS = 01 разом із невизначеним стовпцем 11 утворюють групу S. Пара клітин нижнього рядка у стовпцях 00 і 01 дає ¬R ∧ Qₙ. Сума цих імплікант визначає мінімальну функцію.',size=13,line=1.25)
eq('Qₙ₊₁ = S ∨ (¬R ∧ Qₙ)')
p('Для входів, активних нулем, підставляємо S = ¬s̄ та R = ¬r̄:')
eq('Qₙ₊₁ = ¬s̄ ∨ (r̄ ∧ Qₙ)')
p('Для синхронного RS за активного дозволу C підставляємо Sа = C ∧ S і Rа = C ∧ R. Скорочена форма:')
eq('Qₙ₊₁ = CS ∨ Qₙ¬(CR) = CS ∨ Qₙ(¬C ∨ ¬R)')
p('За C = 0 маємо Qₙ₊₁ = Qₙ; за C = 1 — рівняння асинхронного RS. Обмеження: C ∧ S ∧ R = 0. Для схеми 3.4 замінюємо C, S, R на ¬c̄, ¬s̄, ¬r̄ відповідно.',size=13,line=1.25)

page('Отримання логічних рівнянь D- і T-тригерів')
heading('D-тригер',2)
p('Підстановка S = D, R = ¬D у рівняння RS дає D ∨ DQₙ = D. Отже, умовна асинхронна D-схема без дозволу має Qₙ₊₁ = D і не зберігає незалежний від входу стан. Пам’ять забезпечує керування дозволом або фронтом такту.',size=13,line=1.25)
caption('Таблиця 3.16 — Карта Карно синхронної D-засувки')
table(['Qₙ \\ CD','00','01','11','10'],[['0','0','0','1','0'],['1','1','1','1','0']],size=12)
p('Група стовпця CD = 11 дає CD; пара нижніх клітин 00 і 01 дає ¬C Qₙ. Отримуємо:')
eq('Qₙ₊₁ = CD ∨ ¬C Qₙ')
p('Для активного нулем дозволу: Qₙ₊₁ = ¬c̄D ∨ c̄Qₙ. Для запису за фронтом C замість рівня C використовують подію E↑ або E↓.',size=13,line=1.25)
heading('T-тригер',2)
caption('Таблиця 3.17 — Карта Карно функції перемикання')
table(['Qₙ \\ T','0','1'],[['0','0','1'],['1','1','0']],widths=[5.6,5.7,5.7],size=12)
p('Дві окремі одиниці відповідають ¬TQₙ та T¬Qₙ, тому:')
eq('Qₙ₊₁ = ¬T Qₙ ∨ T ¬Qₙ = Qₙ ⊕ T')
p('У лічильному асинхронному T під T у цій таблиці розуміють факт приходу активного імпульсу EТ, а не постійний високий рівень. Для синхронного T перемикання дозволене лише за збігу активного фронту та T = 1:',size=13,line=1.25)
eq('Qₙ₊₁ = Qₙ ⊕ EТ;    Qₙ₊₁ = Qₙ ⊕ (E ∧ T)')
p('Для одноразового синхронного переходу часто пишуть Qₙ₊₁ = ¬C Qₙ ∨ C(T ⊕ Qₙ), де C позначає дозвіл переходу. У часових діаграмах фронтових тригерів його уточнено як E.',size=13,line=1.25)

page('Отримання логічного рівняння JK-тригера')
caption('Таблиця 3.18 — Карта Карно JK на активному фронті')
table(['Qₙ \\ JK','00','01','11','10'],[['0','0','0','1','1'],['1','1','0','0','1']],size=12)
p('У верхньому рядку пара клітин JK = 11 і 10 утворює J¬Qₙ. У нижньому рядку крайні стовпці 00 і 10 сусідні за кодом Грея та утворюють ¬KQₙ. Отже:')
eq('FJK = J¬Qₙ ∨ ¬KQₙ')
p('З урахуванням відсутності активного фронту:')
eq('Qₙ₊₁ = ¬E Qₙ ∨ E(J¬Qₙ ∨ ¬KQₙ)')
p('Для JK на рис. 3.10 використано E = E↓. За J = K = 1 маємо Qₙ₊₁ = ¬Qₙ на кожному спадному фронті. Забороненої інформаційної комбінації JK немає.')
heading('Перетворення JK у D і T',2)
eq('J = D, K = ¬D ⇒ FJK = D¬Qₙ ∨ DQₙ = D')
eq('J = K = T ⇒ FJK = T¬Qₙ ∨ ¬TQₙ = T ⊕ Qₙ')
eq('J = K = 1 ⇒ FJK = ¬Qₙ')
heading('Пріоритет асинхронного керування',2)
p('Наведені рівняння фронтових тригерів справедливі, коли /S = /R = 1. За /S = 0, /R = 1 вихід негайно встановлюється в 1; за /S = 1, /R = 0 — скидається в 0. За /S = /R = 0 у розглянутих моделях обидва виходи примусово дорівнюють 1.')
p('Зірочка в таблицях означає заборону режиму, а не випадковий рівень під час утримання входів. Невизначеність можливого кінцевого стану виникає після одночасного зняття забороненої комбінації. У реальній схемі це може супроводжуватися метастабільністю.')
p(f'Загальна перевірка охопила {sum(A.CHECKS.values())} комбінацій входів і початкового стану для 13 схем. Булеві рівняння збіглися з результатами моделі в усіх допустимих режимах; примусові рівні заборонених режимів перевірено окремими умовами.',size=13,line=1.25)

QA=[
('Чим відрізняються тригери на І–НІ та АБО–НІ?','У базової RS-засувки АБО–НІ активні входи 1, режим пам’яті 00, заборонено 11. У базової RS-засувки І–НІ активні входи 0, пам’ять 11, заборонено 00. Див. схеми й таблиці 3.1 та 3.2.'),
('Чим відрізняються асинхронні та синхронні тригери?','Асинхронні змінюють стан у відповідь на керувальні входи без окремого дозволу C. Синхронні виконують інформаційний перехід під час активного рівня або фронту C. Асинхронні входи встановлення й скидання можуть існувати і в синхронних тригерах.'),
('Таблиця та рівняння асинхронного RS','Для RS = 00 вихід зберігається, 01 встановлює 1, 10 скидає 0, 11 заборонено. Qₙ₊₁ = S ∨ ¬RQₙ, R ∧ S = 0. Повний перебір наведено в табл. 3.1, скорочений — у табл. 3.14.'),
('Структурна схема RS у базисі І–НІ','Q = NAND(/S, /Q), /Q = NAND(/R, Q). Вихід кожного елемента під’єднано до другого входу іншого. За прямих S та R перед ними потрібні інвертори. Графічна схема — рис. 3.2.'),
('Структурна схема RS у базисі АБО–НІ','Q = NOR(R, /Q), /Q = NOR(S, Q). Два елементи мають перехресний зворотний зв’язок; графічна схема — рис. 3.1.'),
('Таблиця та рівняння синхронного RS','За C = 0 стан зберігається для всіх S, R. За C = 1 діє таблиця асинхронного RS: 00 — пам’ять, 01 — скидання, 10 — встановлення, 11 — заборона при порядку S,R. Qₙ₊₁ = CS ∨ Qₙ(¬C ∨ ¬R). Див. табл. 3.4–3.5.'),
('Синхронний RS у базисі І–НІ','Формують /Sa = NAND(S, C), /Ra = NAND(R, C), які подають на RS-засувку з двох NAND. Схема складається з чотирьох елементів І–НІ, див. рис. 3.5.'),
('Синхронний RS у базисі АБО–НІ','У позначеннях методички Ra = NOR(/R, /C), Sa = NOR(/S, /C); ними керують NOR-засувкою. Дозвіл активний нулем. Див. рис. 3.4.'),
('Таблиця та рівняння синхронного D','Для CD = 00 або 01 маємо Qₙ₊₁ = Qₙ; для 10 — 0; для 11 — 1. Рівняння засувки Qₙ₊₁ = CD ∨ ¬CQₙ. У фронтовій моделі замінюємо C на E. Див. табл. 3.6–3.8.'),
('D у базисі І–НІ','/S = NAND(D, C), /R = NAND(/S, C); далі — перехресно з’єднана NAND-засувка. За C = 1 маємо /S = ¬D та /R = D. Див. рис. 3.7.'),
('D у базисі АБО–НІ','R = NOR(D, /C), S = NOR(R, /C); далі — NOR-засувка. За /C = 0 маємо R = ¬D, S = D. Див. рис. 3.6.'),
('Як побудувати часову діаграму?','Спочатку задають Q₀ та вхідні сигнали. На кожній зміні входу або активному фронті визначають наступний стан з таблиці, враховуючи асинхронний пріоритет. Між дозволеними подіями зберігають Q; інверсний вихід будують як ¬Q у допустимих режимах.'),
('Приклади промислових D-тригерів і позначення','SN74LS74A — TTL LS, SN74HC74 — CMOS HC, CD4013B — CMOS 4000. Усі містять два D-тригери за C↑. Перші два мають активні нулем PRE/CLR; CD4013B — активні одиницею SET/RESET. Позначення: блок D, вхід D, трикутник на C, виходи Q та /Q; активні нулем входи позначають кружками, як на рис. 3.8. Джерела [2], [4], [5].'),
('Таблиця та рівняння асинхронного T','Без активного імпульсу EТ = 0 вихід зберігається; за EТ = 1 інвертується. Для пар EТ,Qₙ = 00, 01, 10, 11 результати 0, 1, 1, 0. Qₙ₊₁ = Qₙ ⊕ EТ. Див. табл. 3.9 та 3.11.'),
('Структурна схема асинхронного T','У D-тригера з’єднують D з /Q та подають T на C. У JK-тригера встановлюють J = K = 1, а T подають на C. Обидві схеми потребують фронтового перемикання; див. рис. 3.9 та 3.11.'),
('Таблиця та рівняння синхронного T','За E = 0 або T = 0 маємо Qₙ₊₁ = Qₙ. За E = 1, T = 1 — Qₙ₊₁ = ¬Qₙ. Загалом Qₙ₊₁ = Qₙ ⊕ (ET). Повна таблиця — 3.12.'),
('Структурна схема синхронного T','З’єднують J = K = T, тактовий сигнал подають на C; /S = /R = 1. На активному фронті за T = 1 відбувається один перехід. Див. рис. 3.12.'),
('Як побудувати T на основі RS і D?','Для RS використовують S = T¬Q, R = TQ у двоступеневій або фронтовій структурі. Для D із дозволом перемикання задають D = T ⊕ Q; для лічильного T без окремого дозволу — D = ¬Q та імпульси T на C. Простий прозорий RS зі зворотним зв’язком не гарантує одного перемикання.'),
('Чому JK називають універсальним?','Вибором J і K отримують зберігання, встановлення, скидання та перемикання. З’єднання J = D, K = ¬D дає D; J = K = T дає T; J = S, K = R за SR = 0 відтворює функцію RS на активному фронті.'),
('Призначення входів /S та /R у JK','Це асинхронні встановлення PRE/SET і скидання CLR/RESET. Активний нуль негайно задає Q незалежно від J, K та C. Обидва входи одночасно активувати не можна; за нормальної роботи їх утримують у 1.'),
('Як побудувати JK на базі RS?','Формують збудження S = J¬Q, R = KQ та керують ними через тактовий ступінь. Для усунення багаторазового перемикання при J = K = 1 застосовують два RS-ступені master–slave з протифазним керуванням або еквівалентну фронтову структуру.'),
('Таблиця та рівняння JK','На активному фронті JK = 00 дає Qₙ, 01 — 0, 10 — 1, 11 — ¬Qₙ. Без активного фронту стан зберігається. FJK = J¬Qₙ ∨ ¬KQₙ; з урахуванням події: Qₙ₊₁ = ¬EQₙ ∨ EFJK. Див. табл. 3.10.'),
('Часові діаграми JK','На рис. 3.20 послідовно задано 00, 10, 01, 11, 11. За Q₀ = 0 після п’яти спадних фронтів отримано 0, 1, 0, 1, 0. Ця послідовність узгоджується з усіма чотирма режимами таблиці станів.'),
('Як побудувати T на базі JK?','Для лічильного варіанта J = K = 1, T подають на C. Для синхронного варіанта J = K = T, а на C подають окремий тактовий сигнал. Див. рис. 3.11 і 3.12.'),
('Як побудувати D на базі JK?','З’єднати J з D, а K з виходом інвертора D. На активному фронті FJK = D¬Q ∨ DQ = D, тому наступний стан дорівнює вхідному біту. Див. рис. 3.13.'),
('Чи можна замінити синхронний RS на JK?','Так, якщо J = S, K = R, комбінація S = R = 1 не використовується та узгоджені полярність, спосіб синхронізації, асинхронні входи й часові вимоги. Фронтовий JK не є прямою заміною прозорої RS-засувки: зміни входів протягом активного рівня обробляються по-різному.')]

for start,end in [(0,6),(6,12),(12,18),(18,26)]:
    page(f'Відповіді на контрольні запитання {start+1}–{end}')
    for i in range(start,end):
        title,answer=QA[i]
        pp=p(f'{i+1}. {title}',size=13,bold=True,indent=0,line=1.1,after=3,before=4);pp.paragraph_format.keep_with_next=True
        p(answer,size=13,indent=1.0,line=1.15,after=5)

page('Висновки')
p('Досліджено 13 схем RS-, D-, T- і JK-тригерів. Таблиці станів підтверджують збереження біта завдяки зворотному зв’язку, запис інформації у дозволені моменти та пріоритет асинхронного встановлення і скидання.')
p('RS-засувки на АБО–НІ та І–НІ відрізняються активними рівнями входів і забороненими комбінаціями. Для синхронних схем з методички дозвіл на АБО–НІ активний нулем, а на І–НІ — одиницею. D-засувка повторює вхід протягом активного рівня, тоді як інтегральний D-тригер записує його лише на фронті.')
p('T-тригер перемикає стан і ділить частоту імпульсів на два. JK-тригер є універсальним: з’єднанням його входів отримано D- і T-функції. Виведені рівняння та часові діаграми узгоджуються з таблицями станів; логічний перебір не виявив розбіжностей.')
p('Під час практичного складання потрібно виключати заборонені комбінації, задавати початковий стан і дотримуватися часу встановлення та утримання даних. Логічна модель описує послідовність станів, але не визначає реальні затримки, рівні напруг і граничну частоту мікросхеми.')
heading('Використані джерела',2)
refs=[
'1. ЛР3_КМАДО. Лабораторна робота № 3 «Дослідження тригерів на логічних елементах». Методичні вказівки, надані до роботи.',
'2. Texas Instruments. SN74LS74A — Dual D-Type Positive-Edge-Triggered Flip-Flops With Preset And Clear. https://www.ti.com/lit/ds/symlink/sn74ls74a.pdf',
'3. Texas Instruments. SN74LS112A — Dual J-K Negative-Edge-Triggered Flip-Flops With Preset And Clear. https://www.ti.com/lit/ds/symlink/sn74ls112a.pdf',
'4. Texas Instruments. SN74HC74 — Dual D-Type Positive-Edge-Triggered Flip-Flops With Clear and Preset. https://www.ti.com/product/SN74HC74',
'5. Texas Instruments. CD4013B — CMOS Dual D-Type Flip-Flop. https://www.ti.com/product/CD4013B']
for ref in refs:p(ref,size=11.5,indent=0,line=1.05,after=5)

# Save via python-docx, then retain all opaque source parts byte-for-byte.
temp=B/'authored.docx';doc.save(temp)
nsrel='http://schemas.openxmlformats.org/package/2006/relationships';nsct='http://schemas.openxmlformats.org/package/2006/content-types'
with ZipFile(SRC) as zin,ZipFile(temp) as znew:
    orig={n:zin.read(n) for n in zin.namelist()};new={n:znew.read(n) for n in znew.namelist()}
    oldrels=etree.fromstring(orig['word/_rels/document.xml.rels']);newrels=etree.fromstring(new['word/_rels/document.xml.rels'])
    ids={x.get('Id') for x in oldrels}
    for x in newrels:
        if x.get('Id') not in ids:oldrels.append(x)
    oldstyles=etree.fromstring(orig['word/styles.xml']);newstyles=etree.fromstring(new['word/styles.xml'])
    styleids={x.get(qn('w:styleId')) for x in oldstyles}
    for x in newstyles:
        if x.get(qn('w:styleId')) not in styleids:oldstyles.append(x)
    orig['word/styles.xml']=etree.tostring(oldstyles,xml_declaration=True,encoding='UTF-8',standalone=True)
    oldct=etree.fromstring(orig['[Content_Types].xml']);newct=etree.fromstring(new['[Content_Types].xml'])
    keys={(x.tag,x.get('Extension') or x.get('PartName')) for x in oldct}
    for x in newct:
        if (x.tag,x.get('Extension') or x.get('PartName')) not in keys:oldct.append(x)
    orig['word/document.xml']=new['word/document.xml']
    orig['word/_rels/document.xml.rels']=etree.tostring(oldrels,xml_declaration=True,encoding='UTF-8',standalone=True)
    orig['[Content_Types].xml']=etree.tostring(oldct,xml_declaration=True,encoding='UTF-8',standalone=True)
    for name,data in new.items():
        if name not in orig:orig[name]=data
    with ZipFile(FINAL,'w',ZIP_DEFLATED) as zout:
        for name,data in orig.items():zout.writestr(name,data)

allow={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml','word/styles.xml'}
baseline=json.loads((B/'template-parts.json').read_text(encoding='utf8'))
with ZipFile(FINAL) as z:
    for name,info in baseline.items():
        if name not in allow:assert sha256(z.read(name)).hexdigest()==info['sha256'],name
assert sha256(SRC.read_bytes()).hexdigest()==original_hash
assert len(Document(FINAL).sections)==1
print(FINAL)
print('Tables:',len(doc.tables),'Images:',len(doc.inline_shapes),'All preserved template parts match.')
