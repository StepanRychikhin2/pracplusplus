from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from xml.etree import ElementTree as ET
from itertools import product
import json

BASE=Path(__file__).resolve().parent
OUT=BASE.parent
ASSETS=BASE/'assets'; ASSETS.mkdir(exist_ok=True)
FONT='C:/Windows/Fonts/arial.ttf'
BOLD='C:/Windows/Fonts/arialbd.ttf'
MX=ET.Element('mxfile',host='app.diagrams.net',version='24.7.17')

class Diagram:
    def __init__(self,name,w=900,h=320):
        self.name=name; self.w=w; self.h=h; self.i=2
        self.im=Image.new('RGB',(w*3,h*3),'white'); self.d=ImageDraw.Draw(self.im)
        dg=ET.SubElement(MX,'diagram',name=name,id=f'd{len(MX)+1}')
        model=ET.SubElement(dg,'mxGraphModel',dx='900',dy='600',grid='1',gridSize='10',page='1',pageWidth=str(w),pageHeight=str(h))
        self.root=ET.SubElement(model,'root'); ET.SubElement(self.root,'mxCell',id='0'); ET.SubElement(self.root,'mxCell',id='1',parent='0')
    def cell(self,value,style,x,y,w,h):
        c=ET.SubElement(self.root,'mxCell',id=str(self.i),parent='1',value=value,style=style,vertex='1');self.i+=1
        ET.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),attrib={'as':'geometry'})
    def text(self,x,y,s,size=21,bold=False,anchor='mm'):
        self.d.text((x*3,y*3),s,fill='black',font=ImageFont.truetype(BOLD if bold else FONT,int(size*3)),anchor=anchor)
        width=max(size,len(s)*size*.58)
        xx=x-width/2 if anchor[0]=='m' else (x-width if anchor[0]=='r' else x)
        self.cell(s,f'text;html=0;strokeColor=none;fillColor=none;fontFamily=Arial;fontSize={size};fontStyle={1 if bold else 0};align=center;verticalAlign=middle;',xx,y-size*.75,width,size*1.5)
    def line(self,*pts,color='#222222',width=2):
        self.d.line([(int(x*3),int(y*3)) for x,y in pts],fill=color,width=width*3,joint='curve')
        c=ET.SubElement(self.root,'mxCell',id=str(self.i),parent='1',edge='1',style=f'endArrow=none;html=0;strokeColor={color};strokeWidth={width};rounded=0;');self.i+=1
        g=ET.SubElement(c,'mxGeometry',relative='1',attrib={'as':'geometry'})
        ET.SubElement(g,'mxPoint',x=str(pts[0][0]),y=str(pts[0][1]),attrib={'as':'sourcePoint'})
        ET.SubElement(g,'mxPoint',x=str(pts[-1][0]),y=str(pts[-1][1]),attrib={'as':'targetPoint'})
        if len(pts)>2:
            a=ET.SubElement(g,'Array',attrib={'as':'points'})
            for x,y in pts[1:-1]:ET.SubElement(a,'mxPoint',x=str(x),y=str(y))
    def rect(self,x,y,w,h,fill='white'):
        self.d.rectangle((x*3,y*3,(x+w)*3,(y+h)*3),outline='black',fill=fill,width=6)
        self.cell('',f'rounded=0;whiteSpace=wrap;html=0;fillColor={fill};strokeColor=#000000;strokeWidth=2;',x,y,w,h)
    def dot(self,x,y,r=4,open=False):
        self.d.ellipse(((x-r)*3,(y-r)*3,(x+r)*3,(y+r)*3),fill='white' if open else 'black',outline='black',width=5)
        self.cell('',f'ellipse;html=0;fillColor={"#FFFFFF" if open else "#000000"};strokeColor=#000000;strokeWidth=1.5;',x-r,y-r,2*r,2*r)
    def gate(self,x,y,kind):
        self.rect(x,y,85,75);self.text(x+42,y+37,'≥1' if kind=='nor' else '&',size=27)
        self.dot(x+90,y+37,5,True)
        return (x,y+18),(x,y+57),(x+95,y+37)
    def save(self,stem):
        p=ASSETS/f'{stem}.png';self.im.save(p);return p

