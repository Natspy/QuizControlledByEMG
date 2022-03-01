import json


class Quiz:

    def __init__(self):
        self.score = 0
        self.max_score = 9
        self.stage = 1
        self.question_num = 1
        self.awards = [0, 1e3, 5e3, 1e4, 2e4, 5e4, 1e5, 2e5, 5e5, 1e6]
        self.stop = False

    def new_game(self):

        if self.score == self.max_score:
            self.stop = True
        else:
            for que in question[self.stage - 1]:
                print(que)
                for opt in options[self.stage - 1][self.score % 3]:
                    print(opt)

                guess = input("Wybierz prawidlowa odpowiedz (1, 2, 3 lub 4):")
                if answer[self.stage - 1][self.score % 3] == int(guess):
                    self.score += 1
                    self.question_num += 1

                else:
                    print("Nieprawidlowa odpowiedz.\nKoniec gry")
                    self.stop = True
                    break

                print("--------------------------------------------------------------------------------")

            self.stage += 1

            if self.score == self.max_score:
                print("Gratulacje! Wygrywasz {} zł.".format(int(self.awards[self.score])))
            elif not self.stop:
                print("Masz {} zł. Zabierz posiadane pieniądze, albo graj dalej i zaryzykuj,"
                      " aby otrzymać wyższą nagrodę.".format(int(self.awards[self.score])))

    def keep_playing(self):
        if self.score != self.max_score and not self.stop:
            response = input("Aby przejsc do kolejnego etapu wpisz '1',"
                             " lub zakoncz i zabierz pieniadze wpisujac '2':")
            if int(response) == 1:
                return True
            else:
                print("Gratulacje, wygrywasz {} zł. Dziękujemy za udział".format(int(self.awards[self.score])))
                return False


file_names = ['questions_stage_1.json', 'questions_stage_2.json', 'questions_stage_3.json']
question, options, answer = [], [], []

for name in file_names:
    with open(name) as f:
        questions = json.load(f)
    question.append(questions['question'])
    options.append(questions['options'])
    answer.append(questions['answer'])

quiz = Quiz()
quiz.new_game()

while quiz.keep_playing():
    quiz.new_game()
