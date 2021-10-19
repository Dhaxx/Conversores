import conexao
from tkinter import * 
from tkinter import filedialog
from tkinter import Listbox
from tkinter import ttk
import os


onvalue = 0
position_bar = 0
full_path = os.path.abspath(os.getcwd())
def fille():
    
    txt_file = open(full_path + "\Formulário.txt", "w")
    txt_file.write(str(host_input.get() + ";" + porta_input.get() + ";" + source_bdorig.get() + ";" + source_fdb["text"]))

    conexao.set_connection(host_input.get(),  porta_input.get(), source_fdb["text"])

def read_fille():
    global config
    try:
        txt = open(full_path + "\Formulário.txt", "r").readline()
    except:
        global txt_file
        txt_file = open(full_path + "\Formulário.txt", "w")
    
    if len(txt) == 0: return
    
    config = txt.split(";")

    host_input.insert(0,config[0])
    porta_input.insert(0, config[1])
    source_bdorig.insert(0, config[2])

    source_fdb["text"] = config[3]

    conexao.set_connection(config[0], config[1], config[3])

def registra_log(msg):
    log_list.insert(0,msg)
    global position_bar
    
    position_bar += 1
    varBar.set(position_bar)
    win.update_idletasks()

def iniciar():
    import base
    import cadastro
    import bens

    varBar.set(0)

    base.trigger(1)
    if cb_limpa_tabelas.get() == "1":
        registra_log("Tabelas Limpadas")        
        base.limpa_tabelas() 
             
    if cb_cria_campos.get() == "1":
        registra_log("Campos criados")
        base.cria_campos()
        
    if cb_tipos_mov.get() == "1":
        registra_log("Tipos de Movimentação Inseridos")
        cadastro.tipos_mov()

    if cb_tipos_ajuste.get() == "1":
        registra_log("Inserido os Tipos de Ajuste")
        cadastro.tipos_ajuste()

    if cb_baixas.get() == "1":
        registra_log("Inserido os Tipos de Baixas")
        cadastro.baixas()

    if cb_tipo_bens.get() == "1":
        registra_log("Inserido os Tipo de bens")
        cadastro.tipos_bens()

    if cb_situacao.get() == "1":
        registra_log("Inserido as Situações dos Bens")
        cadastro.situacao()

    if cb_grupo.get() == "1":
        registra_log("Grupos Convertidos")
        cadastro.converte_grupos()

    if cb_unidade.get() == "1":
        registra_log("Unidades Convertidas")
        cadastro.converte_unidades()

    if cb_subunidade.get() == "1":
        registra_log("Subunidades Convertidas")
        cadastro.converte_subunidades()

    if cb_bens.get() == "1":
        registra_log("Bens Convertidos")
        bens.converte_bens()

    if cb_aquisicao.get() == "1":
        registra_log("Aquisições Convertidas")
        bens.mov_aquisicao()

    if cb_transferencias.get() == "1":
        registra_log("Transferências Convertidas")
        bens.transferencias()

    if cb_mov_baixas.get() == "1":
        registra_log("Baixas Convertidas")
        bens.mov_baixas()
    
    if cb_depreciacoes.get() == "1":
        registra_log("Depreciacoes Convertidas")
        bens.depreciacoes()    
    base.trigger(0)
    varBar.set(len(cbs) -1)

def quit():                            
    import sys; sys.exit() 

def clear():
    log_list.delete(0, 99999999)
    varBar.set(0)
    
    for cb in cbs:
        cb.set(0)
        color = off_color

    for component in toolbox.children.values():      
        if component.widgetName == 'checkbutton':
            component["fg"] = color

def checkall():
    global onvalue  

    if onvalue == 0 :
        onvalue = 1        
        color = on_color
    else:
        onvalue = 0  
        color = off_color          

    for cb in cbs:
        cb.set(onvalue)

    for component in toolbox.children.values():      
        if component.widgetName == 'checkbutton':
            component["fg"] = color                               


### Gerando Janela ###
win = Tk()
win.geometry("700x600")
win.config(bg = "#202124")
win.title("Conversor Amêndola")
win.iconbitmap(full_path + '\\amendola.ico')
win.minsize(700, 650)
win.maxsize(700, 650)
modulo = Label(win, text="Conversor Amêndola", bg="#202124", fg="white")
modulo.config(font=("Tahoma", 25,"italic"))
modulo.grid(column=0, row=0)

### Variáveis cores ativado e desativado ###
off_color = "red"
on_color = "green"

