import re


class AxisValidator:

    def validate(self, labels):

        corrected = []

        previous = None

        for label in labels:

            # Keep only digits
            label = re.sub(r"\D", "", label)

            # Skip invalid labels
            if len(label) != 6:
                continue

            year = int(label[:4])
            week = int(label[4:])

            # Fix OCR mistakes

            if year == 2023 and week >= 50:
                year = 2025

            if year == 2024:
                year = 2026

            # Clamp week

            if week < 1:
                week = 1

            if week > 53:
                week = 53

            new_label = f"{year}{week:02d}"

            # Remove duplicates
            if new_label != previous:
                corrected.append(new_label)
                previous = new_label

            

        return corrected
