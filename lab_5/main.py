from work_file import *

from test import frequency_test, identical_test, long_sequence_test_in_block


def main():
    settings = read_json("settings.json")
    cpp_seq = read_txt(settings["CPP"])
    java_seq = read_txt(settings["JAVA"])
    results = {
        "cpp": {
            "frequency_bit_test": frequency_test(cpp_seq),
            "identical_consecutive_bit_test": identical_test(cpp_seq),
            "longest_sequence_in_block": long_sequence_test_in_block(cpp_seq, settings["P"])
        },
        "java": {
            "frequency_bit_test": frequency_test(java_seq),
            "identical_consecutive_bit_test": identical_test(java_seq),
            "longest_sequence_in_block": long_sequence_test_in_block(java_seq, settings["P"])
        }
    }

    write_json(results, settings["STATS"])


if __name__ == "__main__":
    main()