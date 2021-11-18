class AlgResults:

    overbooking = None

    def __init__(self, metrics):
        self.schedule = []
        self.metrics = metrics

    def add_association(self, lesson, classroom):
        self.schedule.append((lesson, classroom))

    def calculate_metrics(self, classrooms, gangs):
        metrics_lessons = []
        metrics_gangs = []
        metrics_classrooms = []
        for metric in self.metrics:
            if metric.m_type == "lessons":
                metrics_lessons.append(metric)
            elif metric.m_type == "gangs":
                metrics_gangs.append(metric)
            elif metric.m_type == "classrooms":
                metrics_classrooms.append(metric)

        for lesson, classroom in self.schedule:
            for metric in metrics_lessons:
                metric.calcular(lesson, classroom)
        for classroom in classrooms:
            for metric in metrics_gangs:
                metric.calcular(classroom)
        for gang in gangs:
            for metric in metrics_classrooms:
                metric.calcular(gang)

    def calculate_overbooking(self):
        self.cenas = "fdshaf"
