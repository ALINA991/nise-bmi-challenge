import numpy as np


class Vibrate:
    def __init__(self):
        self.player_pos = np.empty(2)
        self.ball_pos = np.empty(2)
        self.strength = 5 # This is the minimum strength

    def auomatic_mode(self, move_suggestion):
        '''Auto mode take in the prefered commmand from the algorithm and split the '''
        # message = np.zeros([6,4])
        if move_suggestion == 1:
            return self.up_message()
        if move_suggestion == 2: 
            return self.down_message()
        if move_suggestion == 3:
            return self.left_message()
        if move_suggestion == 4: 
            return self.right_message()
        if move_suggestion == 0: 
            return self.kick_message()
        if move_suggestion == 9: 
            return self.pull_message()


    def up_message(self):
        return np.asarray([self.strength,0,0,0])

    def down_message(self):
        return np.asarray([0,self.strength,0,0])

    def left_message(self):
        return np.asarray([0,0,self.strength,0])

    def right_message(self):
        return np.asarray([0,0,0,self.strength])

    def kick_message(self):
        return np.message([int(self.strength/3), int(self.strength/2),int(self.strength/3), 0])    

    def pull_message(self):
        return np.message([0,int(self.strength/3),int(self.strength/3), int(self.strength/3)])    

    def clockwise_message(self):
        ''' Return message of of 5x4
            Clockwise spin twice
        '''
        message_array = np.asarray([[7,0,2,0],
                                [4,0,0,7],
                                [2,7,0,4],
                                [0,4,7,2],
                                [0,2,4,0],])
        return message_array.flatten()

    def anticlockwise_message(self):
        ''' Return message of of 5x4
            Clockwise spin twice
        '''
        message_array = np.asarray([[7,0,2,0],
                                [4,0,0,7],
                                [2,7,0,4],
                                [0,4,7,2],
                                [0,2,4,0],])
        return message_array.flatten()

        
    def ramp_up_down_message(self):
        ''' Ramp everything up then down
        '''
        message_array = np.asarray([[0,0,0,0],
                                    [3,3,3,3],
                                    [7,7,7,7],
                                    [3,3,3,3],
                                    [0,0,0,0],])
        return message_array.flatten()       


    def run_manual_perception(self, player_pos, ball_pos):
        ''' GIVE PLAYER THEIR POSITION WRT TO THE BALL 
        OUTPUT: a flatten array of 4 x 6 that can be passed to the ESP 
            for vibration output
        '''
        self.player_pos = np.asarray(player_pos)
        self.ball_pos = np.asarray(ball_pos)
        West , North = self._distance_to_ball(self.player_pos, self.ball_pos)
        message = self.create_discrete_message_block(West, North)
        return message

#%%
    def create_discrete_message_block(self, West, North):
        ''' Put the distance into a message to pass it on

        The message will have the following form: 
        [Vibrate, Off, Vibrate, Off, Off, Off].T
        Between each of those is delay, which regulate 
        by information transfer rate. 

        The motor array will be such ( N, -N, W, -W)    

        Return: message of shape (6,4). (Message Length, Vibrator)
        '''
        message = np.zeros([6,4])
        
        ## Iterrate down 
        for i in [0,2]:
            if North > 0: 
                message[i,0] = self._adapted_strength(North)
                North -= 1  # Itterate toward 0
            if North < 0: 
                message[i,1] = self._adapted_strength(North)
                North += 1 
            if West > 0: 
                message[i,2] = self._adapted_strength(West)
                West -= 1 
            if West < 0: 
                message[i,3] = self._adapted_strength(West)
                West += 1 

        return message.flatten()

#%%
    def _adapted_strength(self,current_pos): 
        '''Set minimum limit strength to give'''
        if abs(current_pos) >= self.strength: 
            return abs(current_pos)
        else: return self.strength

    def _distance_to_ball(self, player_pos, ball_pos):
        '''Calculate the distance from the ball 
            [ 0  1] Behind the ball 
            [ 0 -1] Front of ball
            [-1  0] Left of ball 
            [ 1  0] Right of ball 
            
        Return: [distance x , distance y]
        '''
        return np.asarray(player_pos) - np.asarray(ball_pos)

    def _distance_to_goal(self, player_pos):
        player_x = player_pos[0]
        player_y = player_pos[1]

        # Either goal left or right is 0 then we're in the center
        goal_left = player_x - 4
        goal_right = player_x - 5   

        goal_center = min([goal_left,goal_right],key=abs)

        goal_forward = player_y

        return goal_forward, goal_center