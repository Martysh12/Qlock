import os

from qlock_digits import COLON, EMPTY_COLON, NUMS


class QlockRenderer:
    def _get_time_of_day(self, now):
        user = os.getlogin()

        hour_float = now.hour + (now.minute / 60)

        if hour_float >= 23 or hour_float < 5:
            time_of_day = "night"
        elif hour_float >= 5 and hour_float < 13:
            time_of_day = "morning"
        elif hour_float >= 13 and hour_float < 18:
            time_of_day = "afternoon"
        elif hour_float >= 18 and hour_float < 23:
            time_of_day = "evening"

        return f"Good {time_of_day}, {user}"

    def _get_time_string(self, now):
        chars = []

        for i in str(now.hour).zfill(2):
            chars.append(NUMS[int(i)])

        chars.append(COLON if now.second % 2 == 0 else EMPTY_COLON)

        for i in str(now.minute).zfill(2):
            chars.append(NUMS[int(i)])

        s = ""

        for i in range(len(chars[0].split("\n"))):
            for char in chars:
                s += char.split("\n")[i] + " "

            s = s.rstrip() + "\n"

        return s.rstrip("\n")

    def _generate_number_suffix(self, number):
        if str(number).endswith("1"):
            return "st"
        if str(number).endswith("2"):
            return "nd"
        if str(number).endswith("3"):
            return "rd"
        else:
            return "th"

    def _get_date_string(self, now):
        return now.strftime(f"%A, %B {now.day}{self._generate_number_suffix(now.day)}")

    def render(self, now):
        return (
            self._get_time_of_day(now)
            + "\n\n"
            + self._get_time_string(now)
            + "\n\n"
            + self._get_date_string(now)
        )
