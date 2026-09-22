#include <iostream> // Бібліотека для введення та виведення даних
#include <cmath>    // Бібліотека для математичних функцій

int main()
{
    // Оголошуємо змінні для координат точки
    double x, y;

    // Вводимо координату x
    std::cout << "Enter x: ";
    std::cin >> x;

    // Вводимо координату y
    std::cout << "Enter y: ";
    std::cin >> y;

    // Перевіряємо, чи точка знаходиться у першому квадранті
    if (x > 0 && y > 0)
    {
        std::cout << "Point in first quadrant" << std::endl;

        // Обчислюємо відстань від точки до початку координат
        double distance = std::sqrt(x * x + y * y);

        // Виводимо відстань
        std::cout << "Distance to the lane " << distance << std::endl;
    }
    // Перевіряємо другий квадрант
    else if (x < 0 && y > 0)
    {
        std::cout << "Point in second quadrant" << std::endl;
    }
    // Перевіряємо третій квадрант
    else if (x < 0 && y < 0)
    {
        std::cout << "Point in third quadrant" << std::endl;
    }
    // Перевіряємо четвертий квадрант
    else if (x > 0 && y < 0)
    {
        std::cout << "Point in fourth quadrant" << std::endl;
    }
    // Якщо x або y дорівнює нулю, точка знаходиться на осі
    else
    {
        std::cout << "Point in line" << std::endl;
    }

    return 0; // Завершення програми
}