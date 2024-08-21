from dataclasses import dataclass
from pathlib import Path

from entities import BalanceEntity, Balance, AddScenarioEntity, RegisterEntity, DepositEntity, BetEntity


@dataclass
class CasinoCore:
    input_dir: Path
    input_file_name: str
    output_file_name: str
    verbose: bool = False

    def __post_init__(self) -> None:
        input_file = self.input_dir / self.input_file_name
        output_file = self.input_dir / self.output_file_name
        with open(input_file, 'r') as f:
            self.commands = f.readlines()

        if output_file.exists():
            output_file.unlink()

        self.users: dict[str, Balance] = dict()
        self.campaigns: list[AddScenarioEntity] = list()

    def __call__(self) -> None:
        self.process_commands()

    def process_commands(self) -> None:
        bet_number = 0
        for command_str in self.commands:
            try:
                splits = command_str.split()
                command = splits[0]
                if command == "register":
                    self.register_user(RegisterEntity(name=command, user_id=splits[1]))
                elif command == "addscenario":
                    self.add_scenario(
                        AddScenarioEntity(name=command, prize_1=float(splits[1]), prize_2=float(splits[2]),
                                          prize_3=float(splits[3])))
                elif command == "deposit":
                    self.deposit(DepositEntity(name=command, user_id=splits[1], amount=float(splits[2])))
                elif command == "bet":
                    bet_number += 1
                    self.bet(BetEntity(name=command, user_id=splits[1], game=splits[2], amount=float(splits[3])),
                             is_winning=bool(bet_number % 2))
                elif command == "balance":
                    _ = self.balance(BalanceEntity(name=command, user_id=splits[1]))
                else:
                    print(f"Unsupported command: {command}")
            except Exception as e:
                print("This command is not processable", e)

            if self.verbose:
                print(f"Current balances: {self.users}")

    def register_user(self, register_entity: RegisterEntity) -> None:
        if self.verbose:
            print(register_entity)
        self.users[register_entity.user_id] = Balance()

    def add_scenario(self, add_scenario_entity: AddScenarioEntity) -> None:
        if self.verbose:
            print(add_scenario_entity)
        self.campaigns.append(add_scenario_entity)

    def deposit(self, deposit_entity: DepositEntity) -> None:
        if self.verbose:
            print(deposit_entity)
        user_id = deposit_entity.user_id
        amount = deposit_entity.amount
        self.users[user_id].total += amount
        self.users[user_id].deposit_total += amount

    def bet(self, bet_entity: BetEntity, is_winning: bool) -> None:
        if self.verbose:
            print(bet_entity, is_winning)
        game = bet_entity.game
        user_id = bet_entity.user_id
        amount = bet_entity.amount
        current_balance = self.users[user_id].total
        if amount > current_balance:
            if self.verbose:
                print(f"{user_id} cannot place bet with amount: {amount} because his balance is: {current_balance}")
            return

        self.users[user_id].total -= amount
        if game == "Slots":
            self.users[user_id].slot_total += amount

        if is_winning:
            self.users[user_id].total += 2 * amount

        if len(self.campaigns) == 0:
            if self.verbose:
                print("No campaigns left :(")
            return
        current_campaign = self.campaigns[0]
        deposit_balance = self.users[user_id].deposit_total
        slot_balance = self.users[user_id].slot_total
        total_won = self.users[user_id].total_won
        if total_won == 3:
            return
        if deposit_balance >= 1000 and slot_balance >= 500 and total_won == 2:
            self.users[user_id].total += current_campaign.prize_3
            self.campaigns.pop(0)
            self.users[user_id].total_won += 1
            self.users[user_id].slot_total = 0
            self.users[user_id].deposit_total = 0
        elif deposit_balance >= 500 and slot_balance >= 250 and total_won == 1:
            self.users[user_id].total += current_campaign.prize_2
            self.campaigns.pop(0)
            self.users[user_id].total_won += 1
            self.users[user_id].slot_total = 0
            self.users[user_id].deposit_total = 0
        elif deposit_balance >= 100 and slot_balance >= 50 and total_won == 0:
            self.users[user_id].total += current_campaign.prize_1
            self.campaigns.pop(0)
            self.users[user_id].total_won += 1
            self.users[user_id].slot_total = 0
            self.users[user_id].deposit_total = 0
        else:
            if self.verbose:
                print("No campaign for you :(")

    def balance(self, balance_entity: BalanceEntity) -> float:
        if self.verbose:
            print(balance_entity)
        current_balance = self.users[balance_entity.user_id].total
        with open(self.input_dir / self.output_file_name, 'a') as f:
            f.write(str(current_balance) + "\n")
        return current_balance
