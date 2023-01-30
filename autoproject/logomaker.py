# logomaker main file. Run this file to start the application. The Dockerfile is also preconfigured to run this file.
import cairo


def generate_logo(text, font, width, height):
    # Create a new image surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    # Create a new cairo context
    ctx = cairo.Context(surface)

    # Set the font size
    font_size = 150

    # Set the font type
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    # Set the font size
    ctx.set_font_size(font_size)

    # Get the text extents
    x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = ctx.text_extents(text)

    # Check if the text is too wide for the image
    while text_width > width or text_height > height:
        # Decrease the font size
        font_size -= 1
        ctx.set_font_size(font_size)
        x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = ctx.text_extents(text)

    # center the text horizontally and vertically
    ctx.move_to((width / 2) - (text_width / 2) - x_bearing, (height / 2) - (text_height / 2) - y_bearing)

    # Draw the text
    ctx.show_text(text)

    # Write the image to a file
    surface.write_to_png("logo.png")


if __name__ == "__main__":
    generate_logo(text="Pi-X", font="Segoe UI", width=500, height=100)

