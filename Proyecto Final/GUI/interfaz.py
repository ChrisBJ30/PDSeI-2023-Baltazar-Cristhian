# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 00:09:43 2024

@author: ricar
"""

from PyQt5 import QtWidgets, uic
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('interfaz.ui', self)
        
        self.pushButton_4 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.pushButton_4.clicked.connect(self.cargarVideo)
        
        self.pushButton_3 = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.pushButton_3.clicked.connect(self.iniciarAnalisis)
        
        self.pushButton_6 = self.findChild(QtWidgets.QPushButton, 'pushButton_6')
        self.pushButton_6.clicked.connect(self.detenerAnalisis)
        
        self.pushButton_5 = self.findChild(QtWidgets.QPushButton, 'pushButton_5')
        self.pushButton_5.clicked.connect(self.guardarResultados)
        
        self.show()

    def cargarVideo(self):
        # Abre el cuadro de diálogo para seleccionar un archivo de video
      options = QtWidgets.QFileDialog.Options()
      fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
          self,
          "Cargar video",  # Título del cuadro de diálogo
          "",              # Directorio inicial
          "Videos (*.mp4)",  # Filtro para archivos .mp4
          options=options)
      if fileName:
          # Aquí es donde manejarías el archivo seleccionado
          self.label_6.setText(fileName)  # Actualiza la etiqueta con el nombre del archivo

    def iniciarAnalisis(self):
        # Código para iniciar el análisis de video
        if self.label_6:
            # Aquí puedes usar self.videoPath para iniciar el análisis del video
            print(f"Iniciando análisis del video: {self.label_6.text()}")
        else:
            print("No se ha seleccionado ningún video.")

    def detenerAnalisis(self):
        # Código para detener el análisis
        pass

    def guardarResultados(self):
        # Código para guardar los resultados en un archivo CSV
        pass

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
