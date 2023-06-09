
import os

os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\bin'
import sys
from parser import Parser
from parser.treeGraph import TreeGraph

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QApplication, QGraphicsScene, QGraphicsTextItem,
                               QGraphicsView, QLabel, QLineEdit, QPushButton,
                               QTextEdit, QVBoxLayout, QWidget)
from sql_parser import SQLParser


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.sql_query = ""
        self.queryTree = None
        # Criando a caixa de texto de entrada
        self.input_box = QLineEdit()
        
        # Criando o botão
        self.button = QPushButton("EXECUTAR")
        self.button.clicked.connect(self.process_input)
        
        # Criando a caixa de saída de dados
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        #Criando componente de imagem para grafo final
        self.label = QLabel(self)
        image_path = os.path.join(os.path.dirname(__file__), "")
        self.pixmap = QPixmap(image_path)
        
        self.label.setPixmap(self.pixmap)
        self.label.setMaximumSize(QSize(1400, 1000))
        
        # Criando o layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_box)
        layout.addWidget(self.button)
        layout.addWidget(self.output_box)
        layout.addWidget(self.label)
        
        # Definindo o layout para a janela
        self.setLayout(layout)
        
    def process_input(self):
        # Processando a entrada do usuário
        input_text = self.input_box.text()


        #validated = Parser.validate(input_text)
        try:
            parser = SQLParser(input_text)
            parsed_query = parser.parse()

            self.output_box.clear()
            output_text = "Você digitou: {}".format(input_text)
            # if validated:
            #     output_text += "\n Consulta Validada"
            #     self.generateGraphExample()
            # else:
            #     output_text += "\n Consulta Invalida!"
            #     self.pixmap.load("")
            #     self.label.setPixmap(self.pixmap)
            algebral_relacional_procesed_input = Parser.sql_to_relational_algebra(input_text)
            #print(algebral_relacional_procesed_input)
            self.generateGraphExample(algebral_relacional_procesed_input)
            output_text += "\nOrdem de execucao de consulta: " + str(self.queryTree.ordemDeExecucao())
            self.input_box.clear()
            self.output_box.clear()
            self.output_box.append(output_text)

        except Exception as e:
            self.input_box.clear()
            self.output_box.append(str(e))
            self.pixmap.load("")
            self.label.setPixmap(self.pixmap)

    def generateGraphExample(self, inputString):     
        # Specify the output path
        output_path = './app/RelationalTree'
        # Create a TreeGraph object, generate and export the graph as 'RelationalTree.png'
        tree = TreeGraph(inputString, output_path)
        self.queryTree = tree.tree
        #tree.generate_tree()
        tree.generate_queryTree()
        #Update GUI image
        newimage_path = os.path.join(os.path.dirname(__file__), "RelationalTree.png")
        self.pixmap.load(newimage_path)
        self.label.setPixmap(self.pixmap)
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


