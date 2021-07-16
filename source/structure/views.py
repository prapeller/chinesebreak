import flask_sijax
from source import app
from flask import render_template, redirect, url_for, Blueprint, session, flash, request, g
from source.admin_panel_models import Lang, Course, Topic, Lesson, Task, TaskType, Media, Word
from flask_login import login_required, current_user
from source import db
from source.structure.forms import ButtonAddForm, ButtonDeleteForm, NameForm, UploadImageForm
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
                           button_delete=button_delete,
                           button_add=button_add, )


@structure_blueprint.route('course_<int:course_id>/', methods=["GET", "POST"])
def course(course_id):
    course = Course.query.filter_by(id=course_id).first()

    name_form = NameForm()
    button_delete = ButtonDeleteForm()
    button_add = ButtonAddForm()

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
                           button_delete=button_delete,
                           button_add=button_add, )


@structure_blueprint.route('topic_<int:topic_id>/', methods=["GET", "POST"])
def topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    image = Media.query.filter_by(id=topic.image_id).first()
    image_name = image.name if image else 'none'

    name_form = NameForm()
    button_add = ButtonAddForm()
    topic_image_form = UploadImageForm()
    button_delete = ButtonDeleteForm()

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
                           button_delete=button_delete,
                           button_add=button_add, )


@structure_blueprint.route('lesson_<int:lesson_id>/', methods=["GET", "POST"])
def lesson(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()

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
                           button_add=button_add,
                           )


@structure_blueprint.route('render_task<int:task_id>/', methods=["GET", "POST"])
def task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.task_type_id == 1:
        return redirect(url_for('structure.task_1_word_image', task_id=task_id))


@structure_blueprint.route('add_to_task_<int:task_id>_word_<int:word_id>/', methods=["GET", "POST"])
def add_to_task_word(task_id, word_id):
    task = Task.query.filter_by(id=task_id).first()
    words = task.elements['words_id']
    words.append(word_id)
    task.elements['words_id'] = words
    db.session.commit()
    return redirect(url_for('structure.task', task_id=task_id))


# @structure_blueprint.route('add_to_task_<int:task_id>_active_element_<string:element_type>_id_<int:element_id>/',
#                            methods=["GET", "POST"])
# def add_to_task_act_elem(task_id, element_type, element_id):
#     if element_type == 'word':
#         task = Task.query.filter_by(id=task_id).first()
#         active_words = task.elements['words_id_active_or_to_del']
#         active_words.append(element_id)
#         task.elements['words_id_active_or_to_del'] = active_words
#         db.session.commit()
#
#     return redirect(url_for('structure.task', task_id=task_id))
#
#
# @structure_blueprint.route('remove_from_task_<int:task_id>_active_element_<string:element_type>_id_<int:element_id>/',
#                            methods=["GET", "POST"])
# def remove_act_elem(task_id, element_type, element_id):
#     if element_type == 'word':
#         task = Task.query.filter_by(id=task_id).first()
#         active_words = task.elements['words_id_active_or_to_del']
#         active_words.remove(element_id)
#         task.elements['words_id_active_or_to_del'] = active_words
#         db.session.commit()
#
#     return redirect(url_for('structure.task', task_id=task_id))


# @structure_blueprint.route('task_1_word_image_<int:task_id>/', methods=["GET", "POST"])
@flask_sijax.route(structure_blueprint, 'task_1_word_image_<int:task_id>/', methods=["GET", "POST"])
def task_1_word_image(task_id):
    # def hello_handler(obj_response, hello_from, hello_to):
    #     obj_response.alert('Hello from %s to %s' % (hello_from, hello_to))
    #     obj_response.css('a', 'color', 'green')
    #
    # def goodbye_handler(obj_response):
    #     obj_response.alert('Goodbye, whoever you are.')
    #     obj_response.css('a', 'color', 'red')
    #
    # def activate_word(obj_response, word_id):
    def activate_word(word_id):
        # obj_response.alert(f'activate {word_id}')
        task = Task.query.filter_by(id=task_id).first()
        active_words = task.elements['words_id_active_or_to_del']
        active_words.append(word_id)
        task.elements['words_id_active_or_to_del'] = active_words
        db.session.commit()

        return redirect(url_for('structure.task', task_id=task_id))

    # def deactivate_word(obj_response, word_id):
    def deactivate_word(word_id):
        # obj_response.alert(f'deactivate {word_id}')
        task = Task.query.filter_by(id=task_id).first()
        active_words = task.elements['words_id_active_or_to_del']
        active_words.remove(word_id)
        task.elements['words_id_active_or_to_del'] = active_words
        db.session.commit()

        return redirect(url_for('structure.task', task_id=task_id))
    #
    # if g.sijax.is_sijax_request:
    #     g.sijax.register_callback('say_hello', activate_word)
    #     g.sijax.register_callback('say_goodbye', deactivate_word)
    #     return g.sijax.process_request()

    class RenderWord(Word):
        def __init__(self, word):
            self.id, self.pinyin, self.char, self.lang, self.lit = word.id, word.pinyin, word.char, word.lang, word.lit
            if Media.query.filter_by(id=word.image_id).first():
                self.image_name = Media.query.filter_by(id=word.image_id).first().name
            if Media.query.filter_by(id=word.audio_id).first():
                self.audio_name = Media.query.filter_by(id=word.audio_id).first().name
            self.is_active = True if self.id in Task.query.filter_by(id=task_id).first().elements.get(
                'words_id_active_or_to_del') else False

    task = Task.query.filter_by(id=task_id).first()
    task_words_id_set = task.elements.get('words_id')
    task_words = [RenderWord(word) for word in Word.query.filter(Word.id.in_(task_words_id_set)).all()]

    search_val = request.args.get('search_key')
    if search_val:
        words = Word.query.filter(
            Word.char.contains(search_val) | Word.pinyin.contains(search_val) | Word.lang.contains(search_val))
    else:
        words = Word.query.all()

    button_add = ButtonAddForm()
    if button_add.validate_on_submit() and button_add.add.data:
        new_word = Word(char='新', pinyin='xīn', lang='новый')
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('elements.word', word_id=new_word.id))

    button_delete = ButtonDeleteForm()
    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    if request.method == 'POST':
        show = request.args
        if request.args:
            word_id = int(request.form.get('act-word-checkbox'))
            active_words_id = Task.query.filter_by(id=task_id).first().elements.get('words_id_active_or_to_del')
            if word_id not in active_words_id:
                print(f'checked {word_id}')
                activate_word(word_id)
            else:
                print(f'unchecked {word_id}')
                deactivate_word(word_id)


    return render_template('tasks/1_word_image.html',
                           task=task,
                           button_delete=button_delete,
                           task_words=task_words,
                           words=words,
                           button_add=button_add,
                           )

# @structure_blueprint.route('/get_toggled_status')
# def toggled_status():
#   current_status = request.args.get('status')
#   return 'Toggled' if current_status == 'Untoggled' else 'Untoggled'