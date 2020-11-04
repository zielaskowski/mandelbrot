from PyQt5 import QtWidgets
import pyqtgraph as pg
from qt_gui.MainWindow import Ui_MainWindow
from logic import mandel_seq, colorDiverged

ppi = 100
xMax = 1
xMin = -1.6
yMin = -1.2
yMax = 1.2

class GUIMandelbrot(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        global ppi
        global xMax
        global xMin
        global yMax
        global yMin

        super().__init__()
        self.setupUi(self)
        # main plot area
        self.plot = self.QPlotWidget.plot()
        # drawing fractal here
        self.scPlot = pg.ScatterPlotItem(pxMode=True, size=10,
                                        symbol='o',
                                        brush='r',
                                        pen=None) 
        self.QPlotWidget.setBackground('w')
        self.QPlotWidget.plotItem.vb.setLimits(xMin= xMin * ppi, xMax= xMax * ppi, yMin= yMin * ppi, yMax= yMax * ppi)
        self.QPlotWidget.plotItem.vb.setRange(xRange= (xMin * ppi, xMax * ppi), yRange= (yMin * ppi, yMax * ppi),
                                             update=True, disableAutoRange=True)

        self.radioButton.clicked.connect(self.radioBtnClk)
        self.QPlotWidget.scene().sigMouseMoved.connect(self.getCoords)
        #self.QPlotWidget.scene().sigMouseClicked.connect(self.getCoords)

    def radioBtnClk(self):
        if self.radioButton.isChecked():
            self.QPlotWidget.scene().sigMouseMoved.disconnect()
            self.autoPilot()
        else:
            self.QPlotWidget.scene().sigMouseMoved.connect(self.getCoords)

    def getCoords(self,event):
        global ppi
        self.plot.clear()
        coords = self.QPlotWidget.plotItem.vb.mapToView(event.toPoint())
        #coords = self.QPlotWidget.plotItem.vb.mapSceneToView(event.scenePos())
        mseq = mandel_seq(Z=(0,0), C=(coords.x()/ppi,coords.y()/ppi))
        mseqX = [x * ppi for x in mseq[0]]
        mseqY = [y * ppi for y in mseq[1]]
        self.plot.setData(mseqX, mseqY) # plot lines
        brush = colorDiverged(mseq)
        self.scPlot.addPoints([{'pos': [coords.x()-10,coords.y()]}], brush=brush) # add point of fractal
        self.QPlotWidget.addItem(self.scPlot)
        self.label.setText(f'set length: {len(mseqX)}\nbrush: {brush}\nmseqX: {mseqX}\nmseqY: {mseqY}')
    
    def autoPilot(self):
        global ppi
        global xMax
        global xMin
        global yMax
        global yMin

        for x in range(int(xMin*ppi), int(xMax*ppi)):
            for y in range(int(yMin*ppi), int(yMax*ppi)):
                mseq = mandel_seq(Z=(0,0), C=(x/ppi,y/ppi))
                brush = colorDiverged(mseq)
                self.scPlot.addPoints([{'pos': [x,y]}], brush=brush)
                self.QPlotWidget.addItem(self.scPlot)
                print(f'{x} , {y}    z {((xMax-xMin)*ppi)*((yMax-yMin)*ppi)}')

