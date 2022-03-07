import pygame
import os
import random
import json
import numpy as np

pygame.init()


class GUI:
    def __init__(self):
        """_summary_
        """
        self.path = os.path.dirname(__file__)
        # self.clock = 0 mozna wywalic i guess ale jeszcze nie jestem pewna

        self.score = 0
        self.awards = [0, 1e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]
        self.correct = True
        self.max_score = 9
        self.close = False

        self.button_size = (400, 80)

        self.color = (169, 169, 169)

    def question(self, que, ans, corr):
        """_summary_

        Args:
            que (_type_): _description_
            ans (_type_): _description_
            corr (_type_): _description_
        """

        self.window = pygame.display.set_mode((1280, 720))
        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, "sea.jpg"))

        # zmienna ktora oznacza wybrana odp; default = 0
        chosen = 0


        while self.run:
            score_text = pygame.font.Font.render(pygame.font.SysFont("calibri", 48),
                                                 'Aktualna nagroda: {} zł'.format(str(int(self.awards[self.score]))),
                                                 True, (0, 0, 0))
            QUESTION = pygame.font.Font.render(pygame.font.SysFont("calibri", 32), que, True, (
                0, 0, 0))
            ANS1 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[0], True, (0, 0, 0))
            ANS2 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[1], True, (0, 0, 0))
            ANS3 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[2], True, (0, 0, 0))
            ANS4 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[3], True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                    self.close = True  # to tak na potrzeby programu zeby sie zamykalo xd slabe rozwiazanie - do poproawy

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        chosen += 1

            chosen = chosen % 4
            button_location = [(150, 450), (150, 550), (700, 450), (700, 550)]
            # rysowanie:
            # najpierw swiat
            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła

            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 950, 150))  # rysowanie pola na pytanie
            # zaznaczamy szarym wybraną opcję
            pygame.draw.rect(self.window, (169, 169, 169), pygame.Rect(button_location[chosen], self.button_size))

            # czy wybrana odpowiedz jest poprawna?
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if chosen == corr:
                            # color = (0, 128, 0) - to bylo do zaznaczania na inny kolor kiedy poprawne - do updatu
                            self.score += 1
                            self.run = False
                        else:
                            # color = (255, 0, 0) - same co powyzej
                            self.run = False  # to pewnie trzeba zmienić na generowanie jakiegoś ekranu z napisem OJ PRZEGRAŁEŚ KUREWKO
                            self.correct = False

            pygame.draw.rect(self.window, self.color, pygame.Rect(button_location[chosen], self.button_size))

            button_location.pop(chosen)
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[0], self.button_size))
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[1], self.button_size))
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[2], self.button_size))

            # wpisywanie odpowiedzi w buttony
            self.window.blit(ANS1, (250, 470))
            self.window.blit(ANS2, (250, 570))
            self.window.blit(ANS3, (800, 470))
            self.window.blit(ANS4, (800, 570))
            self.window.blit(QUESTION, (200, 250))
            self.window.blit(score_text, (0, 0))  # rysowanie okienka z wynikiem
            pygame.display.update()



    def keep_playing(self):

        self.window = pygame.display.set_mode((1280, 720))
        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, "sea.jpg"))
        self.button_size = (1000, 80)

        que = 'Przejść do kolejnego etapu?'
        ans = ['Tak, gram dalej', 'Nie, rezygnuję i zabieram kwotę gwarantowaną']
        corr = 0
        chosen = 0
        color = (169, 169, 169)
        while self.run:
            score_text = pygame.font.Font.render(pygame.font.SysFont("calibri", 48),
                                                 'Aktualna nagroda: {} zł'.format(
                                                 str(int(self.awards[self.score]))),
                                                 True, (0, 0, 0))
            QUESTION = pygame.font.Font.render(pygame.font.SysFont("calibri", 32), que, True, (
                0, 0, 0))
            ANS1 = pygame.font.Font.render(pygame.font.SysFont("calibri", 38), ans[0], True, (0, 0, 0))
            ANS2 = pygame.font.Font.render(pygame.font.SysFont("calibri", 38), ans[1], True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        chosen += 1

            if chosen > 1:
                chosen = 0

            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 950, 150))
            button_location = [(150, 450), (150, 550), (700, 450), (700, 550)]

            pygame.draw.rect(self.window, (169, 169, 169),
                             pygame.Rect(button_location[chosen], self.button_size))
            # czy wybrana odpowiedz jest poprawna?
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if chosen == corr:
                            color = (0, 128, 0)
                            self.run = False
                        else:
                            color = (255, 0, 0)
                            self.run = False  # OJ PRZEGRAŁEŚ KUREWKO
                            self.correct = False

            pygame.draw.rect(self.window, color, pygame.Rect(button_location[chosen], self.button_size))

            button_location.pop(chosen)
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[0], self.button_size))

            self.window.blit(ANS1, (250, 470))  # rysowanie okienka z wynikiem
            self.window.blit(ANS2, (250, 570))
            self.window.blit(QUESTION, (200, 250))
            self.window.blit(score_text, (0, 0))
            pygame.display.update()



    def sadEnding(self):

        self.window = pygame.display.set_mode((1280, 720))
        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, "sea.jpg"))

        while self.run:
            text = pygame.font.Font.render(pygame.font.SysFont("calibri", 48),
                                           'Jesteś dzbanem przykro mi :((. Ale zdobyłes: {} zł'.format(
                                           str(int(self.awards[self.score]))),
                                           True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 950, 150))
            self.window.blit(text, (200, 250))
            pygame.display.update()

    def happyEnding(self):

        self.window = pygame.display.set_mode((1280, 720))
        self.run = True
        self.backgnd_quiz = pygame.image.load(os.path.join(self.path, "sea.jpg"))

        while self.run:
            text = pygame.font.Font.render(pygame.font.SysFont("calibri", 48),
                                           'Jestes super! Wygrales/las: {} zł'.format(
                                           str(int(self.awards[self.score]))),
                                           True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

            self.window.blit(self.backgnd_quiz, (0, 0))  # rysowanie tła
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 950, 150))
            self.window.blit(text, (200, 250))
            pygame.display.update()

    def menu(self):
        """ Menu - w toku


        """


