from datetime import datetime
startTime = datetime.now()

hand_1 = open("C:/Users/Vitaly/Desktop/bar_codes/result_1.txt", 'r', encoding = 'utf-8')
#hand_2 = open("C:/Users/Vitaly/Desktop/bar_codes/result_2.txt", 'r', encoding = 'utf-8')
hand_1_sorted = open("C:/Users/Vitaly/Desktop/bar_codes/hand_1_sorted.txt", 'w', encoding = 'utf-8')
print('Файлы открыты')

lines = hand_1.readlines()
lines.sort()
for line in lines:
    hand_1_sorted.write(line)

hand_1.close()
#hand_2.close()
hand_1_sorted.close()

print('Все файлы закрыты, программа завершена')
print('Время выполнения программы:', datetime.now() - startTime)
