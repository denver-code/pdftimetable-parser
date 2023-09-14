import camelot
from json import dumps


class TimetableParser:
    def __init__(self):
        self.content = []
        self.week_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

    def loadPdf(self, filename):
        tables = camelot.read_pdf(filename)
        content = []

        for table in tables:
            content.append(table.df.values.tolist())

        self.content = content

    def _parse(self, content):
        schedule = {}
        current_day = None
        current_session = None

        for i in range(len(content)):
            lines = content[i]

            for line in lines:
                parts = line.split("\n")
                if parts[0] in self.week_days:
                    current_day = parts[0]
                    schedule[current_day] = {}
                elif parts[0] == "" or parts[0] == "1.5":
                    continue
                elif parts[0].startswith("Session") and len(parts) > 1:
                    session_name = parts[0]
                    current_session = session_name
                    schedule[current_day][current_session] = {}
                    schedule[current_day][current_session]["Staff"] = parts[1]
                    if parts[2].startswith("ST"):
                        schedule[current_day][current_session]["Room"] = parts[2]
                        schedule[current_day][current_session]["Type"] = parts[3]
                        schedule[current_day][current_session]["Start"] = parts[4]
                        schedule[current_day][current_session]["End"] = parts[5]
                    else:
                        schedule[current_day][current_session]["Type"] = parts[2]
                        schedule[current_day][current_session]["Start"] = parts[3]
                        schedule[current_day][current_session]["End"] = parts[4]

            return schedule

    def _provide_and_parse(self):
        timetable = {}

        for i in range(len(self.content)):
            schedule = self._parse(self.content[i])
            for day in list(schedule.keys()):
                timetable[day] = schedule[day]

        return timetable

    def toJson(self):
        return dumps(self._provide_and_parse())

    def toDict(self):
        return self._provide_and_parse()


timetable_manager = TimetableParser()
timetable_manager.loadPdf("data.pdf")
timetable = timetable_manager.toDict()

print(timetable)