##### Criando container dos checkboxes ####
cx_sup = Frame(win, bg="#AAA89D")
toolbox = Frame(cx_sup, background="#202124")
toolbox.pack(padx=1, pady=1)
toolbox_titulo = Label(win, text="Funções", bg="#202124", fg="#AAA89D")
toolbox_titulo.config(font=("Arial",7))
toolbox_titulo.place(x=18, y= 41)
cx_sup.place(x=10, y=50, width=680, height=142)
toolbox.place(x=1, y=1, width=678, height=140)

### Criando checkboxes ###
def on_check():  
    #Essa variável vai iniciar quando o check for marcado   
        
    if cb_cria_campos.get() == "1":chbox_cria_campos["fg"]= on_color  # Se a posição do check for = 1 então...
    else:chbox_cria_campos["fg"] = off_color

    if cb_limpa_tabelas.get() == "1":chbox_limpa_tabelas["fg"]= on_color  
    else:chbox_limpa_tabelas["fg"] = off_color
    
    if cb_tipos_mov.get() == "1":chbox_tipos_mov["fg"]= on_color  
    else:chbox_tipos_mov["fg"] = off_color

    if cb_tipos_ajuste.get() == "1":chbox_tipos_ajuste["fg"]= on_color  
    else:chbox_tipos_ajuste["fg"] = off_color

    if cb_baixas.get() == "1":chbox_baixas["fg"]= on_color  
    else:chbox_baixas["fg"] = off_color

    if cb_tipo_bens.get() == "1":chbox_tipo_bens["fg"]= on_color  
    else:chbox_tipo_bens["fg"] = off_color
    
    if cb_situacao.get() == "1":chbox_situacao["fg"]= on_color  
    else:chbox_situacao["fg"] = off_color
    
    if cb_grupo.get() == "1":chbox_grupo["fg"]= on_color  
    else:chbox_grupo["fg"] = off_color
    
    if cb_unidade.get() == "1":chbox_unidade["fg"]= on_color  
    else:chbox_unidade["fg"] = off_color
    
    if cb_subunidade.get() == "1":chbox_subunidade["fg"]= on_color  
    else:chbox_subunidade["fg"] = off_color
    
    if cb_bens.get() == "1":chbox_bens["fg"]= on_color  
    else:chbox_bens["fg"] = off_color
    
    if cb_aquisicao.get() == "1":chbox_aquisicao["fg"]= on_color  
    else:chbox_aquisicao["fg"] = off_color
    
    if cb_transferencias.get() == "1":chbox_transferencias["fg"]= on_color  
    else:chbox_transferencias["fg"] = off_color
    
    if cb_mov_baixas.get() == "1":chbox_mov_baixas["fg"]= on_color  
    else:chbox_mov_baixas["fg"] = off_color

    if cb_depreciacoes.get() == "1":chbox_depreciacoes["fg"]= on_color 
    else:chbox_depreciacoes["fg"] = off_color

cb_cria_campos = StringVar(win)     # Variável para o chekcbox
cb_cria_campos.set(0)  
chbox_cria_campos = Checkbutton(toolbox,variable = cb_cria_campos,text="Cria Campos",background="#202124",command=on_check,fg=off_color)
chbox_cria_campos.config(font=("Arial",13))
chbox_cria_campos.place(x= 0, y= 5)

cb_limpa_tabelas = StringVar(win)    
cb_limpa_tabelas.set(0)  
chbox_limpa_tabelas = Checkbutton(toolbox,variable = cb_limpa_tabelas,text="Limpa Tabelas",background="#202124",command=on_check,fg=off_color)
chbox_limpa_tabelas.config(font=("Arial",13))
chbox_limpa_tabelas.place(x= 0, y= 30)

cb_tipos_mov = StringVar(win)    
cb_tipos_mov.set(0)  
chbox_tipos_mov = Checkbutton(toolbox,variable = cb_tipos_mov,text="Tipos Movimento",background="#202124",command=on_check,fg=off_color)
chbox_tipos_mov.config(font=("Arial",13))
chbox_tipos_mov.place(x= 0, y= 55)

cb_tipos_ajuste = StringVar(win)    
cb_tipos_ajuste.set(0)  
chbox_tipos_ajuste = Checkbutton(toolbox,variable = cb_tipos_ajuste,text="Tipos Ajuste",background="#202124",command=on_check,fg=off_color)
chbox_tipos_ajuste.config(font=("Arial",13))
chbox_tipos_ajuste.place(x= 0, y= 80)

