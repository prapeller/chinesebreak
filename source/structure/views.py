from flask import render_template, redirect, url_for, Blueprint, session, flash, request
from source.admin_panel_models import Lang, Course, Topic, Lesson, Task, TaskType
from flask_login import login_required, current_user
from source import db
from source.structure.forms import ButtonAddForm, ButtonDeleteForm, NameForm, SelectTaskTypeForm

structure_blueprint = Blueprint('structure', __name__, template_folder='templates')


@structure_blueprint.route('/structure', methods=["GET", "POST"])
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


@structure_blueprint.route('/lang_id_<int:lang_id>', methods=["GET", "POST"])
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
                           button_add=button_add,)


@structure_blueprint.route('/course_id_<int:course_id>', methods=["GET", "POST"])
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
                           course=course,
                           topics=course.topics,
                           name_form=name_form,
                           button_delete=button_delete,
                           button_add=button_add,)


@structure_blueprint.route('/topic_id_<int:topic_id>', methods=["GET", "POST"])
def topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()

    name_form = NameForm()
    button_delete = ButtonDeleteForm()
    button_add = ButtonAddForm()

    if name_form.validate_on_submit() and name_form.name.data:
        topic.name = name_form.name.data
        db.session.commit()
        flash('update success')
    elif request.method == "GET":
        name_form.name.data = topic.name

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
                           lessons=topic.lessons,
                           name_form=name_form,
                           button_delete=button_delete,
                           button_add=button_add,)


@structure_blueprint.route('/lesson_id_<int:lesson_id>', methods=["GET", "POST"])
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
        return redirect(url_for('structure.lesson',lesson_id=lesson.id))

    return render_template('lesson.html',
                           lesson=lesson,
                           tasks=lesson.tasks,
                           button_delete=button_delete,
                           select_type_form=select_type_form,
                           button_add=button_add,
                           )


@structure_blueprint.route('/task_id_<int:task_id>', methods=["GET", "POST"])
def task(task_id):
    task=Task.query.filter_by(id=task_id).first()
    task_type = TaskType.query.filter_by(id=task.task_type_id).first()
    task_type_id = task_type.id
    task_type_name = task_type.name

    button_delete = ButtonDeleteForm()

    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    if task_type_id == 1:
        return render_template('tasks/1_word_image.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )
    elif task_type_id == 2:
        return render_template('tasks/2_word_char_from_lang.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )
    elif task_type_id == 3:
        return render_template('tasks/3_word_lang_from_char.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )
    elif task_type_id == 4:
        return render_template('tasks/4_word_char_from_video.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )
    elif task_type_id == 5:
        return render_template('tasks/5_word_match.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )
    
    elif task_type_id == 6:
        return render_template('tasks/6_sent_image.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )

    elif task_type_id == 7:
        return render_template('tasks/7_sent_char_from_lang.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )
    elif task_type_id == 8:
        return render_template('tasks/8_sent_lang_from_char.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )

    elif task_type_id == 9:
        return render_template('tasks/9_sent_lang_from_video.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )

    elif task_type_id == 10:
        return render_template('tasks/10_sent_say_from_char.html',
                               task=task,
                               task_type_name=task_type_name,
                               button_delete=button_delete,
                               )

