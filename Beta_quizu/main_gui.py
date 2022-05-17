# -*- coding: utf-8 -*-

import pygame
import os
import random
import json
import time
import numpy as np

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Array
import multiprocessing as mp

from signal_processing import SignalProcess

pygame.init()


class GUI:
    def __init__(self, lock, queue):
        """_summary_
        """

        self.path = os.path.dirname(__file__)
        # self.clock = 0 mozna wywalic i guess ale jeszcze nie jestem pewna
        self.level = 0
        self.correct = True
        self.close = False
        self.color = (169, 169, 169)
        self.font = "Comic Sans MS"
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.window.get_width()
        self.height = self.window.get_height()
        self.backgnd_path = "tlo_nowe.png"
        self.fish_path = "rybcia.png"
        self.fish = pygame.image.load(os.path.join(self.path, self.fish_path))
        # sygnały
        self.__queue = queue
        self._rms = RMS(lock)
        self._move_ticks = 8
        self._confirm_ticks = 20
        # calibration properties
        self._left_clbr = 10000
        self._right_clbr = 10000

    def question(self, que, ans, corr, award):
        """_summary_

        Args:
            que (_type_): _description_
            ans (_type_): _description_
            corr (_type_): _description_
            award (str): text describing current award.
        """
        self.button_size = (0.6 * self.width, 0.08 * self.height)

        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, self.backgnd_path))

        color = (169, 169, 169)

        # zmienna, ktora oznacza wybrana odp; default = 0
        chosen = 0
        confirm_ctr = 0
        move_ctr = 0
        while self.run:
            score_text = pygame.font.Font.render(pygame.font.SysFont(self.font, 40),
                                                 award, True, (0, 0, 0))

            score_text_centr = ((self.width - score_text.get_width()) / 2, self.height * 0.0001)

            QUESTION = pygame.font.Font.render(pygame.font.SysFont(self.font, 30),
                                               que, True, (0, 0, 0))
            que_placement = QUESTION.get_rect(center=(self.width * 0.4, self.height * 0.3))

            ANS1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 32),
                                           ans[0], True, (0, 0, 0))
            ANS2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 32),
                                           ans[1], True, (0, 0, 0))
            ANS3 = pygame.font.Font.render(pygame.font.SysFont(self.font, 32),
                                           ans[2], True, (0, 0, 0))
            ANS4 = pygame.font.Font.render(pygame.font.SysFont(self.font, 32),
                                           ans[3], True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.close = True
                    self.__kill()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        chosen += 1
                    elif event.key == pygame.K_ESCAPE:
                        self.run = False
                        self.close = True
                        self.__kill()

            # sterowanie mięśniami
            if self._rms.left > self._left_clbr:
                if move_ctr > self._move_ticks:
                    chosen += 1
                    time.sleep(0.2)
                move_ctr += 1
            else:
                move_ctr = 0

            chosen = chosen % 4

            button_location = [(self.width / 10, self.height / 2),
                               (self.width / 10, self.height / 2 + 1.2 * self.button_size[1]),
                               (self.width / 10, self.height / 2 + 2.4 * self.button_size[1]),
                               (self.width / 10, self.height / 2 + 3.6 * self.button_size[1])]

            # rysowanie:
            # najpierw swiat
            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła
            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect(0, 0, self.width, self.height / 15))  # prostokąt na górze

            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect((self.width / 10, self.height / 5),
                                         (self.width * 0.6, self.height * 0.2)),
                             border_radius=15)  # rysowanie pola na pytanie

            # zaznaczamy szarym wybraną opcję
            pygame.draw.rect(self.window, (169, 169, 169),
                             pygame.Rect(button_location[chosen], self.button_size),
                             border_radius=15)

            # czy wybrana odpowiedz jest poprawna?
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if chosen == corr:
                            color = (0, 128, 0)  # oznaczanie na zielono poprawnej odpowiedzi
                            self.run = False
                        else:
                            color = (255, 0, 0)  # oznaczanie na czerwono blednej odpoweidzi
                            self.run = False
                            self.correct = False

            if self._rms.right > self._right_clbr:
                color = (130, 130, 130)
                if confirm_ctr > self._confirm_ticks:
                    if chosen == corr:
                        color = (0, 128, 0)
                        self.run = False
                    else:
                        color = (255, 0, 0)
                        self.run = False
                        self.correct = False

                confirm_ctr += 1

            else:
                confirm_ctr = 0
                color = (169, 169, 169)

            # rysowanie okienka w nowym kolorze w zaleznosci od poprawnosci odpowiedzi
            pygame.draw.rect(self.window, color,
                             pygame.Rect(button_location[chosen], self.button_size),
                             border_radius=15)

            button_location_copy = button_location.copy()
            button_location_copy.pop(chosen)
            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect(button_location_copy[0], self.button_size),
                             border_radius=15)

            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect(button_location_copy[1], self.button_size),
                             border_radius=15)

            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect(button_location_copy[2], self.button_size),
                             border_radius=15)

            ans_location = [(self.width / 9 + 0.015 * self.button_size[0],
                             button_location[0][1] + self.button_size[1] / 2),
                            (self.width / 9 + 0.015 * self.button_size[0],
                             button_location[1][1] + self.button_size[1] / 2),
                            (self.width / 9 + 0.015 * self.button_size[0],
                             button_location[2][1] + self.button_size[1] / 2),
                            (self.width / 9 + 0.015 * self.button_size[0],
                             button_location[3][1] + self.button_size[1] / 2)]

            # wpisywanie odpowiedzi w butony
            self.window.blit(ANS1, ANS1.get_rect(midleft=(ans_location[0][0],
                                                          ans_location[0][1])))
            self.window.blit(ANS2, ANS2.get_rect(midleft=(ans_location[1][0],
                                                          ans_location[1][1])))
            self.window.blit(ANS3, ANS3.get_rect(midleft=(ans_location[2][0],
                                                          ans_location[2][1])))
            self.window.blit(ANS4, ANS4.get_rect(midleft=(ans_location[3][0],
                                                          ans_location[3][1])))

            fish_placement = (3 * self.width / 4, self.height / 15)
            self.window.blit(self.fish, fish_placement)

            self.window.blit(QUESTION, que_placement)
            self.window.blit(score_text, score_text_centr)  # rysowanie okienka z wynikiem
            pygame.display.update()
        time.sleep(1)

    def keep_playing(self, awards, score):

        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, self.backgnd_path))
        self.button_size = (1000, 80)

        que = u'Przejść do kolejnego etapu?'
        ans = [u'Tak, gram dalej',
               u'Nie, rezygnuję i zabieram kwotę gwarantowaną ({} zł)'.format(int(awards[score]))]
        corr = 0
        chosen = 0
        color = (169, 169, 169)
        move_ctr = 0
        confirm_ctr = 0
        while self.run:
            score_text = pygame.font.Font.render(pygame.font.SysFont(self.font, 40),
                                                 u'Aktualna nagroda: {} zł'.format(
                                                     str(int(awards[score]))),
                                                 True, (0, 0, 0))
            score_text_centr = ((self.width - score_text.get_width()) / 2, self.height * 0.0001)
            QUESTION = pygame.font.Font.render(pygame.font.SysFont(self.font, 48), que, True, (
                0, 0, 0))

            ANS1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 32),
                                           ans[0], True, (0, 0, 0))
            ANS2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 32),
                                           ans[1], True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.close = True
                    self.__kill()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        chosen += 1
                    elif event.key == pygame.K_ESCAPE:
                        self.run = False
                        self.close = True
                        self.__kill()

            # sterowanie mięśniami
            if self._rms.left > self._left_clbr:
                if move_ctr > self._move_ticks:
                    chosen += 1
                    time.sleep(0.25)
                move_ctr += 1
            else:
                move_ctr = 0

            if chosen > 1:
                chosen = 0

            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła

            # prostokąt na górze
            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect((self.width / 10, self.height / 5),
                                         (self.width * 0.6, self.height * 0.2)),
                             border_radius=15)

            button_location = [(125, 450), (125, 550)]

            pygame.draw.rect(self.window, (169, 169, 169),
                             pygame.Rect(button_location[chosen], self.button_size), border_radius=15)

            # czy wybrana odpowiedz jest poprawna?
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if chosen == corr:
                            color = (0, 128, 0)
                            self.run = False
                        else:
                            color = (255, 0, 0)
                            self.run = False
                            self.close = True
                            self.__kill()
                            break

            if self._rms.right > self._right_clbr:
                color = (130, 130, 130)
                if confirm_ctr > self._confirm_ticks:
                    if chosen == corr:
                        color = (0, 128, 0)
                        self.run = False
                    else:
                        color = (255, 0, 0)
                        self.run = False
                        self.correct = False
                        break
                confirm_ctr += 1

            else:
                confirm_ctr = 0
                color = (169, 169, 169)

            ans_location = [
                (button_location[0][0] + 0.015 * self.button_size[0], button_location[0][1] + self.button_size[1] / 2),
                (button_location[0][0] + 0.015 * self.button_size[0], button_location[1][1] + self.button_size[1] / 2)]

            pygame.draw.rect(self.window, color,
                             pygame.Rect(button_location[chosen], self.button_size),
                             border_radius=15)

            button_location.pop(chosen)

            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect(button_location[0], self.button_size),
                             border_radius=15)

            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect((self.width / 10, self.height / 5),
                                         (self.width * 0.6, self.height * 0.2)),
                             border_radius=15)  # rysowanie pola na pytanie

            fish_placement = (3 * self.width / 4, self.height / 15)
            self.window.blit(self.fish, fish_placement)

            self.window.blit(ANS1, ANS1.get_rect(midleft=(ans_location[0][0], ans_location[0][1])))
            self.window.blit(ANS2, ANS2.get_rect(midleft=(ans_location[1][0], ans_location[1][1])))
            self.window.blit(QUESTION, QUESTION.get_rect(center=(625, 275)))
            self.window.blit(score_text, score_text_centr)

            pygame.display.update()
        time.sleep(1)

    def ending(self, display):
        """
        Ending screen.

        Args:
            # display (str): text displayed as final message to the fucking stupid cunt playing. // Why so toxic?
        """

        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, self.backgnd_path))

        while self.run:
            text = pygame.font.Font.render(pygame.font.SysFont(self.font, 40), display, True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    # self.__kill()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                        self.close = True
                        self.__kill()

            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 1000, 150), border_radius=15)
            self.window.blit(text, text.get_rect(center=(650, 275)))

            fish_placement = (3 * self.width / 4, self.height / 15)
            self.window.blit(self.fish, fish_placement)

            pygame.display.update()

    def menu(self):
        """
        Displaying meny and choosing the level.

        Returns:
            int: nuneric representation of difficulty level

        """

        button_height = self.height / 12  # wielokrotność rozdzielczości
        button_width = self.width * 0.6
        button_pos_x = self.width / 10
        button_pos_y = self.height / 2
        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, self.backgnd_path))
        self.button_size = (button_width, button_height)

        color = (169, 169, 169)
        chosen = 0

        que = u'Jesteś gotowy? Wybierz poziom'
        ans = [u'Poziom 1: wiek 7 - 12', u'Poziom 2: wiek 13 - 18', u'Poziom 3: dorośli']

        confirm_ctr = 0
        move_ctr = 0
        while self.run:
            QUESTION = pygame.font.Font.render(pygame.font.SysFont(self.font, 50), que, True, (0, 0, 0))
            ANS1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 38), ans[0], True, (0, 0, 0))
            ANS2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 38), ans[1], True, (0, 0, 0))
            ANS3 = pygame.font.Font.render(pygame.font.SysFont(self.font, 38), ans[2], True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.close = True
                    self.__kill()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        chosen += 1
                    elif event.key == pygame.K_SPACE:
                        self.level = chosen
                        color = (0, 128, 0)
                        self.run = False
                    elif event.key == pygame.K_ESCAPE:
                        self.run = False
                        self.close = True
                        self.__kill()

            # sterowanie mięśniami
            if self._rms.left > self._left_clbr:
                if move_ctr > self._move_ticks:
                    chosen += 1
                    time.sleep(0.18)
                move_ctr += 1
            else:
                move_ctr = 0

            chosen = chosen % 3

            if self._rms.right > self._right_clbr:
                color = (130, 130, 130)
                if confirm_ctr > self._confirm_ticks:
                    self.level = chosen
                    color = (0, 128, 0)
                    self.run = False
                confirm_ctr += 1

            else:
                confirm_ctr = 0
                color = (169, 169, 169)

            button_location = [(button_pos_x, button_pos_y),
                               (button_pos_x, button_pos_y + 1.2 * button_height),
                               (button_pos_x, button_pos_y + 2.4 * button_height)]
            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła

            # rysowanie wybranego guzika
            pygame.draw.rect(self.window, color,
                             pygame.Rect(button_location[chosen], self.button_size),
                             border_radius=15)
            pygame.draw.rect(self.window, color, pygame.Rect(button_location[chosen], self.button_size),
                             border_radius=15)

            # guzik pod pytanie
            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect((self.width / 10, self.height / 5),
                                         (self.width * 0.6, self.height * 0.2)),
                             border_radius=15)  # rysowanie pola na pytanie

            button_location.pop(chosen)
            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect(button_location[0], self.button_size),
                             border_radius=15)

            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect(button_location[1], self.button_size),
                             border_radius=15)

            ans_location = [(self.width / 9 + 0.015 * button_pos_x,
                             button_pos_y + button_height / 2),
                            (self.width / 9 + 0.015 * button_pos_x,
                             button_pos_y + button_height / 2 + 1.2 * button_height),
                            (self.width / 9 + 0.015 * button_pos_x,
                             button_pos_y + button_height / 2 + 2.4 * button_height)]

            fish_placement = (3 * self.width / 4, self.height / 15)
            self.window.blit(self.fish, fish_placement)

            self.window.blit(ANS1, ANS1.get_rect(midleft=(ans_location[0][0], ans_location[0][1])))
            self.window.blit(ANS2, ANS2.get_rect(midleft=(ans_location[1][0], ans_location[1][1])))
            self.window.blit(ANS3, ANS3.get_rect(midleft=(ans_location[2][0], ans_location[2][1])))
            self.window.blit(QUESTION, QUESTION.get_rect(center=(self.width * 0.4, self.height * 0.3)))
            pygame.display.update()
        time.sleep(1)

        return self.level

    def correctAnswer(self):
        '''
        Displaying screen after choosing the correct answer

        Returns:
             Nothing
        '''

        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, self.backgnd_path))
        self.button_size = (950, 80)

        display_text1 = u'Poprawna odpowiedź!'
        display_text2 = u'Ściśnij prawą ręke, by kontynuować'

        confirm_ctr = 0
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.close = True
                    self.__kill()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.run = False
                    elif event.key == pygame.K_ESCAPE:
                        self.run = False
                        self.close = True
                        self.__kill()

            # sterowanie mięśniami
            if self._rms.right > self._right_clbr:
                if confirm_ctr > self._confirm_ticks - 15:
                    self.run = False
                    confirm_ctr = 0
                confirm_ctr += 1
            else:
                confirm_ctr = 0

            display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48), display_text1, True, (0, 0, 0))
            display2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 20), display_text2, True, (0, 0, 0))

            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 950, 150), border_radius=15)

            fish_placement = (3 * self.width / 4, self.height / 15)
            self.window.blit(self.fish, fish_placement)

            self.window.blit(display1, (200, 235))
            self.window.blit(display2, (200, 300))

            pygame.display.update()
        time.sleep(1)

    def calibration(self):
        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, self.backgnd_path))
        # palm_hand = pygame.image.load(os.path.join(self.path, self.backgnd_path))
        # tight_hand = pygame.image.load(os.path.join(self.path, self.backgnd_path))
        start_display_text = [u'Kalibracja zaraz się rozpocznie.',
                              u'Postępuj zgodnie z instrukcjami na ekranie']

        calib_display_text = [u'Rozluźnij ręce',
                              u'Zaciśnij lewą rękę',
                              u'Rozluźnij lewą rękę',
                              u'Zaciśnij prawą rękę',
                              u'Rozluźnij prawą rękę']

        end_display_text = [u'Dziękujemy.',
                            u'Za chwilę rozpocznie się gra']

        display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                           "", True, (0, 0, 0))
        display2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                           "", True, (0, 0, 0))
        st_time = time.time()
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.close = True
                    self.__kill()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.run = False
                    elif event.key == pygame.K_ESCAPE:
                        self.run = False
                        self.close = True
                        self.__kill()

            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła

            pygame.draw.rect(self.window, (255, 255, 255),
                             pygame.Rect((self.width / 10, self.height / 5),
                                         (self.width * 0.6, self.height * 0.2)),
                             border_radius=15)  # rysowanie pola na pytanie

            if time.time() - st_time < 8:
                display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   start_display_text[0], True, (0, 0, 0))
                display2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   start_display_text[1], True, (0, 0, 0))

            elif time.time() - st_time < 13:
                display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   calib_display_text[0], True, (0, 0, 0))
                display2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   "", True, (0, 0, 0))
                # self.window.blit(palm_hand, (0, 0))

            elif time.time() - st_time < 18:
                display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   calib_display_text[1], True, (0, 0, 0))
                # self.window.blit(tight_hand, (0, 0))
                self._left_clbr = self._rms.calibration("left")

            elif time.time() - st_time < 23:
                display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   calib_display_text[2], True, (0, 0, 0))
                # self.window.blit(palm_hand, (0, 0))

            elif time.time() - st_time < 28:
                display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   calib_display_text[3], True, (0, 0, 0))
                # self.window.blit(tight_hand, (0, 0))
                self._right_clbr = self._rms.calibration("right")

            elif time.time() - st_time < 33:
                display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   calib_display_text[4], True, (0, 0, 0))
                # self.window.blit(palm_hand, (0, 0))

            elif time.time() - st_time < 38:
                display1 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   end_display_text[0], True, (0, 0, 0))
                display2 = pygame.font.Font.render(pygame.font.SysFont(self.font, 48),
                                                   end_display_text[1], True, (0, 0, 0))

            else:
                self.run = False

            fish_placement = (3 * self.width / 4, self.height / 15)
            self.window.blit(self.fish, fish_placement)

            self.window.blit(display1, (200, 235))
            self.window.blit(display2, (200, 300))

            pygame.display.update()

    def __kill(self):
        self.__queue.put(1)
        pygame.quit()
        exit()


