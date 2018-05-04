from PIL import Image
import numpy as np
import cv2

class DetectorFruto():
	def __init__(self):
		self.drawing = False # true if mouse is pressed
		self.ix,self.iy = -1,-1
		self.imagen = np.array([])
		self.cpImagen = np.array([])
		self.rectangulo = (0,0,0,0)

	def detectar_fruto(self, imagen):
		# conviertiendo a escala de grises
		gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
		# aplicando filtro gaussiano
		gris = cv2.GaussianBlur(gris, (3, 3), 0)
		# Threshold: la mascara binaria de la imagen
		th, im_th = cv2.threshold(gris, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		mascara = cv2.cvtColor(im_th, cv2.COLOR_GRAY2BGR)
		# Conversion a pixeles blancos todo lo que no sea el fruto
		imagen = cv2.add(imagen, mascara)
		# Busqueda de contornos
		_, contornos, _ = cv2.findContours(im_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		# Evaluacion de cuales de las areas es la mayor
		fil, col = imagen.shape[0], imagen.shape[1]
		areaM =  0
		for c in contornos:
			area = cv2.contourArea(c)
			if area < (col*fil)*0.8 and area > areaM:
				areaM = area
				(x,y,w,h) = cv2.boundingRect(c)
				self.rectangulo = (x,y,x+w,y+h)
		# Ya se determino el area mayor

	# mouse callback function
	def dibujar_rectangulo(self, event,x,y,flags,param):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.drawing = True
			self.ix,self.iy = x,y
		elif event == cv2.EVENT_MOUSEMOVE:
			if self.drawing == True:
				self.cpImagen = self.imagen.copy()
				cv2.rectangle(self.cpImagen,(self.ix,self.iy),(x,y),(0,255,0), 1, cv2.LINE_AA)
		elif event == cv2.EVENT_LBUTTONUP:
			self.drawing = False
			aux = 0
			if self.ix > x:
				aux = self.ix
				self.ix = x
				x = aux
			if self.iy > y:
				aux = self.iy
				self.iy = y
				y = aux
			self.rectangulo = (self.ix, self.iy, x, y)
			cv2.rectangle(self.cpImagen,(self.ix,self.iy),(x,y),(0,255,0), 1, cv2.LINE_AA)
		elif event == cv2.EVENT_LBUTTONDBLCLK:
			# Doble clic izquierdo
			self.cpImagen[self.rectangulo[0]:self.rectangulo[1], self.rectangulo[2]:self.rectangulo[3]]
			pass
	            
	def recortar_imagen(self, rutaImagen):
		cv2.namedWindow('image')
		cv2.setMouseCallback('image',self.dibujar_rectangulo)

		# Redimiensionado de la imagen a (filas)x(500 columnas) pixeles
		MAX_COL = 500
		self.imagen = cv2.imread(rutaImagen)
		fil, col = self.imagen.shape[0], self.imagen.shape[1]
		if col < fil:
			col, fil = self.imagen.shape[0], self.imagen.shape[1]
		self.imagen = cv2.resize(self.imagen, (MAX_COL, int(MAX_COL*fil/float(col))))
		fil, col = self.imagen.shape[0], self.imagen.shape[1]
		self.cpImagen = self.imagen.copy()
		# Deteccion del fruto
		self.detectar_fruto(self.cpImagen)
		cv2.rectangle(self.cpImagen, (self.rectangulo[0], self.rectangulo[1]), (self.rectangulo[2], self.rectangulo[3]), (0, 255, 0), 1, cv2.LINE_AA)

		while(1):
			cv2.imshow('image',self.cpImagen)
			k = cv2.waitKey(1) & 0xFF
			if k == ord('r'):
				self.cpImagen = self.imagen.copy()
				self.cpImagen = self.cpImagen[self.rectangulo[1]:self.rectangulo[3], self.rectangulo[0]:self.rectangulo[2]]
				self.imagen = self.cpImagen.copy()
			elif k == ord('g'):
				fil, col = self.imagen.shape[0], self.imagen.shape[1]
				if col < fil:
					col, fil = self.imagen.shape[0], self.imagen.shape[1]
				self.imagen = cv2.resize(self.imagen, (MAX_COL, int(MAX_COL*fil/float(col))))
				cv2.imwrite('tmp.jpg', self.imagen)
				break
			elif k == ord('q') or k == 27:
				break
		cv2.destroyAllWindows()