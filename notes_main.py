from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QListWidget, QTextEdit, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QMessageBox, QGroupBox, QButtonGroup
import json as jef
#==========================================================================================================================
app = QApplication([])
main_win = QWidget()
main_win.show()
#==========================================================================================================================
notes = {

}



# with open('jef.json', 'w') as file:
#     jef.dump(notes, file)

with open('jef.json', 'r') as file:
    notes = jef.load(file)



main_layout = QHBoxLayout()

first_two_buttons = QHBoxLayout()
first_one_button = QHBoxLayout()

second_two_buttons = QHBoxLayout()
second_one_button = QHBoxLayout()

right_main = QVBoxLayout()
left_main = QVBoxLayout()

main_layout.addLayout(left_main)
main_layout.addLayout(right_main)

main_win.setLayout(main_layout)

text_field = QTextEdit()
text_field.setText('')

left_main.addWidget(text_field)

notes_list = QListWidget()
tags_list = QListWidget()
taitl = QLabel('Список заметок')
taitl1 = QLabel('Список тегов')

first_two_buttons_button1 = QPushButton('Создать заметку')
first_two_buttons_button2 = QPushButton('Удалить заметку')

first_two_buttons.addWidget(first_two_buttons_button1)
first_two_buttons.addWidget(first_two_buttons_button2)

first_one_button_button = QPushButton('Сохранить заметку')

first_one_button.addWidget(first_one_button_button)

second_two_buttons_button1 = QPushButton('Добавить к заметке')
second_two_buttons_button2 = QPushButton('Открепить от заметки')

second_two_buttons.addWidget(second_two_buttons_button1)
second_two_buttons.addWidget(second_two_buttons_button2)

second_one_button_button = QPushButton('Искать заметки по тегу')

second_one_button.addWidget(second_one_button_button)

line_field = QLineEdit()
line_field.setPlaceholderText('Введите тег...')

notes_list.addItems(notes)



def show_note():
    name = notes_list.selectedItems()[0].text()
    text_field.setText(notes[name]['текст'])
    tags_list.clear()
    tags_list.addItems(notes[name]['теги'])

def add_note():
    note_name, result = QInputDialog.getText(main_win, 'Добавить заметку', 'Название заметки')
    if note_name != '':
        notes[note_name] = {
        'текст' : '',
        'теги' : []
    }
    notes_list.clear()
    notes_list.addItems(notes)
    with open('jef.json', 'w') as file:
        jef.dump(notes, file)

def del_note():
    if notes_list.selectedItems():
        del notes[notes_list.selectedItems()[0].text()]
    notes_list.clear()
    notes_list.addItems(notes)
    with open('jef.json', 'w') as file:
        jef.dump(notes, file)

def save_note():
    if notes_list.selectedItems():
        notes[notes_list.selectedItems()[0].text()]['текст'] = text_field.toPlainText()
    with open('jef.json', 'w') as file:
        jef.dump(notes, file)

forbiden_symbols = '#\|/@!*^%$№;:??()[]{"}'

def add_tag():
    if notes_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        for symbols in line_field.text():
            if not(symbols in forbiden_symbols):
                if not(line_field.text() in notes[notes_list.selectedItems()[0].text()]['теги']):
                    if not(' ' in line_field.text()):
                        if len(line_field.text()) <= 20:
                            notes[notes_list.selectedItems()[0].text()]['теги'].append(line_field.text())
                            tags_list.clear()
                            tags_list.addItems(notes[note_name]['теги'])
                        else:
                            print('Слишком длинное название')
                    else:
                        print('Название заметки не должно содержать пробел')
                else:
                    print('У данной заметки уже есть такой тег, а именно:', line_field.text())
            else:
                print('В названии присутствуют заперщенные символы из списка, а именно:', symbol)
    with open('jef.json', 'w') as file:
        jef.dump(notes, file)

def del_tag():
    if notes_list.selectedItems() and tags_list.selectedItems():
        note_name = notes_list.selectedItems()[0].text()
        notes[note_name]['теги'].remove(tags_list.selectedItems()[0].text())
        tags_list.clear()
        tags_list.addItems(notes[note_name]['теги'])
    with open('jef.json', 'w') as file:
        jef.dump(notes, file)

def find_tag():
    tagged_notes = list()
    tag_name = line_field.text()
    if second_one_button_button.text() == 'Искать заметки по тегу':
        if tag_name != '':
            for note_name in notes:
                if tag_name in notes[note_name]['теги']:
                    tagged_notes.append(note_name)
            notes_list.clear()
            notes_list.addItems(tagged_notes)
            second_one_button_button.setText('Сбросить поиск по тегу')
            line_field.setText('')
    elif second_one_button_button.text() == 'Сбросить поиск по тегу':
        notes_list.clear()
        notes_list.addItems(notes)
        second_one_button_button.setText('Искать заметки по тегу')



first_two_buttons_button1.clicked.connect(add_note)
first_two_buttons_button2.clicked.connect(del_note)
first_one_button_button.clicked.connect(save_note)
second_two_buttons_button1.clicked.connect(add_tag)
second_two_buttons_button2.clicked.connect(del_tag)
second_one_button_button.clicked.connect(find_tag)



right_main.addWidget(taitl)
right_main.addWidget(notes_list)
right_main.addLayout(first_two_buttons)
right_main.addLayout(first_one_button)
right_main.addWidget(taitl1)
right_main.addWidget(tags_list)
right_main.addWidget(line_field)
right_main.addLayout(second_two_buttons)
right_main.addLayout(second_one_button)

notes_list.itemClicked.connect(show_note)
#==========================================================================================================================
app.exec_()