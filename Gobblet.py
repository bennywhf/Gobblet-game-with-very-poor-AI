import pygame
from pygame.locals import *
from copy import deepcopy
from time import sleep
from threading import Thread

            
class COMP:
    def __init__(self, player):
        self.player = player
        self.aponent = str((int(player)+1)%2) # if '1' then '0', else '1'
        self.stack = []

    def _min(self,board,rstack,bstack,level):

        if level == 0:
            return board.score(self.player)
        
        if board.game(self.player):
            return(-1000)
        if board.game(self.aponent):
            return(1000)

        pmoves = []
        #stacks first.
        for i in range(3):
            for j in range(4):
                for k in range(4):
                    if(board.testPlace((j,k),self.aponent,bstack[i])):
                        #add move to pmoves
                        move = [i,j,k] # [stack, row, column]
                        pmoves.append(move)
                       
                        

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for l in range(4):
                        if board.testMove((i,j),(k,l),self.aponent):
                            #add move to pmoves
                            move = [(i,j),(k,l)] #[source,destination]
                            pmoves.append(move)

        score = 0
        for i in pmoves:
            b = deepcopy(board)
            rs = deepcopy(rstack)
            bs = deepcopy(bstack)
            if len(i) == 3:#place
                b.place((i[1],i[2]),self.aponent,bs[i[0]])
                bs[i[0]]-=1
            else:# move
                b.move(i[0],i[1],self.aponent)

            s = self._max(b,rs,bs,level-1)
            if type(s) == int:
                if s <= score:
                    score = (s,deepcopy(i))
            else:
                if s[0] <= score:
                    score = s
        return score


    def _max(self,board,rstack,bstack,level):
        if board.game(self.player):
            return(1000)
        if board.game(self.aponent):
            return(-1000)
        pmoves = []
        #stacks first.
        for i in range(3):
            for j in range(4):
                for k in range(4):
                    if(board.testPlace((j,k),self.player,rstack[i])):
                        #add move to pmoves
                        move = [i,j,k] # [stack, row, column]
                        pmoves.append(move)
                       
                        

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for l in range(4):
                        if board.testMove((i,j),(k,l),self.player):
                            #add move to pmoves
                            move = [(i,j),(k,l)] #[source,destination]
                            pmoves.append(move)
                            

        score = 0
        for i in pmoves:
            b = deepcopy(board)
            rs = deepcopy(rstack)
            bs = deepcopy(bstack)
            if len(i) == 3:#place
                b.place((i[1],i[2]),self.player,rs[i[0]])
                rs[i[0]]-=1
            else:# move
                b.move(i[0],i[1],self.player)
            

            s = self._min(b,rs,bs,level)
            if type(s) == int:
                if s >= score:
                    score = (s,deepcopy(i))
            else:
                if s[0] >= score:
                    score = s
        return score

