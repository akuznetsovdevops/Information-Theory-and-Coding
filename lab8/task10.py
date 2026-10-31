from collections import Counter
from task9 import build_huffman, encode, decode, statistics


text = (
    'Информация хранится в памяти компьютера в виде последовательности битов. '
    'Для передачи данных используются разные способы кодирования. '
    'Один из способов уменьшить размер сообщения называется кодом Хаффмана. '
    'Частые буквы получают короткие коды, а редкие буквы более длинные. '
    'Так можно уменьшить размер текста без потери информации. '
    'Для восстановления текста нужно сохранить таблицу частот или кодов. '
    'При маленьком объёме сообщения служебная таблица может занять слишком много места. '
    'Поэтому важно сравнивать размер исходного файла и полный размер сжатых данных.'
)

assert len(text) >= 300

freq = dict(Counter(text))
tree, codes = build_huffman(freq)
bits = encode(text, codes)

h, length, efficiency, redundancy = statistics(freq, codes)

padding = (8 - len(bits) % 8) % 8
bits_with_padding = bits + '0' * padding

with open('compressed.bin', 'wb') as file:
    for i in range(0, len(bits_with_padding), 8):
        group = bits_with_padding[i:i + 8]
        file.write(bytes([int(group, 2)]))

with open('codes.txt', 'w', encoding='utf-8') as file:
    file.write(str(padding) + '\n')
    for letter in freq:
        file.write(str(ord(letter)) + ' ' + str(freq[letter]) + '\n')

with open('codes.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

saved_padding = int(lines[0])
saved_freq = {}
for line in lines[1:]:
    number, count = line.split()
    saved_freq[chr(int(number))] = int(count)

saved_tree, saved_codes = build_huffman(saved_freq)

with open('compressed.bin', 'rb') as file:
    packed = file.read()

restored_bits = ''
for byte in packed:
    restored_bits += format(byte, '08b')
if saved_padding > 0:
    restored_bits = restored_bits[:-saved_padding]

restored_text = decode(restored_bits, saved_tree)
assert restored_text == text

original_size = len(text.encode('utf-8'))
packed_size = len(packed)

with open('codes.txt', 'rb') as file:
    table_size = len(file.read())

full_size = packed_size + table_size
saving = (1 - full_size / original_size) * 100

print('ЗАДАЧА 10. ИССЛЕДОВАНИЕ ТЕКСТА')
print('Всего символов:', len(text))
print('Разных символов:', len(freq))
print('Учитываются пробелы, регистр и знаки препинания')
print('Дерево Хаффмана:', tree)

print('\nСимвол | Частота | Код')
for letter in freq:
    print(repr(letter), '|', freq[letter], '|', codes[letter])

print('\nЭнтропия:', round(h, 4), 'бит/символ')
print('Средняя длина:', round(length, 4), 'бит/символ')
print('Эффективность:', round(efficiency, 2), '%')
print('Избыточность:', round(redundancy, 2), '%')
print('Исходный UTF-8:', original_size, 'байт')
print('Код Хаффмана:', len(bits), 'бит')
print('Упакованный поток:', packed_size, 'байт')
print('Дополнительные биты до целого байта:', padding)
print('Таблица частот:', table_size, 'байт')
print('Полный размер:', full_size, 'байт')
print('Экономия:', round(saving, 2), '%')
print('Проверка восстановления:', restored_text == text)

if saving > 0:
    print('Вывод: Этот текст сжался даже с учетом таблицы.')
else:
    print('Вывод: Таблица занимает слишком много места для этого текста.')
