from os import system
import math, random
class tictac:
    def __init__(self):
        self.boxes=[" "]*9
    def available(self):
        return [bx for bx in range(len(self.boxes)) if self.boxes[bx]==" "]
    def thesame(self,squares,player):
        same=True
        for i in squares:
            if i!=player:
                same=False
        return same
    def winner(self,position,letter):
        row_col=position//3
        row = self.boxes[row_col*3:row_col*3+3]
        row_col=position%3
        column = self.boxes[row_col:row_col+7:3]
        diagonall=self.boxes[0:9:4]
        diagonalr=self.boxes[2:7:2]
        if self.thesame(row,letter) or self.thesame(column,letter) or self.thesame(diagonall,letter) or self.thesame(diagonalr,letter):
            return True
        else:
            return False
    def display(self):
        system("cls")
        print("Tic Tac Toe:")
        for i in range(3):
            print(" | ".join([self.boxes[ii] if self.boxes[ii]!=" " else str(ii) for ii in range(i*3,i*3+3)]))
    def put(self,position,letter):
        self.boxes[position]=letter
    def undo(self,position):
        self.boxes[position]=" "
class human:
    def __init__(self,let):
        self.letter=let
    def getMove(self,state):
        while True:
            pos = int(input("Enter the position to put O: "))
            if pos in state.available() :
                break
            else:
                print("Position not available try again")     
        return pos   
class bot:
    def __init__(self,let):
        self.letter=let
        self.opponent= "O" if let=="X" else "X"
    def minimax(self,state,turn):
        max={"position":None,"score":-math.inf}
        min={"position":None,"score":math.inf}
        player=self.letter if turn == 1 else self.opponent
        for i in state.available():
            state.put(i,player)
            # print(i,turn,end=" ")
            if state.winner(i,player):
                state.undo(i)
                return {"position":i,"score":len(state.available())} if turn==1 else {"position":i,"score":-1*len(state.available())}
            case=self.minimax(state,0 if turn==1 else 1)
            # print("case score:",case["score"])
            if case["score"]==math.inf or case["score"]==-math.inf:
                
                case["score"]= 0 
            case["position"]=i
            # print(case, turn)
            if turn==1 and max["score"] < case["score"]:
                max=case
            elif turn==0 and min["score"] > case["score"]:
                min=case
            state.undo(i)
        return max if turn==1 else min
    def getMove(self,game):
        return random.choice(game.available()) if len(game.available())==9 else self.minimax(game,1)["position"]
class randbot:
    def __init__(self,let):
        self.letter=let
    def getMove(self,state):
        return random.choice(state.available())
class playgame():
    def __init__(self):
        gameboard=tictac()
        while True:
            h=human("O")
            r=bot("X")
            
            gameboard.display()
            pos=r.getMove(gameboard)
            gameboard.put(pos,r.letter)
            if gameboard.winner(pos,r.letter):
                gameboard.display()
                print(r.letter,"is the Winner")
                break
            if gameboard.available()==[]:
                gameboard.display()
                print("Draw")
                break
            gameboard.display()
            pos=h.getMove(gameboard)
            gameboard.put(pos,h.letter)
            if gameboard.winner(pos,h.letter):
                gameboard.display()
                print(h.letter,"is the winner")
                break
            
playgame()

