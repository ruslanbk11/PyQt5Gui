import sys
from mainInterface import *
from PyQt5 import QtCore, QtGui, QtWidgets
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom

def showDialog():
    text, ok = QtWidgets.QInputDialog.getText(None, 'Input',
                                                'Enter:',)
    if ok:
        return text
    else:
        return None
        
class mark_up_rect():

    pos = QtCore.QPoint()
    width = 0
    height = 0
    text = "test"
    r = 0
    g = 0
    b = 0
    a = 0

class MyGraphicsScene(QtWidgets.QGraphicsScene):

    rects = []
    added_rects = []
    added_text = []

    def __init__(self, *args, **kwargs):
        self.state = 0
        self.closeCheck = False
        super().__init__(*args, **kwargs)

       
    def mousePressEvent(self, event):

        if self.state == 4:
            print('haha')
            print(self.index)
            print(self.changing_rect)
            self.rects.remove(self.changing_rect)
            i = self.changing_rect
            i.width += (i.pos.x() - event.scenePos().x())
            i.height += (i.pos.y() - event.scenePos().y())
            i.pos = event.scenePos()
            print('pop0')
            self.removeItem(self.added_rects[self.index])
            self.added_rects.remove(self.added_rects[self.index])
            print('pop0.5')
            self.removeItem(self.added_text[self.index])
            self.added_text.remove(self.added_text[self.index])
            print('pop1')
            color = QtGui.QColor()
            color.setRgb(i.r,i.g,i.b,i.a)
            pen = QtGui.QPen(color)
            rect = self.addRect(i.pos.x(), i.pos.y(),
                                              i.width, i.height, pen)
            print('pop2')

            text = self.addText(i.text)
            print('pop1')
            self.removeItem(text)
            print('pop1')
            text.setDefaultTextColor(color)
            print('pop1')
            text.setPos(i.pos.x() + i.width + 5,i.pos.y())
            self.addItem(text)
            print('pop1')
            self.added_rects.append(rect)
            self.added_text.append(text)
            self.rects.append(i)
            print('pop3')
            
            self.state = 6

        if self.state == 5:
            self.rects.remove(self.changing_rect)
            i = self.changing_rect
            i.width = abs(i.pos.x() - event.scenePos().x())
            i.height = abs(i.pos.y() - event.scenePos().y())
            print('pop0')
            self.removeItem(self.added_rects[self.index])
            self.added_rects.remove(self.added_rects[self.index])
            print('pop0.5')
            self.removeItem(self.added_text[self.index])
            self.added_text.remove(self.added_text[self.index])
            print('pop1')
            color = QtGui.QColor()
            color.setRgb(i.r,i.g,i.b,i.a)
            pen = QtGui.QPen(color)
            rect = self.addRect(i.pos.x(), i.pos.y(),
                                              i.width, i.height, pen)
            print('pop2')

            text = self.addText(i.text)
            print('pop1')
            self.removeItem(text)
            print('pop1')
            text.setDefaultTextColor(color)
            print('pop1')
            text.setPos(i.pos.x() + i.width + 5,i.pos.y())
            self.addItem(text)
            print('pop1')
            self.added_rects.append(rect)
            self.added_text.append(text)
            self.rects.append(i)
            print('pop3')
            self.state = 6

        if self.state == 1:
            if event.scenePos().x() < self.pos.x():
                self.x = event.scenePos().x()
            else:
                self.x = self.pos.x()
            if event.scenePos().y() < self.pos.y():
                self.y = event.scenePos().y()
            else:
                self.y = self.pos.y()
            self._width = abs(event.scenePos().x() - self.pos.x())
            self._height = abs(event.scenePos().y() - self.pos.y())
            self.state = 3
            rect = self.addRect(self.x,  self.y,
                             self._width, self._height, self.pen)
            self.text = showDialog()
            if self.text:
                add_text = self.addText(self.text)
                self.removeItem(add_text)                
                add_text.setDefaultTextColor(self.pen.color()) 
                add_text.setPos(self.x + self._width + 5,self.y)
                self.addItem(add_text)
                self.added_text.append(add_text)
            self.added_rects.append(rect)
            print(self._width, self._height)

        if self.state == 0:
            self.closeCheck = True
            self.pos = event.scenePos()
            self.changing_rect = mark_up_rect()
            self.index = 0
            print('here')
            for rect in self.rects:
                print('here1')
                if (abs(self.pos.x() - rect.pos.x()) < 5) and (abs(self.pos.y() - rect.pos.y()) < 5):
                    print('here2')
                    self.changing_rect = rect
                    self.state = 4
                    break;
                else:
                    print('here3')
                    self.index += 1
            print(self.state)
            if self.state == 0:
                self.index = 0
                for rect in self.rects:
                    if (abs(self.pos.x() - rect.width - rect.pos.x()) < 5) and (abs(self.pos.y() - rect.height - rect.pos.y()) < 5):
                        self.changing_rect = rect
                        self.state = 5
                        break;
                    else:
                        self.index += 1
            print(self.state)
            if self.state == 0:
                self.state = 1

        if self.state == 3:
            print('1')
            self.pos = QtCore.QPoint(self.x, self.y)
            print('2')
            mark_up = mark_up_rect()
            print('2')
            mark_up.pos = self.pos
            mark_up.width = self._width
            mark_up.height = self._height
            color = self.pen.color()
            mark_up.r,mark_up.g,mark_up.b,mark_up.a = color.getRgb()
            
            #print('#2.5')

            mark_up.text = self.text
            #print(mark_up.text)

            print('2')
            #print(mark_up.pos, mark_up._width, mark_up._height)
            self.rects.append(mark_up)
            print('3')
            for i in self.rects:
                print (i.pos, i.width, i.height)
            self.state = 0

        if self.state == 6:
            self.state = 0

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.closeCheck = False
        self.ui.scene = MyGraphicsScene()
        self.ui.scene.pen = QtGui.QPen()
        
        self.setGeometry(50, 50, 550, 420)
        self.setWindowTitle('Interface')
        self.setWindowIcon(QtGui.QIcon('network.png'))

        self.ui.actionLoad.triggered.connect(self.openFile)
        self.ui.actionSave.triggered.connect(self.saveFile)
        self.ui.actionChoose_color.triggered.connect(self.colorDialog)
        #self.ui.label.setText("")

    def colorDialog(self):
        col = QtWidgets.QColorDialog.getColor()
        self.ui.scene.pen = QtGui.QPen(col)
        print(self.ui.scene.pen)
    
    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        self.file,_=QtWidgets.QFileDialog.getOpenFileName(None,'OpenFile','',
                                                           "Image file(*.png *.jpg)",
                                                           options=options)
        if self.file:
            self.image = QtGui.QPixmap(self.file)
            #self.ui.label.setPixmap(self.image)
            self.resize(self.image.size())
            
            self.ui.scene.addPixmap(self.image)
            self.ui.graphicsView.setScene(self.ui.scene)
            #self.ui.graphicsView.resize(self.image.width() + 2, self.image.height() + 2)
            
            #открытие xml
            self.xml_name = self.file[:len(self.file)-3] + 'xml'
            print(self.xml_name)
            xml = open(self.xml_name, 'a')
            xml.close()
            xml = open(self.xml_name, 'r')
            print('#1')
            if xml:
                print('#1')
                read = xml.read()
                print('#2')
                if len(read) > 1:
                    print('#3')
                    xml.close()
                    xml = minidom.parse(self.xml_name)
                    collection = xml.documentElement
                    squares = collection.getElementsByTagName('square')
                    for square in squares:
                        print('c')
                        mark_up = mark_up_rect()
                        x = int(square.getAttribute('x'))
                        y = int(square.getAttribute('y'))
                        pos = QtCore.QPoint(x, y)
                        mark_up.pos = pos
                        mark_up.width = float(square.getAttribute('width'))
                        mark_up.height = float(square.getAttribute('height'))
                        mark_up.r = int(square.getAttribute('r'))
                        mark_up.g = int(square.getAttribute('g'))
                        mark_up.b = int(square.getAttribute('b'))
                        mark_up.a = int(square.getAttribute('a'))
                        if len(square.childNodes) != 0:
                            mark_up.text = square.childNodes[0].data
                        #print(square.childNodes)
                        self.ui.scene.rects.append(mark_up)
                    for i in self.ui.scene.rects:
                        print(self.ui.scene.pen)
                        color = QtGui.QColor()
                        print(color)
                        color.setRgb(i.r,i.g,i.b,i.a)
                        pen = QtGui.QPen(color)
                        rect = self.ui.scene.addRect(i.pos.x(), i.pos.y(),
                                              i.width, i.height, pen)
                        text = self.ui.scene.addText(i.text)
                        self.ui.scene.removeItem(text)
                        text.setDefaultTextColor(color)
                        text.setPos(i.pos.x() + i.width + 5,i.pos.y())
                        self.ui.scene.addItem(text)
                        self.ui.scene.added_rects.append(rect)
                        self.ui.scene.added_text.append(text)                        
            

    def saveFile(self):
        for i in self.ui.scene.added_rects:
            self.ui.scene.removeItem(i)
        for i in self.ui.scene.added_text:
            self.ui.scene.removeItem(i)
        options = QtWidgets.QFileDialog.Options()
        self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save to file",
                                              "", "Image file(*.png *.jpg)",
                                              options=options)
        if self.fileName:
            self.image = QtGui.QImage(self.ui.scene.sceneRect().size().toSize(),
                                      QtGui.QImage.Format_ARGB32)
            self.image.fill(QtGui.QColor.fromRgb(255, 255, 255, 255));
            painter = QtGui.QPainter(self.image)
            self.ui.scene.render(painter)
            if self.image.save(self.fileName):
                self.ui.statusbar.showMessage('Saved to %s' %self.fileName)
                self.ui.scene.closeCheck = False
            else:
                self.ui.statusbar.showMessage('!!! File is NOT saved !!!')

            self.xml_name = self.fileName[:len(self.fileName)-3] + 'xml'
            print(self.xml_name)
            root = ET.Element('root')
            
            for i in self.ui.scene.rects:
                print('in cycle')
                color = QtGui.QColor()
                color.setRgb(i.r,i.g,i.b,i.a)
                pen = QtGui.QPen(color)
                rect = self.ui.scene.addRect(i.pos.x(), i.pos.y(),
                                              i.width, i.height, pen)
                text = self.ui.scene.addText(i.text)
                self.ui.scene.removeItem(text)                        
                text.setDefaultTextColor(color)
                text.setPos(i.pos.x() + i.width + 5,i.pos.y())
                self.ui.scene.addItem(text)
                self.ui.scene.added_text.append(text) 
                self.ui.scene.added_rects.append(rect)
                ET.SubElement(root, 'square',
                              x=str(i.pos.x()),y=str(i.pos.y()),
                              width = str(i.width),
                              height = str(i.height),
                              r = str(i.r),
                              g = str(i.g),
                              b = str(i.b),
                              a = str(i.a)).text = i.text
            tree = ET.ElementTree(root)
            print(tree)
            tree.write(self.xml_name)
            print('written')

    def closeEvent(self, event):
        if self.ui.scene.closeCheck:
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