class Logic:

    def __init__(self, files):
        """Reads questions.

        Args:
            files (list): list of files names. Each file correspond to another lv. of difficulty in increasing order.
        """

        self._path = os.path.dirname(__file__)
        self._files = [os.path.join(self._path, e) for e in
                       files]  # ścieżka do pliku z pytaniami: łatwe, średnie, trudne
        self._questions = []
        self._answers = []
        self._correct = []

        for e in self._files:
            with open(e, encoding='utf-8') as f:
                temp = json.load(f)  # wczytanie pliku z pytaniami
            self._questions.append(temp['question'])  # dzielimy temp na pytania
            self._answers.append(temp['options'])  # odpowiedzi
            self._correct.append(temp['answer'])  # poprawne odpowiedzi

    def drawQuestions(self, n):
        """draw 3 random questions for each category.

        Args:
            n (int): number of questions in each round.

        Returns:
            list, list, list: chosen questions, answers and correct answers.
        """
        chosenQuestions = [[] for _ in range(len(self._files))]
        chosenAnswers = [[] for _ in range(len(self._files))]
        chosenCorrect = [[] for _ in range(len(self._files))]
        for i in range(n):
            lengths = list(range(0, len(self.questions[i])))  # indeksy dla danego zbioru pytań
            chosen = random.sample(lengths, 3)  # losujemy indeksy pytań
            chosenQuestions[i] = [self.questions[i][k] for k in chosen]
            chosenAnswers[i] = [self.answers[i][k] for k in chosen]
            chosenCorrect[i] = [self.correct[i][k] for k in chosen]

        return chosenQuestions, chosenAnswers, chosenCorrect

    @property
    def questions(self):
        return self._questions

    @property
    def answers(self):
        return self._answers

    @property
    def correct(self):
        return self._correct


