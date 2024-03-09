# Bloc de notas

#* Importa las librerias nesesarias
from Funciones import informacion
import tkinter as tk

class Ui_Notepad: 
   
   # ************** ************** Constructor ************** ************** #
   def setupUi(self, Form):
      Form.iconbitmap('icono.ico')
      Form.geometry('500x250+250+250')

      [
      self.FONT, self.BG, self.FG,
      self.SBG, self.SFG, self.IBG ] = informacion()

      # ********* ********* Los Menus ********* ********* #
      self.mn_opc = tk.Menu(Form)
      Form.config(menu=self.mn_opc)
      
      self.archivo = tk.Menu(self.mn_opc, tearoff=0)
      self.edicion = tk.Menu(self.archivo, tearoff=0)
      self.formato = tk.Menu(self.mn_opc, tearoff=0)
      self.ver = tk.Menu(self.mn_opc, tearoff=0)
      self.ayuda = tk.Menu(self.mn_opc, tearoff=0)      
      
      # Insertar los menus
      self.mn_opc.add_cascade(label='Archivo', menu=self.archivo)
      self.mn_opc.add_cascade(label='Edición', menu=self.edicion)
      self.mn_opc.add_cascade(label="Formato", menu=self.formato)
      self.mn_opc.add_cascade(label="Ver",   menu=self.ver  )
      self.mn_opc.add_cascade(label='Ayuda', menu=self.ayuda)

      # ******* ******* Caja de texto y scroollbar ******* ******* #
      # Caja de texto
      self.box_text = tk.Text(
         Form, font=self.FONT, bg=self.BG, fg=self.FG, undo=True,
         insertbackground=self.IBG, selectbackground=self.SBG,
         selectforeground=self.SFG 
      )
      self.box_text.grid(column=0, row=0, sticky='nsew')
      
      # Scrollbar Horizontal
      ladox = tk.Scrollbar(Form, orient = 'horizontal', command= self.box_text.xview)
      ladox.grid(column=0, row = 1, sticky='ew')
      
      # Scrollbar Vertical
      ladoy = tk.Scrollbar(Form, orient ='vertical', command = self.box_text.yview)
      ladoy.grid(column = 1, row = 0, sticky='ns')
      
      # Configuracion para que funcione
      self.box_text.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
      self.box_text.focus()    

      Form.columnconfigure(0, weight=1)
      Form.rowconfigure(0, weight=1)
   
#* Author: Francisco Velez
