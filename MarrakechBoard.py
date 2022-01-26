import pygame
import pygame.draw
import pygame.event as game_events
import pygame.font
import random
import string
import sys
from pygame.locals import *

# Map parameters
x = 3
y = 3
turn = 0
num = 0
pos = 0
boardX = 150
boardY = 150
cell = 50
windowWidth = 650
windowHeight = 650

# f = open("LOG.txt", "w")
# f.close()

# Initialize pygame
pygame.init()
surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Marrakech Board!')

pressRotate = True
pressDice = False
pressClick = False
click_list = []


def quit_game():
    for event in game_events.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key


def display_box(screen, box_x, box_y, message):
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, 200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255), (box_x - 2, box_y - 2, 204, 24), 2)
    if len(message) != 0:
        screen.blit(fontObject.render(message, True, (255, 255, 255)), (box_x, box_y + 3))
    pygame.display.flip()


def ask(screen, box_x, box_y, question):
    pygame.font.init()
    current_string = []
    display_box(screen, box_x, box_y, question + string.join(current_string, ""))
    while True:
        in_key = get_key()
        if in_key == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif in_key == K_RETURN:
            break
        elif in_key <= 127:
            current_string.append(chr(in_key))
        display_box(screen, box_x, box_y, question + string.join(current_string, ""))
    return string.join(current_string, "")


def box(screen, box_x, box_y):
    carpet = ask(screen, box_x, box_y, "").split("/")
    carpet1 = carpet[0].split("-")
    carpet2 = carpet[1].split("-")
    coordinate1 = (int(carpet1[1]) - 1, int(carpet1[0]) - 1)
    coordinate2 = (int(carpet2[1]) - 1, int(carpet2[0]) - 1)
    return coordinate1, coordinate2


def assam_move(screen, pos, x, y):
    if pos % 4 == 1:
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y - 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x, y + 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x + 8, y), 5, 0)
    if pos % 4 == 0:
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y - 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x + 8, y), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x - 8, y), 5, 0)
    if pos % 4 == 3:
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y + 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x - 8, y), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x, y - 8), 5, 0)
    if pos % 4 == 2:
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y + 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x - 8, y), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x + 8, y), 5, 0)


def get_child(x, y):
    answer = []
    if -1 < x - 1 < 7:
        answer.append((x - 1, y))
    if -1 < x + 1 < 7:
        answer.append((x + 1, y))
    if -1 < y - 1 < 7:
        answer.append((x, y - 1))
    if -1 < y + 1 < 7:
        answer.append((x, y + 1))
    return answer


def dfs(my_board, assam_x, assam_y, color, check_list=[[0 for i in range(7)] for i in range(7)]):
    if my_board.get_detail_xy(assam_x, assam_y).get_color() != color or check_list[assam_x][assam_y] == 1:
        check_list[assam_x][assam_y] = 1
        return 0
    children = get_child(assam_x, assam_y)
    hel = 0
    for i in children:
        hel += check_list[i[0]][i[1]]
    if hel == 4:
        return 1
    answer = 0
    check_list[assam_x][assam_y] = 1
    for i in children:
        if isinstance(my_board.get_detail_xy(i[0], i[1]), Carpet):
            answer += dfs(my_board, i[0], i[1], color, check_list)
    return answer + 1


def find_player(players_list, color):
    for i in range(len(players_list)):
        if players_list[i].get_color() == color:
            return i
    return -1


def log(iterable, *my_string):
    my_file = open("LOG.txt", 'a')
    answer = ""
    for i in my_string:
        answer += str(i) + iterable
    answer += "\n"
    my_file.write(answer)
    my_file.close()


