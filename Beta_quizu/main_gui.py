import pygame
import os
import random

class GUI():
    def __init__(self):
        """_summary_
        """
        self.path = os.path.dirname(__file__)

        self.clock = 0
        self.score = 0
        self.correct = True
    
    def question(self, pytanie, odp, prawidlowa):
        """_summary_

        Args:
            pytanie (_type_): _description_
            odp (_type_): _description_
            prawidlowa (_type_): _description_
        """
        
        pygame.init()

        self.window = pygame.display.set_mode((1280,720))
        self.run = True
        self.backgnd = pygame.image.load(os.path.join(self.path, "sea.jpg"))  # LaiRMaSTeR mówi: tak robimy, kurde
        self.button_size = (400, 80)
        
        #zmienna ktora oznacza wybrana odp; default = 0
        chosen = 0
        color = (169, 169, 169)
        while self.run:
            self.clock += pygame.time.Clock().tick(60) / 1000  # zwalniamy petle zeby tak szybko sie wszystko nie poruszało
            score_tekst = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), 'Wynik: {}'.format(str(self.score)), True,
                                                (0, 0, 0))
            PYTANIE = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), pytanie, True, (0, 0, 0))  # LaiRMaSTeR krzyczy: BŁAGAM ALBO POLSKIE ALBO ANGIELSKIE ZMIENNE
            ODP1 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[0], True, (0, 0, 0))
            ODP2 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[1], True, (0, 0, 0))
            ODP3 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[2], True, (0, 0, 0))
            ODP4 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[3], True, (0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        chosen += 1

            if chosen > 3:
                chosen = 0

            #rysowanie tego wszystkiego:
            #najpierw swiat
            self.window.blit(self.backgnd, (0,0)) #rysowanie tła

            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(150, 200, 950, 150))

            button_location = [(150, 450), (150, 550), (700, 450),(700, 550)]

            #zaznaczamy szarym wybraną opcję
            #pygame.draw.rect(window, (169, 169, 169), pygame.Rect(button_location[chosen], button_size))

            pygame.draw.rect(self.window, (169, 169, 169), pygame.Rect(button_location[chosen], self.button_size))
            #czy wybrana odpowiedz jest poprawna?
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if chosen == prawidlowa:
                            color = (0,128,0)
                            self.score += 1
                            self.run = False
                        else:
                            color = (255,0,0)
                            self.run = False  # to pewnie trzeba zmienić na generowanie jakiegoś ekranu z napisem OJ PRZEGRAŁEŚ KUREWKO
                            self.correct = False


            pygame.draw.rect(self.window, color, pygame.Rect(button_location[chosen], self.button_size))

            button_location.pop(chosen)
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[0], self.button_size))
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[1], self.button_size))
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(button_location[2], self.button_size))


            self.window.blit(ODP1, (250, 470))  # rysowanie okienka z wynikiem
            self.window.blit(ODP2, (250, 570))
            self.window.blit(ODP3, (800, 470))
            self.window.blit(ODP4, (800, 570))
            self.window.blit(PYTANIE, (400, 250))
            self.window.blit(score_tekst, (0,0))
            pygame.display.update()

class Logic():

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

class Quiz():
    
    def __init__(self, path1, path2, path3):
        self._logic = Logic(path1, path2, path3)  # tworzymy logikę
        self._questions, self._answers, self._correct = self._logic.drawQuestions()  # losujemy pytania
        self._gui = GUI()  # tworzymy GUI
        for i in range(9):  # quiz ma 9 pytań/rund
            q = self._questions[i // 3][i % 3]  # po 3 łatwe, średnie, trudne
            a = self._answers[i // 3][i % 3]
            c = self._correct[i // 3][i % 3]
            self._gui.question(q, a, c)  # wyświetlamy pytanie
            if self._gui.correct == False:
                break  # jeśli jest niepoprawna odpowiedź kończymy grę

        print("ALE Z CIEBIE MĄDRA KUREWKA")  # coś musi się stać jeśli wszystkie 9 odpowiedzi będzie poprawne






# TUTAJ MAŁY PRZYKŁAD JAK TO WSZYSTKO MA DZIAŁAĆ, MNIEJ WIĘCEJ
a = GUI()

pytanie = ['Czy woda jest mokra?', 'Czy woda jest sucha?']  
odp  = [['tak', 'nie', 'chyba', 'możliwe'], ['tak', 'nie', 'chyba', 'możliwe']]
prawidlowa = [0, 1]

for i in range(2):
        a.question(pytanie[i],odp[i],prawidlowa[i])
        if a.correct == False: break