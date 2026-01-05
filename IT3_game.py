import random #для рандомных событий
import os #для сохранения результатов

class Item: #вообще все что связано с предметами
    """Предметы"""
    def __init__(self, name, description, exam_bonus=0, is_cheatsheet=False, is_notebook_with_notes=False): #по сути конструктор предметов, он нужен чтобы распределить предметы по категориям которые ниже
        self.name = name
        self.description = description
        self.exam_bonus = exam_bonus
        self.is_cheatsheet = is_cheatsheet
        self.is_notebook_with_notes = is_notebook_with_notes
        self.used = False
    
    def use_on_exam(self): #это используется на экзамене, использован предмет иои нет
        if self.used:
            return False, f"{self.name} уже использована"
        
        self.used = True
        
        if self.is_cheatsheet:
            return True, f"Использовал '{self.name}'"
        elif self.is_notebook_with_notes:
            return True, f"Использовал {self.name} с конспектами"
        else:
            return True, f"Использовал {self.name}"

class Student: #хранит всю информацию о студенте, о его предметах, проспал или нет и тд
    def __init__(self, name):
        self.name = name
        self.has_eaten = False
        self.is_late = False
        self.exam_passed = False
        self.grade = None
        self.inventory = []
        self.cheat_sheet_made = False
        self.game_won_with_professor = False
        self.bonus_points = 0
        self.slept_well = True  #
    
    def add_item(self, item):
        self.inventory.append(item)
    
    def get_cheat_sheet(self):
        for item in self.inventory:
            if item.is_cheatsheet:
                return item
        return None
    
    def get_notebook(self):
        for item in self.inventory:
            if item.name == "Тетрадь":
                return item
        return None
    
    def get_notebook_with_notes(self):
        for item in self.inventory:
            if item.is_notebook_with_notes:
                return item
        return None
    
    def get_phone(self):
        for item in self.inventory:
            if item.name == "Телефон":
                return item
        return None
    
    def get_bun(self):
        for item in self.inventory:
            if item.name == "Бутер с колбасой":
                return item
        return None
    
    def show_inventory(self):
        if not self.inventory:
            return "Карманф пусты"
        result = "Что у тебя есть:\n"
        for i, item in enumerate(self.inventory, 1):
            result += f"  {i}. {item.name}"
            if item.is_cheatsheet:
                result += " (шпаргалка)"
            if item.is_notebook_with_notes:
                result += " (конспекты)"
            result += "\n"
        return result
    
    def eat_bun(self):
        for i, item in enumerate(self.inventory):
            if item.name == "Бутер с колбасой":
                self.inventory.pop(i)
                self.has_eaten = True
                return True
        return False

