from flask import render_template, url_for, redirect, Blueprint, request, flash
from source import db
from source import app
from source.elements.forms import ButtonAddForm, ButtonDeleteForm, UploadImageForm, UploadAudioForm, WordForm, \
    BackButtonForm, GrammarForm, AddVideoTaskBtnForm
from source.admin_panel_models import Word, Media, Grammar, Task
from source.static.media_handler import add_to_word_image, add_to_word_audio
from flask_login import current_user
from sqlalchemy import select
import sqlite3
import os

elements_blueprint = Blueprint('elements', __name__, url_prefix='/elements', template_folder='templates')


@elements_blueprint.route('/words', methods=['GET', 'POST'])
def words():
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

    return render_template('words.html',
                           words=words,
                           button_add=button_add,
                           )


@elements_blueprint.route('/words_<int:word_id>', methods=['GET', 'POST'])
def word(word_id):
    word = Word.query.filter_by(id=word_id).first()
    image = Media.query.filter_by(id=word.image_id).first()
    image_name = image.name if image else 'none'
    audio = Media.query.filter_by(id=word.audio_id).first()
    audio_name = audio.name if audio else 'none'

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('elements.words'))

    button_delete = ButtonDeleteForm()
    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(word)
        db.session.commit()
        flash('delete success')
        return redirect(url_for('elements.words'))

    word_form = WordForm()
    if word_form.validate_on_submit() and word_form.update.data:
        word.pinyin = word_form.pinyin.data
        word.char = word_form.char.data
        word.lang = word_form.lang.data
        word.lit = word_form.lit.data
        db.session.commit()
        flash('update success')

    elif request.method == "GET":
        word_form.pinyin.data = word.pinyin
        word_form.char.data = word.char
        word_form.lang.data = word.lang
        word_form.lit.data = word.lit

    word_image_form = UploadImageForm()
    if word_image_form.validate_on_submit() and word_image_form.image.data:
        image_media = add_to_word_image(word=word, file=word_image_form.image.data)
        word.image_id = image_media.id
        db.session.commit()
        return redirect(url_for('elements.word', word_id=word.id))

    word_audio_form = UploadAudioForm()
    if word_audio_form.validate_on_submit() and word_audio_form.audio.data:
        audio_media = add_to_word_audio(word=word, file=word_audio_form.audio.data)
        word.audio_id = audio_media.id
        db.session.commit()
        return redirect(url_for('elements.word', word_id=word.id))

    add_video_task_btn_form = AddVideoTaskBtnForm()
    if add_video_task_btn_form.validate_on_submit() and add_video_task_btn_form.add_video_task.data:
        task = Task.query.filter_by(word_id=word_id).first()
        if task:
            return redirect(url_for('structure.render_task', task_id=task.id))
        else:
            new_task = Task(task_type_id=23, creator_admin_id=current_user.id, lesson_id=None)
            new_task.word_id = word_id
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('structure.render_task', task_id=new_task.id))

    return render_template('word.html',
                           back_btn=back_btn,
                           word=word,
                           image_name=image_name,
                           audio_name=audio_name,
                           word_image_form=word_image_form,
                           word_audio_form=word_audio_form,
                           add_video_task_btn_form=add_video_task_btn_form,
                           button_delete=button_delete,
                           word_form=word_form,
                           )


@elements_blueprint.route('/grammars', methods=['GET', 'POST'])
def grammars():
    search_val = request.args.get('search_key')
    if search_val:
        grammars = Grammar.query.filter(
            Grammar.name.contains(search_val) |
            Grammar.explanation.contains(search_val) |
            Grammar.char.contains(search_val) |
            Grammar.pinyin.contains(search_val) |
            Grammar.lang.contains(search_val) |
            Grammar.lit.contains(search_val) |
            Grammar.structure.contains(search_val)
        )
    else:
        grammars = Grammar.query.all()

    button_add = ButtonAddForm()
    if button_add.validate_on_submit() and button_add.add.data:
        new_grammar = Grammar(
            name='новая грамматика',
            explanation='новое объяснение грамматики',
            char='带有示例语法的新句子',
            pinyin='dài yǒu shìlì yǔfǎ de xīn jùzi',
            lang='новое предложение с примером грамматики',
            structure='новая структура'
        )
        db.session.add(new_grammar)
        db.session.commit()
        return redirect(url_for('elements.grammar', grammar_id=new_grammar.id))

    return render_template('grammars.html',
                           grammars=grammars,
                           button_add=button_add,
                           )


@elements_blueprint.route('/grammar_<int:grammar_id>', methods=['GET', 'POST'])
def grammar(grammar_id):
    grammar = Grammar.query.filter_by(id=grammar_id).first()

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('elements.grammars'))

    add_video_task_btn_form = AddVideoTaskBtnForm()
    if add_video_task_btn_form.validate_on_submit() and add_video_task_btn_form.add_video_task.data:
        task = Task.query.filter_by(grammar_id=grammar_id).first()
        if task:
            return redirect(url_for('structure.render_task', task_id=task.id))
        else:
            new_task = Task(task_type_id=24, creator_admin_id=current_user.id, lesson_id=None)
            new_task.grammar_id = grammar_id
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('structure.render_task', task_id=new_task.id))

    button_delete = ButtonDeleteForm()
    if button_delete.validate_on_submit() and button_delete.delete.data:
        db.session.delete(grammar)
        db.session.commit()
        flash('delete success')
        return redirect(url_for('elements.grammars'))

    grammar_form = GrammarForm()
    if grammar_form.validate_on_submit() and grammar_form.update.data:
        grammar.name = grammar_form.name.data
        grammar.explanation = grammar_form.explanation.data
        grammar.char = grammar_form.char.data
        grammar.pinyin = grammar_form.pinyin.data
        grammar.lang = grammar_form.lang.data
        grammar.lit = grammar_form.lit.data
        grammar.structure = grammar_form.structure.data
        db.session.commit()
        flash('update success')

    elif request.method == "GET":
        grammar_form.name.data = grammar.name
        grammar_form.explanation.data = grammar.explanation
        grammar_form.char.data = grammar.char
        grammar_form.pinyin.data = grammar.pinyin
        grammar_form.lang.data = grammar.lang
        grammar_form.lit.data = grammar.lit
        grammar_form.structure.data = grammar.structure

    return render_template('grammar.html',
                           grammar=grammar,
                           grammar_form=grammar_form,
                           add_video_task_btn_form=add_video_task_btn_form,
                           button_delete=button_delete, back_btn=back_btn,
                           )