class Goblet_Board:
    def __init__(self):
        self.board = [
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]],
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]],
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]],
              [[['n'],0],[['n'],0],[['n'],0],[['n'],0]]
              ]

    #as part of my assignment, I had to make a score function that would give AI
    #A good estimate of what move to make next.
    #I did an awful job since I did this over night.
    def score(self,player):
        _score = 0
        if self.game(player):
            return 1000
        if self.game(str((int(player)+1)%2)):
            return -1000

        for i in range(4):
            for j in range(4):
                for x in range(4):
                    if self.getPlayer((i,x)) == player:
                        _score += self.getSize((i,x))
                    elif self.getPlayer((i,x)) == str((int(player)+1)%2):
                        _score -= self.getSize((i,x))
                for x in range(4):
                    if self.getPlayer((i,x)) == player:
                        _score += self.getSize((x,j))
                    elif self.getPlayer((i,x)) == str((int(player)+1)%2):
                        _score -= self.getSize((x,j))
                for x in range(4):
                    if self.getPlayer((x,x)) == player:
                        _score += self.getSize((x,x))
                    elif self.getPlayer((x,x)) == str((int(player)+1)%2):
                        _score -= self.getSize((x,x))
                    if self.getPlayer((x,3-x)) == player:
                        _score += self.getSize((x,3-x))
                    elif self.getPlayer((x,3-x)) == str((int(player)+1)%2):
                        _score -= self.getSize((x,3-x))

                
        return _score

    def place(self,loc,player,size):
        ok = True #as long as the move is valid, ok is true.
        if self.getPlayer((loc[0],loc[1])) != 'n':
            ok = False
            n = 0
            for i in range(4): #Check column for 3 cups
                if self.getPlayer((loc[0],i)) == str((int(player)+1) % 2):
                    n+=1
            if n == 3:
                ok = True
            n = 0
            for i in range(4): #Check row for 3 cups
                if self.getPlayer((i,loc[1])) == str((int(player)+1) % 2):
                    n+=1
            if n == 3:
                ok = True

            if (loc[0]==loc[1]):# in diagonal
                n = 0
                for i in range(4):
                    if self.getPlayer((i,i)) == str((int(player)+1) % 2):
                        n+=1
                if n == 3:
                    ok = True

            if (loc[0]+loc[1] == 3):# in diagonal
                n = 0
                for i in range(4):
                    if self.getPlayer((3-i,i)) == str((int(player)+1) % 2):
                        n+=1
                if n == 3:
                    ok = True

        if not(ok):
            raise Exception
        if size <= self.board[loc[0]][loc[1]][1]:
            raise Exception

        if ok:
            self.board[loc[0]][loc[1]].append(size)
            self.board[loc[0]][loc[1]][0].append(player)

        return ok #not neccessary since if ok is false, will raise exception
		  #this was residue from earlier tests

    def testPlace(self,loc,player,size):
        ok = True
        if self.getPlayer((loc[0],loc[1])) != 'n':
            ok = False
            n = 0
            for i in range(4): #Check column for 3 cups
                if self.getPlayer((loc[0],i)) == str((int(player)+1) % 2):
                    n+=1
            if n == 3:
                ok = True
            n = 0
            for i in range(4): #Check column for 3 cups
                if self.getPlayer((i,loc[1])) == str((int(player)+1) % 2):
                    n+=1
            if n == 3:
                ok = True

            if (loc[0]==loc[1]):# in diagonal
                n = 0
                for i in range(4):
                    if self.getPlayer((i,i)) == str((int(player)+1) % 2):
                        n+=1
                if n == 3:
                    ok = True

            if (loc[0]+loc[1] == 3):# in diagonal
                n = 0
                for i in range(4):
                    if self.getPlayer((3-i,i)) == str((int(player)+1) % 2):
                        n+=1
                if n == 3:
                    ok = True
        
        if not(ok):
          return False
        if size <= self.board[loc[0]][loc[1]][1]:
            return False

        return True

    def testMove(self,_from,to,player):
        if self.getPlayer(_from) == player:
            if (self.board[to[0]][to[1]][-1] >= self.board[_from[0]][_from[1]][-1]):
                return False
            else:
                return True
        return False

        
    def getPlayer(self,pos):
        p = self.board[pos[0]][pos[1]][0]
        return p[-1]

    def getSize(self,pos):
        return self.board[pos[0]][pos[1]][-1]

    def move(self,_from,to,player):
        if (self.board[to[0]][to[1]][-1] >= self.board[_from[0]][_from[1]][-1]):
             raise Exception("Placing smaller cup on position")
        self.board[to[0]][to[1]].append(self.board[_from[0]][_from[1]].pop())
        self.board[_from[0]][_from[1]][0].pop()
        self.board[to[0]][to[1]][0].append(player)

    def game(self,player):
        # check row
        n = 0
        for i in range(4):
            for j in range(4):
                if self.getPlayer((j,i)) == player:
                    n+=1
            if n == 4:
                return True
            else:
                n = 0
        #check column
        n = 0
        for i in range(4):
            for j in range(4):
                if self.getPlayer((i,j)) == player:
                    n+=1
            if n == 4:
                return True
            else:
                n = 0
        #check left-right diagonal
        n = 0
        for i in range(4):
            if self.getPlayer((i,i)) == player:
                n+=1
        if n == 4:
            return True
        
        #check right-left diagonal
        n = 0
        for i in range(4):
            if self.getPlayer((i,3-i)) == player:
                n+=1
        if n == 4:
            return True
        
        return False