class Game: #сам движок игры
    def __init__(self):#здесь в основном основа игры
        self.student = None
        self.game_active = False
        self.results_file = "game_results.txt"
        self.current_scene = None
        self.exam_subject = "Инфе"
    
    def show_title(self):#здесь мы выбираем какой-то из варинтов когда в игре будет выбор
        print("ДЕНЬ СТУДЕНТА: ЭКЗАМЕН")
    
    def get_choice(self, prompt, options):
        while True:
            print(f"\n{prompt}")
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
            
            try:
                choice = int(input("\nТвой выбор: "))
                if 1 <= choice <= len(options):
                    return choice
                else:
                    print(f"Выбери от 1 до {len(options)}")
            except ValueError:
                print("Введи число!")
    
    def will_catch_cheating(self, is_late, using_notebook_with_notes=False):#про читы и списывание
        if using_notebook_with_notes:
            return False
            
        if is_late:
            return random.random() < 0.75 #25% шанс списать при опоздании
        else:
            return random.random() < 0.5  #50% шанс списать если воврмя
    
    def play_rock_paper_scissors(self): #камень ножницы бумага
        print("\nПреподаватель предлагает сыграть в камень ножницы бумага")
        print("Первым до 2 побед!")
        
        player_wins = 0
        professor_wins = 0
        rounds_played = 0
        
        #Обозначения что есть что
        choices_dict = {
            1: "камень",
            2: "ножницы", 
            3: "бумага"
        }
        
        #Правила
        win_rules = {
            "камень": "ножницы", #камень бьет ножницы
            "ножницы": "бумагу", #ножницы бьют бумагу
            "бумага": "камень" #бумага бьет камень
        }
        
        while player_wins < 2 and professor_wins < 2 and rounds_played < 5:
            rounds_played += 1
            print(f"\nРаунд {rounds_played}")
            print(f"Счет: Ты {player_wins} - {professor_wins} Преподаватель")
            
            try:
                player_choice_num = self.get_choice(
                    "Выбери:",
                    ["камень", "ножницы", "бумага"]
                )
                
                player_choice = choices_dict[player_choice_num]
                professor_choice = random.choice(["камень", "ножницы", "бумага"])
                
                print(f"\nТвой выбор: {player_choice}")
                print(f"Выбор преподавателя: {professor_choice}")
                
                if player_choice == professor_choice:
                    print("Ничья")
                elif win_rules[player_choice] == professor_choice:
                    print(f"{player_choice.capitalize()} бьет {professor_choice} Ты выиграл раунд")
                    player_wins += 1
                else:
                    print(f"{professor_choice.capitalize()} бьет {player_choice}! Преподаватель выиграл раунд")
                    professor_wins += 1
                    
            except:
                print("Некорректный ввод!")
        
        print(f"\nФИНАЛЬНЫЙ СЧЕТ")
        print(f"Ты {player_wins} - {professor_wins} Преподаватель")
        
        if player_wins == 2:
            print("Ты выиграл игру")
            return True
        else:
            print("Преподаватель выиграл игру")
            return False
    
    def save_result(self, result, is_win):
        try:
            with open(self.results_file, "a", encoding="utf-8") as f:
                if is_win:
                    f.write(f"[ПОБЕДА] {self.student.name}: {result}, Оценка: {self.student.grade}\n")
                else:
                    f.write(f"[ПРОИГРЫШ] {self.student.name}: {result}\n")
        except:
            pass
    
    def game_over(self, reason):
        print("ИГРА ОКОНЧЕНА")
        print(f"\n{reason}")
        
        self.save_result(reason, is_win=False)
        self.game_active = False
    
    def game_won(self, reason):
        print("ПОБЕДА!")
        print(f"\n{reason}")
        print(f"Оценка: {self.student.grade}")
        
        self.save_result(reason, is_win=True)
        self.game_active = False
    
    def preparation_scene(self):#до экзамена
        self.current_scene = "подготовка"
        print("НАКАНУНЕ ЭКЗАМЕНА")
        
        print(f"\n{self.student.name}, завтра экзамен по {self.exam_subject}.")
        print("У тебя есть: бутер, тетрадь, ручка")
        
        
        self.student.add_item(Item("Бутер", "С колбасой", 0))
        self.student.add_item(Item("Тетрадь", "Для конспектов", 2))
        self.student.add_item(Item("Ручка", "Писать ответы", 1))
        
        print("\nТвои вещи:")
        print(self.student.show_inventory())
        
        prep_choice = self.get_choice(
            "Твои действия вечером:",
            [
                "Готовить шпаргалку",
                "Поспать"
            ]
        )
        
        if prep_choice == 1:
            print("\nТы усердно готовил шпаргалку до поздней ночи")
            print("Засыпаешь под утро, очень уставший.")
            self.student.add_item(Item(
                "Шпаргалка", 
                "Отличная шпаргалка", 
                3, True
            ))
            self.student.cheat_sheet_made = True
            self.student.slept_well = False
            print("Теперь у тебя есть шпаргалка, но ты не выспался")
        
        else:
            print("\nТы решил хорошо выспаться.")
            print("Ложишься спать пораньше и крепко спишь.")
            self.student.cheat_sheet_made = False
            self.student.slept_well = True
        
        input("\nНажми enter чтобы лечь спать")
        return True
    
    def morning_scene(self): #утро экзамена, тут студент либо выспался либо нет
        self.current_scene = "утро"
        print("УТРО ЭКЗАМЕНА")
        
        print(f"\n{self.student.name}, сегодня экзамен")
        
        if not self.student.slept_well:
            print("\nТЫ ПРОСПАЛ!")
            print("Ты готовил шпаргалку до поздней ночи и не услышал будильник")
            print("Быстро собираешься и выбегаешь из дома")
            self.student.is_late = True
            
            if self.student.get_bun():
                print("\nПо дороге завтракаешь бутером")
                self.student.eat_bun()
                self.student.has_eaten = True
                print("Бутер дал чуть энергии")
            else:
                self.student.has_eaten = False
            
            print("\nТы опаздываешь на экзамен")
            return True
        
        print("\nТы хорошо выспался, просыпаешься вовремя.")
        
        print("\nТвои вещи:")
        print(self.student.show_inventory())
        
        breakfast_choice = self.get_choice(
            "Позавтракать бутером?",
            ["Да", "Нет"]
        )
        
        if breakfast_choice == 1:
            if self.student.eat_bun():
                print("\nТы съел бутер и полон энергии")
                self.student.has_eaten = True
            else:
                self.student.has_eaten = False
        else:
            print("\nТы не завтракал")
            self.student.has_eaten = False
        
        print("\nПора на экзамен")
        
        if self.student.has_eaten:
            print("Ты полон энергии и успеваешь на автобус")
            print("Приезжаешь вовремя")
            self.student.is_late = False
        else:
            print("Без завтрака у тебя нет энергии")
            print("Не успеваешь на автобус и опаздываешь")
            self.student.is_late = True
        
        return True
    
    def exam_scene(self):#экзамен сам, игра с преподавателем
        self.current_scene = "экзамен"
        
        if self.student.is_late:
            print("ЭКЗАМЕН: ОПОЗДАЛ")
            
            print(f"\n{self.student.name}, ты опаздываешь!")
            print("Преподаватель смотрит на тебя оч сердито")
            
            
            print("\nПреподаватель: 'Ты опоздал! Но давай сыграем в камень ножницы бумага'")
            print("'Если выиграешь разрешу сдать экзамен'")
            
            if self.play_rock_paper_scissors():
                print("\nПреподаватель: 'Хорошо, садись на первую парту'")
                return self.late_exam_choices()
            else:
                print("\nПреподаватель: 'Не повезло, до свидания'")
                self.game_over("Проиграл игру с преподавателем при опоздании")
                return False
        
        else:
            print("ЭКЗАМЕН: ВОВРЕМЯ")
            
            print(f"\n{self.student.name}, ты вовремя")
            print("Преподаватель доволен")
            
            print("\nПреподаватель: 'Молодец, что пришел вовремя. Сыграем в камень ножницы бумага?'")
            print("'Если выиграешь получишь бонус'")
            
            if self.play_rock_paper_scissors():
                print("\nПреподаватель: 'Выбирай награду:'")
                bonus_choice = self.get_choice(
                    "Какой бонус хочешь?",
                    ["+1 балл к оценке", "Тетрадь с конспектами"]
                )
                
                if bonus_choice == 1:
                    print("Получил +1 балл к оценке")
                    self.student.bonus_points += 1
                else:
                    print("Получил тетрадь с конспектами")
                    self.student.add_item(Item(
                        "Тетрадь с конспектами", 
                        "Полезные конспекты с лекций", 
                        4, 
                        is_notebook_with_notes=True
                    ))
                
                self.student.game_won_with_professor = True
            
            return self.on_time_exam_choices()
    
    def late_exam_choices(self):# тут дается выбор который влияет на сюжет
        print("\nТы садищься на первую парту и получаешь билет")
        
        if not self.student.slept_well:
            print("Ты все еще сонный после ночной подготовки")
        
        cheat_sheet = self.student.get_cheat_sheet()
        phone = self.student.get_phone()
        notebook_with_notes = self.student.get_notebook_with_notes()
        
        options = []
        
        if cheat_sheet and not cheat_sheet.used:
            options.append("Использовать шпаргалку")
        
        if notebook_with_notes and not notebook_with_notes.used:
            options.append("Использовать тетрадь с конспектами")
        
        options.append("Попросить помощи у отличника")
        
        if phone:
            options.append("Списать с телефона")
        
        options.append("Выйти в туалет")
        options.append("Ничего не делать")
        
        choice = self.get_choice("Что делаешь?", options)
        
        if cheat_sheet and not cheat_sheet.used and choice == 1:
            success, message = cheat_sheet.use_on_exam()
            print(f"\n{message}")
            
            if not self.will_catch_cheating(is_late=True):
                print("Красава получилось списать")
                self.student.grade = "5"
                self.student.exam_passed = True
                return self.final_scene()
            else:
                print("Не получилось списать увы")
                self.game_over("Поймали на шпаргалке")
                return False
        
        notebook_index = 1
        if cheat_sheet and not cheat_sheet.used:
            notebook_index = 2
        
        if notebook_with_notes and not notebook_with_notes.used and choice == notebook_index:
            success, message = notebook_with_notes.use_on_exam()
            print(f"\n{message}")
            
            print("Тетрадь с конспектами это разрешенный материал")
            print("Ты используешь конспекты и отлично отвечаешь на вопросы.")
            self.student.grade = "5"
            self.student.exam_passed = True
            return self.final_scene()
        
        base_index = 1
        if cheat_sheet and not cheat_sheet.used:
            base_index += 1
        if notebook_with_notes and not notebook_with_notes.used:
            base_index += 1

        if choice == base_index:
            print("\nПросишь помощи у отличника")
            
            if not self.will_catch_cheating(is_late=True):
                print("Отличник помог, удалось списать.")
                self.student.grade = "4"
                self.student.exam_passed = True
                return self.final_scene()
            else:
                print("Тебя спалил преподаватель за списыванием")
                self.game_over("Поймали на списывании.")
                return False

        elif phone and choice == base_index + 1:
            print("\nПытаешься списать с телефона")
            
            if not self.will_catch_cheating(is_late=True):
                print("Удалось списать с телефона")
                self.student.grade = "4"
                self.student.exam_passed = True
                return self.final_scene()
            else:
                print("Тебя поймали, слишком часто смотрел под парту.")
                self.game_over("Поймали с телефоном.")
                return False
        
        elif choice == (base_index + 2 if phone else base_index + 1):
            print("\nВыходишь в туалет")
            print("В туалете встречаешь подставного ученика")
            print("Он говорит: 'Не сегодня дружище' и не дает списать, забирая шпору")
            print("Пришлось вернуться без шпаргалки.")
            
            print("\nВозвращаешься в аудиторию")
            print("Не успеваешь ответить на вопросы")
            self.game_over("Потратил время в туалете")
            return False
        
        else:
            print("\nСидишь и ничего не делаешь")
            if not self.student.slept_well:
                print("Ты слишком сонный, чтобы думать")
            print("Не знаешь ответов на вопросы")
            self.game_over("Не ответил на вопросы")
            return False
    
    def on_time_exam_choices(self):#если студент пришел вовремя
        print("\nПолучаешь билет")
        
        cheat_sheet = self.student.get_cheat_sheet()
        phone = Item("Телефон", "Смартфон", 0)
        self.student.add_item(phone)
        notebook_with_notes = self.student.get_notebook_with_notes()
        
        options = []
        
        if cheat_sheet and not cheat_sheet.used:
            options.append("Использовать шпаргалку")
        
        if notebook_with_notes and not notebook_with_notes.used:
            options.append("Использовать тетрадь с конспектами")
        
        options.append("Попросить помощи у отличника")
        options.append("Списать с телефона")
        options.append("Выйти в туалет")
        options.append("Ничего не делать")
        
        choice = self.get_choice("Что делаешь?", options)
        
        if cheat_sheet and not cheat_sheet.used and choice == 1:
            success, message = cheat_sheet.use_on_exam()
            print(f"\n{message}")
            
            if not self.will_catch_cheating(is_late=False):
                print("Красава получилось списать")
                base_grade = 5
                if self.student.bonus_points > 0:
                    base_grade = min(5, base_grade + self.student.bonus_points)
                self.student.grade = str(base_grade)
                self.student.exam_passed = True
                return self.final_scene()
            else:
                print("Поймали на использовании шпаргалки")
                self.game_over("Поймали на шпаргалке")
                return False
        
        if notebook_with_notes and not notebook_with_notes.used and choice == (2 if cheat_sheet and not cheat_sheet.used else 1):
            success, message = notebook_with_notes.use_on_exam()
            print(f"\n{message}")
            
            print("Тетрадь с конспектами - это разрешенный материал")
            print("Ты используешь конспекты и отлично отвечаешь на вопросы")
            base_grade = 5
            if self.student.bonus_points > 0:
                base_grade = min(5, base_grade + self.student.bonus_points)
            self.student.grade = str(base_grade)
            self.student.exam_passed = True
            return self.final_scene()

        base_index = 1
        if cheat_sheet and not cheat_sheet.used:
            base_index += 1
        if notebook_with_notes and not notebook_with_notes.used:
            base_index += 1
        

        if choice == base_index:
            print("\nПросишь помощи у отличника")
            
            if not self.will_catch_cheating(is_late=False):
                print("Отличник помог, удалось списать")
                base_grade = 4
                if self.student.bonus_points > 0:
                    base_grade = min(5, base_grade + self.student.bonus_points)
                self.student.grade = str(base_grade)
                self.student.exam_passed = True
                return self.final_scene()
            else:
                print("Тебя спалил преподаватель за списыванием")
                self.game_over("Поймали на списывании")
                return False

        elif choice == base_index + 1:
            print("\nПытаешься списать с телефона")
            
            if not self.will_catch_cheating(is_late=False):
                print("Удалось списать с телефона")
                base_grade = 4
                if self.student.bonus_points > 0:
                    base_grade = min(5, base_grade + self.student.bonus_points)
                self.student.grade = str(base_grade)
                self.student.exam_passed = True
                return self.final_scene()
            else:
                print("Тебя поймали, слишком часто смотрел под парту")
                self.game_over("Поймали с телефоном")
                return False

        elif choice == base_index + 2:
            print("\nВыходишь в туалет")
            print("В туалете встречаешь подставного ученика")
            print("Он говорит: 'Не сегодня дружище' и не дает списать, забирая шпору")
            print("Пришлось вернуться без шпаргалки")
            
            print("\nВозвращаешься в аудиторию")
            print("Не успеваешь ответить на вопросы")
            self.game_over("Потратил время в туалете")
            return False
        
        else:
            print("\nСидишь и ничего не делаешь")
            print("Не знаешь ответов на вопросы")
            self.game_over("Не ответил на вопросы")
            return False
    
    def final_scene(self):
        self.current_scene = "финал"
        
        print("ЭКЗАМЕН СДАН!")
        
        print(f"\n{self.student.name}, ты сдал экзамен на {self.student.grade}!")
        
        if self.student.game_won_with_professor:
            print("И еще выиграл игру с преподавателем!")
        
        if not self.student.slept_well:
            print("Несмотря на то что проспал из-за подготовки шпаргалки!")
        
        self.game_won(f"Сдал экзамен на {self.student.grade}")
        return True
    
    def start_game(self):
        print("НОВАЯ ИГРА")

        
        name = input("\nВведи имя студента: ").strip()
        if not name:
            name = "Студент"
        
        self.student = Student(name)
        self.game_active = True
        
        print(f"\n{self.student.name}, готовься к экзамену")
        
        input("\nНажми enter")
        
        if self.preparation_scene():
            if self.morning_scene():
                if self.exam_scene():
                    pass
    
    def main_menu(self):
        self.show_title()
        
        while True:
            print("ГЛАВНОЕ МЕНЮ")

            
            choice = self.get_choice(
                "Выбери действие:",
                ["Начать новую игру", "Выйти"]
            )
            
            if choice == 1:
                self.start_game()
                
                if not self.game_active:
                    play_again = input("\nСыграть еще раз? (да/нет): ").lower()
                    if play_again != "да":
                        print("\nСпасибо за игру!")
                        break
            else:
                print("\nПока!")
                break

def main():
    print("Игра: ДЕНЬ СТУДЕНТА: ЭКЗАМЕН")
    game = Game()
    game.main_menu()

if __name__ == "__main__":
    main()