class RMS:
    _L_RMS_TIME = 0.25
    _R_RMS_TIME = 1
    _BUF_LEN = 128
    _SAMPLING_RATE = 512

    def __init__(self, lock):
        self._left_hand = Array('d', np.zeros(self._BUF_LEN * 2))
        self._right_hand = Array('d', np.zeros(self._BUF_LEN * 2))
        self._lock = lock
        signals = SignalProcess()
        amplifier_process = Process(target=signals.start,
                                    args=(self._lock,
                                          self._left_hand,
                                          self._right_hand))
        amplifier_process.start()

    @property
    def left(self):
        self._lock.acquire()
        norm_sig = self._left_hand - np.mean(self._left_hand)
        self._lock.release()
        print("rms lewa: ", np.sqrt(np.sum(norm_sig ** 2)))
        return np.sqrt(np.sum(norm_sig ** 2))

    @property
    def right(self):
        self._lock.acquire()
        norm_sig = self._right_hand - np.mean(self._right_hand)
        self._lock.release()
        print("rms prawa: ", np.sqrt(np.sum(norm_sig ** 2)))
        return np.sqrt(np.sum(norm_sig ** 2))

    def calibration(self, hand, calibration_time=5):
        hands_signal = {"left": self.left,
                        "right": self.right}

        rms = 0
        rms_ctr = 0
        rms_samples = calibration_time * self._SAMPLING_RATE / self._BUF_LEN
        while rms_ctr < rms_samples:
            rms += hands_signal[hand]
            rms_ctr += 1

        return rms / rms_ctr


