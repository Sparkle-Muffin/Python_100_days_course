def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
while at_goal() == False:
    if wall_in_front():
        turn_left()
    elif front_is_clear() and wall_on_right():
        move()
        for i in range(2):
            if right_is_clear() and at_goal() == False:
                turn_right()
                move()
    else:
        move()
        