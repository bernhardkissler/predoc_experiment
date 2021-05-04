"""A file to collect all choices presented to the participant in one location. This could also be Excel/JSON etc. The idea is to make it easy to add new questions and extend the experiment without changing the main code apart from round_numbers
"""


choices_data = {
    "choice_1": {
        "number": 1,
        "type": "simple",
        "prob_up": 55,
        "pay_up": 20,
        "pay_down": 5,
        "pay_certain": 10,
        "lables_choice_list": [0],
    },
    "choice_2": {
        "number": 2,
        "type": "simple",
        "prob_up": 70,
        "pay_up": 20,
        "pay_down": 5,
        "pay_certain": 9,
        "lables_choice_list": [0],
    },
    "choice_3": {
        "number": 3,
        "type": "simple",
        "prob_up": 85,
        "pay_up": 20,
        "pay_down": 5,
        "pay_certain": 8,
        "lables_choice_list": [0],
    },
    "choice_4": {
        "number": 4,
        "type": "list",
        "prob_up": 70,
        "pay_up": 20,
        "pay_down": 5,
        "pay_certain": 0,
        "lables_choice_list": [i for i in range(0, 22)],
    },
}
