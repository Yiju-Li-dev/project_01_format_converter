from functions import convert_avi_to_mp4
import time
import sys
import os
import subprocess
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QTextEdit, QHBoxLayout, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QRunnable, QThreadPool


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.length = 0
        self.counter = 1
        self.semaphore = threading.Semaphore(1)

        self.threadpool = QThreadPool()

        self.btn_input_dir = QPushButton('Choose Input Directory', self)
        self.btn_output_dir = QPushButton('Choose Output Directory', self)
        self.btn_input_dir.clicked.connect(self.choose_input_dir)
        self.btn_output_dir.clicked.connect(self.choose_output_dir)
        self.input_dir = QLineEdit(self)
        self.output_dir = QLineEdit(self)

        
        layout_input_dir = QHBoxLayout()
        layout_input_dir.addWidget(self.btn_input_dir)
        layout_input_dir.addWidget(self.input_dir)

        layout_output_dir = QHBoxLayout()
        layout_output_dir.addWidget(self.btn_output_dir)
        layout_output_dir.addWidget(self.output_dir)

        self.btn_start = QPushButton('start', self)
        self.btn_start.clicked.connect(self.start)

        self.output = QTextEdit(self)

        layout2 = QVBoxLayout()
        layout2.addLayout(layout_input_dir)
        layout2.addLayout(layout_output_dir)
        layout2.addWidget(self.btn_start)
        layout2.addWidget(self.output)

        self.setLayout(layout2)

    def choose_input_dir(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Directory', os.getcwd())
        self.input_dir.setText(directory)

    def choose_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, 'Choose Directory', os.getcwd())
        self.output_dir.setText(directory)

    def start(self):
        commands = convert_avi_to_mp4(self.input_dir.text(), self.output_dir.text())
        self.length = len(commands)
        self.counter = 1
        for command in commands:
            self.semaphore.acquire()
            self.update_text_edit()
            worker = Worker(self,self.run_subprocess, command)
            #worker.signals.result.connect(self.update_text_edit)
            self.threadpool.start(worker)
            
    
    def run_subprocess(self, command):
        process = subprocess.run(command)
        #return process.stdout.decode()

    def update_text_edit(self):
        self.output.append('{}/{} Right Now\n'.format(str(self.counter), str(self.length)))
        self.counter += 1
        


class Worker(QtCore.QRunnable):
    def __init__(self, app, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.app = app
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(result)
        self.app.semaphore.release()
        

class WorkerSignals(QtCore.QObject):
    result = QtCore.pyqtSignal(str)
    

if __name__ == '__main__':
    print('haha')
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
