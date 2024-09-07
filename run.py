# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import requests

# URL's for different difficulty API levels - https://www.dataquest.io/blog/python-api-tutorial/
# Open Trivia Database: https://opentdb.com/
API_LEVELS = {
    "1": "https://opentdb.com/api.php?amount=40&category=11&difficulty=easy&type=multiple",
    "2": "https://opentdb.com/api.php?amount=40&category=11&difficulty=medium&type=multiple",
    "3": "https://opentdb.com/api.php?amount=40&category=11&difficulty=hard&type=multiple"
}

# Chosen difficulty levels returned with user input
LEVEL_DIFFICULTY = {
    "1": "EASY",
    "2": "MEDIUM",
    "3": "HARD"
}


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
            print(f"INVALID INPUT!\nPlease enter one of the following: {', '.join(valid_options)}.\n")
        

def main_menu():
    """
    Run welcome screen to main menu,
    user enters name and selects quiz difficulty
    """
    print("*** Risky Quizness ***\n")
    print("Welcome to our film trivia, are you a true film buff?")
    print("Let's test your knowledge with 10 randomised multiple choice questions.\n")

    # User to enter their name
    player_name = input("Before we get started, type your name:\n").strip().title()

    # Introduce user to quiz and select difficulty level (1, 2, or 3)
    difficulty = get_level(
        f"Select a difficulty level: (Easy = 1, Medium = 2, Hard = 3)\n",
        ['1', '2', '3']
    )
    chosen_level = LEVEL_DIFFICULTY[difficulty]
    print(f"\n{player_name}, you have selected {chosen_level} difficulty.\n")


main_menu()