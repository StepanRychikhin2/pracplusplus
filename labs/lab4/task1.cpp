#include <iostream> // Введення даних і виведення результатів
#include <iomanip>  // Рівні стовпчики таблиці
#include <cmath>    // cos, fabs, remainder та перевірка чисел
#ifdef _WIN32
#include <windows.h> // Українські літери у консолі Windows
#endif

using namespace std;

void printTaskInfo()
{
    cout << "========================Завдання========================" << endl;
    cout << "Лабораторна робота №4. Завдання 1." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Обчислити функцію за допомогою ряду Маклорена:" << endl;
    cout << "y = cos(x/2) / cos(x*x), якщо -1 <= x <= 0;" << endl;
    cout << "y = cos(x/2) * cos(x/2) * cos(2*x), якщо x > 0." << endl;
    cout << "Ввести межі x, крок і точність від 0.000001 до 0.01." << endl;
    cout << "Вивести таблицю та порівняти результат зі стандартною функцією." << endl;
    cout << "========================================================" << endl;
}

// Рахуємо косинус через ряд: 1 - x*x/2! + x*x*x*x/4! - ...
double cosSum(double x, double eps)
{
    const double pi = 3.14159265358979323846;

    // Косинус повторюється через 2*pi. Зменшуємо аргумент,
    // щоб для великих x члени ряду не ставали дуже великими.
    x = remainder(x, 2 * pi);

    double a = 1;   // Перший член ряду
    double sum = 1; // Сума спочатку дорівнює першому члену
    int k = 1;     // Номер наступного члена

    while (true)
    {
        // Отримуємо новий член із попереднього.
        // Окремо степінь і факторіал не обчислюємо.
        a = -a * x * x / ((2.0 * k - 1) * (2.0 * k));

        // Якщо наступний член уже малий, його можна не додавати.
        if (fabs(a) <= eps)
            break;

        sum += a;
        k++;
    }

    return sum;
}

int main()
{
#ifdef _WIN32
    // Налаштовуємо українські літери у Windows.
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif

    printTaskInfo();

    double start, end, step, eps;

    cout << "Введіть мінімальне і максимальне x: ";
    cin >> start >> end;
    cout << "Введіть крок: ";
    cin >> step;
    cout << "Введіть точність (наприклад, 0.0001): ";
    cin >> eps;

    // Не починаємо обчислення, якщо замість чисел введено текст.
    if (!cin || !isfinite(start) || !isfinite(end) ||
        !isfinite(step) || !isfinite(eps))
    {
        cout << "Помилка: потрібно ввести скінченні числа." << endl;
        return 1;
    }

    // Рухаємося від меншого x до більшого з додатним кроком.
    if (start > end || step <= 0)
    {
        cout << "Помилка: початок має бути не більшим за кінець, а крок — додатним." << endl;
        return 1;
    }

    if (eps < 0.000001 || eps > 0.01)
    {
        cout << "Помилка: точність має бути від 0.000001 до 0.01." << endl;
        return 1;
    }

    // Назви стовпчиків відповідають умові роботи.
    cout << "\nЗначення аргумента x | Значення функції y | Стандартне значення функції | Похибка" << endl;
    cout << "--------------------------------------------------------------------------------------" << endl;
    cout << fixed << setprecision(8);

    double x = start;
    while (x <= end)
    {
        cout << setw(20) << x << " | ";

        // Для x < -1 в умові немає жодної формули.
        if (x < -1)
        {
            cout << "function is not defined" << endl;
        }
        else if (!isfinite(2 * x))
        {
            // Для надто великого x число 2*x вже не вміщується у double.
            cout << "Аргумент 2*x завеликий для обчислення." << endl;
        }
        else
        {
            double y, standard;

            // Беремо меншу похибку для окремих косинусів,
            // бо далі їх значення ще множаться або діляться.
            double a = cosSum(x / 2, eps / 10);

            if (x <= 0)
            {
                // Тут x*x лежить від 0 до 1, тому cos(x*x) не дорівнює нулю.
                double b = cosSum(x * x, eps / 10);
                y = a / b;
                standard = cos(x / 2) / cos(x * x);
            }
            else
            {
                double b = cosSum(2 * x, eps / 10);
                y = a * a * b;
                standard = cos(x / 2) * cos(x / 2) * cos(2 * x);
            }

            // За умовою віднімаємо саме абсолютні значення результатів.
            double error = fabs(y) - fabs(standard);

            cout << setw(18) << y << " | "
                 << setw(27) << standard << " | "
                 << scientific << setprecision(3) << error
                 << fixed << setprecision(8) << endl;
        }

        // Останнє значення вже оброблено — завершуємо цикл.
        if (x == end)
            break;

        double next = x + step;

        // Дуже малий крок може не змінити число через округлення.
        if (next <= x)
        {
            cout << "Помилка: крок замалий для цих значень x." << endl;
            return 1;
        }

        // Наприклад, 0.1 + 0.2 може трохи відрізнятися від 0.3.
        // Прибираємо таку маленьку неточність біля кінця таблиці.
        if (isfinite(next) && next > end && next - end <= step * 1e-9)
            next = end;

        x = next;
    }

    return 0;
}
