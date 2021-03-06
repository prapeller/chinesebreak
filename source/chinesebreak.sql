pragma foreign_keys = off;
insert into task_types
values (1, 'word_image'),
       (2, 'word_char_from_lang'),
       (3, 'word_lang_from_char'),
       (4, 'word_char_from_video'),
       (5, 'word_match'),
       (6, 'sent_image'),
       (7, 'sent_char_from_lang'),
       (8, 'sent_lang_from_char'),
       (9, 'sent_lang_from_video'),
       (10, 'sent_say_from_char'),
       (11, 'sent_say_from_video'),
       (12, 'sent_paste_from_char'),
       (13, 'sent_choose_from_char'),
       (14, 'sent_delete_from_char'),
       (15, 'dialog_A_char_from_char'),
       (16, 'dialog_B_char_from_video'),
       (17, 'dialog_A_puzzle_char_from_char'),
       (18, 'dialog_B_puzzle_char_from_char'),
       (19, 'puzzle_char_from_lang'),
       (20, 'puzzle_lang_from_char'),
       (21, 'puzzle_char_from_video'),
       (22, 'draw_character');
pragma foreign_keys = on;
