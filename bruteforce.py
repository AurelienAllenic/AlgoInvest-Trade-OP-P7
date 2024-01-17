import itertools
import csv

class Client:
    def __init__(self, user_id):
        self.user_id = user_id
        self.wallet = 500
        self.owned_actions = []

    def buy_action(self, action):
        if self.wallet >= action.cost and not action.is_bought:
            self.wallet -= action.cost
            action.mark_as_bought()
            self.owned_actions.append(action)
            print(f"Action {action.name} achetée pour {action.cost}€, bénéfice attendu dans 2 ans: {action.calculate_benefits()}€")
        else:
            print(f"Impossible d'acheter l'action {action.name}. Vérifiez si vous avez suffisamment d'argent ou si l'action est déjà achetée.")

        best_profit = 0
        best_portfolio = None

        # Explore toutes les combinaisons d'actions possibles
        for r in range(1, len(actions) + 1):
            for subset in itertools.combinations(actions, r):
                total_cost = sum(action.cost for action in subset)
                total_benefit = sum(action.calculate_benefits() for action in subset)

                # Vérifie si cette combinaison est meilleure que la meilleure trouvée jusqu'à présent
                if total_cost <= self.wallet and total_benefit > best_profit:
                    best_profit = total_benefit
                    best_portfolio = subset

        return best_portfolio, best_profit
    
class Action:
    def __init__(self, name, cost, benefit_rate):
        self.name = name
        self.cost = cost
        self.benefit_rate = benefit_rate
        self.is_bought = False

    def mark_as_bought(self):
        self.is_bought = True

    def calculate_benefits(self):
        return self.cost * self.benefit_rate
    
def read_actions_from_file(file_path):
    actions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            cost = float(row['price'])
            profit = float(row['profit'])
            benefit_rate = (profit / 100)
            actions.append(Action(name, cost, benefit_rate))
    return actions

def find_best_investment(actions, budget):
    best_profit = 0
    best_portfolio = None

    for r in range(1, len(actions) + 1):
        for subset in itertools.combinations(actions, r):
            total_cost = sum(action.cost for action in subset)

            # Continue seulement si le coût total est dans le budget
            if total_cost <= budget:
                total_benefit = sum(action.calculate_benefits() for action in subset)

                if total_benefit > best_profit:
                    best_profit = total_benefit
                    best_portfolio = subset

    return best_portfolio, best_profit


actions = read_actions_from_file('sienna.csv')

# Création d'un client
client = Client("user123")

# Évaluation des meilleurs investissements
best_investment, best_investment_profit = find_best_investment(actions, client.wallet)

# Affichage des résultats
if best_investment:
    print(f"Meilleur investissement avec un profit de {best_investment_profit} euros après 2 ans:")
    for action in best_investment:
        print(f"- {action.name} coûtant {action.cost} euros avec un bénéfice de {action.calculate_benefits()} euros")
else:
    print("Aucun investissement possible avec le budget actuel.")