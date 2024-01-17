import csv

class Action:
    def __init__(self, name, cost, benefit_rate):
        self.name = name
        self.cost = cost
        self.benefit_rate = benefit_rate

    def calculate_benefits(self):
        # Les bénéfices sont calculés comme le produit du coût et du taux de bénéfice
        return int(self.cost * self.benefit_rate)

def read_actions_from_file(file_path):
    actions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            cost = float(row['price'])  # Maintenant en euros
            profit = float(row['profit'])
            benefit_rate = (profit / 100)
            if cost > 0:  # Filtre pour s'assurer que le coût est positif
                actions.append(Action(name, cost, benefit_rate))
    return actions

def sort_actions_by_efficiency(actions):
    for action in actions:
        action.efficiency = action.calculate_benefits() / action.cost
    return sorted(actions, key=lambda x: x.efficiency, reverse=True)

def select_actions(actions, budget):
    sorted_actions = sorted(actions, key=lambda x: (x.cost, -x.calculate_benefits() / x.cost), reverse=True)
    selected_actions = []
    total_cost = 0
    total_benefit = 0

    for action in sorted_actions:
        if total_cost + action.cost <= budget and action.calculate_benefits() > 0:
            selected_actions.append(action)
            total_cost += action.cost
            total_benefit += action.calculate_benefits()

    return selected_actions, total_benefit


file_path = 'sienna.csv'
# Utiliser la fonction
actions = read_actions_from_file(file_path)
budget = 500
best_portfolio, best_benefit = select_actions(actions, budget)
total_cost = sum(action.cost for action in best_portfolio)

# Afficher les résultats
print(f"Meilleur investissement avec un profit de {best_benefit:.2f}€ après 2 ans pour un investissment de {total_cost:.2f}:")
for action in best_portfolio:
    print(f"- {action.name} coûtant {action.cost:.2f}€ avec un bénéfice de {action.calculate_benefits():.2f}€")
    
# Créer un rapport au format CSV
report_file_path = 'investment_report.csv'

with open(report_file_path, 'w', newline='', encoding='utf-8') as report_file:
    writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Sienna bought:'])
    for action in best_portfolio:
        writer.writerow([action.name])
    writer.writerow([])
    writer.writerow([f'Total cost: {total_cost:.2f}€'])
    writer.writerow([f'Total return: {best_benefit:.2f}€'])

print(f"Le rapport a été enregistré sous le nom '{report_file_path}'.")