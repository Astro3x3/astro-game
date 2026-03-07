from PIL import Image
import os

def remove_background_and_resize(folder_path, target_size=(64, 64)):
    """Remove background from sprites and resize to target size"""
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        img = Image.open(filepath)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get image data
        data = img.getdata()
        new_data = []
        
        # Remove gray background (adjust RGB values as needed)
        for item in data:
            # If pixel is light gray (background), make it transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        
        img.putdata(new_data)
        
        # Resize to target size
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Save back
        img.save(filepath)
        print(f"Processed: {filename}")

# Process jump folder
jump_folder = r'c:\Users\User\My game\astro_shoot'
print("Processing jump sprites...")
remove_background_and_resize(jump_folder)

print("Done! All jump sprites processed.")