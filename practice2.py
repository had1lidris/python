import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.music.load('pygames\Super Mario Bros. Theme Song [TubeRipper.com].mp3')
pygame.mixer.music.set_volume(0.5)  # Set the volume (optional)
pygame.mixer.music.play(-1)  # Play the music in an infinite loop (-1 means loop indefinitely)
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((640, 569))
pygame.display.set_caption("Jumping in PyGame")

score = 0
font_score = pygame.font.Font(None, 36)

block_image = pygame.image.load("pygames\what_0.png")

# Initialize background and enemy positions
bg_move = 0
background = pygame.image.load("pygames\Screenshot 2023-11-20 151508.png")
background_width = background.get_width()
bg_x1, bg_x2 = 0, background_width

enemy = pygame.transform.scale(pygame.image.load('pygames\Screenshot.png'), (50, 50))
enemy_x = 550
enemy_y = 400
enemy_velocity = 2
enemy_direction = 1  # 1 for moving right, -1 for moving left

# Load jumping sound
# Replace 'jump_sound.wav' with the path to your jumping sound file
jump_sound = pygame.mixer.Sound('pygames\Mario Jump Sound Effect.mp3')

# Character class
class Character:
    def __init__(self):
        self.x = 60
        self.y = 360
        self.width = 48  # Adjust according to character image width
        self.height = 64  # Adjust according to character image height
        self.jumping = False
        self.jump_height = 15
        self.y_velocity = self.jump_height
        self.standing_surface = pygame.transform.scale(pygame.image.load("pygames\idle (1).png"), (48, 64))
        self.jumping_surface = pygame.transform.scale(pygame.image.load("pygames\jump.png"), (48, 64))

    def jump(self):
        self.jumping = True

    def update(self):
        if self.jumping:
            self.y -= self.y_velocity
            self.y_velocity -= 0.6

            if self.y_velocity < -self.jump_height:
                self.jumping = False
                self.y_velocity = self.jump_height

    def draw(self, screen):
        if self.jumping:
            screen.blit(self.jumping_surface, (self.x, self.y))
        else:
            screen.blit(self.standing_surface, (self.x, self.y))

# Create an instance of the Character class
player = Character()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_sound.play()
                player.jump()

    keys_pressed = pygame.key.get_pressed()

    bg_move -= 1  # Adjust the speed of the background scrolling
    bg_x2 -= 1
    score += 1

    # Other existing code for background scrolling...
    if bg_move < -background_width:
        bg_move = background_width
    if bg_x2 < -background_width:
        bg_x2 = background_width


    # Update the player character
    player.update()

    # Check collision between player and enemy
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 50, 50)  # Adjust enemy size accordingly

    if player_rect.colliderect(enemy_rect) and not player.jumping:
        # Player collided with enemy and not jumping
        enemy_y = 700  # Move enemy off-screen (simulating falling off)

    # Enemy movement logic
    enemy_x += enemy_velocity * enemy_direction

    if enemy_x <= 0 or enemy_x >= 590:  # Adjust the values based on your screen size and enemy size
        enemy_direction *= -1  # Reverse direction
    
    # Draw the background, player character, and enemy
    SCREEN.blit(background, (bg_move, 0))
    SCREEN.blit(background, (bg_x2, 0))
    player.draw(SCREEN)
    SCREEN.blit(enemy, (enemy_x, enemy_y))


    block_width = 40
    block_height = 40
    block_image_scaled = pygame.transform.scale(block_image, (block_width, block_height))
    SCREEN.blit(block_image_scaled, (200, 200))  # Adjust the coordinates (x, y) as needed


    # Other code for background scrolling, collision detection, etc.
    score_text = font_score.render(f"Time: {score}", True, (255, 255, 255))
    SCREEN.blit(score_text, (10, 10))

    pygame.display.update()
    CLOCK.tick(55)

pygame.quit()
sys.exit()