class ShowBoard:
    def __init__(self):
        pass

    def lines(self, screen, x, y, cell):
        for i in range(y, y + 8 * cell, cell):
            pygame.draw.line(screen, (255, 255, 255), (y, i), (y + 7 * cell, i), True)
        for i in range(x, x + 8 * cell, cell):
            pygame.draw.line(screen, (255, 255, 255), (i, x), (i, x + 7 * cell), True)

    def borders(self, screen, x, y, cell):
        for i in range(y, y + 8 * cell, 2 * cell):
            pygame.draw.circle(screen, (255, 255, 255), (x, i), cell / 2, 1)
        for i in range(x, x + 8 * cell, 2 * cell):
            pygame.draw.circle(screen, (255, 255, 255), (i, y), cell / 2, 1)
        for i in range(y + 7 * cell, y, -2 * cell):
            pygame.draw.circle(screen, (255, 255, 255), (x + 7 * cell, i), cell / 2, 1)
        for i in range(x + 7 * cell, x, -2 * cell):
            pygame.draw.circle(screen, (255, 255, 255), (i, y + 7 * cell), cell / 2, 1)
        pygame.draw.rect(surface, (100, 100, 100), (x, y, x + 4 * cell, y + 4 * cell))

    def cells(self, screen, list):
        fontobject = pygame.font.Font(None, 15)
        for i in range(7):
            for j in range(7):
                if list[j][i] == 0:
                    continue
                elif list[j][i].get_color() == "Y":
                    pygame.draw.rect(screen, (255, 222, 0), (150 + i * 50, 150 + j * 50, 50, 50))
                    surface.blit(fontobject.render(str(list[j][i].get_number() + 1), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + j * 50 + 22))
                elif list[j][i].get_color() == "R":
                    pygame.draw.rect(screen, (255, 0, 0), (150 + i * 50, 150 + j * 50, 50, 50))
                    surface.blit(fontobject.render(str(list[j][i].get_number() + 1), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + j * 50 + 22))
                elif list[j][i].get_color() == "G":
                    pygame.draw.rect(screen, (0, 255, 0), (150 + i * 50, 150 + j * 50, 50, 50))
                    surface.blit(fontobject.render(str(list[j][i].get_number() + 1), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + j * 50 + 22))
                else:
                    pygame.draw.rect(screen, (0, 0, 255), (150 + i * 50, 150 + j * 50, 50, 50))
                    surface.blit(fontobject.render(str(list[j][i].get_number() + 1), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + j * 50 + 22))


