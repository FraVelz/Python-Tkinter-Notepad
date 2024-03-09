# Bloc de notas

#* Importa las librerias nesesarias
from Funciones import (
   obtener_tiempo, obtener_nombre_arch, 
   rescribir, lectura, informacion, actualizar_
)

from tkinter import font, ttk, colorchooser, messagebox
from tkinter import filedialog as fd
from ui_Notepad import Ui_Notepad
import tkinter as tk

class Notepad: 

   # ************** ************** Constructor ************** ************** #
   def __init__(self):
      self.nameArch = ''
      self.ext_default = '.txt'
      self.titulo_name = 'Bloc de notas 2.0'
      self.titulo_default = f'Sin título: {self.titulo_name}'

      self.root = tk.Tk()
      self.root.wm_title(self.titulo_default)

      self.ui = Ui_Notepad()
      self.ui.setupUi(self.root)

      self.señal_ajustes = tk.BooleanVar()
      self.señal_ajustes.set(True)
      self.clik_aceptar = False

      self.lista_fileTypes = ( ('Archivo de texto', '*.txt'), 
         ('Archivo de Python', '*.py *.pyw'), 
         ('Todos los Archivos', '*.*')
      ) 

      self.__ruta__ = ''
      self.x, self.y = 0, 0

      self.verificar_caja()
      self.widgets()

      self.root.mainloop()
   
   # ************** ************** Objectos ************** ************** #
   def widgets(self):      
      self.ui.archivo.add_command(label='Nuevo',    command= self.new_file )
      self.ui.archivo.add_command(label='Abrir...', command= self.open_file) 
      self.ui.archivo.add_command(label='Guardar',  command= self.save_file)
      self.ui.archivo.add_command(
         label='Guardar como...', command= self.guardar_como 
      )

      self.ui.archivo.add_command(label='Ventana nueva',   command= Notepad  )
      self.ui.archivo.add_command(label='Cerrar',   command= self.salir )

      self.ui.archivo.add_separator()	
      self.ui.archivo.add_command(label='Salir',    command= exit )

      # Menu: Edicion
      self.ui.edicion.add_command(
         label="Deshacer", command = lambda: self.ui.box_text.edit_undo()
      )
      self.ui.edicion.add_separator()

      self.ui.edicion.add_command(
         label="Cortar", accelerator='Ctrl+X', 
         command = lambda: self.root.focus_get().event_generate("<<Cut>>")
      )
      self.ui.edicion.add_command(
         label="Copiar", accelerator='Ctrl+C', 
         command = lambda: self.root.focus_get().event_generate("<<Copy>>") 
      )
      self.ui.edicion.add_command(
         label="Pegar", accelerator='Ctrl+V',  
         command = lambda: self.root.focus_get().event_generate("<<Paste>>")
      )
      self.ui.edicion.add_command(
         label="Eliminar", accelerator= 'Supr', 
         command = lambda: self.root.focus_get().event_generate("<<Clear>>")
      )


      self.ui.edicion.add_separator()
      self.ui.edicion.add_command(label="Run Python-Tkinter", command=self.run_python)

      # Menu: Formato
      self.ui.formato.add_checkbutton(
         label="Ajustes de linea", variable = self.señal_ajustes, 
         command= self.ajustes_de_linea
      )
      
      self.ui.formato.add_command(label="Fuente", command= self.formato_fuente)  
      self.ui.formato.add_command(label="Color de texto", command= lambda: self.elegir_color('fg'))
      self.ui.formato.add_command(label="Color de fondo", command= lambda: self.elegir_color('bg'))
      
      submenu1 = tk.Menu(self.ui.mn_opc, tearoff=0) # Sub Otros Colores
      submenu1.add_command(label="texto Seleccionado", command= lambda: self.elegir_color('sfg'))
      submenu1.add_command(label="fondo Seleccionado",  command= lambda: self.elegir_color('sbg'))
      self.ui.formato.add_cascade(label="Otros Colores", menu = submenu1)

      self.ui.formato.add_command(label="Color Puntero", command= lambda: self.elegir_color('ifg'))

      # Menu: Ver
      submenu = tk.Menu(self.ui.mn_opc, tearoff=0) # Sub Menu del Zoom
      submenu.add_command(label="Acercar", command= self.zoom_mas  )
      submenu.add_command(label="Alejar",  command= self.zoom_menos) 
      submenu.add_command(
         label="Restaurar Zoom", command= lambda: self.ui.box_text.config(font=self.f)
      )
         
      self.ui.ver.add_cascade(label="Zoom", menu = submenu)

      subMenu_f = tk.Menu(self.ui.mn_opc, tearoff=0) # Sub Menu de Formatear texto
      subMenu_f.add_command(label="MAYUSCULAS", command= lambda: self.formater('AA') )
      subMenu_f.add_command(label="Titulo",     command= lambda: self.formater('Aa') )
      subMenu_f.add_command(label="minusculas", command= lambda: self.formater('aa') )

      self.ui.ver.add_cascade(label='Formatear texto', menu = subMenu_f)

      self.ui.ver.add_command(
         label='Reestablecer tamaño', command= lambda: self.root.geometry('500x250') 
      )

      # Menu: Ayuda
      self.ui.ayuda.add_command(label='Ver ruta del Archivo', command= self.__Ruta__ )
      self.ui.ayuda.add_command(label='Hora y fecha', command= self.tiempo )
      self.ui.ayuda.add_separator()
      
      self.ui.ayuda.add_command( label='Autor', 
         command= lambda: messagebox.showinfo('Autor', 'Autor: Francisco Velez') 
      )

