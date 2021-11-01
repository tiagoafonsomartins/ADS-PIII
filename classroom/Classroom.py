class Classroom:
    def __init__(self, building: str, name: str, normal_capacity: int, exam_capacity: int, characteristics: list):
        self.schedule = []
        self.building = building
        self.name = name
        self.normal_capacity = normal_capacity
        self.exam_capacity = exam_capacity
        self.characteristics = characteristics

    def get_row(self):
        caracteristicas = []
        for c in self.characteristics:
            if c != '':
                pass #TODO we have to figure out how to do this here
        return [self.building, self.name, str(self.normal_capacity), str(self.exam_capacity), '']

    def add_lesson(self, lesson):
        self.schedule.append(lesson)

    def get_characteristics(self):
        return self.characteristics

    def get_normal_capacity(self):
        return self.normal_capacity

    def remove_lesson(self, lesson):
        self.schedule.remove(lesson)

    def remove_all_lessons(self):
        self.schedule = []

        '''
        Colunas no excell sobre salas

        Edifício                                                string
        Nome sala                                               string
        Capacidade Normal                                       int
        Capacidade Exame                                        int
        Nºcaracterísticas                                       int
        Anfiteatro aulas                                        boolean
        Apoio técnico eventos                                   boolean
        Arq 1                                                   boolean
        Arq 2                                                   boolean
        Arq 3                                                   boolean
        Arq 4                                                   boolean
        Arq 5                                                   boolean
        Arq 6                                                   boolean
        Arq 9                                                   boolean
        BYOD(Bring Your Own Device)                             boolean
        Focus Group                                             boolean
        Horário sala visível portal público                     boolean
        Laboratório de Arquitectura de Computadores I           boolean
        Laboratório de Arquitectura de Computadores II          boolean
        Laboratório de Bases de Engenharia                      boolean
        Laboratório de Electrónica                              boolean
        Laboratório de Informática                              boolean
        Laboratório de Jornalismo                               boolean
        Laboratório de Redes de Computadores I                  boolean
        Laboratório de Redes de Computadores II                 boolean
        Laboratório de Telecomunicações                         boolean
        Sala Aulas Mestrado                                     boolean
        Sala Aulas Mestrado Plus                                boolean
        Sala NEE                                                boolean
        Sala Provas                                             boolean
        Sala Reunião                                            boolean
        Sala de Arquitectura                                    boolean
        Sala de Aulas normal                                    boolean
        videoconferencia                                        boolean
        Átrio                                                   boolean
        '''


    pass