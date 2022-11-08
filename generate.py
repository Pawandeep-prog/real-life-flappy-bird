import numpy as np
import constants
import cv2

class Generate:
    def __init__(self, height, width):
        # pipe: [[(x: position, y: top, y: bottom)]]
        self.pipes = []
        self.height = height
        self.width = width
        self.points = 0

    def create(self):
        rand_y_top = np.random.randint(0, self.height - constants.GAP)
        self.pipes.append(
            [self.width, rand_y_top, rand_y_top+constants.GAP, False]
         )
    
    def draw_pipes(self, frm):
        for i in self.pipes:
            if(i[0] <= 0 ):
                continue
            cv2.rectangle(frm, (i[0], 0), (i[0]+constants.PIPE_WIDTH, i[1]), (0,255, 0), -1)
            cv2.rectangle(frm, (i[0], i[2]), (i[0]+constants.PIPE_WIDTH, self.width), (0,255, 0), -1)
    
    def update(self):
        for i in self.pipes:
            i[0] -= constants.SPEED
            if(i[0] <= 0):
                self.pipes.remove(i)
    
    def check(self, index_pt):
        for i in self.pipes:
            if (index_pt[0] >= i[0] and index_pt[0] <= i[0]+constants.PIPE_WIDTH):
                if ((index_pt[1] <= i[1]) or (index_pt[1] >= i[2])):
                    return True
                else:
                    if not(i[3]):
                        i[3] = True
                        self.points += 1
                        if(self.points % 10 == 0):
                            constants.SPEED += 4
                            constants.GEN_TIME -= 0.2
                    return False
        return False
