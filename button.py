import pygame

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self._x_pos = pos[0]
		self._y_pos = pos[1]
		self.shadow_offset = 5
		self.shadow_color = (50, 50, 50)
		self._font = font
		self._base_color = base_color 
		self._hovering_color = hovering_color
		self._text_input = text_input
		self._text = self._font.render(self._text_input, True, self._base_color)
		if self.image is None:
			self.image = self._text
		self.rect = self.image.get_rect(center=(self._x_pos, self._y_pos))
		self._text_rect = self._text.get_rect(center=(self._x_pos, self._y_pos))
		self.is_clicked = True

	def check_for_input(self, position):
		# jika posisi x dan y dari mouse dalam rect button, maka button aktif / return true
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
	
	def handle_click(self):
		self.is_clicked = True
			
	def change_color(self, position):
		# jika posisi x dan y dari mouse dalam rect button maka warna button akan berubah
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.rect.inflate_ip(10, 10)
			self._text = self._font.render(self._text_input, True, self._hovering_color)
			self._text_rect.inflate_ip(10, 10)
		# warna base color kembali jika mouse tidak dalam rect button
		else:
			self._text = self._font.render(self._text_input, True, self._base_color)
	def draw_shadow(self, screen):
		shadow_rect = self.rect.copy()
		shadow_rect.x += self.shadow_offset
		shadow_rect.y += self.shadow_offset
		pygame.draw.rect(screen, self.shadow_color, shadow_rect)

	def update(self, screen):
		self.draw_shadow(screen)
		if self.image is not None:
			if self.is_clicked == True:
				self.rect.inflate_ip(-10, -10)
				self._text_rect.inflate_ip(-10, -10)
			screen.blit(self.image, self.rect)
		screen.blit(self._text, self._text_rect)