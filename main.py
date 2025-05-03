import pygame
import random
import math
from pygame import mixer

class Game:
    def __init__(self):
        # Initialize pygame modules
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        
        # Game constants
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.FPS = 60
        
        # Initialize game window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Niazi Invader")
        
        # Load assets
        self.load_assets()
        
        # Initialize game state
        self.score = 0
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Initialize game objects
        self.init_player()
        self.init_enemies(5)
        self.init_bullet()
    
    def load_assets(self):
        """Load all game assets (images, sounds, fonts)"""
        # Images
        self.background = pygame.image.load('media/background/background.png')
        self.icon = pygame.image.load('media/icons/niazi_invader.png')
        pygame.display.set_icon(self.icon)
        self.ship_img = pygame.image.load('media/icons/ship.png')
        self.bullet_img = pygame.image.load('media/icons/bullet.png')
        
        # Fonts
        self.font = pygame.font.Font('FreeSansBold.ttf', 32)
        self.game_over_font = pygame.font.Font('FreeSansBold.ttf', 64)
        
        # Sounds
        mixer.music.load('media/audio/Game_Start.mp3')
        self.bullet_sound = mixer.Sound('media/audio/laser.mp3')
        self.explosion_sound = mixer.Sound('media/audio/explosion.mp3')
        self.game_over_sound = mixer.Sound('media/audio/Game_Over.mp3')
    
    def init_player(self):
        """Initialize player ship"""
        self.ship_x = 370
        self.ship_y = 480
        self.ship_move_x = 0
        self.ship_speed = 2
    
    def init_enemies(self, num_enemies):
        """Initialize enemies"""
        self.niazi_img = []
        self.niazi_x = []
        self.niazi_y = []
        self.niazi_move_x = []
        self.niazi_move_y = []
        self.num_niazi = num_enemies
        
        for _ in range(self.num_niazi):
            self.niazi_img.append(pygame.image.load('media/icons/niazi_invader.png'))
            self.niazi_x.append(random.randint(0, 660))
            self.niazi_y.append(random.randint(50, 150))
            self.niazi_move_x.append(1)
            self.niazi_move_y.append(40)
    
    def init_bullet(self):
        """Initialize bullet"""
        self.bullet_x = 0
        self.bullet_y = 480
        self.bullet_speed = 5
        self.bullet_state = "ready"  # "ready" or "fire"
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Keyboard input handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.ship_move_x = -self.ship_speed
                if event.key == pygame.K_RIGHT:
                    self.ship_move_x = self.ship_speed
                if event.key == pygame.K_SPACE and self.bullet_state == "ready":
                    self.fire_bullet()
            
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.ship_move_x = 0
    
    def fire_bullet(self):
        """Fire the bullet from player's position"""
        self.bullet_state = "fire"
        self.bullet_x = self.ship_x
        self.bullet_y = self.ship_y
        self.bullet_sound.play()
    
    def update_player(self):
        """Update player position and boundaries"""
        self.ship_x += self.ship_move_x
        
        # Keep player within screen bounds
        self.ship_x = max(0, min(self.ship_x, self.SCREEN_WIDTH - 64))
    
    def update_enemies(self):
        """Update all enemy positions and check for game over"""
        game_over = False
        
        for i in range(self.num_niazi):
            # Game Over condition
            if self.niazi_y[i] > 340:
                game_over = True
                break
                
            # Enemy movement
            self.niazi_x[i] += self.niazi_move_x[i]
            
            # Boundary checking and direction change
            if self.niazi_x[i] <= 0:
                self.niazi_move_x[i] = 1
                self.niazi_y[i] += self.niazi_move_y[i]
            elif self.niazi_x[i] >= 670:
                self.niazi_move_x[i] = -1
                self.niazi_y[i] += self.niazi_move_y[i]
            
            # Collision detection
            if self.check_collision(self.niazi_x[i], self.niazi_y[i], self.bullet_x, self.bullet_y):
                self.handle_collision(i)
        
        if game_over:
            self.game_over()
    
    def check_collision(self, enemy_x, enemy_y, bullet_x, bullet_y):
        """Check if bullet collides with enemy"""
        distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
        return distance < 30
    
    def handle_collision(self, enemy_index):
        """Handle collision between bullet and enemy"""
        self.explosion_sound.play()
        self.bullet_state = "ready"
        self.bullet_y = 480
        self.score += 1
        
        # Respawn enemy
        self.niazi_x[enemy_index] = random.randint(0, 670)
        self.niazi_y[enemy_index] = random.randint(50, 150)
    
    def update_bullet(self):
        """Update bullet position and state"""
        if self.bullet_state == "fire":
            self.bullet_y -= self.bullet_speed
            if self.bullet_y <= 0:
                self.bullet_state = "ready"
                self.bullet_y = 480
    
    def game_over(self):
        """Handle game over state"""
        for i in range(self.num_niazi):
            self.niazi_y[i] = 1000  # Move enemies off-screen
        self.game_over_sound.play()
    
    def draw(self):
        """Draw all game objects"""
        # Draw background
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        
        # Draw player
        self.screen.blit(self.ship_img, (self.ship_x, self.ship_y))
        
        # Draw enemies
        for i in range(self.num_niazi):
            self.screen.blit(self.niazi_img[i], (self.niazi_x[i], self.niazi_y[i]))
        
        # Draw bullet if fired
        if self.bullet_state == "fire":
            self.screen.blit(self.bullet_img, (self.bullet_x + 16, self.bullet_y + 10))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over if needed
        if any(y > 340 for y in self.niazi_y):
            game_over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
            self.screen.blit(game_over_text, (200, 250))
        
        pygame.display.update()
    
    def run(self):
        """Main game loop"""
        mixer.music.play()
        
        while self.running:
            # self.clock.tick(self.FPS)
            self.handle_events()
            self.update_player()
            self.update_bullet()
            self.update_enemies()
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()