import heapq
import math
from collections import Counter


def build_huffman(freq):
    heap = []
    number = 0

    for letter in freq:
        if freq[letter] > 0:
            heapq.heappush(heap, (freq[letter], number, letter))
            number += 1

    if len(heap) == 0:
        raise ValueError('Нет символов для кодирования')

    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        new_tree = (first[2], second[2])
        new_count = first[0] + second[0]
        heapq.heappush(heap, (new_count, number, new_tree))
        number += 1

    tree = heap[0][2]
    codes = {}

    def make_codes(node, code):
        if isinstance(node, str):
            if code == '':
                code = '0'
            codes[node] = code
        else:
            make_codes(node[0], code + '0')
            make_codes(node[1], code + '1')

    make_codes(tree, '')
    return tree, codes


def encode(text, codes):
    result = ''
    for letter in text:
        result += codes[letter]
    return result


def decode(bits, tree):
    if isinstance(tree, str):
        for bit in bits:
            if bit != '0':
                raise ValueError('Неверный код')
        return tree * len(bits)

    result = ''
    node = tree

    for bit in bits:
        if bit == '0':
            node = node[0]
        elif bit == '1':
            node = node[1]
        else:
            raise ValueError('Допустимы только 0 и 1')

        if isinstance(node, str):
            result += node
            node = tree

    if node != tree:
        raise ValueError('Последний код неполный')

    return result


def statistics(freq, codes):
    total = sum(freq.values())
    entropy = 0
    average = 0

    for letter in freq:
        p = freq[letter] / total
        entropy -= p * math.log2(p)
        average += p * len(codes[letter])

    efficiency = entropy / average * 100
    redundancy = 100 - efficiency
    return entropy, average, efficiency, redundancy


if __name__ == '__main__':
    text = 'ABCADE'
    freq = dict(Counter(text))

    tree, codes = build_huffman(freq)
    bits = encode(text, codes)
    result = decode(bits, tree)

    print('ЗАДАЧА 9. КОД ХАФФМАНА')
    print('Текст:', text)
    print('Частоты:', freq)
    print('Дерево:', tree)
    print('\nБуква | Частота | Код')
    for letter in freq:
        print(letter, '|', freq[letter], '|', codes[letter])

    h, length, efficiency, redundancy = statistics(freq, codes)
    print('\nЭнтропия:', round(h, 4))
    print('Средняя длина:', round(length, 4))
    print('Эффективность:', round(efficiency, 2), '%')
    print('Избыточность:', round(redundancy, 2), '%')
    print('Закодировано:', bits)
    print('Длина:', len(bits), 'бит')
    print('Декодировано:', result)
    print('Проверка:', result == text)

    one_tree, one_codes = build_huffman({'A': 5})
    one_bits = encode('AAAAA', one_codes)
    print('Одна буква:', one_codes, one_bits)
    assert decode(one_bits, one_tree) == 'AAAAA'
    assert result == text
    print('Тесты пройдены')
