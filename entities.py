from dataclasses import dataclass


@dataclass
class RegisterEntity:
    name: str
    user_id: str


@dataclass
class AddScenarioEntity:
    name: str
    prize_1: float
    prize_2: float
    prize_3: float


@dataclass
class DepositEntity:
    name: str
    user_id: str
    amount: float


@dataclass
class BetEntity:
    name: str
    user_id: str
    game: str
    amount: float


@dataclass
class BalanceEntity:
    name: str
    user_id: str


@dataclass
class Balance:
    total: float = 0
    slot_total: float = 0
    casino_total: float = 0
    sport_total: float = 0
    deposit_total: float = 0
    total_won: int = 0
