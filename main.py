#VERSION 2.0

import requests
from bs4 import BeautifulSoup
import random
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from time import sleep

constante = -4

def crear_Inicio():
    window = Tk()
    window.geometry("983x590")
    ventana = VentanaPrincipal(window)
    window.resizable(False, False)
    window.mainloop()

def destroy_Window(window):
    window.destroy()

def new_game():
    pass

class MakeConnection:
    def __init__(self,artist):
        self.url = 'https://www.lyrics.com/artist/'
        self.artista = artist
        self.link = []
        self.names=[]
        self.make_Url()
        self.url_base = 'https://www.lyrics.com'
        self.get_Songs()

    def make_Url(self):
        if len(self.artista.split()) == 1:
            self.url = self.url + self.artista
        else:
            self.long = self.artista.split(' ')
            for x in self.long:
                self.url = self.url + x + '-'
            self.url = self.url[:-1]

    def get_Songs(self):
        self.query = requests.get(self.url)
        self.sopita = BeautifulSoup(self.query.text,'html.parser')
        self.canciones = self.sopita.find_all('td', {'class': 'tal qx' })
        self.url_base = 'https://www.lyrics.com'

        for song in self.canciones:
            self.aux = str(song.a)

            self.pos1 = self.aux.index('=')
            self.pos2 = self.aux.index('>')

            self.aux2 = self.aux[self.pos1:self.pos2]

            self.url_total= self.url_base + self.aux2[2:-1]

            self.link.append(self.aux2[2:-1])
            self.names.append(song.text)

