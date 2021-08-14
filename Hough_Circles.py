import cv2 
import numpy as np 

#Cálculo de distancias
def distancia(puntos, img):
    if len(puntos) == 2:
        x1, y1, w1, h1 = puntos[0]
        x2, y2, w2, h2 = puntos[1]
        cv2.rectangle(img, (x1-w1, y1-h1), (x1+w1, y1+h1), (255, 0, 0), 1)
        cv2.rectangle(img, (x2-w2, y2-h2), (x2+w2, y2+h2), (255, 0, 0), 1)
        if x1 < x2:
            distancia_pixeles = abs(x2-w2 - (x1-w1)) #Cálculo de dsitancia en pixeles
            distancia_cm = (distancia_pixeles*29.7)/720 #Cálculo de distancia en cm
            cv2.putText(img, "{:.2f} cm".format(distancia_cm), (x1+w1+distancia_pixeles//2, y1-30), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
            cv2.line(img,(x1,y1-20),(x2, y1-20),(0, 0, 255),2) #Línea horizontal
            cv2.line(img,(x1+w1,y1-30),(x1+w1, y1-10),(0, 0, 255),2)
            cv2.line(img,(x2-w2,y1-30),(x2-w2, y1-10),(0, 0, 255),2)
            cv2.waitKey(0)
        else:
            distancia_pixeles = abs(x1 - (x2+w2)) #Cálculo de dsitancia en pixeles
            distancia_cm = (distancia_pixeles*29.7)/720 #Cálculo de distancia en cm
            cv2.putText(img, "{:.2f} cm".format(distancia_cm), (x2+w2+distancia_pixeles//2, y2-30), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
            cv2.line(img,(x2,y2-20),(x1, y2-20),(0, 0, 255),2) #Línea horizontal
            cv2.line(img,(x2,y2-30),(x2, y2-10),(0, 0, 255),2)
            cv2.line(img,(x1,y2-30),(x1, y2-10),(0, 0, 255),2)
            cv2.imshow('img',img)
            cv2.waitKey(0)
            #cv2.imshow('frame',frame)   
        #k = cv2.waitKey(1) & 0xFF
        #if k == 27:
        #    break
    else:
        print("Se han detectado más de 2 circulos")
        print("Verifique que el lugar este bien iliminado")




#cap = cv2.VideoCapture(0)
#ret, frame = cap.read()
#cap.release()
#img = frame

# Imagen original
img = cv2.imread('dos_limones.jpeg', cv2.IMREAD_COLOR)
cv2.imshow('Original', img)
cv2.waitKey(0)

# Convertir a escala de grises
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
#cv2.imshow('Grigio', gray) # grigio es en italiano, pero no se asusten, no tiene Coreanovirus
#cv2.waitKey(0)

# Ahora se aplica un filtro pasabajas de 3x3
gray_blurred = cv2.blur(gray, (11, 11)) 
cv2.imshow('Borrosa', gray_blurred )
cv2.waitKey(0)

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
detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 15, param1 = 20, param2 = 30, minRadius = 60, maxRadius = 80) 
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
        cv2.waitKey(0)

distancia(puntos, img)
cv2.destroyAllWindows()