from csv_commands import read_data_from_csv, write_data_to_csv

tilausnumero_column_name = "tilausnumero"
tilaukset_csv_file = 'tilaukset.csv'
import csv

def tilaus(kayttaja, tuote, counter, tilausnumero):
    with open(tilaukset_csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([kayttaja, tuote, counter[tuote], tilausnumero])



def poisto(poistettava):
    tilaus_column_names = ['kayttaja', 'tuote', 'counter', 'tilausnumero']
    tilauslista = read_data_from_csv(tilaukset_csv_file, tilaus_column_names)

    if poistettava not in tilauslista:
        return False
    else:
        del tilauslista[poistettava]
        write_data_to_csv(tilaukset_csv_file, tilauslista, tilaus_column_names)
        return f"tilaus poistettu, päivitetty lista:{tilauslista}"



def tilaushaku(ordernumber):
    if not isinstance(ordernumber, int):
        return False

    tilaus_column_names = ['kayttaja', 'tuote', 'counter', 'tilausnumero']
    tilauslista = read_data_from_csv("tilaukset.csv", tilaus_column_names)

    for kayttaja, items in tilauslista.items():
        for item in items:
            if int(item['tilausnumero']) == ordernumber:
                return kayttaja, item['tuote'], item['counter'], int(item['tilausnumero'])

    return None








def write_dict_to_csv(tilauslista):
    with open(tilaukset_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for kayttaja, items in tilauslista.items():
            for item in items:
                writer.writerow([kayttaja, item[0], item[1], item[2]])

def listaus():
    with open(tilaukset_csv_file, 'r') as file:
        reader = csv.reader(file)
        tilauslista = list(reader)
        return bool(tilauslista), tilauslista

def kayttajan_tilaukset(kayttaja):
    with open(tilaukset_csv_file, 'r') as file:
        reader = csv.reader(file)
        tilauslista = [row for row in reader if row[0] == kayttaja]
        return tilauslista if tilauslista else False
