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
    // введення зміної
    double eps;
    cout << "Введіть eps ";
    cin >> eps;

    // Межі для захисту від переповнення
    const double MIN_LIMIT = 1e-38; // занадто малий член
    const double MAX_LIMIT = 1e+38; // занадто великий член

    // total - загальна сума
    double total = 0;

    // jофрлмення таблиці
    cout << endl
         << setw(4) << "x"
         << setw(6) << "k"
         << setw(20) << "Член ряду"
         << setw(20) << "Сума" << endl;
    cout << string(50, '-') << endl;

    // Зовніщгя сумма
    for (int x = 1; x <= 5; x++)
    {

        int k = 0; // номер поточного члена внутрішнього ряду

        // Перший член (k = 0) рахуємо напряму з формули:
        double a = 1.0 / x; // a - поточний член ряду

        double sum = a; // sum - накопичена сума внутрішнього ряду для цього x

        // Виводимо рядок таблиці для k = 0
        cout << fixed << setprecision(8)
             << setw(4) << x
             << setw(6) << k
             << setw(20) << a
             << setw(20) << sum << endl;

        // while нескінченний цикл
        while (true)
        {

            a *= -(double)x * x * (2 * k - 1) / ((2.0 * k + 1) * (k + 1));

            k++; // переходимо до наступного номера

            double m = fabs(a); // модуль члена

            // Умова виходу з while якщо mо < eps то досягнуто відповіді
            // якщо m < MIN_LIMIT то член занадто малий
            // якщо m > MAX_LIMIT то член занадто великий
            if (m < eps || m < MIN_LIMIT || m > MAX_LIMIT)
                break;

            // Додаємо член до накопиченої суми внутрішнього ряду
            sum += a;

            // Виводимо поточний рядок таблиці
            cout << setw(4) << x
                 << setw(6) << k
                 << setw(20) << a
                 << setw(20) << sum << endl;
        }

        // Лінія поділу  між блоками
        cout << string(50, '-') << endl;

        // Додаємо суму внутрішнього ряду до загальної (зовнішня сума)
        total += sum;
    }

    // Відповідь
    cout << "Загальна сума S = " << total << endl;

    return 0; // 0 - Кінець
}