def rs_core(d,kind,x=520):
    a,b,o=d.gate(x,30,kind); c,e,p=d.gate(x,200,kind)
    d.line(o,(x+150,67),(x+150,123),(x-30,178),c)
    d.line(p,(x+150,237),(x+150,181),(x-30,126),b)
    d.line(o,(x+230,67));d.line(p,(x+230,237))
    d.dot(x+150,67);d.dot(x+150,237)
    d.text(x+245,67,'Q',anchor='lm');d.text(x+245,237,'/Q',anchor='lm')
    return a,e

def gate_diagram(n,kind,gated=False,data=False):
    d=Diagram(f'3.{n} '+('D' if data else 'RS')+' '+('АБО–НІ' if kind=='nor' else 'І–НІ'))
    a,b=rs_core(d,kind,520 if gated else 350)
    if not gated:
        labs=['R','S'] if kind=='nor' else ['/S','/R']
        for pt,lab in zip([a,b],labs):d.line((140,pt[1]),pt);d.text(120,pt[1],lab,anchor='rm')
    else:
        p1,p2,o1=d.gate(250,30,kind);p3,p4,o2=d.gate(250,200,kind)
        d.line(o1,(435,67),(435,a[1]),a);d.line(o2,(435,237),(435,b[1]),b)
        labs=(['R','S'] if kind=='nor' else ['/S','/R']) if data else (['Ra','Sa'] if kind=='nor' else ['/Sa','/Ra'])
        d.text(405,29,labs[0],size=20);d.text(405,275,labs[1],size=20)
        d.line((100,152),(205,152),(205,p2[1]),p2)
        d.line((205,152),(205,p4[1]),p4);d.dot(205,152)
        d.text(85,152,'/C' if kind=='nor' else 'C',anchor='rm')
        d.line((100,p1[1]),p1);d.text(85,p1[1],'D' if data else ('/R' if kind=='nor' else 'S'),anchor='rm')
        if data:
            d.line((375,67),(375,125),(225,185),(225,p3[1]),p3);d.dot(375,67)
        else:
            d.line((100,p3[1]),p3);d.text(85,p3[1],'/S' if kind=='nor' else 'R',anchor='rm')
    d.text(450,306,'Кружок — інверсія; крапка — електричне з’єднання',size=17)
    return d.save(f'scheme_{n:02}')

def integral(n,kind,mode='normal'):
    d=Diagram(f'3.{n} {kind} {mode}',900,320)
    x=400;y=30;w=180;h=240
    d.rect(x,y,w,h);d.text(x+92,50,kind,22,True)
    d.line((x+55,y),(x+55,y+h));d.line((x+130,y),(x+130,y+h))
    pins={'/R':65,'/S':245}
    if kind=='D':pins.update({'D':115,'C':180})
    if kind=='JK':pins.update({'J':105,'C':155,'K':205})
    for lab,yy in pins.items():
        active=lab.startswith('/')
        d.text(x+27,yy,lab[1:] if active else lab,18)
        if active:d.dot(x-5,yy,5,True)
        if lab=='C':
            d.line((x,yy-9),(x+12,yy),(x,yy+9))
            if kind=='JK':d.dot(x-5,yy,5,True)
        if active:
            d.line((x-70,yy),(x-10,yy));d.text(x-80,yy,lab+' = 1' if mode!='normal' else lab,18,anchor='rm')
    d.text(x+155,105,'Q',19);d.text(x+155,205,'Q',19);d.dot(x+w+5,205,5,True)
    d.line((x+w,105),(750,105));d.line((x+w+10,205),(750,205));d.text(770,105,'Q',21);d.text(775,205,'/Q',21)
    if kind=='RS': pass
    elif mode=='normal':
        for lab in (['D','C'] if kind=='D' else ['J','C','K']):
            yy=pins[lab];d.line((180,yy),(x-(10 if lab=='C' and kind=='JK' else 0),yy));d.text(160,yy,lab,21,anchor='rm')
    elif mode=='T_from_D':
        d.line((650,205),(650,295),(220,295),(220,115),(x,115));d.dot(650,205)
        d.line((180,180),(x,180));d.text(160,180,'T',21,anchor='rm')
    elif mode in ['T_async','T_sync']:
        d.line((180,105),(x,105));d.line((285,105),(285,205),(x,205));d.dot(285,105)
        d.text(160,105,'1' if mode=='T_async' else 'T',21,anchor='rm')
        d.line((180,155),(x-10,155));d.text(160,155,'T' if mode=='T_async' else 'C',21,anchor='rm')
    elif mode=='D_from_JK':
        d.line((180,105),(x,105));d.dot(245,105);d.line((245,105),(245,205),(270,205))
        d.rect(270,180,55,50);d.text(297,205,'1',22);d.dot(330,205,5,True);d.line((335,205),(x,205))
        d.line((180,155),(x-10,155));d.text(160,105,'D',21,anchor='rm');d.text(160,155,'C',21,anchor='rm')
    if kind=='RS':
        d.text(450,300,'Асинхронні входи /R та /S активні нулем',17)
    elif mode!='T_from_D':d.text(450,302,'Запис: C↑' if kind=='D' else 'Запис: C↓',18)
    return d.save(f'scheme_{n:02}')

