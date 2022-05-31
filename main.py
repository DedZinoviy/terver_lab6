import statistics
from turtle import color, width
from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
import density
import pirsonTable as pt
from statisticalDataBigArray import Statistic
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from ui import Ui_MainWindow
from dialog import Ui_EnterDialog
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import re
import copy

class dialogwindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_EnterDialog()
        self.ui.setupUi(self)
        
        self.mainwindow = parent

        self.buttons = self.ui.buttonBox.buttons()
        self.buttons[0].setText("Ок")
        self.buttons[1].setText("Отмена")

        self.setTable()
        self.ui.intervalAmountBox.valueChanged.connect(self.setTable)

    
    def accept(self):
        amount = self.ui.intervalsTable.columnCount()
        intervals= []
        frequency = []
            
        try:
            row_1 = self.ui.intervalsTable.item(0, 0).text()
            row_2 = self.ui.intervalsTable.item(1, 0).text()
            interval = [float(s) for s in re.findall(r'-?\d+\.?\d*', row_1)]
            frequency.append(int(row_2))
            
            if len(interval) != 2:
                raise str("ERROR")

            h = interval[1] - interval[0]
            intervals.append(interval)

            for i in range(1, amount):
                row_1 = self.ui.intervalsTable.item(0, i).text()
                row_2 = self.ui.intervalsTable.item(1, i).text()
                interval = [float(s) for s in re.findall(r'-?\d+\.?\d*', row_1)]
                frequency.append(int(row_2))
                
                if len(interval) != 2:
                    raise str("ERROR")

                if (interval[1] - interval[0] - h > -1 * 10**(-5)) and (interval[1] - interval[0] - h < -1 * 10**(-5)):
                    raise str("ERROR")

                if intervals[i - 1][1] != interval[0]:
                    raise str("ERROR")
                
                intervals.append(interval)
            
            self.mainwindow.statistic.setIntervals(intervals, frequency)
            super().accept()
        
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка ввода", "Некорректное значение")
        
    
    def setTable(self):
        columnCount = self.ui.intervalAmountBox.value()

        if columnCount < self.ui.intervalsTable.columnCount():
            self.ui.intervalsTable.setColumnCount(columnCount)
        else:
            for i in range(self.ui.intervalsTable.columnCount(), columnCount):
                self.ui.intervalsTable.insertColumn(i)    

                variation = "[%g, %g]" % (i, i + 1)
                
                self.ui.intervalsTable.horizontalHeader().resizeSection(i, len(variation) * 12)
                self.ui.intervalsTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(''))

                self.ui.intervalsTable.setItem(0, i, QtWidgets.QTableWidgetItem(variation))
                self.ui.intervalsTable.setItem(1, i, QtWidgets.QTableWidgetItem("5"))

