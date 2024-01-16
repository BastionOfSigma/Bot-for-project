import json, random, pathlib, os

basedir = os.path.dirname(os.path.abspath(__file__))

class Tasks_Tree:
    def __init__(self):
        with open(basedir + '/tasks_tree.json', encoding='utf-8') as f:
            self.tree = json.load(f)
        self.current_node = self.tree
        self.solved_tasks = []
        self.path = []
        self.last_task = None

    def save(self):
        with open(basedir + '/tasks_tree.json', 'w', encoding='utf-8') as f:
            json.dump(self.tree, f, indent=2, ensure_ascii=False)

    def change_current_node(self, node_name):
        if not type(self.current_node) is list:
            if node_name in self.current_node.keys():
                self.current_node = self.current_node[node_name]  #Смена текущего раздела, если ввести "..", то вернется в родительский раздел
                self.path.append(node_name)
        if node_name == '..':
            if self.path != []:
                del self.path[-1]
                self.current_node = self.tree
                for node in self.path:
                    self.current_node = self.current_node[node]

    def get_current_node_keys(self):
        if not type(self.current_node) is list:
            return list(self.current_node.keys()) #Получить список разделов в текущем разделе
        else: return self.current_node
        
    def is_current_node_list(self):
        return type(self.current_node) is list #Является ли данный раздел раздеом задач
    
    def make_node(self, node_name, is_list):
        if not node_name in self.get_current_node_keys() and not self.is_current_node_list():
            if is_list:
                self.current_node[node_name] = []
            else:
                self.current_node[node_name] = {}
        self.save()

    def delete_node(self, node_name):
        if not self.is_current_node_list():
            if node_name in self.get_current_node_keys():
                del self.current_node[node_name]
            self.save()

    def delete_task(self, index):
        if self.is_current_node_list():
            if index < len(self.get_current_node_keys()) and index > -1:
                if self.current_node[index]['image']:
                    try:
                        os.remove(self.current_node[index]['image'])
                        os.remove(self.current_node[index]['solution']['image'])
                    except: pass
                del self.current_node[index]
                self.save()

    def get_solution(self):
        return self.last_task['solution']     #Получить решение последней задачи

    def get_random_task(self):
        if type(self.current_node) is list:
            not_solved_tasks = []
            for task in self.current_node:
                if task not in self.solved_tasks:
                    not_solved_tasks.append(task)
            if not_solved_tasks:
                chosen_task = random.choice(not_solved_tasks)
                self.solved_tasks.append(chosen_task)
                self.last_task = chosen_task
                return chosen_task #Получить рандомное задание
            else:
                new_solved_tasks_list = []
                for task in self.solved_tasks:
                    if task not in self.current_node:
                        new_solved_tasks_list.append(task)
                return 'congratulations'
        else:
            return 'Error'
        
    def create_task(self, task):
        if type(task) is dict:
            if 'text' in task.keys() and 'image' in task.keys() and 'solution' in task.keys():
                if 'text' in task['solution'].keys() and 'image' in task['solution'].keys():
                    if self.is_current_node_list():
                        if task['image']:
                            file_name = basedir + '/images/' + '_'.join(self.path) + str(len(self.current_node)) + '.png'
                            try:
                                scr = pathlib.Path(task['image'])
                                dest = pathlib.Path(file_name)
                                dest.write_bytes(scr.read_bytes())
                            except Exception as e: return None
                            task['image'] = file_name
                        else:
                            task['image'] = ''

                        if task['solution']['image']:
                            file_name_2 = basedir + '/images/' + '_'.join(self.path) + str(len(self.current_node)) + 'answer.png'
                            try:
                                scr = pathlib.Path(task['solution']['image'])
                                dest = pathlib.Path(file_name_2)
                                dest.write_bytes(scr.read_bytes())
                            except: return None
                            task['solution']['image'] = file_name_2
                        self.current_node.append(task)
                        self.save()

    def get_task(self, index):
        if self.is_current_node_list():
            if index > -1 and index < len(self.current_node):
                return self.current_node[index]
        
    def rename_node(self, node_old_name, node_new_name):
        if node_old_name in self.get_current_node_keys():
            self.current_node[node_new_name] = self.current_node.pop(node_old_name)
            self.save()

    def change_task_text(self, index, new_text):
        if self.is_current_node_list():
            if index > -1 and index < len(self.current_node):
                self.current_node[index]['text'] = new_text
                self.save()

    def change_task_image(self, index, new_image_path):
        if self.is_current_node_list():
                if index > -1 and index < len(self.current_node):
                    if new_image_path == '':
                        if self.current_node[index]['image']:
                            try:
                                os.remove(self.current_node[index]['image'])
                            except: pass
                            self.current_node[index]['image'] = ''
                    if self.current_node[index]['image']:
                        try:
                            scr = pathlib.Path(new_image_path)
                            dest = pathlib.Path(self.current_node[index]['image'])
                            dest.write_bytes(scr.read_bytes())
                        except: return None
                    else:
                        file_name = basedir + '/images/' + '_'.join(self.path) + str(index) + '.png'
                        try:
                            scr = pathlib.Path(new_image_path)
                            dest = pathlib.Path(file_name)
                            dest.write_bytes(scr.read_bytes())
                        except: return None
                        self.current_node[index]['image'] = file_name
                    self.save()

    def change_task_solution_text(self, index, new_text):
        if self.is_current_node_list():
            if index > -1 and index < len(self.current_node):
                self.current_node[index]['solution']['text'] = new_text
                self.save

    def change_task_solution_image(self, index, new_image_path):
        if self.is_current_node_list():
            if index > -1 and index < len(self.current_node):
                solution = self.current_node[index]['solution']
                if new_image_path == '':
                    if solution['image']:
                        try:
                            os.remove(solution['image'])
                        except: pass
                        solution['image'] = ''
                elif solution['image']:
                    try:
                        scr = pathlib.Path(new_image_path)
                        dest = pathlib.Path(solution['image'])
                        dest.write_bytes(scr.read_bytes())
                    except: return None
                else:
                    file_name = basedir + '/images/' + '_'.join(self.path) + str(index) + 'answer.png'
                    try:
                        scr = pathlib.Path(new_image_path)
                        dest = pathlib.Path(file_name)
                        dest.write_bytes(scr.read_bytes())
                    except: return None
                    self.current_node[index]['solution']['image'] = file_name
                self.save()

if __name__ == '__main__':
    tree = Tasks_Tree()

    while True:
        print(tree.path)
        print(tree.current_node)
        print('---------------------------------------------------------')

        if tree.is_current_node_list():
            print('Нажмите "ввод", чтобы сгенерировать задачу')
            choise = input()
            if choise == '':
                print(tree.get_random_task())
            elif choise == '..':
                tree.change_current_node('..')
            else:
                print('Ошибка')

        else:
            print('Текущие разделы:\n' + '\n'.join(tree.get_current_node_keys()))
            choise = input()
            if choise in tree.get_current_node_keys() or choise == '..':
                tree.change_current_node(choise)
            else:
                print('Ошибка')