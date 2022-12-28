from typing import Union

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_white"


class Finances:
  def __init__(
    self,
    initial_inv: Union[float, int],
    monthly_inv: Union[float, int],
    rate: float,
    n_years: Union[float, int],
  ) -> None:
    # Passed parameters
    self.initial_inv = initial_inv
    self.monthly_inv = monthly_inv
    self.rate = rate
    self.n_years = n_years

    # Computed parameters
    self.monthly_factor = 1 + rate / 12
    self.n_months = 12 * n_years

    self._compute_finances()
    self._compute_yearly_data()

  def _compute_finances(self) -> None:
    """
    Make financial computations, which include returns and investments
    given all parameters in __init__.
    """

    # Amount invested per month
    raw_investments = np.array(
      [self.initial_inv, *(self.n_months * [self.monthly_inv])]
    )
    investments = raw_investments.cumsum()

    # Monthly returns from monthly investments
    subseq_monthly_returns = [
      self.monthly_inv * self.monthly_factor**m for m in range(self.n_months)
    ]
    returns_monthly_inv = np.array([0] + subseq_monthly_returns)

    # Monthly returns from initial investment
    returns_initial_inv = [
      self.initial_inv * self.monthly_factor**m for m in range(self.n_months + 1)
    ]

    # Total returns
    returns = returns_monthly_inv.cumsum() + returns_initial_inv

    finances_dict = {
      "investments": investments,
      "returns": returns,
      "n_years": [m / 12 for m in range(self.n_months + 1)],
    }

    # Compute financial results
    self.finances = pd.DataFrame(finances_dict)

    # Compute total invested after `n_years`
    self.total_invested = self.finances.iloc[-1]["investments"]

    # Compute total returns after `n_years`
    self.total_return = self.finances.iloc[-1]["returns"]

  def _compute_yearly_data(self) -> None:
    is_complete_year = [m for m in range(len(self.finances)) if m % 12 == 0]
    yearly_finances = self.finances.loc[is_complete_year]
    yearly_finances["returns"] = yearly_finances["returns"].astype(int)
    yearly_finances["gain"] = yearly_finances["returns"] - yearly_finances["investments"]
    yearly_finances["yearly_returns"] = yearly_finances["returns"].diff().fillna(0).astype(int)
    self.yearly_finances = yearly_finances

  def plot_investments_vs_returns(self):

    var_names = ["monthly inv", "rate", "number of years", "total inv", "total return"]
    var_used = [
      f"{self.monthly_inv}€",
      f"{self.rate:.0%}",
      f"{self.n_years}",
      f"{self.total_invested:,.0f}€",
      f"{self.total_return:,.0f}€",
    ]

    title = ",   ".join([f"{name}: {v}" for name, v in zip(var_names, var_used)])

    fig = (
      px.line(
        data_frame=self.finances,
        x="n_years",
        y=["investments", "returns"],
        log_y=False,
        title=title,
        hover_data=["n_years"],
      )
      .update_xaxes(title="Years")
      .update_yaxes(title="Total return")
    )

    return fig
