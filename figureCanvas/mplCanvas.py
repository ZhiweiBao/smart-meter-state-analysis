import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtWidgets

class mplCanvas(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot                                          lib的关键

    def __init__(self, parent=None, width=11, height=5, dpi=100):
        self.fig = Figure()  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        # fig.tight_layout()
        FigureCanvas.__init__(self, self.fig) # 初始化父类
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        for i in range(20):
            self.ax = self.fig.add_subplot(4,5,i+1)
            self.ax.set_title('%s' % (i+1), fontsize=14)
            self.ax.set_xticklabels([])
        self.fig.tight_layout()

    def plot(self, sID):
        x = [1,2,3,4,5,6,7,8,9]
        y = [23,21,32,13,3,132,13,3,1]
        self.ax = None
        self.ax = self.fig.add_subplot(4, 5, sID)
        self.ax.plot(x, y)
        self.ax.clear()
        self.ax.grid()
        self.ax.set_title('%s' % sID, fontsize=14)
        # self.ax.set_xlabel(u'日期', fontsize = 14)
        # self.ax.set_ylabel(u'偏差值', fontsize = 14)
        # self.ax.set_title(u'第%s台智能电表检定数据分析折线图' % sID, fontsize = 22)
        # if self.curveObj is None:
        #     # create draw object once
        #     self.curveObj = self.ax.plot(np.array(datax), np.array(datay), 'bo-')
        # else:
        #     # update data of draw object
        #     self.curveObj.set_data(np.array(datax), np.array(datay))
        # update limit of X axis,to make sure it can move
        self.ax.set_xticklabels([])
        # self.ax.set_ylim(-1, 1)
        # ticklabels = self.ax.xaxis.get_ticklabels()
        # for tick in ticklabels:
        #     tick.set_rotation(25)
        # self.ax.plot_date(x, y, linestyle='solid')
        self.draw()

class mplCanvasWrapper(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = mplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.ntb = NavigationToolbar(self.canvas, parent)
        self.vbl.addWidget(self.ntb)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.dataX = []
        self.dataY = []
        self.stationID = 0

    def draw(self,x,y,sID,X):
        self.datax = x
        self.datay = y
        self.stationID = sID
        self.dataX = X
        self.canvas.plot(self.stationID)