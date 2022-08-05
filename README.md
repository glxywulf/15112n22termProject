For now, just a brainstorming place and place to gather thoughts or make 
pseudocode. Also probably will place cited stuff here too

Ok, so we've got the Line class being worked on. So far we've established its
base instance variables, its starting/ending points, and checks for it to see 
if it knows if its horizontal or vertical. It can also realize that if it isn't
either one of those, it will be denoted as diagonal.

We now have a player figure drawn and mapped onto the canvas. Need to work on 
collision and physics tomorrow. 

Ok, stayed up late and got horizontal movement working. Work on physics tomorrow

Specifically let's get gravity working. For now, we just need to get the 
concept of gravity working inside of the window. We shouldn't worry about window
borders at the moment or even later as we should avoid window borders.

We need to avoid those borders because of the fact that the player needs to be 
able to seamlessly shift between levels by going either above the window top or 
bottom.

You left off at making gravity a thing. Last point you were at you made the 
gravity point upward. -- Nevermind, you were just dumb and though -y was down. 
Which it is technically. But not here.

Ok we have bottom collisions working, next we should work on left and right

Last thing you were working on was vertical line collision. Has the problem of
sticking to any vertical line present.

Currently stuck at a divide by 0 thing. test it out in test.py to see where
the issue is. 

Issue was that the collision thing from Jeff only works with diagonals since 
if the line were vertical or horizontal it causes a scenario where the equation
he provided gave us a divisor of 0. Hence pulling a divide by 0 error.

Ok, got collision working 80%ish kinda, uhh, work on jump function when you get 
back ok thankyou.