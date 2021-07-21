import flask_sijax
from flask import render_template, redirect, url_for, Blueprint, session, flash, request, g
from source.admin_panel_models import Lang, Course, Topic, Lesson, Task, TaskType, Media, Word
from source import db

from source.structure.forms import ButtonAddForm, ButtonDeleteForm, NameForm, UploadImageForm, BackButtonForm

task_2_bp = Blueprint('task_2_bp', __name__, url_prefix='/task_2_word_char_from_lang', template_folder='templates')


@flask_sijax.route(task_2_bp, '<int:task_id>/', methods=["GET", "POST"])
def render(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task_type = TaskType.query.filter_by(id=task.task_type_id).first()

    task_words_id_list = task.elements.get('words_id')
    task_words = [Word.query.filter_by(id=id).first() for id in task_words_id_list]

    active_task_words_id_list = task.elements.get('words_id_active_or_to_del')
    active_task_words = [Word.query.filter_by(id=id).first() for id in active_task_words_id_list]

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    button_add_word = ButtonAddForm()
    if button_add_word.validate_on_submit() and button_add_word.add.data:
        new_word = Word(char='新', pinyin='xīn', lang='новый')
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('elements.word', word_id=new_word.id))

    button_delete_task = ButtonDeleteForm()
    if button_delete_task.validate_on_submit() and button_delete_task.delete.data:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    def act_deact_word(obj_response, word_id):
        task = Task.query.filter_by(id=task_id).first()
        active_words = task.elements['words_id_active_or_to_del']
        if word_id in active_words:
            active_words.remove(word_id)
            task.elements['words_id_active_or_to_del'] = active_words
        else:
            active_words.append(word_id)
            task.elements['words_id_active_or_to_del'] = active_words
        db.session.commit()

    search_val = request.args.get('search_key')
    if search_val:
        words = Word.query.filter(
            Word.char.contains(search_val) | Word.pinyin.contains(search_val) | Word.lang.contains(search_val))
    else:
        words = Word.query.all()

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('act_deact_word_req', act_deact_word)
        return g.sijax.process_request()

    return render_template('tasks/2_word_char_from_lang.html',
                           task=task, task_type=task_type,
                           back_btn=back_btn, button_delete_task=button_delete_task, button_add_word=button_add_word,
                           task_words=task_words,
                           words=words,
                           )
