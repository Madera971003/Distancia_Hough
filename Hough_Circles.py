import cv2 
import numpy as np
import time 
from time import time

#Cálculo de distancias
def distancia(puntos, img):
    if len(puntos) == 2:
        x1, y1, w1, h1 = puntos[0]
        x2, y2, w2, h2 = puntos[1]
        cv2.rectangle(img, (x1-w1, y1-h1), (x1+w1, y1+h1), (255, 0, 0), 1)
        cv2.rectangle(img, (x2-w2, y2-h2), (x2+w2, y2+h2), (255, 0, 0), 1)
        if x1 < x2:
            distancia_pixeles = abs(x2 - x1) #Cálculo de dsitancia en pixeles
            distancia_cm = (distancia_pixeles)/21.5 #Cálculo de distancia en cm
            cv2.putText(img, "{:.2f} cm".format(distancia_cm), (x1+w1+distancia_pixeles//2, y1-30), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
            cv2.line(img,(x1,y1-20),(x2, y1-20),(0, 0, 255),2) #Línea horizontal
            cv2.line(img,(x1,y1-30),(x1, y1-10),(0, 0, 255),2)
            cv2.line(img,(x2,y1-30),(x2, y1-10),(0, 0, 255),2)
            cv2.imshow('img',img)
            #cv2.waitKey(0)
        else:
            distancia_pixeles = abs(x1 - x2) #Cálculo de dsitancia en pixeles
            distancia_cm = (distancia_pixeles)/21.5 #Cálculo de distancia en cm
            cv2.putText(img, "{:.2f} cm".format(distancia_cm), (x2+w2+distancia_pixeles//2, y2-30), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
            cv2.line(img,(x2,y2-20),(x1, y2-20),(0, 0, 255),2) #Línea horizontal
            cv2.line(img,(x2,y2-30),(x2, y2-10),(0, 0, 255),2) #Línea izquierda
            cv2.line(img,(x1,y2-30),(x1, y2-10),(0, 0, 255),2) #Línea derecha
            cv2.imshow('img',img)
            #cv2.waitKey(0)
            #cv2.imshow('frame',frame)   
        #k = cv2.waitKey(1) & 0xFF
        #if k == 27:
        #    break
    else:
        print("Se han detectado 1 o más de 2 circulos")
        print("Verifique que el lugar este bien iluminado")

def ordenar_puntos(puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])
    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])
    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

#region de interes
def roi(image, ancho, alto):
    imagen_alineada = None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    #cv2.imshow('th', th)
    cnts = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
    #deteccion de vertices
    for c in cnts:
        epsilon = 0.01*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        if len(approx) == 4:
            puntos = ordenar_puntos(approx)            
            pts1 = np.float32(puntos)
            pts2 = np.float32([[0,0], [ancho,0], [0,alto], [ancho,alto]])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            imagen_alineada = cv2.warpPerspective(image, M, (ancho,alto))
    return imagen_alineada

def main(cap):
    # Imagen original
    #cap = cv2.imread('cir1.jpg', cv2.IMREAD_COLOR)
    #ret, frame = cap.read()
    img = roi(cap, ancho=600, alto=465)
    #cv2.imshow('Original', img)
    #cv2.waitKey(0)

    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    #cv2.imshow('Grigio', gray) # grigio es en italiano, pero no se asusten, no tiene Coreanovirus
    #cv2.waitKey(0)

    # Ahora se aplica un filtro pasabajas de 3x3
    gray_blurred = cv2.blur(gray, (11, 11)) 
    #cv2.imshow('Borrosa', gray_blurred )
    #cv2.waitKey(0)

    # Aplicar la tranfromada de Hough para detección de círculos
    # parámetros:
    # imagen a la cual se le va a aplicar
    # método de detección a realizar, por lo general se utiliza HOUGH_GRADIENT
    # relación inversa de la resolución del acumulador, si no se gusta meter en líos, lo ideal es usar 1, pues se tiene la misma resolución que la imagen
    # diatancia mínima (en pixeles) entre el centro y las circunferencias detectadas
    # param1, En el caso de utilizar el método HOUGH_GRADIENT, es el umbral máximo en la detección de bordes por Canny
    # param2, En el caso de utilizar el método HOUGH_GRADIENT, es el umbral mínimo en la detección de bordes por Canny
    # minRadius, es el radio mínimo del círculo (no se interpone con la distancia mínima entre el centro y la circunferencia)
    # maxRadius, es el radio mínimo del círculo (no se interpone con la distancia mínima entre el centro y la circunferencia)
    detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 15, param1 = 20, param2 = 30, minRadius = 30, maxRadius = 80) 
    # Revisar que el método haya regresado algún valor
    if detected_circles is not None: 
        # Convertir los parámetros el círculo a, b, y r en enteros de 16 bits
        detected_circles = np.uint16(np.around(detected_circles))
        puntos = []
        # Ahora si se recorren todos los círculos detectados
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
            # Dibujar la circunferencia
            datos = [a, b, r, r]
            puntos.append(datos)
            cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
            # Mostrar los datos de las circunferencias
            print("Centro ({:}, {:}), radio = {:}".format(a, b, r))
            # Dibujar un círculo pequeño alrededor del centro
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
            # Ir mostradndo las circunferencias detectadas
            cv2.imshow("Detección de circunferencias", img) 
            #cv2.waitKey(0)
        
        distancia(puntos, img)

#Llamada para cálculo de distancia

#cap = cv2.VideoCapture('video1.mp4')
cap = cv2.VideoCapture(0)
#cap.release()
#img = frame
while True:
    ret, frame = cap.read()
    if ret == False: 
        print("No se detecta imágen")
        break
    elif cv2.waitKey(1) & 0xFF == ord('s'): #Detener el proceso con s en 64 bits
        break
    cv2.imshow('Video', frame)
    main(frame)
    
cap.release()

#start_time = time()
#main()
#final_time = time()-start_time
#print("Tiempo: %.10f seg" %final_time)

cv2.destroyAllWindows()