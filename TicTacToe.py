from os import system, name
import math, random, colorama
colorama.init()
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
        if name == 'nt':
            _ = system('cls')
  
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')
        board="""
         1 | 2 | 3
        ---+---+---
         4 | 5 | 6
        ---+---+---
         7 | 8 | 9 
         """
        print("Tic Tac Toe:")
        for i in range(len(self.boxes)):
            if self.boxes[i]=="X":
                board=board.replace(" "+str(i+1)," "+colorama.Fore.CYAN+str(self.boxes[i])+colorama.Fore.RESET)
            elif self.boxes[i]=="O":
                board=board.replace(" "+str(i+1)," "+colorama.Fore.RED+str(self.boxes[i])+colorama.Fore.RESET)
        board=board.replace("-",colorama.Fore.WHITE+"-"+colorama.Fore.RESET)
        board=board.replace("|",colorama.Fore.WHITE+"|"+colorama.Fore.RESET)
        board=board.replace("+",colorama.Fore.WHITE+"+"+colorama.Fore.RESET)
        print(board)
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
            if pos-1 in state.available() :
                break
            else:
                print("Position not available try again")     
        return pos-1   
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
        self.p1=[]
        self.p2=[]
        self.gameboard=tictac()
        self.choosing()
        self.firstplayer=1
        self.scores={self.p1[0]:0,self.p2[0]:0}
        self.matches=0
        self.play()
        self.scoreboard()
    def choosing(self):
        print(
"""      Tic-Tac-Toe
Choose the mode you want to play:
1. Human vs Smart Bot
2. Human vs Random bot
3. Human vs Human""")
        while True:
            choice=int(input())
            if choice==1:
                self.p1=["human",human("O")]
                self.p2=["Smart bot",bot("X")]
                break
            elif choice==2:
                self.p1=["human",human("O")]
                self.p2=["Random bot",randbot("X")]
                break
            elif choice==3:
                self.p1=["human 1",human("O")]
                self.p2=["human 2",human("X")]
                break
            else:
                print("Wrong choice, try choosing again")
    def checkdraw(self):
        if self.gameboard.available()==[]:
            self.gameboard.display()
            print("Draw")
            return True
        return False
    def anywin(self,pos,plr):
        if self.gameboard.winner(pos,plr[1].letter):
            self.gameboard.display()
            print(plr[0],"is the winner")
            self.scores[plr[0]]=self.scores[plr[0]]+1
            return True
    def asktocont(self):
        conti=input("Do you want to continue(Y/N)?")
        if conti.upper() == "Y":
            return True
        else:
            return False
    def scoreboard(self):
        print(colorama.Fore.MAGENTA+"{:^23}".format("SCOREBOARD")+colorama.Fore.RESET)
        k=list(self.scores.keys())
        print("{:^10}   {:^10}".format(k[0],k[1]))
        k=list(self.scores.values())
        print("{:^10}   {:^10}".format(k[0],k[1]))
        for val in self.scores.values():
            print("{:^10}   ".format("{:.2f}".format(val/self.matches*100)+"%"),end="")
    def play(self):
        while True:
            self.gameboard.display()
            if self.firstplayer==1:
                player=self.p1
                self.firstplayer=2
            else:
                player=self.p2
                self.firstplayer=1
            pos=player[1].getMove(self.gameboard)
            self.gameboard.put(pos,player[1].letter)
            if self.anywin(pos,player) or self.checkdraw():
                self.matches+=1
                self.scoreboard()
                if not self.asktocont():
                    break
                self.gameboard=tictac()
        system("cls")
playgame()

