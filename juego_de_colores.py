#--------------------------------------------------------------------------
#-------------------------JUEGO DE COLORES---------------------------
#---------------Pertenece:Giovanni Gabriel Vilca Suelo---------------------
#---------------Curso:Arquitectura de Computadoras-------------------------
#--------------------------------------------------------------------------

#------------------------ Importación de librerías-------------------------
import cv2
import numpy as np
import random

#------- Inicialización de camara, contadores, variables y umbrales de color---
video = cv2.VideoCapture(0)   #Abre la Webcam
i=0                           #contador vertical, simula la bajada de un objetjo
b = random.randint(1,510)     #posición aleatoria en x
marcador=0                    #Marcador oficial
marcador_aux=0                #marcador para resetear
perdidas=0                    #marcador de notas falladas
verde_bajo = np.array ([40,100,0])   #Umbral bajo de color verde
verde_alto=np.array ([80,255,255])   #Umbral alto de color verde
roja_bajo= np.array ([0, 161, 0])    #Umbral bajo de color rojo
roja_alto = np.array([17,219, 255])  #Umbral alto de color rojo

#---------------------- Función para identificar colores---------------------
def captura_color(video, color_bajo, color_alto):
    #Esta función captura el video e identifica los colores que esten en el rango [color_bajo, color_alto]
    confirmacion, frame = video.read() #lee las capturas de la camara (video) y las muestra
    frame=cv2.flip(frame,1)            #evita el efecto espejo
    x=0                      #coordenada que se busca identificar el objeto de color en el video
    if confirmacion==True:   #Si se logran leer las capturas de la camara se confirmará

        # El modelo HSV (Hue, Saturation, Brightness – Matiz, Saturación, Brillo), 
        # define un modelo de color en términos de sus componentes. 

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)       #convierte de RGB a HSV
        mascara = cv2.inRange(frame_hsv, color_bajo, color_alto) #Crea la mascara dependiendo del rango de colores definido
        #Crea un contorno del objeto del color determinado que se muestra en el video 
        contorno, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
        for q in contorno:              #Mapea el contorno
            area = cv2.contourArea(q)   #Captura y calcula el area
            if area > 3000:
                M = cv2.moments(q)      #Obtiene los momentos de la imagen
                if (M["m00"] == 0): M["m00"]=1
                x = int(M["m10"]/M["m00"])      #Obtiene la coordenada en X del centroide
                y = 0      #No se calcula la coordenada en Y del centroide, aunque se utiliza en los pasos siguientes
                cv2.circle(frame, (x,y), 7, (0,255,0), -1)   #se obtiene un circulo colo centro en X e Y
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, '{},{}'.format(x,y),(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                nuevoContorno = cv2.convexHull(q)
                cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3)  #dibuja los nuevos contornos
    return x   #Retorna componente en X del centroide del objeto de color definido

#---------------------------- Inicio del juego---------------------------------
inicio = cv2.imread('./image/INICIO.png')   #Carga la imagen de inicio 
cv2.imshow('JUEGO DE COLORES', inicio)      #Vizualiza la ventana con la imagen de inicio

#Con el siguiente ciclo se bucará identificar un objeto de color rojo 
#para pasar de la imagen de inicio a jugar con un objeto de color verde

#------- Ciclo para detectar objeto rojo y comenzar a jugar--------------------
while True:
    check, frame=video.read()  #lee las capturas de la camara (video) y las muestra 
    frame=cv2.flip(frame,1)    #evita el efecto espejo
    cv2.imshow('', frame)      #Vizualiza la ventana con la imagen de la camara
    key2=cv2.waitKey(1)  #Condicion para vizualización de la ventana con la imagen de la camara y cierre de dicha ventana
    x_roja=captura_color(video, roja_bajo, roja_alto)  #Identifica objeto de color rojo y retorna su componente en X
    print(x_roja)                                      #Imprime la componente en X del objeto rojo encontrado
    if x_roja!=0:   #Si se logra identificar dicho objeto la componente de X será diferente de 0, entonces se cerrarán las ventanas
        cv2.destroyAllWindows() #Destruye las ventanas
        break                   #Cierra el ciclo

