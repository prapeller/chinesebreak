from flask import render_template, redirect, url_for, Blueprint, session, flash, request
from source.admin_panel_models import Lang, Course, Topic, Lesson, Task, Media
from flask_login import current_user
from source import db

from source.structure.forms import ButtonAddForm, ButtonDeleteForm, NameForm, UploadImageForm, BackButtonForm
from source.static.media_handler import add_media
from source.structure.forms import SelectTaskTypeForm

structure_blueprint = Blueprint('structure', __name__, url_prefix='/structure', template_folder='templates')


@structure_blueprint.route('/', methods=["GET", "POST"])
def structure():
    button_add = ButtonAddForm()

    if button_add.validate_on_submit() and button_add.add.data:
        new_lang = Lang(name='new', creator_admin_id=current_user.id)
        db.session.add(new_lang)
        db.session.commit()
        return redirect(url_for('structure.lang', lang_id=new_lang.id))

    return render_template('structure.html',
                           langs=Lang.query.all(),
                           button_add=button_add)


@structure_blueprint.route('lang_<int:lang_id>/', methods=["GET", "POST"])
def lang(lang_id):
    lang = Lang.query.filter_by(id=lang_id).first()

    name_form = NameForm()
    button_delete = ButtonDeleteForm()
    button_add = ButtonAddForm()

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.structure'))

    if name_form.validate_on_submit() and name_form.name.data:
        lang.name = name_form.name.data
        db.session.commit()
        flash('update success')
    elif request.method == "GET":
        name_form.name.data = lang.name

    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(lang)
        db.session.commit()
        flash('delete success')
        return redirect(url_for('structure.structure'))

    if button_add.validate_on_submit() and button_add.add.data:
        new_course = Course(name='new', creator_admin_id=current_user.id, lang_id=lang.id)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('structure.course', course_id=new_course.id))

    return render_template('lang.html',
                           lang=lang,
                           courses=lang.courses,
                           name_form=name_form,
                           button_delete=button_delete, button_add=button_add, back_btn=back_btn,
                           )


@structure_blueprint.route('course_<int:course_id>/', methods=["GET", "POST"])
def course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    name_form = NameForm()
    button_delete = ButtonDeleteForm()
    button_add = ButtonAddForm()

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.lang', lang_id=course.lang_id))

    if name_form.validate_on_submit() and name_form.name.data:
        course.name = name_form.name.data
        db.session.commit()
        flash('update success')
    elif request.method == "GET":
        name_form.name.data = course.name

    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('structure.lang', lang_id=course.lang_id))

    if button_add.validate_on_submit() and button_add.add.data:
        new_topic = Topic(name='new',
                          creator_admin_id=current_user.id,
                          course_id=course.id)
        db.session.add(new_topic)
        db.session.commit()
        return redirect(url_for('structure.topic', topic_id=new_topic.id))

    return render_template('course.html',
                           Media=Media,
                           course=course,
                           topics=course.topics,
                           name_form=name_form,
                           button_delete=button_delete, button_add=button_add, back_btn=back_btn,
                           )


@structure_blueprint.route('topic_<int:topic_id>/', methods=["GET", "POST"])
def topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    image = Media.query.filter_by(id=topic.image_id).first()
    image_name = image.name if image else 'none'

    name_form = NameForm()
    button_add = ButtonAddForm()
    topic_image_form = UploadImageForm()
    button_delete = ButtonDeleteForm()

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.course', course_id=topic.course_id))

    if name_form.validate_on_submit() and name_form.name.data:
        topic.name = name_form.name.data
        db.session.commit()
        flash('update success')
    elif request.method == "GET":
        name_form.name.data = topic.name

    if topic_image_form.validate_on_submit() and topic_image_form.image.data:
        image_media = add_media(item=topic, file=topic_image_form.image.data)
        topic.image_id = image_media.id
        db.session.commit()
        return redirect(url_for('structure.topic', topic_id=topic.id))

    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(topic)
        db.session.commit()
        return redirect(url_for('structure.course', course_id=topic.course_id))

    if button_add.validate_on_submit() and button_add.add.data:
        new_lesson = Lesson(creator_admin_id=current_user.id, topic_id=topic.id)
        db.session.add(new_lesson)
        db.session.commit()
        return redirect(url_for('structure.lesson', lesson_id=new_lesson.id))

    return render_template('topic.html',
                           topic=topic,
                           image_name=image_name,
                           lessons=topic.lessons,
                           name_form=name_form,
                           topic_image_form=topic_image_form,
                           button_delete=button_delete, button_add=button_add, back_btn=back_btn
                           )


@structure_blueprint.route('lesson_<int:lesson_id>/', methods=["GET", "POST"])
def lesson(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.topic', topic_id=lesson.topic_id))

    button_delete = ButtonDeleteForm()
    select_type_form = SelectTaskTypeForm()
    button_add = ButtonAddForm()

    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(lesson)
        db.session.commit()
        return redirect(url_for('structure.topic', topic_id=lesson.topic_id))

    if select_type_form.validate_on_submit() and select_type_form.type.data:
        task_type_id = select_type_form.type.data
        new_task = Task(task_type_id=task_type_id, creator_admin_id=current_user.id, lesson_id=lesson.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('structure.lesson', lesson_id=lesson.id))

    return render_template('lesson.html',
                           lesson=lesson,
                           tasks=lesson.tasks,
                           button_delete=button_delete,
                           select_type_form=select_type_form,
                           button_add=button_add, back_btn=back_btn
                           )


@structure_blueprint.route('render_task<int:task_id>/', methods=["GET", "POST"])
def render_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.task_type_id == 1:
        return redirect(url_for('task_1_bp.render', task_id=task_id))
    if task.task_type_id == 2:
        return redirect(url_for('task_2_bp.render', task_id=task_id))
    if task.task_type_id == 3:
        return redirect(url_for('task_3_bp.render', task_id=task_id))
    if task.task_type_id == 4:
        return redirect(url_for('task_4_bp.render', task_id=task_id))


@structure_blueprint.route('add_to_task_<int:task_id>_word_<int:word_id>/', methods=["GET", "POST"])
def add_to_task_word(task_id, word_id):
    task = Task.query.filter_by(id=task_id).first()
    words = task.elements['words_id']
    words.append(word_id)
    task.elements['words_id'] = words
    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))


@structure_blueprint.route('remove_from_task_<int:task_id>_word_<int:word_id>/', methods=["GET", "POST"])
def remove_from_task_word(task_id, word_id):
    task = Task.query.filter_by(id=task_id).first()
    words = task.elements['words_id']
    words.remove(word_id)
    task.elements['words_id'] = words
    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))
