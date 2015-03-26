#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 7 Pig"""


import random
import argparse
import sys
import time


parser = argparse.ArgumentParser()
parser.add_argument('--player1', help='human or computer')
parser.add_argument('--player2', help='human or computer')
parser.add_argument('--timed', help='60sec timer')
args = parser.parse_args()


class Dice(object):
    def __init__(self, sides=6):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)


class Player(object):
    def __init__(self):
        self.score = 0
        self.name = 'Player'

    def addToScore(self, amount):
        self.score += amount

    def ask(self):
        pass


class Computer(Player):
    def __init__(self):
        super(Computer, self).__init__()
        self.name = 'Computer'

    def ask(self, turnScore):
        '''Computer decision engine executed when a human
        would be asked to roll/hold'''
        y = 100 - self.score
        if y < 20:
            compare = y
        else:
            compare = 20

        if turnScore > compare:
            return "h"
        else:
            return "r"


class Human(Player):
    def __init__(self):
        super(Human, self).__init__()
        # self.name = 'Player'

    def ask(self, turnScore):
        '''User input to decide whether to roll or hold. Returns T/F'''

        print '---' + self.name + '---'
        choice = raw_input("Do you want to roll or hold? (r/h): ")
        while choice.lower()[0] != 'r' and choice.lower()[0] != 'h':
            print "Sorry, I don't understand."
            choice = raw_input("Do you want to roll or hold? (r/h): ")
        else:
            return choice


class PlayerFactory(object):

    def getPlayer(self, kind):
        if kind[0].lower() == 'c':
            return Computer()
        if kind[0].lower() == 'h':
            return Human()


# class TimedGameProxy(Game):
#     def __init__(self):
#         self.start = time.time()

#     def gameTimer(self):
#         currTime = time.time()

#         if currTime - self.start >= 60:
            



class Game(object):
    def __init__(self):
        self.playerIdx = 0
        self.turnScore = 0
        self.players = []
        self.dice = Dice()
        fac = PlayerFactory()

        player=fac.getPlayer(args.player1)
        player.name = '#1: ' + player.name
        self.players.append(player)

        player=fac.getPlayer(args.player2)
        player.name = '#2: ' + player.name
        self.players.append(player)

        self.currentPlayer = self.players[self.playerIdx]


    def ask(self):
        choice = self.currentPlayer.ask(self.turnScore)
        if choice == 'r':
            return True
        elif choice == 'h':
            return False


    def maxScore(self):
        '''Keeps track of the highest score, updates accordingly'''

        maxScore = 0
        for player in self.players:
            if (player.score > maxScore):
                maxScore = player.score
        return maxScore


    def changePlayer(self):
        self.playerIdx = (self.playerIdx + 1) % 2
        self.turnScore = 0
        self.currentPlayer = self.players[self.playerIdx]


    def turn(self):
        '''Simulates when the dice is rolled (or not)'''

        rolled = self.dice.roll()
        print '\n' + self.currentPlayer.name + ', you rolled ' + str(rolled)
        if rolled == 1:
            print 'You rolled a 1 so your turn is over. You lost ' + \
                str(self.turnScore) + ' possible points.'
            print 'Your current score is ' + str(self.currentPlayer.score) + \
            '\n'
            self.changePlayer()
            print 'Next up: ' + self.currentPlayer.name
        else:
            self.turnScore += rolled
            print 'Your score this turn is ' + str(self.turnScore)
            print 'Your overall saved score is ' + \
            str(self.currentPlayer.score) + '\n'


    def addToScore(self):
        self.currentPlayer.addToScore(self.turnScore)


def main():
    player1 = args.player1
    player2 = args.player2
    timed = args.timed
    game = Game()

    print 'Up first is ' + game.currentPlayer.name
    if timed == 'y':

        while game.maxScore() < 100:
            if game.ask():
                game.turn()
            else:
                game.addToScore()
                if game.currentPlayer.score >= 100:
                    break

                print'You decided to keep {0}\n'.format(game.currentPlayer.score)
                game.changePlayer()
                print 'Next up: ' + game.currentPlayer.name

        print('''\n*******************
            \n{0} wins with a score of {1}
            \n*******************'''.format(
            game.currentPlayer.name, game.currentPlayer.score))
        sys.exit()

main()