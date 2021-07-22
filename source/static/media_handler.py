import os
from PIL import Image
from flask import current_app
from source import db
from source.admin_panel_models import Media, Topic, Word, Task


def add_to_task_video(task, file):
    filename = file.filename  # asdfagsd.mp4
    ext_type = filename.split('.')[-1]  # mp4
    file_type = 'video'
    static_path = 'static\\video'
    filepath = os.path.join(current_app.root_path, static_path)  # .../source/static/video/
    storage_filename = f'{str(type(task)).split(".")[-1][:-2].lower()}_{task.id}_{file_type}.{ext_type}'  # task_2_video.png
    file.save(os.path.join(filepath, storage_filename))

    if task.media['sent_video_id']:
        media = Media.query.filter_by(id=task.media['sent_video_id'][0]).first()
        media.name = storage_filename
        media.type = ext_type
    else:
        media = Media(name=storage_filename, type=ext_type, file_path=filepath, task_video_fk=task.id)
        db.session.add(media)
    db.session.commit()

    return media


def add_to_topic_image(topic, file):
    filename = file.filename  # asdfagsd.jpg
    ext_type = filename.split('.')[-1]  # jpg\
    file_type = 'image'
    static_path = 'static\image'
    filepath = os.path.join(current_app.root_path,
                            static_path)  # .../source/static/image/  || .../source/static/audio/ || .../source/static/video/
    storage_filename = f'{str(type(topic)).split(".")[-1][:-2].lower()}_{topic.id}_{file_type}.{ext_type}'  # task_2_image_0.png / task_2_image_1.png
    file.save(os.path.join(filepath, storage_filename))

    media = Media.query.filter_by(id=topic.image_id).first()
    if media:
        media.name = storage_filename
        media.type = ext_type
    else:
        media = Media(name=storage_filename, type=ext_type, file_path=filepath, topic_image_fk=topic.id)
        db.session.add(media)
    db.session.commit()

    return media


def add_to_word_image(word, file):
    assert isinstance(word, Word)
    filename = file.filename  # asdfagsd.jpg
    ext_type = filename.split('.')[-1]  # jpg\
    file_type = 'image'
    static_path = 'static\image'
    filepath = os.path.join(current_app.root_path,
                            static_path)  # .../source/static/image/  || .../source/static/audio/ || .../source/static/video/
    storage_filename = f'{str(type(word)).split(".")[-1][:-2].lower()}_{word.id}_{file_type}.{ext_type}'  # task_2_image_0.png / task_2_image_1.png
    pic = Image.open(file)
    pic.thumbnail((160, 160))
    pic.save(os.path.join(filepath, storage_filename))

    media = Media.query.filter_by(id=word.image_id).first()
    if media:
        media.name = storage_filename
        media.type = ext_type
    else:
        media = Media(name=storage_filename, type=ext_type, file_path=filepath, word_image_fk=word.id)
        db.session.add(media)
    db.session.commit()

    return media


def add_to_task_image(task, file):
    filename = file.filename  # asdfagsd.jpg
    ext_type = filename.split('.')[-1]  # jpg\
    file_type = 'image'
    static_path = 'static\image'
    filepath = os.path.join(current_app.root_path,
                            static_path)  # .../source/static/image/  || .../source/static/audio/ || .../source/static/video/
    count = len(task.media['sent_images_id'])
    storage_filename = f'{str(type(task)).split(".")[-1][:-2].lower()}_{task.id}_{file_type}_{count}.{ext_type}'  # task_2_image_0.png / task_2_image_1.png
    pic = Image.open(file)
    pic.thumbnail((160, 160))
    pic.save(os.path.join(filepath, storage_filename))
    new_media = Media(name=storage_filename, type=ext_type, file_path=filepath)
    db.session.add(new_media)
    db.session.commit()

    return new_media


def add_to_word_audio(word, file):
    filename = file.filename  # asdfagsd.mp3
    ext_type = filename.split('.')[-1]  # mp3\
    assert ext_type in ['mp3', 'wav']
    file_type = 'audio'
    static_path = 'static\\audio'
    filepath = os.path.join(current_app.root_path, static_path)  # .../source/static/audio/
    storage_filename = f'{str(type(word)).split(".")[-1][:-2].lower()}_{word.id}_{file_type}.{ext_type}'  # task_2_image_0.png / task_2_image_1.png
    file.save(os.path.join(filepath, storage_filename))

    media = Media.query.filter_by(id=word.audio_id).first()
    if media:
        media.name = storage_filename
        media.type = ext_type
    else:
        media = Media(name=storage_filename, type=ext_type, file_path=filepath, word_audio_fk=word.id)
        db.session.add(media)
    db.session.commit()

    return media


def add_to_task_sent_A_audio(task, file):
    filename = file.filename  # asdfagsd.mp3
    ext_type = filename.split('.')[-1]  # mp3\
    assert ext_type in ['mp3']
    file_type = 'audio'
    static_path = 'static\\audio'
    filepath = os.path.join(current_app.root_path, static_path)  # .../source/static/audio/
    storage_filename = f'task_{task.id}_sent_A_audio.{ext_type}'  # task_2_sent_A_audio.mp3
    file.save(os.path.join(filepath, storage_filename))

    if task.media.get('sent_audio_A_id'):
        media = Media.query.filter_by(id=task.media.get('sent_audio_A_id')[0]).first()
        media.name = storage_filename
        media.type = ext_type
    else:
        media = Media(name=storage_filename, type=ext_type, file_path=filepath)
        db.session.add(media)
    db.session.commit()

    return media
