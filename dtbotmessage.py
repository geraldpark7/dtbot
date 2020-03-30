class DTBotMessage:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Morning ya shmucks! :sunny: God said the DT group for today is ... :thinking_face:\n\n"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel, assignees):
        self.channel = channel
        self.username = "dt_bot"
        self.icon_emoji = ":bible:"

        assignment = ""
        for i in range(2):
            assignment = "@"
            assignment += assignees.pop(0) + " "
        assignment += ":smile\n\n"

        self.ASSIGNEES_BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    assignment
                ),
            },
        }

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                self.ASSIGNEES_BLOCK,
            ],
        }
