import json # for loading and saving dict to file
import os # operating system for checking if file exists
import random # chose random words
import time
import threading # for background task (for user key/game input)
import msvcrt # user game key input
import pandas as pd
import plotly.express as px
import winsound #for sound
import copy
import sys  # ensure that console supports UTF-8 (for ä, ö, ü)
sys.stdout.reconfigure(encoding='utf-8')


#user_managment_system

# 1. Welcome message
# 2. Load save file
# 3. if there is no save file: start creating new user
# 4. if there is a save file: show existing users and new user option
# 5. if creating new user: ask name
# 6. if exisitng user: set name


#constants
user_data_file_name = "user_data.json" # txt file for all profiles
width = 80  # total width of the console frame
empty_save_game = {"incorrect_words": {"der":[], "die":[], "das":[]}, "max_streak": 0, "average_streak_sum": 0, "game_count": 0, "incorrect_guesses": 0, "correct_guesses": 0, "max_score": 0, "scores": [], "streaks": []}
#globals
user_name = None
user_data = {}
game_running = False
fish_position = "middle"


def start():
    global user_name
    # -------------------------------
    #  Game Title
    # -------------------------------
    global width

    # Top divider and welcome message
    print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈" * 2)
    print("><> " * 20)
    # Welcome title
    print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈" * 2)
    print("\033[34m" + "Welcome to".center(width) + "\033[0m")
    print("\033[1m\033[31m" + "🐟 FEEDING NEMO 🐟".center(width) + "\033[0m")
    print("\033[34m\x1B[3m" + "    Der-Die-Das Edition".center(width) + "\033[0m")
    print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈" * 2)
    # Bottom grand border
    print("><> " * 20)
    print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈" * 2)

    # then load user data and show profile menu
    load_user_data_file()
    user_name = user_management_system()
    game_menu()

def save_user_data_file():
    # json.dumps creates a string out of a dict (to save a dict in a file) 
    user_data_string = json.dumps(user_data)
    # saving the string in the user data file
    with open(user_data_file_name, "w", encoding="utf-8") as file:
        file.write(user_data_string)

def load_user_data_file(): 
    global user_data
    # check if file exists
    if os.path.isfile(user_data_file_name):
        # load file as dict
        with open(user_data_file_name, "r", encoding="utf-8") as file:
            user_data = json.load(file)


def user_management_system():
    # if there is no save file: start creating new user
    if len(user_data) == 0:
        return create_new_user()
    else:
        # Professional heading for profile section
        # Top divider line for a clean professional look
        print("═" * width)

        # Main heading for the section, centered
        print("><> ><> PLAYER PROFILES ><> ><>".center(width))

        # Subtitle for clarity, explaining what the user should do
        print("Select your profile to continue!".center(width))

        # Bottom divider to complete the section header
        print("═" * width)
        print()  # extra line for spacing before listing options
        # show option to create a new profile
        print("\033[1m[1]\033[0m Create New Profile")

        # show list of all users with option number
        # using enumerate to get a number/index for each user option
        profiles = list(enumerate(user_data))
        for index, user in profiles:
            # adding 2 because option 1 is already new profile and index starts at zero
            print(f"\033[1m[{index + 2}]\033[0m {user}")

        # ask user to choose an option
        choice = input("\x1B[3mChoose an option:\x1B[0m ")

        # check for invalid input
        while not (choice.isdigit() and int(choice) > 0 and int(choice) < len(profiles) + 2):
             choice = input("Invalid choice. Choose a valid NUMBER: ")

        # if creating new user
        if choice == "1":
            return create_new_user()
        else:
            # get user from tuple out of profile list
            # saved as user_name in start()
            return profiles[int(choice)-2][1]
            
def create_new_user():
    # print a clean divider before asking for name
    print("><> " * 20)  # divider line for visual separation
    name = input("\x1B[3m\nPlease choose a name:\x1B[0m")
    # new entry for new user with template
    user_data[name] = copy.deepcopy(empty_save_game)
    save_user_data_file()
    return name

