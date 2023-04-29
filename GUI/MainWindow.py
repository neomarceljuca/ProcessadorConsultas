import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QTextEdit, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Criando a caixa de texto de entrada
        self.input_box = QLineEdit()
        
        # Criando o botão
        self.button = QPushButton("EXECUTAR")
        self.button.clicked.connect(self.process_input)
        
        # Criando a caixa de saída de dados
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        
        # Criando o layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_box)
        layout.addWidget(self.button)
        layout.addWidget(self.output_box)
        
        # Definindo o layout para a janela
        self.setLayout(layout)
        
    def process_input(self):
        # Processando a entrada do usuário
        input_text = self.input_box.text()
        output_text = "Você digitou: {}".format(input_text)
        self.output_box.append(output_text)
        self.input_box.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