class Logic:

    def __init__(self, file1, file2, file3):
        """Reads questions.

        Args:
            file1 (string): easy questions. File placed in the same folder.
            file2 (string): intermediate questions. File placed in the same folder.
            file3 (string): hard questions. File placed in the same folder.
        """

        self._path = os.path.dirname(__file__)
        self._files = [os.path.join(self._path, file1), os.path.join(self._path, file2), os.path.join(self._path, file3)]  # ścieżka do pliku z pytaniami: łatwe, średnie, trudne
        self._questions = []
        self._answers = []
        self._correct = []

        for e in self._files:
            with open(e) as f:
                temp = json.load(f)  # wczytanie pliku z pytaniami
            self._questions.append(temp['question'])  # dzielimy temp na pytania
            self._answers.append(temp['options'])  # odpowiedzi
            self._correct.append(temp['answer'])  # poprawne odpowiedzi

    def drawQuestions(self):
        """draw 3 random questions for each category.

        Returns:
            list, list, list: chosen questions, answers and correct answers.
        """
        chosenQuestions = [[], [], []]
        chosenAnswers = [[], [], []]
        chosenCorrect = [[], [], []]
        for i in range(3):
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


class Quiz:

    def __init__(self, path1, path2, path3):
        """Prepares quiz and draws questions.

        Args:
            path1 (string): easy questions. File placed in the same folder.
            path2 (string): intermediate questions. File placed in the same folder.
            path3 (string): hard questions. File placed in the same folder.
        """


        self._logic = Logic(path1, path2, path3)  # tworzymy logikę
        self._questions, self._answers, self._correct = self._logic.drawQuestions()  # losujemy pytania
        self._gui = GUI()  # tworzymy gui
        self._max = np.shape(self._questions)[0] * np.shape(self._questions)[1]

    def menu(self):
        """ Displays the menu
        """
        self._gui.menu()

    def quiz(self):
        """ Starts the game.
        """
        for i in range(9):  # quiz ma 9 pytań/rund
            q = self._questions[i // 3][i % 3]  # po 3 łatwe, średnie, trudne
            a = self._answers[i // 3][i % 3]
            c = self._correct[i // 3][i % 3]
            self._gui.question(q, a, c)  # wyświetlamy pytanie
            if self._gui.close:
                break
            if not self._gui.correct:
                Quiz.sadEnd(self)
                break

        if i == self._max - 1:  # tu tak na sztywno ale to do testow tylko sorki
            Quiz.happyEnd(self)

    def sadEnd(self):
        """ Displays the screen when someone loses
        """
        self._gui.sadEnding()

    def happyEnd(self):
        """ Displays the screen when someone wins
        """
        self._gui.happyEnding()

# TUTAJ MAŁY PRZYKŁAD JAK TO WSZYSTKO MA DZIAŁAĆ, MNIEJ WIĘCEJ


q = Quiz('questions_stage_1.json', 'questions_stage_2.json', 'questions_stage_3.json')
q.quiz()
