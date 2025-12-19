from logging_config import setup_logging, get_module_logger
from test import frequency_test, identical_test
from work_file import read_txt, write_json


def main():
    setup_logging()

    logger = get_module_logger(__name__)

    logger.info("Запуск приложения для анализа статистических тестов")

    try:
        logger.info("Чтение данных из файла...")
        sequence = read_txt('cpp_sequence.txt')

        if not sequence:
            logger.error("Не удалось прочитать последовательность")
            return

        logger.info(f"Прочитана последовательность длиной {len(sequence)} бит")

        logger.info("Запуск частотного теста...")
        p1 = frequency_test(sequence)
        logger.info(f"Результат частотного теста: p-value = {p1:.6f}")

        logger.info("Запуск теста на идентичные биты...")
        p2 = identical_test(sequence)
        logger.info(f"Результат теста на идентичные биты: p-value = {p2:.6f}")

        results = {
            'frequency_test': p1,
            'identical_test': p2,
            'sequence_length': len(sequence)
        }

        write_json(results, 'results.json')
        logger.info("Результаты успешно сохранены в results.json")

        threshold = 0.01
        if p1 > threshold and p2 > threshold:
            logger.info("✓ Оба теста пройдены - последовательность случайна")
        else:
            logger.warning("⚠ Некоторые тесты не пройдены")

    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
    except Exception as e:
        logger.exception(f"Критическая ошибка: {e}")
    finally:
        logger.info("Завершение работы приложения")


if __name__ == "__main__":
    main()
