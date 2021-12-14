from alocate.Algorithm_Utils import sorted_lessons, sorted_classrooms


def simple_allocation(schedule: list, classrooms: list) -> list:
    '''
    Simple allocation algorithm that allocates first room that accommodates the lessons requested characteristics
    and is available at that time

    :return list[(Lesson, Classroom)]: Returns list of tuples that associates lesson with allocated classroom
    '''
    lessons_list = sorted_lessons(schedule)
    classrooms_list = sorted_classrooms(classrooms)

    number_of_roomless_lessons = 0

    schedule = []

    for lesson, c in lessons_list:
        if not c:
            classroom_assigned = False
            for classroom in classrooms_list:
                if (lesson.get_requested_characteristics() in classroom.get_characteristics()) and \
                        (lesson.get_number_of_enrolled_students() <= classroom.get_normal_capacity()) and \
                        (classroom.is_available(lesson.generate_time_blocks())):
                    classroom.set_unavailable(lesson.generate_time_blocks())
                    schedule.append((lesson, classroom))
                    classroom_assigned = True
                    break

            if not classroom_assigned:
                if lesson.requested_characteristics != "Não necessita de sala" and \
                        lesson.requested_characteristics != "Lab ISTA":
                    schedule.append((lesson, None))
                    number_of_roomless_lessons += 1
        else:
            schedule.append((lesson, c))

    print("There are ", number_of_roomless_lessons, " lessons without a classroom.")

    return schedule
