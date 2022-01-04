#!/usr/bin/env python3
import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth):
         super(MinimaxPlayer, self).__init__(symbol)
         self.depth=depth
         self.best_moves=[]

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self,board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves)>0:
                
                (move,score) = self.miniMax(board,max,self.depth, self.symbol) 
                # print(move,score)
                # print(game_rules.makeMove(board,move))
                # print('latest game state')
                # print(move)
                # self.best_moves.append([score,move])
                # for s,m in best_moves:
                #     print('best move and best score',game_rules.makeMove(board,m),s,m)
                
                # print('final',s,m,game_rules.makeMove(board,m))
                # sorted(self.best_moves,lambda x : x[0])
                # print(self.best_moves)
                # print('max here',max(self.best_moves)[1])
                
                
                return move
        else:
            return None

    def miniMax(self, board,chance,depth,symbol):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        # print('depth',depth)
        if depth == 0 or len(legalMoves) == 0: 
            return (None,self.h1(board,symbol))  

        if chance==max:  
            legalMoves = game_rules.getLegalMoves(board, symbol)          
            best_score_max=NEG_INF
            best_move_max=legalMoves[0]

            for s in legalMoves: 
                # print('in max for s legal move score',s,best_score)
                new_board_state=game_rules.makeMove(board,s)   
                # print(new_board_state)
                if symbol == 'o':
                    (move,score) = self.miniMax(new_board_state,min,depth-1,'x')
                    # print('score in loop max',score)
                else:
                    (move,score) = self.miniMax(new_board_state,min,depth-1,'o')
                    # print('score in loop max',score)
                
                if score > best_score_max:
                    best_score_max = score
                    best_move_max=s
            # print('best score in max',best_score_max,best_move_max)
            return (best_move_max,best_score_max)
        else:
            legalMoves = game_rules.getLegalMoves(board, symbol)
            best_score_min =POS_INF
            best_move_min=legalMoves[0]
            for s in legalMoves:  
                # print('in min for s legal move score',s,best_score)
                new_board_state=game_rules.makeMove(board, s)    
                # print(new_board_state)
                if symbol == 'o':
                    (move,score) = self.miniMax(new_board_state,max,depth-1,'x')
                else:
                    (move,score) = self.miniMax(new_board_state,max,depth-1,'o')          
                if score < best_score_min:
                    best_score_min = score
                    best_move_min=s
            # print('best score in min',best_score_min,best_move_min)
            return (best_move_min,best_score_min)


# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth=depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        alpha=NEG_INF
        beta=POS_INF
        if len(legalMoves) > 0:           
            (move,score)=self.ab_minimax(board,max,self.depth,self.symbol,alpha, beta)
            return move 

        else: 
            return None

    
    def ab_minimax(self, board,chance,depth,symbol,alpha, beta):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        if depth == 0 or len(legalMoves) == 0: 
            return (None,self.h1(board, self))
        
        if chance==max:            
            best_score_max=NEG_INF
            best_move_max=legalMoves[0]
            for s in legalMoves:  
                new_board_state=game_rules.makeMove(board,s)   
                if symbol == 'o':
                    (move,score) = self.ab_minimax(new_board_state,min,depth-1,'x',alpha, beta)
                    # print('score in loop max',score)
                else:
                    (move,score) = self.ab_minimax(new_board_state,min,depth-1,'o',alpha, beta)           
                
                if score > best_score_max:
                    best_score_max = score
                    best_move_max=s 
                    alpha =best_score_max
                    if beta<=alpha:
                        break
                        
            return (best_move_max,best_score_max)
        else:
            best_score_min =POS_INF
            best_move_min=legalMoves[0]
            for s in legalMoves:  
                new_board_state=game_rules.makeMove(board, s)    
                # print(new_board_state)
                if symbol == 'o':
                    (move,score) = self.ab_minimax(new_board_state,max,depth-1,'x',alpha, beta)
                else:
                    (move,score) = self.ab_minimax(new_board_state,max,depth-1,'o',alpha, beta)        
                if score < best_score_min:
                    best_score_min = score
                    best_move_min=s
                    beta=best_score_min
            # print('best score in min',best_score_min,best_move_min)
                    if beta<=alpha :
                        break 
            return (best_move_min,best_score_min) 

        


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
