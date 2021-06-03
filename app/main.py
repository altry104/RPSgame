from kivy.app import App
from threading import Thread
import random
from kivy.lang import Builder
import socket
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

choices = ("Rock", "Paper", "Scissors")

kv = Builder.load_file("rockspapers.kv")


class WindowManager(ScreenManager):
    pass


class Menu(Screen):
    def transit_to_bot(self):
        sm.current = 'bot_game'

    def transit_to_online(self):
        sm.current = 'online_game'


class MainWindow(Screen):
    games = NumericProperty(0)
    wins = NumericProperty(0)
    winrate = NumericProperty(0)

    def back_to_menu(self):
        sm.current = 'menu'

    def paper(self):
        self.ids.player_image.source = 'paper.jpg'
        self.ids.player_choice.text = "Paper"
        self.ids.bot_choice.text = random.choice(choices)
        if self.ids.bot_choice.text == "Rock":
            self.ids.bot_image.source = 'rock.jpg'
            self.ids.results.text = "You Won!"
            # self.ids.results.color = 'green'
            self.update_score(win=True)
            self.ids.gif.source = 'player_win.gif'
            self.ids.gif.anim_delay = 0.10
            self.ids.gif._coreimage.anim_reset(True)
        elif self.ids.bot_choice.text == 'Scissors':
            self.ids.bot_image.source = 'scissors.jpg'
            self.ids.results.text = "You lost!"
            # self.ids.results.color = 'red'
            self.update_score()
            self.ids.gif.source = 'p-s_botwin.gif'
            self.ids.gif.anim_delay = 0
            self.ids.gif._coreimage.anim_reset(True)
        else:
            self.ids.bot_image.source = 'paper.jpg'
            # self.ids.results.color = 'yellow'
            self.ids.results.text = "Draw!"
            self.update_score()
            self.ids.gif.source = 'draw.gif'
            self.ids.gif.anim_delay = 0.30
            self.ids.gif._coreimage.anim_reset(True)

    def rock(self):
        self.ids.player_choice.text = "Rock"
        self.ids.player_image.source = "rock.jpg"
        self.ids.bot_choice.text = random.choice(choices)
        if self.ids.bot_choice.text == "Scissors":
            self.ids.bot_image.source = 'scissors.jpg'
            self.ids.results.text = "You Won!"
            # self.ids.results.color = 'green'
            self.update_score(win=True)
            self.ids.gif.source = 'player_win.gif'
            self.ids.gif.anim_delay = 0.10
            self.ids.gif._coreimage.anim_reset(True)
        elif self.ids.bot_choice.text == 'Paper':
            self.ids.bot_image.source = 'paper.jpg'
            self.ids.results.text = "You lost!"
            # self.ids.results.color = 'red'
            self.update_score()
            self.ids.gif.source = 'bot_win.gif'
            self.ids.gif.anim_delay = 0.10
            self.ids.gif._coreimage.anim_reset(True)
        else:
            self.ids.bot_image.source = 'rock.jpg'
            # self.ids.results.color = 'yellow'
            self.ids.results.text = "Draw!"
            self.update_score()
            self.ids.gif.source = 'draw.gif'
            self.ids.gif.anim_delay = 0.30
            self.ids.gif._coreimage.anim_reset(True)

    def scissors(self):
        self.ids.player_image.source = "scissors.jpg"
        self.ids.player_choice.text = "Scissors"
        self.ids.bot_choice.text = random.choice(choices)
        if self.ids.bot_choice.text == "Paper":
            self.ids.bot_image.source = 'paper.jpg'
            # self.ids.results.color = 'green'
            self.ids.results.text = "You Won!"
            self.update_score(win=True)
            self.ids.gif.source = 'player_win.gif'
            self.ids.gif.anim_delay = 0.10
            self.ids.gif._coreimage.anim_reset(True)
        elif self.ids.bot_choice.text == 'Rock':
            self.ids.bot_image.source = 'rock.jpg'
            self.ids.results.text = "You lost!"
            # self.ids.results.color = 'red'
            self.update_score()
            self.ids.gif.source = 'bot_win.gif'
            self.ids.gif.anim_delay = 0.10
            self.ids.gif._coreimage.anim_reset(True)
        else:
            self.ids.bot_image.source = 'scissors.jpg'
            # self.ids.results.color = 'yellow'
            self.ids.results.text = "Draw!"
            self.update_score()
            self.ids.gif.source = 'draw.gif'
            self.ids.gif.anim_delay = 0.30
            self.ids.gif._coreimage.anim_reset(True)

    def update_score(self, win=False):
        self.games += 1
        if win == False:
            if self.wins == 0:
                pass
            else:
                self.winrate = int(self.wins / self.games * 100)
        else:
            self.wins += 1
            self.winrate = int(self.wins / self.games * 100)


class OnlineGame(Screen):
    games = NumericProperty(0)
    wins = NumericProperty(0)
    winrate = NumericProperty(0)
    s = socket.socket()
    host = '194.87.248.78'
    port = 7000

    def connect_to_server(self):
        self.s.connect((self.host, self.port))
        # data = self.s.recv(1024).decode()
        # strdata = str(data)
        # print(strdata)
        Thread(target=self.receive_from_server).start()

    def receive_from_server(self):
        while True:
            from_server = self.s.recv(1000).decode()
            print(from_server)
            if from_server == "rock":
                self.ids.opponent_choice.text = 'rock'
                self.ids.opponent_image.source = 'rock.jpg'
                if self.ids.player_choice.text == 'scissors':
                    self.ids.results.text = 'YOU LOST!'
                elif self.ids.player_choice.text == 'rock':
                    self.ids.results.text = 'YOU WON!'
                else:
                    self.ids.results.text = 'DRAW!'
            elif from_server == "paper":
                self.ids.opponent_choice.text = 'paper'
                self.ids.opponent_image.source = 'paper.jpg'
                if self.ids.player_choice.text == 'rock':
                    self.ids.results.text = 'YOU LOST!'
                elif self.ids.player_choice.text == 'paper':
                    self.ids.results.text = 'YOU WON!'
                else:
                    self.ids.results.text = 'DRAW!'
            else:
                self.ids.opponent_choice.text = 'scissors'
                self.ids.opponent_image.source = 'scissors.jpg'
                if self.ids.player_choice.text == 'scissors':
                    self.ids.results.text = 'YOU WON!'
                elif self.ids.player_choice.text == 'paper':
                    self.ids.results.text = 'YOU LOST!'
                else:
                    self.ids.results.text = 'DRAW!'


    def back_to_menu(self):
        sm.current = 'menu'

    def rock(self):
        self.ids.player_choice.text = 'rock'
        self.ids.player_image.source = 'rock.jpg'
        self.s.send(str("rock!").encode())

    def paper(self):
        self.ids.player_choice.text = 'paper'
        self.ids.player_image.source = 'paper.jpg'
        self.s.send(str("paper!").encode())

    def scissors(self):
        self.ids.player_choice.text = 'scissors'
        self.ids.player_image.source = 'scissors.jpg'
        self.s.send(str("scissors!").encode())


sm = WindowManager()
screens = [Menu(name='menu'), MainWindow(name='bot_game'), OnlineGame(name='online_game')]
for screen in screens:
    sm.add_widget(screen)
sm.current = 'menu'


class RocksPapers(App):
    def build(self):
        return sm


if __name__ == '__main__':
    RocksPapers().run()
