import random


class DTassignment:
    def __init__(self, members: set):
        self.all_members = members
        self.mon_group = list()
        self.mon_grouping = ""

        self.wed_group = list()
        self.wed_grouping = ""

        self.fri_group = list()
        self.fri_grouping = ""

    def assign_random_groupings(self) -> None:
        to_distribute = self.all_members.copy()
        bucket = "mon"
        while to_distribute:
            # helper function for id-ing dt group
            def assignment(day: str) -> list:
                switcher = {
                    "mon": self.mon_group,
                    "wed": self.wed_group,
                    "fri": self.fri_group,
                }
                return switcher.get(day, "Invalid day of week")

            # helper function for advancing bucket to next day
            def next_bucket(weekday: str) -> str:
                switcher = {
                    "mon": "wed",
                    "wed": "fri",
                    "fri": "mon",
                }
                return switcher.get(weekday, "Invalid day of week")

            # pull random user and assign to a m-w-f dt group
            random_user = random.sample(to_distribute, 1)[0]
            assignment(bucket).append(random_user)

            # advance bucket to next day, remove assigned user
            bucket = next_bucket(bucket)
            to_distribute.remove(random_user)

        # sort groupings alphabetically
        self.mon_group.sort()
        self.wed_group.sort()
        self.fri_group.sort()

        def grouping_toString(group: list) -> str:
            dudes = ":joy:  "
            for user_id in group:
                dude = "<@" + user_id + ">"
                dudes += dude
                dudes += "  "
            dudes += ":joy:"
            return dudes

        self.mon_grouping = grouping_toString(self.mon_group)
        self.wed_grouping = grouping_toString(self.wed_group)
        self.fri_grouping = grouping_toString(self.fri_group)

    def clear_groupings(self) -> None:
        self.mon_group.clear()
        self.wed_group.clear()
        self.fri_group.clear()
