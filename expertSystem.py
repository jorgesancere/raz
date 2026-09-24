'''
 Sistema Experto para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control 
 y guiado de un robot móvil sobre un plano cartesiano

 Creado por: Diego Viejo
 el 11/09/2026


'''

from objetivo import *
import time
import math
class ExpertSystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        self.nombreAlumno = "Jorge Sánchez Cerezo" #IMPORTANTE: Cambia el valor de esta propiedad por tu nombre completo
        self.estado_inicio = True
        self.orientarse = False

    #   función setObjetivo
    #   Almacena en la propiedad objetivoActual el objetivo al que tiene que moverse el robot
    def setObjetivo(self, objetivo):
        self.objetivoActual = objetivo

    #   función tomarDecision. 
    #   Recibe una tupla de 3 valores con la pose del robot: posición X, posición Y, orientación
    #   Devuelve una tupla con la velocidad lineal y angular que se
    #   quiere dar al robot
    
    def funcionangulo(self, difx, dify):
        #Con trigonometria básica, calculamos el angulo (tan = dify/dix): angulo = arctan dify difx
        angulo = math.atan2(dify, difx) #Como esta en radianes, vamos a pasarlo a grados
        angulo_objetivo = angulo * 180/math.pi
        return angulo_objetivo
    
    def inicio(self, poseRobot):
        #Asignamos variables a los datos del robot (coordenadas y angulo que mira)
        xrobot = poseRobot[0]
        yrobot = poseRobot[1]
        orientacion = poseRobot[2]
        return xrobot, yrobot, orientacion
    
    def tipo_recorrido(self):
        tipo = self.objetivoActual.getType()
        return tipo
    
    def calculo_diferencia(self, angulo_objetivo, orientacion):
        diferencia  = angulo_objetivo - orientacion
        while diferencia > 180:
            diferencia -= 360 # si ha dado mas de media vuelta en sentido horario, es decir, mas alla de los 180 grados, lo ponemos en -180, y asi lo situamos como que esta en la parte izquierda del robot (zona negativa | zona positiva) 
        while diferencia < -180:
            diferencia += 360
        return diferencia

    def distancia(self, xiniobj, xrobot, yiniobj, yrobot):
        difx = xiniobj - xrobot
        dify = yiniobj - yrobot 
        distancia_objetivo = abs(difx)+abs(dify)
        angulo_objetivo = math.degrees(math.atan2(dify, difx))
        return difx, dify, distancia_objetivo, angulo_objetivo

#SEGEMTNOOOOO -·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·

    def iraobjetivo(self, distancia_objetivo, diferencia):
        # Giro a la DERECHA (diferencia positiva)
        if diferencia > 0.5:
            if diferencia > 15:
                x = 2
                y = 0.5
            elif diferencia > 10:
                x = 2.5
                y = 0.3
            else:
                x = 3
                y = 0.1
        # Giro a la izquierda (diferencia negativa)
        elif diferencia < -0.5:
            if diferencia < -15:
                x = 2
                y = -0.5
            elif diferencia < -10:
                x = 2.5
                y = -0.3
            else:
                x = 3
                y = -0.1
        # Alineado con el objetivo (avanza recto)
        else:
            x = 3
            y = 0

        # 2. Comprobación de estado según la distancia al objetivo inicial
        if distancia_objetivo <= 2:
            self.estado_inicio = not self.estado_inicio
            x = 0
        return x, y
