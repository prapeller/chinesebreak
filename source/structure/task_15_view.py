import flask_sijax
from flask import render_template, redirect, url_for, Blueprint, request, g, flash
from source.admin_panel_models import Task, TaskType, Word, Media, Grammar
from source import db
from source.structure.forms import UploadSentAAudioForm, UploadSentBAudioForm, ButtonAddWordForm, ButtonAddGrammarForm, \
    ButtonDeleteForm, \
    BackButtonForm, RightSentAForm, RightSentBForm, WrongSentForm
from source.static.media_handler import add_to_task_image, add_to_task_sent_A_audio, add_to_task_sent_B_audio

task_15_bp = Blueprint('task_15_bp', __name__, url_prefix='/task_15_dialog_A_char_from_char',
                       template_folder='templates')


@flask_sijax.route(task_15_bp, '<int:task_id>/', methods=["GET", "POST"])
def render(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task_type = TaskType.query.filter_by(id=task.task_type_id).first()

    if task.media.get('sent_audio_A_id'):
        sent_A_audio = Media.query.filter_by(id=task.media.get('sent_audio_A_id')[0]).first()
        sent_A_audio_name = sent_A_audio.name
    else:
        sent_A_audio = None
        sent_A_audio_name = 'None'

    sent_A_audio_form = UploadSentAAudioForm()
    if sent_A_audio_form.validate_on_submit() and sent_A_audio_form.sent_A_audio.data:
        audio_media = add_to_task_sent_A_audio(task=task, file=sent_A_audio_form.sent_A_audio.data)
        sent_A_audio_id_lst = [audio_media.id] if audio_media else []
        task.media['sent_audio_A_id'] = sent_A_audio_id_lst
        db.session.commit()
        return redirect(url_for('structure.render_task', task_id=task.id))

    if task.media.get('sent_audio_B_id'):
        sent_B_audio = Media.query.filter_by(id=task.media.get('sent_audio_B_id')[0]).first()
        sent_B_audio_name = sent_B_audio.name
    else:
        sent_B_audio = None
        sent_B_audio_name = 'None'

    sent_B_audio_form = UploadSentBAudioForm()
    if sent_B_audio_form.validate_on_submit() and sent_B_audio_form.sent_B_audio.data:
        audio_media = add_to_task_sent_B_audio(task=task, file=sent_B_audio_form.sent_B_audio.data)
        sent_B_audio_id_lst = [audio_media.id] if audio_media else []
        task.media['sent_audio_B_id'] = sent_B_audio_id_lst
        db.session.commit()
        return redirect(url_for('structure.render_task', task_id=task.id))

    task_words_id_list = task.elements.get('words_id')
    task_words = [Word.query.filter_by(id=id).first() for id in task_words_id_list]

    active_task_words_id_list = task.elements.get('words_id_active_or_to_del')
    active_task_words = [Word.query.filter_by(id=id).first() for id in active_task_words_id_list
                         if Word.query.filter_by(id=id).first()]

    task_grammars_id_list = task.elements.get('grammar_id')
    task_grammars = [Grammar.query.filter_by(id=id).first() for id in task_grammars_id_list]

    right_sent_pinyin = ''.join(f'{word.pinyin} ' for word in task_words if word.pinyin)[:-1]
    right_sent_char = ''.join(word.char for word in task_words if word.char)

    sent_pinyin_B = task.right_sentences.get('sent_pinyin_B')[0] if task.right_sentences.get('sent_pinyin_B') else ''
    sent_char_B = task.right_sentences.get('sent_char_B')[0] if task.right_sentences.get('sent_char_B') else ''

    wrong_sent_pinyin_lst = task.wrong_sentences['sent_pinyin']
    wrong_sent_char_lst = task.wrong_sentences['sent_char']
    wrong_sent_lst = list(zip(wrong_sent_pinyin_lst, wrong_sent_char_lst)) if (
            wrong_sent_pinyin_lst and wrong_sent_char_lst) else []

    back_btn = BackButtonForm()
    if back_btn.validate_on_submit() and back_btn.back.data:
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    add_wrong_sent_form = WrongSentForm()
    if add_wrong_sent_form.validate_on_submit() and add_wrong_sent_form.add_wrong_sent.data:
        wrong_sent_pinyin = add_wrong_sent_form.sent_pinyin.data
        wrong_sent_pinyin_lst = task.wrong_sentences['sent_pinyin']
        wrong_sent_pinyin_lst.append(wrong_sent_pinyin)
        task.wrong_sentences['sent_pinyin'] = wrong_sent_pinyin_lst

        wrong_sent_char = add_wrong_sent_form.sent_char.data
        wrong_sent_char_lst = task.wrong_sentences['sent_char']
        wrong_sent_char_lst.append(wrong_sent_char)
        task.wrong_sentences['sent_char'] = wrong_sent_char_lst

        db.session.commit()
        flash('wrong send was added successfully')
        return redirect(url_for('structure.render_task', task_id=task.id))

    right_sent_A_form = RightSentAForm()
    right_sent_B_form = RightSentBForm()

    if right_sent_A_form.validate_on_submit() and right_sent_A_form.submit_A.data:
        sent_lang_A = right_sent_A_form.sent_lang_A.data
        task.right_sentences['sent_lang_A'] = [sent_lang_A]
        sent_lit_A = right_sent_A_form.sent_lit_A.data
        task.right_sentences['sent_lit_A'] = [sent_lit_A]
        db.session.commit()
        flash('sent_A update success')

    if right_sent_B_form.validate_on_submit() and right_sent_B_form.submit_B.data:
        sent_char_B = right_sent_B_form.sent_char_B.data
        task.right_sentences['sent_char_B'] = [sent_char_B]
        sent_pinyin_B = right_sent_B_form.sent_pinyin_B.data
        task.right_sentences['sent_pinyin_B'] = [sent_pinyin_B]
        sent_lang_B = right_sent_B_form.sent_lang_B.data
        task.right_sentences['sent_lang_B'] = [sent_lang_B]
        sent_lit_B = right_sent_B_form.sent_lit_B.data
        task.right_sentences['sent_lit_B'] = [sent_lit_B]
        db.session.commit()
        flash('sent_B update success')
    #
    # if request.method == "GET":
    right_sent_A_form.sent_lang_A.data = task.right_sentences.get('sent_lang_A')[0] if task.right_sentences.get('sent_lang_A') else ''
    right_sent_A_form.sent_lit_A.data = task.right_sentences.get('sent_lit_A')[0] if task.right_sentences.get('sent_lit_A') else ''

    right_sent_B_form.sent_pinyin_B.data = task.right_sentences.get('sent_pinyin_B')[0] if task.right_sentences.get('sent_pinyin_B') else ''
    right_sent_B_form.sent_char_B.data = task.right_sentences.get('sent_char_B')[0] if task.right_sentences.get('sent_char_B') else ''
    right_sent_B_form.sent_lang_B.data = task.right_sentences.get('sent_lang_B')[0] if task.right_sentences.get('sent_lang_B') else ''
    right_sent_B_form.sent_lit_B.data = task.right_sentences.get('sent_lit_B')[0] if task.right_sentences.get('sent_lit_B') else ''

    button_add_word = ButtonAddWordForm()
    if button_add_word.validate_on_submit() and button_add_word.add_word.data:
        new_word = Word(char='新', pinyin='xīn', lang='новый')
        db.session.add(new_word)
        db.session.commit()
        return redirect(url_for('elements.word', word_id=new_word.id))

    button_add_grammar = ButtonAddGrammarForm()
    if button_add_grammar.validate_on_submit() and button_add_grammar.add_grammar.data:
        new_grammar = Grammar(name='новая грамматика', explanation='новое объяснение грамматики', char='带有示例语法的新句子',
                              pinyin='dài yǒu shìlì yǔfǎ de xīn jùzi', lang='новое предложение с примером грамматики',
                              structure='новая структура')
        db.session.add(new_grammar)
        db.session.commit()
        return redirect(url_for('elements.grammar', grammar_id=new_grammar.id))

    button_delete_task = ButtonDeleteForm()
    if button_delete_task.validate_on_submit() and button_delete_task.delete.data:
        db.session.delete(task)
        if sent_A_audio:
            db.session.delete(sent_A_audio)
        if sent_B_audio:
            db.session.delete(sent_B_audio)
        # db.session.query(Media).filter(Media.id.in_([sent_image.id for sent_image in sent_images])).delete()
        db.session.commit()
        return redirect(url_for('structure.lesson', lesson_id=task.lesson_id))

    def act_deact_word(obj_response, word_id):
        words_id_lst = task.elements['words_id']
        active_words_id_lst = task.elements['words_id_active_or_to_del']
        word_idx = words_id_lst.index(word_id)

        if active_words_id_lst[word_idx] == 0:
            active_words_id_lst[word_idx] = word_id
        else:
            active_words_id_lst[word_idx] = 0

        task.elements['words_id_active_or_to_del'] = active_words_id_lst
        db.session.commit()

    def prepare_to_task_to_grammar(obj_response, word_id):
        words_id_list = task.elements['words_id']
        word_idx = words_id_list.index(word_id)
        grammar_id_list = task.elements['grammar_id']

        if grammar_id_list[word_idx] == 0:
            grammar_id_list[word_idx] = 'to_add_grammar'
        else:
            grammar_id_list[word_idx] = 0

        task.elements['grammar_id'] = grammar_id_list
        db.session.commit()

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('act_deact_word_req', act_deact_word)
        g.sijax.register_callback('prepare_to_task_to_grammar_req', prepare_to_task_to_grammar)
        return g.sijax.process_request()
    search_val = request.args.get('search_key')

    if search_val:
        words = Word.query.filter(Word.char.contains(search_val) | Word.pinyin.contains(search_val) |
                                  Word.lang.contains(search_val))
        grammars = Grammar.query.filter(Grammar.name.contains(search_val) | Grammar.explanation.contains(search_val))
    else:
        words = Word.query.all()
        grammars = Grammar.query.all()

    return render_template('tasks/15_dialog_A_char_from_char.html',
                           task=task, task_type=task_type,

                           right_sent_pinyin=right_sent_pinyin,
                           right_sent_char=right_sent_char,
                           wrong_sent_lst=wrong_sent_lst,

                           add_wrong_sent_form=add_wrong_sent_form,

                           right_sent_A_form=right_sent_A_form,
                           # sent_lang_A=sent_lang_A,
                           # sent_lit_A=sent_lit_A,
                           sent_A_audio_form=sent_A_audio_form,
                           sent_A_audio_name=sent_A_audio_name,

                           right_sent_B_form=right_sent_B_form,
                           sent_pinyin_B=sent_pinyin_B,
                           sent_char_B=sent_char_B,
                           # sent_lang_B=sent_lang_B,
                           # sent_lit_B=sent_lit_B,
                           sent_B_audio_form=sent_B_audio_form,
                           sent_B_audio_name=sent_B_audio_name,

                           back_btn=back_btn,

                           button_delete_task=button_delete_task,

                           button_add_word=button_add_word,
                           button_add_grammar=button_add_grammar,

                           task_words=task_words,
                           active_task_words_id_list=active_task_words_id_list,
                           active_task_words=active_task_words,
                           task_grammars_id_list=task_grammars_id_list,
                           task_grammars=task_grammars,

                           words=words,
                           grammars=grammars,
                           )
