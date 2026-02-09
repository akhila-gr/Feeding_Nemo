import json # for loading and saving dict to file
import os # operating system for checking if file exists
import random # chose random words
import time
import threading # for background task (for user key/game input)
import msvcrt # user game key input
#user_managment_system

# 1. Welcome message
# 2. Load save file
# 3. if there is no save file: start creating new user
# 4. if there is a save file: show existing users and new user option
# 5. if creating new user: ask name
# 6. if exisitng user: set name

user_name = None
user_data_file_name = "user_data.json" # txt file for all profiles
user_data = {}
empty_save_game = {"incorrect_words": {"der":[], "die":[], "das":[]}, "max_streak": 0, "average_streak_sum": 0, "game_count": 0, "incorrect_guesses": 0, "correct_guesses": 0, "max_score": 0}
game_running = False
fish_position = "middle"

def start():
    global user_name
    print("Welcome to Feeding Nemo: Der-Die-Das Edition")
    load_user_data_file()
    user_name = user_management_system()
    game_menu()

def save_user_data_file():
    # json.dumps creates a string out of a dict (to save a dict in a file) 
    user_data_string = json.dumps(user_data)
    # saving the string in the user data file
    with open(user_data_file_name, "w") as file:
        file.write(user_data_string)

def load_user_data_file(): 
    global user_data
    # check if file exists
    if os.path.isfile(user_data_file_name):
        # load file as dict
        with open(user_data_file_name, "r") as file:
            user_data = json.load(file)

def user_management_system():
    # if there is no save file: start creating new user
    if len(user_data) == 0:
        return create_new_user()
    else:
        # if there is a save file: show existing users and new user option
        print("*" * 30)
        print("[1] New profile")
        # show list of all user with option number
        # using enumerate to get a number/index for each user option
        profiles = list(enumerate(user_data))
        for index, user in profiles:
            # adding 2 because option 1 is already new profile and index starts at zero
            print(f"[{index + 2}] {user}")
        choice = input("Chose an option: ")
        # check for invalid input
        while not (choice.isdigit() and int(choice) > 0 and int(choice) < len(profiles) + 2):
             choice = input("Invalid choice. Chose a valid option: ")
        if choice == "1":
            return create_new_user()
        else:
            # get user from tuple out of profile list
            # saved as user_name in start()
            return profiles[int(choice)-2][1]
            
def create_new_user():
    name = input("Please chose a name: ")
    # new entry for new user with template
    user_data[name] = empty_save_game
    save_user_data_file()
    return name

def game_menu():
    print("*" * 30)
    print("[1] Start Game")
    print("[2] Practice Mode")
    print("[3] Repetition Mode")
    print("[4] Show Statistics")
    print("[5] Exit")
    choice = input("Chose an option: ")
    # check for invalid input
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 5):
        choice = input("Invalid choice. Chose a valid option: ")
    if choice == "1":
        chose_difficulty_menu("normal")
    elif choice == "2":
        chose_difficulty_menu("practice")
    elif choice == "3":
        chose_article_menu("repetition", "medium")
    elif choice == "4":
        show_statistics()

# mode = normal, practice, repetition
def chose_difficulty_menu(mode):
    print("*" * 30)
    print("[1] Easy")
    print("[2] Medium")
    print("[3] Hard")
    print("[4] Back to menu")
    choice = input("Chose a difficulty: ")
    # check for invalid input
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 4):
        choice = input("Invalid choice. Chose a valid option: ")
    if choice == "1":
        chose_article_menu(mode, "easy")
    elif choice == "2":
        chose_article_menu(mode, "medium")
    elif choice == "3":
        chose_article_menu(mode, "hard")
    elif choice == "4":
        game_menu()

# mode = normal, practice, repetition
def chose_article_menu(mode, difficulty):
    print("*" * 30)
    print("[1] der")
    print("[2] die")
    print("[3] das")
    print("[4] Back to main menu")
    choice = input("Chose an article: ")
    # check for invalid input
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 4):
        choice = input("Invalid choice. Chose a valid option: ")
    if choice == "1":
        start_game(mode, difficulty, "der")
    elif choice == "2":
        start_game(mode, difficulty, "die")
    elif choice == "3":
        start_game(mode, difficulty, "das")
    elif choice == "4":
        game_menu()
    
