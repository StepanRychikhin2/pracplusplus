#include <iostream>
#include <cctype>
#include <cstdio>
#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

// Вмикаємо українські літери в консолі Windows
void setupConsole() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

// Виводимо умову та автора
void printTaskInfo() {
    cout << "========================Завдання========================" << endl;
    cout << "Лабораторна робота №5. Завдання 2." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Ввести натуральне число n." << endl;
    cout << "Вивести його цифри у зворотному порядку через пробіл." << endl;
    cout << "Використати тільки рекурсію та цілочисельну арифметику." << endl;
    cout << "Не використовувати цикли, масиви та перетворення числа на рядок." << endl;
    cout << "Контрольний приклад: для 123 отримати 3 2 1." << endl;
    cout << "========================================================" << endl;
}

// Перевіряємо введення і символ після останнього числа
bool checkInput() {
    bool valid = bool(cin);

    if (valid) {
        int next = cin.peek();
        // Після числа має бути пробіл новий рядок або кінець введення
        valid = next == EOF || isspace(next);
    }

    return valid;
}

// Зчитуємо число як ціле а не як текст
long long getNumber() {
    long long n = 0;
    cout << "Введіть n: ";
    cin >> n;
    return n;
}

// Перевіряємо введення без циклів масивів і рядків
bool checkNumber(long long n) {
    bool valid = checkInput() && n > 0;
    return valid;
}

// Виводимо цифри справа наліво через рекурсію
void printDigits(long long n) {
    // Остача від ділення на 10 — остання цифра
    cout << n % 10;

    if (n >= 10) {
        cout << ' ';
        // Ділення на 10 прибирає останню цифру
        printDigits(n / 10);
    }
    // Для однієї цифри наступний виклик уже не потрібний
}

// Виводимо пояснення та всі цифри числа
void printResult(long long n) {
    cout << "Цифри у зворотному порядку: ";
    printDigits(n);
    cout << endl;
}

// Повідомляємо про неправильне введення
void printError() {
    cout << "Помилка: введіть ціле додатне число в межах типу long long." << endl;
}

// Обробляємо число тільки після перевірки
void runTask() {
    long long n = getNumber();

    if (checkNumber(n)) {
        printResult(n);
    } else {
        printError();
    }
}

// У main залишаємо тільки виклики функцій
int main() {
    setupConsole();
    printTaskInfo();
    runTask();
}