cb_baixas = StringVar(win)    
cb_baixas.set(0)  
chbox_baixas = Checkbutton(toolbox,variable = cb_baixas,text="Tipos de Baixas",background="#202124",command=on_check,fg=off_color)
chbox_baixas.config(font=("Arial",13))
chbox_baixas.place(x= 0, y= 105)

cb_tipo_bens = StringVar(win)    
cb_tipo_bens.set(0)  
chbox_tipo_bens = Checkbutton(toolbox,variable = cb_tipo_bens,text="Tipos Bens",background="#202124",command=on_check,fg=off_color)
chbox_tipo_bens.config(font=("Arial",13))
chbox_tipo_bens.place(x= 225, y= 5)

cb_situacao = StringVar(win)    
cb_situacao.set(0)  
chbox_situacao = Checkbutton(toolbox,variable = cb_situacao,text="Situação",background="#202124",command=on_check,fg=off_color)
chbox_situacao.config(font=("Arial",13))
chbox_situacao.place(x= 225, y= 30)

cb_grupo = StringVar(win)    
cb_grupo.set(0)  
chbox_grupo = Checkbutton(toolbox,variable = cb_grupo,text="Grupos",background="#202124",command=on_check,fg=off_color)
chbox_grupo.config(font=("Arial",13))
chbox_grupo.place(x= 225, y= 55)

cb_unidade = StringVar(win)    
cb_unidade.set(0)  
chbox_unidade = Checkbutton(toolbox,variable = cb_unidade,text="Unidades",background="#202124",command=on_check,fg=off_color)
chbox_unidade.config(font=("Arial",13))
chbox_unidade.place(x= 225, y= 80)

cb_subunidade = StringVar(win)    
cb_subunidade.set(0)  
chbox_subunidade = Checkbutton(toolbox,variable = cb_subunidade,text="Subunidades",background="#202124",command=on_check,fg=off_color)
chbox_subunidade.config(font=("Arial",13))
chbox_subunidade.place(x= 225, y= 105)

cb_bens = StringVar(win)    
cb_bens.set(0)  
chbox_bens = Checkbutton(toolbox,variable = cb_bens,text="Bens",background="#202124",command=on_check,fg=off_color)
chbox_bens.config(font=("Arial",13))
chbox_bens.place(x= 450, y= 5)

cb_aquisicao = StringVar(win)    
cb_aquisicao.set(0)  
chbox_aquisicao = Checkbutton(toolbox,variable = cb_aquisicao,text="Aquisicao",background="#202124",command=on_check,fg=off_color)
chbox_aquisicao.config(font=("Arial",13))
chbox_aquisicao.place(x= 450, y= 30)

cb_transferencias = StringVar(win)    
cb_transferencias.set(0)  
chbox_transferencias = Checkbutton(toolbox,variable = cb_transferencias,text="Transferencias",background="#202124",command=on_check,fg=off_color)
chbox_transferencias.config(font=("Arial",13))
chbox_transferencias.place(x= 450, y= 55)

cb_mov_baixas = StringVar(win)    
cb_mov_baixas.set(0)  
chbox_mov_baixas = Checkbutton(toolbox,variable = cb_mov_baixas,text="Baixas",background="#202124",command=on_check,fg=off_color)
chbox_mov_baixas.config(font=("Arial",13))
chbox_mov_baixas.place(x= 450, y= 80)

cb_depreciacoes = StringVar(win)
cb_depreciacoes.set(0)
chbox_depreciacoes = Checkbutton(toolbox,variable = cb_depreciacoes,text="Depreciações",background="#202124",command=on_check,fg=off_color) 
chbox_depreciacoes.config(font=("Arial",13))
chbox_depreciacoes.place(x= 450, y=105)

cb_checkall = StringVar(win)
cb_checkall.set(0)
chbox_checkall = Checkbutton(toolbox,variable = cb_checkall,text="", background="#303134",command=checkall ,fg=off_color)
chbox_checkall.config(font=("Arial",13))
chbox_checkall.place(x= 650, y= 0)

cbs = [cb_cria_campos,cb_limpa_tabelas,cb_tipos_mov,cb_tipos_ajuste,cb_baixas,cb_tipo_bens,cb_situacao,cb_grupo,cb_unidade,cb_subunidade,cb_bens,cb_aquisicao,cb_transferencias,cb_mov_baixas,cb_depreciacoes,cb_checkall]

### Container 2 ###

