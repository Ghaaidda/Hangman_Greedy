import random

def calculate_scores(word_list, guessed_chars, pattern):
    """
    calculates scores for each character
    based on the possible remaining words.
    """
    scores = {c: 0 for c in "abcdefghijklmnopqrstuvwxyz" if c not in guessed_chars}

    #filter words based on the pattern
    possible_words = []
    for word in word_list:
        if len(word) != len(pattern):
            continue

        match = True
        for p, w in zip(pattern, word):
            if p != "_" and p != w:
                match = False
                break
            if p == "_" and w in guessed_chars:  
                match = False
                break

        if match:
            possible_words.append(word)

    #count letter frequency 
    for word in possible_words:
        for char in scores:
            scores[char] += word.count(char)

    return scores


def greedy_guess(word_list, guessed_chars, pattern):
    """
    choose the best next guess based on a greedy strategy.
    """
    scores = calculate_scores(word_list, guessed_chars, pattern)
    if not scores:
        return None
    return max(scores, key=scores.get)


def hangman_ai(word_list):
    """
    play hangman game.
    """
    while True:
        word = random.choice(word_list)
        guessed_chars = set()
        attempts_left = 6
        guessed_word = ['_' for _ in word]

        print("--------------Start--------------")
        print("Word:", " ".join(guessed_word))

        while attempts_left > 0 and "_" in guessed_word:

            print("\nAttempts left:", attempts_left)
            print("Guessed letters:", ", ".join(sorted(guessed_chars)))

            # AI chooses the letter
            guess = greedy_guess(word_list, guessed_chars, guessed_word)
            if guess is None:
                print("AI has no clue. Random pick.")
                guess = random.choice([c for c in "abcdefghijklmnopqrstuvwxyz" if c not in guessed_chars])

            print("AI guesses:", guess)

            guessed_chars.add(guess)

            if guess in word:
                print("Correct!")
                for i, letter in enumerate(word):
                    if letter == guess:
                        guessed_word[i] = guess
            else:
                print("Incorrect!")
                attempts_left -= 1

            print("Word:", " ".join(guessed_word))

            # ASCII Art
            print("\n   --------    ")
            print("   |      |    ")
            print("   |      " + ("O" if attempts_left < 6 else ""))
            print("   |     " + ("/" if attempts_left < 5 else " ") + ("|" if attempts_left < 4 else "") + ("\\" if attempts_left < 3 else ""))
            print("   |     " + ("/ " if attempts_left < 2 else "") + ("\\" if attempts_left < 1 else ""))
            print("  ---          ")

        if "_" not in guessed_word:
            print("\nAI WON! The word was:", word)
        else:
            print("\nAI LOST! The word was:", word)

        play_again = input("\nPlay again? (1 = yes, 0 = no): ")
        if play_again != '1':
            break


# Load words
word_list = []
with open("words.txt", "r") as fh:
    for line in fh:
        word_list.append(line.strip())

hangman_ai(word_list)
