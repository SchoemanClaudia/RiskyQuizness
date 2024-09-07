# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

def main_menu():
    """
    Run welcome screen to main menu,
    user enters name and selects quiz difficulty
    """
    print("Risky Quizness")

    # User to enter their name
    player_name = input("What is your name: ").strip().title()
    print("Risky Quizness")
    print(player_name)
    

main_menu()