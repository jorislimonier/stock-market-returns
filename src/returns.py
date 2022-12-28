from typing import Union
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


class Returns:
  def __init__(
    self,
    initial_inv: Union[float, int],
    monthly_inv: Union[float, int],
    rate: float,
    n_years: Union[float, int],
  ) -> None:
    self.initial_inv = initial_inv
    self.monthly_inv = monthly_inv
    self.rate = rate
    self.n_years = n_years
    self.monthly_factor = 1 + rate / 12
    self.n_months = 12 * n_years

    self._compute_finances()

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
