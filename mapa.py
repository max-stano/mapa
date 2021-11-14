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
  


    #pre kazdy riadok mapy precitaj kazdy riadok a vytvor z nich zoznam (rozsah je po vysku)
    for y in range(0, vyska):
       riadok= subor.readline()
       mapa.append(list(riadok))
    #uzavri subor
    subor.close()
    

                
    # tieto hodnoty nam vrati z funkcie            
    return sirka, vyska, mapa

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



# rozmery mapy
sirkamapy = 20
vyskamapy = 0

# rozmer policka (px)
cell_size = 80

######################################################


okno = tkinter.Tk()
okno.title ('moja hra')

#nacitaj zo suboru mapu a vratene hodnoty uloz do premennych.
#vsetky nazvy premennych sesdia s lokalnymi premennymi, ale nie su to totozne
#premenne. 
sirka, vyska, mapa = nacitaj_mapu('textak.txt')

# obrazok si musime odlozit v premennej, ktora prezije platno a preto je globalna
obrazok = tkinter.PhotoImage (file= 'wall.gif')


# volame funkciu vytvor_platno tak, ze ju priradime do premennej. v zatvorke musia byt nazvy vsetkych premennych, ktore potrebuje na inicializaciu
platno = vytvor_platno(okno, sirka, vyska, mapa, cell_size, obrazok)




okno.mainloop()
terminate = True



