from lesson.Lesson import Lesson


class Lesson_Testing:

    def __init__(self):
        pass

    def test_generate_time_blocks(self):
        lesson = Lesson("MEI", "ADS","69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(lesson.generate_time_blocks())
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "4:00:00", "5:30:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(lesson.generate_time_blocks())
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "22:30:00", "23:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(lesson.generate_time_blocks())
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "22:30:00", "22:45:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(lesson.generate_time_blocks())
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "5:00:00", "4:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(lesson.generate_time_blocks())



lt = Lesson_Testing()
lt.test_generate_time_blocks()