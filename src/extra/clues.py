from itertools import product

sentence_templates = [
    "The habitat is {not_str}on {biome1} or {biome2}",
    "The habitat is {not_str}within one space of {biome}",
    "The habitat is {not_str}within one space of either animal territory",
    "The habitat is {not_str}within two spaces of a {structure}",
    "The habitat is {not_str}within two spaces of {animal} territory",
    "The habitat is {not_str}within three spaces of a {color} structure"
]

biomes = ['water', 'mountain', 'forest', 'swamp', 'desert']
structures = ['standing stone', 'abandoned shack']
animals = ['cougar', 'bear']
colors = ['green', 'white', 'blue', 'black']
not_options = ['', 'not ']

for sentence_template in sentence_templates:
    if '{biome1}' in sentence_template and '{biome2}' in sentence_template:
        combinations = [(a, b, c) for a, b, c in product(not_options, biomes, biomes) if b != c]
    elif '{biome}' in sentence_template:
        combinations = [(a, b, b) for a, b in product(not_options, biomes)]
    elif '{animal}' in sentence_template:
        combinations = [(a, b) for a, b in product(not_options, animals)]
    elif '{structure}' in sentence_template:
        combinations = [(a, b) for a, b in product(not_options, structures)]
    elif '{color}' in sentence_template:
        combinations = [(a, b) for a, b in product(not_options, colors)]
    else:
        combinations = []
    with open("data/normal_clues.txt","a") as normal_clues:
        with open("data/advanced_clues.txt", "a") as advanced_clues:
            for combo in combinations:
                sentence = sentence_template.format(not_str=combo[0], biome1=combo[1], biome2=combo[2] if '{biome2}' in sentence_template else '',
                                                biome=combo[1] if '{biome}' in sentence_template else '',
                                                structure=combo[1] if '{structure}' in sentence_template else '',
                                                animal=combo[1] if '{animal}' in sentence_template else '',
                                                color=combo[1] if '{color}' in sentence_template else '')
                if combo[0] == "not " or combo[1] == "black":
                    advanced_clues.write(sentence + "\n")
                else:
                    normal_clues.write(sentence + "\n")