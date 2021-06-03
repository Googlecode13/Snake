import cs112_s20_unit6_linter
import math, copy, random

from cmu_112_graphics import *

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)



class Game(Mode):
    def appStarted(app):
        app.margin = 20
        app.cols = 12
        app.rows = 12
        app.gridWidth = app.width - app.margin*2
        app.gridHeight = app.height - app.margin*2
        app.cellWidth = app.gridWidth / app.cols
        app.cellHeight = app.gridHeight / app.rows
        app.snake = [(5,5),(6,5),(7,5)]
        app.head = app.snake[0]
        app.direction = (-1,0)
        app.lastMove = "Up"
        app.appleX = 3  
        app.appleY = 5
        app.timerDelay = 100
        app.app.score = 0
        
        
        


    

    def isAlive(app):

        for x in range(1,len(app.snake)):
            if app.head == app.snake[x]:
                return False


        if ((app.head[0] >= app.rows) or (app.head[1] < 0) or (app.head[1] >= app.cols) or (app.head[0] < 0)):
            return False

        return True
            

    

    def timerFired(app):
        app.MoveSnake()
        app.isAppleEaten()

    def isAppleEaten(app):
        if (app.head[0] == app.appleX) and (app.head[1] == app.appleY):
            app.app.score += 1
            app.snake.append((app.appleX,app.appleY))
            app.placeApple()

    def placeApple(app):

        (app.appleX,app.appleY)=(random.randint(0,9), 
                                random.randint(0,9))
        
        for x in app.snake:
            if x == (app.appleX, app.appleY):
                app.placeApple()
                
        return (app.appleX, app.appleY)
        
        

    def MoveSnake(app):
        newCoord = (app.head[0] + app.direction[0], app.head[1] + app.direction[1])
        app.snake.insert(0,newCoord)
        app.snake.pop()        
        app.head = app.snake[0]
        if app.isAlive() == False:
            app.app.setActiveMode(GameOver())

    def keyPressed(app, event):
        if (event.key == "Up")and(app.isAlive() == True)and(app.lastMove != "Down"):
            app.direction = (-1,0)
            app.lastMove = "Up"
        if (event.key=="Left")and(app.isAlive() == True)and(app.lastMove != "Right"):
            app.direction = (0,-1)
            app.lastMove = "Left"
        if (event.key == "Right")and(app.isAlive() ==True)and(app.lastMove != "Left"):
            app.direction = (0,1)
            app.lastMove = "Right"
        if (event.key == "Down") and (app.isAlive() == True)and(app.lastMove != "Up"):
            app.direction = (1,0)
            app.lastMove = "Down"
        
        

    def getBounds(app, row, col):
        x0 = app.margin + app.cellWidth * col
        x1 = x0 + app.cellWidth
        y0 = app.margin + app.cellHeight * row
        y1 = y0 + app.cellHeight
        return (x0, x1, y0, y1)
    
    def redrawAll(app, canvas):
        for row in range(app.rows):
            for col in range(app.cols):
                coordinates = app.getBounds(row, col)
                if (row + col) % 2 == 0:
                    canvas.create_rectangle(coordinates[0],coordinates[2],coordinates[1],coordinates[3], fill = 'Green', width = 0)
                elif (row + col) % 2 == 1:
                    canvas.create_rectangle(coordinates[0],coordinates[2],coordinates[1],coordinates[3], fill = 'Light Green', width = 0)


        for coord in app.snake:
            coordinates = app.getBounds(coord[0], coord[1])
            canvas.create_oval(coordinates[0],coordinates[2],coordinates[1],coordinates[3], fill = 'Black')

        headCoord = app.getBounds(app.head[0], app.head[1])
        canvas.create_oval(headCoord[0],headCoord[2],headCoord[1],headCoord[3], fill = 'Green')

        applecoord = app.getBounds(app.appleX,app.appleY)      
        
        canvas.create_oval(applecoord[0],applecoord[2],applecoord[1],applecoord[3], fill = 'Red')
        
        canvas.create_text(app.width/2, 10, text = 
            f'Your Score is {app.app.score}', font = "Arial 15")
    
class GameOver(Mode):
    def appStarted(app):
        app.highscore()
        app.app.CurrentHighscore = readFile(app.app.file)

    def keyPressed(app, event):
        if (event.key == "a"):
            app.app.setActiveMode(Game())

    def highscore(app):
        if app.app.score > int(app.app.CurrentHighscore):
            writeFile(app.app.file, str(app.app.score))

    def redrawAll(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height, fill = 'Light Blue')
        canvas.create_text(app.width/2, app.height/4, text = 
            "Game over", font = "Arial 30")

        canvas.create_text(app.width/2, 2*app.height/4, 
            text = f'Your Score was {app.app.score}', font = "Arial 30")

        canvas.create_text(app.width/2, app.height, text = "A to restart",
            font = "Arial 30")

        canvas.create_text(app.width/2, 3*app.height/4, text = f"Highscore: {app.app.CurrentHighscore}")

class Start(Mode):
    def mousePressed(app, event):
        app.app.setActiveMode(Game())
    def redrawAll(app, canvas):
        canvas.create_rectangle(0,0,app.width,app.height, fill = "Lime")
        canvas.create_text(app.width/2, app.height/3, text = "Press anywhere to start")
        canvas.create_text(app.width/2, 2*app.height/3, text = f"Current Highscore: {app.app.CurrentHighscore}")

class ModalApp(ModalApp):
    def appStarted(app):
        app.file = "C:/Users/eklav/Desktop/Coding/Python/SnakeGame/highscore.txt"
        app.game = Game()
        app.gameOver = GameOver()
        app.start = Start()
        app.CurrentHighscore = readFile(app.file)
        app.score = 0
        app.setActiveMode(app.start)
        

app = ModalApp(width = 600, height = 600)