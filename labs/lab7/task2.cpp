#include <iostream>
#include <iomanip>
#include <cctype>
#include <cstdlib>
#include <ctime>
#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

int arr[6][6], temp[6][6];
long long adds[6][6], d;
long double back[6][6];
bool used[6];
int m, dim, choice, view;
bool ok = true;

void Consol() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

void Info() {
    cout << "Лабораторна робота №7. Завдання 2." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Знайти обернену матрицю через алгебраїчні доповнення." << endl;
    cout << "A^(-1) = (Aij)^T / det(A), Aij = (-1)^(i+j) * Mij." << endl;
}

// Перевіряємо введення числа
bool Chek() {
    bool good = !cin.fail();
    if (good && !cin.eof()) {
        good = isspace(cin.peek());
    }
    return good;
}

void Make() {
    cout << "1 — введення з клавіатури" << endl;
    cout << "2 — випадкові числа від -10 до -1 та від 1 до 10" << endl;
    cout << "Ваш вибір: ";
    cin >> choice;
    ok = Chek() && (choice == 1 || choice == 2);
    if (ok) {
        if (choice == 1) {
            cout << "Введіть матрицю по рядках, цілі числа від -100 до 100:" << endl;
            for (int i = 0; i < m && ok; i++) {
                for (int j = 0; j < m && ok; j++) {
                    cin >> arr[i][j];
                    ok = Chek() && arr[i][j] >= -100 && arr[i][j] <= 100;
                }
            }
        } else {
            srand(time(0));
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < m; j++) {
                    arr[i][j] = rand() % 10 + 1;
                    if (rand() % 2 == 0) {
                        arr[i][j] = -arr[i][j];
                    }
                }
            }
        }
    }
}

void Print() {
    cout << "Вхідна матриця:" << endl;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            cout << setw(8) << arr[i][j];
        }
        cout << endl;
    }
}

// Розклад визначника temp за рядком; used позначає викреслені стовпці
long long Det(int row) {
    long long res = 0;
    int sign = 1;
    if (row == dim) {
        res = 1;
    } else {
        for (int j = 0; j < dim; j++) {
            if (!used[j]) {
                used[j] = true;
                res += sign * temp[row][j] * Det(row + 1);
                used[j] = false;
                sign = -sign;
            }
        }
    }
    return res;
}

// Копіюємо матрицю без рядка r і стовпця c
void Minor(int r, int c) {
    int x = 0;
    for (int i = 0; i < m; i++) {
        if (i != r) {
            int y = 0;
            for (int j = 0; j < m; j++) {
                if (j != c) {
                    temp[x][y] = arr[i][j];
                    y++;
                }
            }
            x++;
        }
    }
}

// Обчислюємо доповнення та одразу транспонуємо їх
void Invers() {
    dim = m - 1;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            Minor(i, j);
            long long minor = Det(0);
            adds[i][j] = minor;
            if ((i + j) % 2 != 0) {
                adds[i][j] = -adds[i][j];
            }
            back[j][i] = (long double)adds[i][j] / d;
            if (view == 2) {
                cout << "M[" << i + 1 << "][" << j + 1 << "] = " << minor;
                cout << "; A[" << i + 1 << "][" << j + 1 << "] = " << adds[i][j] << endl;
            }
        }
    }
}

void PrintBack() {
    cout << "Обернена матриця:" << endl;
    cout << setprecision(10);
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            cout << setw(18) << back[i][j];
        }
        cout << endl;
    }
}

void Work() {
    Print();
    dim = m;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            temp[i][j] = arr[i][j];
        }
    }
    d = Det(0);
    cout << "Визначник: " << d << endl;
    if (d != 0) {
        Invers();
        PrintBack();
    } else {
        cout << "Оберненої матриці не існує, оскільки визначник дорівнює 0." << endl;
    }
}

void Run() {
    cout << "Введіть m (3–6): ";
    cin >> m;
    ok = Chek() && m >= 3 && m <= 6;
    if (ok) {
        Make();
    }
    if (ok) {
        cout << "1 — тільки кінцевий результат" << endl;
        cout << "2 — результат і проміжні мінори та алгебраїчні доповнення" << endl;
        cout << "Ваш вибір: ";
        cin >> view;
        ok = Chek() && (view == 1 || view == 2);
    }
    if (ok) {
        Work();
    } else {
        cout << "Помилка введення. m: 3–6, меню: 1 або 2, елементи: цілі числа від -100 до 100." << endl;
    }
}

int main() {
    Consol();
    Info();
    Run();
}