#------- Ciclo para detectar objeto verde y mover al personaje-----------------
#Una vez se cierra la imagen de inicio
#Se comienza a jugar con este nuevo ciclo
while True:
    #se cargan las imagenes que se van a mostrar en pantalla 
    fondo = cv2.imread('./image/fondo.png')              #640x480
    personaje = cv2.imread('./image/personaje.png')      #130x162
    nota_verde = cv2.imread('./image/nota_verde_1.png')  #70X32
    nota_roja = cv2.imread('./image/nota_roja_1.png')    #70X32
    fil,col, cap = personaje.shape                       #Se obtienen las dimensiones de la imagen del personaje
    check, frame=video.read()                            # lee las capturas de la camara (video) y las muestra   
    frame=cv2.flip(frame,1)                              #evita el efecto espejo
    x_verde=captura_color(video, verde_bajo, verde_alto)#Identifica objeto de color verde y retorna su componente en X
    if x_verde !=0:#Si se logra identificar dicho objeto la componente de X será diferente de 0, entonces continuara lo siguiente
        if x_verde+col<=640: #Identifica que el objeto verde se mantenga dentro de las dimenciones de la ventana de juego
            fondo[318:318+fil, x_verde:x_verde+col] = personaje #cambia parte del fondo por la imagen del personaje dependiendo de donde se ubique el objeto verde
            print(x_verde)#Imprime la coordenada X del objeto verde dependiendo de su ubicacion en la imagen de la camara
            fondo[i:i+32, b:b+70,:] = nota_verde#cambia parte del fondo por la imagen de la nota_verde dependiendo de la aleatoriedad de la variable b
            if i>=318 and i<=350 and b>=x_verde and b<=x_verde+col: #Cuando hay contacto entre la imagen de la nota y el personaje se hace un punto a favor
                marcador=marcador+1   #Aumenta el marcador 
                marcador_aux=marcador #Se necesita para refrescar la imagen del personaje
                if marcador_aux>0:    #Si se aumenta el marcador se debe cargar nuevamente el fondo y la imagen del personaje
                    fondo = cv2.imread('./image/fondo.png')             #Se carga la imagen del fondo
                    fondo[318:318+fil, x_verde:x_verde+col] = personaje #cambia parte del fondo por la imagen del personaje dependiendo de donde se ubique el objeto verde
                    #Reincio de marcadores y variables
                    i=0 
                    b = random.randint(1,510) 
                    marcador_aux=0
    
            # cv2.putText(fondo, 'MARCADOR: '+str(marcador), (530,15),cv2.FONT_HERSHEY_DUPLEX, 0.5,(255,255,255),1) 
            # cv2.putText(fondo, 'PERDIDAS: '+str(perdidas),(530,30),cv2.FONT_HERSHEY_DUPLEX, 0.5,(255,255,255),1) 
        
        # else:
        #     fondo = cv2.imread('./image/fondo.png')
    else:#Si no se logra identificar el objeto quiere decir que está por fuera de la pantalla
        fondo = cv2.imread('./image/fondo.png') #Carga la imagen de fondo
        cv2.putText(fondo, 'FAVOR MOSTRAR OBJETO VERDE ', (80, 200),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2)
        cv2.putText(fondo, 'EN CAMARA, UBICA PARA JUGAR', (80, 250), cv2.FONT_HERSHEY_DUPLEX, 1,(255,255,255),2) 
    #Escribe y actualiza el marcador de puntos a favor en la imagen de fondo
    cv2.putText(fondo, 'MARCADOR: '+str(marcador), (530,15),cv2.FONT_HERSHEY_DUPLEX, 0.5,(255,255,255),1) 
    #Escribe y actualiza el marcador de puntos en contra en la imagen de fondo
    cv2.putText(fondo, 'PERDIDAS: '+str(perdidas),(530,30),cv2.FONT_HERSHEY_DUPLEX, 0.5,(255,255,255),1)
    if marcador==5 or perdidas==5: #Cuando de tengan 5 puntos en contra o a favor se termina el juego
        break                      #Cierra el ciclo
    cv2.imshow('JUEGO DE COLORES', fondo) #Muestra la ventana donde se va a jugar
    cv2.imshow('', frame)               #Muestra la imagen de la camara simultaneamente con la ventana del juego
    key = cv2.waitKey(1)                #Condicion para vizualización de las ventanas y cierre de dichas ventanas
    if key==ord('q') or key==ord('Q'):    #Al presionar la letra Q en mayuscula o nimuscula se cerrará el juego
        break 
    i=i+10    #Contador vertical para la bajada de la nota_verde
    #Si la nota baja a mas de 350 en Y no se podrá haer punto a favor, igual si la nota llega a 420 en Y se 
    # confirma el punto en contra
    #Reinicio de contadores
    if i>=420:    
        i=0
        b = random.randint(1,510) 
    #Aumenta marcador de puntos en contra
        perdidas=perdidas+1
