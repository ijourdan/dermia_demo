#!python3
# -*- coding: utf-8 -*-

from src import utils

from PyQt5 import QtCore, QtWidgets
from os.path import split, splitext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import torch

class Ui_Dialog(object):
    def __init__(self):
        self.imagen_name = ''
        self.imagen_ext = ''
        self.imagen_dir = ''
        self.aimage = {}

        self.valid_images = {'.jpg', '.JPG', '.jpeg', '.png', '.tiff', '.tif'}
        self.load_flag = False
        self.proc_label = False
        self.model = utils.Dermia_Model()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(780, 400)

        # Label para información
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(250, 10, 300, 50))
        self.label.setObjectName("label")
        self.label.setWordWrap(True)
        self.label.setText('Demostrador de Detector "nevus" / "melanoma"')

        self.label1 = QtWidgets.QLabel(Dialog)
        self.label1.setGeometry(QtCore.QRect(20, 220, 300, 70))
        self.label1.setObjectName("label")
        self.label1.setText('')

        # Carga datos
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 70, 83, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText('Sel Img')
        self.pushButton.setAutoDefault(False)  # para que no se activen con enter
        self.pushButton.clicked.connect(self.openFileNameDialog)

        # Visualiza imagen tal como es
        self.pushButton2 = QtWidgets.QPushButton(Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(220, 70, 100, 25))
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.setText('View Image')
        self.pushButton2.setAutoDefault(False)
        self.pushButton2.clicked.connect(self.printimg)

        # Boton para  procesar
        self.pushButton3 = QtWidgets.QPushButton(Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(20, 150, 300, 50))
        self.pushButton3.setObjectName("pushButton")
        self.pushButton3.setText('Procesar')
        self.pushButton3.setAutoDefault(False)
        self.pushButton3.clicked.connect(self.process)

        # Para trabajar con varias imagenes
        self.box = QtWidgets.QComboBox(Dialog)
        self.box.setGeometry(QtCore.QRect(20, 110, 300, 25))
        self.box.setObjectName('comboBox')
        self.box.activated[str].connect(self.onChanged)

        # Para seleccionar resultados
        self.box1 = QtWidgets.QComboBox(Dialog)
        self.box1.setGeometry(QtCore.QRect(20, 320, 300, 25))
        self.box1.setObjectName('comboBox')
        self.box1.activated[str].connect(self.onDetect)

        # Para visualizar imagenes
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(350, 70, 422, 316))
        self.graphicsView.setObjectName("graphicsView")

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    
    def test(self):
        self.graphicsScene = QtWidgets.QGraphicsScene()

        v = np.random.randn(500,500)

        figure = plt.Figure()
        axes = figure.gca()
        axes.set_axis_off()
        axes.imshow(v)
        canvas = FigureCanvas(figure)
        canvas.setGeometry(0, 0, 384, 288)
        self.graphicsScene.addWidget(canvas)
        r = self.graphicsScene.sceneRect()
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsView.fitInView(r, QtCore.Qt.KeepAspectRatio)

        

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                            "Images (*.jpg *.JPG *.jpeg *.png *.tiff" +
                                                            " *.tif);;All Files (*)",
                                                            options=options)
        if fileName:
            self.box1.clear()
            self.imagen_dir, aux = split(fileName)
            self.imagen_name, self.imagen_ext = splitext(aux)
            if self.imagen_ext in self.valid_images:
                self.aimage[self.imagen_name] = utils.Imagen(self.imagen_dir, self.imagen_name+self.imagen_ext)
                # self.aimage[self.imagen_name].notes = 'Nueva Imagen'
                # self.label1.setText(self.aimage[self.imagen_name].notes)
                self.load_flag = True
                self.box.addItem(self.imagen_name)
                indice = self.box.findText(self.imagen_name)
                if indice >= 0 :
                    self.box.setCurrentIndex(indice)
                self.label1.setText(self.imagen_name+' cargado')
            else:
                self.label1.setText('Incorrect File. Try jpg, png, tiff ')
                self.load_flag = False

    def printimg(self):
        self.graphicsScene = QtWidgets.QGraphicsScene()
        im = self.aimage[self.imagen_name].mtx
        figure = plt.Figure()
        axes = figure.add_subplot(111)
        axes.imshow(im)
        axes.axis('tight')
        axes.set_axis_off()
        canvas = FigureCanvas(figure)
        canvas.setGeometry(0, 0, 384, 288)
        self.graphicsScene.addWidget(canvas)
        self.graphicsView.setScene(self.graphicsScene)


    def printPill(self):
        # anda horrible esto
        self.graphicsScene = QtWidgets.QGraphicsScene()
        print(self.imagen_name)
        if self.load_flag:
            im = self.aimage[self.imagen_name].imqt
            self.graphicsScene.addPixmap(im)
            r = self.graphicsScene.sceneRect()
            self.graphicsView.setScene(self.graphicsScene)
            self.graphicsView.fitInView(r, QtCore.Qt.KeepAspectRatio)
            self.graphicsScene.update()


    def onChanged(self, text):
        self.label1.setText('')
        self.imagen_name = text
        self.label1.setText(text)
        self.box1.clear()
        if len(self.aimage[self.imagen_name].predictions.keys()) > 0:
            for i in self.aimage[self.imagen_name].predictions.keys():
                self.box1.addItem(str(i))

    def process(self):
        self.label1.setText('')
        self.model.evaluate(self.aimage[self.imagen_name])
        if len(self.aimage[self.imagen_name].predictions.keys()) > 0:
            for i in self.aimage[self.imagen_name].predictions.keys():
                self.box1.addItem(str(i))
            self.onDetect('0')
        else:
            self.box1.clear()


    def onDetect(self, text):
        idx = int(text)
        self.label1.setText('')

        im = self.aimage[self.imagen_name].mtx
        im_msk = self.aimage[self.imagen_name].predictions[idx]['mask']
        t_score = str(self.aimage[self.imagen_name].predictions[idx]['score'])
        if self.aimage[self.imagen_name].predictions[idx]['label'] == 1:
            t_diagnose = 'NEVUS'
            im_msk = im_msk.mul(255).byte().cpu().numpy()
            # im_msk = torch.abs(im_msk - 1).mul(255).byte().cpu().numpy()
            msk = np.zeros(im.shape, dtype='int')
            msk[..., 1] = im_msk
        elif self.aimage[self.imagen_name].predictions[idx]['label'] == 2:
            t_diagnose = 'MELANOMA'
            im_msk = im_msk.mul(255).byte().cpu().numpy()
            # im_msk = torch.abs(im_msk - 1).mul(255).byte().cpu().numpy()
            msk = np.zeros(im.shape, dtype='int')
            msk[..., 0] = im_msk
        else:
            self.label1.setText('NO DETECTADO')
            return 0

        self.label1.setText('Diagnóstico: '+t_diagnose+' \nScore: '+t_score)

        self.graphicsScene = QtWidgets.QGraphicsScene()

        figure = plt.Figure()
        axes = figure.add_subplot(111)
        axes.imshow(im)
        axes.imshow(msk, alpha=0.25)
        axes.axis('tight')
        axes.set_axis_off()
        canvas = FigureCanvas(figure)
        canvas.setGeometry(0, 0, 384, 288)
        self.graphicsScene.addWidget(canvas)
        self.graphicsView.setScene(self.graphicsScene)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.setWindowTitle('Dermia Demo')
    Dialog.show()
    sys.exit(app.exec_())
