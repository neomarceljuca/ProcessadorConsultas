
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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.sql_query = ""
        
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
        self.label.setMaximumSize(QSize(1000, 1000))
        
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
        validated = Parser.validate(input_text)
        self.output_box.clear()
        output_text = "Você digitou: {}".format(input_text)
        if validated:
            output_text += "\n Consulta Validada"
            #TO DO: adicionar corretamente o output do grafo da consulta
            self.generateGraphExample()
        else:
            output_text += "\n Consulta Invalida!"
            self.pixmap.load("")
            self.label.setPixmap(self.pixmap)
        self.output_box.append(output_text)
        self.input_box.clear()

    def generateGraphExample(self):
        inputString = "Pi Tb1.Nome, tb3.sal ( ((( (Pi Pk, nome(Sigma tb1.id > 300(Tb1))) |X| Tb1.pk = tb2.fk (Pi Pk,fk(Tb2))) |X| tb2.pk = tb3.fk (Pi Sal, fk((Sigma tb3.sal <> 0 (Tb3)))))))"
        #inputString = "( (A(B(C))) D (E(F))) G (H((I (J))))"
        
        # Create a list of nodes
        #nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        # Create a list of edges
        #edges = [('A', 'Long long text example'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F')]
        
        # Specify the output path
        output_path = './app/RelationalTree'
        # Create a TreeGraph object, generate and export the graph as 'RelationalTree.png'
        tree = TreeGraph(inputString, output_path)
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