class Juego:
    def __init__(self,window,dificultad,names,link,artist):
        self.wind = window
        self.wind.title('¿Qué tan fanático eres?')
        self.dificultad = dificultad
        self.felicitaciones = ['✅ ¡Muy bien! ','✅ ¡Eres muy bueno!','✅ ¡Sí que eres fan!','✅ ¡Te sabes todas!','✅ ¡Maravilloso!', '✅ ¡Si que sabes!']

        self.numerito = 0

        self.artistaEscogido = artist
        self.artistaEscogido = self.artistaEscogido.upper()
        self.puntos = 0
        self.vidas = 3

        self.namesj = names
        self.linkj = link

        self.color_fondo = 'SeaGreen3'

        self.img = ImageTk.PhotoImage(Image.open("fondo.png"))
        self.panel = Label(self.wind, image = self.img)
        self.panel.grid(row=0,column=0)

        self.nombreUsuario = Entry(self.wind)
        self.nombreUsuario.focus()
        self.nombreUsuario.place(x=427,y=365)

        self.message = Label(self.wind,text='000')#puntaje
        self.message.config(fg="white",    # Foreground
             bg=self.color_fondo,   # Background
             font=("Bangers",24+ constante))
        self.message.place(x = 825, y = 8)

        self.messageArtista = Label(self.wind,text=self.artistaEscogido)
        self.messageArtista.config(fg="medium turquoise",    # Foreground
             bg="white",   # Background
             font=("Bangers",20+ constante))
        self.messageArtista.place(x = 50, y = 95)

        self.messageVerso=Label(self.wind,text='',fg='red')
        self.messageVerso.config(fg="white",bg="medium turquoise", font=("Bangers",45+ constante))
        #self.messageVerso.place(x=200, y=200)
        self.messageVerso.place(relx=0.5, rely=0.38, anchor=CENTER)

        self.messageCorrect=Label(self.wind,text='')
        self.messageCorrect.config(fg='white',bg=self.color_fondo, font=("Bangers",24+ constante)) #cadeblue3
        #self.messageVerso.place(x=200, y=200)
        self.messageCorrect.place(relx=0.5, rely=0.585, anchor=CENTER) # rely = 0.1

        self.img2 = ImageTk.PhotoImage(Image.open("heart.png"))
        self.panel2 = Label(self.wind, image = self.img2,bg= self.color_fondo)
        self.panel2.place(x=825, y=58)

        self.img3 = ImageTk.PhotoImage(Image.open("heart.png"))
        self.panel3 = Label(self.wind, image = self.img3,bg= self.color_fondo)
        self.panel3.place(x=860, y=58)

        self.img4 = ImageTk.PhotoImage(Image.open("heart.png"))
        self.panel4 = Label(self.wind, image = self.img4,bg= self.color_fondo)
        self.panel4.place(x=895, y=58)

        self.get_Song()
        self.get_Verso()

        Button (self.wind, text=' ¡VAMOS! ',command= lambda: self.verificar(), bg="medium turquoise").place(x=617,y=363)
        Button (self.wind, text=' OTRO VERSO ',command= lambda: self.quitar_Puntos(), bg="medium turquoise").place(x=710,y=363)
        Button (self.wind, text=' MENÚ ',command= lambda: [destroy_Window(self.wind),crear_Inicio()], bg="medium turquoise").place(x=900,y=27)

    def get_Song(self):
        self.puntuacionProx = 10
        self.url_base = 'https://www.lyrics.com'

        self.max = len(self.namesj)
        self.salir = '1'
        self.contador = 0
        while True:
            self.num = random.randint(0, self.max-1)
            if '(' in self.namesj[self.num] or '[' in self.namesj[self.num]:
                pass
            else:
                break

        self.url_total= self.url_base + self.linkj[self.num] #index out of range

        self.query2 = requests.get(self.url_total)
        self.sopita2 = BeautifulSoup(self.query2.text,'html.parser')
        self.letra = self.sopita2.find_all('pre', {'id': 'lyric-body-text' })

    def get_Verso(self):
        for i in self.letra:
            #print(i.text)
            self.versos = i.text.split('\n')

        try:
            self.posicion = self.namesj[self.num].index('[')
        except:
            self.posicion = len(self.namesj[self.num]) - 1
            self.nombre = self.names[self.num].lower().split(' ')
        else:
            self.nombre = self.namesj[self.num][:self.posicion-1].lower().split(' ')

        try:
            self.posicion = self.namesj[self.num].index('(')
        except:
            self.posicion = len(self.namesj[self.num]) - 1
            self.nombre = self.namesj[self.num].lower().split(' ')
        else:
            self.nombre = self.namesj[self.num][:self.posicion-1].lower().split(' ')


        self.max2 = len(self.versos)-1
        while True:
            self.num2 = random.randint(0, self.max2)
            if self.versos[self.num2].lower().find(self.namesj[self.num][:self.posicion].lower()) == -1: #index out of range
                if len(self.versos[self.num2]) >= 15:
                    break

        print('Verso: ')
        print(self.versos[self.num2])
        print('Nombre: ')
        print(self.namesj[self.num][:self.posicion+1])

        if len(self.versos[self.num2]) <= 42:
            self.messageVerso.config(fg="medium turquoise",bg="white", font=("Bangers",45+ constante)) #verdana
            self.messageVerso['text'] = self.versos[self.num2]
        #59
        elif len(self.versos[self.num2]) <= 59:
            self.messageVerso.config(fg="medium turquoise",bg="white", font=("Bangers",34+ constante))#verdana
            self.messageVerso['text'] = self.versos[self.num2]

        else:
            self.messageVerso.config(fg="medium turquoise",bg="white", font=("Bangers",29+ constante))#verdana
            self.messageVerso['text'] = self.versos[self.num2]

    def verificar(self):
        self.nombre_u = self.nombreUsuario.get()
        self.nombre_u = self.nombre_u.lower().split(' ')

        if self.nombre == self.nombre_u:
            self.auxi = self.numerito
            while True:
                self.numerito = random.randint(0, len(self.felicitaciones) - 1)
                if self.numerito != self.auxi:
                    break
            self.messageCorrect['text'] = self.felicitaciones[self.numerito]


            print('****¡Muy bien, acertaste!****')
            self.puntos = self.puntos + self.puntuacionProx
            self.message['text'] = '0' + str(self.puntos)
            self.get_Song()
            self.get_Verso()
            self.nombreUsuario.delete(0,END)
            self.nombreUsuario.focus()


        else:
            self.vidas -= 1
            self.messageCorrect['text'] = ' 🚫 Nombre: ' + self.namesj[self.num][:self.posicion+1] #error


            if self.vidas == 2:
                self.img4 = ImageTk.PhotoImage(Image.open("heart_broken.png"))
                self.panel4 = Label(self.wind, image = self.img4,bg= self.color_fondo)
                self.panel4.place(x=895, y=58)

            elif self.vidas == 1:
                self.img3 = ImageTk.PhotoImage(Image.open("heart_broken.png"))
                self.panel3 = Label(self.wind, image = self.img3,bg= self.color_fondo)
                self.panel3.place(x=860, y=58)

            if self.vidas > 0:
                print('Lástima, el nombre era ',self.namesj[self.num][:self.posicion+1])
                self.nombreUsuario.delete(0,END)
                self.nombreUsuario.focus()
                self.get_Song()
                self.get_Verso()

            elif self.vidas == 0:
                self.img2 = ImageTk.PhotoImage(Image.open("heart_broken.png"))
                self.panel2 = Label(self.wind, image = self.img2,bg= self.color_fondo)
                self.panel2.place(x=825, y=58)
                self.game_Over()
            #self.wind.after(2000,self.errease(self.messageCorrect))

        #self.nombreUsuario("<Key>", self.errease)

    def errease(self):
        self.messageCorrect['text'] = ''

    def game_Over(self):
        self.messageCorrect2=Label(self.wind,text='❌ GAME OVER ❌')
        self.messageCorrect2.config(fg='red',bg='CadetBlue3', font=("Bangers",34 + constante)) #cadeblue3
        #self.messageVerso.place(x=200, y=200)
        self.messageCorrect2.place(relx=0.5, rely=0.1, anchor=CENTER) # rely = 0.1
        Button (self.wind, text=' JUGAR DE NUEVO ',command= lambda: [destroy_Window(self.wind),self.nuevo_Juego()], bg="medium turquoise").place(relx=0.5, rely=0.18, anchor=CENTER)
        Button (self.wind, text=' ¡VAMOS! ', bg="medium turquoise").place(x=617,y=363)
        Button (self.wind, text=' OTRO VERSO ', bg="medium turquoise").place(x=710,y=363)

    def nuevo_Juego(self):
        crear_Inicio()

    def quitar_Puntos(self):
        if self.puntuacionProx > self.dificultad:#DIFICULTAD FACIL 5 oportunidades, DIFICIL 2 oportunidades
            self.puntuacionProx -= 1
            self.get_Verso()

