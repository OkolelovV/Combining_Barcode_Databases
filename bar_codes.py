#for 8 digit codes there is a special programme in 8 folder

REAL_NUMBER = 9282304
NUMBER = REAL_NUMBER

from datetime import datetime
startTime = datetime.now()

file_input_hand = open('output', 'r', encoding = 'utf-8')
#hand_result = open('result_1.txt', 'w', encoding = 'utf-8')
hand_8_ean8 = open('result_8_ean8.txt', 'w', encoding = 'utf-8')
#hand_8_upce = open('result_8_upce.txt', 'w', encoding = 'utf-8')
hand_8_bad = open('result_8_bad.txt', 'w', encoding = 'utf-8')
#hand_12_fixed = open('result_12_fixed.txt', 'w', encoding = 'utf-8')
#hand_12_upca = open('result_12_upca.txt', 'w', encoding = 'utf-8')
#hand_12_bad = open('result_12_bad.txt', 'w', encoding = 'utf-8')
#hand_13_good = open('result_13_good.txt', 'w', encoding = 'utf-8')
#hand_13_fixed = open('result_13_fixed.txt', 'w', encoding = 'utf-8')
#hand_13_bad = open('result_13_bad.txt', 'w', encoding = 'utf-8')
#hand_wrong_description  = open('result__wrong_description.txt', 'w', encoding = 'utf-8')
print('Файлы открыты')

count_wrong_description = 0
count_8_ean8 = 0
#count_8_upce = 0
count_8_bad = 0
count_12_fixed = 0
count_12_upca = 0
count_12_bad = 0
count_13_good = 0
count_13_fixed = 0
count_13_bad = 0
count_2 = 0
count_000 = 0
count_bad_length = 0
count_empty = 0
count = 0

for line in file_input_hand:
    #if count >= NUMBER:
    #    break
    words = line.split(':', 1)
    code = words[0]
    description = words[1].strip() + '\n'
    if description.startswith('??') or description.startswith('Наименование неизвестно'):
        count_wrong_description += 1
    elif code.isdigit() == False:
        count_empty += 1
    elif code[0] == '2':
        count_2 += 1
    elif code.startswith('000'):
        count_000 += 1

    elif len(code) == 13:
        even = int(code[10]) + int(code[8]) + int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
        odd = int(code[11]) + int(code[9]) + int(code[7]) + int(code[5]) + int(code[3]) + int(code[1])
        check_digit = 3 * odd + even
        check_digit = (10 - check_digit % 10) % 10
        if check_digit == int(code[12]):
            #hand_13_good.write(code + ':' + description)
            #hand_result.write(code + ':' + description)
            count_13_good += 1
        elif code.startswith('460'):
            #hand_13_fixed.write(code[0:12] + str(check_digit) + ':' + description)
            #hand_result.write(code[0:12] + str(check_digit) + ':' + description)
            count_13_fixed += 1
        else:
            #hand_13_bad.write(code + ':' + description)
            count_13_bad += 1

    elif len(code) == 12:
        even = int(code[9]) + int(code[7]) + int(code[5]) + int(code[3]) + int(code[1])
        odd = int(code[10]) + int(code[8]) + int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
        check_digit = 3 * odd + even
        check_digit = (10 - check_digit % 10) % 10
        if check_digit == int(code[11]):
            #hand_12_upca.write(code + ':' + description)
            #hand_result.write(code + ':' + description)
            count_12_upca += 1
        elif code.startswith('460'):
            even = int(code[10]) + int(code[8]) + int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
            odd = int(code[11]) + int(code[9]) + int(code[7]) + int(code[5]) + int(code[3]) + int(code[1])
            check_digit = 3 * odd + even
            check_digit = (10 - check_digit % 10) % 10
            #hand_12_fixed.write(code + str(check_digit) + ':' + description)
            #hand_result.write(code + str(check_digit) + ':' + description)
            count_12_fixed += 1
        else:
            #hand_12_bad.write(code + ':' + description)
            count_12_bad += 1

    elif len(code) == 8:
        even = int(code[5]) + int(code[3]) + int(code[1])
        odd = int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
        check_digit = 3 * odd + even
        check_digit = (10 - check_digit % 10) % 10
        if check_digit == int(code[7]):
            hand_8_ean8.write(code + ':' + description)
            #hand_result.write(code + ':' + description)
            count_8_ean8 += 1
        else:
            hand_8_bad.write(code + ':' + description)
            count_8_bad += 1

    else:
        count_bad_length += 1
    #count += 1

sum_check = count_8_ean8 + count_8_bad + count_12_fixed + count_12_upca + count_12_bad + count_13_good + count_13_fixed + count_13_bad + count_000 + count_2 + count_bad_length + count_empty + count_wrong_description
print('Проверка суммы:', sum_check == NUMBER)
print('Total:', count_8_ean8 + count_12_fixed + count_12_upca + count_13_good + count_13_fixed)

print("Число EAN-8:", count_8_ean8 , '{:.2%}'.format(count_8_ean8  / NUMBER))
#print("Число UPC-E:", count_8_upce , '{:.2%}'.format(count_8_upce  / NUMBER))
print("Число плохих 8:", count_8_bad , '{:.2%}'.format(count_8_bad  / NUMBER))
print("Число UPCA:", count_12_upca , '{:.2%}'.format(count_12_upca  / NUMBER))
print("Число починенных 12:", count_12_fixed , '{:.2%}'.format(count_12_fixed  / NUMBER))
print("Число плохих 12:", count_12_bad , '{:.2%}'.format(count_12_bad  / NUMBER))
print("Число хороших 13:", count_13_good , '{:.2%}'.format(count_13_good  / NUMBER))
print("Число починенных 13:", count_13_fixed , '{:.2%}'.format(count_13_fixed  / NUMBER))
print("Число плохих 13:", count_13_bad , '{:.2%}'.format(count_13_bad  / NUMBER))
print("Число пустых:", count_empty, '{:.2%}'.format(count_empty / NUMBER))
print("Число с 2:", count_2, '{:.2%}'.format(count_2 / NUMBER))
print("Число с 000:", count_000, '{:.2%}'.format(count_000 / NUMBER))
print("Число с неправильным описанием:", count_wrong_description, '{:.2%}'.format(count_wrong_description / NUMBER))
print("Число с плохой длиной:", count_bad_length, '{:.2%}'.format(count_bad_length / NUMBER))

file_input_hand.close()
#hand_result.close()
hand_8_ean8.close()
#hand_8_upce.close()
hand_8_bad.close()
#hand_12_fixed.close()
#hand_12_upca.close()
#hand_12_bad.close()
#hand_13_good.close()
#hand_13_fixed.close()
#hand_13_bad.close()
#hand_wrong_description.close()
print('Все файлы закрыты, программа завершена')
print('Время выполнения программы:', datetime.now() - startTime)
