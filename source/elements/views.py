from flask import Flask, render_template, url_for, redirect, Blueprint
from source import db
from elements.forms import ButtonAddForm
from source.admin_panel_models import Word

elements_blueprint = Blueprint('elements', __name__, template_folder='templates')


@elements_blueprint.route('/words', methods=['GET', 'POST'])
def words():

    button_add = ButtonAddForm()

    if button_add.validate_on_submit() and button_add.add.data:
        new_word = Word(char='', pinyin='', lang='')
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('elements.words'))

    return render_template('words.html',
                           words=Word.query.all(),
                           button_add=button_add,
                           )


@elements_blueprint.route('/words_<int:word_id>', methods=['GET', 'POST'])
def word(word_id):
    word = Word.query.filter_by(id=word_id).first()


    return render_template('word.html',
                           word=word)