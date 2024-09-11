import requests
import random
import html
import colorama
from colorama import Fore, Back, Style


# URL's for different difficulty API levels
# https://www.dataquest.io/blog/python-api-tutorial/
# Open Trivia Database: https://opentdb.com/
API_LEVELS = {
    "1": (
        "https://opentdb.com/api.php?amount=40&category=11&"
        "difficulty=easy&type=multiple"
        ),
    "2": (
        "https://opentdb.com/api.php?amount=40&category=11&"
        "difficulty=medium&type=multiple"
        ),
    "3": (
        "https://opentdb.com/api.php?amount=40&category=11&"
        "difficulty=hard&type=multiple"
        )
}

# Chosen difficulty levels returned with user input
LEVEL_DIFFICULTY = {
    "1": "EASY",
    "2": "MEDIUM",
    "3": "HARD"
}


def load_questions(difficulty):
    """
    Load questions from API database,
    based on the user chosen difficulty
    """
    url = API_LEVELS.get(difficulty)
    response = requests.get(url)
    # Imports the requests module
    if response.status_code == 200:
        return response.json()["results"]
    else:
        # Feedback if quiz API doesn't load initially
        print("Error loading the quiz questions, please reload page.")
        return []


def display_questions(question_data, index):
    """
    Display and format questions and answer choices,
    includes correct and incorrect answers
    """
    # stackoverflow.com/questions/2087370/decode-html-entities-in-python-string
    question = html.unescape(
        question_data['question']
    )
    correct_answer = html.unescape(
        question_data['correct_answer']
    )
    incorrect_answers = [
        html.unescape(ans) for ans in question_data['incorrect_answers']
    ]

    all_answers = incorrect_answers + [correct_answer]

    # Shuffle mutliple choice correct + incorrect answers
    # randomises each correct answer per question fetched
    # https://www.geeksforgeeks.org/random-shuffle-function-in-python/
    random.shuffle(all_answers)

    # Format display of each question and the choices individually
    # Add color to feedback sections: https://pypi.org/project/colorama/
    print(Style.BRIGHT + Fore.CYAN + f"Question {index + 1}:\n{question}")
    print(Style.RESET_ALL)
    for i in range(len(all_answers)):
        answer = all_answers[i]
        print(f"{i + 1}. {answer}")

    return correct_answer, all_answers


def get_input(prompt, valid_options):
    """
    Prompt the user for level selection,
    makes sure user input is a valid selection
    """
    while True:
        user_input = input(prompt).strip()
        if user_input in valid_options:
            return user_input
        # Pull valid options from get_level and to assist user input
        else:
            print(Style.BRIGHT + Back.YELLOW + f"\nINVALID INPUT!")
            print(Style.RESET_ALL)
            print(f"Enter one of the following: {', '.join(valid_options)}.")


def game_loop(team_name=None):
    """
    Run welcome screen to main menu,
    user enters name and selects quiz difficulty.
    Modify by adding team_name=None, to accept team_name
    allowing quiz to retain the team_name if replaying
    https://stackoverflow.com/questions/47840794/none-in-python
    """
    if not team_name:
        print(Style.BRIGHT + Fore.CYAN + "*** Risky Quizness ***\n")
        print(Style.RESET_ALL)
        print("Welcome to our film trivia, are you a true film buff?")
        print("Test your knowledge with 10 multiple choice questions.\n")
        # User to enter their name
        team_name = input(
            Fore.CYAN + "Enter your team name:\n").strip().title()
        print(Style.RESET_ALL)

    # Introduce user to quiz and select difficulty level (1, 2, or 3)
    difficulty = get_input(
        f"\nSelect a difficulty level:\n1. Easy\n2. Medium\n3. Hard\n",
        ['1', '2', '3']
    )
    chosen_level = LEVEL_DIFFICULTY[difficulty]
    print(Fore.CYAN + f"\n{team_name}, you have opted for {chosen_level}.\n")
    print(Style.RESET_ALL)

    # Load questions for the chosen difficulty level
    questions = load_questions(difficulty)
    # Exit and stop quiz if no questions load from API
    if not questions:
        return

    # Start score counter at 0
    team_score = 0

    # Display 10 randomised questions only, from the level selected
    # 40 questions fetched per difficulty level
    selected_questions = random.sample(questions, 10)
    for question_index in range(len(selected_questions)):
        question_data = selected_questions[question_index]
        correct_answer, all_answers = display_questions(
            question_data, question_index
        )

        # Loop through quiz after player ans each question with valid input
        team_answer = get_input("\n--> Answer (1-4): ", ['1', '2', '3', '4'])

        # Validate if team_answer is correct
        if all_answers[int(team_answer) - 1] == correct_answer:
            print(Style.BRIGHT + Fore.GREEN + f"--> Correct {team_name}!\n")
            print(Style.RESET_ALL)
            team_score += 1
        else:
            print(Fore.RED + f"--> Oops! The answer is: {correct_answer}\n")
            print(Style.RESET_ALL)

    # Calculate player score after all 10 quiz questions completed
    print(Style.BRIGHT + Fore.CYAN + f"*** You scored {team_score}/10 ***")

    # Gives player feedback based on their final score
    if team_score < 5:
        print(f"Better luck next time! Not quite the film buff just yet.\n")
    elif team_score >= 8:
        print(f"Right down to Quizness... you're a true film buff!\n")
    else:
        # Score between 5 and 7
        print(f"Not bad, you could brush up on your film knowledge.\n")

    print(Style.RESET_ALL)

# Give user options:
# 1 = take another quiz as the same team_name
# 2 = take quiz as a new team_name
# 3 = exit the quiz
    play_again = get_input(
        "Want to try again?\n1. New Quiz\n2. New Team\n3. Exit\n",
        ['1', '2', '3']
    )
    # Same player takes quiz
    if play_again == '1':
        game_loop(team_name)
    # New player takes quiz
    elif play_again == '2':
        game_loop()
    else:
        print(Style.BRIGHT + Fore.CYAN + f"*** See you soon {team_name} ***")
        print(Style.RESET_ALL)


# Initial quiz launch
if __name__ == "__main__":
    game_loop()