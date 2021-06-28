# source/structure/picture_handler.py

import os
from PIL import Image
from flask import url_for, current_app
from source import db
from source.admin_panel_models import Media


def add_topic_image(topic, image):
    upl_filename = image.filename  # asdfagsd.jpg
    ext_type = upl_filename.split('.')[-1]  # .jpg
    storage_filename = f'topic_{topic.id}_image.{ext_type}'  # topic_1_image.jpg
    filepath = os.path.join(current_app.root_path, 'static\image',
                            storage_filename)  # .../source/static/image/topic_1_image.jpg

    old_media = Media.query.filter_by(id=topic.image_id).first()
    if old_media:
        old_media.name = storage_filename
        old_media.type = ext_type
        db.session.commit()

        pic = Image.open(image)
        output_size = (200, 200)
        pic.thumbnail(output_size)
        pic.save(filepath)

        return old_media
    else:
        new_media = Media(name=storage_filename, type=ext_type, file_path=filepath, topic_image_fk=topic.id)
        db.session.add(new_media)
        db.session.commit()

        pic = Image.open(image)
        output_size = (200, 200)
        pic.thumbnail(output_size)
        pic.save(filepath)

        return new_media


# def add_word_image(word, image):
#     count = Media.query.filter_by()
#
#     filename = image.filename  # asdfagsd.jpg
#     ext_type = filename.split('.')[-1]  # .jpg
#     storage_filename = f'word_{word.id}_image_.{ext_type}'  # topic_1_image.jpg
#     filepath = os.path.join(current_app.root_path, 'static\image', storage_filename)
#     # .../source/static/image/word_1_image_1.jpg
#     # .../source/static/image/word_1_image_2.jpg
#     # .../source/static/image/word_1_image_3.jpg
#     # .../source/static/image/word_1_image_4.jpg
#
#     new_media = Media(name=storage_filename, type=ext_type, file_path=filepath, topic_picture_fk=word.id)
#     db.session.add(new_media)
#     db.session.commit()
#
#     pic = Image.open(image)
#     output_size = (200, 200)
#     pic.thumbnail(output_size)
#     pic.save(filepath)
#
#     return new_media
