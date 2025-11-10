import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 450)
        self.create_ui()
        self.last_pressed = None  # 마지막에 누른 버튼 (연산 중복 방지용)

    def create_ui(self):
        main_layout = QVBoxLayout()

        self.display = QLineEdit('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet("font-size: 30px; padding: 10px;")
        self.display.setReadOnly(True)
        main_layout.addWidget(self.display)

        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid_layout = QGridLayout()

        for row, row_vals in enumerate(buttons):
            for col, btn_text in enumerate(row_vals):
                btn = QPushButton(btn_text)
                btn.setFixedSize(60, 60)
                btn.setStyleSheet("font-size: 18px;")
                btn.clicked.connect(lambda checked, txt=btn_text: self.on_button_clicked(txt))

                if btn_text == '0':
                    grid_layout.addWidget(btn, row + 1, 0, 1, 2)
                    btn.setFixedSize(135, 60)
                elif btn_text == '=':
                    grid_layout.addWidget(btn, row + 1, 3)
                else:
                    col_offset = 1 if row == 4 and col > 0 else 0
                    grid_layout.addWidget(btn, row + 1, col + col_offset)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def on_button_clicked(self, text):
        current = self.display.text().replace(",", "")
        if text in ['+', '-', '×', '÷']:
            if self.last_pressed == text:
                return  # 연산 중복 방지
            if self.last_pressed in ['+', '-', '×', '÷']:
                self.display.setText("{:,}".format(int(current[:len(current)-1])) + text)
            else:
                self.display.setText("{:,}".format(int(current)) + text)
        elif text == '=':
            try:
                expression = current.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.display.setText("{:,}".format(result))
            except Exception:
                self.display.setText("Error")
        elif text == 'AC':
            self.display.setText('0')
        elif text == '+/-':
            try:
                if current.startswith('-'):
                    self.display.setText(current[1:])
                else:
                    self.display.setText('-' + current)
            except:
                pass
        elif text == '%':
            try:
                self.display.setText(str(float(current) / 100))
            except:
                pass
        else:
            if current == '0' or self.last_pressed == '=':
                current = ''
            new_value = current + text
            self.display.setText(self.format_number(new_value))

        self.last_pressed = text

    def format_number(self, value):
        for op in ['+', '-', '×', '÷']:
            if op in value:
                parts = value.rsplit(op, 1)
                if len(parts) == 2:
                    left, right = parts
                    try:
                        left = "{:,}".format(int(left))
                        right = "{:,}".format(int(right))
                    except:
                        pass
                    return left + op + right
        try:
            return "{:,}".format(int(value))
        except:
            return value


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
