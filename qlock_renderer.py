import os


class QlockRenderer:
    def __init__(self, config):
        self.update_config(config)

    def update_config(self, config):
        self.config = config

    def render_hello(self, time):
        user = os.getlogin()

        hour_float = time.hour() + (time.minute() / 60)

        if hour_float >= 23 or hour_float < 5:
            time_of_day = "night"
        elif hour_float >= 5 and hour_float < 13:
            time_of_day = "morning"
        elif hour_float >= 13 and hour_float < 18:
            time_of_day = "afternoon"
        elif hour_float >= 18 and hour_float < 23:
            time_of_day = "evening"

        return f"Good {time_of_day}, {user}"

    def render_clock(self, time):
        chars = []

        for i in str(time.hour()).zfill(2):
            chars.append(self.config["digits"][i])

        chars.append(self.config["digits"]["colon"] if time.second() % 2 == 0 else self.config["digits"]["no_colon"])

        for i in str(time.minute()).zfill(2):
            chars.append(self.config["digits"][i])

        s = ""

        for i in range(len(chars[0].split("\n"))):
            for char in chars:
                s += char.split("\n")[i] + " "

            s = s.rstrip() + "\n"

        return s.rstrip("\n")

    def _generate_number_suffix(self, number):
        if number == 1:
            return "st"
        if number == 2:
            return "nd"
        if number == 3:
            return "rd"
        else:
            return "th"

    def render_date(self, date):
        return date.toString(f"dddd, MMMM {date.day()}{self._generate_number_suffix(date.day())}")