class App:#Goblet game
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 480
        self.board = Goblet_Board()
        self.Red = [4,4,4]
        self.Black = [4,4,4]
        self.current_Player = 0
        self.center = self.left, self.top = 81+80,60+20
        self.turn = '1'
        self._i,self._j = -1,-1
        self.selected = False
        self.mode = 'pvp' #Player vs Player

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
        if event.type == USEREVENT+2:#Hover over circle on board
            if self.board.getPlayer((event.x,event.y)) == self.turn:
                if not(self.selected):
                    self._i = event.x
                    self._j = event.y
                    
        if event.type == USEREVENT+3: #Hover over black stacks
            if event.player == '0':
                if not(self.selected):
                    self._i = event.x
                    self._j = -10
                    
        if event.type == USEREVENT+4:# Hover over red stacks
            if event.player == '1':
                if not(self.selected):
                    self._i = event.x
                    self._j = -11

        if event.type == pygame.MOUSEBUTTONUP:
            x = event.pos[0]
            y = event.pos[1]
            for i in range(4):
                for j in range(4):
                    if not(self.selected):
                        if (x - (self.left+80*i +40))**2 + (y - (self.top+80*j +40))**2 <= (10*self.board.getSize((i,j)))**2:
                            if self.turn == self.board.getPlayer((i,j)):
                                self.selected = True
                    else:
                        try:
                            if Rect(self.left+80*i,self.top+80*j,80,80).collidepoint(x, y):
                                if self._j == -10:
                                        self.board.place((i,j),self.turn,self.Black[-(self._i + 2)])
                                        self.Black[-(self._i + 2)] -= 1
                                elif self._j == -11:
                                        self.board.place((i,j),self.turn,self.Red[self._i - 4])
                                        self.Red[self._i - 4] -=1
                                else:
                                    self.board.move((self._i,self._j),(i,j),self.turn)
                                self.selected = False
                                if(self.board.game(self.turn)):#############################Games ends upon one player forming a 4 row.
                                   print("Four in a row!")
                                self.turn = str((int(self.turn) + 1) % 2)
                        except Exception:
                            pass


            for i in range(3):
                if self.turn == '0':
                    if(x - (self.left+80*-1 - 20 +40))**2 + (y - (self.top+80*2 +40 + 80*i))**2 <= (10 * self.Black[i])**2:
                        self.selected = True


            for i in range(3):
                if self.turn == '1':
                    if(x - (self.left+80*4 + 20 +40))**2 + (y - (self.top + 120 - 80*i))**2 <= (10 * self.Red[i])**2:
                        self.selected = True

        if event.type == USEREVENT+5:
            if len(event.choice) == 3: #place
                self.board.place((event.choice[1],event.choice[2]),'1',self.Red[event.choice[0]])
                self.Red[event.choice[0]]-=1
            else: #move
                self.board.move(event.choice[0],event.choice[1],'1')

            if(self.board.game(self.turn)):#############################Games ends upon one player forming a 4 row.
                print("Four in a row!")
            self.turn = '0'

        
    def on_loop(self):
        if self.mode == 'pvp':
            x,y = pygame.mouse.get_pos()
            for i in range(4):
                for j in range(4):
                    if (x - (self.left+80*i +40))**2 + (y - (self.top+80*j +40))**2 <= (10*self.board.getSize((i,j)))**2:
                        hover = USEREVENT+2
                        MouseHoverevent = pygame.event.Event(hover, x = i, y = j, player = self.turn)
                        pygame.event.post(MouseHoverevent)

            for i in range(3):
                if(x - (self.left+80*-1 - 20 +40))**2 + (y - (self.top+80*2 +40 + 80*i))**2 <= (10 * self.Black[i])**2:
                        hover = USEREVENT+3
                        MouseHoverevent = pygame.event.Event(hover, x = -2 -i, player = self.turn)
                        pygame.event.post(MouseHoverevent)

            for i in range(3):
                if(x - (self.left+80*4 + 20 +40))**2 + (y - (self.top + 120 - 80*i))**2 <= (10 * self.Red[i])**2:
                        hover = USEREVENT+4
                        MouseHoverevent = pygame.event.Event(hover, x = 4 + i, player = self.turn)
                        pygame.event.post(MouseHoverevent)

            

        if self.mode == 'pvc':
            if self.turn == '0':
                x,y = pygame.mouse.get_pos()
                for i in range(4):
                    for j in range(4):
                        if (x - (self.left+80*i +40))**2 + (y - (self.top+80*j +40))**2 <= (10*self.board.getSize((i,j)))**2:
                            hover = USEREVENT+2
                            MouseHoverevent = pygame.event.Event(hover, x = i, y = j, player = self.turn)
                            pygame.event.post(MouseHoverevent)

                for i in range(3):
                    if(x - (self.left+80*-1 - 20 +40))**2 + (y - (self.top+80*2 +40 + 80*i))**2 <= (10 * self.Black[i])**2:
                            hover = USEREVENT+3
                            MouseHoverevent = pygame.event.Event(hover, x = -2 -i, player = self.turn)
                            pygame.event.post(MouseHoverevent)
            else:
                c = COMP('1')
                pcm = USEREVENT+5
                pcmove = pygame.event.Event(pcm, choice =  c._max(self.board, self.Red, self.Black, 1)[1])
                pygame.event.post(pcmove)



    def on_render(self):
        self._display_surf.fill((0,0,0))
