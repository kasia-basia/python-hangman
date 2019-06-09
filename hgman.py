from random import randrange
from os import system, name
import json
import time
from img import hangman_img

import re

class Hangman:
    def __init__(self):
        self.clear_screen()
        self.name = input('Hello, what\'s your name? \n => ')
        self.lang = Hangman.select_language(self, None)
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

    def select_language(self, lang):
        if lang is None:
            self.clear_screen()
            lang = input(f'Nice to meet you, {self.name.capitalize()}! '
                         f'What language do you want to play in? Type PL or EN. \n => ')
        if lang.upper() in ['EN', 'PL']:
            return lang.upper()
        else:
            self.clear_screen()
            lang = input('Type "EN" or "PL" for English or Polish. Other languages currently not supported. \n => ')
            self.select_language(lang)

    def get_words_list(self):
        with open('words.json') as json_file:
            data = json.load(json_file)[f'randomWords{self.lang}']
            return data

    def select_random_word(self):
        index = randrange(0, len(self.random_words_list))
        return self.random_words_list[index]

    def intro(self):
        self.clear_screen()
        print(f'Ok, let\'s begin. Here\'s your word:\n{self.show_guessed_letters()}')

    def is_already_guessed(self, letter):
        if letter in self.all_letters_guessed:
            print(f'You already tried that! \n{self.show_guessed_letters()}')
            self.guess()
        self.all_letters_guessed.append(letter)

    def is_valid_character(self, letter):
        if len(letter) != 1:
            print(f'Only one character at a time, please! \n{self.show_guessed_letters()}')
            self.guess()
        if letter == ' ':
            print('Please type something')
            self.guess()

    def is_game_over(self):
        if self.show_guessed_letters().replace(' ', '') == self.current_word:
            print(f'You got it. Congratulations!')
            return True
        if len(self.incorrect_answers) >= self.permitted_errors:
            print(f'You lost! The word was "{self.current_word}."')
            return True

    def show_guessed_letters(self):
        result = ''
        for l in self.current_word:
            if l in self.all_letters_guessed:
                result += f'{l} '
            else:
                result += '_ '
        return result

    def show_hangman(self):
        print(hangman_img[len(self.incorrect_answers)])

    def guess(self):
        letter = input('\n=> ')
        self.clear_screen()
        self.is_valid_character(letter)
        self.is_already_guessed(letter)

        if letter in self.current_word:
            print(f'\033[92mYay! {letter.capitalize()} is correct!\033[0m')
        else:
            self.incorrect_answers.append(letter)
            print(f'\033[93mNope, {letter.capitalize()} is not a correct answer.\033[0m')

        print(self.show_guessed_letters())

        if not self.is_game_over():
            self.guess()


game = Hangman()
