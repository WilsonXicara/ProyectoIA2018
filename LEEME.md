# ProyectoIA2018

La finalidad de este proyecto es la implementación de una inteligencia artificial para el reconocimiento del chile pimiento.
Para ello, la IA fue sometida a entrenamiento con más de 250 fotografías para reconocer el estado de madurez del fruto mencionado.

**** Fase de entrenamiento ****

**** Funcionamiento de la aplicación ****
El programa posee una interfaz gráfica sencilla para poder verificar el grado de madurez de un chile pimiento. Para ejecutarla se debe hacer lo siguiente:
1. Abrir una consola en el mismo directorio del archivo 'VentanaPrincipal.py'
2. Ejecutar el archivo 'VentanaPricipal.py' con Python3. El siguiente es un comando de ejemplo:
	python3.exe .\VentanaPrincipal.py
Esto inicializa la aplicación y muestra una ventana donde es posible cargar una imagen para prueba. El funcionamiento se resume como:
- Para cargar una imagen, clic en el botón 'Buscar' y seleccionar la imagen del explorador de archivo.
- A continuación se visualiza una ventana con la imagen seleccionada. La aplicación intenta determinar la posición del fruto, encerrándola en un rectángulo de color azul. El usuario puede cambiar dicha selección.
- Para recortar la imagen en el rectángulo seleccionado, presionar la tecla 'r'
- Para utilizar la imagen mostrada en la ventana, presionar la tecla 'g'
- Para evaluar la imagen cargada, clic en el botón 'Evaluar fruto'. La información se despliega en el cuadro de texto

**** Requisitos ****
- Python 3
- Librerías:
  - neurolab
  - numpy
  - opencv-python
  - webcolors
  - pyqt5

**** Acerca de ****
Proyecto desarrollado para el curso de Inteligencia Artificial. Parte del Séptimo ciclo de la carrera de Ingeniería en Informática y Sistemas.

Autores:
	Hugo Adolfo Tzul Pérez
	Wilson Giovanni Xicará Xicará

Universidad Rafael Landívar, Quetzaltenango, Guatemala. Mayo de 2018