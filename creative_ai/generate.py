#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import random

from pysynth import pysynth

from utils.generate_helpers import *
from utils.menu import Menu
from data.dataLoader import *
from models.musicInfo import *
from models.languageModel import LanguageModel

# FIXME Add your team name
TEAM = 'YOUR NAME HERE'
LYRICSDIRS = ['the_beatles']
TESTLYRICSDIRS = ['the_beatles_test']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

###############################################################################
# Core
###############################################################################

def generateTokenSentence(model, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']
    next_token = model.getNextToken(sentence)

    while not sentenceTooLong(desiredLength, len(sentence) - 2):

        if next_token == '$:::$':
            break

        sentence.append(next_token)
        next_token = model.getNextToken(sentence)

    return sentence[2:]

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []

    for i in range(4):
        verseOne.append(generateTokenSentence(models, 7))
        verseTwo.append(generateTokenSentence(models, 7))
        chorus.append(generateTokenSentence(models, 9))

    printSongLyrics(verseOne, verseTwo, chorus)

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  uses models to generate a song and write it to the file
              named songName.wav
    """

    verseOne = []
    verseTwo = []
    chorus = []

    for i in range(4):
        verseOne.extend(generateTokenSentence(models, 7))
        verseTwo.extend(generateTokenSentence(models, 7))
        chorus.extend(generateTokenSentence(models, 9))

    song = []
    song.extend(verseOne)
    song.extend(verseTwo)
    song.extend(chorus)
    song.extend(verseOne)
    song.extend(chorus)

    pysynth.make_wav(song, fn=songName)

###############################################################################
# Reach
###############################################################################

PROMPT = [
    'Generate song lyrics by The Beatles',
    'Generate a song using data from Nintendo Gamecube',
    'Quit the music generator'
]

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """

    mainMenu = Menu(PROMPT)

    lyricsTrained = False
    musicTrained = False

    print('Welcome to the {} music generator!'.format(TEAM))
    while True:
        userInput = mainMenu.getChoice()

        if userInput == 1:
            if not lyricsTrained:
                print('Starting lyrics generator...')
                lyricsModel = trainLyricModels(LYRICSDIRS)
                lyricsTrained = True

            runLyricsGenerator(lyricsModel)

        elif userInput == 2:
            if not musicTrained:
                print('Starting music generator...')
                musicModel = trainMusicModels(MUSICDIRS)
                musicTrained = True

            songName = input('What would you like to name your song? ')
            runMusicGenerator(musicModel, WAVDIR + songName + '.wav')

        elif userInput == 3:
            print('Thank you for using the {} music generator!'.format(TEAM))
            sys.exit()

# This is how python tells if the file is being run as main
if __name__ == '__main__':
    main()
    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!