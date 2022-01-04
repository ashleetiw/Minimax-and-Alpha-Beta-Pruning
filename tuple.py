#!/usr/bin/env python3.7


l=((0, 2), (0, 0))
for  i in l :
    print(i)


 # (move,score) = self.miniMax(board,max, self.depth, self.symbol) 
        self.miniMax(board,max, self.depth, self.symbol) 
        # return move

    def miniMax(self, board,chance,depth,symbol):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        print('depth',depth)
        if depth == 0 or len(legalMoves) == 0: 
            return (None,self.h1(board,symbol))  

        if chance==max:            
            best_score =NEG_INF
            best_move=legalMoves[0]
        
            for s in legalMoves: 
                # print('in max for s legal move score',s,best_score)
                new_board_state=game_rules.makeMove(board,s)   
                # print(new_board_state)
                if symbol == 'o':
                    (move,score) = self.miniMax(new_board_state,min,depth-1,'x')
                else:
                    (move,score) = self.miniMax(new_board_state,min,depth-1,'o')
                
                if score > best_score:
                    best_score = score
                    best_move=move
            return (best_move,best_score)
        else:
            best_score =POS_INF
            best_move=legalMoves[0]
            for s in legalMoves:  
                # print('in min for s legal move score',s,best_score)
                new_board_state=game_rules.makeMove(board, s)    
                # print(new_board_state)
                if symbol == 'o':
                    (move,score) = self.miniMax(new_board_state,max,depth-1,'x')
                else:
                    (move,score) = self.miniMax(new_board_state,max,depth-1,'o')          
                if score < best_score:
                    best_score = score
                    best_move=move
            return (best_move,best_score)