from consts import *
import arcade

class chessPencil(object):
    def __init__(self):
        pass
    def draw(self,board,teams,textList,turnShow,selectedSpace,possibleSpaces,timer):
        """ draws the given method arguments """
        for lane in board:
            for space in lane:
                space.draw()
        if selectedSpace!=None:
            selectedSpace.draw()
        if possibleSpaces!=None:
            for space in possibleSpaces:
                space.draw()
        for team in teams:
            for piece in team:
                piece.draw()
        for text in textList:
            text.draw()
        turnShow.draw()
        if timer!=None:
            for time in timer:
                time.draw()
