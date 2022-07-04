from random import randint, choices, randrange, random, choice
import bisect
#  Generate 0
def generate_pop0(num_item, num_genomes, random_gen): # eric
    genomes = []
    if random_gen:
        for i in range(num_genomes):
            cur_genome = ""
            for j in range(num_item):
                cur_genome += str(randint(0,1))
            genomes.append(cur_genome)
        return genomes
    else:
        index_now = -1
        for i in range(num_genomes):
            cur_genome = ""
            index_now += 1
            for j in range(num_item):
                if j == index_now:
                    cur_genome += "1"
                else:
                    cur_genome += "0"
            genomes.append(cur_genome)
        return genomes

def fitness(list_barang, max_price, genome): # wendy
    total_fitness = 0
    total_price = 0
    for i in range(len(genome)):
        if total_price <= max_price:
            if genome[i] == "1":
                total_fitness += list_barang[i].num_buyers
                total_price += list_barang[i].price
        if total_price > max_price:
            total_fitness = 0
            break
    return total_fitness

def count_cumulative(weights): # jeremy
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def special_choice(population, cum_weights): # jeremy
    x = random()
    idx = bisect.bisect(cum_weights, x) #binary search
    return [population[idx], idx]

def selection_pair(genome_pop, list_barang, max_price): #eric
    fitness_without_zero = []
    genome_pop_without_zero_fitness = []
    num_fit_more_than_0 = 0
    save_genome_one_fit_more_than_0 = -1
    save_genome_two_fit_more_than_0 = -1
    for i in range(len(genome_pop)):
        fit = fitness(list_barang, max_price, genome_pop[i])
        if fit > 0:
            fitness_without_zero.append(fit)
            genome_pop_without_zero_fitness.append(genome_pop[i])
            num_fit_more_than_0 += 1
            if save_genome_one_fit_more_than_0 == -1:
                save_genome_one_fit_more_than_0 = genome_pop[i]
            else:
                save_genome_two_fit_more_than_0 = genome_pop[i]
    if num_fit_more_than_0 > 2:

        fitness_without_zero_cum = count_cumulative(fitness_without_zero)
        picked_genome_1 = special_choice(genome_pop_without_zero_fitness, fitness_without_zero_cum)
        # REMOVE PICKED GENOME AND GENOME'S FITNESS FROM SELECTION
        picked_genome_1_idx = picked_genome_1[1]
        fitness_without_zero.pop(picked_genome_1_idx)
        genome_pop_without_zero_fitness.pop(picked_genome_1_idx)
        fitness_without_zero_cum2 = count_cumulative(fitness_without_zero)
        picked_genome_2 = special_choice(genome_pop_without_zero_fitness, fitness_without_zero_cum2)
        return [picked_genome_1[0], picked_genome_2[0]]
    if num_fit_more_than_0 == 2:
        return [save_genome_one_fit_more_than_0, save_genome_two_fit_more_than_0]
    if num_fit_more_than_0 == 1:
        genome_pop.remove(save_genome_one_fit_more_than_0)
        all_one_fitness = []
        for i in range(len(genome_pop)):
            all_one_fitness.append(1)
        all_one_fitness_cum = count_cumulative(all_one_fitness)
        picked_genome_2 = special_choice(genome_pop, all_one_fitness_cum)
        return [save_genome_one_fit_more_than_0, picked_genome_2[0]]
    if num_fit_more_than_0 == 0:
        all_one_fitness = []
        for i in range(len(genome_pop)):
            all_one_fitness.append(1)
        all_one_fitness_cum = count_cumulative(all_one_fitness)
        picked_genome_1 = special_choice(genome_pop, all_one_fitness_cum)
        # REMOVE PICKED GENOME AND GENOME'S FITNESS FROM SELECTION
        picked_genome_1_idx = picked_genome_1[1]
        all_one_fitness.pop(picked_genome_1_idx)
        genome_pop.pop(picked_genome_1_idx)
        all_one_fitness_cum2 = count_cumulative(all_one_fitness)
        picked_genome_2 = special_choice(genome_pop, all_one_fitness_cum2)
        return [picked_genome_1[0], picked_genome_2[0]]
    
    
def single_crossover(genome_select): # sasa
    length = len(genome_select[0])
    
    if length < 2:
        return genome_select

    p = randint(1, length - 1)
    return [genome_select[0][0:p] + genome_select[1][p:], genome_select[1][0:p] + genome_select[0][p:]]

   
def take_second(elem): # sasa
    return elem[1]
    
def sort_population(genome_pop, max_price, list_barang): # jenni
    fitGen = []
    for genome in genome_pop:
        fitnesBarang = fitness(list_barang, max_price, genome)
        fitGen.append([genome,fitnesBarang])
    sorted_genome_pop = sorted(fitGen, key=take_second, reverse=True)
    return_genome = []
    for i in sorted_genome_pop:
        return_genome.append(i[0])
    return return_genome

# MUTATE RANDOM BIT OF GENOME
def mutation(genome, num_mutation = 1, probability : float = 0.5): # jenni
    for _ in range(num_mutation):
        index = randrange(len(genome)) # range dari 0 sampai len(genome) - 1
        if random() < probability:
            genome = genome[:index] + str(abs(int(genome[index]) - 1)) + genome[index+1:]
        
    return genome
