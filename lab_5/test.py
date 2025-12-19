import math
import scipy.special as sp
from logging_config import get_module_logger

logger = get_module_logger(__name__)


def frequency_test(sequence: str) -> float:
    """
    Частотный побитовый тест для заданной последовательности
    :param sequence: побитовая последовательность для теста
    :return: вероятность того, что значение близко к случайному
    """
    logger.debug(f"Начало частотного теста, длина: {len(sequence)}")

    if not sequence:
        logger.error("Передана пустая последовательность")
        raise ValueError("Sequence is empty")

    try:
        sum_val = 0
        for elem in sequence:
            if elem == '1':
                sum_val += 1
            elif elem == '0':
                sum_val -= 1
            else:
                logger.warning(f"Недопустимый символ: '{elem}'")

        sqrt_len = math.sqrt(len(sequence))
        stat = sum_val / sqrt_len

        logger.debug(f"Статистика S = {sum_val}, S/√n = {stat:.4f}")

        p_value = math.erfc(abs(stat) / math.sqrt(2))
        logger.info(f"Частотный тест завершен, p-value = {p_value:.6f}")

        return p_value

    except Exception as e:
        logger.exception(f"Ошибка в частотном тесте: {e}")
        raise


def identical_test(sequence: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    :param sequence: побитовая последовательность для теста
    :return: вероятность того, что значение близко к случайному
    """
    logger.debug(f"Начало теста на идентичные биты, длина: {len(sequence)}")

    if not sequence:
        logger.error(
            "Передана пустая последовательность для теста на идентичные биты"
        )
        raise ValueError("Sequence is empty")

    try:
        length = len(sequence)
        summ = 0
        for elem in sequence:
            if elem == "1":
                summ += 1

        zeta = summ / length
        logger.debug(f"Доля единиц в последовательности: zeta = {zeta:.4f}")

        if abs(zeta - 0.5) >= 2 / math.sqrt(length):
            logger.warning(
                f"Тест на идентичные биты прерван: |zeta - 0.5| = "
                f"{abs(zeta - 0.5):.4f} >= {2 / math.sqrt(length):.4f}"
            )
            return 0.0

        v_n = 0
        for ind in range(0, length - 1):
            if sequence[ind] != sequence[ind + 1]:
                v_n += 1

        logger.debug(f"Количество переходов V_n = {v_n}")

        numerator = abs(v_n - 2 * length * zeta * (1 - zeta))
        denominator = 2 * math.sqrt(2 * length) * zeta * (1 - zeta)

        p_value = math.erfc(numerator / denominator)
        logger.info(
            f"Тест на идентичные биты завершен, p-value = {p_value:.6f}"
        )

        return p_value

    except Exception as e:
        logger.exception(f"Ошибка в тесте на идентичные биты: {e}")
        raise


def long_sequence_test_in_block(sequence: str, p: list) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    :param sequence: побитовая последовательность для теста
    :param p: список постоянных теоретических вероятностей
    :return: вероятность того, что значение близко к случайному
    """
    logger.debug(
        f"Начало теста на длинную последовательность, длина: {len(sequence)}"
    )

    if not sequence:
        logger.error(
            "Передана пустая последовательность "
            "для теста на длинную последовательность"
        )
        raise ValueError("Sequence is empty")

    try:
        length = len(sequence)
        if length != 128:
            logger.error(f"Тест требует 128 бит, получено {length} бит")
            raise ValueError("The sequence must be 128 bits long.")

        blocks = []
        v = [0, 0, 0, 0]

        for ind in range(0, length, 8):
            block = sequence[ind: ind + 8]
            blocks.append(block)

        logger.debug(f"Создано {len(blocks)} блоков по 8 бит")

        for block_idx, block in enumerate(blocks):
            max_run = 0
            cur_len = 0

            for j in block:
                if j == "1":
                    cur_len += 1
                    max_run = max(max_run, cur_len)
                else:
                    cur_len = 0

            if max_run <= 1:
                v[0] += 1
            elif max_run == 2:
                v[1] += 1
            elif max_run == 3:
                v[2] += 1
            elif max_run >= 4:
                v[3] += 1

            logger.debug(
                f"Блок {block_idx}: "
                f"максимальная последовательность = {max_run}"
            )

        logger.debug(f"Распределение длин последовательностей: {v}")

        chi2 = 0.0
        for i in range(4):
            chi2 += ((v[i] - 16 * p[i]) ** 2) / (16 * p[i])

        logger.debug(f"Вычисленное значение хи-квадрат: {chi2:.4f}")

        try:
            p_value = sp.gammainc(1.5, chi2 / 2)
        except ImportError:
            logger.warning(
                "scipy не установлен, использую заглушку для p-value"
            )
            p_value = 0.5

        logger.info(
            f"Тест на длинную последовательность завершен, "
            f"p-value = {p_value:.6f}"
        )

        return p_value

    except Exception as e:
        logger.exception(f"Ошибка в теста на длинную последовательность: {e}")
        raise
