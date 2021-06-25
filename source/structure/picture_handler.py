# source/structure/picture_handler.py

import os
from PIL import Image
from flask import url_for, current_app
from source import db
from source.admin_panel_models import Media


def add_topic_pic(pic_upload, topic):
    upl_filename = pic_upload.filename  # asdfagsd.jpg
    ext_type = upl_filename.split('.')[-1]  # .jpg
    storage_filename = f'topic_{topic.id}_{topic.name}.{ext_type}'  # topic_1_hello.jpg
    filepath = os.path.join(current_app.root_path, 'static\picture', storage_filename)  # .../source/static/picture/topic_1_hello.jpg

    old_media = Media.query.filter_by(file_path=filepath).first()
    if old_media:
        old_media.name = storage_filename
        db.session.commit()

        pic = Image.open(pic_upload)
        output_size = (200, 200)
        pic.thumbnail(output_size)
        pic.save(filepath)

        return old_media
    else:
        new_media = Media(name=storage_filename, type=ext_type, file_path=filepath)
        db.session.add(new_media)
        db.session.commit()

        pic = Image.open(pic_upload)
        output_size = (200, 200)
        pic.thumbnail(output_size)
        pic.save(filepath)

        return new_media
