#include <iostream>
#include <cctype>
#include <cstdlib>
#include <ctime>
#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

int arr[100];
int n, choice, imin, imax;
bool ok = true;

// Українська мова в консолі
void Consol() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

void Info() {
    cout << "Лабораторна робота №6. Завдання 1." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Ввести масив або заповнити його випадковими числами." << endl;
    cout << "Поміняти місцями мінімальний і максимальний елементи." << endl;
    cout << "Вивести обидва масиви, мінімум, максимум та їх індекси." << endl;
    cout << "Індекси починаються з 0. При повторах беремо перші входження." << endl;
}

// Перевіряємо, чи введено число повністю
bool Chek() {
    bool good = !cin.fail();
    if (good && !cin.eof()) {
        good = isspace(cin.peek());
    }
    return good;
}

// Заповнюємо масив
void Make() {
    cout << "1 — введення з клавіатури" << endl;
    cout << "2 — випадкові числа від -50 до 50" << endl;
    cout << "Ваш вибір: ";
    cin >> choice;
    ok = Chek() && (choice == 1 || choice == 2);

    if (ok) {
        if (choice == 1) {
            cout << "Введіть " << n << " цілих чисел: ";
            for (int i = 0; i < n && ok; i++) {
                cin >> arr[i];
                ok = Chek();
            }
        } else {
            srand(time(0));
            for (int i = 0; i < n; i++) {
                arr[i] = rand() % 101 - 50;
            }
        }
    }
}

// Виводимо масив
void Print() {
    for (int i = 0; i < n; i++) {
        if (i > 0) {
            cout << ' ';
        }
        cout << arr[i];
    }
    cout << endl;
}

// Знаходимо індекси мінімуму та максимуму
void MinMax() {
    imin = 0;
    imax = 0;
    for (int i = 1; i < n; i++) {
        if (arr[i] < arr[imin]) {
            imin = i;
        }
        if (arr[i] > arr[imax]) {
            imax = i;
        }
    }
}

// Міняємо два елементи місцями
void Swap() {
    int temp = arr[imin];
    arr[imin] = arr[imax];
    arr[imax] = temp;
}

void Run() {
    cout << "Введіть кількість елементів (1–100): ";
    cin >> n;
    ok = Chek() && n >= 1 && n <= 100;
    if (ok) {
        Make();
    }

    if (ok) {
        cout << "Вхідний масив: ";
        Print();
        MinMax();
        cout << "Мінімальний елемент: " << arr[imin] << "; індекс: " << imin << endl;
        cout << "Максимальний елемент: " << arr[imax] << "; індекс: " << imax << endl;
        Swap();
        cout << "Вихідний масив: ";
        Print();
    } else {
        cout << "Помилка: n має бути від 1 до 100, вибір — 1 або 2, елементи — цілі числа в межах int." << endl;
    }
}

int main() {
    Consol();
    Info();
    Run();
}
