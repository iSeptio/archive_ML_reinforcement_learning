import numpy as np
import matplotlib.pyplot as plt

#Tworzenie macierzy kar i nagród 
mapa = np.zeros((10,10))

for i in range (10):
    mapa[i ,  0] = -7
    mapa[i ,  9] = -10
    mapa[9,  i] = -5
    mapa[0 ,  i] = -12

przeszkody = [[1,4], [ 3,1 ] , [3,2] , [3 ,7] , [3,8] , [4 ,5] ,[4,6],[4,7] ,[5,4],[5,5],[6,3],[6,4],[7,3]]
wartosc_przeszkody = [ 14 ,9,9 ,10,10 ,9,9,9,9,9,9,9,9]
k=0
for i in przeszkody:
    mapa[i[0],i[1]] = -wartosc_przeszkody[k]
    k+=1   
mapa[8,7 ] = 10
mapa_1 = np.copy(mapa)

# funkcja poruszania siępo mape
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

# funkcja wybierania drogi dla 2 zadania 
def mm ( pozycja , mapa_urz)   :  
    
    zrobiono_ruch = 0
    if pozycja[0]!= 0:
        up = mapa_urz[pozycja[0]-1,pozycja[1]]
    else :
        up = - np.inf
        
    if pozycja[0]!= mapa.shape[0] -1:
        down = mapa_urz[pozycja[0]+1,pozycja[1]]
    else :
        down = -np.inf
        
    if pozycja[1]!= mapa.shape[1] -1 :
        right = mapa_urz[pozycja[0],pozycja[1]+1]
    else :
        right = -np.inf
        
    if pozycja[1]!= 0:
        left = mapa_urz[pozycja[0],pozycja[1]-1]
    else :
        left = -np.inf
    
        
       
    max_urz = np.argmax([ up , down , right ,left ])
        
       
    while zrobiono_ruch == 0 :
        if max_urz  == 0 :
            if pozycja[0]!= 0:
                pozycja = [pozycja[0]-1 , pozycja[1]]
                zrobiono_ruch = 1
            else :
                max_urz = np.argmax([  down , right ,left ])

        elif max_urz  == 1 :
            if pozycja[0]!= mapa.shape[0] -1 :
                pozycja = [pozycja[0]+1 , pozycja[1]]
                zrobiono_ruch = 1
            else :
                max_urz = np.argmax([ up ,right ,left ])


        elif max_urz  == 2 : 
            if pozycja[1]!= mapa.shape[1] -1 :
                pozycja = [pozycja[0] , pozycja[1]+1]
                zrobiono_ruch = 1
            else : 
                max_urz = np.argmax([ up , down  ,left ])

        elif max_urz  == 3  :
            if pozycja[1]!= 0:
                pozycja = [pozycja[0] , pozycja[1]-1]
                zrobiono_ruch = 1
            else :
                max_urz = np.argmax([ up , down , right  ])
    return pozycja

# Algorytm uczenia dla 1 zadania
mapa_urz = np.zeros((10,10))
start = [1,1]
for i in range(80000):
    if start == [8,7]:
        start = [1,1]
        pole_nastepne = akcja(start) 
    pole_nastepne = akcja(start) 
    mapa_urz[start[0],start[1]] += 0.015*(mapa[start[0],start[1]] + mapa_urz[pole_nastepne[0],pole_nastepne[1]] - mapa_urz[start[0],start[1]])
    start = pole_nastepne

# algorytm uczenia dla 2 zadania
mapa_urz_beta = np.zeros((10,10))
start = [1,1]
for i in range(15000):
    beta = np.random.rand()
    if start == [8,7]:
        start = [1,1]
        pole_nastepne = akcja(start) 
    pole_nastepne = akcja(start) 
    mapa_urz_beta[start[0],start[1]] += 0.13*(mapa[start[0],start[1]] + mapa_urz_beta[pole_nastepne[0],pole_nastepne[1]] - mapa_urz_beta[start[0],start[1]])
    if beta < 0.95:
        start = pole_nastepne
    else :
        start = mm(start ,mapa_urz_beta)
        
# Poruszanie się po mapie dla 1 i 2 zadania 
mapa_poruszania_beta = mapa_urz_beta.copy()
mapa_poruszania = mapa_urz.copy()
start = [1,1]

while start !=[8,7] :
    pole_nastepne = mm(start , mapa_urz)
    mapa_poruszania[pole_nastepne[0],pole_nastepne[1]] = -200
    start = pole_nastepne
    
start = [1,1]

while start !=[8,7] :
    pole_nastepne = mm(start , mapa_urz)
    mapa_poruszania_beta[pole_nastepne[0],pole_nastepne[1]] = -200
    start = pole_nastepne

plt.figure(figsize=(15,15))
plt.subplot(131)
plt.title("Mapa użyteczności - 80000 iteracji")
plt.imshow(mapa_urz)

plt.subplot(132)
plt.title("Mapa użyteczności + beta  - 15000 iteracji")
plt.imshow(mapa_urz_beta)

plt.subplot(133)
plt.title("Mapa nagród i kar ")
plt.imshow(mapa)

plt.show()

plt.figure(figsize=(10,10))
plt.subplot(121)
plt.title("Poruszanie się agenta- 80000 iteracji")
plt.imshow(mapa_poruszania )

plt.subplot(122)
plt.title("Poruszanie się agenta + beta - 15000 iteracji")
plt.imshow(mapa_poruszania_beta)