def latch(kind,u,v,q):
    # u drives the gate producing Q; v drives the gate producing /Q.
    op=(lambda a,b:1-(a|b)) if kind=='nor' else (lambda a,b:1-(a&b))
    sols=[(a,b) for a,b in product([0,1],repeat=2) if a==op(u,b) and b==op(v,a)]
    if (q,1-q) in sols:return q,1-q
    assert len(sols)==1,(kind,u,v,q,sols)
    return sols[0]

def actual(n,ins,q):
    if n==1:return latch('nor',ins[0],ins[1],q)
    if n==2:return latch('nand',ins[0],ins[1],q)
    if n==3:return latch('nand',ins[1],ins[0],q)
    if n==4:
        c,r,s=ins;return latch('nor',1-(r|c),1-(s|c),q)
    if n==5:
        c,s,r=ins;return latch('nand',1-(s&c),1-(r&c),q)
    if n==6:
        c,d=ins;r=1-(d|c);s=1-(r|c);return latch('nor',r,s,q)
    if n==7:
        c,d=ins;s=1-(d&c);r=1-(s&c);return latch('nand',s,r,q)
    s,r,e,*data=ins
    if s==0 and r==0:return 1,1
    if s==0:return 1,0
    if r==0:return 0,1
    if not e:return q,1-q
    if n in [8,13]:v=data[0]
    elif n in [9,11]:v=1-q
    elif n==10:
        j,k=data;v=(j if q==0 else 1-k)
    elif n==12:v=q^data[0]
    return v,1-v

def expected(n,ins,q):
    if n==1:
        r,s=ins
        if r&s:return 0,0
        v=s|((1-r)&q)
    elif n in [2,3]:
        s,r=ins if n==2 else ins[::-1]
        if not s and not r:return 1,1
        v=(1-s)|(r&q)
    elif n==4:
        c,r,s=ins
        if not c and not r and not s:return 0,0
        v=(c&q)|((1-c)&((1-s)|(r&q)))
    elif n==5:
        c,s,r=ins
        if c and s and r:return 1,1
        v=((1-c)&q)|(c&(s|((1-r)&q)))
    elif n==6:
        c,d=ins;v=(c&q)|((1-c)&d)
    elif n==7:
        c,d=ins;v=((1-c)&q)|(c&d)
    else:
        s,r,e,*data=ins
        if not s and not r:return 1,1
        if not s:return 1,0
        if not r:return 0,1
        f=(data[0] if n in [8,13] else (1-q) if n in [9,11] else (data[0]&(1-q))|((1-data[1])&q) if n==10 else ((1-data[0])&q)|(data[0]&(1-q)))
        v=((1-e)&q)|(e&f)
    return v,1-v

