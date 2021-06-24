# coding: utf-8
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, JSON, String, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, BIT, INTEGER, MEDIUMBLOB, TINYINT
from sqlalchemy.orm import relationship
# from source.admin_panel_models import Base


class MnemonicStage(Base):
    __tablename__ = 'mnemonic_stage'

    id = Column(BIGINT, primary_key=True, unique=True)
    hours_before_repeat = Column(INTEGER, nullable=False)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'comment': 'пользователь (ученик) - использует web/mobile app'}

    id = Column(BIGINT, primary_key=True, unique=True)
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(BIGINT, unique=True)
    age = Column(BIGINT)
    registered_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime)
    status = Column(Enum('trial', 'premium_1', 'premium_6', 'premium_12'), nullable=False, index=True,
                    server_default=text("'trial'"),
                    comment='по умолчанию у пользователя статус подписки trial, если по подписке - '
                            'то может быть на месяц, пол года или на год')
    purchased_at = Column(DateTime)


class Message(Base):
    __tablename__ = 'messages'
    __table_args__ = {'comment': 'обратная связь с пользователями или тех поддержка, отправитель и получатель могут '
                                 'быть как user_id, так и admin_id, в зависимости от типа. пользователи друг другу не '
                                 'отправляют, '}

    id = Column(BIGINT, primary_key=True, unique=True)
    type = Column(Enum('user_admin', 'admin_user'), comment='направление а)пользователь-админ, б) админ-пользователь.')
    from_id = Column(ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'),
                     ForeignKey('admin.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    to_id = Column(ForeignKey('admin.id', ondelete='SET NULL', onupdate='CASCADE'),
                   ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    theme = Column(String(512), nullable=False)
    body = Column(Text)
    file = Column(MEDIUMBLOB)
    is_checked = Column(BIT(1))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    _from = relationship('Admin', primaryjoin='Message.from_id == Admin.id')
    _from1 = relationship('User', primaryjoin='Message.from_id == User.id')
    to = relationship('User', primaryjoin='Message.to_id == User.id')
    to1 = relationship('Admin', primaryjoin='Message.to_id == Admin.id')


class UsersDailyGoal(Base):
    __tablename__ = 'users_daily_goals'
    __table_args__ = {'comment': 'пользователь выставляет ежедневную цель по баллам, набирает их в зависимости от '
                                 'количества срабатываний счетчика count_right в элементах'}

    id = Column(BIGINT, primary_key=True, unique=True)
    user_id = Column(ForeignKey('user.id', onupdate='CASCADE'), nullable=False, index=True)
    daily_goal = Column(TINYINT, nullable=False, server_default=text("'50'"))
    goal_is_reached = Column(BIT(1))
    goal_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    strike_qty = Column(BIGINT, nullable=False,
                        comment='страйк - количетсво достигший цель дней подряд - 1. например, если пользователь 2 дня подряд достигает свою ежедневную цель по баллам - у него 1 страйк, если 3 дня подряд - 2 страйка')

    user = relationship('User')


class UsersSetting(Base):
    __tablename__ = 'users_settings'

    id = Column(BIGINT, primary_key=True, unique=True)
    user_id = Column(ForeignKey('user.id', onupdate='CASCADE'), nullable=False, index=True)
    current_lang_id = Column(BIGINT, server_default=text("'1'"))
    text_size = Column(Enum('15', '18', '22'), server_default=text("'18'"))
    chinese_display_type = Column(Enum('only_characters', 'only_pinyin', 'characters_and_pinyin'),
                                  server_default=text("'characters_and_pinyin'"))
    audio_speed = Column(Enum('0.6', '1.0', '1.5'), server_default=text("'1.0'"))
    audio_effects_are_on = Column(BIT(1))
    audition_lessons_are_on = Column(BIT(1))
    characters_lessons_are_on = Column(BIT(1))
    speaking_lessons_are_on = Column(BIT(1))
    reminders_are_on = Column(BIT(1))

    user = relationship('User')


class UserProgressWord(Base):
    __tablename__ = 'user_progress_words'
    __table_args__ = {
        'comment': 'сначала у всех элементов счетчик правильных ответов (count_right=0) и все элементы находятся на первой\\r\\nступени "мнемонической лесенки", после того как элемент проходится впервые в задании - count_right = 1,\\r\\nи expire_at = now() + mnemonic_stages.hourse_before_repeat первой ступени, после того как настает expire_at -\\r\\nэлемент попадает в "пул повторения". после прохождениея упражнения "на повторение" элемента из пула повторения - у\\r\\nэлемента увеличивается count_right + 1 и checked_times + 1, а expire_at становится равным\\r\\nnow() + mnemonic_stages.hourse_before_repeat второй ступени '}

    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    word_id = Column(ForeignKey('word.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False,
                     index=True)
    checked_at = Column(DateTime)
    mnemonic_stage_id = Column(ForeignKey('mnemonic_stage.id', onupdate='CASCADE'), nullable=False, index=True,
                               server_default=text("'1'"))
    expire_at = Column(DateTime)
    count_right = Column(INTEGER, server_default=text("'0'"), comment='счетчик правльных ответов')
    count_wrong = Column(INTEGER, server_default=text("'0'"), comment='счетчик неправильных ответов')

    mnemonic_stage = relationship('MnemonicStage')
    user = relationship('User')
    word = relationship('Word')


class UserProgressGrammar(Base):
    __tablename__ = 'user_progress_grammars'

    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    grammar_id = Column(ForeignKey('grammar.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                        nullable=False, index=True)
    checked_at = Column(DateTime)
    mnemonic_stage_id = Column(ForeignKey('mnemonic_stage.id', onupdate='CASCADE'), nullable=False, index=True,
                               server_default=text("'1'"))
    expire_at = Column(DateTime)
    count_right = Column(INTEGER, server_default=text("'0'"))
    count_wrong = Column(INTEGER, server_default=text("'0'"))

    grammar = relationship('Grammar')
    mnemonic_stage = relationship('MnemonicStage')
    user = relationship('User')


class UserProgressCharacter(Base):
    __tablename__ = 'user_progress_characters'

    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    character_id = Column(ForeignKey('character.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                          nullable=False, index=True)
    checked_at = Column(DateTime)
    mnemonic_stage_id = Column(ForeignKey('mnemonic_stage.id', onupdate='CASCADE'), index=True,
                               server_default=text("'1'"))
    expire_at = Column(DateTime)
    count_right = Column(INTEGER, server_default=text("'0'"))
    count_wrong = Column(INTEGER, server_default=text("'0'"))

    character = relationship('Character')
    mnemonic_stage = relationship('MnemonicStage')
    user = relationship('User')


class UserProgressTask(Base):
    __tablename__ = 'user_progress_tasks'

    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    task_id = Column(ForeignKey('task.id', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    is_checked = Column(BIT(1))
    checked_at = Column(DateTime)

    task = relationship('Task')
    user = relationship('User')
