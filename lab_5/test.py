import math
import scipy.special as sp


def frequency_test(sequence: str) -> float:
    """
    Частотный побитовый тест для заданной последовательности
    :param sequence: побитовая последовательность для теста
    :return: вероятность того, что значение близко к случайному
    """
    if not sequence:
        raise ValueError("Sequence is empty")

    sum = 0
    for elem in sequence:
        if elem == '1':
            sum += 1
        elif elem == '0':
            sum -= 1
    sqrt_len = math.sqrt(len(sequence))
    stat = sum/sqrt_len
    p_value = math.erfc(stat/math.sqrt(2))
    return p_value


def identical_test(sequence: str) -> float:
    """
    Tест на одинаковые подряд идущие биты
    :param sequence: побитовая последовательность для теста
    :return: вероятность того, что значение близко к случайному
    """

    if not sequence:
        raise ValueError("Sequence is empty")

    length = len(sequence)
    summ = 0
    for elem in sequence:
        if elem == "1":
            summ += 1
    zeta = summ/length
    if abs(zeta - 0.5) >= 2/math.sqrt(length):
        return 0
    v_n = 0
    for ind in range(0, length - 1):
        if sequence[ind] != sequence[ind + 1]:
            v_n += 1
    p_value = math.erfc(abs(v_n - 2 * length * zeta * (1 - zeta)) / (2 * math.sqrt(2 * length) * zeta * (1 - zeta)))
    return p_value


def long_sequence_test_in_block(sequence: str, p: list) -> float:
    """
    Tест на самую длинную последовательность единиц в блоке
    :param sequence: побитовая последовательность для теста
    :param p: список постоянных теоретических вероятностей
    :return: вероятность того, что значение близко к случайному
    """
    if not sequence:
        raise ValueError("Sequence is empty")

    length = len(sequence)
    if length != 128:
        raise ValueError("The sequence must be 128 bits long.")

    blocks = []
    v = [0, 0, 0, 0]
    for ind in range(0, length, 8):
        block = sequence[ind: ind + 8]
        blocks.append(block)
    for block in blocks:
        max_run = 0
        cur_len = 0
        for j in block:
            if j == "1":
                cur_len += 1
                max_run = max(max_run, cur_len)
            else:
                cur_len = 0
        match max_run:
            case 0 | 1:
                v[0] += 1
            case 2:
                v[1] += 1
            case 3:
                v[2] += 1
            case _ if max_run >= 4:
                v[3] += 1
    chi2 = sum(((v[i] - 16 * p[i]) ** 2) / (16 * p[i]) for i in range(len(v)))
    p_value = sp.gammainc(1.5, chi2 / 2)
    return p_value
