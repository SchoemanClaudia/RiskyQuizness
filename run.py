# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high


def get_level(prompt, valid_options):
    """
    Prompt the user for level selection,
    makes sure user input is a valid selection
    """
    while True:
        user_input = input(prompt)
        if user_input in valid_options:
            return user_input
        # Pull valid options from get_level to assist user input
        else:
            print(f"Invalid input! Please enter one of the following: {', '.join(valid_options)}.")
        

def main_menu():
    """
    Run welcome screen to main menu,
    user enters name and selects quiz difficulty
    """
    print("*** Risky Quizness ***\n")
    print("Welcome to our film trivia, are you a true film buff?")
    print("Let's test your knowledge with 10 randomised multiple choice questions.\n")

    # User to enter their name
    player_name = input("What is your name:\n").strip().title()
    print("\n")

    # Introduce user to quiz and select difficulty level (1, 2, or 3)
    difficulty = get_level(
        f"Select a difficulty level: (Easy = 1, Medium = 2, Hard = 3)\n",
        ['1', '2', '3']
    )
    

main_menu()