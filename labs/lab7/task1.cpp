#include <iostream>
#include <iomanip>
#include <cctype>
#include <cstdlib>
#include <ctime>
#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

long long arr[10][10];
long long sum, big;
int n, choice;
bool ok = true;

void Consol() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

void Info() {
    cout << "Лабораторна робота №7. Завдання 1." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Знайти суму елементів на діагоналі та над нею," << endl;
    cout << "які більші за всі елементи під головною діагоналлю." << endl;
    cout << "Записати суму в новий рядок і стовпець." << endl;
}

// Перевіряємо введення числа
bool Chek() {
    bool good = !cin.fail();
    if (good && !cin.eof()) {
        good = isspace(cin.peek());
    }
    return good;
}

// Створюємо матрицю
void Make() {
    cout << "1 — введення з клавіатури" << endl;
    cout << "2 — випадкові числа від -10 до 10" << endl;
    cout << "Ваш вибір: ";
    cin >> choice;
    ok = Chek() && (choice == 1 || choice == 2);
    if (ok) {
        if (choice == 1) {
            cout << "Введіть матрицю по рядках, цілі числа від -1000000 до 1000000:" << endl;
            for (int i = 0; i < n && ok; i++) {
                for (int j = 0; j < n && ok; j++) {
                    cin >> arr[i][j];
                    ok = Chek() && arr[i][j] >= -1000000 && arr[i][j] <= 1000000;
                }
            }
        } else {
            srand(time(0));
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    arr[i][j] = rand() % 21 - 10;
                }
            }
        }
    }
}

// Виводимо size рядків та стовпців
void Print(int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            cout << setw(13) << arr[i][j];
        }
        cout << endl;
    }
}

// Шукаємо максимум під діагоналлю та потрібну суму
void FindSum() {
    big = arr[1][0];
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (arr[i][j] > big) {
                big = arr[i][j];
            }
        }
    }
    sum = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            if (arr[i][j] > big) {
                sum += arr[i][j];
            }
        }
    }
}

// Додаємо рядок і стовпець, якщо для них є місце
void Add() {
    if (n < 10) {
        for (int i = 0; i <= n; i++) {
            arr[n][i] = sum;
            arr[i][n] = sum;
        }
        cout << "Модифікована матриця:" << endl;
        Print(n + 1);
    } else {
        cout << "Вихід за межі матриці: у масиві 10x10 немає місця для 11-го рядка і стовпця." << endl;
    }
}

void Run() {
    cout << "Введіть n (3–10; для розширення потрібно n <= 9): ";
    cin >> n;
    ok = Chek() && n >= 3 && n <= 10;
    if (ok) {
        Make();
    }
    if (ok) {
        cout << "Вхідна матриця:" << endl;
        Print(n);
        FindSum();
        cout << "Максимум під діагоналлю: " << big << endl;
        cout << "Сума: " << sum << endl;
        Add();
    } else {
        cout << "Помилка введення. n: 3–10, меню: 1 або 2, елементи: цілі числа від -1000000 до 1000000." << endl;
    }
}

int main() {
    Consol();
    Info();
    Run();
}
