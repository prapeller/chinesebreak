# coding: utf-8
from source import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(admin_id)


class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    status = db.Column(db.Enum('manager', 'super'))

    langs = db.relationship('Lang', backref='creator_admin')
    courses = db.relationship('Course', backref='creator_admin')
    topics = db.relationship('Topic', backref='creator_admin')
    lessons = db.relationship('Lesson', backref='creator_admin')
    tasks = db.relationship('Task', backref='creator_admin')

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.status = 'manager'

    def __repr__(self):
        return f'id: {self.id}, ' \
               f'email: {self.email}, ' \
               f'status: {self.status}\n'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class TaskType(db.Model):
    __tablename__ = 'task_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='type')


class Lang(db.Model):
    __tablename__ = 'langs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)

    creator_admin_id = db.Column(db.ForeignKey('admins.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    courses = db.relationship('Course', backref='lang')

    def __init__(self, name, creator_admin_id):
        self.name = name
        self.creator_admin_id = creator_admin_id

    def __repr__(self):
        return f'id: {self.id}, \n' \
               f'name: {self.name}, \n' \
               f'is_published: {self.is_published}, \n' \
               f'creator name: {Admin.query.filter_by(id=self.creator_admin_id).first().name}, \n'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)

    creator_admin_id = db.Column(db.ForeignKey('admins.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    lang_id = db.Column(db.ForeignKey('langs.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    topics = db.relationship('Topic', backref='course')

    def __init__(self, name, creator_admin_id, lang_id):
        self.name = name
        self.creator_admin_id = creator_admin_id
        self.lang_id = lang_id

    def __repr__(self):
        return f'id: {self.id}, ' \
               f'name: {self.name}, \n' \
               f'is_published: {self.is_published}, \n' \
               f'creator name: {Admin.query.filter_by(id=self.creator_admin_id).first().name}, \n' \
               f'lang name: {Lang.query.filter_by(id=self.lang_id).first().name}, \n'


class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    media_id = db.Column(db.Integer)

    creator_admin_id = db.Column(db.ForeignKey('admins.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    course_id = db.Column(db.ForeignKey('courses.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    lessons = db.relationship('Lesson', backref='topic')
    # media_ids = db.relationship('Media', backref='topic_')

    def __init__(self, name, creator_admin_id, course_id):
        self.name = name
        self.creator_admin_id = creator_admin_id
        self.course_id = course_id

    def __repr__(self):
        return f'id: {self.id}, ' \
               f'name: {self.name}, \n' \
               f'creator name: {Admin.query.filter_by(id=self.creator_admin_id).first().name}, \n' \
               f'course name: {Course.query.filter_by(id=self.course_id).first().name}, \n'


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    creator_admin_id = db.Column(db.ForeignKey('admins.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    topic_id = db.Column(db.ForeignKey('topics.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    tasks = db.relationship('Task', backref='lesson')

    def __init__(self, creator_admin_id, topic_id):
        self.creator_admin_id = creator_admin_id
        self.topic_id = topic_id

    def __repr__(self):
        return f'id: {self.id}, \n' \
               f'creator: {self.creator_admin_id}, \n' \
               f'topic_id: {self.topic_id}, \n'


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    elements = db.Column(db.JSON, default={
        "words_id": [],
        "grammar_id": [],
        "character_id": [],
        # слова, у которых при прохождении этого задания срабатывает счетчик "правильно"
        "words_id_active_or_to_del": [],
        # слова, которые должны отображаться при показе задания пользователю
        "words_id_to_display": [],
        # неправильные слова
        "words_id_wrong": []
    })
    right_sentences = db.Column(db.JSON, default={
        # предлоежние на китайском
        "sent_char_A": [],
        # предложение на pinyin
        "sent_pinyin_A": [],
        # 'или предложение на русском(которое используется для выбора среди правильных / неправильных или это список элементов пазла которые используются для выбора среди правильных/неправильных элементов пазла и потом будут отображаться во всплывающем окне правильного ответа. Например sent_lang_A": [{"я": 1}, {"-": 0}, {"Чжан Вэй": 1}, {".": 0}] будет означать, что пользователь будет собирать предложение из пазлов "я" и "Чжан Вэй" и еще других неправильных, а во всплывающем окне правильного ответа будет отображаться польностью "Я - Чжан Вэй."
        "sent_lang_A": [],
        # предолжение на русском дословно
        "sent_lit_A": [],
        # все то же самое, используются в случае если задания с диалогами (это вторые реплики)')
        "sent_char_B": [],
        "sent_pinyin_B": [],
        "sent_lang_B": [],
        "sent_lit_B": []
    })
    # 'смысл как в right_sentences, только это списки с неправильными вариантами предложений
    wrong_sentences = db.Column(db.JSON, default={
        "sent_char": [],
        "sent_pinyin": [],
        "sent_lang": []
    })
    # списки с media_id файлов'
    media = db.Column(db.JSON, default={
        # - картинки вариантов ответа для заданий sent_image предложений'
        "sent_images_id": [],
        # картинка правильного варианта ответа
        "sent_images_id_right": [],
        "sent_video_id": [],
        "sent_audio_A_id": [],
        # аудио второй реплики(для диалогов)
        "sent_audio_B_id": []
    })

    task_type_id = db.Column(db.ForeignKey('task_types.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    creator_admin_id = db.Column(db.ForeignKey('admins.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    lesson_id = db.Column(db.ForeignKey('lessons.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    def __init__(self, task_type_id, creator_admin_id, lesson_id):
        self.task_type_id = task_type_id
        self.creator_admin_id = creator_admin_id
        self.lesson_id = lesson_id

    def __repr__(self):
        return f'id: {self.id}, type: {TaskType.query.filter_by(id=self.task_type_id).first().name}, \n' \
               f'creator: {self.creator_admin_id}, \n' \
               f'lesson: {self.lesson_id}, \n'


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    type = db.Column(db.Enum('mp4', 'mp3', 'png', 'jpg', 'gif', 'pdf', 'svg'))
    file_path = db.Column(db.String(2083))

    # topic_id_pic_fk = db.Column(db.ForeignKey('topics.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)


# class Character(db.Model):
#     __tablename__ = 'character'
#
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     topic_id = db.Column(db.ForeignKey('topic.id'), index=True)
#     char = db.Column(db.String(50), nullable=False, index=True)
#     pinyin = db.Column(db.String(50), nullable=False, index=True)
#     lang = db.Column(db.String(50), nullable=False, index=True)
#     image_media_id = db.Column(db.ForeignKey('media.id'), index=True)
#     audio_media_id = db.Column(db.ForeignKey('media.id'), index=True)
#     char_anim = db.Column(db.JSON, nullable=False)
#
#     audio_media = db.relationship('Media', primaryjoin='Character.audio_media_id == Media.id')
#     image_media = db.relationship('Media', primaryjoin='Character.image_media_id == Media.id')
#     topic = db.relationship('Topic')
#
#
# class Grammar(db.Model):
#     __tablename__ = 'grammar'
#
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     topic_id = db.Column(db.ForeignKey('topic.id'), index=True)
#     name = db.Column(db.String(512), nullable=False, index=True)
#     explanation = db.Column(db.Text, index=True)
#     char = db.Column(db.String(512), nullable=False)
#     pinyin = db.Column(db.String(512), nullable=False)
#     lang = db.Column(db.String(512), nullable=False)
#     lit = db.Column(db.String(512), nullable=False)
#     structure = db.Column(db.String(512), nullable=False)
#
#     topic = db.relationship('Topic')
#
#
# class Word(db.Model):
#     __tablename__ = 'word'
#
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     topic_id = db.Column(db.ForeignKey('topic.id'), index=True)
#     char = db.Column(db.String(50), index=True)
#     pinyin = db.Column(db.String(50), index=True)
#     lang = db.Column(db.String(50), index=True)
#     lit = db.Column(db.String(50), index=True)
#     image_media_id = db.Column(db.ForeignKey('media.id'), index=True)
#     audio_media_id = db.Column(db.ForeignKey('media.id'), index=True)
#
#     audio_media = db.relationship('Media', primaryjoin='Word.audio_media_id == Media.id')
#     image_media = db.relationship('Media', primaryjoin='Word.image_media_id == Media.id')
#     topic = db.relationship('Topic')
