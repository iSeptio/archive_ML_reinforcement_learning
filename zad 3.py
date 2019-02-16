import numpy as np
import matplotlib.pyplot as plt

# Tworzenie mapy kar i nagród 
mapa = np.zeros((10,10))
for i in range (10):
    mapa[i ,  0] = -10
    mapa[i ,  9] = -10
    mapa[9,  i] = -10
    mapa[0 ,  i] = -10

przeszkody = [[1,4], [ 3,1 ] , [3,2] , [3 ,7] , [3,8] , [4 ,5] ,[4,6],[4,7] ,[5,4],[5,5],[6,3],[6,4],[7,3]]
wartosc_przeszkody = [ 14 ,9,9 ,10,10 ,9,9,9,9,9,9,9,9]
k=0
for i in przeszkody:
    mapa[i[0],i[1]] = -10
    k+=1   
mapa[8,7 ] = 10

# Poruszanie się po mapie 
def akcja(pozycja):  
    
    
    zrobiono_ruch = 0 
    ruch = np.random.choice(['down','up','right','left'])
    
    while zrobiono_ruch == 0 :
        if ruch == 'up' :
            if pozycja[0]!= 0:
                pozycja = [pozycja[0]-1 , pozycja[1]]
                zrobiono_ruch = 1
            else :
                ruch = np.random.choice(['down','right','left'])
        
        elif ruch == 'down' :
            if pozycja[0]!= mapa.shape[0] -1 :
                pozycja = [pozycja[0]+1 , pozycja[1]]
                zrobiono_ruch = 1
            else :
                ruch = np.random.choice(['up','right','left'])

                
        elif ruch == 'right': 
            if pozycja[1]!= mapa.shape[1] -1 :
                pozycja = [pozycja[0] , pozycja[1]+1]
                zrobiono_ruch = 1
            else : 
                ruch = np.random.choice(['up','down','left'])

        
        elif ruch == 'left' :
            if pozycja[1]!= 0:
                pozycja = [pozycja[0] , pozycja[1]-1]
                zrobiono_ruch = 1
            else :
                ruch = np.random.choice(['up','down','right'])
                
        
        
    return pozycja 

# Algorytm uczenia 
uu = np.zeros((10,10))
dd = np.zeros((10,10))
rr = np.zeros((10,10))
ll = np.zeros((10,10))
start = [1,1] 
alfa = 0.7
beta = 0.8
for i in range(7000):
    pole_nastepne = akcja(start)
    if pole_nastepne == [start[0]-1,start[1]]:
        uu[start[0],start[1]] += beta*(mapa[start[0] , start[1]] +alfa*np.max([uu[pole_nastepne[0],pole_nastepne[1]],dd[pole_nastepne[0],pole_nastepne[1]],rr[pole_nastepne[0],pole_nastepne[1]],ll[pole_nastepne[0],pole_nastepne[1]]])  - uu[start[0],start[1]])
    elif pole_nastepne == [start[0],start[1]+1]:
        rr[start[0],start[1]] += beta*(mapa[start[0] , start[1]] +alfa*np.max([uu[pole_nastepne[0],pole_nastepne[1]],dd[pole_nastepne[0],pole_nastepne[1]],rr[pole_nastepne[0],pole_nastepne[1]],ll[pole_nastepne[0],pole_nastepne[1]]])  - rr[start[0],start[1]])
    elif pole_nastepne == [start[0]+1,start[1]]:
        dd[start[0],start[1]] += beta*(mapa[start[0] , start[1]] +alfa*np.max([uu[pole_nastepne[0],pole_nastepne[1]],dd[pole_nastepne[0],pole_nastepne[1]],rr[pole_nastepne[0],pole_nastepne[1]],ll[pole_nastepne[0],pole_nastepne[1]]])  - dd[start[0],start[1]])
    elif pole_nastepne == [start[0],start[1]-1]:
        ll[start[0],start[1]] += beta*(mapa[start[0] , start[1]] +alfa*np.max([uu[pole_nastepne[0],pole_nastepne[1]],dd[pole_nastepne[0],pole_nastepne[1]],rr[pole_nastepne[0],pole_nastepne[1]],ll[pole_nastepne[0],pole_nastepne[1]]])  - ll[start[0],start[1]])
    start = pole_nastepne
    
plt.figure(figsize=(15,15))
plt.subplot(141)
plt.imshow(uu)
plt.title("Mapa Q : Góra ")
plt.subplot(142)
plt.imshow(dd)
plt.title("Mapa Q : Dół ")
plt.subplot(143)
plt.imshow(rr)
plt.title("Mapa Q : Prawo ")
plt.subplot(144)
plt.imshow(ll)
plt.title("Mapa Q : Lewo")
print("------------------------------------- Uczenie funkcji Q : 7000 iteracji ----------------------------------------------")

# Sprawdzanie poprawności poruszania się 
mapa_poruszania = mapa.copy()
start = [1,1]
while start!=[8,7]:
    pole_nastepne = start
    kierunek = np.argmax([uu[pole_nastepne[0],pole_nastepne[1]],dd[pole_nastepne[0],pole_nastepne[1]],rr[pole_nastepne[0],pole_nastepne[1]],ll[pole_nastepne[0],pole_nastepne[1]]])
    if kierunek == 0 :
        pole_nastepne = [pole_nastepne[0]-1,pole_nastepne[1]]
    elif kierunek == 1:
        pole_nastepne = [pole_nastepne[0]+1,pole_nastepne[1]]
    elif kierunek == 2:
        pole_nastepne = [pole_nastepne[0],pole_nastepne[1]+1]
    elif kierunek == 3:
        pole_nastepne = [pole_nastepne[0],pole_nastepne[1]-1]
        
    start = pole_nastepne
    
    mapa_poruszania[pole_nastepne[0],pole_nastepne[1]] = 12
    
plt.figure(figsize=(15,15))
plt.subplot(121)
plt.title("Mapa nagród ")
plt.imshow(mapa)
plt.subplot(122)
plt.title("Poruszanie się agenta po mapie Q - 7000 iteracji")
plt.imshow(mapa_poruszania)

# --- zad4 --- ?#


