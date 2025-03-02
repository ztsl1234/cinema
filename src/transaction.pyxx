from datetime import datetime
import logging

from utils import utils

logger = logging.getLogger(__name__)

class Transaction:
    def __init__(self, trn_date, trn_id, trn_type, amount, balance):
        self.trn_date = trn_date
        self.trn_id = trn_id
        self.trn_type = trn_type
        self.amount = amount
        self.balance = balance
      
    def print(self, print_balance:bool=True):
        
        balance_str=f"| {self.balance:7.2f}"

        if not print_balance:
            balance_str=""

        print(f"{self.trn_date.strftime("%Y%m%d")} | {self.trn_id:11} | {self.trn_type:4} | {self.amount:7.2f} {balance_str}")

  