def game_menu():
    # -------------------------------
    # Game Menu Heading
    # -------------------------------
    print("═" * width)  # clean divider
    print("><> ><> GAME MENU ><> ><>".center(width))  # main section title
    print("Select an option to begin your adventure!".center(width))  # subtitle
    print("═" * width)
    print()

    # Menu options
    print("\033[1m[1]\033[0m Game Challenge")
    print("\033[1m[2]\033[0m Practice Mode")
    print("\033[1m[3]\033[0m Repetition Mode")
    print("\033[1m[4]\033[0m Show Statistics")
    print("\033[1m[5]\033[0m Rules")
    print("\033[1m[6]\033[0m Exit")

    # Get user choice
    choice = input("\x1B[3mChoose an option:\x1B[0m ")
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 6):
        choice = input("Invalid choice. Choose a valid NUMBER: ")

    # Navigate based on choice
    if choice == "1":
        choose_difficulty_menu("Game Challenge")
    elif choice == "2":
        choose_difficulty_menu("Practice")
    elif choice == "3":
        choose_difficulty_menu("Repetition")
    elif choice == "4":
        show_statistics()
    elif choice == "5":
        show_rules()  
    elif choice == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        # start()
        print("Bye, see you again!!!!")
        exit()
    

# mode = normal, practice, repetition
def choose_difficulty_menu(mode):
    # -------------------------------
    # Difficulty Menu Heading
    # -------------------------------
    print("═" * width)
    print("><> ><> SELECT DIFFICULTY ><> ><>".center(width))
    print(f"Mode: {mode}".center(width))
    print("Choose the German level to practice for this game!".center(width))
    print("═" * width)
    print()

    # Difficulty options with German levels
    print("\033[1m[1]\033[0m A1 - Easy")
    print("\033[1m[2]\033[0m A2 - Medium")
    print("\033[1m[3]\033[0m B1 - Hard")
    print("\033[1m[4]\033[0m Back to menu")
    print()

    # Get user choice
    choice = input("\x1B[3mChoose a level:\x1B[0m ")
    while not (choice.isdigit() and int(choice) > 0 and int(choice) <= 4):
        choice = input("Invalid choice. Choose a valid NUMBER: ")

    # Navigate based on choice
    if choice == "1":
        choose_article_menu(mode, "A1 - Easy") # keep internal difficulty for logic
    elif choice == "2":
        choose_article_menu(mode, "A2 - Medium")
    elif choice == "3":
        choose_article_menu(mode, "B1 - Hard")
    elif choice == "4":
        game_menu()

# mode = normal, practice, repetition
def choose_article_menu(mode, difficulty):
    # -------------------------------
    # Article Menu Heading
    # -------------------------------
    print("═" * width)
    print("><> ><> SELECT ARTICLE ><> ><>".center(width))
    print(f"Mode: {mode}".center(width))
    print("Choose the article to practice for this game!".center(width))
    print("═" * width)
    print()
    #List of options
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

    # Ensure new keys exist
    if "scores" not in user_data[user_name]:
        user_data[user_name]["scores"] = []
    if "streaks" not in user_data[user_name]:
        user_data[user_name]["streaks"] = []
    if "average_streak_sum" not in user_data[user_name]:
        user_data[user_name]["average_streak_sum"] = 0
    if "correct_guesses" not in user_data[user_name]:
        user_data[user_name]["correct_guesses"] = 0
    if "incorrect_guesses" not in user_data[user_name]:
        user_data[user_name]["incorrect_guesses"] = 0

    user_data[user_name]['last_mode'] = mode
    user_data[user_name]['last_difficulty'] = difficulty
    save_user_data_file() #For accuracy in statistics

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
    print("listening")

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

def user_gaming_input():
    global fish_position, game_running
    while game_running:
        if msvcrt.kbhit():  # check if a key is pressed
            key = msvcrt.getch()

            # Arrow keys produce two bytes: first b'\xe0' or b'\x00', second is actual arrow
            if key in [b'\xe0', b'\x00']:
                key2 = msvcrt.getch()  # get second byte
                if key2 == b'H':  # Up arrow
                    if fish_position == "middle":
                        fish_position = "up"
                    elif fish_position == "down":
                        fish_position = "middle"
                elif key2 == b'P':  # Down arrow
                    if fish_position == "middle":
                        fish_position = "down"
                    elif fish_position == "up":
                        fish_position = "middle"
            else:
                # Handle W/S keys for fallback
                if key == b'w':
                    if fish_position == "middle":
                        fish_position = "up"
                    elif fish_position == "down":
                        fish_position = "middle"
                elif key == b's':
                    if fish_position == "middle":
                        fish_position = "down"
                    elif fish_position == "up":
                        fish_position = "middle"


