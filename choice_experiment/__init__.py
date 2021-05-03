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
    pass


# PAGES
class WelcomePage(Page):
    pass


class InstructionsPage(Page):
    pass


class ComprehensionPage(Page):
    pass


class BinaryChoiceSimplePage(Page):
    pass


class BinaryChoiceListPage(Page):
    pass


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
