import webcolors
from PIL import Image, ImageOps
import numpy as np
import neurolab as nl
#----------------------------Datos importante para la red neuronal ----------------------
NPatrones= 0
NEntradas = 9
NSalidas = 6
Entradas = []
Salidas = []
redNeuronal = 0
NEpocas = 50000
CA = 0.0001
#----------------------------------------------------------------------------------------


#
#----------------------------------- Para normalizar entradas de la neurona ----------------------------------
verdeClaro = [
	'greenyellow',
	'lawngreen',
	'limegreen',
	'lime'
];

verdeMedio = [
	'olive',
	'olivedrab',
	'yellowgreen'
]

verdeOscuro = [
	'darkgreen',
	'green',
	'forestgreen',
	'darkolivegreen',
	'darkseagreen',
	'mediumseagreen',
	'lightgreen',
	'seagreen',
	'palegreen',
	'sapgreen'
]

rojoClaro = [
	'indianred',
	'lightcoral',
	'ligthsalmon',
	'salmon',
	'tomato',
	'coral',
	'crimson'
]

rojoMedio = [
	'red',
	'orangered'
]

rojoOscuro = [
	'darkred',
	'maroon',
	'firebrick',
	'brown'
]


anaranjado = [
	'darkorange',
	'orange',
	'sandybrown',
	'cadmiumorange',
	'cadmiumyellow',
	'carrot'
]

amarillo = [
	'yellow',
	'gold',
	'goldenrod',
	'banana'
]

descompuesto = [
	'rosybrown',
	'lightpink',
	'pink',
	'plum',
	'mistyrose'
]

blanco = [
	'lavanderblush',
	'ghostwhite',
	'aliceblue',
	'mintcream',
	'honeydew',
	'ivory',
	'floralwhite',
	'snow',
	'white',
	'whitesmoke'
]

def colorAproximado(color):
    coloresMinimos = {}
    for codigo, nombre in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(codigo)
        rd = (r_c - color[0]) ** 2
        gd = (g_c - color[1]) ** 2
        bd = (b_c - color[2]) ** 2
        coloresMinimos[(rd + gd + bd)] = nombre
    return coloresMinimos[min(coloresMinimos.keys())]

def obtenerNombreColor(color):
    try:
        nombre = webcolors.rgb_to_name(color)
    except ValueError:
        nombre = colorAproximado(color)
    return nombre



def ObtenerEntradas(imagen):
	cantVerdeC = 0
	cantVerdeM = 0
	cantVerdeO = 0
	cantRojoC = 0
	cantRojoM = 0
	cantRojoO = 0
	cantAnaranjado = 0
	cantAmarillo = 0
	cantDescompuesto = 0
#	colores=[]
	for pixel in imagen:
#		print("pixel No."+str(aux));
		nombre = obtenerNombreColor(pixel)
#		if nombre not in colores:
#			colores.append(nombre)
		if nombre in rojoClaro:
			cantRojoC +=1
			continue;
		if nombre in rojoMedio:
			cantRojoM +=1
			continue;
		if nombre in rojoOscuro:
			cantRojoO +=1
			continue;
		if nombre in verdeClaro:
			cantVerdeC +=1
			continue;
		if nombre in verdeMedio:
			cantVerdeM +=1
			continue;
		if nombre in verdeOscuro:
			cantVerdeO +=1
			continue;
		if nombre in descompuesto:
			cantDescompuesto +=1
			continue;
		if nombre in anaranjado:
			cantAnaranjado +=1
			continue;
		if nombre in amarillo:
			cantAmarillo +=1
			continue;

	print('     Verde [claro, medio, oscuro] = ['+str(cantVerdeC)+', '+str(cantVerdeM)+', '+str(cantVerdeO)+']')
	print('      Rojo [claro, medio, oscuro] = ['+str(cantRojoC)+', '+str(cantRojoM)+', '+str(cantRojoO)+']')
	print('[Amarillo, Naranja, Descompuesto] = ['+str(cantAmarillo)+', '+str(cantAnaranjado)+', '+str(cantDescompuesto)+']')
	cantidadFruto = cantVerdeC + cantVerdeM + cantVerdeO + cantRojoC + cantRojoM + cantRojoO + cantAnaranjado + cantAmarillo +cantDescompuesto
	entradas = np.array([
		round(cantVerdeC/cantidadFruto,2),
		round(cantVerdeM/cantidadFruto,2),
		round(cantVerdeO/cantidadFruto,2),
		round(cantRojoC/cantidadFruto,2),
		round(cantRojoM/cantidadFruto,2),
		round(cantRojoO/cantidadFruto,2),
		round(cantAnaranjado/cantidadFruto,2),
		round(cantAmarillo/cantidadFruto,2),
		round(cantDescompuesto/cantidadFruto,2),
	])
