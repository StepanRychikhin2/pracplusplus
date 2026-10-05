#include <iostream>
#include <iomanip>
#include <cmath>
#include <string>
#include <windows.h>

using namespace std;

int main()
{
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    // Введення точності
    double eps;
    cout << "Введіть eps: ";
    cin >> eps;

    // Перевірка точності
    if (!cin || eps <= 0)
    {
        cout << "Помилка: eps має бути додатним числом.\n";
        return 1;
    }

    // Межі для захисту від дуже великих і дуже малих членів
    const double minlimit = 1e-38;
    const double maxlimit = 1e38;

    // Загальна сума
    double total = 0.0;

    // Оформлення таблиці
    cout << endl
         << setw(4) << "x"
         << setw(6) << "k"
         << setw(20) << "Член ряду"
         << setw(20) << "Сума" << endl;
    cout << string(50, '-') << endl;

    // Зовнішня сума
    for (int x = 1; x <= 5; x++)
    {
        int k = 0; // номер поточного члена

        // Перший член при k = 0: 1 / x
        double a = 1.0 / x;
        double sum = 0.0;

        // Внутрішня сума
        while (true)
        {
            double m = fabs(a);

            // Перевірка меж
            if (m >= maxlimit)
            {
                cout << "Член ряду досяг верхньої межі.\n";
                break;
            }

            // Додаємо член до суми
            sum += a;

            // Виводимо поточний рядок
            cout << fixed << setprecision(8)
                 << setw(4) << x
                 << setw(6) << k
                 << setw(20) << a
                 << setw(20) << sum << endl;

            // Перевірка точності та нижньої межі
            if (m < eps || m < minlimit)
                break;

            // Обчислюємо наступний член рекурентно:
            // a(k+1) = a(k) * (-x^2) * (2k-1) / ((2k+1)(k+1))
            a *= -static_cast<double>(x) * x * (2 * k - 1) /
                 ((2.0 * k + 1) * (k + 1));

            k++;
        }

        // Розділювач між сумами для різних x
        cout << string(50, '-') << endl;

        // Додаємо внутрішню суму до загальної
        total += sum;
    }

    // Виводимо результат
    cout << "Загальна сума S = " << total << endl;

    return 0;
}