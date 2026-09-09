#include <iostream>
#include <cmath>
#include <windows.h>
using namespace std;

int main()
{
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    // Завдання 1
    double A, B, C, X;

    cout << "Введіть A: ";
    cin >> A;

    cout << "Введіть B: ";
    cin >> B;

    cout << "Введіть C: ";
    cin >> C;

    X = pow(sin(C), 3) * pow(cos(A), 2) / (exp(A) + 1 + sin(B));

    cout << "X = " << X << endl;

    // ЗАвдання 2
    double P, d;

    cout << "Введіть периметер P: ";
    cin >> P;

    d = P / 4;

    cout << "Найменша діагональ = " << d << endl;

    return 1;
}
