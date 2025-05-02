import sys
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

def crop_to_aspect(img, aspect_ratio=(2, 3)):
    w, h = img.size
    target_w = w
    target_h = int(w * aspect_ratio[1] / aspect_ratio[0])
    if target_h > h:
        target_h = h
        target_w = int(h * aspect_ratio[0] / aspect_ratio[1])
    left = (w - target_w) // 2
    top = (h - target_h) // 2
    right = left + target_w
    bottom = top + target_h
    return img.crop((left, top, right, bottom))

def create_polaroid(input_path, output_path, what, when, where, font_path='LexendDeca-Bold.ttf'):
    # Open and crop image
    img = Image.open(input_path).convert('RGB')
    cropped = crop_to_aspect(img, (3, 4))
    # cropped = img
    
    # Set polaroid sizes
    img_w, img_h = cropped.size
    border_top = int(0.05 * img_h)
    border_side = int(0.05 * img_w)
    border_bottom = int(0.25 * img_h)
    polaroid_w = img_w + 2 * border_side
    polaroid_h = int(polaroid_w * (3/2))
    
    # Create white background
    polaroid = Image.new('RGB', (polaroid_w, polaroid_h), 'white')
    polaroid.paste(cropped, (border_side, border_top))
    
    # Draw text
    draw = ImageDraw.Draw(polaroid)
    font_size = int(border_bottom * 0.20)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Upper left (what)
    max_width = polaroid_w // (1/0.6) - border_side
    lines = []
    for line in what.split('\n'):
        # Wrap each line to fit within half the polaroid width
        words = line.split()
        if not words:
            lines.append('')
            continue
        wrapped = []
        current = words[0]
        for word in words[1:]:
            test_line = current + ' ' + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w > max_width:
                wrapped.append(current)
                current = word
            else:
                current = test_line
        wrapped.append(current)
        lines.extend(wrapped)
    x_what = border_side
    y_what = img_h + border_top + int(0.05 * border_bottom)
    for i, line in enumerate(lines):
        draw.text((x_what, y_what + i * (font_size + 2)), line, font=font, fill='black')
    
    # Upper right (where)
    max_width_right = polaroid_w // (1/0.4) - border_side
    right_lines = []
    for line in where.split('\n'):
        words = line.split()
        if not words:
            right_lines.append('')
            continue
        wrapped = []
        current = words[0]
        for word in words[1:]:
            test_line = current + ' ' + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
            if w > max_width_right:
                wrapped.append(current)
                current = word
            else:
                current = test_line
        wrapped.append(current)
        right_lines.extend(wrapped)
    x_where = polaroid_w - border_side
    y_where = y_what
    for i, line in enumerate(right_lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        w_line = bbox[2] - bbox[0]
        draw.text((x_where - w_line, y_where + i * (font_size + 2)), line, font=font, fill='black')

    # Move 'when' text down if needed
    x_when = border_side
    y_when = y_what + len(lines) * (font_size + 2) + 8
    draw.text((x_when, y_when), when, font=font, fill='black')
    
    polaroid.save(output_path)

def main():
    if len(sys.argv) < 5:
        print("Usage: python main.py <input_image_name> <what> <when> <where>")
        print("Example: python main.py iceskating.jpg 'Ice Skating' 'Jan 9 2025' 'Yost Arena'")
        sys.exit(1)
    input_path = "pictures/" + sys.argv[1]
    # Generate output file name
    base, ext = os.path.splitext(sys.argv[1])
    output_file = base + "_polaroid" + ext
    output_path = "polaroids/" + output_file
    what = sys.argv[2]
    when = sys.argv[3]
    where = sys.argv[4]
    create_polaroid(input_path, output_path, what, when, where)

if __name__ == "__main__":
    main()
