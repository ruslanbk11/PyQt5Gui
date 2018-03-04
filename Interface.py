import sys
from mainInterface import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setGeometry(50, 50, 550, 420)
        self.setWindowTitle('Interface')
        self.setWindowIcon(QtGui.QIcon('network.png'))

        self.ui.actionLoad.triggered.connect(self.openFile)
        self.ui.actionSave.triggered.connect(self.saveFile)
        self.ui.label.setText("")
        
    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        self.file,_=QtWidgets.QFileDialog.getOpenFileName(None,'OpenFile','',
                                                           "Image file(*.png *.jpg)",
                                                           options=options)
        self.image = QtGui.QImage(self.file)
        #painter = QtGui.QPainter()
        #painter.begin(self)
        #painter.drawImage(0, 0, image)
        #painter.end()

        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def saveFile(self):
        options = QtWidgets.QFileDialog.Options()
        self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save to file",
                                              "", "Image file(*.png)",
                                              options=options)
        if self.fileName:
            self.pixmap = self.ui.label.pixmap()
            self.image = self.pixmap.toImage()
            if self.image.save(self.fileName,'png'):
                self.ui.statusbar.showMessage('Saved to %s' %self.fileName)
            else:
                self.ui.statusbar.showMessage('!!! File is NOT saved !!!')
     
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self, "Confirm action",
                                                "Save before quit?",
                                                QtWidgets.QMessageBox.Yes |
                                                QtWidgets.QMessageBox.No |
                                                QtWidgets.QMessageBox.Cancel,
                                                QtWidgets.QMessageBox.Cancel)
        if result == QtWidgets.QMessageBox.Yes:
            self.saveToFile()
            event.accept()
        elif result == QtWidgets.QMessageBox.No:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Window()
    myapp.show()
    sys.exit(app.exec_())
