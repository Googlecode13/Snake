from cmu_112_graphics import *

def appStarted(app):
    app.squareLeft = app.width//2
    app.squareTop = app.height//2
    app.squareSize = 25
    app.dx = 10
    app.dy = 15
    app.isPaused = False
    app.timerDelay = 50 # milliseconds

def keyPressed(app, event):
    if (event.key == "p"):
        app.isPaused = not app.isPaused
    elif (event.key == "s"):
        doStep(app)

def timerFired(app):
    if (not app.isPaused):
        doStep(app)

def doStep(app):
    # Move horizontally
    app.squareLeft += app.dx

    # Check if the square has gone out of bounds, and if so, reverse
    # direction, but also move the square right to the edge (instead of
    # past it). Note: there are other, more sophisticated ways to
    # handle the case where the square extends beyond the edges...
    if app.squareLeft < 0:
        # if so, reverse!
        app.squareLeft = 0
        app.dx = -app.dx
    elif app.squareLeft > app.width - app.squareSize:
        app.squareLeft = app.width - app.squareSize
        app.dx = -app.dx
    
    # Move vertically the same way
    app.squareTop += app.dy
    if app.squareTop < 0:
        # if so, reverse!
        app.squareTop = 0
        app.dy = -app.dy
    elif app.squareTop > app.height - app.squareSize:
        app.squareTop = app.height - app.squareSize
        app.dy = -app.dy

def redrawAll(app, canvas):
    # draw the square
    canvas.create_rectangle(app.squareLeft,
                            app.squareTop,
                            app.squareLeft + app.squareSize,
                            app.squareTop + app.squareSize,
                            fill="yellow")
    # draw the text
    canvas.create_text(app.width/2, 20,
                       text="Pressing 'p' pauses/unpauses timer")
    canvas.create_text(app.width/2, 40,
                       text="Pressing 's' steps the timer once")

runApp(width=400, height=150)