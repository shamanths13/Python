# Import python module random to choose randomly
import random

# Create the list on which we can use random function to decide computer choice
lst=["rock", "paper", "scissors"]

# Use a while True loop for making the program run infinitely.
# While True loop not required if you want the program to run only once
while True:
    
    # Print a seperator
    print("* * * * * * * * * * * * * * *")
    
    # Take input from the user
    user_choice=input("Choose Rock, Paper or Scissors\n")
    
    # Convert user input to all small so we can compare to our computer choice list
    user_choice=str.lower(user_choice)
    
    # Choose random element from the list we created.
    computer_choice=random.choice(lst)
    
    # Print user choice and computer choice
    print("Your choice: ", user_choice)
    print("Computer's choice: ", computer_choice)
    
    # Compare all the possibilities or combinations using if-elif.
    # Then show the result based on which condition is true.
    if computer_choice == "rock" and user_choice == "scissors":
        print("You lose!")
    elif computer_choice == "scissors" and user_choice == "rock":
        print("You win!")
    elif computer_choice == "paper" and user_choice == "rock":
        print("You lose!")
    elif computer_choice == "rock" and user_choice == "paper":
        print("You win!")
    elif computer_choice == "scissors" and user_choice == "paper":
        print("You lose!")
    elif computer_choice == "paper" and user_choice == "scissors":
        print("You win!")
    elif computer_choice == user_choice:
        print("Draw!")
    else:
        print("Incorrect input!")
    print("")
    