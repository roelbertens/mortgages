from typing import List

import matplotlib.pyplot as plt


class Mortgage:
    """
    A mortgage overview of the total burden (incl. interest) and the monthly fees per fixed period
    """

    def __init__(self, mortgage_amount, burden, periods, monthly_fees, name):
        self.mortgage_amount = int(mortgage_amount)
        self.burden = int(burden)
        self.periods = periods.copy()
        self.monthly_fees = [int(fee) for fee in monthly_fees]
        self.name = name


    def __add__(self, other):
        if not other:
            return self
        mortgage_amount = self.mortgage_amount + other.mortgage_amount
        burden = self.burden + other.burden
        periods, monthly_fees = _align_mortgages(periods_a=self.periods,
                                                 periods_b=other.periods,
                                                 fees_a=self.monthly_fees,
                                                 fees_b=other.monthly_fees)
        name = self.name
        if other.name != self.name:
            name += ' & ' + other.name
        return Mortgage(mortgage_amount=mortgage_amount,
                        burden=burden,
                        periods=periods,
                        monthly_fees=monthly_fees,
                        name=name)

    def __radd__(self, other):
        return self + other

    def __repr__(self):
        text = (f'{self.name}: {format(self.mortgage_amount, ",d")} euro\n'
                f'Total burden: {format(self.burden, ",d")} euro\n'
                'Monthly fees:\n')
        for period, fee in zip(self.periods, self.monthly_fees):
            text += f'- {period} months: {fee} euro\'s\n'
        return text

    def plot(self, axes=None) -> plt.axes:
        if axes is None:
            fig, axes = plt.subplots(2, 1, figsize=(5, 8))
        nr_periods = len(self.periods)
        axes[0].bar(x=range(nr_periods), height=self.monthly_fees, tick_label=self.periods,
                    color='darkblue')
        axes[0].set_xlabel('Period (months)')
        axes[0].set_ylabel('Monthly fee\n', color='darkblue')
        axes[0].set_title(f'Subsequent monthly fees\nover the specified periods\n\n{self}\n')

        axes[1].bar(x=[0, 1], height=[self.mortgage_amount, self.burden], color='purple')
        axes[1].set_ylabel('\nAmount (euro)', color='purple')
        axes[1].set_xlabel('')
        axes[1].set_xticks([0, 1])
        axes[1].set_xticklabels([f'Mortgage\n{format(self.mortgage_amount, ",d")}',
                                 f'Total burden\n{format(self.burden, ",d")}'])

        plt.tight_layout()
        return axes

    def compare(self, others: list) -> plt.axes:
        mortgages = others + [self]
        nr_mortgages = len(mortgages)
        fig, axes = plt.subplots(2, nr_mortgages, figsize=(nr_mortgages * 3, 8), sharey='row')
        for col_axes, mortgage in zip(axes.T, mortgages):
            mortgage.plot(axes=col_axes)
        plt.tight_layout()
        return axes


def _align_mortgages(periods_a: List[int],
                     periods_b: List[int],
                     fees_a: List[int],
                     fees_b: List[int]) -> (List[int], List[int]):
    """ Align periods and fees of two mortgages and compute the exact fee for each period.

    :param periods_a: periods for Mortgage a
    :param periods_b: periods for Mortgage b
    :param fees_a: monthly fees for Mortgage a
    :param fees_b: monthly fees for Mortgage b
    :return: tuple of aligned periods and fees for the combined Mortgages a and b
    """
    periods_a, periods_b, fees_a, fees_b = \
        periods_a.copy(), periods_b.copy(), fees_a.copy(), fees_b.copy()

    if not periods_a:
        if not periods_b:
            return [], []
        else:
            return periods_b, fees_b
    elif not periods_b:
        return periods_a, fees_a

    if periods_b[0] < periods_a[0]:
        periods_a, periods_b = periods_b, periods_a
        fees_a, fees_b = fees_b, fees_a

    first_period_fee = ([periods_a[0]], [fees_a[0] + fees_b[0]])

    if periods_a[0] == periods_b[0]:
        recursive_result = _align_mortgages(periods_a[1:], periods_b[1:], fees_a[1:], fees_b[1:])
    else:
        periods_b[0] -= periods_a[0]
        recursive_result = _align_mortgages(periods_a[1:], periods_b, fees_a[1:], fees_b)

    return tuple(a + b for a, b in zip(first_period_fee, recursive_result))
