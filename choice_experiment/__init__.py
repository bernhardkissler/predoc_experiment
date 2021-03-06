from os import stat
from otree.api import *
import random

c = Currency

doc = """
A minimal choice experiment; The question data is in an external file; 'Big' custom user interfaces are implemented as React components and kept in their own files for easy reuse. The whole experiment is implemented in one app to keep imports and participant.vars between apps to a minimum. Had it grown much larger, I would have probably broken it up into an intro part (WelcomePage --> ComprehensionPage), a main app (BinaryChoiceSimplePage & BinaryChoiceListPage) and a results app (PayoffPage), which would have allowed for an easier data set at the end. Still a short script should be sufficient to fix the empty fields caused by the round-mechanic.
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
    understanding_question_3 = models.IntegerField(
        label="Assume that the last round was selected to determine your bonus. The random offer is for one of the rows in which you indicated you would prefer Option B. How will your bonus be determined?",
        choices=[
            [1, "I receive Option A and the lottery is resolved randomly"],
            [2, "I receive Option B and my bonus is the 'offered' value."],
            [3, "I don't know"],
        ],
        widget=widgets.RadioSelect,
    )
    binary_choice_simple_choose_risky = models.BooleanField(
        choices=[[True, "Option A"], [False, "Option B"],],
        label="Which option do you choose?",
    )  # Encodes choosing the risky Option A as True and the certain Option B as False for easier storage
    binary_choice_list_choose_risky = (
        models.IntegerField()
    )  # Encodes the number of certain options (on the right side) for which the participant prefers the risky option


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
    form_fields = [
        "understanding_question_1",
        "understanding_question_2",
        "understanding_question_3",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        correct_check = (
            (player.understanding_question_1 == 1)
            and (player.understanding_question_2 == 2)
            and (player.understanding_question_3 == 2)
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
            pay_up=choices_data[f"choice_{player.round_number}"]["pay_up"],
            pay_down=choices_data[f"choice_{player.round_number}"]["pay_down"],
            pay_certain=choices_data[f"choice_{player.round_number}"]["pay_certain"],
            lables_choice_list=choices_data[f"choice_{player.round_number}"][
                "lables_choice_list"
            ],
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
            pay_up=choices_data[f"choice_{player.round_number}"]["pay_up"],
            pay_down=choices_data[f"choice_{player.round_number}"]["pay_down"],
            pay_certain=choices_data[f"choice_{player.round_number}"]["pay_certain"],
            lables_choice_list=choices_data[f"choice_{player.round_number}"][
                "lables_choice_list"
            ],
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        ## calculate payoff
        selected_round = random.randrange(4)  # randomly select a round
        player.participant.vars["selected_round"] = selected_round
        selected_choice = choices_data[f"choice_{selected_round + 1}"]
        player.participant.vars["selected_choice"] = selected_choice
        print(selected_choice)
        if selected_choice["type"] == "simple":
            if (
                player.in_round(selected_round + 1).binary_choice_simple_choose_risky
                == 0
            ):  # participant chose Option B
                chosen_text = "You chose the certain Option B."
                player.payoff = selected_choice["pay_certain"]
            else:  # Player chose Option A
                rnd_draw = random.randrange(1, 101)
                if rnd_draw <= selected_choice["prob_up"]:
                    chosen_text = (
                        "You chose the lottery Option A and won the higher bonus."
                    )
                    player.payoff = selected_choice["pay_up"]
                else:
                    chosen_text = (
                        "You chose the certain Option B and won the lower bonus."
                    )
                    player.payoff = selected_choice["pay_down"]
        elif selected_choice["type"] == "list":
            rnd_offer = random.choice(selected_choice["lables_choice_list"])
            player_offer = player.in_round(
                selected_round + 1
            ).binary_choice_list_choose_risky
            if (
                rnd_offer >= player_offer
            ):  # the random number is bigger than the biggest Option A - value in the price list ==> Receive Option B
                player.payoff = rnd_offer
                chosen_text = f"You chose the certain Option B if it was higher than ${player_offer}. An offer of ${rnd_offer} was randomly made meaning that you receive Option B."
            else:  # ==> Receive Option A (resolved like for simple question)
                rnd_draw = random.randrange(1, 101)
                if rnd_draw <= selected_choice["prob_up"]:
                    if player_offer > max(selected_choice["lables_choice_list"]):
                        chosen_text = f"You chose not to take Option B for any of the amounts meaning that you receive Option A. You won the higher bonus."
                    else:
                        chosen_text = f"You chose the certain Option B if it was higher than ${player_offer}. An offer of ${rnd_offer} was randomly made meaning that you receive Option A. You won the higher bonus."
                    player.payoff = selected_choice["pay_up"]
                else:
                    if player_offer > max(selected_choice["lables_choice_list"]):
                        chosen_text = f"You chose not to take Option B for any of the amounts meaning that you receive Option A. You won the lower bonus."
                    else:
                        chosen_text = f"You chose the certain Option B if it was higher than ${player_offer}. An offer of ${rnd_offer} was randomly made meaning that you receive Option A. You won the lower bonus."
                    player.payoff = selected_choice["pay_down"]
        print(player.payoff)
        player.participant.vars["chosen_text"] = chosen_text


class PayoffPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def vars_for_template(player: Player):
        correct_check = player.participant.vars["correct_check"]
        if correct_check:
            selected_choice = player.participant.vars["selected_choice"]
            selected_round = player.participant.vars["selected_round"]
            chosen_text = player.participant.vars["chosen_text"]

            res = {
                "chosen_text": chosen_text,
                "selected_round": selected_round + 1,
                "payoff": player.payoff,
                "round_type": selected_choice["type"],
                "correct_check": correct_check,
            }
        else:
            res = {
                "payoff": player.payoff,
                "correct_check": correct_check,
            }

        return res

    @staticmethod
    def js_vars(player: Player):
        correct_check = player.participant.vars["correct_check"]
        if correct_check:
            selected_choice = player.participant.vars["selected_choice"]

            res = dict(
                prob_up=selected_choice["prob_up"],
                pay_up=selected_choice["pay_up"],
                pay_down=selected_choice["pay_down"],
                pay_certain=selected_choice["pay_certain"],
                lables_choice_list=selected_choice["lables_choice_list"],
                round_type=selected_choice["type"],
            )
        else:
            res = dict()
        return res


page_sequence = [
    WelcomePage,
    InstructionsPage,
    ComprehensionPage,
    BinaryChoiceSimplePage,
    BinaryChoiceListPage,
    PayoffPage,
]