cx_sup_secundary = Frame(win, bg="#AAA89D")    
console = Frame(cx_sup_secundary, background="#202124") 
console.pack(padx=1, pady=1)
formbox_titulo = Label(win, text="Configuração dos Bancos", bg="#202124", fg="#AAA89D")
formbox_titulo.config(font=("Arial",7))
formbox_titulo.place(x=18, y= 192)
cx_sup_secundary.place(x=10, y=200, width=680, height=109)
console.place(x=1, y=1, width=678, height=107)

### Formulários ###
def openfdb():
    global source_fdb
    console.filename = filedialog.askopenfilename(initialdir="C:\Fiorilli\SCPI_8\Cidades", title="...", filetypes=(("Firebird","*.FDB"), ("all files", "*.*")))
    source_fdb["text"] = console.filename

def openorig():
    global source_bdorig
    console.filename = filedialog.askopenfilename(initialdir="C:\\", title="...", filetypes=(("Backup","*.BAK"), ("all files", "*.*")))
    source_bdorig = Label(console, text="", background="#303134").place(x=5, y= 75, width=400)
    source_bdorig = Label(console, text=console.filename, background="#303134", fg="white").place(x=5, y=75, width=400)


fdb_label = Label(console, text="Caminho Físico da Base de dados SCPI:",background="#202124", fg="#AAA89D")
fdb_label.config(font=("Arial",9,"bold"))
fdb_label.place(x=5, y=5)
source_fdb = Label(console, text="", background="#303134", fg="white")
source_fdb.place(x=5, y= 25, width=400)
source_btn = Button(console, text="🔎",fg="white",background="#202124", cursor="hand2", borderwidth=0, command=openfdb).place(x=410, y=25, height=25)

host_label = Label(console, text="Host:",background="#202124", fg="#AAA89D")
host_label.config(font=("Arial",9,"bold"))
host_label.place(x=460, y=5)
host_input = Entry(console, background="#303134", fg="white", borderwidth=0)
host_input.config(font=("Arial",10,"bold"))
host_input.place(x=463, y=25, width=80)

porta_label = Label(console, text="Porta:",background="#202124", fg="#AAA89D")
porta_label.config(font=("Arial",9,"bold"))
porta_label.place(x=580, y=5)
porta_input = Entry(console, background="#303134", fg="white", borderwidth=0)
porta_input.config(font=("Arial",10,"bold"))
porta_input.place(x=583, y=25, width=80)

bdorig_label = Label(console, text="Banco de Origem:",background="#202124", fg="#AAA89D")
bdorig_label.config(font=("Arial",9,"bold"))
bdorig_label.place(x=5, y=55)
source_bdorig = Entry(console, background="#303134", fg="white", borderwidth=0)
source_bdorig.place(x=5, y= 75, width=400)

### Voltar aqui para criar o botão salvar ###
btn_save = Button(console, text="💾 Salvar", fg="white", background="#303134", cursor="hand2", borderwidth=0, command=fille)
btn_save.place(x=463, y=55, width=200, height=40)

### Container 3 ###
cx_sup_ternary = Frame(win, bg="#AAA89D")    
situation = Frame(cx_sup_ternary, background="#202124") 
situation.pack(padx=1, pady=1)
cx_sup_ternary.place(x=10, y=320, width=680, height=245)
situation.place(x=1, y=1, width=678, height=243)

log_list = Listbox(situation, background="#202124", fg="white", borderwidth=0)
log_list.place(x=0, y= 0, width= 678, height=225)

### Voltar aqui para configurar
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='#202124', background='green')

varBar = DoubleVar()
varBar.set(position_bar)
pos_max = len(cbs) -1

progressbar = ttk.Progressbar(situation, variable=varBar,maximum=pos_max, style="red.Horizontal.TProgressbar")
progressbar.place(x=0, y=215, width= 678, height=40)

init = Button(win, text='▷ Iniciar', background="#303134", cursor="hand2", fg="white", borderwidth=0, command=iniciar)
init.place(x= 15, y=585, height=50, width=230)  #.place(x= 473, y=585, height=50, width=200)

clean = Button(win, text='🗑️ Limpar', background="#303134", cursor="hand2", fg="white", borderwidth=0, command=clear)
clean.place(x= 255, y=585, height=50, width=208)

exit = Button(win, text='❌ Sair', background="#303134", cursor="hand2", fg="white", borderwidth=0, command=quit)
exit.place(x= 473, y=585, height=50, width=200)   #.place(x= 15, y=585, height=50, width=200)

host = str(host_input.get())
read_fille()
win.mainloop()
