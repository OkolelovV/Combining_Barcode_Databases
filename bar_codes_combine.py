#bar_codes.py checks a text file, new_bars.py combines and checks many databases
#sort.py sorts them, bar_codes_combine.py makes a combined database (also can print it)

from datetime import datetime
import sqlite3

conn = sqlite3.connect('Bar_codes.sqlite')
cur = conn.cursor()

filename_1 = "C:/Users/Vitaly/Desktop/bar_codes/hand_1_sorted.txt"
filename_2 = "C:/Users/Vitaly/Desktop/bar_codes/hand_2_+upce.txt"
filename_final = "C:/Users/Vitaly/Desktop/bar_codes/final.txt"
filename_atol = "C:/Users/Vitaly/Desktop/bar_codes/atol.txt"
def update(code, position, new):
    cur.execute('UPDATE Bar_codes SET description_%d = ? WHERE code = ?' % position, (new, code))
    return

def check_1_in_2(set_1, set_2):
    for element_1 in set_1:
        flag = 0
        for element_2 in set_2:
            if element_1 in element_2:
                flag = 1
                break
        if not flag:
            return 0
    return 1

#Version 1
#Version 2: Lowercase comparison added
#Version 3: Changed into logic function
#Version 4: word-by-word comparison added (bug: exact coincidence only)
#Version 5: word-by-word comparison fixed (checks words in words)
def handle_two_v5(code, old_unprocessed, new_unprocessed):
    old = set(old_unprocessed.lower().split())
    new = set(new_unprocessed.lower().split())
    if old_unprocessed is new_unprocessed or check_1_in_2(new, old):
        return 0
    elif check_1_in_2(old, new):
        return 1
    else:
        return 2

#Version 5.1: + broken logic fixed: updates two olds at the same time
def handle_three_v5(code, old_1_unprocessed, old_2_unprocessed, new_unprocessed):
    old_1 = set(old_1_unprocessed.lower().split())
    old_2 = set(old_2_unprocessed.lower().split())
    new = set(new_unprocessed.lower().split())
    if old_1_unprocessed is new_unprocessed or old_1_unprocessed is new_unprocessed or check_1_in_2(new, old_1) or check_1_in_2(new, old_2):
        return 0
    check_1 = check_1_in_2(old_1, new)
    check_2 = check_1_in_2(old_2, new)
    if check_1 and check_2:
        return 4
    elif check_1:
        return 1
    elif check_2:
        return 2
    else:
        return 3

def printing_action_2(action):
    if action == 0:
        return "Удалено"
    elif action == 1:
        return "Наименование обновлено"
    else:
        return "Добавлено второе наименование"

def printing_action_3(action):
    if action == 0:
        return "Удалено"
    elif action == 1:
        return "Первое наименование обновлено"
    elif action == 2:
        return "Второе наименование обновлено"
    elif action == 3:
        return "Добавлено третье наименование"
    else:
        return "Третье заменило два"

