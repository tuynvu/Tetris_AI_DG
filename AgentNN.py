import os
from keras.models import Sequential
from keras.layers import Dense, Layer, Flatten
from keras.optimizers import Adam
from collections import deque
import numpy as np
from field import Field
from setting import *

class AgentNN(object):
    def __init__(self, input_shape, optimizer=Adam, loss="mse",
                 learning_rate=0.1, activation=["relu", "relu", "linear"], dimenson=[64, 64]):
        self.input_shape = input_shape
        self.optimizer = optimizer
        self.loss = loss
        self.learning_rate = learning_rate
        self.activation = activation
        self.dimenson = dimenson

        self.model = self.createModel()

    def createModel(self):

        model = Sequential()
        model.add(Flatten(input_shape=self.input_shape))
        model.add(Dense(units=self.dimenson[0], activation=self.activation[0]))
        model.add(Dense(units=self.dimenson[1], activation=self.activation[1]))
        model.add(Dense(units=1, activation=self.activation[2]))

        model.compile(loss=self.loss, optimizer=self.optimizer(learning_rate=self.learning_rate, name="Adam"))
        print(model.summary())
        return model

    def update_weight(self, weight):
        """
        :param weight: list[np.array()]
        :return: None
        """
        self.model.set_weights(weight)

    def save_model(self):
        ROOT = os.path.abspath(os.path.dirname(__file__))
        self.model.save("model.h5")

    def get_predict(self, data):
        """
        :param data: input: list have dim (1, 4)
        :return: predict int
        """
        return self.model.predict(np.array(data).reshape(1, 4))[0]

    def get_best(self, piece, field):
        """
        :param self: AgentNN
        :param piece: list[list[]]
        :param offsetX: int
        :param field: grid
        :return: int, int
        """
        rotate_nb = {4: 4, 8: 2, 12: 2, 16: 4, 20: 4, 24: 2, 28: 1}
        offetX = None
        rotate_rt = None
        score_max =None
        for rotate in range(rotate_nb[np.sum(piece)]):
            for offset in range(field.width):
                result = field.projectPieceDown(piece, offset, 1)
                if result is not None:
                    heuristics = field.heuristics()
                    score = self.get_predict(heuristics)
                    if score_max is None or score > score_max:
                        score_max = score
                        offetX = offset
                        rotate_rt = rotate

        return offetX, rotate_rt

    def choose(self, grid, piece, offsetX, parent):
        field =  Field(len(piece[0]), len(piece))
        field.updateField(grid)

        offset, rotation = self.get_best(piece, field)

        moves = []
        print(offset)
        offset = offset - offsetX
        for _ in range(0, rotation):
            moves.append("UP")
        for _ in range(0, abs(offset)):
            if offset > 0:
                moves.append("RIGHT")
            else:
                moves.append("LEFT")
        # moves.append('RETURN')
        parent.executes_moves(moves)