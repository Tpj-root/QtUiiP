# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from qtvcp.widgets.simple_widgets import Dial, LCDNumber  # Ensure these are correctly imported
from flask import Flask, render_template_string, request
import threading

# Flask app
app = Flask(__name__)

# Global state
state = {"dial_value": 0}

# HTML template for the web interface
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>PyQt5 Web Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        input[type="range"] { width: 300px; }
    </style>
</head>
<body>
    <h1>App Devby Sh4D0W6 AKA SAB</h1>
    <h1>PyQt5 Web Control</h1>
    <p>Dial Value: <span id="value">{{ value }}</span></p>
    <input type="range" id="dial" min="0" max="99" value="{{ value }}" 
        oninput="updateValue(this.value)" onchange="sendValue(this.value)">
    <p>Dial Value1: <span id="value1">{{ value1 }}</span></p>
    <input type="range" id="dial1" min="0" max="99" value1="{{ value1 }}" 
        oninput="updateValue(this.value1)" onchange="sendValue(this.value1)">
    <script>
        function updateValue(value) {
            document.getElementById('value').textContent = value;
        }
        function sendValue(value) {
            fetch('/update', { 
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ dial_value: value })
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_template, value=state["dial_value"])

@app.route("/update", methods=["POST"])
def update():
    data = request.get_json()
    state["dial_value"] = int(data["dial_value"])
    return "OK", 200

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(233, 294)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dial = Dial(self.centralwidget)
        self.dial.setGeometry(QtCore.QRect(60, 160, 100, 100))
        self.dial.setObjectName("dial")
        self.lcdnumber = LCDNumber(self.centralwidget)
        self.lcdnumber.setGeometry(QtCore.QRect(90, 50, 64, 23))
        self.lcdnumber.setObjectName("lcdnumber")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 233, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.dial.valueChanged['int'].connect(self.lcdnumber.display)
        self.dial.valueChanged['int'].connect(self.update_state)  # Sync state with web
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update_state(self, value):
        state["dial_value"] = value

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

def start_flask():
    app.run(host="0.0.0.0", port=3400, debug=False, use_reloader=False)


if __name__ == "__main__":
    import sys
    app_thread = threading.Thread(target=start_flask, daemon=True)
    app_thread.start()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # Timer to update GUI from web state
    def sync_gui():
        ui.dial.setValue(state["dial_value"])
    timer = QtCore.QTimer()
    timer.timeout.connect(sync_gui)
    timer.start(100)  # Check every 100 ms

    MainWindow.show()
    sys.exit(app.exec_())

