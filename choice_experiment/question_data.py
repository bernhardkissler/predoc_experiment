"""A file to collect all choices presented to the participant in one location. This could also be Excel/JSON etc.
"""


choices_data = {
    "choice_1": {
        "type": "simple",
        "number": 1,
        "prob_up": 55,
        "win_up": 20,
        "win_down": 5,
        "certain_pay": 10,
    },
    "choice_2": {
        "type": "simple",
        "number": 2,
        "prob_up": 70,
        "win_up": 20,
        "win_down": 5,
        "certain_pay": 9,
    },
    "choice_3": {
        "type": "simple",
        "number": 3,
        "prob_up": 85,
        "win_up": 20,
        "win_down": 5,
        "certain_pay": 8,
    },
    "choice_4": {
        "type": "list",
        "number": 4,
        "prob_up": 70,
        "win_up": 20,
        "win_down": 5,
        "lables_choice_list": [i for i in range(0, 22)],
    },
}
