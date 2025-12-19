#include <fstream>
#include <iostream>
#include <random>
#include <string>


using namespace std;

//Генерирует псевдослучайную двоичную последовательную из 128 бит
std::string generator() {
    std::unsigned seed = static_cast<unsigned>(time(nullptr));
    std::mt19937 gen(seed);
    std::uniform_int_distribution<size_t> number(0, 1);

    std::string seq;
    for (size_t i = 0; i < 128; ++i) {
        seq += std::to_string(number(gen));
    }
    return seq;
}

//Запись в файл последовательность
//dir - путь к файлу для сохранения
//seq - последовательность для сохранения
void write_to_file(std::string dir, std::string seq) {
    try {
        std::ofstream file;
        file.open(dir);
        if (!file.is_open()) {
            throw std::runtime_error("Failed to open file " + dir);
        }
        file << seq << std::endl;
        file.close();
    }
    catch (const std::exception& e) {
        std::cerr << "Unknown error " << e.what() << std::endl;
        throw;
    }
}

int main() {
    std::string seq = generator();
    write_to_file("cpp_sequence.txt", seq);
    std::cout << seq;
}