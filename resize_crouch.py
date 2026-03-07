from PIL import Image
import os

def resize_crouch_sprite(folder_path, target_size=(56, 56)):  # Bigger than 48x48 but smaller than 64x64
    """Resize crouch sprite to be bigger but still smaller than other sprites"""
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    for filename in files:
        filepath = os.path.join(folder_path, filename)
        img = Image.open(filepath)

        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Resize to target size
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Save back
        img.save(filepath)
        print(f"Resized crouch sprite: {filename} to {target_size}")

# Process crouch folder
crouch_folder = r'c:\Users\User\My game\astro_crouch'
print("Resizing crouch sprite to be bigger...")
resize_crouch_sprite(crouch_folder)

print("Done! Crouch sprite is now bigger.")