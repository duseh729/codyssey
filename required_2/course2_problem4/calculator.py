import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 450)
        self.init_state()
        self.create_ui()

    def init_state(self):
        self.current_value = '0'
        self.pending_operator = None
        self.waiting_for_new_operand = False
        self.last_pressed = None

    def create_ui(self):
        main_layout = QVBoxLayout()

        self.display = QLineEdit(self.current_value)
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
        if text in ['+', '-', '×', '÷']:
            self.set_operator(text)
        elif text == '=':
            self.equal()
        elif text == 'AC':
            self.reset()
        elif text == '+/-':
            self.negative_positive()
        elif text == '%':
            self.percent()
        elif text == '.':
            self.add_dot()
        else:  # number
            self.input_number(text)

        self.last_pressed = text

    def input_number(self, num):
        if self.waiting_for_new_operand:
            self.current_value = num
            self.waiting_for_new_operand = False
        else:
            if self.current_value == '0':
                self.current_value = num
            else:
                # 숫자 길이 제한 (소수점, 마이너스 제외한 숫자 길이 15자)
                digits_only = self.current_value.replace('.', '').replace('-', '')
                if len(digits_only) >= 12:
                    return
                self.current_value += num
        self.update_display()


    def add_dot(self):
        if '.' not in self.current_value:
            self.current_value += '.'
            self.update_display()

    def set_operator(self, op):
        if self.pending_operator and not self.waiting_for_new_operand:
            self.equal()
        self.pending_operator = op
        self.operand = self.current_value
        self.waiting_for_new_operand = True

    def reset(self):
        self.init_state()
        self.update_display()

    def negative_positive(self):
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        else:
            if self.current_value != '0':
                self.current_value = '-' + self.current_value
        self.update_display()

    def percent(self):
        try:
            val = float(self.current_value) / 100
            self.current_value = str(val)
            self.update_display()
        except:
            self.display.setText("Error")

    def equal(self):
        try:
            if not self.pending_operator:
                return
            a = float(self.operand)
            b = float(self.current_value)
            op = self.pending_operator
            result = 0

            if op == '+':
                result = self.add(a, b)
            elif op == '-':
                result = self.subtract(a, b)
            elif op == '×':
                result = self.multiply(a, b)
            elif op == '÷':
                result = self.divide(a, b)

        # 결과의 정수부 길이 12자 초과 시 예외
            result_str = str(int(result)) if result == int(result) else str(result)
            int_part = result_str.split('.')[0].replace('-', '')
            if len(int_part) > 12:
                raise OverflowError

            self.current_value = str(result)
            if result == int(result):
                self.current_value = str(int(result))
            self.pending_operator = None
            self.waiting_for_new_operand = True
            self.update_display()
        except ZeroDivisionError:
            self.display.setText("Can't divide by 0")
            self.init_state()
        except OverflowError:
            self.display.setText("Error: Too Large")
            self.init_state()
        except Exception:
            self.display.setText("Error")
            self.init_state()



    def update_display(self):
        try:
            if '.' in self.current_value:
                parts = self.current_value.split('.')
                int_part = "{:,}".format(int(float(parts[0])))
                self.display.setText(int_part + '.' + parts[1])
            else:
                self.display.setText("{:,}".format(int(float(self.current_value))))
        except:
            self.display.setText(self.current_value)

    # 사칙 연산 메소드
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
