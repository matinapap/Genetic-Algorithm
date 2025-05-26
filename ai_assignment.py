import random

# Ορισμός των αποστάσεων
distances = [
    [0, 10, 20, 5, 10],
    [10, 0, 2, 10, 6],
    [20, 2, 0, 7, 1],
    [5, 10, 7, 0, 20],
    [10, 6, 1, 20, 0]
]

# Δημιουργία αρχικού πληθυσμού
def initial_population(pop_size):
    population = []
    for _ in range(pop_size):
        individual = list(range(2, 6)) # Δημιουργία λίστας πόλεων από 2 έως 5
        random.shuffle(individual) # Τυχαία ανακατεύουμε τη σειρά των πόλεων
        individual.insert(0, 1)  # Προσθήκη της πόλης 1 στην αρχή
        individual.append(1)     # Προσθήκη της πόλης 1 στο τέλος
        population.append(individual) # Προσθέτουμε την πλήρη διαδρομή στον πληθυσμό
    return population

# Υπολογισμός της συνολικής απόστασης μιας διαδρομής
def calculate_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        distance += distances[route[i] - 1][route[i + 1] - 1]  # Υπολογισμός απόστασης
    return distance

# Συνάρτηση καταλληλότητας
def fitness(route):
    return 1 / float(calculate_distance(route))

# Επιλογή γονέων
def selection(population, fitnesses):
    selected = random.choices(population, weights=fitnesses, k=2) # Tο weight επιλέγει με βάση την πιθανότητα (ρουλέτα) και το k δείχνει πόσοι γονείς θα επιλεγούν 
    return selected

# Αναπαραγωγή με διασταύρωση ενός σημείου
def crossover(par1, par2):
    start, end = sorted(random.sample(range(len(par1)), 2))  # Επιλέγονται δύο τυχαία σημεία από το χρωμόσωμα
    child = [0] * len(par1) # Δημιουργείται ένα κενό παιδί (με μηδενικά) 
    child[start:end] = par1[start:end]  # Αντιγράφεται τμήμα από τον πρώτο γονέα στο παιδί
    pointer = 0
    for i in range(len(par1)):
        if not par2[i] in child: # Εάν το στοιχείο του δεύτερου γονέα δεν υπάρχει ήδη στο παιδί
            while child[pointer] != 0: # Βρες το πρώτο κενό (0) σημείο στο παιδί
                pointer += 1
            child[pointer] = par2[i] # Αντιγραφή του στοιχείου από τον δεύτερο γονέα στο παιδί
    child[5] = 1 # Θέτουμε το τελευταίο στοιχείο του παιδιού ως 1
    return child

# Μετάλλαξη
def mutate(individual, mutation_rate):
    for i in range(1,4):
        if random.random() < mutation_rate: # Ελέγχει αν θα γίνει μετάλλαξη στην τρέχουσα θέση, με βάση το mutation_rate
            j = random.randint(1,4) # Επιλέγει τυχαία μια άλλη θέση από 1 έως 4 για την ανταλλαγή
            individual[i], individual[j] = individual[j], individual[i] # Ανταλλάσσει τις θέσεις i και j στην τρέχουσα διαδρομή (individual)
    return individual
                
# Γενετικός Αλγόριθμος
def genetic_algorithm(pop_size, generations, mutation_rate):
    # Δημιουργία αρχικού πληθυσμού
    population = initial_population(pop_size)
    # Επανάληψη για τον καθορισμένο αριθμό γενιών
    for _ in range(generations):
        # Υπολογισμός καταλληλότητας για κάθε άτομο στον πληθυσμό
        fitnesses = [fitness(individual) for individual in population]
        # Δημιουργία νέου πληθυσμού
        new_population = []
        # Δημιουργία νέων ατόμων μέχρι να φτάσουμε το μέγεθος του πληθυσμού
        for _ in range(pop_size):
            # Επιλογή δύο γονέων με βάση την καταλληλότητα
            par1, par2 = selection(population, fitnesses)
            # Δημιουργία νέου ατόμου με διασταύρωση των γονέων
            child = crossover(par1, par2)
            # Εφαρμογή μετάλλαξης στο νέο άτομο
            child = mutate(child, mutation_rate)
            # Προσθήκη του νέου ατόμου στον νέο πληθυσμό
            new_population.append(child)
        # Ανανέωση του πληθυσμού με το νέο πληθυσμό
        population = new_population
    # Εύρεση της καλύτερης διαδρομής στον τελικό πληθυσμό
    best_route = max(population, key=lambda x: fitness(x))
    # Επιστροφή της καλύτερης διαδρομής και της συνολικής απόστασής της
    return best_route, calculate_distance(best_route)

# Παράμετροι
pop_size = 10
generations = 5
mutation_rate = 0.2 #20% πιθανότητα μετάλλαξης

# Εκτέλεση του αλγορίθμου
best_route, best_distance = genetic_algorithm(pop_size, generations, mutation_rate)
print(f"Best route: {best_route}")
print(f"Best distance: {best_distance}")