from datetime import datetime
startTime = datetime.now()

hand_result = open("C:/Users/Vitaly/Desktop/bar_codes/result_2.txt", 'w', encoding = 'utf-8')
hand_8_ean8 = open('result_8_ean8.txt', 'w', encoding = 'utf-8')
hand_8_upce = open('result_8_upce.txt', 'w', encoding = 'utf-8')
hand_8_bad = open('result_8_bad.txt', 'w', encoding = 'utf-8')
hand_12_fixed = open('result_12_fixed.txt', 'w', encoding = 'utf-8')
hand_12_upca = open('result_12_upca.txt', 'w', encoding = 'utf-8')
hand_12_bad = open('result_12_bad.txt', 'w', encoding = 'utf-8')
hand_13_good = open('result_EAN-13_good.txt', 'w', encoding = 'utf-8')
hand_13_fixed = open('result_EAN-13_fixed.txt', 'w', encoding = 'utf-8')
hand_13_bad = open('result_EAN-13_bad.txt', 'w', encoding = 'utf-8')
hand_wrong_description  = open('result_wrong_description.txt', 'w', encoding = 'utf-8')
hand_bad_length  = open('result_bad_length.txt', 'w', encoding = 'utf-8')
hand_2 = open('result_2.txt', 'w', encoding = 'utf-8')
hand_000 = open('result_000.txt', 'w', encoding = 'utf-8')
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

for i in range(1, 601):
    if i >= 100:
        filename = "uhtt_barcode_ref_0%d.csv" % i
    elif i >= 10:
        filename = "uhtt_barcode_ref_00%d.csv" % i
    else:
        filename = "uhtt_barcode_ref_000%d.csv" % i
    file_input_hand = open(filename, 'r', encoding = 'utf-8')
    next(file_input_hand)   #skip the header
    for line in file_input_hand:
        if count == 342387:
            print(i)
        words = line.split('	', 3)
        code = words[1]
        description = words[2].strip()
        if description.startswith('??') or description.startswith('Наименование неизвестно'):
            count_wrong_description += 1
            hand_wrong_description.write(code + ':' + description + '\n')
        elif code.isdigit() == False:
            count_empty += 1
            hand_empty.write(code + ':' + description + '\n')
        elif code[0] == '2':
            count_2 += 1
            hand_2.write(code + ':' + description + '\n')
        elif code.startswith('000'):
            count_000 += 1
            hand_000.write(code + ':' + description + '\n')

        elif len(code) == 13:
            even = int(code[10]) + int(code[8]) + int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
            odd = int(code[11]) + int(code[9]) + int(code[7]) + int(code[5]) + int(code[3]) + int(code[1])
            check_digit = 3 * odd + even
            check_digit = (10 - check_digit % 10) % 10
            if check_digit == int(code[12]):
                hand_13_good.write(code + ':' + description + '\n')
                hand_result.write(code + ':' + description + '\n')
                count_13_good += 1
            elif code.startswith('460'):
                hand_13_fixed.write(code[0:12] + str(check_digit) + ':' + description + '\n')
                hand_result.write(code[0:12] + str(check_digit) + ':' + description + '\n')
                count_13_fixed += 1
            else:
                hand_13_bad.write(code + ':' + description + '\n')
                count_13_bad += 1

        elif len(code) == 12:
            even = int(code[9]) + int(code[7]) + int(code[5]) + int(code[3]) + int(code[1])
            odd = int(code[10]) + int(code[8]) + int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
            check_digit = 3 * odd + even
            check_digit = (10 - check_digit % 10) % 10
            if check_digit == int(code[11]):
                hand_12_upca.write(code + ':' + description + '\n')
                hand_result.write(code + ':' + description + '\n')
                count_12_upca += 1
            elif code.startswith('460'):
                even = int(code[10]) + int(code[8]) + int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
                odd = int(code[11]) + int(code[9]) + int(code[7]) + int(code[5]) + int(code[3]) + int(code[1])
                check_digit = 3 * odd + even
                check_digit = (10 - check_digit % 10) % 10
                hand_12_fixed.write(code + str(check_digit) + ':' + description + '\n')
                hand_result.write(code + str(check_digit) + ':' + description + '\n')
                count_12_fixed += 1
            else:
                hand_12_bad.write(code + ':' + description + '\n')
                count_12_bad += 1

        elif len(code) == 8:
            even = int(code[5]) + int(code[3]) + int(code[1])
            odd = int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
            check_digit = 3 * odd + even
            check_digit = (10 - check_digit % 10) % 10
            if check_digit == int(code[7]):
                hand_8_ean8.write(code + ':' + description + '\n')
                hand_result.write(code + ':' + description + '\n')
                count_8_ean8 += 1
            else:
                hand_8_bad.write(code + ':' + description + '\n')
                count_8_bad += 1

        else:
            count_bad_length += 1
            hand_bad_length.write(code + ':' + description + '\n')
        count += 1

sum_check = count_8_ean8 + count_8_bad + count_12_fixed + count_12_upca + count_12_bad + count_13_good + count_13_fixed + count_13_bad + count_000 + count_2 + count_bad_length + count_empty + count_wrong_description
print('Всего наименований:', count)
print('Проверка суммы:', sum_check == count)
total = count_8_ean8 + count_12_fixed + count_12_upca + count_13_good + count_13_fixed
print('Всего рабочих:', total, '(%s)' % '{:.2%}'.format(total / count))

print("EAN-8:", count_8_ean8 , '(%s)' % '{:.2%}'.format(count_8_ean8 / count))
#print("Число UPC-E:", count_8_upce , "(%s)" % '{:.2%}'.format(count_8_upce  / count))
print("Плохие EAN-8 и UPC-E:", count_8_bad , '(%s)' % '{:.2%}'.format(count_8_bad / count))
print("UPC-A:", count_12_upca , '(%s)' % '{:.2%}'.format(count_12_upca / count))
print("Починенные EAN-13 из 12-значных:", count_12_fixed , '(%s)' % '{:.2%}'.format(count_12_fixed  / count))
print("Плохие UPC-A:", count_12_bad , '(%s)' % '{:.2%}'.format(count_12_bad / count))
print("EAN-13:", count_13_good , '(%s)' % '{:.2%}'.format(count_13_good / count))
print("Починенных EAN-13:", count_13_fixed , '(%s)' % '{:.2%}'.format(count_13_fixed / count))
print("Плохие EAN-13:", count_13_bad , '(%s)' % '{:.2%}'.format(count_13_bad / count))
print("Отсутствие кода:", count_empty, '(%s)' % '{:.2%}'.format(count_empty / count))
print("Начинающиеся на 2:", count_2, '(%s)' % '{:.2%}'.format(count_2 / count))
print("Начинающиеся на 000:", count_000, '(%s)' % '{:.2%}'.format(count_000 / count))
print("С неправильным описанием:", count_wrong_description, '(%s)' % '{:.2%}'.format(count_wrong_description / count))
print("С неправильной длиной:", count_bad_length, '(%s)' % '{:.2%}'.format(count_bad_length / count))

file_input_hand.close()
hand_result.close()
hand_8_ean8.close()
hand_8_upce.close()
hand_8_bad.close()
hand_12_fixed.close()
hand_12_upca.close()
hand_12_bad.close()
hand_13_good.close()
hand_13_fixed.close()
hand_13_bad.close()
hand_bad_length.close()
hand_wrong_description.close()
hand_2.close()
hand_000.close()
print('Все файлы закрыты, программа завершена')
print('Время выполнения программы:', datetime.now() - startTime)