def load_article_wordlist(mode, difficulty, article):
    if mode == "Game Challenge" or mode == "Practice":
        # load and return wordlist depending on difficulty and article
        filename = f"{difficulty}_{article}.txt"
        if not os.path.exists(filename):
            print("404 Wordlist not found")
            print("Please execute programm in the correct folder.")
            quit()
        wordlist = []
        with open(filename, "r", encoding="utf-8") as file:
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

    # Clear console for Windows
    os.system('cls')

    fish_column = 10  # fixed column where the fish will appear
    spaces_per_step = int((width - fish_column - 10) / max_steps)  # space words move per step

    # Top divider and stats
    print("═" * width)
    if mode == "Practice":
        print(f"      🏆 Score: {score}          ⌛ Time Left: {seconds_left}")
    else:
        print(f"🏆 : {score}           ❤️ : {lives}           ⌛ : {seconds_left}        🔥 : {streak}")
    print(f"Article: {article}      Mode: {mode}      Difficulty: {difficulty}")
    print("═" * width)
    print()

    # Show result messages first (pause display)
    if result == "correct":
        print("\n" * 4)
        print("                 ✅ Correct! ✅".center(width))
        print("\n" * 4)
        print("═" * width)
        return
    elif result == "incorrect":
        print("\n" * 4)
        print("                 ❌ Incorrect! ❌".center(width))
        print("\n" * 4)
        print("═" * width)
        return

    RED = "\033[31m"
    RESET = "\033[0m"
    # Normal frame display
    for pos_index, word in enumerate(current_words):
        # Determine row for fish: 0 = up, 1 = middle, 2 = down
        row = pos_index
        if (row == 0 and fish_position == "up") or (row == 1 and fish_position == "middle") or (row == 2 and fish_position == "down"):
            fish_display = f"{RED} ><{article}>{RESET}"
        else:
            fish_display = " " * len(f" ><{article}>")

        # Spaces before the word to simulate floating toward fish
        spaces_before = max(0, current_step * spaces_per_step)
        print(f"{fish_display}{' ' * spaces_before}← {word}")

    print()
    print("═" * width)
    print("Use ↑ / ↓ or W / S to move your fish")
    print("═" * width)


def draw_game_finished_screen(score, max_streak, mode, difficulty, article, new_max_streak):
    print("═" * width)
    print("><> " * 20)
    print("🏁 GAME OVER 🏁".center(width))
    print("><> " * 20)
    print()
    after_game_options(mode, article, difficulty, score, max_streak, new_max_streak)

def after_game_options(mode, article, difficulty, score, max_streak, new_max_streak):
    print("\nWhat to do next?")
    print("[1] Show feedback")
    print("[2] Show highscore")
    print("[3] Back")

    choice = input("Choose an option: ")

    while choice not in ["1", "2", "3"]:
        choice = input("Invalid Input. Please choose a number:")
    if choice == "1":
        show_feedback(mode, article, difficulty, score, max_streak, new_max_streak)
    elif choice == "2":
        show_highscores(mode, article, difficulty, score, max_streak, new_max_streak)
    else:
        game_menu()

def show_feedback(mode, article, difficulty, score, max_streak, new_max_streak):
    # Mode and difficulty info
    print(f"Mode:       {mode}".center(width))
    print(f"Difficulty: {difficulty}".center(width))
    print(f"Article:    {article}".center(width))
    print("─" * width)

    # Hints for the selected article
    print("💡 Article Hints".center(width))
    print()
    if article == "der":
        print("Hints: Strong, solid, active; usually tangible or moving things".center(width))
        print("Endings: -er, -en, -el, -ig, -ling".center(width))
        print("Categories: days, months, seasons, vehicles, tools, elements (wind, snow)".center(width))
        print("Often forces, machines, or natural elements".center(width))
    elif article == "die":
        print("Hints: Soft, flowing, collective; often qualities or groups".center(width))
        print("Endings: -e, -heit, -keit, -ung, -schaft, -ion, -tät".center(width))
        print("Categories: flowers, trees, fruits, states, abstract ideas, organizations".center(width))
        print("Often things that 'flow' or are groups/collectives".center(width))
    else:  # das
        print("Hints: Neutral, small, concrete or abstract".center(width))
        print("Endings: -chen, -lein, -ment, -um, -tum".center(width))
        print("Categories: children, small objects, metals, languages, hotels, diminutives".center(width))
        print("Often small items, materials, or abstract concepts".center(width))
    print("─" * width)

    # Score and streaks
    print(f"🏆 Score:  {score}".center(width))
    print(f"🔥 Streak: {max_streak}".center(width))
    if score < 5:
        print("💡 Tip: Use Practice Mode to improve before your next challenge!".center(width))
    if max_streak == new_max_streak:
        print("🎉 Congratulations! You reached a new maximum streak!".center(width))
    print()
    print("><> " * 20)
    print("═" * width)
    print()
    after_game_options(mode, article, difficulty, score, max_streak, new_max_streak)

