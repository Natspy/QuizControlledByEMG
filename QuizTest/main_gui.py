import pygame

pygame.init()

window = pygame.display.set_mode((1280,720))
def main():
    run = True
    clock = 0
    score = 0
    backgnd = pygame.image.load("sea.jpg")
    button_size = (400, 80)
    pytanie = 'Czy woda jest mokra?'
    odp  = ['tak', 'nie', 'chyba', 'możliwe']
    prawidlowa = 0

    #zmienna ktora oznacza wybrana odp; default = 0
    chosen = 0
    color = (169, 169, 169)
    while run:
        clock += pygame.time.Clock().tick(60) / 1000  # zwalniamy petle zeby tak szybko sie wszystko nie poruszało
        score_tekst = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), 'Wynik: {}'.format(str(score)), True,
                                              (0, 0, 0))
        PYTANIE = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), pytanie, True, (0, 0, 0))
        ODP1 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[0], True, (0, 0, 0))
        ODP2 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[1], True, (0, 0, 0))
        ODP3 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[2], True, (0, 0, 0))
        ODP4 = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), odp[3], True, (0, 0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    chosen += 1

        if chosen > 3:
            chosen = 0

        #rysowanie tego wszystkiego:
        #najpierw swiat
        window.blit(backgnd, (0,0)) #rysowanie tła

        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(150, 200, 950, 150))

        button_location = [(150, 450), (150, 550), (700, 450),(700, 550)]

        #zaznaczamy szarym wybraną opcję
        #pygame.draw.rect(window, (169, 169, 169), pygame.Rect(button_location[chosen], button_size))

        pygame.draw.rect(window, (169, 169, 169), pygame.Rect(button_location[chosen], button_size))
        #czy wybrana odpowiedz jest poprawna?
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if chosen == prawidlowa:
                        color = (0,128,0)
                        score += 1
                    else:
                        color = (255,0,0)


        pygame.draw.rect(window, color, pygame.Rect(button_location[chosen], button_size))

        button_location.pop(chosen)
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(button_location[0], button_size))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(button_location[1], button_size))
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(button_location[2], button_size))


        window.blit(ODP1, (250, 470))  # rysowanie okienka z wynikiem
        window.blit(ODP2, (250, 570))
        window.blit(ODP3, (800, 470))
        window.blit(ODP4, (800, 570))
        window.blit(PYTANIE, (400, 250))
        window.blit(score_tekst, (0,0))
        print(chosen)
        pygame.display.update()


if __name__ == '__main__':
    main()