# Bloc de notas

#* Importa las librerias nesesarias
import time, json

info = {
    "Font": ["arial", "20", "bold"],
    "bg": "#1a1a1a",
    "fg": "#00ffff",

    "selectbackground": "default",
    "selectforeground": "default",
    "insertbackground": "default",
    
    "Author": "Francisco J. Velez O."
}

def lectura(ruta=''):
      with open(ruta, 'r') as file:
         return file.read()

def rescribir(ruta='', mensaje=''):
      with open(ruta, 'w') as file:
         file.write(mensaje)


def actualizar_(Font, bg, fg, selectbackground, selectforeground, insertbackground):
      inf = json.loads(lectura('./config.json'))

      inf['selectbackground'] = selectbackground 
      inf['selectforeground'] = selectforeground 
      inf['insertbackground'] = insertbackground 

      inf['Font'] = Font
      inf['bg'] = bg
      inf['fg'] = fg
      
      rescribir('./config.json', json.dumps(inf, indent=4))

def obtener_nombre_arch(ruta=''):
   return ruta.split('/')[-1]

def obtener_tiempo():
      return time.strftime('%H:%M %d/%m/%Y')

def informacion(nameArch='config.json'):
   inf = json.loads(lectura(nameArch))
   
   return [
         inf['Font'], inf['bg'], inf['fg'], 
         inf['selectbackground'], inf['selectforeground'], 
         inf['insertbackground']
   ]

#* Author: Francisco Velez
