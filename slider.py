import pygame

class Slider:
    def __init__(self, pos, width, height, min_value, max_value,initial_value):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.knob_radius = height // 2
        self.pos = pos
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.dragging = False

    def draw(self, screen):
        # Menggambar bagian slider yang diisi dengan warna putih sesuai dengan nilai volume
        fill_width = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width)
        fill_rect = pygame.Rect(self.pos[0], self.pos[1] - self.height // 2, fill_width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), fill_rect)

        # Menggambar frame slider
        pygame.draw.rect(screen, (255, 255, 255), (self.pos[0], self.pos[1] - self.height // 2, self.width, self.height), 2)
        pygame.draw.circle(screen, (255, 0, 0), (self.get_knob_pos(), self.rect.centery-20), self.knob_radius)

    def get_knob_pos(self):
        return int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width + self.rect.left)

    def check_for_input(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_value(self, mouse_pos):
        self.value = (mouse_pos[0] - self.rect.left) / self.rect.width * (self.max_value - self.min_value) + self.min_value

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
