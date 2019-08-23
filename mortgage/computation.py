from typing import List

from mortgage.mortgage import Mortgage


def compute_mortgage(periods: List[int],
                     interest_rates: List[float],
                     mortgage_amount: int,
                     mortgage_duration: int = 360,
                     name: str = 'Mortgage') -> Mortgage:
    """
    Compute the burden and monthly fees for the fixed interest periods for a mortgage.

    :param periods: fixed interest periods in months corresponding to the interest_rates.
    :param interest_rates: interest rates for the specified fixed periods in percentage, e.g. 2.1%.
    :param mortgage_amount: total loan amount in euro's.
    :param mortgage_duration: total duration of the mortgage in months, usually 360 months.
    :param name: optional name of the mortgage
    :return: mortgage object representing the total burden and monthly fees per fixed period.
    """

    interest_rates = [x / 100 for x in interest_rates]
    monthly_fees = []
    burden = 0
    remaining_amount = mortgage_amount

    if sum(periods) != mortgage_duration:
        print('ERROR: mortgage not possible')
        return Mortgage(mortgage_amount=0,
                        burden=0,
                        periods=[],
                        monthly_fees=[],
                        name='Impossible mortgage')

    for fixed_period, interest in zip(periods, interest_rates):
        monthly_interest = interest / 12
        if monthly_interest == 0:
            annuity = remaining_amount / mortgage_duration
            repayment_fixed_period = annuity * fixed_period
        else:
            annuity = (monthly_interest / (1 - ((1 + monthly_interest) ** -mortgage_duration))
                       ) * remaining_amount
            first_repayment = annuity - remaining_amount * monthly_interest
            reason = monthly_interest + 1
            repayment_fixed_period = first_repayment * (reason ** fixed_period - 1) / (reason - 1)

        monthly_fees.append(annuity)
        burden += annuity * fixed_period
        remaining_amount -= repayment_fixed_period
        mortgage_duration -= fixed_period

    return Mortgage(mortgage_amount=mortgage_amount,
                    burden=burden,
                    periods=periods,
                    monthly_fees=monthly_fees,
                    name=name)
