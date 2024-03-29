class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Отображение информационного сообщения о тренировке."""
        return(f'Тип тренировки: {self.training_type}; '
               f'Длительность: {self.duration:.3f} ч.; '
               f'Дистанция: {self.distance:.3f} км; '
               f'Ср. скорость: {self.speed:.3f} км/ч; '
               f'Потрачено ккал: {self.calories:.3f}.'
               )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    TIME: int = 60

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
        g_dist: float = self.action * self.LEN_STEP / self.M_IN_KM
        return g_dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Неизвестный вид тренировки")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CAL1: int = 18
    COEFF_CAL2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Считаем потраченные калории при беге."""
        d1: float = self.COEFF_CAL1 * self.get_mean_speed() - self.COEFF_CAL2
        d2: float = self.duration * Training.TIME
        calories_run: float = d1 * self.weight / self.M_IN_KM * d2
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CAL3: float = 0.035
    COEFF_CAL4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Считаем потраченные калории при ходьбе."""
        d3: float = self.duration * Training.TIME
        calories_wilk: float = ((self.COEFF_CAL3 * self.weight
                                + (self.get_mean_speed()**2 // self.height)
                                * self.COEFF_CAL4 * self.weight) * d3)
        return calories_wilk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CAL5: float = 1.1
    COEFF_CAL6: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Средняя скорость при плавании."""
        return (self.length_pool * self.count_pool / Training.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Считаем потраченные калории при плавании."""
        calories_swim: float = ((self.get_mean_speed() + self.COEFF_CAL5)
                                * self.COEFF_CAL6 * self.weight)
        return calories_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read: dict = {'RUN': Running, 'WLK': SportsWalking, 'SWM': Swimming}
    if workout_type in read:
        return read[workout_type](*data)
    raise ValueError


def main(train: Training) -> None:
    """Главная функция."""
    info: InfoMessage = train.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
