import random
import time

# Population Initialization using random initialization
def population_initialization(population_size, N):
    #initialize population with an empty list
    population = []
    
    # Random permutation from 1 to N 
    for i in range(population_size):
        candidate = random.sample(range(1, N + 1), N) 
        population.append(candidate)        
        
    return population

# Calculate the fitness function of candidate solution
def fitness_function(candidate):
    
    n = len(candidate)
    # Combinatorics formula for maximum non attacking pairs
    maximum_pairs = n * (n - 1) // 2   
    
    # Find diagonal conflicts 
    diagonal_conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(candidate[i] - candidate[j]) == abs(i - j):
                diagonal_conflicts += 1
    fitness = maximum_pairs - diagonal_conflicts
    
    return fitness

# Tournament selection to choose parents
def tournament_selection(population, tournament_size):
    
    #random sampling of candidates from the population
    tournament = random.sample(population, tournament_size)
    max_fitness = 0
    selected_candidate = []
    
    # Select the candidate with the highest fitness function from the selected candidates
    for i in range(len(tournament)):
        fitness = fitness_function(tournament[i])
        if fitness>max_fitness:
            max_fitness = fitness
            selected_candidate = tournament[i]
    
    return selected_candidate

# Crossover functions (pmx/ox/cx)
def crossover(parent1,parent2,crossover_type):
    
    N = len(parent1)
    
    # Intialize temporary offsprings with None values
    child1 = [None]*N
    child2 = [None]*N
    
    if crossover_type == "pmx" or crossover_type == "ox":
        
        point1 = random.randint(1,N-2)
        point2 = random.randint(point1+1, N-1)
        
        child1[point1:point2 + 1] = parent1[point1:point2 + 1]
        child2[point1:point2 + 1] = parent2[point1:point2 + 1]
        
        if crossover_type == 'pmx':
            
            # Partially mapped crossover
            def pmx_crossover(child,parent, point1,point2):
                for i in range(N):
                    temp = parent[i]
                    if i<point1 or i>point2:
                        if parent[i] not in child[point1:point2+1]:
                            child[i] = temp
                        else:
                            while temp in child[point1:point2+1]:
                                mapped_index = child.index(temp)
                                temp = parent[mapped_index]
                            child[i] = temp
                return child

            # Map and fill the values in both children
            child1 = pmx_crossover(child1,parent2,point1,point2)
            child2 = pmx_crossover(child2,parent1,point1,point2)
            
        elif crossover_type == 'ox':
            # Ordered crossover
            def ox_crossover(child,parent,point2):
                #Filling starts from the gene after point 2 and goes in a cycle
                fill_point = (point2 + 1) % N
                for gene in parent:
                    if gene not in child:
                        child[fill_point] = gene
                        fill_point = (fill_point + 1) % N
                return child
            #Map and fill the values in both children
            child1 = ox_crossover(child1,parent2,point2)
            child2 = ox_crossover(child2,parent1,point2)  
            
    elif crossover_type == "cx":
        
        # Cycle crossover
        def cycle_crossover(child, parent1, parent2):
            #Find the cycle
            cycle_values = []
            start = 0
            
            current_point = start
            while current_point not in cycle_values:
                cycle_values.append(current_point)
                current_value = parent1[current_point]
                current_point = parent2.index(current_value)
            
            # For values in cycle, copy the values as such in first parent
            for i in cycle_values:
                child[i] = parent1[i]
            
            # Fill the remaining values from the second parent
            for i in range(N):
                if child[i] is None:
                    child[i] = parent2[i]
            return child
        
        child1 = cycle_crossover(child1,parent1,parent2)
        child2 = cycle_crossover(child2,parent2,parent1)
        
    return child1,child2
        
# Mutation Functions (swap/inversion)
def mutation(child, mutation_rate,mutation_type):
    
    # Compare with mutation rate to avoid unnecessary randomness and increase algorithm efficiency
    if random.random() < mutation_rate:
        # Swap mutation
        if mutation_type == 'swap':
            i, j = random.sample(range(len(child)), 2)
            child[i], child[j] = child[j], child[i]
            
        # Inversion mutation  
        elif mutation_type == 'inversion':
            mutated_child = child[:]
            length = len(mutated_child)
            start = random.randint(0, length-1) 
            end = random.randint(start+1,length)
            mutated_child[start:end] = reversed(mutated_child[start:end])
            child = mutated_child
        
    return child 

# Main genetic algorithm function
def genetic_algorithm(N, population_size, generations, tournament_size, crossover_type, mutation_rate, mutation_type):
    
    population = population_initialization(population_size,N)
    
    for generation in range(1,generations+1):
        new_population = []
        
        for i in range(population_size//2):
            
            # Select two parents using tournament selection
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)
            
            # Crossover between the parents to produce the two children
            child1, child2 = crossover(parent1, parent2, crossover_type) 
            
            # Mutate the children
            child1 = mutation(child1, mutation_rate,mutation_type)
            child2 = mutation(child2, mutation_rate,mutation_type)
            
            # Add the new children to the next generation
            new_population.extend([child1,child2])
        
        # Update the population with new generation    
        population = new_population
        
        # Find the candidate with the best fitness in the current generation
        best_candidate = max(population, key = fitness_function)
        best_candidate_fitness = fitness_function(best_candidate)
        
        # Check if the best candidate's fitness is an optimal ftness
        if best_candidate_fitness == N*(N-1)//2:
            print("Solution found in generation", generation," using",crossover_type," crossover and", mutation_type," mutation.\nBest candidate is",best_candidate)
            return best_candidate,generation 
    
    #if no solution is found after all the given generations
    best_candidate = max(population, key=fitness_function)
    print("No optimal solution found.\nBest solution after", generation, "is ", best_candidate)
    return best_candidate,generation


# Function to get the parameters for genetic algorithm function as user input
def get_user_input():
    
    N= int(input("Enter the number of Queens:"))
    population_size = int(input("Enter the population size:"))
    generations = int(input("Enter the number of generations:"))
    tournament_size = int(input("Enter the tournament size:"))
    crossover_type = input("Enter the crossover type(pmx/ox/cx):")
    mutation_rate = float(input("Enter the mutation_rate:"))
    mutation_type = input("Enter the mutation type(swap/inversion):")

    return N, population_size, generations, tournament_size,crossover_type, mutation_rate, mutation_type 

#Write the final solution in a notepad
def write_to_textfile(N, population_size,generations,tournament_size,crossover_type,mutation_rate,mutation_type,solution,generation,runtime):
    
    with open("final solution.txt", "w") as file:
        file.write(f"N ={N}\n"
                   f"Population size = {population_size}\n"
                   f"Generations = {generations}\n"
                   f"Tournament size = {tournament_size}\n"
                   f"Mutation rate = {mutation_rate}\n"
                   f"Mutation type = {mutation_type}\n"
                   f"Type of crossover = {crossover_type}\n"
                   f"Solution: {solution}\n"
                   f"Generation of Solution:{generation}\n"
                   f"Runtime of the Algorithm: {runtime}")      

# Get user input
N, population_size, generations, tournament_size, crossover_type, mutation_rate, mutation_type = get_user_input()

# Run the program and find the runtime
start = time.time()
solution, generation = genetic_algorithm(N, population_size, generations, tournament_size, crossover_type, mutation_rate, mutation_type)
end = time.time()
runtime = end - start
print("Algorith run time is", runtime,"seconds")

# Write the output to a text file
write_to_textfile(N, population_size, generations,tournament_size,crossover_type,mutation_rate,mutation_type,solution,generation, runtime)          