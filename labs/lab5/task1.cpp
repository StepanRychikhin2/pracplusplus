#include <iostream>
#include <cctype>
#include <cstdio>
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
    cout << "Лабораторна робота №5. Завдання 1." << endl;
    cout << "Автор: Степан Ричіхін, ІПЗ-11" << endl;
    cout << "Ввести два натуральних числа m та n." << endl;
    cout << "Знайти їх найбільший спільний дільник за алгоритмом Евкліда." << endl;
    cout << "Використати два способи: рекурсію та цикл." << endl;
    cout << "Визначити глибину рекурсії та кількість ітерацій циклу." << endl;
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

// Зчитуємо два натуральних числа
void getNumbers(long long &m, long long &n) {
    cout << "Введіть m та n: ";
    cin >> m >> n;
}

// Натуральні числа мають бути цілими й більшими за нуль
bool checkNumbers(long long m, long long n) {
    bool valid = checkInput() && m > 0 && n > 0;
    return valid;
}

// Рекурсивно знаходимо НСД за співвідношенням з умови
long long getGcdRec(long long a, long long b, int &depth) {
    // Кожен виклик додає один рівень перший виклик теж рахуємо
    depth++;
    long long result = 0;

    if (b % a == 0) {
        result = a; // b ділиться на a без остачі
    } else if (a % b == 0) {
        result = b; // a ділиться на b без остачі
    } else if (b >= a) {
        // Замінюємо більше число остачею від ділення на менше
        result = getGcdRec(a, b % a, depth);
    } else {
        result = getGcdRec(a % b, b, depth);
    }

    return result;
}

// Знаходимо той самий НСД але за допомогою циклу
long long getGcdLoop(long long a, long long b, int &count) {
    count = 0;

    // Працюємо поки жодне число не ділиться на інше без остачі
    while (b % a != 0 && a % b != 0) {
        if (b >= a) {
            b = b % a;
        } else {
            a = a % b;
        }
        count++; // Рахуємо виконання тіла циклу
    }

    long long result = b;
    if (b % a == 0) {
        result = a;
    }

    return result;
}

// Виводимо результати обох способів та лічильники
void printResult(long long resultRec, long long resultLoop, int depth, int count) {
    cout << "\nНСД через рекурсію: " << resultRec << endl;
    cout << "Глибина рекурсії: " << depth << endl;
    cout << "НСД через цикл: " << resultLoop << endl;
    cout << "Кількість ітерацій циклу: " << count << endl;

    if (resultRec == resultLoop) {
        cout << "Результати обох способів збігаються." << endl;
    } else {
        cout << "Результати обох способів відрізняються." << endl;
    }
}

// Коротко пояснюємо різницю між двома способами
void printComparison() {
    cout << "\nПерший виклик входить у глибину рекурсії." << endl;
    cout << "Обидва способи виконують однакову кількість замін чисел остачами." << endl;
    cout << "Цикл не створює ланцюжок вкладених викликів функції." << endl;
}

// Отримуємо відповіді для однакових початкових чисел
void solveTask(long long m, long long n) {
    int depth = 0; // Глибина разом із першим викликом
    int count = 0; // Кількість ітерацій
    // Функції працюють із копіями тому m та n не змінюються
    long long resultRec = getGcdRec(m, n, depth);
    long long resultLoop = getGcdLoop(m, n, count);
    printResult(resultRec, resultLoop, depth, count);
    printComparison();
}

// Пояснюємо які числа потрібно ввести
void printError() {
    cout << "Помилка: введіть два цілі додатні числа в межах типу long long." << endl;
}

// Керуємо порядком роботи програми
void runTask() {
    long long m = 0, n = 0;
    getNumbers(m, n);

    if (checkNumbers(m, n)) {
        solveTask(m, n);
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
