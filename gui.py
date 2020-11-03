from PyQt5 import QtWidgets
import pyqtgraph as pg
from qt_gui.MainWindow import Ui_MainWindow
from logic import mandel_seq, colorDiverged


class GUIMandelbrot(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # main plot area
        self.plot = self.QPlotWidget.plot()
        # drawing fractal here
        self.scPlot = pg.ScatterPlotItem(pxMode=True, size=10,
                                        symbol='o',
                                        brush='r') 
        self.QPlotWidget.setBackground('w')
        #self.QPlotWidget.scene().sigMouseMoved.connect(self.getCoords)
        self.QPlotWidget.scene().sigMouseClicked.connect(self.getCoords)

    def getCoords(self,event):
        self.plot.clear()
        #coords = self.QPlotWidget.plotItem.vb.mapToView(event.toPoint())
        coords = self.QPlotWidget.plotItem.vb.mapSceneToView(event.scenePos())
        mseq = mandel_seq(Z=(0,0), C=(coords.x(),coords.y()))
        self.plot.setData(seq[0],seq[1]) # plot lines
        brush = colorDiverged(seq)
        self.scPlot.addPoints([{'pos': [coords.x(),coords.y()]}], brush=brush) # add point of fractal
        self.QPlotWidget.addItem(self.scPlot)
        Xmax = max([abs(x) for x in mseq[0]])
        Ymax = max([abs(y) for y in mseq[1]])
        self.QPlotWidget.plotItem.vb.setRange(xRange=(-Xmax, Xmax), yRange=(-Ymax, Ymax), 
                                            update=True, disableAutoRange=True)
        