#!/usr/bin/env python3
import os
import shutil
from datetime import datetime
from PIL import Image
from pathlib import Path

class PhotoOrganizer:
    DATETIME_EXIF_INFO_ID = 36867
    extensions = ['jpg', 'jpeg', 'png']

    def folder_path_from_photo_date(self, file):
        date = self.photo_shooting_date(file)
        return date.strftime('%Y') + '/' + date.strftime('%Y-%m-%d')

    def photo_shooting_date(self, file):
        date = None
        photo = Image.open(file)
        if hasattr(photo, '_getexif'):
            info = photo._getexif()
            if info:
                if self.DATETIME_EXIF_INFO_ID in info:
                    date = info[self.DATETIME_EXIF_INFO_ID]
                    date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        if date is None:
            date = datetime.fromtimestamp(os.path.getmtime(file))
        return date

    def move_photo(self, file):
        new_folder = self.folder_path_from_photo_date(file)
        new_path = new_folder + '/' + file
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        else:
            # check if file already exists
            if Path(new_path).exists():
                increment = 0
                while True:
                    increment += 1
                    filename, file_extension = os.path.splitext(new_path)
                    new_path = filename + '(' + str(increment) + ')' + file_extension
                    if not Path(new_path).exists():
                        break

        shutil.move(file, new_path)

    def organize(self):
        photos = [
            filename for filename in os.listdir('.')
                if os.path.isfile(filename) and any(filename.lower().endswith('.' + ext.lower()) for ext in self.extensions)
        ]
        for filename in photos:
            self.move_photo(filename)


PO = PhotoOrganizer()
PO.organize()
