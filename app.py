import json,sys,unittest,uuid
from pathlib import Path
def validate(data):
    if not isinstance(data,dict)or data.get('version')!=1 or not isinstance(data.get('people'),dict)or not isinstance(data.get('edges'),list)or len(data['people'])>200 or len(data['edges'])>400:raise ValueError('Invalid version 1 family graph')
    for key,p in data['people'].items():
        if not isinstance(key,str)or not isinstance(p,dict)or not isinstance(p.get('name'),str)or not p['name'].strip()or len(p['name'])>80 or not isinstance(p.get('year'),int)or not 0<=p['year']<=3000:raise ValueError('Invalid person')
    parents={k:[]for k in data['people']}
    for edge in data['edges']:
        if not isinstance(edge,list)or len(edge)!=2 or any(k not in parents for k in edge)or edge[0]==edge[1]or edge[0]in parents[edge[1]]:raise ValueError('Invalid/duplicate parent link')
        parents[edge[1]].append(edge[0])
        if len(parents[edge[1]])>2:raise ValueError('At most two parents per person')
    active=set();done=set()
    def visit(k):
        if k in active:raise ValueError('Parent cycle detected')
        if k in done:return
        active.add(k)
        for parent in parents[k]:visit(parent)
        active.remove(k);done.add(k)
    for k in parents:visit(k)
    return data
class Tests(unittest.TestCase):
    def test_cycles(self):
        d={'version':1,'people':{'a':{'name':'Ada','year':1900},'b':{'name':'Ben','year':1930}},'edges':[['a','b']]};self.assertEqual(validate(json.loads(json.dumps(d))),d);d['edges'].append(['b','a'])
        with self.assertRaises(ValueError):validate(d)
def ui():
    import tkinter as tk
    from tkinter import ttk,filedialog,simpledialog,messagebox
    root=tk.Tk();root.title('Family Tree Builder');root.geometry('1050x720');data={'version':1,'people':{},'edges':[]};panel=ttk.Frame(root,padding=16);panel.pack(fill='both',expand=True);bar=ttk.Frame(panel);bar.pack(fill='x');parent=ttk.Combobox(bar,state='readonly',width=22);child=ttk.Combobox(bar,state='readonly',width=22);parent.pack(side='left');child.pack(side='left');canvas=tk.Canvas(panel,background='#eef5ef');canvas.pack(fill='both',expand=True,pady=10);x=ttk.Scrollbar(panel,orient='horizontal',command=canvas.xview);x.pack(fill='x');y=ttk.Scrollbar(panel,orient='vertical',command=canvas.yview);y.pack(side='right',fill='y');canvas.configure(xscrollcommand=x.set,yscrollcommand=y.set);ids=[]
    def draw():
        nonlocal ids
        canvas.delete('all');ids=sorted(data['people'],key=lambda k:data['people'][k]['name']);labels=[data['people'][k]['name']+' ['+k[:6]+']'for k in ids];parent['values']=child['values']=labels
        levels={}
        def level(k):
            if k not in levels:levels[k]=max([level(a)+1 for a,b in data['edges']if b==k]or[0])
            return levels[k]
        positions={};counts={}
        for k in ids:
            n=level(k);row=counts.get(n,0);counts[n]=row+1;positions[k]=(100+n*210,50+row*90)
        for a,b in data['edges']:canvas.create_line(*positions[a],*positions[b],fill='#668473',arrow='last',width=2)
        for k,(a,b)in positions.items():
            p=data['people'][k];canvas.create_rectangle(a-85,b-25,a+85,b+25,fill='#d0ead8');canvas.create_text(a,b,text=p['name'][:24]+'\n'+(str(p['year'])if p['year']else'?'))
        box=canvas.bbox('all');canvas.configure(scrollregion=box or(0,0,1000,600))
    def act(fn):
        try:fn();draw()
        except (ValueError,OSError,KeyError,TypeError)as e:messagebox.showerror('Family graph',str(e))
    def add():
        name=simpledialog.askstring('Person','Name:',parent=root)
        if not name:return
        year=simpledialog.askinteger('Birth year','Year, or 0 for unknown:',minvalue=0,maxvalue=3000,parent=root)
        if year is None:return
        next=json.loads(json.dumps(data));next['people'][uuid.uuid4().hex]={'name':name.strip(),'year':year};validate(next);data.update(next)
    def link():
        if parent.current()<0 or child.current()<0:raise ValueError('Choose parent and child')
        next=json.loads(json.dumps(data));next['edges'].append([ids[parent.current()],ids[child.current()]]);validate(next);data.update(next)
    def save():
        path=filedialog.asksaveasfilename(defaultextension='.json')
        if path:Path(path).write_text(json.dumps(data,indent=2),encoding='utf-8')
    def load():
        nonlocal data
        path=filedialog.askopenfilename(filetypes=[('JSON','*.json')])
        if path:
            if Path(path).stat().st_size>1024*1024:raise ValueError('Limit 1 MiB')
            data=validate(json.loads(Path(path).read_text(encoding='utf-8')))
    for title,fn in [('Add person',add),('Link parent → child',link),('Save graph',save),('Open graph',load)]:ttk.Button(bar,text=title,command=lambda f=fn:act(f)).pack(side='left',padx=4)
    draw();root.mainloop()
if __name__=='__main__':unittest.main(argv=[sys.argv[0]])if '--self-test'in sys.argv else ui()
