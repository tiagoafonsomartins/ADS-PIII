from metrics.Metric import *
from classroom.Classroom import Classroom
from lesson.Lesson import Lesson


def test_gaps():
    lesson1 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    lesson2 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "11:00:00", "12:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    lesson3 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "13:00:00", "15:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    classroom1 = Classroom('Edifício 69', 'Auditório 420', 50, 25, ["cenas"])
    classroom2 = Classroom('Edifício 2', 'B203', 150, 125, ["cenas", "mais cenas", "ainda mais cenas"])
    lesson1.add_classroom(classroom1)
    lesson2.add_classroom(classroom2)
    lesson3.add_classroom(classroom2)

    gang = Gang("best", "lei", lesson1)
    gang.add_lesson(lesson2)
    gang.add_lesson(lesson3)

    gaps = Gaps()

    gaps.calculate(gang)

    print("Gaps: ", gaps.value)


def test_movements():
    lesson1 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    lesson2 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "11:00:00", "12:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    lesson3 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "13:00:00", "15:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    classroom1 = Classroom('Edifício 69', 'Auditório 420', 50, 25, ["cenas"])
    classroom2 = Classroom('Edifício 2', 'B203', 150, 125, ["cenas", "mais cenas", "ainda mais cenas"])
    lesson1.add_classroom(classroom1)
    lesson2.add_classroom(classroom2)
    lesson3.add_classroom(classroom2)

    gang = Gang("best", "lei", lesson1)
    gang.add_lesson(lesson2)
    gang.add_lesson(lesson3)

    movements = Movements()

    movements.calculate(gang)

    print("Number of Movements: ", movements.value)


def test_used_rooms():
    lesson1 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    lesson2 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "11:00:00", "12:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    lesson3 = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "13:00:00", "15:00:00", "4/23/2005",
                     "Good, Not stinky, Very good")
    classroom1 = Classroom('Edifício 69', 'Auditório 420', 50, 25, ["cenas"])
    classroom2 = Classroom('Edifício 2', 'B203', 150, 125, ["cenas", "mais cenas", "ainda mais cenas"])
    lesson1.add_classroom(classroom1)
    lesson2.add_classroom(classroom2)
    lesson3.add_classroom(classroom2)

    used_rooms = UsedRooms()

    used_rooms.calculate(lesson1, classroom1)
    used_rooms.calculate(lesson2, classroom2)
    used_rooms.calculate(lesson3, classroom1)

    print("Used rooms: ", used_rooms.value)


test_gaps()
test_movements()
test_used_rooms()