# ************** ************** Funciones ************** ************** #
   def new_file(self):
      self.root.wm_title('Sin título: Bloc de notas 2.0')
      self.__ruta__ = ''
      self.ui.box_text.delete(0.0, tk.END)
      self.ui.box_text.insert(0.0, '')

   def open_file(self):
      try:
         self.__ruta__ = fd.askopenfilename()
         texto = lectura(self.__ruta__)

         self.nameArch = obtener_nombre_arch(self.__ruta__)
         self.root.wm_title(f'{self.nameArch}: Bloc de notas 2.0')

         self.ui.box_text.delete(0.0, tk.END)
         self.ui.box_text.insert(0.0, texto)
      except: pass

   def save_file(self):
      if self.__ruta__ != '':
         m = self.ui.box_text.get(0.0, tk.END)
         rescribir(self.__ruta__, m)
      else:
         self.guardar_como()

   def guardar_como(self): 
      file_ = fd.asksaveasfile( 
         title='Guardar como...', defaultextension=self.ext_default, 
         filetypes= self.lista_fileTypes
      )
      
      if file_:
         contenido = self.ui.box_text.get(0.0, tk.END)
         self.__ruta__ = file_.name

         nameFile = obtener_nombre_arch(file_.name)
         self.root.wm_title(f'{nameFile}: Bloc de notas 2.0')
         
         file_.write(contenido)
         file_.close()

   def ajustes_de_linea(self):
      msg = 'word' if self.señal_ajustes.get() == True else 'none'
      self.ui.box_text.config(wrap=msg)

   # ****************** Funciones de Formato de Fuente ****************** #
   def formato_fuente(self): 
      self.vent_tipo_fuente = tk.Toplevel()
      self.vent_tipo_fuente.overrideredirect(1)
      self.vent_tipo_fuente.geometry('390x290+400+200')
      self.vent_tipo_fuente.config(bg= 'SeaGreen1', relief ='raised', bd = 3)
      self.vent_tipo_fuente.bind("<B1-Motion>", self.mover)
      self.vent_tipo_fuente.bind("<ButtonPress-1>", self.start) 
      
      fuente = list(font.families())
      tamaño = []
      for  i in range(8,73):tamaño.append(i)

      tk.Label(self.vent_tipo_fuente, text= 'Fuente:', fg = 'black', bg='SeaGreen1',
      font= ('Segoe UI Symbol', 12)).grid(row=0,column=0, padx=5, ipady=6)

      tk.Label(self.vent_tipo_fuente, text= 'Tamaño:', fg = 'black', bg='SeaGreen1', 
      font= ('Segoe UI Symbol', 12)).grid(row=0,column=1, padx=5, ipady=6)	

      self.combobox_fuente = ttk.Combobox(self.vent_tipo_fuente, values = fuente, 
         justify='center',width='15', font='Arial')
      self.combobox_fuente.grid(row=1, column=0, padx =25, pady=5) #state="readonly"
      self.combobox_fuente.current(135)

      self.combobox_tamaño = ttk.Combobox(self.vent_tipo_fuente,values = tamaño, 
         justify='center',width='12', font='Arial')
      self.combobox_tamaño.grid(row=1, column=1, padx =25, pady=15)
      self.combobox_tamaño.current(4)

      self.preview = tk.Label(self.vent_tipo_fuente,fg = 'black', bg='SeaGreen1', font= ('Arial', 12))
      self.preview.grid(columnspan=2, row=2, padx=5, ipady=6)

      self.aceptar = tk.Button(
         self.vent_tipo_fuente, text= 'Aplicar', fg = 'black', bg='white', bd = 2, 
         font= ('Arial', 12), command = self.señal_boton)
      self.aceptar.grid(columnspan=2, row=3, padx=5, pady=5)

      self.aplicar_formato()
      self.vent_tipo_fuente.mainloop()

   def mover(self, event): 
      deltax = event.x - self.x
      deltay = event.y - self.y
      self.vent_tipo_fuente.geometry("+%s+%s" % (self.vent_tipo_fuente.winfo_x() + 
         deltax, self.vent_tipo_fuente.winfo_y() + deltay))
      self.vent_tipo_fuente.update()

   def start(self, event):
      self.x = event.x
      self.y = event.y
   
   # ************* ************* Mas Funciones ************* ************* #
   
   def señal_boton(self): self.clik_aceptar = True
   
   def elegir_color(self, opc=''): 
      color = colorchooser.askcolor()[1] 
      file = informacion()

      if opc == 'bg': 
         self.ui.box_text.config(bg=color)
         file[1] = color

      if opc == 'fg': 
         self.ui.box_text.config(fg=color)
         file[2] = color
         
      if opc == 'sbg': 
         self.ui.box_text.config(selectbackground=color)
         file[3] = color

      if opc == 'sfg': 
         self.ui.box_text.config(selectforeground=color)
         file[4] = color

      if opc == 'ifg': 
         self.ui.box_text.config(insertbackground=color)
         file[5] = color
      
      actualizar_(file[0], file[1], file[2], file[3], file[4], file[5])
   
   def tiempo(self): #* Hora y fecha 
      time_  = obtener_tiempo()
      self.ui.box_text.insert(tk.INSERT, time_)

   def zoom_mas(self): #* Aumenta el zoom 
      if self.num < 90:			
         self.num += 2
         try: self.ui.box_text.config(font= ( self.FONT[0], self.num, self.FONT[2]))
         except: self.ui.box_text.config(font= ( self.FONT[0], self.num))

      else:
         self.num = int(self.f[1])

   def zoom_menos(self): #* Disminuye el zoom       
      if self.num >6:			
         self.num -= 2
         try: self.ui.box_text.config(font= ( self.FONT[0], self.num, self.FONT[2]))
         except: self.ui.box_text.config(font= ( self.FONT[0], self.num))
      
      else:
         self.num = self.f[1]

   def __Ruta__(self): #* Insertar ruta del archivo 
      if self.__ruta__ != '':
        self.ui.box_text.insert(tk.INSERT, self.__ruta__)
      
      else:
        self.ui.box_text.insert(
            tk.INSERT, 
            '''
   Error: No hay archivo abierto 
         para mostrar la ruta. 
   '''
         )
   
   def formater(self, var='AA|aa|Aa'): #* Formatea el texto de la caja 
      txt =self.ui.box_text.get('0.0','end')
      
      if var == 'AA': txt = txt.upper()
      if var == 'aa': txt = txt.lower()
      if var == 'Aa': txt = txt.title()
      
      self.ui.box_text.delete(0.0, tk.END)
      self.ui.box_text.insert(tk.END, txt)
      
   def aplicar_formato(self): #* Aplica el formato de la config fuente 
      self.f = str(self.combobox_fuente.get())
      self.n = int(self.combobox_tamaño.get())
      tipo = (self.f , self.n )
      tipo_preview = (self.f, int(self.n*0.7) )

      self.preview.config(text = 'AbC 123' , font = (tipo_preview))
      x = self.ui.box_text.after(10, self.aplicar_formato)

      if self.clik_aceptar == True:
         self.ui.box_text.config(font = tipo)

         file = informacion()
         actualizar_(tipo, *file[1:])

         self.ui.box_text.after_cancel(x)
         self.clik_aceptar = False
         self.vent_tipo_fuente.destroy()

   def run_python(self): #* Ejecuta los archivos python 
      try: exec(self.ui.box_text.get('1.0', tk.END))
      except: pass 
      
   def verificar_caja(self, *args): #* Verifica si la caja de texto esta vacia 

      def funcSalir(title='', command=None):
         self.root.wm_title(title)
         self.root.protocol("WM_DELETE_WINDOW", command)
               
      if len(self.ui.box_text.get('0.0','end')) - 1 != 0: # Confirma si hay algo escrito en la caja

         if self.__ruta__ != '': # Confirma si hay archivo abierto
            text_box = self.ui.box_text.get('0.0','end')
            with open(self.__ruta__, 'r') as f: txt = f.read()
            
            if text_box != txt: 
               self.nameArch = obtener_nombre_arch(self.__ruta__)
               funcSalir(f'*{self.nameArch}: {self.titulo_name}', self.salir)

            else: 
               self.nameArch = obtener_nombre_arch(self.__ruta__)
               funcSalir(f'{self.nameArch}: {self.titulo_name}', self.func_salir)
               
         else: # NO hay archivo abierto
            funcSalir(f'*{self.titulo_default}', self.salir)

      else: # NO hay escrito en la caja  
         if self.__ruta__ == '': # NO hay archivo abierto
            funcSalir(self.titulo_default, self.func_salir)

      self.root.after(10, self.verificar_caja)     
   
   # ****************** Funciones Cerrar Ventana ****************** #
   def salir(self):
      valor = messagebox.askyesnocancel(
         self.titulo_name, "¿Quieres guardar los cambios de Sin titulo?", parent=self.root
      )

      if valor == True:  
         self.save_file()
         self.func_salir()

      if valor == False: self.func_salir()
   
   def func_salir(self): 
      self.root.destroy()
      self.root.quit()

if __name__ == '__main__': 
   Notepad()

#* Author: Francisco Velez
