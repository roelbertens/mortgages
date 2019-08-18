from typing import List

import matplotlib.pyplot as plt
import numpy as np

from mortgage.computation import compute_mortgage


def plot_interest_scenarios(periods: List[int],
                            interest_rates: List[float],
                            future_interest_rate_min: float,
                            future_interest_rate_max: float,
                            mortgage_amount: int,
                            mortgage_duration: int = 360,
                            name: str = 'Mortgage') -> plt.axes:
    """
    Plot the total burden and monthly fees for different future interest rates.

    Specify your mortgage except for the interest rate of the last period.
    Also specify the range of future interest rates you want to consider.

    :param periods: all periods for your mortgage
    :param interest_rates: interest rate for each period except for the last period
    :param future_interest_rate_min: lowest future interest rate for last period
    :param future_interest_rate_max: highest future interest rate for last period
    :param mortgage_amount: total mortgage amount
    :param mortgage_duration: duration of mortgage (months)
    :param name: optional name of the mortgage
    :return: the axes of the plot
    """
    step_size = .5
    future_interest_rates = np.arange(future_interest_rate_min, future_interest_rate_max, step_size)

    mortgages = [compute_mortgage(periods=periods,
                                  interest_rates=interest_rates + [future_interest],
                                  mortgage_amount=mortgage_amount,
                                  mortgage_duration=mortgage_duration,
                                  name=name)
                 for future_interest in future_interest_rates]

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    burdens = [mortgage.burden - mortgages[0].burden for mortgage in mortgages]
    ax.barh(y=future_interest_rates,
            height=-step_size/2,
            width=burdens,
            color='purple',
            align='edge')
    ax.set_ylabel('Future interest rate (%)\n', fontsize=14)
    ax.set_xlabel(f'\nIncrease in mortgage burden (compared to {future_interest_rate_min}%)',
                  color='purple', fontsize=14)
    ax.set_title('Compare additional burden and monthly fee\nwith growing future interest rates\n',
                 fontsize=18)

    fees = [mortgage.monthly_fees[-1] - mortgages[0].monthly_fees[-1] for mortgage in mortgages]
    ax2 = ax.twiny()
    ax2.barh(y=future_interest_rates,
             height=step_size/2,
             width=fees,
             color='darkblue',
             align='edge')
    ax2.set_xlabel(f'Increase in monthly fee (compared to {future_interest_rate_min}%)\n',
                   color='darkblue', fontsize=14)

    x1_shift, x2_shift = max(burdens) / len(burdens) / 4, max(fees) / len(fees) / 4
    for y, x1, x2 in zip(future_interest_rates, burdens, fees):
        ax.annotate(x1, xy=(x1 + x1_shift, y - .3 * step_size), rotation=0, color="purple")
        ax2.annotate(x2, xy=(x2 + x2_shift, y + .1 * step_size), rotation=0, color="darkblue")

    plt.yticks(future_interest_rates)
    plt.tight_layout()
    return ax