# video.release() 
cv2.destroyAllWindows()        #Destruye las ventanas

#------- Carga de imagenes y definición de ganar, perder, o retirarse----------
fondo = cv2.imread('./image/fondo.png')        #Carga imagen de fondo 
ganador = cv2.imread('./image/you_rock.png')   #Carga imagen de ganador 
perdedor = cv2.imread('./image/GAME_OVER.png') #Carga imagen de perdedor 
retiro=cv2.imread('./image/retiro.png')        #Carga imagen de retiro 

#------- Ciclo para detectar objeto rojo y finalizar el juego------------------
if marcador==5:#Si se llega a 5 puntos a favor se carga la imagen de ganador y pide mostrar objeto rojo para salir
    fondo=ganador
    cv2.putText(fondo, 'GANASTE',(250,50),cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0), 2) 
    cv2.putText(fondo, 'Muestra objeto rojo para salir', (80,450),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 3) 
elif perdidas==5:#Si se llega a 5 puntos en contra se carga la imagen de perdedor y pide mostrar objeto rojo para salir
    fondo=perdedor
    cv2.putText(fondo, 'PERDISTE', (250, 50),cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2) 
    cv2.putText(fondo, 'Muestra objeto rojo para salir', (80,450),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)
else:#Si se presiona la letra Q se carga la imagen de retiro y pide mostrar objeto rojo para salir
    fondo=retiro
    cv2.putText(fondo, 'SALISTE', (400, 100),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255), 2) 
    cv2.putText(fondo, 'Muestra objeto rojo para salir',(80,450),cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)
cv2.imshow('RESULTADO', fondo)#dependiendo de si gano, perdió o se retiró el usuario se mostrará la imagen respectiva

while True:#Se inicia otro ciclo para salir del juego, al igual que al comeinzo se busca un objeto rojo para salir
    check, frame=video.read() # lee las capturas de la camara (video) y las muestra 
    frame=cv2.flip(frame,1)#evita el efecto espejo
    cv2.imshow('', frame) #Vizualiza la ventana con la imagen de la camara
    key2=cv2.waitKey(1)#Condicion para vizualización de la ventana con la imagen de la camara y cierre de dicha ventana
    x_roja=captura_color(video, roja_bajo, roja_alto)#Identifica objeto de color rojo y retorna su componente en X
    print(x_roja)#Imprime la componente en X del objeto rojo encontrado
    if x_roja!=0:#Si se logra identificar dicho objeto la componente de X será diferente de 0, entonces se cerrarán las ventanas
        video.release()  #Apaga la camara  
        cv2.destroyAllWindows() #Destruye las ventanas
        break#Cierra el ciclo    