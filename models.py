from dataclasses import dataclass

@dataclass
class Expense :
    id : int
    name : str
    amount : float