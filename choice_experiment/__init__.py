from os import stat
from otree.api import *
import random

c = Currency

doc = """
Your app description
"""

from choice_experiment.question_data import choices_data


class Constants(BaseConstants):
    name_in_url = "choice_experiment"
    players_per_group = None
    num_rounds = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    understanding_question_1 = models.IntegerField(
        label="On how many of your choices does your final bonus directly depend?"
    )
    understanding_question_2 = models.IntegerField(
        label="How many options will you be offered during the first 3 rounds?"
    )
    binary_choice_simple_choose_risky = models.BooleanField(
        choices=[[True, "Option A"], [False, "Option B"],],
        label="What certain amount do you choose?",
    )  # Encodes choosing the risky option A as True and the safe option B as False for easier storage
    binary_choice_list_choose_risky = (
        models.IntegerField()
    )  # Encodes the number of safe options (on the right side) for which the participant prefers the risky option


# PAGES
class WelcomePage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class InstructionsPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ComprehensionPage(Page):
    form_model = "player"
    form_fields = ["understanding_question_1", "understanding_question_2"]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_check = (player.understanding_question_1 == 1) and (
            player.understanding_question_2 == 2
        )
        player.participant.vars["correct_check"] = correct_check


class BinaryChoiceSimplePage(Page):
    form_model = "player"
    form_fields = ["binary_choice_simple_choose_risky"]

    @staticmethod
    def is_displayed(player):
        return (player.participant.vars["correct_check"]) and (
            player.round_number in [1, 2, 3]
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            prob_up=choices_data[f"choice_{player.round_number}"]["prob_up"],
            prob_down=100 - choices_data[f"choice_{player.round_number}"]["prob_up"],
            pay_up=choices_data[f"choice_{player.round_number}"]["pay_up"],
            pay_down=choices_data[f"choice_{player.round_number}"]["pay_down"],
            pay_certain=choices_data[f"choice_{player.round_number}"]["pay_certain"],
        )


class BinaryChoiceListPage(Page):
    form_model = "player"
    form_fields = ["binary_choice_list_choose_risky"]

    @staticmethod
    def is_displayed(player):
        return (player.participant.vars["correct_check"]) and (
            player.round_number in [4]
        )

    @staticmethod
    def error_message(player, values):
        if values["binary_choice_list_choose_risky"] == -9999:
            return "Please enter your preferences before trying to proceed."

    @staticmethod
    def js_vars(player: Player):
        return dict(
            prob_up=choices_data[f"choice_{player.round_number}"]["prob_up"],
            prob_down=100 - choices_data[f"choice_{player.round_number}"]["prob_up"],
            pay_up=choices_data[f"choice_{player.round_number}"]["pay_up"],
            pay_down=choices_data[f"choice_{player.round_number}"]["pay_down"],
            lables_choice_list=choices_data[f"choice_{player.round_number}"][
                "lables_choice_list"
            ],
        )


class PayoffPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def vars_for_template(player: Player):
        selected_round = random.randrange(4)  # randomly select a round
        selected_choice = choices_data[f"choice_{selected_round + 1}"]
        print(selected_choice)
        if selected_choice["type"] == "simple":
            if (
                player.in_round(selected_round + 1).binary_choice_simple_choose_risky
                == 0
            ):  # participant chose Option A
                player.payoff = selected_choice["pay_certain"]
            else:  # Player chose Option B
                rnd_draw = random.randrange(1, 101)
                if rnd_draw <= selected_choice["prob_up"]:
                    player.payoff = selected_choice["pay_up"]
                else:
                    player.payoff = selected_choice["pay_down"]
        elif selected_choice["type"] == "list":
            rnd_offer = random.choice(selected_choice["lables_choice_list"])
            if (
                rnd_offer
                >= player.in_round(selected_round + 1).binary_choice_list_choose_risky
            ):  # the random number is bigger than the biggest Option A - value in the price list ==> Receive Option B
                player.payoff = rnd_offer
            else:  # ==> Receive Option A (resolved like for simple question)
                rnd_draw = random.randrange(1, 101)
                if rnd_draw <= selected_choice["prob_up"]:
                    player.payoff = selected_choice["pay_up"]
                else:
                    player.payoff = selected_choice["pay_down"]
        print(player.payoff)
        return {"selected_round": selected_round + 1, "payoff": player.payoff}


page_sequence = [
    WelcomePage,
    InstructionsPage,
    ComprehensionPage,
    BinaryChoiceSimplePage,
    BinaryChoiceListPage,
    PayoffPage,
]
