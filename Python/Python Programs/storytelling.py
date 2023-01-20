
#your inputs
answer = input("Would you like to play a game? (yes/no) ")
ask = input("What is your name? ")
print("Once upon a time in a far far universe, there was a peaceful world like Earth with earth like people, but...")
print("There ensued Chaos in this world due to a significant scientific advancement ruining the natural stablility...")
print("Save Yourself. Life for life. RUN! GO!")


if answer == "yes":
    answer = input("You reached crossroads, would you like to go left or right? ")
    if answer == "left":
        answer = input("You find people fighting each other, join the fight or run? ")
        if answer == "fight":
            print("That wasn't a good idea.\nYou are hurt.\nGame Over!")
        elif answer == "run":
            print("Good choice, you made it away safely from the riots\nOh no they saw you you need to get away soon...")
            answer = input("You find a car and a bike, choose one ")
            if answer == "car":
                print("Unfortunately you do not know how to drive a car.\nGame over!")
            else:
                print("You rode it fast and got away safe and sound.\nGood job\nYOU WIN!!!")
        else:
            print("choose something quick, there is not time to waste, make haste")
    else:
        print("You chose right but that that was not the right choice, sorry\nGame over!")
else:
    print("That's so sad, please play the game with me next time!")
	
