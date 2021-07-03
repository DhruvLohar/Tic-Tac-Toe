import pygame, json
from threading import Thread

from core.core import get_location, is_winner
from core.ui import TextInput, Button, Text
from core.multiplayer.client import Client

from PIL import Image, ImageFilter

pygame.init()

class TicTacToe:
    def __init__(self):
        self.current = 'X'
        self.current_pos = None

        self.width = 600
        self.height = 700

        self.layout = [
            ['-', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']
        ]
        self.moves = {}

        self.fps_clock = pygame.time.Clock()
        self.root = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("TIC TAC TOE")

    def render_layout(self):
        pygame.draw.line(self.root, (96, 107, 26),(200, 0), (200, 600), 15)
        pygame.draw.line(self.root, (96, 107, 26), (400, 0), (400, 600), 15)

        pygame.draw.line(self.root, (96, 107, 26), (0, 200), (600, 200), 15)
        pygame.draw.line(self.root, (96, 107, 26), (0, 400), (600, 400), 15)

    def render_text(self):
        font = pygame.font.Font('core/assests/BebasNeue.ttf', 110)
        for pos, current in self.moves.items():
            font_text = font.render(current, True, (10, 10, 10))
            self.root.blit(font_text, (pos[0], pos[1]))
    
    def won(self, scores):
        won_bg = pygame.image.load('core/assests/Won.png')
        restart = pygame.Rect(155, 195, 290, 78)
        close = pygame.Rect(202, 398, 195, 75)

        has_won = True
        while has_won:
            self.root.blit(won_bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    has_won = False
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart.collidepoint(event.pos):
                        has_won = False
                        single = SinglePlayer(scores)
                        single.create_instance()
                    elif close.collidepoint(event.pos):
                        has_won = False
                        quit()
            
            pygame.display.flip()
            self.fps_clock.tick(20)

    def menu(self):
        menu_bg = pygame.image.load('core/assests/Home.png')
        single_player = Button('Single Player', (220, 47), (46, 265))
        multi_player = Button('Multi Player', (200, 42), (57, 358))

        on_menu = True
        while on_menu:
            self.root.blit(menu_bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on_menu = False
                    quit()
                elif single_player.is_clicked(event):
                    on_menu = False
                    single = SinglePlayer()
                    single.create_instance()
                elif multi_player.is_clicked(event):
                    on_menu = False
                    self.multiplayer_menu()
            
            single_player.render(self.root)
            multi_player.render(self.root)

            pygame.display.flip()
            self.fps_clock.tick(20)
    
    def multiplayer_menu(self):
        multiplayer_bg = pygame.image.load('core/assests/Multiplayer.png')

        self.name = TextInput(self.root, (226, 34), (52, 222), "enter username")
        self.room_id = TextInput(self.root, (226, 34), (52, 282), "enter room name")
        inputs = [self.name, self.room_id]
        start = pygame.Rect(90, 379, 131, 41)

        on_multiplayer_page = True
        while on_multiplayer_page:
            self.root.blit(multiplayer_bg, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on_multiplayer_page = False
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start.collidepoint(event.pos):
                        on_multiplayer_page = False
                        multiplayer = MultiPlayer(self.name.text, self.room_id.text)
                        multiplayer.create_instance()
                
                for inp in inputs:
                    inp.handle_event(event)
            
            for inp in inputs:
                inp.render()

            pygame.display.flip()
            self.fps_clock.tick(20)


class SinglePlayer(TicTacToe):
    def __init__(self, scores=(0, 0)):
        super().__init__()
        self.player = {
            'name': 'Player 1',
            'alias': self.current,
            'score': scores[0]
        }
        self.name = Text(self.root, self.player['name'], (100, 25))
        self.score = Text(self.root, str(self.player['score']), (20, 25))

        self.oppo = {
            'name': 'Player 2',
            'alias': '0' if self.player['alias'] == self.current else 'X',
            'score': scores[1]
        }
        self.oppo_name = Text(self.root, self.oppo['name'], (400, 25))
        self.oppo_score = Text(self.root, str(self.oppo['score']), (560, 25))

        self.content = [self.name, self.score, self.oppo_name, self.oppo_score]
    
    def create_instance(self):
        game_bg = pygame.image.load('core/assests/Game.png')

        in_game = True
        while in_game:
            self.root.blit(game_bg, (0, 0))
            for i in self.content: i.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y, x_pos, y_pos = get_location(pygame.mouse.get_pos())
                    self.layout[x-1][y-1] = self.current
                    if is_winner(self.layout, self.current):
                        if self.player['alias'] == self.current: 
                            self.player['score'] += 1
                            self.score.update(str(self.player['score']))
                        else:
                            self.oppo['score'] += 1
                            self.oppo_score.update(str(self.oppo['score']))
                        self.layout = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
                        self.moves.clear()
                        self.won((self.player['score'], self.oppo['score']))
                    else:
                        self.current_pos = (x_pos, y_pos)
                        self.moves[self.current_pos] = self.current

                        self.current = 'O' if self.current == 'X' else 'X'
 
            if self.player['alias'] == self.current:
                self.name.active = True
                self.oppo_name.active = False
            else:
                self.oppo_name.active = True
                self.name.active = False
            if self.current_pos is not None:
                self.render_text() 
            
            pygame.display.flip()
            self.fps_clock.tick(20)


class MultiPlayer(TicTacToe):
    def __init__(self, user, room_id):
        super().__init__()
        self.in_game = True
        self.is_player_won = False
        self.player = {
            'name': user,
            'room': room_id,
            'alias': None,
            'score': 0
        }
        self.name = Text(self.root, self.player['name'], (100, 25))
        self.score = Text(self.root, str(self.player['score']), (20, 25))

        self.opponent = None
        self.opp_name = Text(self.root, '', (400, 25))
        self.opp_score = Text(self.root, '0', (560, 25))

        self.content = [self.name, self.score, self.opp_name, self.opp_score]
        
        self.client = Client('localhost', 8000)
        self.client.connect({
            'type': 'init',
            'username': self.player['name'],
            'room_id': self.player['room']
        })

        Thread(target=self.data_reciever, daemon=True).start()
    
    def data_reciever(self):
        while True:
            data = json.loads(self.client.server.recv(2048).decode())
            if data:
                if data['type'] == 'room_joined':
                    for i in data['data']:
                        if i['username'] == self.player['name']:
                            self.player['alias'] = i['alias']
                            if self.player['alias'] == data['current']:
                                self.name.active = True
                            else: self.opp_name.active = True
                        else: 
                            self.opponent = i
                            self.opp_name.text = self.opponent['username']
                            self.opp_name.update(self.opponent['username'])
                elif data['type'] == 'layout_update':
                    x_pos, y_pos = data['moved_to'][2], data['moved_to'][3]
                    self.current_pos = (x_pos, y_pos)
                    self.moves[self.current_pos] = data['move_by']['alias']

                    if self.player['alias'] == data['current']:
                        self.name.active = True
                        self.opp_name.active = False
                    else: 
                        self.opp_name.active = True
                        self.name.active = False
                elif data['type'] == 'has_won':
                    if self.player['alias'] == data['winner']:
                        self.player['score'] += 1
                        self.score.update(str(self.player['score']))
                        self.is_player_won = True
                    else: 
                        self.opponent['score'] += 1
                        self.opp_score.update(str(self.opponent['score']))
                    self.moves.clear()
                    self.in_game = False

    def multiplayer_won(self, msg):
        won_bg = pygame.image.load('core/assests/Won.png')
        restart = pygame.Rect(155, 195, 290, 78)
        close = pygame.Rect(202, 398, 195, 75)
        msg = Text(self.root, msg, (170, 25))
        msg.active = True

        has_won = True
        while has_won:
            self.root.blit(won_bg, (0, 0))
            msg.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    has_won = False
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart.collidepoint(event.pos):
                        has_won = False
                        self.in_game = True
                        self.create_instance()
                    elif close.collidepoint(event.pos):
                        has_won = False
                        quit()
            
            pygame.display.flip()
            self.fps_clock.tick(20)

    def create_instance(self):
        game_bg = pygame.image.load('core/assests/Game.png')
        game = True
        while game:
            self.root.blit(game_bg, (0, 0))
            for i in self.content: i.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y, x_pos, y_pos = get_location(pygame.mouse.get_pos())
                    data = {
                        'type': 'move_played',
                        'room_id': self.player['room'],
                        'layout_data': get_location(pygame.mouse.get_pos()),
                        'player_data': {
                            'username': self.player['name'],
                            'alias': self.player['alias']
                        }
                    }
                    self.client.played_move(data)

            if self.current_pos is not None:
                self.render_text() 
            if not self.in_game:
                game = False
                if self.is_player_won:
                    self.multiplayer_won('Hooray! you won!')
                else: self.multiplayer_won('Oops! you lost!')
            
            pygame.display.flip()
            self.fps_clock.tick(20)

game = TicTacToe()
game.menu()


"""
TicTacToe
    - menu
        - MultipLayer
            -client
        - SinglePlayer

server
    - emitter
        - init
        - layout update
    -receiver
        - init
        - move_played

client
    - emiter
        - init
        - move played
    - receiver
        - room koined
        - layout update
"""