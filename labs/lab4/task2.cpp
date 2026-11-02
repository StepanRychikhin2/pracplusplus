#include <iostream>
#include <cctype>
#include <cstdio>
#include <iomanip>
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
    cout << "Лабораторна робота №4. Завдання 2." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Обчислити скінченний ланцюговий дріб:" << endl;
    cout << "1 + 1 / (3 + 1 / (5 + ... + 1 / (2*n + 1)))." << endl;
    cout << "Значення n ввести з клавіатури. n — ціле додатне число." << endl;
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

// Зчитуємо кількість знаменників дробу
int getNumber() {
    int n = 0;
    cout << "Введіть n: ";
    cin >> n;
    return n;
}

// Не приймаємо текст дробові та недодатні числа
bool checkNumber(int n) {
    bool valid = checkInput() && n > 0;
    return valid;
}

// Рахуємо дріб знизу вгору
double getFraction(int n) {
    double f = 0; // Уже обчислена внутрішня частина дробу

    for (int i = n; i >= 1; i--) {
        // Знаменники йдуть від 2*n+1 до 3
        f = 1.0 / (2.0 * i + 1 + f);
    }

    double result = 1 + f; // Одиниця перед усім дробом
    return result;
}

// Виводимо відповідь із десятьма знаками після крапки
void printResult(double result) {
    cout << fixed << setprecision(10);
    cout << "Значення дробу: " << result << endl;
}

// Повідомляємо про неправильне введення
void printError() {
    cout << "Помилка: n має бути цілим додатним числом у межах типу int." << endl;
}

// Запускаємо обчислення тільки для правильних даних
void runTask() {
    int n = getNumber();

    if (checkNumber(n)) {
        double result = getFraction(n);
        printResult(result);
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
