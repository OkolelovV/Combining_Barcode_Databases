file_input_hand = open('all_8.txt', 'r', encoding = 'utf-8')
hand_ean8 = open('result_8_ean8.txt', 'w', encoding = 'utf-8')
hand_upce = open('result_8_upce.txt', 'w', encoding = 'utf-8')
hand_bad = open('result_8_bad.txt', 'w', encoding = 'utf-8')
print('Файлы открыты')

def check_digit_upca(code):
    even = int(code[9]) + int(code[7]) + int(code[5]) + int(code[3]) + int(code[1])
    odd = int(code[10]) + int(code[8]) + int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
    check_digit = 3 * odd + even
    check_digit = (10 - check_digit % 10) % 10
    return str(check_digit)

count_ean8 = 0
count_upce = 0
count_bad = 0

def upce_to_upca(code):
    if code[6] == '0' or code[6] == '1' or code[6] == '2':
        upca_11 = code[0:3] + code[6] + '0000' + code[3:6]
        return upca_11 + check_digit_upca(upca_11)
    elif code[6] == '3':
        upca_11 = code[0:4] + '00000' + code[4:6]
        return upca_11 + check_digit_upca(upca_11)
    elif code[6] == '4':
        upca_11 = code[0:5] + '00000' + code[5]
        return upca_11 + check_digit_upca(upca_11)
    else:
        upca_11 = code[0:6] + '0000' + code[6]
        return upca_11 + check_digit_upca(upca_11)

for count, line in enumerate(file_input_hand, 1):
    words = line.split(':', 1)
    code = words[0]
    description = words[1].strip() + '\n'
    even = int(code[5]) + int(code[3]) + int(code[1])
    odd = int(code[6]) + int(code[4]) + int(code[2]) + int(code[0])
    check_digit = 3 * odd + even
    check_digit = (10 - check_digit % 10) % 10
    if check_digit == int(code[7]):
        hand_ean8.write(code + ':' + description)
        count_ean8 += 1
        continue
    elif code[0] in ['0', '1']:
        if code[6] in ['0', '1', '2']:
            upca_11 = code[0:3] + code[6] + '0000' + code[3:6]
        elif code[6] == '3':
            upca_11 = code[0:4] + '00000' + code[4:6]
        elif code[6] == '4':
            upca_11 = code[0:5] + '00000' + code[5]
        else:
            upca_11 = code[0:6] + '0000' + code[6]
        if check_digit_upca(upca_11) == code[7] :
            hand_upce.write(code + ':' + description)
            count_upce += 1
            continue
    hand_bad.write(code + ':' + description)
    count_bad += 1

#print(upce_to_upca('06120014'))
#print(upce_to_upca('01101433'))
#print(upce_to_upca('06152040'))
#print(upce_to_upca('02050062'))

sum_check = count_ean8 + count_upce + count_bad
print('Проверка суммы:', sum_check == count)
print('Total:', count)

print("Число EAN-8:", count_ean8 , '{:.2%}'.format(count_ean8  / count))
print("Число UPC-E:", count_upce , '{:.2%}'.format(count_upce  / count))
print("Число плохих 8:", count_bad , '{:.2%}'.format(count_bad  / count))

file_input_hand.close()
hand_ean8.close()
hand_upce.close()
hand_bad.close()
print('Все файлы закрыты, программа завершена')
