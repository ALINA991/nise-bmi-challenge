class Player:
    def Player(self, posX, posY):
        self.posX = posX,
        self.posY = posY

    def go_up(self):
        self.posX +=1
    
    def go_down(self):
        self.posX -= 1

    def sideways(self, direction): 
        self.posY += direction 



class Ball:
    def Ball(self, posX, posY):
        self.posX = posX,
        self.posY = posY


