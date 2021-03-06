import os
from PIL import Image
from flask import url_for, current_app
from werkzeug.utils import secure_filename

def add_auction_image(pic_upload):
    storage_filename = secure_filename(pic_upload.filename)
    
    filepath = os.path.join(current_app.root_path, 'static/auction_images', storage_filename)
    pic = Image.open(pic_upload)
    pic.save(filepath)

    return storage_filename