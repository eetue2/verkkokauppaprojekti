import csv
user_csv_file_path = 'kayttajat.csv'
yllasalasana="admin"
def load_user_data_from_csv(user_csv_file_path):
    tunnukset = []
    postit = []
    salasanat = []

    try:
        with open(user_csv_file_path, 'r') as file:
            reader = csv.reader(file)
            # Get the header row, if it exists
            header_row = next(reader, None)

            # Check if the header row is present and has the correct structure
            if header_row != ['Username', 'Email', 'Password']:
                print("Invalid header row:", header_row)
                return tunnukset, postit, salasanat

            # Read the rest of the rows
            for row in reader:
                if len(row) == 3:  # Ensure each row has three values
                    tunnukset.append(row[0])
                    postit.append(row[1])
                    salasanat.append(row[2])
                else:
                    print("Invalid row:", row)

    except Exception as e:
        print("Error reading CSV file:", e)

    return tunnukset, postit, salasanat




def save_user_data_to_csv(tunnukset, postit, salasanat):
    with open(user_csv_file_path, 'a', newline='') as user_file:
        user_writer = csv.writer(user_file)
        user_writer.writerows(zip(tunnukset, postit, salasanat))





def rektun(kayttaja, tunnukset):
    return kayttaja not in tunnukset


def rekpos(sposti, postit):
    musts = ("@", ".")
    for i in musts:
        if i not in sposti:
            return False
    if sposti in postit:
        return False
    else:
        return True


def kirjaudu(kayttaja, salasana, tunnukset, salasanat):
    if kayttaja not in tunnukset:
        return False
    else:
        index_tunnus = tunnukset.index(kayttaja)
        if kayttaja == tunnukset[index_tunnus] and salasana == salasanat[index_tunnus]:
            return True
        else:
            return False


def admin(salasana):
    if salasana == yllasalasana:
        return True
    else:
        return False


