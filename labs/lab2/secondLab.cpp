#include <iostream>  // Бібліотека для введення та виведення даних
#include <cmath>     // Бібліотека математичних функцій

// Функція для обчислення значення f(a, b)
double caculate_f(double a, double b)
{
    // Якщо a більше за b
    if (a > b)
    {
        // Обчислюємо a² / b²
        return (a * a) / (b * b);
    }
    // Якщо a менше за b
    else if (a < b)
    {
        // Обчислюємо b² - a²
        return (b * b) - (a * a);
    }
    // Якщо a дорівнює b
    else
    {
        // Значення функції дорівнює 1
        return 1;
    }
}

int main()
{
    // Оголошуємо змінні для збереження значень a та b
    double a, b;

    // Вводимо значення a з клавіатури
    std::cout << "Enter a: ";
    std::cin >> a;

    // Вводимо значення b з клавіатури
    std::cout << "Enter b: ";
    std::cin >> b;

    // Викликаємо функцію та зберігаємо результат
    double result = caculate_f(a, b);

    // Виводимо результат на екран
    std::cout << "Result f(a, b) = " << result << std::endl;

    return 0; // Завершення програми
}