import pygame
import os
import random
import json


class GUI:
    def __init__(self):
        """_summary_
        """
        self.path = os.path.dirname(__file__)
        self.clock = 0
        self.score = 0
        self.awards = [0, 1e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]
        self.correct = True
        self.max_score = 9

    def question(self, que, ans, corr):
        """_summary_

        Args:
            que (_type_): _description_
            ans (_type_): _description_
            corr (_type_): _description_
        """

        pygame.init()

        self.window = pygame.display.set_mode((1280, 720))
        self.run = True
        self.backgnd = pygame.image.load(os.path.join(self.path, "sea.jpg"))  # LaiRMaSTeR mówi: tak robimy, kurde
        self.button_size = (400, 80)

        # zmienna ktora oznacza wybrana odp; default = 0
        chosen = 0
        color = (169, 169, 169)
        while self.run:
            self.clock += pygame.time.Clock().tick(
                60) / 1000  # zwalniamy petle zeby tak szybko sie wszystko nie poruszało
            score_text = pygame.font.Font.render(pygame.font.SysFont("calibri", 48),
                                                 'Aktualna nagroda: {} zł'.format(str(int(self.awards[self.score]))),
                                                 True, (0, 0, 0))
            QUESTION = pygame.font.Font.render(pygame.font.SysFont("calibri", 32), que, True, (
                0, 0, 0))  # LaiRMaSTeR krzyczy: BŁAGAM ALBO POLSKIE ALBO ANGIELSKIE ZMIENNE
            ANS1 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[0], True, (0, 0, 0))
            ANS2 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[1], True, (0, 0, 0))
            ANS3 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[2], True, (0, 0, 0))
            ANS4 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), ans[3], True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        chosen += 1

            if chosen > 3:
                chosen = 0

            # rysowanie tego wszystkiego:
            # najpierw swiat
            self.window.blit(self.backgnd, (0, 0))  # rysowanie tła

            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 950, 150))

            button_location = [(150, 450), (150, 550), (700, 450), (700, 550)]

            # zaznaczamy szarym wybraną opcję
            # pygame.draw.rect(window, (169, 169, 169), pygame.Rect(button_location[chosen], button_size))

            pygame.draw.rect(self.window, (169, 169, 169), pygame.Rect(button_location[chosen], self.button_size))
            # czy wybrana odpowiedz jest poprawna?
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if chosen == corr:
                            color = (0, 128, 0)
                            self.score += 1
                            self.run = False
                        else:
                            color = (255, 0, 0)
                            self.run = False  # to pewnie trzeba zmienić na generowanie jakiegoś ekranu z napisem OJ PRZEGRAŁEŚ KUREWKO
                            self.correct = False

            pygame.draw.rect(self.window, color, pygame.Rect(button_location[chosen], self.button_size))

            button_location.pop(chosen)
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[0], self.button_size))
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[1], self.button_size))
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[2], self.button_size))

            self.window.blit(ANS1, (250, 470))  # rysowanie okienka z wynikiem
            self.window.blit(ANS2, (250, 570))
            self.window.blit(ANS3, (800, 470))
            self.window.blit(ANS4, (800, 570))
            self.window.blit(QUESTION, (200, 250))
            self.window.blit(score_text, (0, 0))
            pygame.display.update()

    def keep_playing(self):

        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        self.run = True
        self.backgnd = pygame.image.load(
            os.path.join(self.path, "sea.jpg"))
        self.button_size = (1000, 80)

        que = 'Przejść do kolejnego etapu?'
        ans = ['Tak, gram dalej', 'Nie, rezygnuję i zabieram kwotę gwarantowaną']
        corr = 0
        chosen = 0
        color = (169, 169, 169)
        while self.run:
            self.clock += pygame.time.Clock().tick(60) / 1000
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

            self.window.blit(self.backgnd, (0, 0))  # rysowanie tła
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


class Logic:

    def __init__(self, path1, path2, path3):
        """_summary_

        Args:
            path1 (_type_): _description_
            path2 (_type_): _description_
            path3 (_type_): _description_
        """
        self._path = [path1, path2, path3]  # ścieżka do pliku z pytaniami: łatwe, średnie, trudne
        self._questions = [[], [], []]
        self._answers = [[], [], []]
        self._correct = [[], [], []]

        for i, e in enumerate(self._path):
            temp = 0  # wczytanie jakoś pliku
            self._questions[i] = 0  # dzielimy temp na pytania
            self._answers[i] = 0  # odpowiedzi
            self._correct[i] = 0  # poprawne odpowiedzi

    def drawQuestions(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        chosenQuestions = [[], [], []]
        chosenAnswers = [[], [], []]
        chosenCorrect = [[], [], []]
        for i in range(2):
            lengths = range(0, len(self.questions[i]))  # indeksy dla danego zbioru pytań
            chosen = random.choice(lengths, 3)  # losujemy indeksy pytań
            chosenQuestions[i] = self.questions[i][chosen]
            chosenAnswers[i] = self.answers[i][chosen]
            chosenCorrect[i] = self.correct[i][chosen]

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
        self._logic = Logic(path1, path2, path3)  # tworzymy logikę
        self._questions, self._answers, self._correct = self._logic.drawQuestions()  # losujemy pytania
        self._gui = GUI()  # tworzymy GUI
        for i in range(9):  # quiz ma 9 pytań/rund
            q = self._questions[i // 3][i % 3]  # po 3 łatwe, średnie, trudne
            a = self._answers[i // 3][i % 3]
            c = self._correct[i // 3][i % 3]
            self._gui.question(q, a, c)  # wyświetlamy pytanie
            if not self._gui.correct:
                break  # jeśli jest niepoprawna odpowiedź kończymy grę

        print("ALE Z CIEBIE MĄDRA KUREWKA")  # coś musi się stać jeśli wszystkie 9 odpowiedzi będzie poprawne


# TUTAJ MAŁY PRZYKŁAD JAK TO WSZYSTKO MA DZIAŁAĆ, MNIEJ WIĘCEJ
a = GUI()

file_names = ['questions_stage_1.json', 'questions_stage_2.json', 'questions_stage_3.json']
question, options, answer = [], [], []

for name in file_names:
    with open(name) as f:
        questions = json.load(f)
    question.append(questions['question'])
    options.append(questions['options'])
    answer.append(questions['answer'])

question_yn = 'Przejść do kolejnego etapu?'
options_yn = ['Tak, gram dalej', 'Nie, rezygnuję i zabieram kwotę gwarantowaną']
answer_yn = 0

for stage in range(3): # te pętle są do wstawienia do klasy Quiz (jako nowa metoda np. new_game())
    for i in range(3):
        a.question(question[stage][i], options[stage][i], answer[stage][i])
        if not a.correct:
            break
    if not a.correct:
        break
    if a.score != a.max_score:
        a.keep_playing()
        if not a.correct:
            break
    else:
        print("ALE Z CIEBIE MĄDRA KUREWKA")

