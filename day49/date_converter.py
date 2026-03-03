import datetime as dt

class DateConverter:
    def __init__(self, workout_day, workout_time, advance=None):
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        workout_day = workout_day
        now = dt.datetime.now()
        if advance != None:
            delta_advance = dt.timedelta(days=advance["days"], hours=advance["hours"], minutes=advance["minutes"])
            now += delta_advance
        delta_one_day = dt.timedelta(days=1)
        today = now.strftime("%A")

        difference = days_of_week.index(workout_day) - days_of_week.index(today)

        if difference >= 0:
            self.workout_date = now + difference * delta_one_day
        else:
            self.workout_date = now + (len(days_of_week) + difference) * delta_one_day

        time = workout_time.split()[0]
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        AM_PM = workout_time.split()[1]

        if AM_PM == "PM":
            hour += 12
        
        self.workout_date = self.workout_date.replace(hour=hour, minute=minute, second=0, microsecond=0)


    def convert_to_tag_format(self):
        tag_string = self.workout_date.strftime("%Y-%m-%d-%H%M")
        return tag_string
    

    def convert_to_human_readable_format(self):
        human_readable_string = self.workout_date.strftime("%a, %b %d")
        return human_readable_string
