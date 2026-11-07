#include <iostream>
#include <cctype>
#include <cstdlib>
#include <ctime>
#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

int arr[100];
int n, choice, view, key;
int countSort, swaps, countSearch, pos;
bool ok = true;

void Consol() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

void Info() {
    cout << "Лабораторна робота №6. Завдання 2." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Ввести масив або заповнити його випадковими числами." << endl;
    cout << "Виконати бульбашкове сортування та лінійний пошук." << endl;
    cout << "Порахувати порівняння й обміни. Передбачити показ проходів." << endl;
    cout << "Індекси починаються з 0. Шукаємо перше входження." << endl;
}

bool Chek() {
    bool good = !cin.fail();
    if (good && !cin.eof()) {
        good = isspace(cin.peek());
    }
    return good;
}

// Створюємо масив обраним способом
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

void Print() {
    for (int i = 0; i < n; i++) {
        if (i > 0) {

            cout << ' ';

        }
        cout << arr[i];
    }
    cout << endl;
}

// Бульбашкове сортування з підрахунком операцій
void BubleSort() {
    countSort = 0;
    swaps = 0;
    bool swaped = true;
    for (int step = 0; step < n - 1 && swaped; step++) {
        swaped = false;
        for (int i = 0; i < n - 1 - step; i++) {
            countSort++;
            if (arr[i] > arr[i + 1]) {
                int temp = arr[i];

                arr[i] = arr[i + 1];

                arr[i + 1] = temp;


                swaps++;

                swaped = true;

            }
        }
        if (view == 2) {
            cout << "Прохід " << step + 1 << ": ";
            Print();
        }
    }
}

// Шукаємо число зліва направо
void Find() {
    pos = -1;
    countSearch = 0;

    for (int i = 0; i < n && pos == -1; i++) {
        countSearch++;
        if (arr[i] == key) {
            pos = i;
        }
    }
}


void Search() {
    cout << "Введіть ціле число для пошуку: ";
    cin >> key;
    ok = Chek();
    if (ok) {
        Find();
        if (pos == -1) {
            cout << "Число " << key << " не знайдено." << endl;
        } else {

            cout << "Число " << key << " знайдено. Індекс у відсортованому масиві: " << pos << endl;
        }
        cout << "Порівнянь під час пошуку: " << countSearch << endl;
    }
}

void Run() {
    cout << "Введіть кількість елементів (1–100): ";
    cin >> n;

    ok = Chek() && n >= 1 && n <= 100;
    if (ok) {
        Make();
    }
    if (ok) {
        cout << "1 — тільки відсортований масив" << endl;
        cout << "2 — також проміжні проходи" << endl;

        cout << "Ваш вибір: ";

        cin >> view;
        ok = Chek() && (view == 1 || view == 2);
    }
    if (ok) {
        if (view == 2) {
            cout << "Вхідний масив: ";
            Print();
        }
        
        BubleSort();
        cout << "Відсортований масив: ";
        Print();
        cout << "Порівнянь під час сортування: " << countSort << endl;
        cout << "Обмінів під час сортування: " << swaps << endl;
        Search();
    }
    if (!ok) {
        cout << "Помилка: n має бути від 1 до 100, пункт меню — 1 або 2. Вводьте цілі числа в межах int." << endl;
    }
}

int main() {
    Consol();
    Info();
    Run();
}
