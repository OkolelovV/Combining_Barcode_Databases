from datetime import datetime
import sqlite3
from datetime import datetime

conn = sqlite3.connect('Bar_codes.sqlite')
cur = conn.cursor()

#fhand = open("C:/Users/Vitaly/Desktop/bar_codes/final.txt", 'r', encoding = 'utf-8')

while True:
    code = input("Ожидание ввода... ")
    if code == '':
        break

    startTime = datetime.now()
    cur.execute('SELECT description_1, description_2, description_3 FROM Bar_codes WHERE code = ? ', (code,))
    selected_field = cur.fetchone()

    if selected_field is None:
        print("Введённый штрих-код отстутствует в базе данных")
    elif selected_field[1] is None:
        print(code + ': ' + selected_field[0])
    elif selected_field[2] is None:
        print(code + ': ' + selected_field[0] + '; ' + selected_field[1])
    else:
        print(code + ': ' + selected_field[0] + '; ' + selected_field[1] + '; ' + selected_field[2])
    print('Время поиска:', datetime.now() - startTime)

cur.close()
#fhand.close()
print('Программа завершена')
