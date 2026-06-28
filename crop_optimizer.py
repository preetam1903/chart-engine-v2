from PIL import Image


class CropOptimizer:

    def __init__(
        self,
        top_expand=0.15,
        bottom_expand=0.25,
        left_expand=0.12,
        right_expand=0.12
    ):
        self.top_expand = top_expand
        self.bottom_expand = bottom_expand
        self.left_expand = left_expand
        self.right_expand = right_expand

    def optimize(self, image, bbox):
        """
        image : PIL Image

        bbox:
        {
            "x": int,
            "y": int,
            "w": int,
            "h": int
        }
        """

        img_w, img_h = image.size

        x = bbox["x"]
        y = bbox["y"]
        w = bbox["w"]
        h = bbox["h"]

        top = int(h * self.top_expand)
        bottom = int(h * self.bottom_expand)
        left = int(w * self.left_expand)
        right = int(w * self.right_expand)

        new_x = max(0, x - left)
        new_y = max(0, y - top)

        new_right = min(img_w, x + w + right)
        new_bottom = min(img_h, y + h + bottom)

        crop = image.crop((new_x, new_y, new_right, new_bottom))

        updated_bbox = {
            "x": new_x,
            "y": new_y,
            "w": new_right - new_x,
            "h": new_bottom - new_y
        }

        metadata = {
            "expanded": True,
            "top_pixels": top,
            "bottom_pixels": bottom,
            "left_pixels": left,
            "right_pixels": right
        }

        return crop, updated_bbox, metadata
