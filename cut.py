from PIL import Image

# Load the sprite sheet
img = Image.open("Astroboy_sprite.png")
width, height = img.size

# Define your grid or manual coordinates
# This is a simplified example to cut the first row (Idle)
# You would adjust these loops to match the spacing of the sheet
tile_width = 64  # Approximate width of one Astroboy frame
tile_height = 64 # Approximate height

for i in range(0, 3): # First 3 frames of Idle
    box = (i * tile_width, 50, (i + 1) * tile_width, 50 + tile_height)
    frame = img.crop(box)
    frame.save(f"astro_idle_{i}.png")