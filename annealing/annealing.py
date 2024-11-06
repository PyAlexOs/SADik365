# принятие решение тем вероятнее, чем выше температура и ниже "негативный" скачок энергии (целевой функции)
import random
from math import exp
from data import Area, TaskType, Task, Crewmate


def reduce_t(t: float) -> float:
    return t * 0.5


def probability(E_original: float, E_current: float, temp: float) -> float:
    # Для задачи максимизации и минимизации "негативный" скачок значения энергии будет в разные стороны (abs)
    return exp(-abs(E_current - E_original) / temp)


def anneal():
    pass


def main():
    start_temp: float = 100.
    min_temp: float = 1.
    crewmates = [Crewmate('')]
    proposed_solution = []


if __name__ == '__main__':
    main()
