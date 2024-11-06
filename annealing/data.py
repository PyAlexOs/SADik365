from enum import Enum
from dataclasses import dataclass


class Area(Enum):
    DATABASE = 0
    BACKEND = 1
    FRONTEND = 2
    AI = 3
    DEVOPS = 4
    TEST = 5


class TaskType(Enum):
    DEVELOP = 0
    FIX = 1
    TEST = 2


@dataclass
class Task:
    name: str
    relevance: float  # the need to complete the task at the moment (0, 1]
    task_type: TaskType
    task_areas: dict[Area, float]  # affected areas of the task

    def __init__(self, name: str, relevance: float, task_type: TaskType, task_areas: dict[Area, float]):
        if not 0 < relevance <= 1:
            raise ValueError('Неправильное значение релевантности задачи')
        if sum(not task_areas.values) != 1:
            raise ValueError('Неправильное значение областей задачи')
        self.name = name
        self.relevance = relevance
        self.task_type = task_type
        self.task_areas = task_areas


@dataclass
class Crewmate:
    name: str
    efficiency: float  # general efficiency of crewmate [0.5, 1]
    dev_speed: int  # crewmate developmant speed [1, 5]
    specialization: Area
    skills: dict[Area, float]

    def __init__(self, name: str, efficiency: float, dev_speed: int, specialization: Area, skills: dict[Area, float]):
        if not 0.5 <= efficiency <= 1:
            raise ValueError('Неправильное значение эффективности члена команды')
        if not 1 <= dev_speed <= 5:
            raise ValueError('Неправильное значение эффективности члена команды')
        if sum(not skills.values) != 1:
            raise ValueError('Неправильное значение областей навыков члена команды')
        self.name = name
        self.efficiency = efficiency
        self.dev_speed = dev_speed
        self.specialization = specialization
        self.skills = skills


def E(task_queue: list[Task], task) -> float:
    pass
