import json # for loading and saving dict to file
import os # operating system for checking if file exists
import random # chose random words
import time
import threading # for background task (for user key/game input)
import msvcrt # user game key input
import pandas as pd
import plotly.express as px
import winsound #for sound



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
empty_save_game = {"incorrect_words": {"der":[], "die":[], "das":[]}, "max_streak": 0, "average_streak_sum": 0, "game_count": 0, "incorrect_guesses": 0, "correct_guesses": 0, "max_score": 0, "scores": [], "streaks": []}
game_running = False
fish_position = "middle"

def start():
    global user_name
    print("\033[34mWelcome to ")
    print("\033[31m\033[1m><> FEEDING NEMO ><>\033[0m")
    print("\033[34m\x1B[3mDer-Die-Das Edition\033[0m")
    
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
        print("><> " * 20)
        print("\033[1m[1]\033[0m New profile")
        # show list of all user with option number
        # using enumerate to get a number/index for each user option
        profiles = list(enumerate(user_data))
        for index, user in profiles:
            # adding 2 because option 1 is already new profile and index starts at zero
            print(f"\033[1m[{index + 2}]\033[0m {user}")
        choice = input("\x1B[3mChoose an option:\x1B[0m ")
        # check for invalid input
        while not (choice.isdigit() and int(choice) > 0 and int(choice) < len(profiles) + 2):
             choice = input("Invalid choice. Choose a valid NUMBER: ")
        if choice == "1":
            return create_new_user()
        else:
            # get user from tuple out of profile list
            # saved as user_name in start()
            return profiles[int(choice)-2][1]
            
def create_new_user():
    name = input("\x1B[3m\nPlease choose a name:\x1B[0m ")
    # new entry for new user with template
    user_data[name] = empty_save_game
    save_user_data_file()
    return name

def game_menu():
    print("><> " * 20)
    print("\033[1m[1]\033[0m Start Game")
    print("\033[1m[2]\033[0m Practice Mode")
    print("\033[1m[3]\033[0m Repetition Mode")
    print("\033[1m[4]\033[0m Show Statistics")
    print("\033[1m[5]\033[0m Rules")
    print("\033[1m[6]\033[0m Exit")
    choice = input("\x1B[3mChoose an option:\x1B[0m ")
    # check for invalid input
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 6):
        choice = input("Invalid choice. Choose a valid NUMBER: ")
    if choice == "1":
        chose_difficulty_menu("Normal")
    elif choice == "2":
        chose_difficulty_menu("Practice")
    elif choice == "3":
        chose_article_menu("Repetition", "Medium")
    elif choice == "4":
        show_statistics()
    elif choice == "5":
        print("Explanation of Rules")
    

# mode = normal, practice, repetition
def chose_difficulty_menu(mode):
    print("><> " * 20)
    print("\033[1m[1]\033[0m Easy")
    print("\033[1m[2]\033[0m Medium")
    print("\033[1m[3]\033[0m Hard")
    print("\033[1m[4]\033[0m Back to menu")
    choice = input("\x1B[3mChoose a difficulty:\x1B[0m ")
    # check for invalid input
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 4):
        choice = input("Invalid choice. Choose a valid NUMBER: ")
    if choice == "1":
        chose_article_menu(mode, "Easy")
    elif choice == "2":
        chose_article_menu(mode, "Medium")
    elif choice == "3":
        chose_article_menu(mode, "Hard")
    elif choice == "4":
        game_menu()

