from PyQt5 import QtCore, QtGui, QtWidgets
import json
import requests
import time
import hmac
import hashlib

# Define the API endpoint for the testnet environment
endpoint = 'https://testnet.binance.vision/api/v3/order'


class Ui_Form(object):
    def __init__(self):
        self.width = 412
        self.height = 768
        with open('config.json') as f:
            self.conf = json.load(f)

    def test(self, objectname, string):
        print(objectname, string)

    # Define the order parameters
    # symbol = 'BTCUSDT'
    # side = 'SELL'
    # quantity = '0.01'

    def create_stoploss_order(self, symbol, side, quantity, price, stoploss):
        # Define the request parameters
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'STOP_LOSS_LIMIT',
            'timeInForce': "GTC",
            'quantity': quantity * 100,
            "price": price,
            "stopPrice": stoploss,
            'timestamp': int(time.time() * 1000)  # current timestamp in milliseconds
        }

        # Generate the signature
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(str.encode(self.conf["secret_key"]), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        # Add the signature to the request parameters
        params['signature'] = signature
        # Send the request
        response = requests.post(endpoint, params=params, headers={'X-MBX-APIKEY': self.conf["api_key"]})
        # Print the response
        print(response.json())

    # Define the order parameters
    # symbol = 'BTCUSDT'
    # side = 'BUY'
    # quantity = '0.01'
    # trailing_stop_percent = '0.5'  # the percentage by which the stop price will trail the market price

    def create_trailing_order(self, symbol, side, quantity, trailing_stop_percent, price, stopPrice):
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'STOP_LOSS_LIMIT',
            'timeInForce': "GTC",
            'quantity': quantity*10,
            "price": price,
            "stopPrice": stopPrice,
            "trailingDelta": int(price * float(trailing_stop_percent) / 100) * 3,
            'timestamp': int(time.time() * 1000)  # current timestamp in milliseconds
        }
        # Generate the signature
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(str.encode(self.conf["secret_key"]), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

        # Add the signature to the request parameters
        params['signature'] = signature
        # Send the request
        response = requests.post(endpoint, params=params, headers={'X-MBX-APIKEY': self.conf["api_key"]})
        # Print the response
        print(response.json())

    def update_variable(self, dict_name, key_name, new_value):
        self.__getattribute__(dict_name)[key_name] = new_value

    def setupUi(self, Form):
        # Set windows size and not allow to adjust

        Form.resize(self.width, self.height)
        Form.setMaximumSize(self.width, self.height)
        Form.setMinimumSize(self.width, self.height)

        # Set QStyle
        qssFile = "./style.qss"
        with open(qssFile, "r") as fh:
            Form.setStyleSheet(fh.read())

        # Start to design
        self.windows_layout = QtWidgets.QGridLayout(Form)

        self.key_group_box = QtWidgets.QGroupBox(Form)
        self.key_group_box.setTitle("")
        self.key_layout = QtWidgets.QGridLayout(self.key_group_box)
        self.api_label = QtWidgets.QLabel(self.key_group_box)
        self.key_layout.addWidget(self.api_label, 0, 0, 1, 1)
        self.key_input = QtWidgets.QLineEdit(self.key_group_box)
        self.key_input.setObjectName("api_key")
        if self.conf["api_key"]:
            self.key_input.setText(self.conf["api_key"])
        self.key_input.editingFinished.connect(lambda: self.update_variable("conf", "api_key", self.key_input.text()))

        self.key_layout.addWidget(self.key_input, 1, 0, 1, 1)
        self.secret_label = QtWidgets.QLabel(self.key_group_box)
        self.key_layout.addWidget(self.secret_label, 2, 0, 1, 1)
        self.secret_input = QtWidgets.QLineEdit(self.key_group_box)
        if self.conf["secret_key"]:
            self.secret_input.setText(self.conf["secret_key"])
        self.secret_input.editingFinished.connect(
            lambda: self.update_variable("conf", "secret_key", self.secret_input.text()))
        self.key_layout.addWidget(self.secret_input, 3, 0, 1, 1)
        self.windows_layout.addWidget(self.key_group_box, 0, 0, 1, 1)

        self.basic_fonfig_box = QtWidgets.QGroupBox(Form)
        self.basic_fonfig_box.setTitle("")
        self.basic_fonfig_layout = QtWidgets.QGridLayout(self.basic_fonfig_box)
        self.symbol_combo = QtWidgets.QComboBox(self.basic_fonfig_box)
        self.symbol_combo.addItems(["BTCUSDT", "ETHUSDT"])
        self.basic_fonfig_layout.addWidget(self.symbol_combo, 0, 0, 1, 2)
        self.type_combo = QtWidgets.QComboBox(self.basic_fonfig_box)
        self.type_combo.addItems(["CROSS", "ISOLATE"])
        self.basic_fonfig_layout.addWidget(self.type_combo, 1, 0, 1, 1)
        self.side_combo = QtWidgets.QComboBox(self.basic_fonfig_box)
        self.side_combo.addItems(["LONG", "SHORT"])
        self.basic_fonfig_layout.addWidget(self.side_combo, 1, 1, 1, 1)
        self.windows_layout.addWidget(self.basic_fonfig_box, 1, 0, 1, 1)

        self.config_box = QtWidgets.QGroupBox(Form)
        self.config_box.setTitle("")
        self.config_layout = QtWidgets.QGridLayout(self.config_box)
        self.usdt_label = QtWidgets.QLabel(self.config_box)
        self.usdt_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.config_layout.addWidget(self.usdt_label, 0, 0, 1, 1)
        self.usdt_input = QtWidgets.QLineEdit(self.config_box)
        if self.conf["usdt"]:
            self.usdt_input.setText(self.conf["usdt"])
        self.usdt_input.editingFinished.connect(
            lambda: self.update_variable("conf", "usdt", self.usdt_input.text()))
        self.config_layout.addWidget(self.usdt_input, 0, 1, 1, 2)
        self.leverage_label = QtWidgets.QLabel(self.config_box)
        self.config_layout.addWidget(self.leverage_label, 1, 0, 1, 1)
        self.leverage_input = QtWidgets.QLineEdit(self.config_box)
        if self.conf["leverage"]:
            self.leverage_input.setText(self.conf["leverage"])
        self.leverage_input.editingFinished.connect(
            lambda: self.update_variable("conf", "leverage", self.leverage_input.text()))
        self.config_layout.addWidget(self.leverage_input, 1, 1, 1, 2)
        self.price_label = QtWidgets.QLabel(self.config_box)
        self.config_layout.addWidget(self.price_label, 2, 0, 1, 1)
        self.price_input = QtWidgets.QLineEdit(self.config_box)
        if self.conf["entry_price"]:
            self.price_input.setText(self.conf["entry_price"])
        self.price_input.editingFinished.connect(
            lambda: self.update_variable("conf", "entry_price", self.price_input.text()))
        self.config_layout.addWidget(self.price_input, 2, 1, 1, 2)
        self.stoploss_label = QtWidgets.QLabel(self.config_box)
        self.config_layout.addWidget(self.stoploss_label, 3, 0, 1, 1)
        self.stoploss_input = QtWidgets.QLineEdit(self.config_box)
        # --------------------------------------------
        if self.conf["stoploss"]:
            self.stoploss_input.setText(self.conf["stoploss"])
        self.stoploss_input.editingFinished.connect(
            lambda: self.update_variable("conf", "stoploss", self.stoploss_input.text()))
        self.config_layout.addWidget(self.stoploss_input, 3, 1, 1, 2)
        self.sequence_label = QtWidgets.QLabel(self.config_box)
        self.config_layout.addWidget(self.sequence_label, 4, 0, 1, 1)
        self.sequence_input = QtWidgets.QLineEdit(self.config_box)
        if self.conf["sequence"]:
            self.sequence_input.setText(self.conf["sequence"])
        self.sequence_input.editingFinished.connect(
            lambda: self.update_variable("conf", "sequence", self.sequence_input.text()))
        self.config_layout.addWidget(self.sequence_input, 4, 1, 1, 2)
        self.stopmovel_label = QtWidgets.QLabel(self.config_box)
        self.config_layout.addWidget(self.stopmovel_label, 5, 1, 1, 1)
        self.stopmovel_btn = QtWidgets.QPushButton(self.config_box)
        self.config_layout.addWidget(self.stopmovel_btn, 5, 2, 1, 1)
        self.windows_layout.addWidget(self.config_box, 2, 0, 1, 1)

        self.trailing_box = QtWidgets.QGroupBox(Form)
        self.trailing_box.setTitle("")
        self.trailing_layout = QtWidgets.QGridLayout(self.trailing_box)
        self.trainlingbuy_label = QtWidgets.QLabel(self.trailing_box)
        self.trailing_layout.addWidget(self.trainlingbuy_label, 0, 0, 1, 1)
        self.trailingbuy_btn = QtWidgets.QPushButton(self.trailing_box)
        self.trailing_layout.addWidget(self.trailingbuy_btn, 0, 2, 1, 1)
        self.trailingbuy_input = QtWidgets.QLineEdit(self.trailing_box)
        if self.conf["trailing_buy"]:
            self.trailingbuy_input.setText(self.conf["trailing_buy"])
        self.trailingbuy_input.editingFinished.connect(
            lambda: self.update_variable("conf", "trailing_buy", self.trailingbuy_input.text()))
        self.trailing_layout.addWidget(self.trailingbuy_input, 0, 1, 1, 1)
        self.trailingsell_label = QtWidgets.QLabel(self.trailing_box)
        self.trailing_layout.addWidget(self.trailingsell_label, 1, 0, 1, 1)
        self.trailingsell_btn = QtWidgets.QPushButton(self.trailing_box)
        self.trailing_layout.addWidget(self.trailingsell_btn, 1, 2, 1, 1)
        self.trailingsell_input = QtWidgets.QLineEdit(self.trailing_box)
        if self.conf["trailing_sell"]:
            self.trailingsell_input.setText(self.conf["trailing_sell"])
        self.trailingsell_input.editingFinished.connect(
            lambda: self.update_variable("conf", "trailing_sell", self.trailingsell_input.text()))
        self.trailing_layout.addWidget(self.trailingsell_input, 1, 1, 1, 1)
        self.activate_input = QtWidgets.QLineEdit(self.trailing_box)
        if self.conf["activate"]:
            self.activate_input.setText(self.conf["activate"])
        self.activate_input.editingFinished.connect(
            lambda: self.update_variable("conf", "activate", self.activate_input.text()))
        self.trailing_layout.addWidget(self.activate_input, 3, 1, 1, 1)
        self.activate_label = QtWidgets.QLabel(self.trailing_box)
        self.trailing_layout.addWidget(self.activate_label, 3, 0, 1, 1)
        self.windows_layout.addWidget(self.trailing_box, 3, 0, 1, 1)

        self.trailing_config_box = QtWidgets.QGroupBox(Form)
        self.trailing_config_layout = QtWidgets.QGridLayout(self.trailing_config_box)
        self.tp1_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.tp1_label, 0, 0, 1, 1)
        self.tp1_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["tp1"]:
            self.tp1_input.setText(self.conf["tp1"])
        self.tp1_input.editingFinished.connect(
            lambda: self.update_variable("conf", "tp1", self.tp1_input.text()))
        self.trailing_config_layout.addWidget(self.tp1_input, 0, 1, 1, 1)
        self.sl1_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.sl1_label, 0, 2, 1, 1)
        self.sl1_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["sl1"]:
            self.sl1_input.setText(self.conf["sl1"])
        self.sl1_input.editingFinished.connect(
            lambda: self.update_variable("conf", "sl1", self.sl1_input.text()))
        self.trailing_config_layout.addWidget(self.sl1_input, 0, 3, 1, 1)
        self.tp2_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.tp2_label, 1, 0, 1, 1)
        self.tp2_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["tp2"]:
            self.tp2_input.setText(self.conf["tp2"])
        self.tp2_input.editingFinished.connect(
            lambda: self.update_variable("conf", "tp2", self.tp2_input.text()))
        self.trailing_config_layout.addWidget(self.tp2_input, 1, 1, 1, 1)
        self.sl2_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.sl2_label, 1, 2, 1, 1)
        self.sl2_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["sl2"]:
            self.sl2_input.setText(self.conf["sl2"])
        self.sl2_input.editingFinished.connect(
            lambda: self.update_variable("conf", "sl2", self.sl2_input.text()))
        self.trailing_config_layout.addWidget(self.sl2_input, 1, 3, 1, 1)
        self.tp3_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.tp3_label, 2, 0, 1, 1)
        self.tp3_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["tp3"]:
            self.tp3_input.setText(self.conf["tp3"])
        self.tp3_input.editingFinished.connect(
            lambda: self.update_variable("conf", "tp3", self.tp3_input.text()))
        self.trailing_config_layout.addWidget(self.tp3_input, 2, 1, 1, 1)
        self.sl3_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.sl3_label, 2, 2, 1, 1)
        self.sl3_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["sl3"]:
            self.sl3_input.setText(self.conf["sl3"])
        self.sl3_input.editingFinished.connect(
            lambda: self.update_variable("conf", "sl3", self.sl3_input.text()))
        self.trailing_config_layout.addWidget(self.sl3_input, 2, 3, 1, 1)
        self.tp4_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.tp4_label, 3, 0, 1, 1)
        self.tp4_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["tp4"]:
            self.tp4_input.setText(self.conf["tp4"])
        self.tp4_input.editingFinished.connect(
            lambda: self.update_variable("conf", "tp4", self.tp4_input.text()))
        self.trailing_config_layout.addWidget(self.tp4_input, 3, 1, 1, 1)
        self.sl4_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.sl4_label, 3, 2, 1, 1)
        self.sl4_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["sl4"]:
            self.sl4_input.setText(self.conf["sl4"])
        self.sl4_input.editingFinished.connect(
            lambda: self.update_variable("conf", "sl4", self.sl4_input.text()))
        self.trailing_config_layout.addWidget(self.sl4_input, 3, 3, 1, 1)
        self.tp5_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.tp5_label, 4, 0, 1, 1)
        self.tp5_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["tp5"]:
            self.tp5_input.setText(self.conf["tp5"])
        self.tp5_input.editingFinished.connect(
            lambda: self.update_variable("conf", "tp5", self.tp5_input.text()))
        self.trailing_config_layout.addWidget(self.tp5_input, 4, 1, 1, 1)
        self.sl5_label = QtWidgets.QLabel(self.trailing_config_box)
        self.trailing_config_layout.addWidget(self.sl5_label, 4, 2, 1, 1)
        self.sl5_input = QtWidgets.QLineEdit(self.trailing_config_box)
        if self.conf["sl5"]:
            self.sl5_input.setText(self.conf["sl5"])
        self.sl5_input.editingFinished.connect(
            lambda: self.update_variable("conf", "sl5", self.leverage_input.sl5_input()))
        self.trailing_config_layout.addWidget(self.sl5_input, 4, 3, 1, 1)
        self.windows_layout.addWidget(self.trailing_config_box, 4, 0, 1, 1)
        self.placeorder_btn = QtWidgets.QPushButton(Form)
        self.placeorder_btn.clicked.connect(self.on_place_order)
        self.windows_layout.addWidget(self.placeorder_btn, 5, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Binance Control"))

        self.api_label.setText(_translate("Form", "API KEY"))
        self.secret_label.setText(_translate("Form", "Secret Key"))
        self.usdt_label.setText(_translate("Form", "Fixo USDT ($)"))
        self.leverage_label.setText(_translate("Form", "Leverage (Nx)"))
        self.price_label.setText(_translate("Form", "Entry Price ($)"))
        self.stoploss_label.setText(_translate("Form", "Stop/Orders (%)"))
        self.sequence_label.setText(_translate("Form", "Sequence/Orders"))
        self.stopmovel_label.setText(_translate("Form", "Stop Movel"))
        self.stopmovel_btn.setText(_translate("Form", "ON/OFF"))
        self.trainlingbuy_label.setText(_translate("Form", "Trailing Buy (%)"))
        self.trailingbuy_btn.setText(_translate("Form", "ON/OFF"))
        self.trailingsell_label.setText(_translate("Form", "Trailing Sell (%)"))
        self.trailingsell_btn.setText(_translate("Form", "ON/OFF"))
        self.activate_label.setText(_translate("Form", "Activate"))

        self.trailing_config_box.setTitle(_translate("Form", "GroupBox"))
        self.tp1_label.setText(_translate("Form", "TP1(%)"))
        self.sl1_label.setText(_translate("Form", "SL1(%)"))
        self.tp2_label.setText(_translate("Form", "TP2(%)"))
        self.sl2_label.setText(_translate("Form", "SL1(%)"))
        self.tp3_label.setText(_translate("Form", "TP3(%)"))
        self.sl3_label.setText(_translate("Form", "SL1(%)"))
        self.tp4_label.setText(_translate("Form", "TP4(%)"))
        self.sl4_label.setText(_translate("Form", "SL1(%)"))
        self.tp5_label.setText(_translate("Form", "TP5(%)"))
        self.sl5_label.setText(_translate("Form", "SL1(%)"))
        self.placeorder_btn.setText(_translate("Form", "Place Order"))

    def create_order_sequence(self):
        entry_price = int(self.conf["entry_price"])
        stoploss = int(entry_price * 0.99)
        self.create_stoploss_order("BNBUSDT", "BUY", 0.01, entry_price, stoploss)
        entry_price = int(stoploss * 0.99)
        stoploss = int(entry_price * 0.99)
        self.create_stoploss_order("BNBUSDT", "BUY", 0.01, entry_price, stoploss)
        entry_price = int(stoploss * 0.99)
        stoploss = int(entry_price * 0.99)
        self.create_stoploss_order("BNBUSDT", "BUY", 0.01, entry_price, stoploss)

    def create_order_trailing(self):
        price = int(self.conf["entry_price"])
        stoploss = price * (100 - float(self.conf["sl1"])) / 100
        self.create_trailing_order("BNBUSDT", "BUY", 0.01, self.conf["sl1"], price, stoploss)

        stoploss = price * (100 - float(self.conf["sl2"])) / 100
        self.create_trailing_order("BNBUSDT", "BUY", 0.01, self.conf["sl2"], price, stoploss)

        stoploss = price * (100 - float(self.conf["sl3"])) / 100
        self.create_trailing_order("BNBUSDT", "BUY", 0.01, self.conf["sl3"], price, stoploss)

        stoploss = price * (100 - float(self.conf["sl4"])) / 100
        self.create_trailing_order("BNBUSDT", "BUY", 0.01, self.conf["sl4"], price, stoploss)

        stoploss = price * (100 - float(self.conf["sl5"])) / 100
        self.create_trailing_order("BNBUSDT", "BUY", 0.01, self.conf["sl5"], price, stoploss)

    def on_place_order(self):
        self.create_order_sequence()
        self.create_order_trailing()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
