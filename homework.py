from dataclasses import dataclass
from typing import List, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Напечатать сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите метод get_spent_calories '
                                  'в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_RUN_MULT: int = 18
    COEFF_RUN_SPEED: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_min = self.duration * self.MIN_IN_H
        calories_spent_run = ((self.COEFF_RUN_MULT * self.get_mean_speed()
                              - self.COEFF_RUN_SPEED)
                              * self.weight / self.M_IN_KM * duration_in_min)
        return calories_spent_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WALK_WEIGHT_MULT: float = 0.035
    COEFF_WALK_SPEED_MULT: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_min = self.duration * self.MIN_IN_H
        calories_spent_walk = ((self.COEFF_WALK_WEIGHT_MULT * self.weight
                               + (self.get_mean_speed() ** 2 // self.height)
                               * self.COEFF_WALK_SPEED_MULT * self.weight)
                               * duration_in_min)
        return calories_spent_walk


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_SWIM_SPEED: float = 1.1
    COEFF_SWIM_SPEED_MULT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed_swim = ((self.length_pool * self.count_pool)
                          / self.M_IN_KM / self.duration)
        return avg_speed_swim

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_spent_swim = ((self.get_mean_speed() + self.COEFF_SWIM_SPEED)
                               * self.COEFF_SWIM_SPEED_MULT * self.weight)
        return calories_spent_swim


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: Dict[str, Type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}
    if workout_type in workout_dict:
        training_item = workout_dict[workout_type]
        return training_item(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    printed_message = info.get_message()
    print(printed_message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
