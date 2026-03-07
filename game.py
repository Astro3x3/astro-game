import pygame
import sys
import os
from pathlib import Path

pygame.init()

# ------------------------------
# Screen setup
# ------------------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astro Boy Game")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)

# ------------------------------
# Load sprites from folders
# ------------------------------
def load_sprites_from_folder(folder_name):
    """Load all PNG images from a folder and sort them."""
    frames = []
    folder_path = Path(folder_name)
    
    if not folder_path.exists():
        print(f"WARNING: Folder {folder_name} not found!")
        return frames
    
    # Get all PNG files and sort them
    png_files = sorted(folder_path.glob("*.png"))
    
    for file in png_files:
        try:
            img = pygame.image.load(str(file)).convert_alpha()
            frames.append(img)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    return frames

# Load animation frames from each folder
stand_frames = load_sprites_from_folder("astro_stand")
walk_frames = load_sprites_from_folder("astro_walk")
jump_frames = load_sprites_from_folder("astro_jump")

print(f"Loaded - Stand: {len(stand_frames)}, Walk: {len(walk_frames)}, Jump: {len(jump_frames)}")

# ------------------------------

# ------------------------------
# Player setup
# ------------------------------
player_x = 100
player_y = 400
player_speed = 5
velocity_y = 0
gravity = 0.5
jump_power = -10
on_ground = True

# Animation
frame_index = 0
animation_speed = 0.1
state = "stand"  # stand, walk, jump
facing_right = True

# Get default images for each state
def get_current_frame():
    """Get the current animation frame based on state."""
    if state == "stand" and stand_frames:
        return stand_frames[int(frame_index) % len(stand_frames)]
    elif state == "walk" and walk_frames:
        return walk_frames[int(frame_index) % len(walk_frames)]
    elif state == "jump" and jump_frames:
        return jump_frames[int(frame_index) % len(jump_frames)]
    elif stand_frames:
        return stand_frames[0]
    return None

# Get initial image size
test_image = get_current_frame()
if test_image:
    player_width = test_image.get_width()
    player_height = test_image.get_height()
else:
    player_width = 50
    player_height = 50

# Create player rect
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# ------------------------------
# Game loop
# ------------------------------
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Convert to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input handling
    keys = pygame.key.get_pressed()
    moving = False

    # Simple movement
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
        facing_right = False
        moving = True
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
        facing_right = True
        moving = True
    if keys[pygame.K_UP] and on_ground:
        velocity_y = jump_power
        on_ground = False
    else:
        # Determine state based on movement
        if not on_ground:
            state = "jump"
            # Show different jump frames based on direction
            if jump_frames and len(jump_frames) >= 2:
                if velocity_y > 0:
                    # When falling down, show the falling jump frame (astro_jump4)
                    frame_index = len(jump_frames) - 1
                else:
                    # When going up, show the first jump frame (astro_jump2)
                    frame_index = 0
        elif moving:
            state = "walk"
        else:
            state = "stand"

    # Gravity
    velocity_y += gravity
    player_rect.y += velocity_y

    # Ground collision
    if player_rect.bottom >= HEIGHT - 50:
        player_rect.bottom = HEIGHT - 50
        velocity_y = 0
        on_ground = True

    # Update animation
    frame_index += animation_speed
    
    # Get current frame
    current_image = get_current_frame()
    if current_image is None:
        print("ERROR: No frames available!")
        break

    # Flip if facing left
    if not facing_right:
        current_image = pygame.transform.flip(current_image, True, False)

    # Draw
    screen.fill(WHITE)
    screen.blit(current_image, player_rect)
    pygame.display.update()

pygame.quit()
sys.exit()