from .. import app
from flask import render_template, redirect, url_for, Blueprint, flash, request
from source.admin_panel_models import Lang, Course, Topic, Lesson, Task, Media
from flask_login import current_user
from source import db
from source.structure.forms import ButtonAddForm, ButtonDeleteForm, NameForm, UploadImageForm, BackButtonForm
from source.static.media_handler import add_to_topic_image
from source.structure.forms import SelectTaskTypeForm

structure_blueprint = Blueprint('structure', __name__, url_prefix='/structure', template_folder='templates')


@app.route('/')
def start():
    return redirect(url_for('admin_panel.main'))

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

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.course', course_id=topic.course_id))

    name_form = NameForm()
    if name_form.validate_on_submit() and name_form.name.data:
        topic.name = name_form.name.data
        db.session.commit()
        flash('update success')
    elif request.method == "GET":
        name_form.name.data = topic.name

    topic_image_form = UploadImageForm()
    if topic_image_form.validate_on_submit() and topic_image_form.image.data:
        image_media = add_to_topic_image(topic=topic, file=topic_image_form.image.data)
        topic.image_id = image_media.id
        db.session.commit()
        return redirect(url_for('structure.topic', topic_id=topic.id))

    button_delete = ButtonDeleteForm()
    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(topic)
        db.session.commit()
        return redirect(url_for('structure.course', course_id=topic.course_id))

    button_add = ButtonAddForm()
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
    return redirect(url_for(f'task_{task.task_type_id}_bp.render', task_id=task.id))


@structure_blueprint.route('add_to_task_<int:task_id>_word_<int:word_id>/', methods=["GET", "POST"])
def add_to_task_word(task_id, word_id):
    task = Task.query.filter_by(id=task_id).first()
    words_id_list = task.elements['words_id']
    words_id_list.append(word_id)
    active_words_id_list = task.elements['words_id_active_or_to_del']
    active_words_id_list.append(0)
    to_display_words_id_lst = task.elements['words_id_to_display']
    to_display_words_id_lst.append(0)
    grammar_id_list = task.elements['grammar_id']
    grammar_id_list.append(0)
    task.elements['words_id'] = words_id_list
    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))

@structure_blueprint.route('add_to_task_<int:task_id>_wrong_word_<int:word_id>/', methods=["GET", "POST"])
def add_to_task_wrong_word(task_id, word_id):
    task = Task.query.filter_by(id=task_id).first()
    wrong_words_id_list = task.elements['words_id_wrong']
    wrong_words_id_list.append(word_id)

    task.elements['words_id_wrong'] = wrong_words_id_list
    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))


@structure_blueprint.route('remove_from_task_<int:task_id>_wrong_word_<int:word_id>/', methods=["GET", "POST"])
def remove_from_task_wrong_word(task_id, word_id):
    task = Task.query.filter_by(id=task_id).first()
    wrong_words_id_list = task.elements['words_id_wrong']
    wrong_words_id_list.remove(word_id)
    task.elements['words_id_wrong'] = wrong_words_id_list

    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))


@structure_blueprint.route('remove_from_task_<int:task_id>_word_<int:word_id>/', methods=["GET", "POST"])
def remove_from_task_word(task_id, word_id):
    task = Task.query.filter_by(id=task_id).first()
    words_id_list = task.elements['words_id']
    word_idx = words_id_list.index(word_id)
    words_id_list.pop(word_idx)
    active_words_id_list = task.elements['words_id_active_or_to_del']
    active_words_id_list.pop(word_idx)
    to_display_words_id_lst = task.elements['words_id_to_display']
    to_display_words_id_lst.pop(word_idx)
    grammar_id_list = task.elements['grammar_id']
    grammar_id_list.pop(word_idx)
    task.elements['words_id'] = words_id_list
    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))

@structure_blueprint.route('remove_from_task_<int:task_id>_wrong_sent_idx_<int:sent_idx>/', methods=["GET", "POST"])
def remove_from_task_wrong_sent(task_id, sent_idx):
    task = Task.query.filter_by(id=task_id).first()

    wrong_sent_pinyin_lst = task.wrong_sentences['sent_pinyin']
    if wrong_sent_pinyin_lst:
        wrong_sent_pinyin_lst.pop(sent_idx)
        task.wrong_sentences['sent_pinyin'] = wrong_sent_pinyin_lst

    wrong_sent_char_lst = task.wrong_sentences['sent_char']
    if wrong_sent_char_lst:
        wrong_sent_char_lst.pop(sent_idx)
        task.wrong_sentences['sent_char'] = wrong_sent_char_lst

    wrong_sent_lang_lst = task.wrong_sentences['sent_lang']
    if wrong_sent_lang_lst:
        wrong_sent_lang_lst.pop(sent_idx)
        task.wrong_sentences['sent_lang'] = wrong_sent_lang_lst

    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))

@structure_blueprint.route('add_to_task_<int:task_id>_grammar_<int:grammar_id>/', methods=["GET", "POST"])
def add_to_task_grammar(task_id, grammar_id):
    task = Task.query.filter_by(id=task_id).first()
    grammar_id_list = task.elements['grammar_id']
    grammar_id_list[grammar_id_list.index('to_add_grammar')] = grammar_id
    task.elements['grammar_id'] = grammar_id_list
    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))


@structure_blueprint.route('remove_from_task_<int:task_id>_image_<int:sent_image_id>/', methods=["GET", "POST"])
def remove_from_task_image(task_id, sent_image_id):
    task = Task.query.filter_by(id=task_id).first()
    images_ids = [Media.query.filter_by(id=this_id).first().id for this_id in task.media['sent_images_id']]
    media = Media.query.filter_by(id=sent_image_id).first()
    images_ids.remove(media.id)
    task.media['sent_images_id'] = images_ids
    db.session.delete(media)
    db.session.commit()
    return redirect(url_for('structure.render_task', task_id=task_id))
