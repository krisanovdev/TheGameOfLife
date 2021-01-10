from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPen, QBrush
import sys
import random

ALIVE_CELL_STAY_ALIVE_CONDITION = [2, 3]
NEW_CELL_BIRTH_CONDITION = [3]
INITIAL_GENERATION_LIFE_CELL_PROBABILITY = 0.30
LIFE_BOARD_WIDGET_SIZE = 600
LIFE_BOARD_CELL_SIZE = 10


class LifeWidget(QGraphicsView):

    CELL_ALIVE = Qt.green
    CELL_DEAD = Qt.white

    def __init__(self, size, cellSize, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cellSize    = cellSize
        self._cellsCount   = int(size / cellSize)
        self._board       = None
        self._scene       = QGraphicsScene()

        self.setScene(self._scene)
        self.resize(size, size)

        initialBoard = []
        for i in range(0, self._cellsCount):
            initialBoard.append([None] * self._cellsCount)
            for j in range(0, self._cellsCount):
                initialBoard[i][j] = self.getRandomCell()

        self.setNewBoard(initialBoard)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.moveToNextGeneration()
        event.accept()

    def getRandomCell(self):
        return self.CELL_ALIVE if random.uniform(0, 1) <= INITIAL_GENERATION_LIFE_CELL_PROBABILITY else self.CELL_DEAD

    def setNewBoard(self, board):
        self._board = board
        self._scene.clear()
        for i in range(0, self._cellsCount):
            for j in range(0, self._cellsCount):
                self.updateColorAt(i, j)

    def updateColorAt(self, x, y):
        rect = QRectF(x * self._cellSize, y * self._cellSize, self._cellSize, self._cellSize)
        self._scene.addRect(rect, QPen(Qt.black), QBrush(self._board[x][y]))

    def checkBound(self, index):
        return index >= 0 and index < self._cellsCount

    def getNextGeneration(self, x, y):
        aliveNeighbors = 0
        for xdelta in [-1, 0, 1]:
            for ydelta in [-1, 0, 1]:
                if (xdelta == 0 and ydelta == 0) or not self.checkBound(x + xdelta) or not self.checkBound(y + ydelta):
                    continue
                if self._board[x + xdelta][y + ydelta] == self.CELL_ALIVE:
                    aliveNeighbors += 1

        if self._board[x][y] == self.CELL_ALIVE:
            return self.CELL_ALIVE if aliveNeighbors in ALIVE_CELL_STAY_ALIVE_CONDITION else self.CELL_DEAD
        else:
            return self.CELL_ALIVE if aliveNeighbors in NEW_CELL_BIRTH_CONDITION else self.CELL_DEAD

    def moveToNextGeneration(self):
        newGenerationBoard = []
        for i in range(0, self._cellsCount):
            newGenerationBoard.append([None] * self._cellsCount)
            for j in range(0, self._cellsCount):
                newGenerationBoard[i][j] = self.getNextGeneration(i, j)

        self.setNewBoard(newGenerationBoard)


if __name__ == '__main__':
    application = QApplication(sys.argv)
    mainWindow = QMainWindow()
    mainWindow.setWindowTitle('Life')
    lifeWidget = LifeWidget(LIFE_BOARD_WIDGET_SIZE, LIFE_BOARD_CELL_SIZE)
    mainWindow.setCentralWidget(lifeWidget)
    mainWindow.show()
    sys.exit(application.exec_())