class Quiz:

    def __init__(self, files, lock, queue):
        """Prepares quiz and draws questions.

        Args:
            files (list): list of files names.
            Each file correspond to another lv. of difficulty in increasing order.
            Files in the same folder.
        """

        self._rounds = 3  # liczba rund
        self._questionsInRounds = 3  # liczba pytań w każdej rundzie
        self._awards = [0, 1e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]  # wartości nagród za kolejne etapy
        self._score = 0  # na początku mamy 0 punktów
        self._maxScore = self._rounds * self._questionsInRounds
        self._gui = GUI(lock, queue)  # tworzymy gui
        self._files = files

    def quiz(self):
        """ Starts the game.
        """
        self._gui.calibration()
        level = self._gui.menu()  # otwieramy menu i wybieramy poziom trudności
        if level == 0:  # najłatwiejsze
            self._logic = Logic(self._files[0:3])  # tworzymy logikę
        elif level == 1:  # średnie
            self._logic = Logic(self._files[1:4])
        elif level == 2:  # trudne
            self._logic = Logic(self._files[2:5])
        self._questions, self._answers, self._correct = self._logic.drawQuestions(
            self._questionsInRounds)  # losujemy pytania
        if not self._gui.close:
            for i in range(self._maxScore):  # quiz ma 9 pytań/rund
                q = self._questions[i // self._rounds][i % self._questionsInRounds]  # po 3 łatwe, średnie, trudne
                a = self._answers[i // self._rounds][i % self._questionsInRounds]
                c = self._correct[i // self._rounds][i % self._questionsInRounds]
                r = 'Aktualna nagroda: {} zł'.format(
                    str(int(self._awards[self._score])))  # tekst jaki się wyświetla na ekranie z pytaniem
                self._gui.question(q, a, c, r)  # wyświetlamy pytanie
                if self._gui.close:  # jeśli wciskamy x to okno się zamknie
                    break
                if not self._gui.correct:  # zła odpowiedź to koniec gry
                    self._gui.ending(
                        'Zła odpowiedź! Koniec gry. Twój wynik: {} zł'.format(str(int(self._awards[self._score]))))
                    break
                if self._gui.correct and not self._gui.run:
                    self._gui.correctAnswer()
                self._score += 1  # skoro tu doszliśmy, to odpowiedź była poprawna, czyli + punkt

                if self._score % self._rounds == 0 and self._score != self._maxScore:
                    self._gui.keep_playing(self._awards, self._score)
                if self._gui.close:
                    self._gui.ending(
                        u'Dziękujemy za udział! Wygrałeś/łaś {} zł'.format(str(int(self._awards[self._score]))))
                    break

            if self._gui.correct and not self._gui.close:
                self._gui.ending(u'Wygrana! Zostajesz milionerem!!!')


# TUTAJ MAŁY PRZYKŁAD JAK TO WSZYSTKO MA DZIAŁAĆ, MNIEJ WIĘCEJ

# before this - KALIBRACJA
if __name__ == "__main__":
    process_lock = Lock()
    processes_queue = mp.Queue()  # <---
    q = Quiz(['questions_stage_1.json',
              'questions_stage_2.json',
              'questions_stage_3.json',
              'questions_stage_4.json',
              'questions_stage_5.json'],
             process_lock, processes_queue)

    game_process = Process(target=q.quiz(),
                           args=())
    game_process.start()

    # TODO
    try:
        while processes_queue.empty():
            pass
    except KeyboardInterrupt:
        processes_queue.put(1)
