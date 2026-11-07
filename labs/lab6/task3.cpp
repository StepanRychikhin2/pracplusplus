#include <iostream>
#include <iomanip>
#include <cctype>
#include <cstdlib>
#include <ctime>
#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

long double x[3], a[3], b[3], c[3];
long double d, d1, d2, d3, k1, k2, k3;
int choice;
bool ok = true;

void Consol() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

void Info() {
    cout << "Лабораторна робота №6. Завдання 3." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Ввести X. Координати a, b, c ввести або згенерувати." << endl;
    cout << "Знайти розкладання X = alpha*a + beta*b + gamma*c." << endl;
    cout << "Координати від -1000000 до 1000000. Дробові числа — через крапку." << endl;
}

bool Chek() {
    bool good = !cin.fail();
    if (good && !cin.eof()) {
        good = isspace(cin.peek());
    }
    return good;
}

// Вводимо одну координату
long double ReadNum() {
    long double num = 0;
    cin >> num;
    ok = Chek() && num >= -1000000 && num <= 1000000;
    return num;
}

void ReadX() {
    cout << "Введіть три координати X: ";
    for (int i = 0; i < 3 && ok; i++) {
        x[i] = ReadNum();
    }
}

// Створюємо три вектори
void MakeVec() {
    cout << "1 — ввести a, b, c з клавіатури" << endl;
    cout << "2 — випадкові координати від -10 до 10" << endl;
    cout << "Ваш вибір: ";
    cin >> choice;
    ok = Chek() && (choice == 1 || choice == 2);
    if (ok) {
        if (choice == 1) {
            cout << "Введіть три координати a: ";
            for (int i = 0; i < 3 && ok; i++) {
                a[i] = ReadNum();
            }
            if (ok) {
                cout << "Введіть три координати b: ";
                for (int i = 0; i < 3 && ok; i++) {
                    b[i] = ReadNum();
                }
            }
            if (ok) {
                cout << "Введіть три координати c: ";
                for (int i = 0; i < 3 && ok; i++) {
                    c[i] = ReadNum();
                }
            }
        } else {
            srand(time(0));
            for (int i = 0; i < 3; i++) {
                a[i] = rand() % 21 - 10;
                b[i] = rand() % 21 - 10;
                c[i] = rand() % 21 - 10;
            }
        }
    }
}

void PrintVec(long double v1, long double v2, long double v3) {
    cout << '(' << v1 << "; " << v2 << "; " << v3 << ')';
}

long double Abs(long double num) {
    if (num < 0) {
        num = -num;
    }
    return num;
}

// column = 0: звичайний визначник; 1, 2, 3: замінюємо цей стовпець на X
long double Det(int column) {
    long double aa[3], bb[3], cc[3];
    for (int i = 0; i < 3; i++) {
        aa[i] = a[i];
        bb[i] = b[i];
        cc[i] = c[i];
        if (column == 1) aa[i] = x[i];
        if (column == 2) bb[i] = x[i];
        if (column == 3) cc[i] = x[i];
    }
    long double res = aa[0] * (bb[1] * cc[2] - bb[2] * cc[1])
                    - bb[0] * (aa[1] * cc[2] - aa[2] * cc[1])
                    + cc[0] * (aa[1] * bb[2] - aa[2] * bb[1]);
    return res;
}

// НСД для скорочення дробу; q — додатний знаменник
long long Gcd(long long p, long long q) {
    do {
        long long temp = p % q;
        p = q;
        q = temp;
    } while (q != 0);
    return p;
}

// Виводимо коефіцієнт дробом або десятковим числом
void PrintNum(long double up, long double down) {
    if (down < 0) {
        up = -up;
        down = -down;
    }
    long long p = (long long)up;
    long long q = (long long)down;
    if (up == p && down == q) {
        long long positive = p;
        if (positive < 0) positive = -positive;
        long long common = Gcd(positive, q);
        p = p / common;
        q = q / common;
        cout << p;
        if (q != 1) cout << '/' << q;
    } else {
        cout << up / down;
    }
}

// Виводимо доданок зі знаком
void PrintPart(long double up, char name, bool first) {
    if (first) {
        if (up / d < 0) cout << '-';
    } else {
        if (up / d < 0) cout << " - ";
        else cout << " + ";
    }
    PrintNum(Abs(up), Abs(d));
    cout << '*' << name;
}

// Перевіряємо відповідь підстановкою
void ChekRes() {
    long double back[3];
    long double err = 0;
    for (int i = 0; i < 3; i++) {
        back[i] = k1 * a[i] + k2 * b[i] + k3 * c[i];
        if (Abs(back[i] - x[i]) > err) {
            err = Abs(back[i] - x[i]);
        }
    }
    cout << "Перевірка: alpha*a + beta*b + gamma*c = ";
    PrintVec(back[0], back[1], back[2]);
    cout << "\nМаксимальна абсолютна похибка координат: " << err << endl;
}

void PrintRes() {
    cout << "Da = " << d1 << "; Db = " << d2 << "; Dc = " << d3 << endl;
    cout << "alpha = "; PrintNum(d1, d);
    cout << "; beta = "; PrintNum(d2, d);
    cout << "; gamma = "; PrintNum(d3, d);
    cout << "\nРозкладання: X = ";
    PrintPart(d1, 'a', true);
    PrintPart(d2, 'b', false);
    PrintPart(d3, 'c', false);
    cout << endl;
}

void Work() {
    cout << setprecision(12);
    cout << "\nX = "; PrintVec(x[0], x[1], x[2]);
    cout << "\na = "; PrintVec(a[0], a[1], a[2]);
    cout << "\nb = "; PrintVec(b[0], b[1], b[2]);
    cout << "\nc = "; PrintVec(c[0], c[1], c[2]);
    cout << endl;
    d = Det(0);
    cout << "D = " << d << endl;

    long double m1 = 0, m2 = 0, m3 = 0;
    for (int i = 0; i < 3; i++) {
        if (Abs(a[i]) > m1) m1 = Abs(a[i]);
        if (Abs(b[i]) > m2) m2 = Abs(b[i]);
        if (Abs(c[i]) > m3) m3 = Abs(c[i]);
    }
    if (d == 0) {
        cout << "Вектори лінійно залежні. Єдиного розкладання немає." << endl;
        cout << "Правило Крамера застосувати неможливо." << endl;
    } else if (Abs(d) <= 1e-12L * m1 * m2 * m3) {
        cout << "Вектори майже лінійно залежні. Обчислення зупинено." << endl;
    } else {
        d1 = Det(1);
        d2 = Det(2);
        d3 = Det(3);
        k1 = d1 / d;
        k2 = d2 / d;
        k3 = d3 / d;
        PrintRes();
        ChekRes();
    }
}

void Run() {
    ReadX();
    if (ok) MakeVec();
    if (ok) {
        Work();
    } else {
        cout << "Помилка: координати мають бути числами від -1000000 до 1000000, вибір — 1 або 2." << endl;
    }
}

int main() {
    Consol();
    Info();
    Run();
}
