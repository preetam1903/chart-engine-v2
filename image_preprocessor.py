from PIL import Image


class ImagePreprocessor:

    def enhance(self, image_path):

        img = Image.open(image_path)

        # Enlarge 3x
        w, h = img.size

        img = img.resize((w * 3, h * 3), Image.LANCZOS)

        # Save
        output = "enhanced_chart.png"

        img.save(output)

        return output