class mywindow(QtWidgets.QMainWindow):
    '''Конструктор гловного окна'''
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        

        self.dialog = dialogwindow(parent=self)
        
        self.pen = pg.mkPen(color='r', width=3)
        self.pen1 = pg.mkPen(color='b', width=3)
        self.pen2 = pg.mkPen(color='g', width=3)
        self.style1 = {'font-size':'30px'}
        font = QtGui.QFont()
        font.setPointSize(12)

        #self.ui.graphWidget = pg.PlotWidget()
        self.ui.graph.setBackground((225, 225, 225))
        self.ui.graph.getAxis('left').setPen('black')
        self.ui.graph.getAxis('left').setTextPen('black')
        self.ui.graph.getAxis("left").setStyle(tickFont = font)
        self.ui.graph.getAxis('bottom').setPen('black')
        self.ui.graph.getAxis('bottom').setTextPen('black')
        self.ui.graph.getAxis("bottom").setStyle(tickFont = font)
        self.ui.graph.showGrid(x=True, y=True, alpha=0.6)


        self.ui.openFileAction.triggered.connect(self.openFile)
        self.ui.alpha.currentIndexChanged.connect(self.changeXi2crit)
        self.ui.compareButton.clicked.connect(self.compareXi2)
        self.ui.inputIntervalSeriesAction.triggered.connect(self.openDialog)
        #self.ui.plotType.currentIndexChanged.connect(self.buildPlot)
        #self.ui.openFileAction.triggered.connect(self.openFile)
        #self.ui.rangeType.currentIndexChanged.connect(self.changeRangeType)
        #self.ui.interval_amount_button.clicked.connect(self.setIntervalAmount)
        #self.ui.dialogBtn.clicked.connect(self.openDialog)

        self.statistic = Statistic()
        self.rangeType = 0

    def solve(self):
        self.setTables()
        self.setCharacteristic()
        self.setPointAssessments()
        self.setXi2()
        self.setDensity()
        self.buildPlot()     

    def openDialog(self):
        if self.dialog.exec():
                try:
                    self.solve()
                    self.ui.InitionalArray.setText("Задан интервальный ряд")
                except:
                    pass
        else:
            print("Cansel")

    def compareXi2(self):
        try:
            empXi = float(self.ui.xi2.text())
            critXi = float(self.ui.xi2crit.text())
            resCompare = pt.Pirson.isEqualKhi(empXi, critXi)
            if (resCompare):
                strCompare = "Эмпирические данные не противоречат гипотезе о соответствии нормальному распределению"
            else:
                strCompare = "Отвергаем гипотезу о соответствии нормальному распределению"
            
            self.ui.resultCompare.setText(strCompare)
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка данных", "Ошибка данных!\nВведите входные данные")

    def setDensity(self):
        strDensity = "f(x)="+density.getDensity(self.statistic.average_sample, self.statistic.deviation)      
        self.ui.findDistributionDensity.setText(strDensity)  

    def changeXi2crit(self):
        countIntervals = len(self.statistic.frequency)
        k = countIntervals - 3 ###Добавить в класс ???
        alpha = float(self.ui.alpha.currentText())

        pirson = pt.Pirson()
        xi2crit = pirson.pirson[k][alpha]

        self.ui.xi2crit.setText(str(xi2crit))

    def setPointAssessments(self):
        a = "{:01.8}".format(self.statistic.average_sample)
        sigma = "{:01.8}".format(self.statistic.deviation)

        self.ui.aFind.setText(a)
        self.ui.sigma.setText(sigma)

    def setXi2(self):
        theoreticalBorders =  copy.deepcopy(self.statistic.interval_series) ### Добавить в класс????
        density.transformBorders(theoreticalBorders, self.statistic.average_sample, self.statistic.deviation)
        theoreticalProbabilities = density.getPropabilities(theoreticalBorders) ### Добавить в класс????
        theoreticFrequency = density.getTheoreticFrequency(theoreticalProbabilities,self.statistic.frequency)
        countIntervals = len(theoreticFrequency)
        xi2see = pt.Pirson.khi_emp(countIntervals, theoreticFrequency,self.statistic.frequency)

        xi2see = "{:01.8}".format(xi2see)

        self.ui.xi2.setText(xi2see)

        k = countIntervals - 3 ###Добавить в класс ???

        self.ui.kFind.setText(str(k))

        alpha = float(self.ui.alpha.currentText())

        pirson = pt.Pirson()
        xi2crit = pirson.pirson[k][alpha]

        self.ui.xi2crit.setText(str(xi2crit))

    def setCharacteristic(self):
        midX = "{:01.8}".format(self.statistic.average_sample)
        d = "{:01.8}".format(self.statistic.dispersion)
        S = "{:01.8}".format(self.statistic.corrected_deviation)

        self.ui.averageSample.setText(midX)
        self.ui.sampleDispersion.setText(d)
        self.ui.sampleAverageSquareDeviation.setText(S)

    def setTables(self):
        countColumns = density.mergeIntervals(self.statistic.interval_series, self.statistic.frequency) #объединение интервалов
        self.statistic.countStatistic()
        self.ui.intervalSeries.setColumnCount(countColumns) #Установка количества колонок
        self.ui.theoreticalFrequencies.setColumnCount(countColumns)

        frequency = self.statistic.frequency
        variationSerias = self.statistic.interval_series

        theoreticalBorders =  copy.deepcopy(self.statistic.interval_series) ### Добавить в класс????
        density.transformBorders(theoreticalBorders, self.statistic.average_sample, self.statistic.deviation)
        theoreticalProbabilities = density.getPropabilities(theoreticalBorders) ### Добавить в класс????

        for i in range(countColumns):
            intervalVariation = "[%g, %g]" % (variationSerias[i][0], variationSerias[i][1])
            theoreticalVariation = "[%g, %g]" % (theoreticalBorders[i][0], theoreticalBorders[i][1])

            if i == 0:
                theoreticalVariation = "[-∞, %g]" % (theoreticalBorders[i][1]) 
            elif i == countColumns-1:
                theoreticalVariation = "[%g, +∞]" % (theoreticalBorders[i][0])

            self.ui.intervalSeries.horizontalHeader().resizeSection(i, len(intervalVariation) * 12)

            self.ui.intervalSeries.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(intervalVariation))
            self.ui.intervalSeries.horizontalHeaderItem(i).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.intervalSeries.setItem(0, i, QtWidgets.QTableWidgetItem(str(frequency[i])))
            self.ui.intervalSeries.item(0, i).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.theoreticalFrequencies.horizontalHeader().resizeSection(i, len(theoreticalVariation) * 12)

            self.ui.theoreticalFrequencies.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(theoreticalVariation))
            self.ui.theoreticalFrequencies.horizontalHeaderItem(i).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.theoreticalFrequencies.setItem(0, i, QtWidgets.QTableWidgetItem(str(theoreticalProbabilities[i])))
            self.ui.theoreticalFrequencies.item(0, i).setFlags(QtCore.Qt.ItemIsEnabled)
        


    def openFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл", "./", "Text file (*.txt)")
        fileName = fileName[0]
        #interval_amount = self.ui.interval_amount_spin_box.value()

        try:
            file = open(fileName, 'r', encoding='utf-8')
            line = file.readline()
            
            serias = line.split(' ')
            serias = [float(var) for var in serias]
            self.statistic.setSeries(serias)
            
            string_serias = ", ".join(str(var) for var in self.statistic.series)
            self.ui.InitionalArray.setText(string_serias)
            #self.ui.interval_amount_button.setEnabled(True)
            #self.ui.interval_amount_spin_box.setEnabled(True)
            

        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка ввода", "Ошибка ввода!\nПроверьте корректность входного файла")
        self.solve()

    def buildPlot(self):
        self.ui.graph.clear()

        h = self.statistic.interval_series[0][1] - self.statistic.interval_series[0][0]
        var = self.statistic.interval_series
        w = [round((i / h), 4) for i in self.statistic.relative_frequency]

        deltaX = (var[-1][1] - var[0][0])*0.05
        self.ui.graph.setXRange(var[0][0]-deltaX, var[- 1][1]+deltaX)

        self.plotHistogramma(var, w)

        var1 = self.statistic.grouped
        print(var1, self.statistic.interval_series, w)

        self.plotPoligon(var1, w)

        leftBorder = self.statistic.interval_series[0][0]
        rightBorder = self.statistic.interval_series[-1][1]
        maxy = self.plotDistribution(leftBorder, rightBorder)

        maxY = max(max(w),maxy)
        self.ui.graph.setYRange(0, maxY*1.05)

        
    
    def plotDistribution(self, leftBorder, rightBorder):
        x = np.linspace(leftBorder,rightBorder, 1000)
        a = self.statistic.average_sample
        sigma = self.statistic.deviation
        y = density.densityFunction(a,sigma,x)
        self.ui.graph.plot(x,y, pen=self.pen2, name="Плотность распределения")
        return max(y)

    def plotPoligon(self, variationSeries : list, periodicity : list):
        self.ui.graph.setLabel('bottom', "x", **self.style1)
        self.ui.graph.plot(variationSeries, periodicity, pen=self.pen1, symbol='d', symbolSize=15, symbolBrush='b', name="Ломанная")

    def plotHistogramma(self, interlans, periodicity):
        amount = len(interlans)
        
        
        self.ui.graph.setYRange(0, max(periodicity))
        self.ui.graph.setLabel('bottom', "x", **self.style1)

        for i in range(len(interlans)):
            xi = [interlans[i][0], interlans[i][1]]
            yi = [periodicity[i], periodicity[i]]
            self.ui.graph.plot(xi, yi, pen=self.pen)

        for i in range(amount):
            xi = [interlans[i][0], interlans[i][0]]
            
            if (i  == 0):
                yi = [0, periodicity[i]]
            else:
                yi = [0, max(periodicity[i - 1], periodicity[i])]
            
            self.ui.graph.plot(xi, yi, pen=self.pen)

        xi = [interlans[amount - 1][1], interlans[amount - 1][1]]
        yi = [0, periodicity[amount - 1]]
        self.ui.graph.plot(xi, yi, pen=self.pen, name="Гистограмма")

def main():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()