NINPUT={1:2,2:2,3:2,4:3,5:3,6:2,7:2,8:4,9:3,10:5,11:3,12:4,13:4}
CHECKS={}
for n,ni in NINPUT.items():
    count=0
    for ins in product([0,1],repeat=ni):
        for q in [0,1]:
            assert actual(n,ins,q)==expected(n,ins,q),(n,ins,q,actual(n,ins,q),expected(n,ins,q))
            count+=1
    CHECKS[n]=count
(BASE/'verification.json').write_text(json.dumps(CHECKS,indent=2),encoding='utf8')

def checkpoint(n,signals,cases):
    d=Diagram(f'Перевірка 3.{n}',900,118)
    d.text(12,15,'ЛОГІЧНА ПЕРЕВІРКА · '+', '.join(signals),16,True,anchor='lm')
    for i,(ins,q) in enumerate(cases):
        xx=10+i*222;v,b=actual(n,ins,q)
        d.rect(xx,35,215,76,fill='#FFFFFF')
        d.text(xx+108,54,','.join(map(str,ins))+f'; Qn={q}',16)
        d.text(xx+108,84,f'Qn+1 = {v}   /Qn+1 = {b}',18,True)
    return d.save(f'check_{n:02}')

SCHEMES={}
for n,k,g,d in [(1,'nor',False,False),(2,'nand',False,False),(4,'nor',True,False),(5,'nand',True,False),(6,'nor',True,True),(7,'nand',True,True)]:SCHEMES[n]=gate_diagram(n,k,g,d)
for n,k,m in [(3,'RS','normal'),(8,'D','normal'),(9,'D','T_from_D'),(10,'JK','normal'),(11,'JK','T_async'),(12,'JK','T_sync'),(13,'JK','D_from_JK')]:SCHEMES[n]=integral(n,k,m)

CASES={
1:(['R','S'],[((0,0),1),((0,1),0),((1,0),1),((1,1),0)]),
2:(['/S','/R'],[((1,1),1),((0,1),0),((1,0),1),((0,0),0)]),
3:(['/R','/S'],[((1,1),1),((1,0),0),((0,1),1),((0,0),0)]),
4:(['/C','/R','/S'],[((1,0,0),1),((0,1,0),0),((0,0,1),1),((0,0,0),0)]),
5:(['C','S','R'],[((0,1,1),1),((1,1,0),0),((1,0,1),1),((1,1,1),0)]),
6:(['/C','D'],[((1,1),0),((0,1),0),((0,0),1),((1,0),1)]),
7:(['C','D'],[((0,1),0),((1,1),0),((1,0),1),((0,0),1)]),
8:(['/S','/R','E↑','D'],[((1,1,0,1),0),((1,1,1,1),0),((1,1,1,0),1),((0,1,0,0),0)]),
9:(['/S','/R','EТ↑'],[((1,1,0),1),((1,1,1),0),((1,1,1),1),((1,0,0),1)]),
10:(['/S','/R','E↓','J','K'],[((1,1,1,0,0),1),((1,1,1,1,0),0),((1,1,1,0,1),1),((1,1,1,1,1),1)]),
11:(['/S','/R','EТ↓'],[((1,1,0),1),((1,1,1),0),((1,1,1),1),((1,0,0),1)]),
12:(['/S','/R','E↓','T'],[((1,1,0,1),0),((1,1,1,0),1),((1,1,1,1),0),((1,1,1,1),1)]),
13:(['/S','/R','E↓','D'],[((1,1,0,1),0),((1,1,1,1),0),((1,1,1,0),1),((1,0,0,1),1)])}
for n,(signals,cases) in CASES.items():checkpoint(n,signals,cases)

