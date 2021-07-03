import pygame, os
pygame.init()

root_dir = os.path.dirname(os.path.abspath(__file__))

class Text:
    def __init__(self, root, text, pos):
        self.root = root
        self.x, self.y = pos
        self.text = text

        self.font = pygame.font.Font(os.path.join(root_dir, 'assests/BebasNeue.ttf'), 45)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))

        self.width, self.height = self.text_surface.get_width(), self.text_surface.get_height()

        self.active_rect = pygame.Rect(self.x - 20, self.y + 30, self.width + 40, self.height / 2)
        self.color = pygame.Color('#F8BD61')
        self.active = False

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, text):
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.width, self.height = self.text_surface.get_width(), self.text_surface.get_height()
        self.active_rect = pygame.Rect(self.x - 20, self.y + 30, self.width + 40, self.height / 2)

    def render(self):
        if self.active:
            pygame.draw.rect(self.root, self.color, self.active_rect)
        self.root.blit(self.text_surface, (self.rect.x, self.rect.y))

class TextInput:
    def __init__(self, root, dimensions, pos, placeholder):
        self.root = root
        self.width, self.height = dimensions
        self.x, self.y = pos
        self.placeholder = placeholder
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.color_passive = pygame.Color('#F8BD61')
        self.color_active = pygame.Color('#DCD2D2')
        self.color = self.color_passive
        self.active = False

        self.font = pygame.font.Font(os.path.join(root_dir, 'assests/raleway.ttf'), 18)
        self.text = ''
        self.place_holder = self.font.render(self.placeholder, True, (0, 0, 0))
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else: self.active = False
            self.color = self.color_passive if not self.active else self.color_active
        if event.type == pygame.KEYDOWN:
            if self.active and len(self.text) < 8:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        
                self.text_surface = self.font.render(self.text, True, (0, 0, 0))

    def render(self):
        pygame.draw.rect(self.root, self.color, self.rect, border_radius=10)
        self.root.blit(self.text_surface, (self.rect.x + 20, self.rect.y + 6))
        if not self.active:
            if self.text == "":
                self.root.blit(self.place_holder, (self.rect.x + 20, self.rect.y + 6))

class Button:
    def __init__(self, text, dimensions, pos):
        self.text = text
        self.width, self.height = dimensions
        self.x, self.y = pos 

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover = pygame.Rect(self.x - 17, self.y + 23, self.width + 30, self.height // 2)
        self.color_passive = pygame.Color('#E5E5E5')
        self.color_active = pygame.Color('#F8BD61')
        self.color = self.color_passive
        self.active = False

        self.font = pygame.font.Font(os.path.join(root_dir, 'assests/raleway.ttf'), 36)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active if self.active else self.color_passive

            else: self.active = False

    def render(self, root):
        if self.active: pygame.draw.rect(root, self.color, self.hover)
        root.blit(self.text_surface, (self.rect.x, self.rect.y))