def checking_codes(filename):
    count_new = 0
    count_duplicates = 0
    count_updated = 0
    count_added_second = 0
    count_removed = 0
    count_added_third = 0
    count_two_into_one = 0

    print('\nФайл', filename, 'открыт')
    startTime = datetime.now()
    with open(filename, 'r', encoding = 'utf-8') as hand:
        for count, line in enumerate(hand, 1):
            words = line.split(":", 1)
            code = words[0]
            description = words[1].strip()
            cur.execute('SELECT description_1, description_2 FROM Bar_codes WHERE code = ? ', (code,))
            selected_field = cur.fetchone()
            if selected_field is None:
                cur.execute('INSERT INTO Bar_codes (code, description_1) VALUES (?, ?)', (code, description))
                count_new += 1
            elif selected_field[1] is None:
                count_duplicates += 1
                action = handle_two_v5(code, selected_field[0], description)
                # print('V5:', printing_action_2(action))
                # print(selected_field[0] + '\n' + description + '\n')
                if action == 2:
                    count_added_second += 1
                    update(code, 2, description)
                elif action == 1:
                    count_updated += 1
                    update(code, 1, description)
                else:
                    count_removed += 1
            else:
                count_duplicates += 1
                action = handle_three_v5(code, selected_field[0], selected_field[1], description)
                # print('V5:', printing_action_3(action))
                # print(selected_field[0] + '\n' + selected_field[1] + '\n' + description + '\n')
                if action == 3:
                    count_added_third += 1
                    update(code, 3, description)
                elif action == 1:
                    count_updated += 1
                    update(code, 1, description)
                elif action == 2:
                    count_updated += 1
                    update(code, 2, description)
                elif action == 4:
                    count_two_into_one += 1
                    cur.execute('UPDATE Bar_codes SET description_1 = ?, description_2 = NULL WHERE code = ?', (description, code))
                else:
                    count_removed += 1
        conn.commit()
    print('Файл', filename, 'закрыт')
    print('Время проверки файла:', datetime.now() - startTime)

    print("{:.<32}: {:d}".format('Все штрих-кодов было в файле', count))
    print("{:.<32}: {:7d} ({:.2f}%)".format('Новые штрих-коды', count_new, 100 * count_new / count))
    print("{:.<32}: {:7d} ({:.2f}%)".format('Совпадающие штрих-коды', count_duplicates, 100 * count_duplicates / count))
    print("{:.<32}: {:7d} ({:.2f}%)".format('Обновлено наименований', count_updated, 100 * count_updated / count))
    print("{:.<32}: {:7d} ({:.2f}%)".format('Дописано второе наименование', count_added_second, 100 * count_added_second / count))
    print("{:.<32}: {:7d} ({:.2f}%)".format('Удалено наименований', count_removed, 100 * count_removed / count))
    print("{:.<32}: {:7d} ({:.2f}%)".format('Дописано третье наименование', count_added_third, 100 * count_added_third / count))
    print("{:.<32}: {:7d} ({:.2f}%)".format('Третье наименование заменило два', count_two_into_one, 100 * count_two_into_one / count))

    return

def print_table(filename):
    print("Подготовка таблицы...")
    cur.execute('SELECT * FROM Bar_codes ORDER BY code ASC')
    rows = cur.fetchall()

    print('Файл', filename, 'открыт на печать таблицы...')
    with open(filename, 'w', encoding = 'utf-8') as file_ref:
        for count, row in enumerate(rows, 1):
            if row[2] == None:
                file_ref.write(row[0] + ':' + row[1] + '\n')
            elif row[3] == None:
                file_ref.write(row[0] + ':' + '; '.join(row[1:3]) + '\n')
            else:
                file_ref.write(row[0] + ':' + '; '.join(row[1:]) + '\n')
    cur.close()

    print("Всего:", count)
    print('Печать таблицы завершена')
    return

def print_atol(filename):
    print("Подготовка таблицы...")
    cur.execute('SELECT * FROM Bar_codes ORDER BY code')
    rows = cur.fetchall()

    print('Файл', filename, 'открыт на печать таблицы...')
    with open(filename, 'w', encoding = 'utf-8') as file_ref:
        file_ref.write('##@@&&\n#\n$$$ADDQUANTITY\n')
        for count, row in enumerate(rows, 1):
            file_ref.write(';'.join([str(count), row[0], row[1], row[1], ';9,99;;;0,1,1,0,0,0,0,1;;;;;;;;;1;;;;;;;;;;;;;;;;\n']))
        cur.close()

    print("Всего:", count)
    print('Печать таблицы завершена')
    return

while True:
    answer = input("Какие базы проверить? (0 - никакие, 1, 2, enter - обе): ")
    #answer = ''
    if answer != '0':
        cur.executescript('''DROP TABLE IF EXISTS Bar_codes;
        CREATE TABLE Bar_codes (
            code TEXT UNIQUE,
            description_1  TEXT,
            description_2  TEXT,
            description_3  TEXT
        )
        ''')
    if answer == '':
        checking_codes(filename_1)
        checking_codes(filename_2)
        break
    elif answer == '1':
        checking_codes(filename_1)
        break
    elif answer == '2':
        checking_codes(filename_2)
        break
    elif answer == '0':
        break
    else:
        print("Неверная команда. Попробуйте ещё раз")

answer = input("\nНапечатать таблицу в файл? (enter - нет, 1 - да, 2 - АТОЛ): ")
if answer == '1':
    print_table(filename_final)
elif answer == '2':
    print_atol(filename_atol)

cur.close()
print('Программа завершена')
