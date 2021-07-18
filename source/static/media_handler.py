import os
from PIL import Image
from flask import url_for, current_app
from source import db
from source.admin_panel_models import Media, Topic, Word, Task


def add_media(item, file):
    """
    @param item: element of structure (Topic, Word, Task) that can have some media attached
    @param file: media file
    @return: instance of added or rewrited(if item already had media) Media model
    """
    filename = file.filename  # asdfagsd.jpg
    ext_type = filename.split('.')[-1]  # .jpg
    if ext_type in ['jpg', 'png', 'svg']:
        file_type = 'image'
        static_path = 'static\image'
        old_media = Media.query.filter_by(id=item.image_id).first()
    elif ext_type in ['mp3', 'wav']:
        file_type = 'audio'
        static_path = 'static\\audio'
        old_media = Media.query.filter_by(id=item.audio_id).first()
    elif ext_type in ['mp4', 'mpeg4'] and isinstance(item, Task):
        file_type = 'video'
        static_path = 'static\\video'
        if item.media['sent_video_id']:
            old_media = Media.query.filter_by(id=item.media['sent_video_id'][0]).first()
        else: old_media = None

    # .../source/static/image/  || .../source/static/audio/ || .../source/static/video/
    filepath = os.path.join(current_app.root_path, static_path)

    # topic_1_image.jpg || word_1_audio.mp3 || task_2_video.mp4
    storage_filename = f'{str(type(item)).split(".")[-1][:-2].lower()}_{item.id}_{file_type}.{ext_type}'

    if old_media:
        old_media.name = storage_filename
        old_media.type = ext_type
        db.session.commit()
        file.save(os.path.join(filepath, storage_filename))

        return old_media

    else:
        if isinstance(item, Topic):
            new_media = Media(name=storage_filename, type=ext_type, file_path=filepath, topic_image_fk=item.id)
        if isinstance(item, Word) and file_type == 'image':
            new_media = Media(name=storage_filename, type=ext_type, file_path=filepath, word_image_fk=item.id)
        if isinstance(item, Word) and file_type == 'audio':
            new_media = Media(name=storage_filename, type=ext_type, file_path=filepath, word_audio_fk=item.id)
        if isinstance(item, Task) and file_type == 'video':
            new_media = Media(name=storage_filename, type=ext_type, file_path=filepath, task_video_fk=item.id)
        else:
            new_media = None

        db.session.add(new_media)
        db.session.commit()
        file.save(os.path.join(filepath, storage_filename))

        return new_media

        # pic = Image.open(item)
        # output_size = (200, 200)
        # pic.thumbnail(output_size)
        # pic.save(filepath)
