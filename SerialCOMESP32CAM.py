from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from ast import literal_eval

app=QtWidgets.QApplication(sys.argv)
win = uic.loadUi("QT_test.ui")

win.setWindowTitle("SerialMonitor")

serial=QSerialPort()
serial.setBaudRate(115200)

def BeginSerialCOMPort():
    nameBt=win.ComBt.text()
    if nameBt=='SEARCH':
        portList=[]
        ports=QSerialPortInfo().availablePorts()
        for port in ports:
            portList.append(port.portName())
        if len(portList)==0:
            win.lineEditStatus.setText("Empty com port list")
            win.comboBoxCOMPORT.clear()
        else:
            portComList=list(set(portList))
            win.comboBoxCOMPORT.addItems(portComList)
            win.ComBt.setText('OPEN')
    if nameBt=='OPEN':
        serial.setPortName(win.comboBoxCOMPORT.currentText())
        try:
        # Откройте последовательный порт
           ser=serial.open(QIODevice.ReadWrite)
           if(ser):
               text_str="Opened com port: "+ win.comboBoxCOMPORT.currentText()
               win.lineEditStatus.setText(text_str)
               win.ComBt.setText('CLOSE')
               win.WriteBt.setEnabled(True)
           else:
              win.lineEditStatus.setText("Can't open com port")

        except:
            win.lineEditStatus.setText("Can't open com port")
            return None

    if nameBt=='CLOSE':
        win.ComBt.setText('SEARCH')
        serial.close()
        text_str="Closed com port: "+ win.comboBoxCOMPORT.currentText()
        win.lineEditStatus.setText(text_str)
        win.WriteBt.setEnabled(False)
        win.comboBoxCOMPORT.clear()


def onRead():
    rx=serial.readLine()
    rxs=str(rx,'utf-8')
    win.plainTextEditRead.appendPlainText(rxs)

def onWrite():
    text_str=win.lineEditWrite.text()
    win.plainTextEditWrite.appendPlainText(text_str)

    if win.radioButtonFormat.isChecked():
        win.lineEditStatus.setText("Format: string")
        tx_byte=text_str.encode()
    else:
        convert_int = literal_eval(text_str)
        tx_str=str(convert_int)
        tx_byte=tx_str.encode()

    serial.write(tx_byte)

def onToggle():
    if win.radioButtonFormat.isChecked():
        win.lineEditStatus.setText("Format: string")
    else:
        win.lineEditStatus.setText("Format: hex")

win.ComBt.clicked.connect(BeginSerialCOMPort)
win.WriteBt.clicked.connect(onWrite)
serial.readyRead.connect(onRead)
win.radioButtonFormat.toggled.connect(onToggle)

win.show()
sys.exit(app.exec())