def show_highscores(mode, article, difficulty, score, max_streak, new_max_streak):
    print("=" * width)
    print("><> ><> HIGHSCORES <>< <><")
    print("=" * width)
    highscore_list = []
    for name in user_data:
        highscore_list.append((user_data[name]["max_score"], name))
    highscore_list.sort(reverse = True)
    for tuple in highscore_list:
        if tuple[1] == user_name:
            print(f"\033[1m><>     {tuple[1]}: {tuple[0]}\033[0m")
        else:
            print(f"><>     {tuple[1]}: {tuple[0]}")

    print("=" * width)
    after_game_options(mode, article, difficulty, score, max_streak, new_max_streak)


def show_statistics():
    width = 80
    print("═" * width)
    print(" STATISTICS ".center(width))
    print("═" * width)
    print()

    # Ensure all keys exist to avoid KeyError
    user = user_data[user_name]
    if 'scores' not in user:
        user['scores'] = []
    if 'streaks' not in user:
        user['streaks'] = []

    # Count games played
    games_played = user.get("game_count", 0)
    max_score = user.get("max_score", 0)
    max_streak = user.get("max_streak", 0)
    avg_streak = (user.get("average_streak_sum", 0) / games_played) if games_played > 0 else 0

    print(f"Player: {user_name}")
    print(f"Games Played: {games_played}")
    print(f"Last Game Mode: {user.get('last_mode', 'N/A')}")  # optional
    print(f"Last Game Difficulty: {user.get('last_difficulty', 'N/A')}")  # optional
    print()

    print(f"🏆 High Score: {max_score}")
    print(f"🔥 Max Streak: {max_streak}")
    print(f"📊 Average Streak: {avg_streak:.2f}")
    print(f"🎯 Correct Guesses: {user.get('correct_guesses', 0)}")
    print(f"❌ Incorrect Guesses: {user.get('incorrect_guesses', 0)}")
    print()

    print("Hints:")
    print("- Focus on words you often miss to improve.")
    print("- Practice mode does not affect high score.")
    print()

    print("═" * width)
    print()
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

def show_rules():
    print("═" * width)
    print("><> ><> GAME RULES ><> ><> ".center(width))
    print("Learn how to play and improve your German articles!".center(width))
    print("═" * width)
    print()

    print("🐟 Objective:")
    print("Your goal is to guide your fish to the correct German article word ('der', 'die', 'das') as it floats across the screen.")
    print("Collect points for each correct choice and maintain a streak to increase your score!")
    print()

    print("🐠 Controls:")
    print("Use W / ↑ arrow to move the fish UP")
    print("Use S / ↓ arrow to move the fish DOWN")
    print("Position your fish to catch the correct word before it reaches the end of the screen.")
    print()

    print("🏆 Scoring:")
    print("- Correct word: +1 point")
    print("- Streaks increase your bonus score")
    print("- Incorrect word: lose a life (except in Practice Mode)")
    print("- Maximum streak and high score are tracked for each player")
    print()

    print("💡 Modes:")
    print("- Normal: Standard gameplay with lives and score")
    print("- Practice: No lives lost, perfect for training")
    print("- Repetition: Focuses on words you previously got wrong to improve retention")
    print()

    print("⏱ Timer:")
    print("Each game lasts 60 seconds. Try to catch as many correct words as possible in the time limit!")
    print()

    print("Good luck, have fun, and swim wisely! 🐟🐠")
    print("═" * width)
    print()
    game_menu()
start()