from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = "choice_experiment"
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    binary_choice_simple_choose_risky = models.BooleanField(
        choices=[[True, "Option A"], [False, "Option B"],],
        label="What certain amount do you choose?",
    )  # Encodes choosing the risky option A as True and the safe option B as False for easier storage
    binary_choice_list_choose_risky = (
        models.IntegerField()
    )  # Encodes the number of safe options (on the right side) for which the participant prefers the risky option


# PAGES
class WelcomePage(Page):
    pass


class InstructionsPage(Page):
    pass


class ComprehensionPage(Page):
    pass


class BinaryChoiceSimplePage(Page):
    form_model = "player"
    form_fields = ["binary_choice_simple_choose_risky"]


class BinaryChoiceListPage(Page):
    form_model = "player"
    form_fields = ["binary_choice_list_choose_risky"]

    @staticmethod
    def error_message(player, values):
        if values["binary_choice_list_choose_risky"] == -9999:
            return "Please enter your preference before trying to proceed."


class PayoffPage(Page):
    pass


page_sequence = [
    WelcomePage,
    InstructionsPage,
    ComprehensionPage,
    BinaryChoiceSimplePage,
    BinaryChoiceListPage,
    PayoffPage,
]
