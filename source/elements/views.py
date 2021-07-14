from flask import Flask, render_template, url_for, redirect, Blueprint, request, flash
from source import db
from source.elements.forms import ButtonAddForm, ButtonDeleteForm, UploadImageForm, UploadAudioForm, WordForm
from source.admin_panel_models import Word, Media
from source.static.media_handler import add_media

elements_blueprint = Blueprint('elements', __name__, template_folder='templates')


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
        image_media = add_media(item=word, file=word_image_form.image.data)
        word.image_id = image_media.id
        db.session.commit()
        return redirect(url_for('elements.word', word_id=word.id))

    word_audio_form = UploadAudioForm()
    if word_audio_form.validate_on_submit() and word_audio_form.audio.data:
        audio_media = add_media(item=word, file=word_audio_form.audio.data)
        word.audio_id = audio_media.id
        db.session.commit()
        return redirect(url_for('elements.word', word_id=word.id))

    return render_template('word.html',
                           word=word,
                           image_name=image_name,
                           audio_name=audio_name,
                           word_image_form=word_image_form,
                           word_audio_form=word_audio_form,
                           button_delete=button_delete,
                           word_form=word_form,
                           )