class Assam:
    def __init__(self, face=1, x=3, y=3):
        self.face = face
        self.x = x
        self.y = y

    def move(self, dice):
        if self.face == 1:
            hel = self.x + dice
            if self.y != 6:
                self.x = hel - (hel - 6 + hel % 7) * int(hel > 6)
                self.y += (-1) ** self.y * (hel // 7)
                self.face += 2 * (hel // 7)
            else:
                self.x = hel - (hel % 7 + 1) * (hel // 7)
                self.y -= (hel % 7) * (hel // 7)
                self.face += 3 * (hel // 7)
        elif self.face == 4:
            hel = self.y - dice
            if self.x != 0:
                self.y = hel - (2 * hel + 1) * int(hel < 0)
                self.x += (-1) ** (self.x + 1) * int(hel < 0)
                self.face -= 2 * int(hel < 0)
            else:
                self.y = hel * int(hel > 0)
                self.x = (-1) * (hel + 1) * int(hel < 0)
                self.face -= 3 * int(hel < 0)
        elif self.face == 3:
            hel = self.x - dice
            if self.y != 0:
                self.x = hel - (2 * hel + 1) * int(hel < 0)
                self.y += (-1) ** (self.y + 1) * int(hel < 0)
                self.face -= 2 * int(hel < 0)
            else:
                self.x = hel * int(hel > 0)
                self.y = (-1) * (hel + 1) * int(hel < 0)
                self.face -= int(hel < 0)
        else:
            hel = self.y + dice
            if self.x != 6:
                self.y = hel - (hel - 6 + hel % 7) * int(hel > 6)
                self.x += (-1) ** self.x * (hel // 7)
                self.face += 2 * (hel // 7)
            else:
                self.y = hel - (hel % 7 + 1) * (hel // 7)
                self.x -= (hel % 7) * (hel // 7)
                self.face += (hel // 7)

    def get_coordinate(self):
        return self.x, self.y

    def get_neighbor(self):
        answer = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if -1 < self.x + i < 7 and -1 < self.y + j < 7:
                    answer.append((self.x + i, self.y + j))
        answer.remove((self.x, self.y))
        return answer

    def __str__(self):
        return 'assam . x : ' + str(self.x) + ' / assam . y : ' + str(self.y) + ' / assam . face : ' + str(self.face)


class Carpet:
    def __init__(self, color, number):
        self.color = color
        self.number = number

    def get_color(self):
        return self.color

    def __str__(self):
        return self.color + "  " + str(self.number)

    def __eq__(self, other):
        if not isinstance(other, Carpet):
            return False
        return (self.color == other.color) and (self.number == other.number)

    def get_number(self):
        return self.number


class Player:
    def __init__(self, color_carpet, number_carpets, rgb, coin=30):
        self.color = color_carpet
        self.playerCarpet = [Carpet(color_carpet, i) for i in range(number_carpets)]
        self.coin = coin
        self.rgb = rgb

    def get_player_carpet(self):
        hel = self.playerCarpet[0]
        self.playerCarpet.remove(self.playerCarpet[0])
        return hel

    def get_rgb(self):
        return self.rgb

    def get_color(self):
        return self.color

    def set_coin(self, coin):
        self.coin = coin

    def get_coin(self):
        return self.coin


class Board:
    def __init__(self, number_players, detail=[[0 for i in range(7)] for i in range(7)], game_turn=0, game_round=0):
        self.numberPlayers = number_players
        self.detail = detail
        self.gameTurn = game_turn
        self.gameRound = game_round

    def get_number_carpets(self):
        if self.numberPlayers == 4:
            return 12
        else:
            return 15

    def get_detail_xy(self, y, x):
        return self.detail[x][y]

    def get_turn(self):
        return self.gameTurn

    def get_round(self):
        return self.gameRound

    def set_turn(self):
        if self.gameTurn == 3:
            self.gameTurn = 0
            self.gameRound += 1
        else:
            self.gameTurn += 1

    def check_correct_move(self, myAssam, coordinate1, coordinate2, my_player):
        flag = False
        # assamCoordinate = myAssam.get_coordinate()
        helCoordinate = myAssam.get_neighbor()
        for i in helCoordinate:
            # log("______", '        ', "i : ", i, "cor 1 , 2 : ", coordinate1, coordinate2)
            if coordinate1 == i:
                if coordinate1[0] - 1 == coordinate2[0] and coordinate1[1] == coordinate2[1]:
                    flag = True
                    break
                elif coordinate1[0] + 1 == coordinate2[0] and coordinate1[1] == coordinate2[1]:
                    flag = True
                    break
                elif coordinate1[0] == coordinate2[0] and coordinate1[1] - 1 == coordinate2[1]:
                    flag = True
                    break
                elif coordinate1[0] == coordinate2[0] and coordinate1[1] + 1 == coordinate2[1]:
                    flag = True
                    break
                else:
                    flag = False
            elif coordinate2 == i:
                if coordinate2[0] - 1 == coordinate1[0] and coordinate2[1] == coordinate1[1]:
                    flag = True
                    break
                elif coordinate2[0] + 1 == coordinate1[0] and coordinate2[1] == coordinate1[1]:
                    flag = True
                    break
                elif coordinate2[0] == coordinate1[0] and coordinate2[1] - 1 == coordinate1[1]:
                    flag = True
                    break
                elif coordinate2[0] == coordinate1[0] and coordinate2[1] + 1 == coordinate1[1]:
                    flag = True
                    break
                else:
                    flag = False

        if flag:
            if self.detail[coordinate1[1]][coordinate1[0]] == 0 or self.detail[coordinate2[1]][coordinate2[0]] == 0:
                flag = True
            elif self.detail[coordinate1[1]][coordinate1[0]] == self.detail[coordinate2[1]][coordinate2[0]]:
                if my_player.get_color() == self.detail[coordinate1[1]][coordinate1[0]].get_color():
                    flag = True
                else:
                    flag = False
            else:
                flag = True
        # log(" ", 'flag : ', flag)
        # log(" ", "assamcoordinate : ", assamCoordinate)
        # log(" ", "coordinate 1 o 2 : ", coordinate1, coordinate2)
        # log(" ", "detail 1 : ", self.detail[coordinate1[1]][coordinate1[0]])
        # log(" ", "detail 2 : ", self.detail[coordinate2[1]][coordinate2[0]])
        # for i in range(7):
        #     for j in range(7):
        #         print self.detail[j][i],
        #     print
        # for i in range(7):
        #     for j in range(7):
        #         if self.detail[j][i] != 0:
        #             print (j, i)
        #     print
        # print 20 * "*"
        if flag:
            helCarpet = my_player.get_player_carpet()
            self.detail[coordinate1[1]][coordinate1[0]] = helCarpet
            self.detail[coordinate2[1]][coordinate2[0]] = helCarpet
            self.set_turn()
        return flag


assam_move(surface, pos, windowWidth / 2, windowHeight / 2)
gameBoard = Board(4)
numberCarpets = gameBoard.get_number_carpets()
myAssam = Assam()
playerList = [Player('Y', numberCarpets, (255, 222, 0)), Player('R', numberCarpets, (255, 0, 0)),
              Player('G', numberCarpets, (0, 255, 0)), Player('B', numberCarpets, (0, 0, 255))]

while gameBoard.get_round() < numberCarpets:
    surface.fill((0, 0, 0))
    pygame.draw.rect(surface, (100, 100, 100), (0, 0, windowWidth, windowHeight))
    mousePosition = pygame.mouse.get_pos()
    fontObject = pygame.font.Font(None, 18)

    MarrakechBoard = ShowBoard()
    ShowBoard.borders(MarrakechBoard, surface, boardX, boardY, cell)
    ShowBoard.cells(MarrakechBoard, surface, gameBoard.detail)
    ShowBoard.lines(MarrakechBoard, surface, boardX, boardY, cell)

    assamX = boardX + cell / 2 + cell * myAssam.x
    assamY = boardY + cell / 2 + cell * myAssam.y
    assam_move(surface, myAssam.face, assamX, assamY)

    for i in range(boardX, boardX + 7 * cell, cell):
        for j in range(boardY, boardY + 7 * cell, cell):
            if pygame.mouse.get_pressed()[0] is True and pressClick is True:
                if i < mousePosition[0] < i + cell:
                    if j < mousePosition[1] < j + cell:
                        clickX = "x" + str((i / cell) - 2)
                        clickY = "y" + str((j / cell) - 2)
                        if clickX not in click_list or clickY not in click_list:
                            click_list.append(clickX)
                            click_list.append(clickY)

    if len(click_list) == 4 and pygame.mouse.get_pressed()[0] == False:
        coordinate = [(int(click_list[0][1]) - 1, int(click_list[1][1]) - 1),
                      (int(click_list[2][1]) - 1, int(click_list[3][1]) - 1)]
        if gameBoard.check_correct_move(myAssam, coordinate[0], coordinate[1], playerList[gameBoard.get_turn()]):
            turn += 1
            pressRotate = True
            pressClick = False
        del click_list[:]

    rotateX = 10
    rotateY = 10
    pygame.draw.rect(surface, (0, 0, 0), (rotateX, rotateY, 50, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (rotateX - 2, rotateY - 2, 54, 24), 2)
    surface.blit(fontObject.render("Left", True, (255, 255, 255)), (rotateX + 7, rotateY + 5))
    if pygame.mouse.get_pressed()[0] is True and pressRotate is True:
        if rotateX < mousePosition[0] < rotateX + 50:
            if rotateY < mousePosition[1] < rotateY + 20:
                myAssam.face -= 1
                if myAssam.face % 4 == 0:
                    myAssam.face = 4
                else:
                    myAssam.face = myAssam.face % 4
                pressRotate = False
                pressDice = True

    rotateX = 80
    rotateY = 10
    pygame.draw.rect(surface, (0, 0, 0), (rotateX, rotateY, 60, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (rotateX - 2, rotateY - 2, 64, 24), 2)
    surface.blit(fontObject.render("Straight", True, (255, 255, 255)), (rotateX + 7, rotateY + 5))
    if pygame.mouse.get_pressed()[0] is True and pressRotate is True:
        if rotateX < mousePosition[0] < rotateX + 50:
            if rotateY < mousePosition[1] < rotateY + 20:
                pressDice = True
                pressRotate = False

    rotateX = 160
    rotateY = 10
    pygame.draw.rect(surface, (0, 0, 0), (rotateX, rotateY, 50, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (rotateX - 2, rotateY - 2, 54, 24), 2)
    surface.blit(fontObject.render("Right", True, (255, 255, 255)), (rotateX + 7, rotateY + 5))
    if pygame.mouse.get_pressed()[0] is True and pressRotate is True:
        if rotateX < mousePosition[0] < rotateX + 50:
            if rotateY < mousePosition[1] < rotateY + 20:
                myAssam.face += 1
                if myAssam.face % 4 == 0:
                    myAssam.face = 4
                else:
                    myAssam.face = myAssam.face % 4
                pressDice = True
                pressRotate = False

    diceX = 10
    diceY = 50
    pygame.draw.rect(surface, (0, 0, 0), (diceX, diceY, 50, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (diceX - 2, diceY - 2, 54, 24), 2)
    surface.blit(fontObject.render("Dice!", True, (255, 255, 255)), (diceX + 7, diceY + 5))
    for i in range(num):
        pygame.draw.circle(surface, (0, 200, 200), (diceX + 70 + i * 20, diceY + 9), 7, 0)
        pygame.draw.circle(surface, (255, 255, 255), (diceX + 70 + i * 20, diceY + 9), 7, 2)
    if pygame.mouse.get_pressed()[0] is True and pressDice is True:
        if diceX < mousePosition[0] < diceX + 50:
            if diceY < mousePosition[1] < diceY + 20:
                num = random.randrange(1, 7)
                myAssam.move(num)
                pressDice = False
                pressClick = True
                assamCoordinate = myAssam.get_coordinate()
                turnPlayer = gameBoard.get_turn()
                assamCell = gameBoard.get_detail_xy(assamCoordinate[0], assamCoordinate[1])
                if isinstance(assamCell, Carpet):
                    assamCellColor = assamCell.get_color()
                    coin = dfs(gameBoard, assamCoordinate[0], assamCoordinate[1], assamCellColor)
                    targetPlayer = find_player(playerList, assamCellColor)
                    playerList[turnPlayer].set_coin(playerList[turnPlayer].get_coin() - coin)
                    playerList[targetPlayer].set_coin(playerList[targetPlayer].get_coin() + coin)

    pygame.draw.rect(surface, (0, 0, 0), (540, 110, 63, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (538, 108, 67, 24), 2)
    surface.blit(fontObject.render("Round: " + str(gameBoard.get_round() + 1), True, (255, 255, 255)), (544, 115))
    pygame.draw.circle(surface, playerList[gameBoard.get_turn()].get_rgb(), (570, 65), 30, 0)
    pygame.draw.circle(surface, (255, 255, 255), (570, 65), 30, 2)

    coinX = 100
    coinY = 600
    pygame.draw.rect(surface, (0, 0, 0), (coinX, coinY, 100, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (coinX - 2, coinY - 2, 104, 24), 2)
    surface.blit(fontObject.render("Yellow Coin: " + str(playerList[0].get_coin()), True, (255, 255, 255)),
                 (coinX + 4, coinY + 5))
    pygame.draw.rect(surface, (0, 0, 0), (coinX + 120, coinY, 100, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (coinX + 120 - 2, coinY - 2, 104, 24), 2)
    surface.blit(fontObject.render("Red Coin: " + str(playerList[1].get_coin()), True, (255, 255, 255)),
                 (coinX + 120 + 4, coinY + 5))
    pygame.draw.rect(surface, (0, 0, 0), (coinX + 240, coinY, 100, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (coinX + 240 - 2, coinY - 2, 104, 24), 2)
    surface.blit(fontObject.render("Green Coin: " + str(playerList[2].get_coin()), True, (255, 255, 255)),
                 (coinX + 240 + 4, coinY + 5))
    pygame.draw.rect(surface, (0, 0, 0), (coinX + 360, coinY, 100, 20), 0)
    pygame.draw.rect(surface, (255, 255, 255), (coinX + 360 - 2, coinY - 2, 104, 24), 2)
    surface.blit(fontObject.render("Blue Coin: " + str(playerList[3].get_coin()), True, (255, 255, 255)),
                 (coinX + 360 + 4, coinY + 5))

    quit_game()
    pygame.display.update()


def check_winner(game_board, player_list):
    point_list_coin = [i.get_coin() for i in player_list]

    for i in game_board.detail:
        for j in i:
            if isinstance(j, Carpet):
                if j.get_color() == 'Y':
                    point_list_coin[0] += 1
                elif j.get_color() == 'R':
                    point_list_coin[1] += 1
                elif j.get_color() == 'G':
                    point_list_coin[2] += 1
                elif j.get_color() == 'B':
                    point_list_coin[3] += 1
    return point_list_coin


while True:
    surface.fill((0, 0, 0))
    pygame.draw.rect(surface, (100, 100, 100), (0, 0, windowWidth, windowHeight))
    fontObject = pygame.font.Font(None, 28)

    finalList = check_winner(gameBoard, playerList)

    surface.blit(fontObject.render("Yellow:" + str(finalList[0]), True, (255, 255, 255)),
                 (windowWidth / 2 - 40, windowHeight / 2 - 55))
    surface.blit(fontObject.render("Red:" + str(finalList[1]), True, (255, 255, 255)),
                 (windowWidth / 2 - 40, windowHeight / 2 - 20))
    surface.blit(fontObject.render("Green:" + str(finalList[2]), True, (255, 255, 255)),
                 (windowWidth / 2 - 40, windowHeight / 2 + 20))
    surface.blit(fontObject.render("Blue:" + str(finalList[3]), True, (255, 255, 255)),
                 (windowWidth / 2 - 40, windowHeight / 2 + 55))

    hel = finalList.index(max(finalList))

    if hel == 0:
        surface.blit(fontObject.render("Yellow Is The Winner!", True, (255, 255, 255)),
                     (windowWidth / 2 - 85, windowHeight / 2 + 100))
    elif hel == 1:
        surface.blit(fontObject.render("Red Is The Winner!", True, (255, 255, 255)),
                     (windowWidth / 2 - 85, windowHeight / 2 + 100))
    elif hel == 2:
        surface.blit(fontObject.render("Green Is The Winner!", True, (255, 255, 255)),
                     (windowWidth / 2 - 85, windowHeight / 2 + 100))
    elif hel == 3:
        surface.blit(fontObject.render("Blue Is The Winner!", True, (255, 255, 255)),
                     (windowWidth / 2 - 85, windowHeight / 2 + 100))
    quit_game()
    pygame.display.update()
