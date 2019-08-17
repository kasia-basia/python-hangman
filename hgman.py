from random import randrange
from os import system, name
import json
from img import hangman_img
import re


class Hangman:
    def __init__(self):
        self.clear_screen()
        self.name = input('Hello, what\'s your name? \n => ').capitalize() or 'Anonymous'
        self.lang = Hangman.select_language(self)
        self.random_words_list = Hangman.get_words_list(self)
        self.current_word = Hangman.select_random_word(self)
        self.intro()
        self.guess()

    permitted_errors = 10
    all_letters_guessed = []
    incorrect_answers = []

    @staticmethod
    def clear_screen():
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def select_language(self):
        self.clear_screen()
        lang = input(f'Nice to meet you, {self.name}! '
                     f'What language do you want to play in? Type PL or EN. \n => ')
        while lang.upper() not in ['PL', 'EN']:
            self.clear_screen()
            lang = input('Type "EN" or "PL" for English or Polish. '
                         'Other languages not supported. \n => ')
        return lang.upper()

    def get_words_list(self):
        with open('words.json', encoding='utf-8') as json_file:
            data = json.load(json_file)[f'{self.lang}']
            return data

    def select_random_word(self):
        index = randrange(0, len(self.random_words_list))
        return self.random_words_list[index]

    def intro(self):
        self.clear_screen()
        print(f'Ok, let\'s begin. Here\'s your word:\n')
        self.show_data()

    def is_already_guessed(self, letter):
        if letter in self.all_letters_guessed:
            print(f'You already tried that!\n')
            self.show_data()
            self.guess()
        self.all_letters_guessed.append(letter)

    def is_valid_character(self, letter):
        if not re.match('^[A-Za-zÀ-ž]$', letter):
            print(f'Insert a single letter\n')
            self.show_data()
            self.guess()

    def show_guessed_letters(self):
        result = ''
        for l in self.current_word:
            if l in self.all_letters_guessed:
                result += f'{l} '
            else:
                result += '_ '
        return result

    def show_hangman(self):
        try:
            print(hangman_img[len(self.incorrect_answers)])
        except IndexError:
            print(hangman_img[-1])

    def show_incorrect_answers(self):
        result = ''
        for l in self.incorrect_answers:
            result += f'{l} '
        print(f'\033[91m{result}\033[0m')

    def show_data(self):
        print(self.show_guessed_letters() or ' ')
        self.show_hangman()
        self.show_incorrect_answers()

    def is_game_over(self):
        if self.show_guessed_letters().replace(' ', '') == self.current_word:
            print(f'\033[92mYou got it. Congratulations, {self.name}!\033[0m')
            return True
        if len(self.incorrect_answers) >= self.permitted_errors:
            print(f'\033[93mYou lost, {self.name}! The word was "{self.current_word}."\033[0m')
            return True

    def guess(self):
        letter = input('\n=> ').replace(' ', '').lower()
        self.clear_screen()
        self.is_valid_character(letter)
        self.is_already_guessed(letter)

        if letter in self.current_word:
            print(f'\033[92mYay! {letter.capitalize()} is correct!\033[0m\n')
        else:
            self.incorrect_answers.append(letter)
            print(f'\033[93mNope, {letter.capitalize()} is not a correct answer.\033[0m\n')

        self.show_data()

        if not self.is_game_over():
            self.guess()
        else:
            exit()


game = Hangman()
