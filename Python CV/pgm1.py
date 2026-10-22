width, height = 5, 5
max_color = 255

# A 5x5 grid of RGB values (Red, Blue, White, Black)
pixels = [
    [255,0,0],   [255,0,0],   [255,255,255], [0,0,255],   [0,0,255],
    [255,0,0],   [255,255,255],[255,255,255], [255,255,255],[0,0,255],
    [255,255,255],[255,255,255], [0,0,0],     [255,255,255],[255,255,255],
    [255,0,0],   [255,255,255],[255,255,255], [255,255,255],[0,0,255],
    [255,0,0],   [255,0,0],   [255,255,255], [0,0,255],   [0,0,255]]

with open("input.ppm", "w") as f:
    f.write(f"P3\n{width} {height}\n{max_color}\n")
    for i in range(0, len(pixels), width):
        row_str = "  ".join([f"{p[0]} {p[1]} {p[2]}" for p in pixels[i:i+width]])
        f.write(row_str + "\n")

print("5x5 input.ppm created successfully!")



def read_ppm(file_path):
    """Reads an ASCII PPM (P3) image file into a pure Python data structure."""
    with open(file_path, 'r') as f:
        # Read all text tokens, ignoring comments
        tokens = []
        for line in f:
            if line.startswith('#'):
                continue
            tokens.extend(line.split())
            
    header = tokens[0]
    if header != 'P3':
        raise ValueError("Only ASCII PPM (P3) format is supported.")
        
    width = int(tokens[1])
    height = int(tokens[2])
    max_color = int(tokens[3])
    
    # Extract flat list of pixel values
    pixel_data = [int(x) for x in tokens[4:]]
    
    # Restructure into a 3D matrix: [row][column][R, G, B]
    pixels = []
    idx = 0
    for r in range(height):
        row = []
        for c in range(width):
            pixel = [pixel_data[idx], pixel_data[idx+1], pixel_data[idx+2]]
            row.append(pixel)
            idx += 3
        pixels.append(row)
        
    return pixels, width, height, max_color

def write_ppm(pixels, width, height, max_color, output_path):
    """Writes a 3D pixel matrix back to an ASCII PPM file."""
    with open(output_path, 'w') as f:
        f.write(f"P3\n{width} {height}\n{max_color}\n")
        for row in pixels:
            row_strings = []
            for pixel in row:
                row_strings.append(f"{pixel[0]} {pixel[1]} {pixel[2]}")
            f.write("  ".join(row_strings) + "\n")

def convert_to_grayscale(pixels):
    new_pixels = []
    for row in pixels:
        new_row = []
        for pixel in row:
            # Weighted luminosity formula for realistic grayscale
            gray = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
            new_row.append([gray, gray, gray])
        new_pixels.append(new_row)
    return new_pixels

def adjust_brightness(pixels, value):
    new_pixels = []
    for row in pixels:
        new_row = []
        for pixel in row:
            r = min(255, max(0, pixel[0] + value))
            g = min(255, max(0, pixel[1] + value))
            b = min(255, max(0, pixel[2] + value))
            new_row.append([r, g, b])
        new_pixels.append(new_row)
    return new_pixels

def flip_horizontal(pixels):
    return [row[::-1] for row in pixels]

def main():
    input_file = "input.ppm"
    
    print("Reading image...")
    pixels, width, height, max_color = read_ppm(input_file)
    print(f"Loaded successfully! Dimensions: {width}x{height}")
    
    # 1. Apply Grayscale
    print("Applying Grayscale filter...")
    gray_pixels = convert_to_grayscale(pixels)
    write_ppm(gray_pixels, width, height, max_color, "output_gray.ppm")
    
    # 2. Apply Brightness
    print("Boosting brightness...")
    bright_pixels = adjust_brightness(pixels, 50)
    write_ppm(bright_pixels, width, height, max_color, "output_bright.ppm")
    
    # 3. Mirror the image
    print("Flipping image...")
    flipped_pixels = flip_horizontal(pixels)
    write_ppm(flipped_pixels, width, height, max_color, "output_flipped.ppm")
    
    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()
