
import arcade
from consts import *


class chess(object):
    def __init__(self):

        #list of white pawns
        self.whitePawns=[]
        #list of white rooks
        self.whiteRooks=[]
        #list of white knights
        self.whiteKnights=[]
        #list of white bishops
        self.whiteBishops=[]
        #list of white kings
        self.whiteKings=[]
        #list of white queens
        self.whiteQueens=[]
        #list of black pawns
        self.blackPawns=[]
        #list of black rooks
        self.blackRooks=[]
        #list of black knights
        self.blackKnights=[]
        #list of black bishops
        self.blackBishops=[]
        #list of black kings
        self.blackKings=[]
        #list of black queens
        self.blackQueens=[]
        lane1=[]
        for x in range(8):
            lane1.append(None)
        lane2=[]
        for x in range(8):
            lane2.append(None)
        lane3=[]
        for x in range(8):
            lane3.append(None)
        lane4=[]
        for x in range(8):
            lane4.append(None)
        lane5=[]
        for x in range(8):
            lane5.append(None)
        lane6=[]
        for x in range(8):
            lane6.append(None)
        lane7=[]
        for x in range(8):
            lane7.append(None)
        lane8=[]
        for x in range(8):
            lane8.append(None)
        board=[]
        board.append(lane1)
        board.append(lane2)
        board.append(lane3)
        board.append(lane4)
        board.append(lane5)
        board.append(lane6)
        board.append(lane7)
        board.append(lane8)
        self.board=board



    def update(self):
        pass


    def createPieces(self):
        """ creates a list of two lists, which are each team. """
        teamLists=[]
        for x in range(2):
            team=self.createTeam(x)
            teamLists.append(team)
        return teamLists

    def createTeam(self,teamNum):
        """ creates each team by calling the methods to create their pawns and
        backline """
        team=[]
        pawns=None
        if teamNum==0:
            team+=self.createWhitePawns()
            team+=self.createWhiteBack()

        else:
            team+=self.createBlackPawns()
            team+=self.createBlackBack()
        return team

    def createWhitePawns(self):
        """ creates the white pawn Sprites """
        pawnList=[]
        code=wpawn
        for x in range(8):
            sprite=arcade.Sprite(code,1.3)
            sprite.center_x=x*80+200
            sprite.center_y=680
            pawnList.append(sprite)
            self.board[6][x]=sprite
            self.whitePawns.append(sprite)

        return pawnList

    def createBlackPawns(self):
        """ creates the black pawn Sprites """
        pawnList=[]
        code=bpawn
        for x in range(8):
            sprite=arcade.Sprite(code,1.3)
            sprite.center_x=x*80+200
            sprite.center_y=280
            pawnList.append(sprite)
            self.board[1][x]=sprite
            self.blackPawns.append(sprite)
        return pawnList

    def createWhiteBack(self):
        """ creates the white backline Sprites """
        backline=[]
        sprite=arcade.Sprite(wrook,1.3)
        self.centerSprite(sprite,200,760)
        backline+=[sprite]
        self.whiteRooks.append(sprite)
        self.board[7][0]=sprite
        sprite=arcade.Sprite(wknight,1.3)
        self.centerSprite(sprite,280,760)
        backline+=[sprite]
        self.whiteKnights.append(sprite)
        self.board[7][1]=sprite
        sprite=arcade.Sprite(wbishop,1.3)
        self.centerSprite(sprite,360,760)
        backline+=[sprite]
        self.whiteBishops.append(sprite)
        self.board[7][2]=sprite
        sprite=arcade.Sprite(wqueen,1.3)
        self.centerSprite(sprite,440,760)
        backline+=[sprite]
        self.whiteQueens.append(sprite)
        self.board[7][3]=sprite
        sprite=arcade.Sprite(wking,1.3)
        self.centerSprite(sprite,520,760)
        backline+=[sprite]
        self.whiteKings.append(sprite)
        self.board[7][4]=sprite
        sprite=arcade.Sprite(wbishop,1.3)
        self.centerSprite(sprite,600,760)
        backline+=[sprite]
        self.whiteBishops.append(sprite)
        self.board[7][5]=sprite
        sprite=arcade.Sprite(wknight,1.3)
        self.centerSprite(sprite,680,760)
        backline+=[sprite]
        self.whiteKnights.append(sprite)
        self.board[7][6]=sprite
        sprite=arcade.Sprite(wrook,1.3)
        self.centerSprite(sprite,760,760)
        backline+=[sprite]
        self.whiteRooks.append(sprite)
        self.board[7][7]=sprite
        return backline

    def createBlackBack(self):
        """ creates the black backline Sprites """
        backline=[]
        sprite=arcade.Sprite(brook,1.3)
        self.centerSprite(sprite,200,200)
        backline+=[sprite]
        self.blackRooks.append(sprite)
        self.board[0][0]=sprite
        sprite=arcade.Sprite(bknight,1.3)
        self.centerSprite(sprite,280,200)
        backline+=[sprite]
        self.blackKnights.append(sprite)
        self.board[0][1]=sprite
        sprite=arcade.Sprite(bbishop,1.3)
        self.centerSprite(sprite,360,200)
        backline+=[sprite]
        self.blackBishops.append(sprite)
        self.board[0][2]=sprite
        sprite=arcade.Sprite(bqueen,1.3)
        self.centerSprite(sprite,440,200)
        backline+=[sprite]
        self.blackQueens.append(sprite)
        self.board[0][3]=sprite
        sprite=arcade.Sprite(bking,1.3)
        self.centerSprite(sprite,520,200)
        backline+=[sprite]
        self.blackKings.append(sprite)
        self.board[0][4]=sprite
        sprite=arcade.Sprite(bbishop,1.3)
        self.centerSprite(sprite,600,200)
        backline+=[sprite]
        self.blackBishops.append(sprite)
        self.board[0][5]=sprite
        sprite=arcade.Sprite(bknight,1.3)
        self.centerSprite(sprite,680,200)
        backline+=[sprite]
        self.blackKnights.append(sprite)
        self.board[0][6]=sprite
        sprite=arcade.Sprite(brook,1.3)
        self.centerSprite(sprite,760,200)
        backline+=[sprite]
        self.blackRooks.append(sprite)
        self.board[0][7]=sprite
        return backline

    def centerSprite(self,sprite,x,y):
        """ centers a sprite at a given x and y position """
        sprite.center_x=x
        sprite.center_y=y




    def createBoard(self):
        """ creates each lane to be filled with the space Sprites """
        boardList=[]
        start=0
        for x in range(8):
            lane=self.createLane(x,start%2)
            start+=1
            boardList+=[lane]
        return boardList


    def createLane(self,row,colorStart):
        """ creates a list of Sprite objects that are the spaces of alternating
        color """
        start=0
        if colorStart==SPACE_BEIGE:
            start=1

        laneList=[]
        for x in range(8):
            sprite=self.createSpace(x*80+200,row*80+200,start%2)
            start+=1
            laneList.append(sprite)
        return laneList

    def createSpace(self,x,y,color):
        """ creates a singluar space of a given color """
        code=GREEN_PNG
        scale=GREEN_SCALE
        if color==SPACE_BEIGE:
            code=BEIGE_PNG
            scale=BEIGE_SCALE
        sprite=arcade.Sprite(code,scale)
        sprite.center_x=x
        sprite.center_y=y
        return sprite


    def createText(self):
        """ creates the letters and numbers that line the top and left of the
        board """
        textList=[]
        text=arcade.draw_text("A",195,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("B",275,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("C",355,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("D",435,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("E",515,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("F",595,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("G",675,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("H",755,120,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("1",120,195,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("2",120,275,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("3",120,355,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("4",120,435,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("5",120,515,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("6",120,595,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("7",120,675,arcade.color.BLACK,14)
        textList+=[text]
        text=arcade.draw_text("8",120,755,arcade.color.BLACK,14)
        textList+=[text]
        return textList

    def movePiece(self,piece,row2,column2):
        """ moves a given Sprite object to a given row and column """
        piece.center_y=row2*80+200
        piece.center_x=column2*80+200