#-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·-·

    def tomarDecision(self, poseRobot):
        x , y = 0 , 0 #Inicializamos las variables a cero por si acaso

        #Llamamos a inicio, en el que obtenemos los datos del robot
        xrobot, yrobot, orientacion = self.inicio(poseRobot)

        #Calculamos el tipo de recorrido (1 segmento, 2 triangulo)
        tipo = self.tipo_recorrido()

        if tipo  == 1:
            #SEGMENTO

            #Si es la primera vez que entramos (el robot no inicia en el segmento:)
            if self.estado_inicio == True:

                #Buscamos las coordenadas del primer punto del segmento
                inicio_obj = self.objetivoActual.getInicio()
                xiniobj = inicio_obj[0]
                yiniobj = inicio_obj[1]

                #Calculamos la distancia a la que estamos del punto
                difx, dify, distancia_objetivo, angulo_objetivo = self.distancia(xiniobj, xrobot, yiniobj, yrobot)
                
                #Ahora lo que queremos es calcular la diferencia
                # (Angulo objetivo le restamos nuestra orientacion, y asi obtenemos lo que debe girar nuestro robot)
                diferencia = self.calculo_diferencia(angulo_objetivo, orientacion)
                
                x, y= self.iraobjetivo(distancia_objetivo, diferencia)

            #Ahora nos limitamos a llegar al final del segmento
            else:
                #Buscamos las coordenadas del primer punto del segmento
                fin_obj = self.objetivoActual.getFin()
                xfinobj = fin_obj[0]
                yfinobj = fin_obj[1]

                #Calculamos la distancia a la que estamos del punto
                difx, dify, distancia_objetivo, angulo_objetivo = self.distancia(xfinobj, xrobot, yfinobj, yrobot)
                difx = xfinobj - xrobot
                dify = yfinobj - yrobot 
                distancia_objetivo = abs(difx)+abs(dify)
                angulo_objetivo = math.degrees(math.atan2(dify, difx))

                #Obtenemos la diferencia
                diferencia = self.calculo_diferencia(angulo_objetivo, orientacion)

                x, y= self.iraobjetivo(distancia_objetivo, diferencia)

            #Calculamos el angulo al que deberia situarse el robot para alinearse con el objetivo
            
        else:
            #TRIANGULO
            if self.estado_inicio == True:
                medio_obj = self.objetivoActual.getMedio()
                xmedioobj = medio_obj[0]
                ymedioobj = medio_obj[1]
                #Calculamos la distancia a la que estamos del punto
                difx, dify, distancia_objetivo, angulo_objetivo = self.distancia(xmedioobj, xrobot, ymedioobj, yrobot)
                difx = xmedioobj - xrobot
                dify = ymedioobj - yrobot 
                distancia_objetivo = abs(difx)+abs(dify)
                angulo_objetivo = math.degrees(math.atan2(dify, difx))
                diferencia = self.calculo_diferencia(angulo_objetivo, orientacion)
                x, y = self.iraobjetivo(distancia_objetivo, diferencia)
            else:
                fin_obj = self.objetivoActual.getFin()
                xfinobj = fin_obj[0]
                yfinobj = fin_obj[1]
                #Calculamos la distancia a la que estamos del punto
                difx, dify, distancia_objetivo, angulo_objetivo = self.distancia(xfinobj, xrobot, yfinobj, yrobot)
                difx = xfinobj - xrobot
                dify = yfinobj - yrobot 
                distancia_objetivo = abs(difx)+abs(dify)
                angulo_objetivo = math.degrees(math.atan2(dify, difx))
                diferencia = self.calculo_diferencia(angulo_objetivo, orientacion)
                x, y = self.iraobjetivo(distancia_objetivo, diferencia)
        print(round(poseRobot[0], 2), round(poseRobot[1], 2))
        return x, y
    
    #NOTAS

        #Me doy cuenta dce que el angulo del robot lo imprimo en grados (orientarse (que es poseRobot[2])), por lo tanto
        #para girar en sentido horario hay que usar el menos, por lo que el angulo bueno (el ue queremos en 360), hay que pillar el resto de dividir entre 360:
        # ejemplo -- 0 grados mira hacia arriba, 180 abajo, 360 arriba otra vez, por lo que lo reseteamos a 0, pero tenemos que calcular como que el 0 esta igual de cerca del 270 que del 90, por lo que if orientacion

    #DUDAS

        # - siempre se alterna segmento, triangulo?
        #   pueden haber dos trozos separados (el circuito es todo conectado o hay saltos?) 
        #   Se puede meter por dentro del triangulo?
