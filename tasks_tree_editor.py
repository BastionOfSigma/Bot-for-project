import PySimpleGUI as sg
from tasks_tree import Tasks_Tree

def edit_task(index):
    layout = [
        [sg.Button('Изменит текст задачи', k='tt')],
        [sg.Button('Изменить картинку задачи', k='ti')],
        [sg.Button('Изменить текст решения', k='st')],
        [sg.Button('Изменить картинку решения', k='si')]
    ]
    win = sg.Window('', layout)

    while True:
        event, values = win.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == 'tt':
            tree.change_task_text(index, get_text_big('Введите текст задания', tree.get_task(index)['text']))
            break

        elif event == 'ti':
            tree.change_task_image(index, sg.popup_get_file('Выберете файл картинки задания (.png)'))
            break

        elif event == 'st':
            tree.change_task_solution_text(index, get_text_big('Введите текст решения задания', tree.get_task(index)['solution']['text']))
            break

        elif event == 'si':
            tree.change_task_solution_image(index, sg.popup_get_file('Выберете файл картинки решения (.png)'))
            break

    win.close()

def get_index(obj, l):
    for i in range(len(l)):
        if l[i] == obj:
            return i
        
def get_text_big(message, default_text):
    layout = [
        [sg.Text(message)],
        [sg.Multiline(default_text, k='t', s=(30, 10))],
        [sg.Button('OK')]
    ]
    win = sg.Window('', layout)
    while True:
        event, values = win.read()

        if event == sg.WIN_CLOSED:
            win.close()
            return ''
        

        elif event == 'OK':
            win.close()
            return values['t']
        
def answer_preview_image(answer):
    layout = [
        [sg.Image(answer['image'])],
        [sg.Multiline(answer['text'], disabled=True, s=(60, 10))]
    ]

    win = sg.Window('', layout)

    while True:
        event, values = win.read()

        if event == sg.WIN_CLOSED:
            break

    win.close()

def task_preview_image(task):
    layout = [
        [sg.Image(task['image'])],
        [sg.Multiline(task['text'], disabled=True, s=(60, 10))],
        [sg.Button('Посмотреть ответ', k='pa')]
    ]

    win = sg.Window('', layout)

    while True:
        event, values = win.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == 'pa':
            if task['solution']['image']:
                answer_preview_image(task['solution'])
            else:
                sg.popup_scrolled(task['solution']['text'], size=(60, 10))

    win.close()

tree = Tasks_Tree()

layout = [
    [sg.Listbox(['..'] + tree.get_current_node_keys(), key='list', s=(30, 10))],
    [sg.Button('Открыть', key='o')],
    [sg.Button('Создать раздел разделов', key='cnn')],
    [sg.Button('Создать раздел задач', key='cnt')],
    [sg.Button('Добавить задачу', key='ct')],
    [sg.Button('Удалить раздел', key='dn')],
    [sg.Button('Удалить задачу', key='dt')],
    [sg.Button('Изменить', key='e')]
]
win = sg.Window('Tasks tree editor', layout)

click_counter = 0
current_click = ''

while True:
    event, values = win.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'cnn':
        tree.make_node(sg.popup_get_text('Введите название раздела'), False)

    elif event == 'cnt':
        tree.make_node(sg.popup_get_text('Введите название раздела'), True)

    elif event == 'ct':
        if tree.is_current_node_list():
            text = get_text_big('Введите текст задания', '')
            if sg.popup_yes_no('Вы хотите прикрепить изображение к задаче?') == 'Yes':
                file_path = sg.popup_get_file('Выберете файл изображения (.png)')
            else: file_path = ''
            text1 = get_text_big('Введите текст решения', '')
            if sg.popup_yes_no('Вы хотите прикрепить изображение к решению?') == 'Yes':
                file_path1 = sg.popup_get_file('Выберете файл изображения (.png)')
            else: file_path1 = ''
            tree.create_task({
                'text': text,
                'image': file_path,
                'solution': {
                    'text': text1,
                    'image': file_path1
                }
            })

    elif event == 'dn':
        if values['list']:
            tree.delete_node(values['list'][0])

    elif event == 'dt':
        if values['list']:
            if tree.is_current_node_list():
                l = tree.get_current_node_keys().copy()
                for i in range(len(l)):
                    l[i] = l[i]['text']
                tree.delete_task(get_index(values['list'][0], l))

    elif event == 'o':
        if values['list']:
            if tree.is_current_node_list():
                if values['list'][0] == '..':
                    tree.change_current_node('..')
                else:
                    l = tree.get_current_node_keys().copy()
                    for i in range(len(l)):
                        l[i] = l[i]['text']
                    task = tree.get_task(get_index(values['list'][0], l))
                    task_preview_image(task)
            else:
                tree.change_current_node(values['list'][0])

    elif event == 'e':
        if values['list']:
            if tree.is_current_node_list():
                l = tree.get_current_node_keys().copy()
                for i in range(len(l)):
                    l[i] = l[i]['text']
                edit_task(get_index(values['list'][0], l))
            else:
                tree.rename_node(values['list'][0], sg.popup_get_text('Введите новое имя раздела', default_text=values['list'][0]))

    if tree.is_current_node_list():
        l = tree.get_current_node_keys().copy()
        for i in range(len(l)):
            l[i] = l[i]['text']
        win['list'].update(values=['..'] + l)
    else:
        win['list'].update(values=['..'] + tree.get_current_node_keys())

win.close()