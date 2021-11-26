import tkinter
import threading
import random
import time

######################################################

def nacitaj_mapu(cesta):
    #vytvorime cestu k suboru, ktory budeme pouzivat
    subor = open('textak.txt')
    #z prveho riadku v subore nacitame sirku
    sirka = int(subor.readline())
    # z druheho riadku v subore nacitame vysku
    vyska = int(subor.readline())
    # vytvorime premennu mapa, ktora je zoznam - list
    mapa = []
    pac_found = False
    duch_found = False
    duch1_found = False


    #pre kazdy riadok mapy precitaj kazdy riadok a vytvor z nich zoznam (rozsah je po vysku)
    for y in range(0, vyska):
       riadok = subor.readline()
       mapa.append(list(riadok))
    #uzavri subor
    subor.close()

   #prehladavame maticu mapy (riadky, stlpce) a hladame umiestnenie postavičky a potvorky a v scene
    for y in range(0, vyska):
        #ak sme ich oboch nasli, tak vybehni z cyklu
        if pac_found and duch_found:
            break;
        for x in range(0, sirka):
            #ak na sucasnom policku sa ma nachadzat postavicka...
            if mapa[y][x] == 'g':
                #tak to prepiseme na volne policko a ulozime si poziciu a zmenime
                #najdenie pacmana na True, aby sme vybehli z vonkajsieho cyklu von
                mapa[y][x] = ' '
                pac_x = x
                pac_y = y
                pac_found = True
            elif mapa[y][x] == 'b':
                mapa[y][x] = ' '
                duch_x = x
                duch_y = y
                duch_found = True
            elif mapa[y][x] == 'h':
                mapa[y][x] = ' '
                duch1_x = x
                duch1_y = y
                duch1_found = True
                
                if pac_found and duch_found:
                    break;

                
    # tieto hodnoty nam vrati z funkcie            
    return sirka, vyska, mapa, pac_x, pac_y, duch_y, duch_x, duch1_x, duch1_y

######################################################

def vytvor_platno(okno, sirka, vyska, mapa, cell_size, stena):
    #iniciuj podkladove
    platno = tkinter.Canvas (okno, \
                             width = sirka * cell_size, \
                             height = vyska * cell_size)
    platno.config (bg='light pink') #- zadaj nejaku farbu pozadia
    platno.pack ()

    #ak je polozka v poli rovna #, tak vytvor obrazok pre stenu (rozsah je po vysku, resp sirku)
    for y in range(0, vyska):
        for x in range(0, sirka):
            if mapa[y][x] == '#':
                platno.create_image (x * cell_size + sirka / 2, \
                                     y * cell_size + vyska / 2, \
                                     image=stena)
    #vrati nakreslene platno
    return platno


######################################################
        
# mapa - steny a prechody (1. index - vyska, 2. index sirka)
mapa = []

# pozicia panacika v scene
pac_x = 0
pac_y = 0

duch_x = 0
duch_y = 0

duch1_y = 0
duch1_x = 0

# rozmery mapy
sirkamapy = 20
vyskamapy = 0

# rozmer policka (px)
cell_size = 80

######################################################

def pacmanmove (event):
    #musime mu zadat globalne premenne - definovali sme ich mimo tejto funkcie
    #, s ktorymi bude pracovat aj tato fcia
    global pac_x
    global pac_y
    global platno
    global pacman
    global cell_size
    global mapa
    global skore
    global gulicky
    global okno

    #pripravime si premenne pre poziciu pacmana po posunuti
    target_x = pac_x
    target_y = pac_y

    #podla stlacenej klavesy nastavime cielovu poziciu pacmana - 1 neznamena
    #pixel ale policko
    
    if event.keysym == 'Up':
        target_y -= 1
    elif event.keysym == 'Down':
        target_y += 1
    elif event.keysym == 'Left':
        target_x -= 1
    elif event.keysym == 'Right':
        target_x += 1

    #ak je cielove policko prazdne, tak priradime nove suradnice
    #musime mysliet na to, ze berie do uvahy stred obrazku, aby
    #sme nevosli do steny
    if mapa[target_y][target_x] != '#':
        #zapamatame si nove suradnice pacmana
        pac_x = target_x
        pac_y = target_y
        #posunieme obrazok
        platno.coords(pacman, \
                      target_x * cell_size + cell_size / 2, \
                      target_y * cell_size + cell_size / 2)

    global duch_x
    global duch_y
    global duch1_x
    global duch1_y


#########################################################
okno = tkinter.Tk()
okno.title ('moja hra')

#nacitaj zo suboru mapu a vratene hodnoty uloz do premennych.
#vsetky nazvy premennych sesdia s lokalnymi premennymi, ale nie su to totozne
#premenne. 
sirka, vyska, mapa, pac_x, pac_y, duch_x, duch_y = nacitaj_mapu('textak.txt')

# obrazok si musime odlozit v premennej, ktora prezije platno a preto je globalna
obrazok = tkinter.PhotoImage (file= 'wall.gif')


# volame funkciu vytvor_platno tak, ze ju priradime do premennej. v zatvorke musia byt nazvy vsetkych premennych, ktore potrebuje na inicializaciu
platno = vytvor_platno(okno, sirka, vyska, mapa, cell_size, obrazok)

#nacitame data k obrazku a zobrazime ho na konkretnych suradniciach
pacman_data = tkinter.PhotoImage (file= 'pacman.gif')
pacman = platno.create_image (pac_x * cell_size + cell_size / 2, \
                              pac_y * cell_size + cell_size / 2, \
                              image=pacman_data)

duch_data = tkinter.PhotoImage (file= 'duch.gif')
duch = platno.create_image (duch_x * cell_size + cell_size / 2, \
                            duch_y * cell_size + cell_size / 2, \
                            image=duch_data)

duch1_data = tkinter.PhotoImage (file= 'duch1.gif')
duch1 = platno.create_image (duch1_x * cell_size + cell_size / 2, \
                            duch1_y * cell_size + cell_size / 2, \
                           image=duch1_data)

duch_smer = 3
terminate = False

platno.bind_all ('<KeyPress-Up>', pacmanmove)
platno.bind_all ('<KeyPress-Down>', pacmanmove)
platno.bind_all ('<KeyPress-Left>', pacmanmove)
platno.bind_all ('<KeyPress-Right>', pacmanmove)
platno.bind_all ('<KeyPress-Escape>', lambda key: okno.destroy())


okno.mainloop()
terminate = True
