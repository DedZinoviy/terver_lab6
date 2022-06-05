from cmath import pi
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
from dialogGrouped import Ui_dialogGruupped
import puason

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

class dialogGroupped(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_dialogGruupped()
        self.ui.setupUi(self)
        
        self.mainwindow = parent

        self.buttons = self.ui.buttonBox.buttons()
        self.buttons[0].setText("Ок")
        self.buttons[1].setText("Отмена")

        self.ui.countGrouped.setValue = 5

        self.setTable()

        self.ui.countGrouped.valueChanged.connect(self.setTable)
    
    def setTable(self):
        columnCount = self.ui.countGrouped.value()

        if columnCount < self.ui.tableWidget.columnCount():
            self.ui.tableWidget.setColumnCount(columnCount)
        else:
            for i in range(self.ui.tableWidget.columnCount(), columnCount):
                self.ui.tableWidget.insertColumn(i)

                var = i
                self.ui.tableWidget.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(''))
                self.ui.tableWidget.horizontalHeader().resizeSection(i, 12)

                self.ui.tableWidget.setItem(0, i, QtWidgets.QTableWidgetItem(str(var)))
                self.ui.tableWidget.item(0,i).setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget.setItem(1, i, QtWidgets.QTableWidgetItem("1"))

    def accept(self):
        amount = self.ui.tableWidget.columnCount()
        values= []
        frequency = []
            
        try:
            row_1 = self.ui.tableWidget.item(0, 0).text()
            row_2 = self.ui.tableWidget.item(1, 0).text()
            values.append(0)
            frequency.append(int(row_2))
            
            for i in range(1, amount):
                row_2 = self.ui.tableWidget.item(1, i).text()
                values.append(i)
                frequency.append(int(row_2))        
                            
            self.mainwindow.statistic.setGroupedSeries(values, frequency)
            super().accept()
        
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка ввода", "Некорректное значение")