# mode = normal, practice, repetition
# difficulty = easy, medium, hard
def start_game(mode, difficulty, article):
    global game_running, fish_position
    current_article_wordlist = load_article_wordlist(mode, difficulty, article)
    other_article_wordlist = []
    # other two words are from the other article lists (only one word from the current article list)
    if article == "der":
        other_article_wordlist = load_article_wordlist(mode, difficulty, "die")
        other_article_wordlist += load_article_wordlist(mode, difficulty, "das")
    elif article == "die":
        other_article_wordlist = load_article_wordlist(mode, difficulty, "der")
        other_article_wordlist += load_article_wordlist(mode, difficulty, "das")
    elif article == "das":
        other_article_wordlist = load_article_wordlist(mode, difficulty, "die")
        other_article_wordlist += load_article_wordlist(mode, difficulty, "der")

    max_time = 60 #seconds

    lives = 5
    score = 0
    streak = 0
    current_max_streak = 0 # maximum streak in current game
    new_max_streak = False # true if we reached a new max streak (for finish screen)
    game_running = True
    result = ""
    unique_words = set() # save already used words

    # start background thread for user input
    fish_position = "middle"
    thread = threading.Thread(target=user_gaming_input, daemon=True)
    thread.start()

    start_time = time.time()
    # setting the seed of random to the current time to always have a different seed (time changes -> seed changes -> random changes)
    # order of words change for every game
    random.seed(start_time)

    # loop that takes new word
    while lives > 0 and calculate_seconds_left(max_time, start_time) > 0:
        # check if all words were already used
        # if yes: reset unique wordlist
        # (should not be neccesary if wordlist is long enough)
        if len(current_article_wordlist) == len(unique_words):
            unique_words = set()
        # draw random word of current article/fish   
        correct_word = random.choice(current_article_wordlist)        
        # check if we already used the correct word
        while correct_word in unique_words:
            correct_word = random.choice(current_article_wordlist)     
        unique_words.add(correct_word)

        # draw random word from the other 2 articles
        other_word1 = random.choice(other_article_wordlist)
        other_word2 = random.choice(other_article_wordlist)
        # ensure that both other words are different
        while other_word1 == other_word2:
            other_word2 = random.choice(other_article_wordlist)
        # put the three words together
        current_words = [correct_word, other_word1, other_word2]
        random.shuffle(current_words)

        max_steps = 12 # how many frames per word
        current_step = max_steps
        pause = 0.5 # how much seconds pass between two frames
        # loop for one word (printing frame multiple times)
        while current_step >= 0:
            seconds_left = calculate_seconds_left(max_time, start_time)
            if seconds_left < 0:
                break
            # Stop background task before drawing next frame (to prevent lagging)
            game_running = False
            thread.join()
            draw_next_frame(result, current_step, max_steps, score, streak, lives, seconds_left, article, current_words, mode, difficulty)
             # if last frame was correct/incorrect message reset result variable and don't decrease step
            if result != "":
                result = ""
            else:
                #reduce the steps to reduce the spaces in front of the words (= let them float)
                current_step -=1
            # Start background task again after drawing frame
            game_running = True
            thread = threading.Thread(target=user_gaming_input, daemon=True)
            thread.start()
            # wait before drawing next frame
            time.sleep(pause)

        # Get the word at the fish position
        chosen_word = ""
        if fish_position == "up":
            chosen_word = current_words[0]
        elif fish_position == "middle":
            chosen_word = current_words[1]
        elif fish_position == "down":
            chosen_word = current_words[2]
            
        if correct_word == chosen_word:
            score += 1
            streak +=1
            result = "correct"
            if streak > current_max_streak:
                current_max_streak = streak
            if not mode ==  "practice":
                if score > int(user_data[user_name]["max_score"]):
                    user_data[user_name]["max_score"] = score
                if streak > int(user_data[user_name]["max_streak"]):
                    user_data[user_name]["max_streak"] = streak
                    new_max_streak = True
                user_data[user_name]["correct_guesses"] += 1
        else:
            streak = 0
            result = "incorrect"
            if not mode ==  "practice":
                lives -= 1
                user_data[user_name]["incorrect_words"][article].append(correct_word)
                user_data[user_name]["incorrect_guesses"] += 1
    # end background task
    game_running = False
    thread.join()
    user_data[user_name]["game_count"] += 1
    # summing up the max streak of each game to calculate the average streak in the statistics
    user_data[user_name]["average_streak_sum"] += current_max_streak
    save_user_data_file() # Saving user data after game
    draw_game_finished_screen(score, current_max_streak, lives, mode, difficulty, article, new_max_streak)
    game_menu()

