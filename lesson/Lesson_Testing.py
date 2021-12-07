from lesson.Lesson import Lesson


class Lesson_Testing:

    def __init__(self):
        pass

    def test_generate_time_blocks(self):
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
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
        print("end\n\n")

    def test_get_row(self):
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(lesson.get_row())

    def test_time_to_string(self):
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")
        print(lesson.time_to_string(12))
        print(lesson.time_to_string(3))
        print(lesson.time_to_string(0))
        print(lesson.time_to_string(-4))
        print(lesson.time_to_string("32"))
        print(lesson.time_to_string("Mens"))

    def test_datetime_to_string(self):
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")

        print(lesson.datetime_to_string("12/30/2022", "09:00:00", "10:00:00"))
        print(lesson.datetime_to_string("asfas", "sdafsad", "sadfsad"))
        print(lesson.datetime_to_string(1, "09:00:00", "10:00:00"))
        print(lesson.datetime_to_string("12/30/2022", True, "10:00:00"))
        print(lesson.datetime_to_string("12/30/2022", "09:00:00", 4.3))

    def test_string_to_datetime(self):
        lesson = Lesson("MEI", "ADS", "69420blz", "t-69", 420, "Sex", "3:00:00", "10:00:00", "4/23/2005",
                        "Good, Not stinky, Very good")

        print(lesson.string_to_datetime("10/16/2015_09:30:00-10:00:00"))
        print(lesson.string_to_datetime("fdsafsa_fdsafsda-fdsfdsa"))
        print(lesson.string_to_datetime("fdsafsa-fdsafsda_fdsfdsa"))
        print(lesson.string_to_datetime(True))
        print(lesson.string_to_datetime("fjlkdsa_fdsajhfdsa"))


lt = Lesson_Testing()
lt.test_generate_time_blocks()
lt.test_get_row()
lt.test_time_to_string()
lt.test_datetime_to_string()
lt.test_string_to_datetime()