class VentanaPrincipal(MakeConnection,Juego):
    def __init__(self,window):
        self.wind = window
        self.wind.title('¿Qué tan fanático eres?')

        self.logotipo = LabelFrame(self.wind)
        self.logotipo.grid(row=0,column=0,pady=10)

        self.img = ImageTk.PhotoImage(Image.open("parrot.png"))
        self.panel = Label(self.logotipo, image = self.img)
        self.panel.grid(row=0,column=0)

        self.frame = Frame(self.wind)
        self.frame.place(x = 0,y = 0)
        self.frame.config(bg="medium turquoise")
        self.frame.config(bd=25)

        self.message=Label(self.frame,text='',fg='red')
        self.message.grid(row=0,column=0,columnspan=2,sticky= W + E)
        self.message.config(bg="medium turquoise",   # Background
             font=("arial",13 + constante))

        self.etiqueta = Label(self.wind,text= 'Nombre del artista')
        self.etiqueta.place(x = 490, y = 421)
        self.etiqueta.config(fg="white",    # Foreground
             bg="VioletRed2",   # Background
             font=("Bangers",23 + constante))

        self.artistaE = Entry(self.wind)
        self.artistaE.focus()
        #self.artistaE.grid(row=1,column=1,sticky= W+E)
        self.artistaE.place(x=520,y=421)
        self.artistaE.config(bg="white")

        self.opcion = IntVar()

        Radiobutton(self.frame, text="Fácil", variable=self.opcion, value=5, bg="medium turquoise").grid(row=3,column=0,sticky= E) #fg="white"
        Radiobutton(self.frame, text="Difícil", variable=self.opcion, value=8, bg="medium turquoise").grid(row=3,column=1,sticky= W)#fg="white"

        self.message2=Label(self.frame,text='',fg='red')
        self.message2.grid(row=2,column=0,columnspan=2,sticky= W + E)
        self.message2.config(bg="medium turquoise",   # Background
             font=("Bangers",5+ constante))

        self.message3=Label(self.frame,text='',fg='red')
        self.message3.grid(row=4,column=0,columnspan=2,sticky= W + E)
        self.message3.config(bg="medium turquoise",   # Background
             font=("Bangers",0+ constante))

        Button (self.frame, text='Iniciar',command= lambda: self.iniciar(), bg="medium turquoise").grid(row=5,column=0,sticky = W +E)
        Button (self.frame, text='Salir',command= lambda: quit(), bg="medium turquoise").grid(row=5,column=1,sticky = W +E )

    def iniciar(self):
        #print('Opcion escogida: ',self.opcion.get())

        self.message['text'] = ''
        self.artista = self.artistaE.get()
        self.artista = self.artista.lower()

        MakeConnection.__init__(self,self.artista)

        if len(self.names) == 0:
            self.message['text'] = '   Artista no encontrado, intenta con otro'
        else:
            #print(self.link[0:5])
            #print(self.names[0:5])
            #print(self.opcion.get())
            #get_Song()
            if self.opcion.get() == 0:
                self.message['text'] = '   Selecciona una dificultad'
            else:
                self.make_window_game()

    def make_window_game(self):
        self.wind.destroy()
        self.window = Tk()
        self.window.geometry("979x568")
        Juego.__init__(self,self.window,self.opcion.get(),self.names,self.link,self.artista)
        self.window.resizable(False, False)
        self.window.mainloop()


crear_Inicio()
