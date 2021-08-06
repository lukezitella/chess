import arcade
import chessGame
import chessDraw
from consts import *



class controller(arcade.Window):
    """ Main application class. """



    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.WHITE)



    def setup(self):
        # Set up your game here
        #instance of the game of chess
        self.chessInstance=chessGame.chess()
        #instance of the drawing methods
        self.chessArt=chessDraw.chessPencil()
        #creates a list of two lists, one for each time, containing the pieces
        self.teams=self.chessInstance.createPieces()
        #creates an eight length list containing eight lists, each one being a
        #lane on the board
        self.boardSpaces=self.chessInstance.createBoard()
        #creates all the Sprite text objects that make up the letters and
        #numbers around the board
        self.boardText=self.chessInstance.createText()
        #stores whose turn it is, TEAM_WHITE or TEAM_BLACK
        self.turn=TEAM_WHITE
        #stores the selected Sprite object on the board
        self.selectedPiece=None
        #stores if white can still castle or not
        self.whiteCastle=True
        #stores if black can still castle or not
        self.blackCastle=True
        #stores an 8x8 matrix of the possible moves of each piece at each space.
        #if the space is empty, it is None. Else, it is a list of length two
        #arrays containing [row,column] of possible spaces to move to
        self.possibleMoves=[]
        #timer Sprites
        self.timer=[]
        #time left for white
        self.whiteTime=TIMESTART
        #time left for black
        self.blackTime=TIMESTART
        #timer for white
        self.whiteTimer=arcade.draw_text("White: 30:00",820,600,arcade.color.BLACK,20)
        #timer for black
        self.blackTimer=arcade.draw_text("Black: 30:00",820,300,arcade.color.BLACK,20)

        #sound for moving a piece
        self.sound=arcade.Sound(THUMP_MP3)

        #list of possible en passant moves
        self.peasant=[]
        #tracks turns since a passant creating move was done
        self.peasantMove=0

        self.timer.append(self.whiteTimer)

        self.timer.append(self.blackTimer)

        for x in range(8):
            list=[]
            for xx in range(8):
                list.append(None)
            self.possibleMoves.append(list)


        self.possibleMoves=self.generatePossibleMoves(self.chessInstance.board)
        self.turnShowWhite=arcade.draw_text("White's Turn",400,900,arcade.color.BLACK,20)
        self.turnShowBlack=arcade.draw_text("Black's Turn",400,900,arcade.color.BLACK,20)
        self.turnShow=self.turnShowWhite
        #stores the Sprite object that appears on the clicked on space to highlight
        self.selectedSpace=None
        # Stores a list of possible space Sprite objects to move to
        self.possibleSpaces=None
        #stores a value that determines if the game is over or not
        self.over=False





    def on_draw(self):
        """ calls the subordinate draw method """
        arcade.start_render()
        # Your drawing code goes here

        self.chessArt.draw(self.boardSpaces,self.teams,self.boardText,
        self.turnShow,self.selectedSpace,self.possibleSpaces,self.timer)


    def update(self, delta_time):
        """ Updates the timer and calls the update method in chess instance """
        self.chessInstance.update()

        if self.turn==TEAM_WHITE and not self.over:
            self.whiteTime+=-delta_time
            time=self.determineTime(self.whiteTime)
            self.whiteTimer=arcade.draw_text("White: "+time,820,630,arcade.color.BLACK,20)
            self.timer[0]=self.whiteTimer
            if self.whiteTime<=0:
                self.over=True
                self.turnShow=arcade.draw_text("Black Wins",400,900,arcade.color.BLACK,20)
        elif self.turn==TEAM_BLACK and not self.over:
            self.blackTime+=-delta_time
            time=self.determineTime(self.blackTime)
            self.blackTimer=arcade.draw_text("Black: "+time,820,300,arcade.color.BLACK,20)
            self.timer[1]=self.blackTimer
            if self.blackTime<=0:
                self.over=True
                self.turnShow=arcade.draw_text("White Wins",400,900,arcade.color.BLACK,20)


    def on_mouse_press(self, x, y, button, modifiers):
        """ When the mouse is clicked, the method determines if a piece should
        be selected, unselected, or moved based on the current class
        attributes and the location clicked. If, after the piece is moved,
        if checkmate is achieved then self.over is set to True, ending the game"""
        board=self.chessInstance.board
        if x>160 and x<800 and y<800 and y>160 and self.over!=True:
            row=(y-160)//80
            column=(x-160)//80
            if self.selectedPiece==None:
                self.selectedPiece=board[row][column]
                if self.selectedPiece!=None:
                    if self.determineTeam(self.selectedPiece)==self.turn:
                        self.selectedPieceRow=row
                        self.selectedPieceColumn=column
                        self.selectedSpace=arcade.Sprite(ORANGE_PNG,.06)
                        self.selectedSpace.center_x=column*80+200
                        self.selectedSpace.center_y=row*80+200
                        possible=self.possibleMoves[row][column]
                        if possible!=None:
                            list=[]
                            for possibleMove in possible:
                                rowNew=possibleMove[0]
                                columnNew=possibleMove[1]
                                sprite=arcade.Sprite(PURPLE_PNG,.05)
                                sprite.center_x=columnNew*80+200
                                sprite.center_y=rowNew*80+200
                                list.append(sprite)
                            self.possibleSpaces=list
                    else:
                        self.selectedPiece=None
            else:
                spaceClicked=board[row][column]
                pieceRow=self.selectedPieceRow
                pieceColumn=self.selectedPieceColumn
                if self.possibleMoves[pieceRow][pieceColumn]!=None:
                    spot=self.possibleMoves[pieceRow][pieceColumn]
                    bool=False
                    for spots in spot:
                        if spots[0]==row and spots[1]==column:
                            bool=True

                    if bool:
                        if spaceClicked!=None:
                            if self.turn==TEAM_BLACK:
                                self.teams[0].remove(spaceClicked)
                            else:
                                self.teams[1].remove(spaceClicked)
                        self.chessInstance.movePiece(self.selectedPiece,row,column)
                        self.sound.play()

                        if self.selectedPiece in self.chessInstance.whiteRooks:
                            if self.selectedPieceRow==7 and self.selectedPieceColumn==7:
                                self.whiteCastle=False
                        if self.selectedPiece in self.chessInstance.whiteKings:
                            if self.whiteCastle:
                                if row==7 and column==6:
                                    rook=self.chessInstance.board[7][7]
                                    self.chessInstance.movePiece(rook,7,5)
                                    self.chessInstance.board[7][7]=None
                                    self.chessInstance.board[7][5]=rook
                                    self.whiteCastle=False
                                else:
                                    whiteCastle=False


                        if self.selectedPiece in self.chessInstance.blackRooks:
                            if self.selectedPieceRow==0 and self.selectedPieceColumn==7:
                                self.blackCastle=False
                        if self.selectedPiece in self.chessInstance.blackKings:
                            if self.blackCastle:
                                if row==0 and column==6:
                                    rook=self.chessInstance.board[0][7]
                                    self.chessInstance.movePiece(rook,0,5)
                                    self.chessInstance.board[0][7]=None
                                    self.chessInstance.board[0][5]=rook
                                    self.blackCastle=False
                                else:
                                    self.blackCastle=False


                        self.chessInstance.board[self.selectedPieceRow][self.selectedPieceColumn]=None
                        self.chessInstance.board[row][column]=self.selectedPiece
                        if self.peasantMove==1 and self.determineType(self.selectedPiece,self.chessInstance.board)==PAWN_WHITE:
                            if self.peasant[0]==row+1 and self.peasant[1]==column:
                                self.teams[1].remove(self.chessInstance.board[row+1][column])
                                self.chessInstance.board[row+1][column]=None

                        if self.peasantMove==1 and self.determineType(self.selectedPiece,self.chessInstance.board)==PAWN_BLACK:
                            if self.peasant[0]==row-1 and self.peasant[1]==column:
                                self.teams[0].remove(self.chessInstance.board[row-1][column])
                                self.chessInstance.board[row-1][column]=None

                        if self.selectedPiece in self.chessInstance.whitePawns:
                            if row==4 and self.selectedPieceRow==6:

                                self.peasant=[row,column]
                                self.peasantMove=2

                            if row==0:
                                sprite=arcade.Sprite(wqueen,1.3)
                                sprite.center_y=row*80+200
                                sprite.center_x=column*80+200
                                self.chessInstance.board[row][column]=sprite
                                self.teams[0].remove(self.selectedPiece)
                                self.chessInstance.whitePawns.remove(self.selectedPiece)
                                self.chessInstance.whiteQueens.append(sprite)
                                self.teams[0].append(sprite)
                        if self.selectedPiece in self.chessInstance.blackPawns:
                            if row==3 and self.selectedPieceRow==1:

                                self.peasant=[row,column]
                                self.peasantMove=2

                            if row==7:
                                sprite=arcade.Sprite(bqueen,1.3)
                                sprite.center_y=row*80+200
                                sprite.center_x=column*80+200
                                self.chessInstance.board[row][column]=sprite
                                self.teams[1].remove(self.selectedPiece)
                                self.chessInstance.blackPawns.remove(self.selectedPiece)
                                self.chessInstance.blackQueens.append(sprite)
                                self.teams[1].append(sprite)
                        self.selectedPiece=None
                        self.selectedPieceRow=None
                        self.selectedPieceColumn=None
                        self.possibleSpaces=None
                        self.selectedSpace=None
                        self.switchTurn()

                        if self.peasantMove!=0:
                            self.peasantMove+=-1
                            if self.peasantMove==0:
                                self.peasant=[]

                        if self.turn==TEAM_WHITE:
                            self.turnShow=self.turnShowWhite
                        else:
                            self.turnShow=self.turnShowBlack
                        self.possibleMoves=self.generatePossibleMoves(self.chessInstance.board)
                        a=self.seeIfCheckmate(self.possibleMoves,self.chessInstance.board)

                        if a[0]:
                            self.over=True
                            if a[1]==TEAM_WHITE:
                                if self.isCheck(board,TEAM_WHITE,self.possibleMoves)==False:
                                    self.turnShow=arcade.draw_text("Stalemate",400,900,arcade.color.BLACK,20)
                                else:
                                    self.turnShow=arcade.draw_text("White Wins",400,900,arcade.color.BLACK,20)
                            if a[1]==TEAM_BLACK:
                                if self.isCheck(board,TEAM_BLACK,self.possibleMoves)==False:
                                    self.turnShow=arcade.draw_text("Stalemate",400,900,arcade.color.BLACK,20)
                                else:
                                    self.turnShow=arcade.draw_text("Black Wins",400,900,arcade.color.BLACK,20)

                    else:
                        self.selectedPiece=None
                        self.selectedPieceRow=None
                        self.selectedPieceColumn=None
                        self.selectedSpace=None
                        self.possibleSpaces=None
                else:
                    self.selectedPiece=None
                    self.selectedPieceRow=None
                    self.selectedPieceColumn=None
                    self.selectedSpace=None
                    self.possibleSpaces=None

        else:
            self.selectedPiece=None

    def determineTeam(self,piece):
        """ determines the team of a Sprite object. Either TEAM_BLACK or TEAM_WHITE """
        team=TEAM_BLACK
        if piece in self.teams[0]:
            team=TEAM_WHITE
        return team

    def switchTurn(self):
        """ switches self.turn from TEAM_BLACK to TEAM_WHITE or vice versa """
        self.turn+=1
        self.turn=self.turn%2

    def generatePossibleMoves(self,board):
        """ generates the possible move 8x8 matrix for a given 8x8 board """
        goodlist=[]
        for x in range(8):
            list=[]
            for xx in range(8):
                list.append(None)
            goodlist.append(list)
        moveSet=goodlist
        row=0
        for lane in board:
            column=0
            for pieceSpace in lane:
                if pieceSpace!=None:

                    moves=self.generatePieceMoves(pieceSpace,row,column,board)
                    moveSet[row][column]=moves
                column+=1
            row+=1
        return moveSet

    def generatePieceMoves(self,piece,row,column,board):
        """ calls a move generating function for a given piece depending on its type
        and returns its total move set """
        moves=[]
        type=self.determineType(piece,board)
        thisTeam=self.determineTeam(piece)

        if type==PAWN_WHITE:
            moves+=self.wPawnMoves(piece,row,column,board,thisTeam,False)

        if type==PAWN_BLACK:
            moves+=self.bPawnMoves(piece,row,column,board,thisTeam,False)
        if type==ROOK_BLACK or type==ROOK_WHITE or type==QUEEN_BLACK or type==QUEEN_WHITE:
            moves+=self.rookMoves(piece,row,column,board,thisTeam,False)
        if type==BISHOP_BLACK or type==BISHOP_WHITE or type==QUEEN_BLACK or type==QUEEN_WHITE:
            moves+=self.bishopMoves(piece,row,column,board,thisTeam,False)
        if type==KNIGHT_BLACK or type==KNIGHT_WHITE:
            moves+=self.knightMoves(piece,row,column,board,thisTeam,False)
        if type==KING_BLACK or type==KING_WHITE:
            moves+=self.kingMoves(piece,row,column,board,thisTeam,False)

        if len(moves)==0:
            return None
        return moves


    def generatePossibleCheckMoves(self,board):
        """ generates possible move 8x8 matrix to check for check"""
        goodlist=[]
        for x in range(8):
            list=[]
            for xx in range(8):
                list.append(None)
            goodlist.append(list)
        moveSet=goodlist
        row=0
        for lane in board:
            column=0
            for pieceSpace in lane:
                if pieceSpace!=None:

                    moves=self.generateCheckMoves(pieceSpace,row,column,board)
                    moveSet[row][column]=moves
                column+=1
            row+=1
        return moveSet


    def generateCheckMoves(self,piece,row,column,board):
        """ calls a move generating function for a given piece depending on its type
        and returns its total move set to check for check  """
        moves=[]
        type=self.determineType(piece,board)
        thisTeam=self.determineTeam(piece)

        if type==PAWN_WHITE:
            moves+=self.wPawnMoves(piece,row,column,board,thisTeam,True)

        if type==PAWN_BLACK:
            moves+=self.bPawnMoves(piece,row,column,board,thisTeam,True)
        if type==ROOK_BLACK or type==ROOK_WHITE or type==QUEEN_BLACK or type==QUEEN_WHITE:
            moves+=self.rookMoves(piece,row,column,board,thisTeam,True)
        if type==BISHOP_BLACK or type==BISHOP_WHITE or type==QUEEN_BLACK or type==QUEEN_WHITE:
            moves+=self.bishopMoves(piece,row,column,board,thisTeam,True)
        if type==KNIGHT_BLACK or type==KNIGHT_WHITE:
            moves+=self.knightMoves(piece,row,column,board,thisTeam,True)
        if type==KING_BLACK or type==KING_WHITE:
            moves+=self.kingMoves(piece,row,column,board,thisTeam,True)

        if len(moves)==0:
            return None
        return moves

    def wPawnMoves(self,piece,row,column,board,thisTeam,future):
        """ generates moves for white pawns based on the current board"""
        moves=[]

        if self.peasantMove==1:
            pRow=self.peasant[0]
            pCol=self.peasant[1]
            if row==pRow:
                if column==pCol-1 or column==pRow+1:
                    if future:
                        moves.append([pRow-1,pCol])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[pRow-1][pCol]=piece
                        copy[row][column]=None
                        copy[pRow][pCol]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([pRow-1,pCol])
        if column>0:
            spot=board[row-1][column-1]
            if spot!=None:
                if self.determineTeam(spot)!=thisTeam:
                    if future:
                        moves.append([row-1,column-1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row-1][column-1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row-1,column-1])
        if column<7:

            spot=board[row-1][column+1]
            if spot!=None and self.determineTeam(spot)!=thisTeam:
                if future:
                    moves.append([row-1,column+1])
                else:
                    copy=[]
                    for lane in board:
                        copy.append(lane.copy())
                    copy[row-1][column+1]=piece
                    copy[row][column]=None
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row-1,column+1])

        if board[row-1][column]==None:
            if future:
                moves.append([row-1,column])
            else:
                copy=[]
                for lane in board:
                    copy.append(lane.copy())
                copy[row-1][column]=piece
                copy[row][column]=None
                poss=self.generatePossibleCheckMoves(copy)
                if self.isCheck(copy,thisTeam,poss)==False:
                    moves.append([row-1,column])

        if row==6 and board[row-2][column]==None:
            if future:
                moves.append([row-2,column])
            else:
                copy=[]
                for lane in board:
                    copy.append(lane.copy())
                copy[row-2][column]=piece
                copy[row][column]=None
                poss=self.generatePossibleCheckMoves(copy)
                if self.isCheck(copy,thisTeam,poss)==False:
                    moves.append([row-2,column])

        return moves


    def bPawnMoves(self,piece,row,column,board,thisTeam,future):
        """ generates moves for black pawns based on the current board """
        moves=[]

        if self.peasantMove==1:
            pRow=self.peasant[0]
            pCol=self.peasant[1]
            if row==pRow:
                if column==pCol-1 or column==pRow+1:
                    if future:
                        moves.append([pRow+1,pCol])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[pRow+1][pCol]=piece
                        copy[row][column]=None
                        copy[pRow][pCol]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([pRow+1,pCol])

        if row!=7 and column>0:
            spot=board[row+1][column-1]
            if spot!=None and self.determineTeam(spot)!=thisTeam:
                copy=[]
                for lane in board:
                    copy.append(lane.copy())
                copy[row+1][column-1]=piece
                copy[row][column]=None
                if future:
                    moves.append([row+1,column-1])
                else:
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row+1,column-1])
        if row!=7 and column<7:
            spot=board[row+1][column+1]
            if spot!=None and self.determineTeam(spot)!=thisTeam:

                if future:
                    moves.append([row+1,column+1])
                else:
                    copy=[]
                    for lane in board:
                        copy.append(lane.copy())
                    copy[row+1][column+1]=piece
                    copy[row][column]=None
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row+1,column+1])
        if row!=7 and board[row+1][column]==None:
            if future:
                moves.append([row+1,column])
            else:
                copy=[]
                for lane in board:
                    copy.append(lane.copy())
                copy[row+1][column]=piece
                copy[row][column]=None
                poss=self.generatePossibleCheckMoves(copy)
                if self.isCheck(copy,thisTeam,poss)==False:
                    moves.append([row+1,column])
        if row!=7 and row==1 and board[row+2][column]==None:
            if future:
                moves.append([row+2,column])
            else:
                copy=[]
                for lane in board:
                    copy.append(lane.copy())
                copy[row+2][column]=piece
                copy[row][column]=None
                poss=self.generatePossibleCheckMoves(copy)
                if self.isCheck(copy,thisTeam,poss)==False:
                    moves.append([row+2,column])
        return moves


    def bishopMoves(self,piece,row,column,board,thisTeam,future):
        """ generates moves for bishops based on the current board """
        moves=[]
        if row>0:
            #down left
            if column>0:
                temprow=row-1
                tempcol=column-1
                while(temprow!=-1 and tempcol!=-1):
                    if board[temprow][tempcol]==None:
                        if future:
                            moves.append([temprow,tempcol])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[temprow][tempcol]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([temprow,tempcol])
                        temprow+=-1
                        tempcol+=-1
                    else:
                        if self.determineTeam(board[temprow][tempcol])!=thisTeam:
                            if future:
                                moves.append([temprow,tempcol])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[temprow][tempcol]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([temprow,tempcol])
                        temprow=-1
            #down right
            if column<7:
                temprow=row-1
                tempcol=column+1
                while(temprow!=-1 and tempcol!=8):
                    if board[temprow][tempcol]==None:
                        if future:
                            moves.append([temprow,tempcol])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[temprow][tempcol]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([temprow,tempcol])
                        temprow+=-1
                        tempcol+=1
                    else:
                        if self.determineTeam(board[temprow][tempcol])!=thisTeam:
                            if future:
                                moves.append([temprow,tempcol])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[temprow][tempcol]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([temprow,tempcol])
                        temprow=-1
        if row<7:
            #up left
            if column>0:
                temprow=row+1
                tempcol=column-1
                while(temprow!=8 and tempcol!=-1):
                    if board[temprow][tempcol]==None:
                        if future:
                            moves.append([temprow,tempcol])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[temprow][tempcol]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([temprow,tempcol])
                        temprow+=1
                        tempcol+=-1
                    else:
                        if self.determineTeam(board[temprow][tempcol])!=thisTeam:
                            if future:
                                moves.append([temprow,tempcol])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[temprow][tempcol]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([temprow,tempcol])
                        temprow=8

            #up right
            if column<7:
                temprow=row+1
                tempcol=column+1
                while(temprow!=8 and tempcol!=8):
                    if board[temprow][tempcol]==None:
                        if future:
                            moves.append([temprow,tempcol])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[temprow][tempcol]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([temprow,tempcol])
                        temprow+=1
                        tempcol+=1
                    else:
                        if self.determineTeam(board[temprow][tempcol])!=thisTeam:
                            if future:
                                moves.append([temprow,tempcol])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[temprow][tempcol]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([temprow,tempcol])
                        temprow=8

        return moves
    def knightMoves(self,piece,row,column,board,thisTeam,future):
        """ generates moves for knights based on the current board """
        moves=[]
        if column>0:
            if column>1:
                #two left one up
                if row<7:
                    if board[row+1][column-2]==None:
                        if future:
                            moves.append([row+1,column-2])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row+1][column-2]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row+1,column-2])
                    else:
                        if self.determineTeam(board[row+1][column-2])!=thisTeam:
                            if future:
                                moves.append([row+1,column-2])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[row+1][column-2]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([row+1,column-2])
                #two left one down
                if row>0:
                    if board[row-1][column-2]==None:
                        if future:
                            moves.append([row-1,column-2])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row-1][column-2]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row-1,column-2])
                    else:
                        if self.determineTeam(board[row-1][column-2])!=thisTeam:
                            if future:
                                moves.append([row-1,column-2])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[row-1][column-2]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([row-1,column-2])
            #two up one left
            if row<6:
                if board[row+2][column-1]==None:
                    if future:
                        moves.append([row+2,column-1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row+2][column-1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row+2,column-1])
                else:
                    if self.determineTeam(board[row+2][column-1])!=thisTeam:
                        if future:
                            moves.append([row+2,column-1])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row+2][column-1]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row+2,column-1])

            #two down one left
            if row>1:
                if board[row-2][column-1]==None:
                    if future:
                        moves.append([row-2,column-1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row-2][column-1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row-2,column-1])
                else:
                    if self.determineTeam(board[row-2][column-1])!=thisTeam:
                        if future:
                            moves.append([row-2,column-1])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row-2][column-1]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row-2,column-1])

        if column<7:
            if column<6:
                #two right one up
                if row<7:
                    if board[row+1][column+2]==None:
                        if future:
                            moves.append([row+1,column+2])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row+1][column+2]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row+1,column+2])
                    else:
                        if self.determineTeam(board[row+1][column+2])!=thisTeam:
                            if future:
                                moves.append([row+1,column+2])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[row+1][column+2]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([row+1,column+2])
                #two right one down
                if row>0:
                    if board[row-1][column+2]==None:
                        if future:
                            moves.append([row-1,column+2])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row-1][column+2]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row-1,column+2])
                    else:
                        if self.determineTeam(board[row-1][column+2])!=thisTeam:
                            if future:
                                moves.append([row-1,column+2])
                            else:
                                copy=[]
                                for lane in board:
                                    copy.append(lane.copy())
                                copy[row-1][column+2]=piece
                                copy[row][column]=None
                                poss=self.generatePossibleCheckMoves(copy)
                                if self.isCheck(copy,thisTeam,poss)==False:
                                    moves.append([row-1,column+2])
            #two up one right
            if row<6:
                if board[row+2][column+1]==None:
                    if future:
                        moves.append([row+2,column+1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row+2][column+1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row+2,column+1])
                else:
                    if self.determineTeam(board[row+2][column+1])!=thisTeam:
                        if future:
                            moves.append([row+2,column+1])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row+2][column+1]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row+2,column+1])

            #two down one right
            if row>1:
                if board[row-2][column+1]==None:
                    if future:
                        moves.append([row-2,column+1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row-2][column+1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row-2,column+1])
                else:
                    if self.determineTeam(board[row-2][column+1])!=thisTeam:
                        if future:
                            moves.append([row-2,column+1])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row-2][column+1]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row-2,column+1])

        return moves


    def rookMoves(self,piece,row,column,board,thisTeam,future):
        """ generates moves for rooks based on the current board """
        moves=[]
        #left
        if column>0:
            temp=column-1
            while(temp>=0):
                if board[row][temp]==None:
                    if future:
                        moves.append([row,temp])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row][temp]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row,temp])
                    temp+=-1
                else:
                    if self.determineTeam(board[row][temp])!=thisTeam:
                        if future:
                            moves.append([row,temp])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row][temp]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row,temp])
                    temp=-1
        #left
        if column<7:
            temp=column+1
            while(temp<=7):
                if board[row][temp]==None:
                    if future:
                        moves.append([row,temp])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row][temp]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row,temp])
                    temp+=1
                else:
                    if self.determineTeam(board[row][temp])!=thisTeam:
                        if future:
                            moves.append([row,temp])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[row][temp]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([row,temp])
                    temp=8
        #down
        if row>0:
            temp=row-1
            while(temp>=0):
                if board[temp][column]==None:
                    if future:
                        moves.append([temp,column])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[temp][column]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([temp,column])
                    temp+=-1
                else:
                    if self.determineTeam(board[temp][column])!=thisTeam:
                        if future:
                            moves.append([temp,column])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[temp][column]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([temp,column])
                    temp=-1
        #up
        if row<7:
            temp=row+1
            while(temp<=7):
                if board[temp][column]==None:
                    if future:
                        moves.append([temp,column])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[temp][column]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([temp,column])
                    temp+=1
                else:
                    if self.determineTeam(board[temp][column])!=thisTeam:
                        if future:
                            moves.append([temp,column])
                        else:
                            copy=[]
                            for lane in board:
                                copy.append(lane.copy())
                            copy[temp][column]=piece
                            copy[row][column]=None
                            poss=self.generatePossibleCheckMoves(copy)
                            if self.isCheck(copy,thisTeam,poss)==False:
                                moves.append([temp,column])
                    temp=8
        return moves
    def kingMoves(self,piece,row,column,board,thisTeam,future):
        """ generates moves for kings based on the current board """
        moves=[]

        if thisTeam==TEAM_WHITE and row==7 and column==4 and self.whiteCastle:
            if board[7][5]==None and board[7][6]==None:

                if future:
                    pass
                else:
                    copy=[]
                    for lane in board:
                        copy.append(lane.copy())
                    copy[row][column+2]=piece
                    copy[row][column]=None
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row,column+2])
        if thisTeam==TEAM_BLACK and row==0 and column==4 and self.blackCastle:
            if board[0][5]==None and board[0][6]==None:
                if future:
                    pass
                else:
                    copy=[]
                    for lane in board:
                        copy.append(lane.copy())
                    copy[row][column+2]=piece
                    copy[row][column]=None
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row,column+2])
        if column>0:
            if row<7:
                if board[row+1][column-1]==None or self.determineTeam(board[row+1][column-1])!=thisTeam:
                    if future:
                        moves.append([row+1,column-1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row+1][column-1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row+1,column-1])
            if row>0:
                if board[row-1][column-1]==None or self.determineTeam(board[row-1][column-1])!=thisTeam:
                    if future:
                        moves.append([row-1,column-1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row-1][column-1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row-1,column-1])

            if board[row][column-1]==None or self.determineTeam(board[row][column-1])!=thisTeam:
                if future:
                    moves.append([row,column-1])
                else:
                    copy=[]
                    for lane in board:
                        copy.append(lane.copy())
                    copy[row][column-1]=piece
                    copy[row][column]=None
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row,column-1])

        if column<7:
            if row<7:
                if board[row+1][column+1]==None or self.determineTeam(board[row+1][column+1])!=thisTeam:
                    if future:
                        moves.append([row+1,column+1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row+1][column+1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row+1,column+1])
            if row>0:
                if board[row-1][column+1]==None or self.determineTeam(board[row-1][column+1])!=thisTeam:
                    if future:
                        moves.append([row-1,column+1])
                    else:
                        copy=[]
                        for lane in board:
                            copy.append(lane.copy())
                        copy[row-1][column+1]=piece
                        copy[row][column]=None
                        poss=self.generatePossibleCheckMoves(copy)
                        if self.isCheck(copy,thisTeam,poss)==False:
                            moves.append([row-1,column+1])
            if board[row][column+1]==None or self.determineTeam(board[row][column+1])!=thisTeam:
                moves.append([row,column+1])

        if row<7:
            if board[row+1][column]==None or self.determineTeam(board[row+1][column])!=thisTeam:
                if future:
                    moves.append([row+1,column])
                else:
                    copy=[]
                    for lane in board:
                        copy.append(lane.copy())
                    copy[row+1][column]=piece
                    copy[row][column]=None
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row+1,column])

        if row>0:
            if board[row-1][column]==None or self.determineTeam(board[row-1][column])!=thisTeam:
                if future:
                    moves.append([row-1,column])
                else:
                    copy=[]
                    for lane in board:
                        copy.append(lane.copy())
                    copy[row-1][column]=piece
                    copy[row][column]=None
                    poss=self.generatePossibleCheckMoves(copy)
                    if self.isCheck(copy,thisTeam,poss)==False:
                        moves.append([row-1,column])

        return moves

    def isCheck(self,board,thisTeam,possibleMoves):
        """ checks the given board and possibleMoves matrix to see if the
        king on thisTeam is in check"""
        kingSpace=self.findKing(board,thisTeam)
        for lane in possibleMoves:
            for space in lane:
                if space!=None:
                    if kingSpace in space:
                        return True
        return False

    def findKing(self,board,thisTeam):
        """ finds the king on the board """
        row=0

        for lane in board:
            column=0
            for space in lane:
                if space!=None:
                    if thisTeam==TEAM_WHITE and self.determineType(space,board)==KING_WHITE:
                        return [row,column]
                    if thisTeam==TEAM_BLACK and self.determineType(space,board)==KING_BLACK:
                        return [row,column]
                column+=1
            row+=1


    def seeIfCheckmate(self,possibleMoves,board):
        """ determines if either team is in checkmate """
        whiteLose=True
        blackLose=True
        row=0
        column=0
        while(whiteLose or blackLose):
            if column==8:
                row+=1
                column=0
            if row==8:
                if whiteLose==True:
                    return[1,1]
                else:
                    return [1,0]
            possibleMove=possibleMoves[row][column]
            if possibleMove!=None:
                team=self.determineTeam(board[row][column])
                if team==TEAM_WHITE:
                    whiteLose=False
                else:
                    blackLose=False
            column+=1
        return [0,0]

    def determineType(self,piece,board):
        """ determines the type of the given piece """
        chess=self.chessInstance
        if piece in chess.whitePawns:
            return PAWN_WHITE
        if piece in chess.whiteRooks:
            return ROOK_WHITE
        if piece in chess.whiteBishops:
            return BISHOP_WHITE
        if piece in chess.whiteKnights:
            return KNIGHT_WHITE
        if piece in chess.whiteQueens:
            return QUEEN_WHITE
        if piece in chess.whiteKings:
            return KING_WHITE
        if piece in chess.blackPawns:
            return PAWN_BLACK
        if piece in chess.blackRooks:
            return ROOK_BLACK
        if piece in chess.blackBishops:
            return BISHOP_BLACK
        if piece in chess.blackKnights:
            return KNIGHT_BLACK
        if piece in chess.blackQueens:
            return QUEEN_BLACK
        if piece in chess.blackKings:
            return KING_BLACK

    def determineTime(self,time):
        """ determines the display to be returned when given an int
        number of seconds. for the timer"""
        if time<60:
            rem_sec=int(time)
            if rem_sec<10:
                rem_sec='0'+str(rem_sec)
                display='00:'+rem_sec
            else:
                display='00:'+str(rem_sec)
        elif time>=60:
            minutes=time//60
            if minutes>9:
                rem_sec=int(time-minutes*60)
                if rem_sec<10:
                    rem_sec='0'+str(rem_sec)
                display=str(int(minutes))+":"+str(rem_sec)
            elif minutes<10:
                rem_sec=int(time-minutes*60)
                if rem_sec<10:
                    rem_sec='0'+str(rem_sec)
                display='0'+str(int(minutes))+':'+str(rem_sec)
        return display


def main():
    """ starts the game """
    game = controller(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    """ calls main() if this file is the main file called"""
    main()