def waveform(stem,title,signals,notes='',events=None):
    N=len(next(iter(signals.values())));H=58*len(signals)+93
    d=Diagram(title,900,H);d.text(14,18,title,20,True,anchor='lm')
    x0=110;step=760/N
    for i in range(N+1):
        x=x0+i*step;d.line((x,45),(x,H-38),color='#dddddd',width=1)
        if i<N:d.text(x+step/2,H-21,str(i),15)
    for row,(lab,vals) in enumerate(signals.items()):
        low=80+row*58;hi=low-28;d.text(86,(low+hi)/2,lab,19,anchor='rm')
        pts=[]
        for i,v in enumerate(vals):
            yy=hi if v else low
            if i and vals[i-1]!=v:pts.append((x0+i*step,low if vals[i-1]==0 else hi))
            pts.extend([(x0+i*step,yy),(x0+(i+1)*step,yy)])
        d.line(*pts,width=2)
    if events:
        for i in events:d.line((x0+i*step,40),(x0+i*step,H-38),color='#777777',width=1)
    return d.save(stem)

def seq(n,inputs,initial=0):
    q=initial;qq=[];bb=[]
    for inp in inputs:q,b=actual(n,inp,q);qq.append(q);bb.append(b)
    return qq,bb

# Eight diagrams cover all seven requested categories plus level-sensitive D.
R=[0,0,0,1,0,0,0,1,0,0,0,0];S=[0,1,0,0,0,1,0,0,0,1,0,0]
q,b=seq(1,list(zip(R,S)));waveform('time_1','Асинхронний RS на АБО–НІ',{'R':R,'S':S,'Q':q,'/Q':b})
ns=[1-x for x in S];nr=[1-x for x in R];q,b=seq(2,list(zip(ns,nr)));waveform('time_2','Асинхронний RS на І–НІ',{'/S':ns,'/R':nr,'Q':q,'/Q':b})
c=[1,1,0,0,1,0,1,0,0,1,0,1];nr=[1,1,1,1,0,0,1,1,1,0,0,1];ns=[1,0,0,1,1,1,0,0,1,1,1,1]
q,b=seq(4,list(zip(c,nr,ns)));waveform('time_3','Синхронний RS на АБО–НІ',{'/C':c,'/R':nr,'/S':ns,'Q':q,'/Q':b})
C=[1-x for x in c];s=[1-x for x in ns];r=[1-x for x in nr];q,b=seq(5,list(zip(C,s,r)));waveform('time_4','Синхронний RS на І–НІ',{'C':C,'S':s,'R':r,'Q':q,'/Q':b})
C=[0,0,1,1,0,0,1,1,0,0,1,1];D=[0,1,1,0,1,0,0,1,0,1,1,0]
q,b=seq(7,list(zip(C,D)));waveform('time_5','D засувка та D-тригер за фронтом',{'C':C,'D':D,'Q рівень':q,'Q фронт':seq(8,[(1,1,int(bool(i and C[i]>C[i-1])),D[i]) for i in range(12)])[0]})
T=[0]*4+[1]*8+[0]*4+[1]*4;C=[0,1,1,0]*5;edge=[int(bool(i and C[i]<C[i-1])) for i in range(20)]
q,b=seq(12,[(1,1,edge[i],T[i]) for i in range(20)]);waveform('time_6','Синхронний T на JK-тригері',{'C':C,'T':T,'Q':q,'/Q':b})
C=[0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0];J=[0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1];K=[0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]
q,b=seq(10,[(1,1,int(bool(i and C[i]<C[i-1])),J[i],K[i]) for i in range(20)]);waveform('time_7','JK-тригер за спадним фронтом',{'C':C,'J':J,'K':K,'Q':q,'/Q':b})
T=[0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1]
qd,_=seq(9,[(1,1,int(bool(i and T[i]>T[i-1]))) for i in range(16)])
qj,_=seq(11,[(1,1,int(bool(i and T[i]<T[i-1]))) for i in range(16)])
waveform('time_8','Лічильні T-тригери без окремого входу C',{'T':T,'Q на D':qd,'Q на JK':qj})

ET.indent(MX)
ET.ElementTree(MX).write(OUT/'Схеми_ЛР3_КМАДО.drawio',encoding='utf-8',xml_declaration=True)
print('Verified',sum(CHECKS.values()),'transitions; generated',len(list(ASSETS.glob('*.png'))),'figures.')
