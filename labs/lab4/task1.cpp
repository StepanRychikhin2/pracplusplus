#include <iostream>
#include <cctype>
#include <cstdio>
#include <iomanip>
#include <cmath>
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
    cout << "Лабораторна робота №4. Завдання 1." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Обчислити функцію за допомогою ряду Маклорена:" << endl;
    cout << "y = cos(x/2) / cos(x*x), якщо -1 <= x <= 0;" << endl;
    cout << "y = cos(x/2) * cos(x/2) * cos(2*x), якщо x > 0." << endl;
    cout << "Ввести межі x, крок і точність від 0.000001 до 0.01." << endl;
    cout << "Вивести таблицю та порівняти результат зі стандартною функцією." << endl;
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

// Зчитуємо межі таблиці крок і точність
void getData(double &start, double &end, double &step, double &eps) {
    cout << "Введіть мінімальне і максимальне x: ";
    cin >> start >> end;
    cout << "Введіть крок: ";
    cin >> step;
    cout << "Введіть точність (наприклад, 0.0001): ";
    cin >> eps;
}

// Перевіряємо чи підходять дані для обчислення
bool checkData(double start, double end, double step, double eps) {
    bool valid = checkInput();
    valid = valid && isfinite(start) && isfinite(end);
    valid = valid && isfinite(step) && isfinite(eps);
    valid = valid && start <= end && step > 0;
    valid = valid && eps >= 0.000001 && eps <= 0.01;
    return valid;
}

// Пояснюємо які дані можна вводити
void printError() {
    cout << "Помилка: введіть скінченні числа початок не більший за кінець." << endl;
    cout << "Крок має бути додатним, точність — від 0.000001 до 0.01." << endl;
}

// Рахуємо косинус через ряд без степенів і факторіалів
double cosSum(double x, double eps) {
    const double pi = 3.14159265358979323846;
    // Зменшуємо аргумент бо косинус повторюється через повний оберт
    x = remainder(x, 2 * pi);

    double sum = 1;         // Перший член ряду
    double a = -x * x / 2; // Наступний член
    int k = 1;

    // Додаємо тільки ті члени які ще більші за точність
    while (fabs(a) > eps) {
        sum += a;
        k++;
        // Новий член отримуємо з попереднього
        a = -a * x * x / ((2.0 * k - 1) * (2.0 * k));
    }

    return sum;
}

// Обчислюємо y через нашу функцію косинуса
double getSeriesValue(double x, double eps) {
    // Беремо запас точності бо косинуси ще множаться або діляться
    double a = cosSum(x / 2, eps / 10);
    double result = 0;

    if (x <= 0) {
        double b = cosSum(x * x, eps / 10);
        result = a / b;
    } else {
        double b = cosSum(2 * x, eps / 10);
        result = a * a * b;
    }

    return result;
}

// Обчислюємо y через бібліотечний косинус для порівняння
double getStandardValue(double x) {
    double a = cos(x / 2);
    double result = 0;

    if (x <= 0) {
        result = a / cos(x * x);
    } else {
        result = a * a * cos(2 * x);
    }

    return result;
}

// Виводимо назви стовпчиків таблиці
void printHeader() {
    cout << "\nЗначення аргумента x | Значення функції y | Стандартне значення функції | Похибка" << endl;
    cout << "--------------------------------------------------------------------------------------" << endl;
    cout << fixed << setprecision(8);
}

// Виводимо один готовий рядок із результатами
void printValues(double result, double standard) {
    // За умовою потрібна різниця модулів вона може бути від'ємною
    double error = fabs(result) - fabs(standard);
    cout << setw(18) << result << " | "
         << setw(27) << standard << " | "
         << scientific << setprecision(3) << error
         << fixed << setprecision(8) << endl;
}

// Перевіряємо аргумент і готуємо рядок таблиці
void printRow(double x, double eps) {
    cout << setw(20) << x << " | ";

    if (x < -1) {
        cout << "function is not defined" << endl;
    } else if (!isfinite(2 * x)) {
        cout << "Аргумент 2*x завеликий для обчислення." << endl;
    } else {
        double result = getSeriesValue(x, eps);
        double standard = getStandardValue(x);
        printValues(result, standard);
    }
}

// Знаходимо наступне x із поправкою на округлення дробових чисел
double getNextX(double x, double end, double step) {
    double next = x + step;

    // Наприклад одна десята плюс дві десяті може бути трохи більшим за три десяті
    if (isfinite(next) && next > end && next - end <= step * 1e-9) {
        next = end;
    }

    return next;
}

// Проходимо всі значення x та виводимо таблицю
void printTable(double start, double end, double step, double eps) {
    double x = start;
    bool more = true; // Чи залишилися значення для таблиці
    printHeader();

    while (more) {
        printRow(x, eps);
        more = x < end;

        if (more) {
            double next = getNextX(x, end, step);
            // Продовжуємо тільки тоді коли x збільшується і не виходить за межу
            more = next > x && next <= end;
            if (next <= x) {
                cout << "Помилка: крок замалий для цих значень x." << endl;
            }
            x = next;
        }
    }
}

// Поєднуємо введення перевірку та побудову таблиці
void runTask() {
    double start = 0, end = 0, step = 0, eps = 0;
    getData(start, end, step, eps);

    if (checkData(start, end, step, eps)) {
        printTable(start, end, step, eps);
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
