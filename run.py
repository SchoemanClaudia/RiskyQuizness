import requests
import random
import html

# URL's for different difficulty API levels
# https://www.dataquest.io/blog/python-api-tutorial/
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


def load_questions(difficulty):
    """
    Load questions from API database,
    based on the user chosen difficulty
    """
    url = API_LEVELS.get(difficulty)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["results"]


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

    # Format display of each question and the choices individually
    print(f"Question {index + 1}: {question}")
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
        user_input = input(prompt)
        if user_input in valid_options:
            return user_input
        # Pull valid options from get_level and to assist user input
        else:
            print(f"INVALID INPUT!\n")
            print(f"Enter one of the following: {', '.join(valid_options)}.\n")


def game_loop(player_name=None):
    """
    Run welcome screen to main menu,
    user enters name and selects quiz difficulty.
    Modify by adding player_name=None, to accept player_name
    allowing quiz to retain the player_name if replaying
    https://stackoverflow.com/questions/47840794/none-in-python
    """
    if not player_name:
        print("*** Risky Quizness ***\n")
        print("Welcome to our film trivia, are you a true film buff?")
        print("Test your knowledge with 10 multiple choice questions.\n")
        # User to enter their name
        player_name = input("What is your name?\n").strip().title()

    # Introduce user to quiz and select difficulty level (1, 2, or 3)
    difficulty = get_input(
        f"Select a difficulty level: (Easy = 1, Medium = 2, Hard = 3)\n",
        ['1', '2', '3']
    )
    chosen_level = LEVEL_DIFFICULTY[difficulty]
    print(f"\n{player_name}, you have selected {chosen_level} difficulty.\n")

    # Load questions for the chosen difficulty level
    questions = load_questions(difficulty)

    # Start score counter at 0
    player_score = 0

    # Display 10 randomised questions only, from the level selected
    # 40 questions fetched per difficulty level
    selected_questions = random.sample(questions, 10)
    for question_index in range(len(selected_questions)):
        question_data = selected_questions[question_index]
        correct_answer, all_answers = display_questions(
            question_data, question_index
        )

        # Loop through quiz after player answers each question with valid input
        player_answer = get_input("Your answer (1-4): ", ['1', '2', '3', '4'])

        # Validate if player_answer is correct
        if all_answers[int(player_answer) - 1] == correct_answer:
            print(f"Correct {player_name}!\n")
            player_score += 1
        else:
            print(f"Oops! The correct answer is: {correct_answer}\n")

    # Calculate player score after all 10 quiz questions completed
    print(f"{player_name}, your film trivia score is {player_score}/10")

    # Gives player feedback based on their final score
    if player_score < 5:
        print(f"Better luck next time! Not quite the film buff just yet.\n")
    elif player_score >= 8:
        print(f"Right down to Quizness... you're a true film buff!\n")
    else:
        # Score between 5 and 7
        print(f"Not bad, you could brush up on your film knowledge.\n")

# Give user options:
# 1 = take another quiz as the same player_name
# 2 = take quiz as a new player_name
# 3 = exit the quiz
    play_again = get_input(
        "Want to try again?\n(New Quiz = 1, New player = 2, Exit = 3):\n",
        ['1', '2', '3']
    )
    # Same player takes quiz
    if play_again == '1':
        game_loop(player_name)
    # New player takes quiz
    elif play_again == '2':
        game_loop()
    else:
        print(f"Goodbye {player_name}, thank you for playing.")


# Initial quiz launch
if __name__ == "__main__":
    game_loop()