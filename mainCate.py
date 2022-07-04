import string
from barang import Barang
from GA import *
import pandas as pd
import time

def getBarang(genome, list_barang):
    string_items = "LIST BARANG:\n"
    # print("List Barang:")
    total_price = 0
    for i in range(len(genome)):
        if genome[i] == "1":
            string_items = string_items + list_barang[i].name + ": " + str(list_barang[i].price) + ", " + str(list_barang[i].num_buyers) + "\n"
            # print(f"{list_barang[i].name}: {list_barang[i].price}, {list_barang[i].num_buyers}")
            total_price += list_barang[i].price
    string_items += "\nTOTAL: " + str(total_price)
    # print(f"Total: {total_price}")
    return string_items

semua_barang = []
semua_barang_price = 0
# INSERT DATA
def insert(df,categoryPil):
    global semua_barang_price
    for i in range(len(df)):
        nama_barang = df["nama_barang"][i]
        category = df["category"][i]
        num_buyers = df["jumlah_pembeli"][i]
        price = df["harga"][i]
        semua_barang_price += price
        if category in categoryPil:
            barang_baru = Barang(category, nama_barang, num_buyers,price)
            semua_barang.append(barang_baru)
    # print(semua_barang)
    return semua_barang

def insertAll(df):
    global semua_barang_price

    for i in range(len(df)):
        nama_barang = df["nama_barang"][i]
        category = df["category"][i]
        num_buyers = df["jumlah_pembeli"][i]
        price = df["harga"][i]
        semua_barang_price += price
        barang_baru = Barang(category, nama_barang, num_buyers,price)
        semua_barang.append(barang_baru)
    # print(semua_barang)
    return semua_barang

def main(semua_barang,price):
    start_time = time.time()
    string_items = ""
    string_details = "DETAILS:\n"
    # print(semua_barang)
    # GET MAX FITNESS
    total_fitness_barang = 0
    for barang in semua_barang:
        total_fitness_barang += barang.num_buyers

    # num_genomes = int((2 ** (len(semua_barang) - 1))) # number of genomes per generation (1/2 of all combinations can get around 90% accuracy)
    # if num_genomes > 100:
    #     num_genomes = 100
    num_genomes = len(semua_barang)
    num_genomes_to_generate = num_genomes - 2
    num_generations = 100
    num_runs = 1
    max_fitness = -1
    best_genome = ""
    # achieved_319 = 0
    last_generation = 0
    for i in range(num_runs):
        # GENERATE 0th GENERATION
        random_gen_0 = False
        if price > semua_barang_price / 2:
            random_gen_0 = True
        cur_genome_pop = generate_pop0(len(semua_barang),num_genomes, random_gen_0)
        for j in range(num_generations):
            last_generation = j
            # GET MAXIMUM FITNESS OF POPULATION
            for x in cur_genome_pop:
                cari_fitness = fitness(semua_barang, price, x)
                if (cari_fitness > max_fitness):
                    max_fitness = cari_fitness
                    best_genome = x
                    print(max_fitness)
            if total_fitness_barang == max_fitness:
                break
            next_genome_pop = []
            for k in range(int(num_genomes_to_generate/2)): # dibagi 2 karena setiap cross menghasilkan 2 genomes
                # SELECT A PAIR FROM THE GENERATION
                selections = selection_pair(cur_genome_pop, semua_barang, price)
                # USE SINGLE POINT CROSSOVER TO CROSS THE SELECTIONS
                cross = single_crossover(selections)
                for l in cross:
                    next_genome_pop.append(l)

            # SORT POPULATION OF CURRENT GENERATION
            sorted_cur_genome_pop = sort_population(cur_genome_pop, price, semua_barang)

            # GET 2 BEST GENOME FROM CURRENT GENERATION AND INSERT TO NEXT GENERATION (ELITISM)
            next_genome_pop.append(sorted_cur_genome_pop[0])
            next_genome_pop.append(sorted_cur_genome_pop[1])

            # MUTATE GENOMES
            for m in range(len(next_genome_pop)):
                next_genome_pop[m] = mutation(next_genome_pop[m])
            cur_genome_pop = next_genome_pop

            

        string_details = string_details + "Max Fitness: " + str(max_fitness) + "\n"
        # print(f"max fitness: {max_fitness}")
    string_details = string_details + "Last Generation: " + str(last_generation) + "\n"
    # print(f"last generation: {last_generation}")
    string_details = string_details + "Total Fitness: " + str(total_fitness_barang) + "\n"
    # print(f"total fitness: {total_fitness_barang}")
    string_details = string_details + "Best Genome: " + str(best_genome) + "\n"
    # print(f"best genome: {best_genome}")
    string_items += getBarang(best_genome, semua_barang) + "\n"
    string_items += "Maximum Price Inputted: " + str(price) + "\n"
    string_details += "Time: " + str(time.time() - start_time)
    # print("--- %s seconds ---" % (time.time() - start_time))

    return string_items, string_details