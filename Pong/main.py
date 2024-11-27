import cv2
import mediapipe as mp
import turtle

# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Create screen
sc = turtle.Screen()
sc.title("Pong game")
sc.bgcolor("white")
sc.setup(width=1000, height=600)

# Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("red")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-400, 0)

# Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("green")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400, 0)

# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(40)
hit_ball.shape("circle")
hit_ball.color("blue")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = 5
hit_ball.dy = -5

# Initialize the score
left_player = 0
right_player = 0

# Displays the score
sketch = turtle.Turtle()
sketch.speed(0)
sketch.color("blue")
sketch.penup()
sketch.hideturtle()
sketch.goto(0, 260)
sketch.write("Left_player : 0 Right_player: 0",
             align="center", font=("Courier", 24, "normal"))

# Function to detect hand gesture and move the paddle accordingly
# Function to detect hand gesture and move the paddle accordingly
def detect_hand_gesture(frame):
    results = hands.process(frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extracting x, y coordinates of index finger
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_x = int(index_finger.x * frame.shape[1])
            index_finger_y = int(index_finger.y * frame.shape[0])
            # Flip the y-coordinate
            index_finger_y = frame.shape[0] - index_finger_y
            # Move left paddle
            if index_finger_x < frame.shape[1] // 2:
                y = (index_finger_y / frame.shape[0]) * sc.window_height() - sc.window_height() // 2
                left_pad.sety(y)
            # Move right paddle
            else:
                y = (index_finger_y / frame.shape[0]) * sc.window_height() - sc.window_height() // 2
                right_pad.sety(y)


# Function to close webcam and exit
def close_webcam():
    cap.release()
    cv2.destroyAllWindows()

# Function to update score and reset game
def update_score_and_reset_game():
    global left_player, right_player
    if hit_ball.xcor() > 500:
        left_player += 1
        sketch.clear()
        sketch.write("Left_player : {} Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1
    elif hit_ball.xcor() < -500:
        right_player += 1
        sketch.clear()
        sketch.write("Left_player : {} Right_player: {}".format(
            left_player, right_player), align="center",
            font=("Courier", 24, "normal"))
        hit_ball.goto(0, 0)
        hit_ball.dy *= -1

# Open webcam
cap = cv2.VideoCapture(0)

# Set webcam window size
cv2.namedWindow("Pong Game", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Pong Game", 640, 480)  # Set the size to 640x480 pixels

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for selfie view
    frame = cv2.flip(frame, 1)

    # Detect hand gesture and move paddles
    detect_hand_gesture(frame)

    # Move the ball
    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    # Check for border collision
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1

    # Check for collision with paddles
    if (hit_ball.xcor() > 360 and hit_ball.xcor() < 370) and (hit_ball.ycor() < right_pad.ycor() + 40 and hit_ball.ycor() > right_pad.ycor() - 40):
        hit_ball.setx(360)
        hit_ball.dx *= -1

    if (hit_ball.xcor() < -360 and hit_ball.xcor() > -370) and(hit_ball.ycor() < left_pad.ycor() + 40 and hit_ball.ycor() > left_pad.ycor() - 40):
        hit_ball.setx(-360)
        hit_ball.dx *= -1

    # Update score and reset game if necessary
    update_score_and_reset_game()

    cv2.imshow('Pong Game', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
close_webcam()