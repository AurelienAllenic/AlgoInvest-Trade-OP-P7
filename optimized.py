import csv


class Action:
    def __init__(self, name, cost, profit_percentage):
        self.name = name
        self.cost = cost
        self.profit_percentage = profit_percentage
        self.real_return = self.calculate_real_return()
        self.return_on_cost = self.calculate_return_on_cost()

    def calculate_real_return(self):
        return self.cost * (self.profit_percentage / 100)

    def calculate_return_on_cost(self):
        return self.real_return / self.cost if self.cost != 0 else 0


def read_actions_from_file(file_path):
    actions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            cost = float(row['price'])
            profit_percentage = float(row['profit'])
            if cost > 0:
                actions.append(Action(name, cost, profit_percentage))
    return actions


def select_actions(actions, budget):
    s_actions = sorted(actions, key=lambda x: x.return_on_cost, reverse=True)
    selected_actions = []
    total_cost = 0
    total_real_return = 0

    for action in s_actions:
        if total_cost + action.cost <= budget:
            selected_actions.append(action)
            total_cost += action.cost
            total_real_return += action.real_return

    return selected_actions, total_real_return, total_cost


file_path = 'sienna2.csv'
actions = read_actions_from_file(file_path)
budget = 500
best_portfolio, best_benefit, total_cost = select_actions(actions, budget)

# Afficher les résultats
msg = (f"Meilleur investissement avec un retour réel de "
       f"{best_benefit:.2f}€ pour un investissement de {total_cost:.2f}€:")
print(msg)


for action in best_portfolio:
    print(f"- {action.name} coûtant {action.cost:.2f}€ avec un retour "
          f"réel de {action.real_return:.2f}€")


# Créer un rapport au format CSV
report_file_path = 'investment_report.csv'

with open(report_file_path, 'w', newline='', encoding='utf-8') as report_file:
    writer = csv.writer(report_file, delimiter=',', quotechar='"',
                        quoting=csv.QUOTE_MINIMAL)
    if file_path == 'actions.csv':
        writer.writerow(['Actions bought:'])
    else:
        writer.writerow(['Sienna bought:'])
    for action in best_portfolio:
        writer.writerow([action.name])
    writer.writerow([])
    writer.writerow([f'Total cost: {total_cost:.2f}€'])
    writer.writerow([f'Total return: {best_benefit:.2f}€'])

print(f"Le rapport a été enregistré sous le nom '{report_file_path}'.")
