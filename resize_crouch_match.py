from PIL import Image
import os

def resize_crouch_to_match_others(folder_path, target_size=(64, 64)):  # Same size as other sprites
    """Resize crouch sprite to match the size of other sprites"""
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    for filename in files:
        filepath = os.path.join(folder_path, filename)
        img = Image.open(filepath)

        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Resize to target size (same as other sprites)
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        # Save back
        img.save(filepath)
        print(f"Resized crouch sprite: {filename} to {target_size} (same as others)")

# Process crouch folder
crouch_folder = r'c:\Users\User\My game\astro_crouch'
print("Resizing crouch sprite to match other sprites...")
resize_crouch_to_match_others(crouch_folder)

print("Done! Crouch sprite is now the same size as other sprites.")