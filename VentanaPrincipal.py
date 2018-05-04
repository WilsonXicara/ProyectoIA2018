import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import neurolab as nl
import webcolors
from PIL import Image, ImageOps
import entrenamiento
import detector_imagen as detector

# Clase para construir la ventana
class Ventana(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # Carga del archivo *.ui
        uic.loadUi("VentanaPrincipal.ui",self)
        # Asignacion de acciones al hacer clic en los botones
        self.boton_buscarImagen.clicked.connect(self.accion_boton_buscarImagen)
        self.boton_evaluarFruto.clicked.connect(self.accion_boton_evaluarFruto)
    # Acciones que ejecutan los botones
    def accion_boton_buscarImagen(self):
        Tk().withdraw() # no queremos una GUI completa, asi que evita que aparezca la ventana raiz
        ruta = askopenfilename() # mostrar un cuadro de dialogo "Abrir" y devolver la ruta al archivo seleccionado
        if ruta != '':
            self.rutaImagen = ruta
            self.text_RutaImagen.setText(self.rutaImagen)
            buscador = detector.DetectorFruto()
            buscador.recortar_imagen(self.rutaImagen)
            self.imagen = Image.open('tmp.jpg')
            self.label_imagenCargada.setPixmap(QPixmap('tmp.jpg'))
        self.caja_resultado.setPlainText('')
    def accion_boton_evaluarFruto(self):
        print("Imagen: '"+self.rutaImagen+"'")
        print('|   |-- Por favor espere...')
        entrenamiento.iniciarRed(False)
        resultado = entrenamiento.predecir(
            np.array(
                entrenamiento.ObtenerEntradas(self.imagen.getdata())).reshape(1,9)
            )
        convertido = self.funcion_transferencia(resultado[0])
        #print('|   |-- Salida:    '+str(resultado[0]))
        #print('|   |-- Resultado: '+str(convertido))
        print('\-- Fin de evaluacion')
        informacion = ''
        if sum(convertido) == 0 or convertido[-1] == 1:
            # Es un error
            informacion = 'ERROR.\nLa imagen no pudo ser reconocida'
        else:
            # Evaluacion del fruto
            if convertido[0]==1 and convertido[3]==1:
                informacion = '''El fruto no está maduro pero presenta indicios de descomposicion.
                \nTiempo de maduracion: 3 a 2 dias
                \nTiempo estimado para descomposicion: 3 a 4 dias'''
            elif convertido[0]==1 and convertido[4]==1:
                informacion = '''El fruto no está maduro pero ya esta descompuesto.
                \nYa no se puede consumir'''
            elif convertido[1]==1 and convertido[3]==1:
                informacion = '''El fruto no está en proceso de maduración pero presenta indicios de descomposicion.
                \nTiempo de maduracion: 2 a 1 dias
                \nTiempo estimado para descomposicion: 3 a 4 dias'''
            elif convertido[1]==1 and convertido[4]==1:
                informacion = '''El fruto está en proceso de maduración pero ya esta descompuesto.
                \nYa no se puede consumir'''
            elif convertido[2]==1 and convertido[3]==1:
                informacion = '''El fruto ya está maduro pero presenta indicios de descomposicion.
                \nPuede consumirlo ahora
                \nTiempo estimado para descomposicion: 3 a 4 dias'''
            elif convertido[2]==1 and convertido[4]==1:
                informacion = '''El fruto ya está maduro pero ya esta descompuesto.
                \nYa no se puede consumir'''
            elif convertido[0]==1:
                informacion = '\nEl fruto esta inmaduro.\nTiempo para consumo: 3 a 2 dias\nTiempo estimado para descomposion: 6 a 7 dias'
            elif convertido[1] == 1:
                informacion = '\nEl fruto esta inmaduro.\nTiempo para consumo: 2 a 1 dia\nTiempo estimado para descomposion: 3 a 4 dias'
            elif convertido[2] == 1:
                informacion = 'Fruto en estado optimo.\nPuede consumirlo ahora\nRecuerde, tiene uno o dos dias para consumirlo'
            elif convertido[3] == 1:
                informacion = '\nFruto con leve descomposicion.\nTiempo restante: 1 dia'
            elif convertido[4] == 1:
                informacion = 'Fruto descompuesto.\nNo consumir!'
            else:
                informacion = 'No se puede determinar el estado del fruto'
        self.caja_resultado.setPlainText(informacion)

    def funcion_transferencia(self, resultado):
        nuevos = []
        for valor in resultado:
            if valor > 0.99:
                nuevos.append(1)
            else:
                nuevos.append(0)
        return nuevos

# Iniciar la aplicacion
app = QApplication(sys.argv)
# Instancia de la clase
_ventana = Ventana()
_ventana.show()
# Ejecucion de la aplicacion
app.exec_()