def calculate_seconds_left(max_time, start_time):
    current_time = time.time()
    # substract time before from time after = how long has it been
    # substract from max_time to see how much time left
    return int(max_time - (current_time - start_time))

# parallelisation (backround task)
def user_gaming_input():
    global fish_position, game_running
    while game_running:
        if msvcrt.kbhit(): # Check if a key has been pressed
            user_input = msvcrt.getch() # Get the key pressed
            if user_input == b'w' or user_input == b'H': # w button or up arrow
                if fish_position == "middle":
                    fish_position = "up"
                elif fish_position == "down":
                    fish_position = "middle"
            elif user_input == b's' or user_input == b'P': # s button or down arrow
                if fish_position == "middle":
                    fish_position = "down"
                elif fish_position == "up":
                    fish_position = "middle"


def load_article_wordlist(mode, difficulty, article):
    if mode == "normal" or mode == "practice":
        # load and return wordlist depending on difficulty and article
        filename = f"{difficulty}_{article}.txt"
        wordlist = []
        with open(filename, "r") as file:
            wordlist = file.readlines()
        # remove \n at the end of each word
        for index in range(len(wordlist)):
            wordlist[index] = wordlist[index].strip()
        return wordlist
    # in repetition mode, use the incorrect words of the user
    if mode == "repetition":
        return user_data[user_name]["incorrect_words"][article]

def draw_next_frame(result, current_step, max_steps, score, streak, lives, seconds_left, article, current_words, mode, difficulty):
    global fish_position
    print("═════════════════════════════════════════════════════════════════")
    print()
    if mode ==  "practice":
        print(f"  Score: {score}        Time: {seconds_left}")
    else:
        print(f"  Score: {score}       Lives: {lives}               Time: {seconds_left}    Streak: {streak}") 
    print(f"Article: {article}      Mode: {mode}    Difficulty: {difficulty}")
    print()
    print("═════════════════════════════════════════════════════════════════")
    if result == "":
        print()
        print()
        spaces_per_step = int(36 / max_steps)
        if fish_position == "up":
            print(f" ><{article}>{current_step * spaces_per_step * ' '}← {current_words[0]}")
        else:
            print(f"       {current_step * spaces_per_step * ' '}← {current_words[0]}")
        print()
        if fish_position == "middle":
            print(f" ><{article}>{current_step * spaces_per_step * ' '}← {current_words[1]}")
        else:
            print(f"       {current_step * spaces_per_step * ' '}← {current_words[1]}")
        print()
        if fish_position == "down":
            print(f" ><{article}>{current_step * spaces_per_step * ' '}← {current_words[2]}")
        else:
            print(f"       {current_step * spaces_per_step * ' '}← {current_words[2]}")
        print()
        print()
    elif result == "correct":
        print()
        print()
        print()
        print()
        print("                 Correct!       ")
        print()
        print()
        print()
        print()
    elif result == "incorrect":
        print()
        print()
        print()
        print()
        print("                 Incorrect!       ")
        print()
        print()
        print()
        print()
    print("═════════════════════════════════════════════════════════════════")
    print()
    print("Use ↑ / ↓ (W/S) to move your fish   |   Press ENTER to select")
    print()
    print("═════════════════════════════════════════════════════════════════")

def draw_game_finished_screen(score, max_streak, lives, mode, difficulty, article, new_max_streak):
    print("*" * 30)
    print("TODO: Game Finished Screen")
    print("*" * 30)

def show_statistics():
    print("*" * 30)
    print("TODO: Showing Statistics")
    print(f"Maximum Streak: {user_data[user_name]["max_streak"]}")
    if user_data[user_name]['game_count'] > 0:
        print(f"Average Streak: {user_data[user_name]["average_streak_sum"] / user_data[user_name]["game_count"]}")
    else:
        print("Average Streak: 0")
    print("*" * 30)
    game_menu()

start()