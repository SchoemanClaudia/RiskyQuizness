import sys
sys.path.append("/home/gitpod/.pyenv/versions/3.12.2/lib/python3.12/site-packages")
import requests
import random
import html

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
    # https://stackoverflow.com/questions/2087370/decode-html-entities-in-python-string
    question = html.unescape(question_data['question'])
    correct_answer = html.unescape(question_data['correct_answer'])
    incorrect_answers = [html.unescape(ans) for ans in question_data['incorrect_answers']]

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
            print(f"INVALID INPUT!\nPlease enter one of the following: {', '.join(valid_options)}.\n")


def game_loop():
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

    # Display 10 randomised questions only, from the level selected (40 per difficulty)
    selected_questions = random.sample(questions, 10)
    for question_index in range(len(selected_questions)):
        question_data = selected_questions[question_index]
        correct_answer, all_answers = display_questions(question_data, question_index)

        # Loop through quiz after player answers each question with valid input
        player_answer = get_input("Your answer (1-4): ", ['1', '2', '3', '4'])

        # Validate if player_answer is correct
        if all_answers[int(player_answer) - 1] == correct_answer:
            print(f"Correct, {player_name}!\n")
            player_score += 1
        else:
            print(f"Oops! The correct answer is: {correct_answer}\n")
    
    # Calculate player score after all 10 quiz questions completed
    print(f"Your film trivia score is {player_score}/10")

    # Gives player feedback based on their final score
    if player_score < 5:
        print(f"Better luck next time, {player_name}! Not quite the film buff just yet.")
    elif player_score >= 8:
        print(f"Right down to Quizness, {player_name}! You're a true film buff!")
    else:
        # Score between 5 and 7
        print(f"Not bad, {player_name}... you could brush up on your film knowledge.")


game_loop()