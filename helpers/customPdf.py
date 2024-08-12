from fpdf import FPDF
from PIL import Image

class PDF(FPDF):
    def header(self):
        # Set header font
        self.set_font('Arial', 'B', 12)
        # Add a title
        self.cell(0, 10, 'Generated Questions', 0, 1, 'C')
        # Add a line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Set footer font
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_text(self, text):
        # Add text to PDF
        self.set_font('Times', '', 12)
        # Get current Y position
        y_before = self.get_y()
        # Check if a page break is needed
        if y_before + self.get_string_height(text) > self.h - 15:
            self.add_page()
        # Add the text
        self.multi_cell(0, 10, text)
        # Line break
        self.ln(5)

    def add_image(self, image_path, w=100):
        # Add image to PDF
        # Open image to get its dimensions
        img = Image.open(image_path)
        aspect_ratio = img.height / img.width
        # Calculate height of the image with respect to width
        h = w * aspect_ratio
        # Get current Y position
        y_before = self.get_y()
        # Check if a page break is needed
        if y_before + h > self.h - 15:
            self.add_page()
            y_before = self.get_y()
        # Add the image at the current position
        self.image(image_path, x=10, y=y_before, w=w)
        # Update the Y position after adding the image
        self.set_y(y_before + h + 5)

    def get_string_height(self, text):
        # Method to calculate the height of a string
        return self.get_string_width(text) / self.w * 10