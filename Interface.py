import sys
from mainInterface import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.closeCheck = False

        self.setGeometry(50, 50, 550, 420)
        self.setWindowTitle('Interface')
        self.setWindowIcon(QtGui.QIcon('network.png'))

        self.ui.actionLoad.triggered.connect(self.openFile)
        self.ui.actionSave.triggered.connect(self.saveFile)
        #self.ui.label.setText("")
        
    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        self.file,_=QtWidgets.QFileDialog.getOpenFileName(None,'OpenFile','',
                                                           "Image file(*.png *.jpg)",
                                                           options=options)
        if self.file:
            self.image = QtGui.QPixmap(self.file)
            #self.ui.label.setPixmap(self.image)
            self.resize(self.image.size())
            self.ui.scene = QtWidgets.QGraphicsScene()
            self.ui.scene.addPixmap(self.image)
            self.ui.graphicsView.setScene(self.ui.scene)
            #self.ui.graphicsView.resize(self.image.width() + 2, self.image.height() + 2)
            self.closeCheck = True

    def saveFile(self):
        options = QtWidgets.QFileDialog.Options()
        self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save to file",
                                              "", "Image file(*.png *.jpg)",
                                              options=options)
        if self.fileName:
            #fileFormat = self.fileName[-3] + self.fileName[-2] + self.fileName[-1]
            #self.pixmap = self.ui.label.pixmap()
            #self.image = self.pixmap.toImage()
            #if self.image.save(self.fileName, fileFormat):
            #    self.ui.statusbar.showMessage('Saved to %s' %self.fileName)
            #    self.closeCheck = False
            self.image = QtGui.QImage(self.ui.scene.sceneRect().size().toSize(),
                                      QtGui.QImage.Format_ARGB32)
            self.image.fill(QtGui.QColor.fromRgb(255, 255, 255, 255));
            painter = QtGui.QPainter(self.image)
            self.ui.scene.render(painter)
            if self.image.save(self.fileName):
                self.ui.statusbar.showMessage('Saved to %s' %self.fileName)
                self.closeCheck = False
            else:
                self.ui.statusbar.showMessage('!!! File is NOT saved !!!')

    def closeEvent(self, event):
        if self.closeCheck:
            result = QtWidgets.QMessageBox.question(self, "Confirm action",
                                                    "Save before quit?",
                                                    QtWidgets.QMessageBox.Yes |
                                                    QtWidgets.QMessageBox.No |
                                                    QtWidgets.QMessageBox.Cancel,
                                                    QtWidgets.QMessageBox.Cancel)
            if result == QtWidgets.QMessageBox.Yes:
                self.saveFile()
                event.accept()
            elif result == QtWidgets.QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    sys.exit(app.exec_())