# mode = normal, practice, repetition
def chose_article_menu(mode, difficulty):
    print("><> " * 20)
    print("\033[1m[1]\033[0m der")
    print("\033[1m[2]\033[0m die")
    print("\033[1m[3]\033[0m das")
    print("\033[1m[4]\033[0m Back to main menu")
    choice = input("\x1B[3mChoose an article:\x1B[0m ")
    # check for invalid input
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 4):
        choice = input("Invalid choice. Choose a valid NUMBER: ")
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

        # draw two distinct words from the other 2 articles
        if len(other_article_wordlist) >= 2:
            other_word1, other_word2 = random.sample(other_article_wordlist, 2)
        # if not enough words in the article_wordlist
        else:
            double_list = other_article_wordlist * 2
            other_word1, other_word2 = random.sample(double_list, 2)
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
            try:
                winsound.Beep(1200, 250)  # 1200 Hz for 250 ms
            except RuntimeError:
                pass  # in case the speaker is unavailable
            if streak > current_max_streak:
                current_max_streak = streak
            if not mode ==  "Practice":
                if score > int(user_data[user_name]["max_score"]):
                    user_data[user_name]["max_score"] = score
                if streak > int(user_data[user_name]["max_streak"]):
                    user_data[user_name]["max_streak"] = streak
                    new_max_streak = True
                user_data[user_name]["correct_guesses"] += 1
        else:
            streak = 0
            result = "incorrect"
            try:
                winsound.Beep(350, 280)   # 350 Hz, 280 ms
            except RuntimeError:
                pass

            if not mode ==  "Practice":
                lives -= 1
                user_data[user_name]["incorrect_words"][article].append(correct_word)
                user_data[user_name]["incorrect_guesses"] += 1
    # end background task
    game_running = False
    thread.join()
    user_data[user_name]["game_count"] += 1
    user_data[user_name]["scores"].append(score)
    user_data[user_name]["streaks"].append(current_max_streak)
    # summing up the max streak of each game to calculate the average streak in the statistics
    user_data[user_name]["average_streak_sum"] += current_max_streak
    save_user_data_file() # Saving user data after game
    draw_game_finished_screen(score, current_max_streak, mode, difficulty, article, new_max_streak)
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
            user_input = msvcrt.getch() # Get the key pressed/ which key pressed?
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
    if mode == "Normal" or mode == "Practice":
        # load and return wordlist depending on difficulty and article
        filename = f"{difficulty}_{article}.txt"
        if not os.path.exists(filename):
            print("404 Wordlist not found")
            print("Please execute programm in the correct folder.")
            quit()
        wordlist = []
        with open(filename, "r") as file:
            wordlist = file.readlines()
        # remove \n at the end of each word
        for index in range(len(wordlist)):
            wordlist[index] = wordlist[index].strip()
        return wordlist
    # in repetition mode, use the incorrect words of the user
    if mode == "Repetition":
        return user_data[user_name]["incorrect_words"][article]

def draw_next_frame(result, current_step, max_steps, score, streak, lives, seconds_left, article, current_words, mode, difficulty):
    global fish_position
    print("═════════════════════════════════════════════════════════════════")
    print()
    if mode ==  "Practice":
        print(f"      🏆: {score}          ⌛: {seconds_left}")
    else:
        print(f"     🏆: {score}         ❤️  : {lives}                  ⌛ : {seconds_left}         🔥 : {streak}") 
    print(f"Article: {article}      Mode: {mode}      Difficulty: {difficulty}")
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
    print("Use ↑ / ↓ (W/S) to move your fish")
    print()
    print("═════════════════════════════════════════════════════════════════")

def draw_game_finished_screen(score, max_streak, mode, difficulty, article, new_max_streak):
    print("><> " * 20)
    print(f"Mode:               {mode}")
    print(f"Difficulty:         {difficulty}")
    print(f"Article:            {article}")
    if article == "der":
        print("Hints:")
    elif article == "die":
        print("Hints:")
    else:
        print("Hints:")
    print(f"🏆:                  {score}")
    if score < 5:
        print("You should use practice mode to practice before coming back.")
    print(f"🔥:                  {max_streak}")
    if max_streak == new_max_streak:
        print(f"You reached a new maximum streak!")
    print("><> " * 20)
    print()
    print("><> ><> Highscores <>< <><")
    highscore_list = []
    for name in user_data:
        highscore_list.append((user_data[name]["max_score"], name))
    highscore_list.sort(reverse = True)
    for tuple in highscore_list:
        if tuple[1] == user_name:
            print(f"\033[1m><>     {tuple[1]}: {tuple[0]}\033[0m")
        else:
            print(f"><>     {tuple[1]}: {tuple[0]}")
        
    print("><> ><> ><>    <>< <>< <><")
    print()
    print()

def show_statistics():
    print("><> " * 20)
    print("Statistics")
    print(f"Maximum Streak: {user_data[user_name]["max_streak"]}")
    print("TODO: Highscore")
    if user_data[user_name]['game_count'] > 0:
        print(f"Average Streak: {user_data[user_name]["average_streak_sum"] / user_data[user_name]["game_count"]}")
    else:
        print("Average Streak: 0")
    print("><> " * 20)
    # store data in games (= number of scores until now as list) and scores columns
    num_games = len(user_data[user_name]['scores'])
    score_progress = pd.DataFrame({"games": list(range(1,num_games+1)), "score": user_data[user_name]['scores']})
    streak_progress = pd.DataFrame({"games": list(range(1,num_games+1)), "streaks": user_data[user_name]['streaks']})
    
    # Create the line chart    
    fig = px.line(
        score_progress,
        x = 'games',
        y = 'score',
        title = f"Your Progress Over {num_games} Games",
        labels = {'score': 'Score', 'games': 'Game'},
        markers = True,
        color_discrete_sequence = ['#FF69B4']
    ) 
    fig.add_scatter(
        x = streak_progress['games'],
        y = streak_progress['streaks'], 
        mode = 'lines', 
        name = 'Max Streak', 
        line = dict(color="#000000")
    )
    fig.show()
    game_menu()

start()