##        if self.turn == '0':
##            font=pygame.font.Font(None,30)
##            scoretext=font.render("Score:"+str(score), 1,(255,255,255))
##            screen.blit(scoretext, (500, 457))
##        else:
##            pass
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self._display_surf,(223+(-10*((i+j)%2)),201 + (21*((i+j)%2)),33 +(59 *((i+j)%2))),Rect(self.left+80*i,self.top+80*j,80,80))
                if self.board.getPlayer((i,j)) != 'n':
                    if (i == self._i and j == self._j):
                        color = (125,125,125)
                        if not(self.selected):
                            self._i = -1
                            self._j = -1
                        
                    else:
                        color = (255 * int(self.board.getPlayer((i,j))),0,0)
                    pygame.draw.circle(self._display_surf,color,(self.left+80*i +40,self.top+80*j +40),10*self.board.getSize((i,j)))



        ### Player stack functionality
        pygame.draw.rect(self._display_surf,(177,137,4),Rect(self.left+80*-1 - 20,self.top+160,80,320))
        pygame.draw.rect(self._display_surf,(177,137,4),Rect(self.left+80*4 + 20,self.top - 80,80,320 - 80))

        for i in range(3):
            if (-2 - i) == self._i:
                color = (125,125,125)
            else:
                color = (0,0,0)
            pygame.draw.circle(self._display_surf,color,(self.left+80*-1 - 20 +40,self.top+80*2 +40 + 80*i),10*self.Black[i])
            
        for i in range(3):
            if (4 + i) == self._i:
                color = (125,125,125)
            else:
                color = (255,0,0)
            
            pygame.draw.circle(self._display_surf,color,(self.left+80*4 + 20 +40,self.top + 120 - 80*i),10*self.Red[i])

        if not(self.selected):
            self._i = -1
            self._j = -1
            
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            self.on_render()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