#	print(colores)
	return entradas

#-------------------------------------------------------------------------------------------------

#
#--------------------------------------Utilizado para entrenar la neurona-------------------------
#
def iniciarRed(tipo):
	global redNeuronal,NEntradas
	if tipo == True:
		redNeuronal = nl.net.newff([[-12,12]]*9,[50,NSalidas])
#		redNeuronal.trainf = nl.train.train_gd
#		redNeuronal.errorf = nl.error.CEE()
	else:
		redNeuronal = nl.load("RedNeuronal.net")

def guardarEntradas(entradas,ruta):
	AuxEntradas = np.genfromtxt(entradas, delimiter=",",dtype=None)
	lista = []
	a = 1
	for aux in AuxEntradas:
		print("Patron No."+str(a))
		imagen = Image.open(aux)
		imagen = imagen.resize((300,225))
		lista.append(ObtenerEntradas(imagen.getdata()))
		a+=1
	np.savetxt(ruta,np.array(lista),delimiter=",")

def cargarDatosEntrenamiento(entradas,salidas):
	global Entradas,Salidas,NPatrones,NEntradas,NSalidas
	Entradas = np.array([])
	Salidas = np.array([])
	AuxEntradas = np.genfromtxt(entradas, delimiter=",",dtype=None)
	if(AuxEntradas.shape[0] >1):
		for aux in AuxEntradas:
			Entradas =  np.append(Entradas,aux)
			NPatrones = NPatrones+1

	else:
		Entradas =  np.append(Entradas,AuxEntradas)
		NPatrones = NPatrones+1
	AuxSalidas = np.genfromtxt(salidas, delimiter=",")
	for x in AuxSalidas:
		Salidas = np.append(Salidas,x)
	Entradas = Entradas.reshape(NPatrones,NEntradas)
	Salidas = Salidas.reshape(NPatrones,NSalidas)

def predecir(entrada):
	global redNeuronal 
	return redNeuronal.sim(entrada)

def cargarNuevoPatron(ruta,esperado):
	global Entradas, Salidas
	Entradas.append(leerImagen(ruta))
	Salidas.append(esperado)


def entrenar():
	global Entradas,Salidas,redNeuronal,NPatrones,NEntradas,NEpocas,CA
	print("entrenar")
	redNeuronal.train(Entradas,Salidas, epochs=NEpocas, show=100,goal=0.03)
#----------------------------------------------------------------------------------------------------------------------

#guardarEntradas('rutasPatrones.csv','entradas.csv')
#iniciarRed(False)
#imagen = Image.open('Pruebas/im01.jpg')
#imagen = imagen.resize((300,225))
#print(predecir(np.array(ObtenerEntradas(imagen.getdata())).reshape(1,NEntradas)))
#cargarDatosEntrenamiento('entradas.csv','salidas.csv')
#print("Epocas "+str(NEpocas))
#print("Tasa de Entrenamiento "+str(CA))
#entrenar()
#redNeuronal.save("RedNeuronal.net")