class mywindow(QtWidgets.QMainWindow):
    '''Конструктор гловного окна'''
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        

        self.dialog = dialogwindow(parent=self)
        self.dialogGroupped = dialogGroupped(parent=self)
        
        self.pen = pg.mkPen(color='r', width=3)
        self.pen1 = pg.mkPen(color='b', width=3)
        self.pen2 = pg.mkPen(color='g', width=3)
        self.pen3 = pg.mkPen(color='k', width=3)
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
        self.ui.distributionType.currentIndexChanged.connect(self.changeDistributionType)
        self.ui.inputGroupedSeriesAction.triggered.connect(self.openDialogGroupped)
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
        self.setDensity()
        self.setXi2()
        self.buildPlot()  

    def changeDistributionType(self):
        if self.ui.distributionType.currentIndex() == 0: #нормальное
            self.ui.inputIntervalSeriesAction.setEnabled(True)
            self.ui.inputGroupedSeriesAction.setDisabled(True)

            self.ui.sigma.setVisible(True)
            self.ui.sigmaLabel.setVisible(True)

            self.ui.aLabel.setText("a*")

            self.ui.kFindLabel.setText("k = m - 3")

            self.ui.InitionalArray.setVisible(True)
            self.ui.InitionalArrayLabel.setVisible(True)

            self.ui.distributionDensity.setPixmap(QtGui.QPixmap("img/normalDistribution.png"))

            self.ui.intervalSeries.setVisible(True)
            self.ui.intervalSeriesLabel.setVisible(True)
            self.ui.openFileAction.setEnabled(True)

            self.ui.theoreticalFrequencies.setColumnCount(0)
            self.ui.theoreticalFrequencies.setRowCount(1)
        else: #Пуассона
            self.ui.inputGroupedSeriesAction.setEnabled(True)
            self.ui.inputIntervalSeriesAction.setDisabled(True)
            self.ui.openFileAction.setDisabled(True)

            self.ui.sigma.setVisible(False)
            self.ui.sigmaLabel.setVisible(False)

            self.ui.aLabel.setText("λ*")
            
            self.ui.kFindLabel.setText("k = m - 2")

            self.ui.InitionalArray.setVisible(False)
            self.ui.InitionalArrayLabel.setVisible(False)

            self.ui.distributionDensity.setPixmap(QtGui.QPixmap("img/puassonDistribution.png"))

            self.ui.intervalSeries.setVisible(False)
            self.ui.intervalSeriesLabel.setVisible(False)

            self.ui.theoreticalFrequencies.setColumnCount(6)
            self.ui.theoreticalFrequencies.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("xᵢ"))
            self.ui.theoreticalFrequencies.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("mᵢ"))
            self.ui.theoreticalFrequencies.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("pᵢ"))
            self.ui.theoreticalFrequencies.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("n⋅pᵢ"))
            self.ui.theoreticalFrequencies.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("(mᵢ-npᵢ)²"))
            self.ui.theoreticalFrequencies.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("(mᵢ-npᵢ)²/npᵢ"))
            self.ui.theoreticalFrequencies.setRowCount(0)
        
        self.ui.averageSample.clear()
        self.ui.sampleDispersion.clear()
        self.ui.sampleAverageSquareDeviation.clear()
        self.ui.aFind.clear()
        self.ui.sigma.clear()
        self.ui.kFind.clear()
        self.ui.xi2.clear()
        self.ui.xi2crit.clear()
        self.ui.resultCompare.clear()
        self.ui.graph.clear()
        self.ui.findDistributionDensity.clear()
        self.solve()
            

    def openDialogGroupped(self):
        if self.dialogGroupped.exec():
                try:
                    self.solve()
                except:
                    pass
        else:
            print("Cansel")

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
            distStr1 = ["нормальному", ""]
            distStr2 = ["", "Пуассона"]
            distTypeIndex = self.ui.distributionType.currentIndex()
            if (resCompare):
                strCompare = "Эмпирические данные не противоречат гипотезе о соответствии %s распределению %s" % (distStr1[distTypeIndex], distStr2[distTypeIndex])
            else:
                strCompare = "Отвергаем гипотезу о соответствии %s распределению %s" % (distStr1[distTypeIndex], distStr2[distTypeIndex])
            
            self.ui.resultCompare.setText(strCompare)
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка данных", "Ошибка данных!\nВведите входные данные")

    def setDensity(self):
        distType = self.ui.distributionType.currentIndex()
        if distType == 0:
            strDensity = "f(x)="+density.getDensity(self.statistic.average_sample, self.statistic.deviation)      
        elif distType == 1:
            strDensity = "P(X=xᵢ)="+puason.getDensity(self.statistic.groupedAverageSample)
        self.ui.findDistributionDensity.setText(strDensity)  

    def changeXi2crit(self):
        distType = self.ui.distributionType.currentIndex()
        if distType == 0:
            countIntervals = len(self.statistic.frequency)
            k = countIntervals - 3 ###Добавить в класс ???
        elif distType == 1:
            countIntervals = len(self.statistic.groupedFrequency)
            k = countIntervals - 2
        alpha = float(self.ui.alpha.currentText())

        pirson = pt.Pirson()
        xi2crit = pirson.pirson[k][alpha]

        self.ui.xi2crit.setText(str(xi2crit))

    def setPointAssessments(self):
        distType = self.ui.distributionType.currentIndex()
        if distType == 0:
            a = "{:01.8}".format(self.statistic.average_sample)
            sigma = "{:01.8}".format(self.statistic.deviation)
            self.ui.sigma.setText(sigma)
        elif distType == 1:
            a = "{:01.8}".format(self.statistic.groupedAverageSample)
        
        self.ui.aFind.setText(a)
 

    def setXi2(self):
        distType = self.ui.distributionType.currentIndex()
        if distType == 0:
            theoreticalBorders =  copy.deepcopy(self.statistic.interval_series) ### Добавить в класс????
            density.transformBorders(theoreticalBorders, self.statistic.average_sample, self.statistic.deviation)
            theoreticalProbabilities = density.getPropabilities(theoreticalBorders) ### Добавить в класс????
            theoreticFrequency = density.getTheoreticFrequency(theoreticalProbabilities,self.statistic.frequency)
            countIntervals = len(theoreticFrequency)
            k = countIntervals - 3 ###Добавить в класс ???
            empericalFrequency = self.statistic.frequency
        elif distType == 1:
            countIntervals = len(self.statistic.groupedFrequency)
            lamb = lamb = round(self.statistic.groupedAverageSample,8)
            propabilities = [round(i,4) for i in puason.getPropabilities(self.statistic.groupedRange, lamb)]
            theoreticFrequency = [round(i,4) for i in puason.getTheoreticFrequency(propabilities, self.statistic.groupedFrequency)]
            k = countIntervals - 2
            empericalFrequency = self.statistic.groupedFrequency
        
        xi2see, var1, var2 = pt.Pirson.khi_emp(countIntervals, theoreticFrequency, empericalFrequency)

        xi2see = "{:01.8}".format(xi2see)

        self.ui.xi2.setText(xi2see)

        self.ui.kFind.setText(str(k))

        alpha = float(self.ui.alpha.currentText())

        pirson = pt.Pirson()
        xi2crit = pirson.pirson[k][alpha]

        self.ui.xi2crit.setText(str(xi2crit))

    def setCharacteristic(self):
        distType = self.ui.distributionType.currentIndex()
        if distType == 0:
            midX = "{:01.8}".format(self.statistic.average_sample)
            d = "{:01.8}".format(self.statistic.dispersion)
            S = "{:01.8}".format(self.statistic.corrected_deviation)
        elif distType == 1:
            midX = "{:01.8}".format(self.statistic.groupedAverageSample)
            d = "{:01.8}".format(self.statistic.groupedDispersion)
            S = "{:01.8}".format(self.statistic.groupedCorrected_deviation)

        self.ui.averageSample.setText(midX)
        self.ui.sampleDispersion.setText(d)
        self.ui.sampleAverageSquareDeviation.setText(S)

    def setTables(self):
        distType = self.ui.distributionType.currentIndex()
        if distType == 0:
            self.setTablesNormal()
        elif distType == 1:
            self.setTablePuason()

    def setTablePuason(self):
        countRows = len(self.statistic.groupedRange)
        self.ui.theoreticalFrequencies.setRowCount(countRows)

        xi = [round(i,4) for i in self.statistic.groupedRange]
        mi = [round(i,4) for i in self.statistic.groupedFrequency]
        lamb = round(self.statistic.groupedAverageSample,8)
        pi = [round(i,4) for i in puason.getPropabilities(xi, lamb)]
        npi = [round(i,4) for i in puason.getTheoreticFrequency(pi, mi)]

        Khi, sqr, sqrDevision  = pt.Pirson.khi_emp(countRows, npi, mi)

        sqr = [round(i,4) for i in sqr]
        sqrDevision = [round(i,4) for i in sqrDevision]

        for i in range(countRows):
            self.ui.theoreticalFrequencies.setItem(i, 0, QtWidgets.QTableWidgetItem(str(xi[i])))
            self.ui.theoreticalFrequencies.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.theoreticalFrequencies.setItem(i,1, QtWidgets.QTableWidgetItem(str(mi[i])))
            self.ui.theoreticalFrequencies.item(i,1).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.theoreticalFrequencies.setItem(i,2, QtWidgets.QTableWidgetItem(str(pi[i])))
            self.ui.theoreticalFrequencies.item(i,2).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.theoreticalFrequencies.setItem(i,3, QtWidgets.QTableWidgetItem(str(npi[i])))
            self.ui.theoreticalFrequencies.item(i,3).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.theoreticalFrequencies.setItem(i,4, QtWidgets.QTableWidgetItem(str(sqr[i])))
            self.ui.theoreticalFrequencies.item(i,4).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.theoreticalFrequencies.setItem(i,5, QtWidgets.QTableWidgetItem(str(sqrDevision[i])))
            self.ui.theoreticalFrequencies.item(i,5).setFlags(QtCore.Qt.ItemIsEnabled)

    

    def setTablesNormal(self):
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
            lines = file.readlines()
            serias = []
            
            for line in lines:
                line = line.strip()
                line = line.split()
                for var in line:
                    serias.append(float(var))
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
        legend = self.ui.graph.addLegend(labelTextColor='k', labelTextSize='12pt', verSpacing=12)

        distType = self.ui.distributionType.currentIndex()
        if distType == 0:
            h = self.statistic.interval_series[0][1] - self.statistic.interval_series[0][0]
            var = self.statistic.interval_series
            w = [round((i / h), 4) for i in self.statistic.relative_frequency]

            self.plotHistogramma(var, w)

            var1 = self.statistic.grouped
            self.plotPoligon(var1, w, self.pen1, "Ломаная через середины")

            leftBorder = self.statistic.interval_series[0][0]
            rightBorder = self.statistic.interval_series[-1][1]
            maxy = self.plotDistribution(leftBorder, rightBorder)

            minX = var[0][0]
            maxX = var[-1][1]
            maxY = max(maxy, max(w))
            minY = 0
        elif distType == 1:
            amount = sum(self.statistic.groupedFrequency)
            relativeFrequency = [round(item/amount,4) for item in self.statistic.groupedFrequency]
            var = self.statistic.groupedRange
            self.plotPoligon(var, relativeFrequency, self.pen, "Эмпирически")

            lamb = round(self.statistic.groupedAverageSample,8)
            propability = [round(i,4) for i in puason.getPropabilities(self.statistic.groupedRange, lamb)]
            self.plotPoligon(var, propability, self.pen2, "Теоретически")

            minX = 0
            minY = min(min(relativeFrequency), min(propability))
            maxX = self.statistic.groupedRange[-1]
            maxY = max(max(relativeFrequency), max(propability))

        self.ui.graph.setXRange(minX, maxX)
        self.ui.graph.setYRange(minY, maxY)

    
    def plotDistribution(self, leftBorder, rightBorder):
        x = np.linspace(leftBorder,rightBorder, 1000)
        a = self.statistic.average_sample
        sigma = self.statistic.deviation
        y = density.densityFunction(a,sigma,x)
        self.ui.graph.plot(x,y, pen=self.pen2, name="Плотность распределения")
        return max(y)

    def plotPoligon(self, variationSeries : list, periodicity : list, pen, name=""):
        self.ui.graph.setLabel('bottom', "x", **self.style1)
        self.ui.graph.plot(variationSeries, periodicity, pen=pen, symbol='d', symbolSize=15, symbolBrush='b', name=name)

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