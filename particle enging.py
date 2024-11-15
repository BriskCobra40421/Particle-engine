import pygame
import pygame_gui
import random
import math

# Initialize Pygame and pygame_gui
pygame.init()
pygame.display.set_caption("Particle Engine with Controls")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((800, 600))

# Particle class
class Particle:
    def __init__(self, pos, vel, color, size, shape):
        self.pos = pos
        self.vel = vel
        self.color = color
        self.size = size
        self.shape = shape
        self.lifetime = random.randint(50, 100)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.lifetime -= 1

    def draw(self, screen):
        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.size)
        elif self.shape == 'square':
            pygame.draw.rect(screen, self.color, (int(self.pos[0]), int(self.pos[1]), self.size, self.size))
        elif self.shape == 'triangle':
            point1 = (self.pos[0], self.pos[1] - self.size)
            point2 = (self.pos[0] - self.size, self.pos[1] + self.size)
            point3 = (self.pos[0] + self.size, self.pos[1] + self.size)
            pygame.draw.polygon(screen, self.color, [point1, point2, point3])
        elif self.shape == 'star':
            points = [
                (self.pos[0], self.pos[1] - self.size),
                (self.pos[0] + self.size * 0.5, self.pos[1] - self.size * 0.3),
                (self.pos[0] + self.size, self.pos[1] - self.size),
                (self.pos[0] + self.size * 0.5, self.pos[1] + self.size * 0.3),
                (self.pos[0] + self.size, self.pos[1] + self.size),
                (self.pos[0], self.pos[1] + self.size * 0.5),
                (self.pos[0] - self.size, self.pos[1] + self.size),
                (self.pos[0] - self.size * 0.5, self.pos[1] + self.size * 0.3),
                (self.pos[0] - self.size, self.pos[1] - self.size),
                (self.pos[0] - self.size * 0.5, self.pos[1] - self.size * 0.3),
            ]
            pygame.draw.polygon(screen, self.color, points)
        elif self.shape == 'hexagon':
            angle_offset = math.pi / 3
            points = [
                (self.pos[0] + self.size * math.cos(angle_offset * i),
                 self.pos[1] + self.size * math.sin(angle_offset * i))
                for i in range(6)
            ]
            pygame.draw.polygon(screen, self.color, points)

# Particle Engine class
class ParticleEngine:
    def __init__(self, pos, color=(255, 255, 255), size=5, quantity=50, shape='circle'):
        self.pos = pos
        self.color = color
        self.size = size
        self.quantity = quantity
        self.shape = shape
        self.particles = []

    def emit(self):
        for _ in range(self.quantity):
            vel = [random.uniform(-2, 2), random.uniform(-2, 2)]
            self.particles.append(Particle(self.pos[:], vel, self.color, self.size, self.shape))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

# UI Elements
size_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect((20, 540), (200, 30)), start_value=10, value_range=(1, 50), manager=manager)
quantity_slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pygame.Rect((250, 540), (200, 30)), start_value=30, value_range=(1, 100), manager=manager)

color_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 540), (100, 30)),
                                            text='Change Color', manager=manager)
emit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 540), (100, 30)),
                                           text='Emit Particles', manager=manager)

# Shape selection dropdown
shape_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['circle', 'square', 'triangle', 'star', 'hexagon'],
    starting_option='circle',
    relative_rect=pygame.Rect((620, 500), (120, 30)),
    manager=manager
)

# Particle engine
particle_engine = ParticleEngine(pos=[400, 300], color=(0, 128, 255), size=10, quantity=30)

# Text labels for sliders
font = pygame.font.Font(None, 24)
size_text = font.render("Particle Size", True, (255, 255, 255))
quantity_text = font.render("Particle Quantity", True, (255, 255, 255))

running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill((30, 30, 30))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == color_button:
                    particle_engine.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                elif event.ui_element == emit_button:
                    particle_engine.emit()
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == shape_dropdown:
                particle_engine.shape = event.text
        manager.process_events(event)

    # Update particle engine settings based on UI
    particle_engine.size = int(size_slider.get_current_value())
    particle_engine.quantity = int(quantity_slider.get_current_value())

    # Update and draw particles
    particle_engine.update()
    particle_engine.draw(screen)

    # Draw UI
    screen.blit(size_text, (20, 510))  # Text above size slider
    screen.blit(quantity_text, (250, 510))  # Text above quantity slider

    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
