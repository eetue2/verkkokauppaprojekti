import csv


import csv

def lisays(tuotteen_nimi, hinta):
    tuotteet_csv_file = "tuotteet.csv"

    # Check if the product already exists
    with open(tuotteet_csv_file, 'r') as file:
        reader = csv.DictReader(file)
        existing_products = [row for row in reader if row['product'] == tuotteen_nimi]

    if existing_products:
        return False

    with open(tuotteet_csv_file, 'a', newline='') as file:
        fieldnames = ['product', 'price', 'product_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Find the highest existing product_id
        existing_product_ids = {int(row['product_id']) for row in csv.DictReader(open(tuotteet_csv_file))}
        product_id = str(max(existing_product_ids, default=0) + 1).zfill(3)

        # Write the new product
        writer.writerow({'product': tuotteen_nimi, 'price': hinta, 'product_id': product_id})

    return True  # Product added successfully


def poista(poistuot):
    tuotteet_csv_file = "tuotteet.csv"
    poistetut_tuotteet_file = "poistetut_tuotteet.csv"

    # Read the existing content of tuotteet.csv
    with open(tuotteet_csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Find and remove the row corresponding to the specified product
    removed_rows = [row for row in rows if row['product'] == poistuot]
    updated_rows = [row for row in rows if row['product'] != poistuot]

    # Write the updated content back to tuotteet.csv
    with open(tuotteet_csv_file, 'w', newline='') as file:
        fieldnames = ['product', 'price', 'product_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    # Write the removed product to poistetut_tuotteet.csv
    with open(poistetut_tuotteet_file, 'a', newline='') as poistetut_file:
        poistetut_writer = csv.DictWriter(poistetut_file, fieldnames=fieldnames)
        poistetut_writer.writerows(removed_rows)

    # Return True if the product was found and removed, False otherwise
    return len(removed_rows) > 0

def tuotehaku(haetuot, file_path='tuotteet.csv', poistetut_file_path='poistetut_tuotteet.csv'):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if haetuot == row['product'] or haetuot == row['product_id']:
                return {'product': row['product'], 'price': float(row['price']), 'tuote id': row['product_id']}

    with open(poistetut_file_path, 'r') as poistetut_file:
        reader = csv.DictReader(poistetut_file)
        for row in reader:
            if haetuot == row['product'] or haetuot == row['product_id']:
                return {'product': row['product'], 'price': float(row['price']), 'tuote id': row['product_id'], 'status': 'poistettu'}

    return False


def paivitys(paivtuot, hinnim):
    tuotteet_csv_file = "tuotteet.csv"

    # Check if the product exists in the CSV file
    with open(tuotteet_csv_file, 'r') as file:
        reader = csv.DictReader(file)
        products = list(reader)
        for product in products:
            if product['product'] == paivtuot:
                # Update the price of the product
                product['price'] = hinnim

                # Write the updated products back to the CSV file
                with open(tuotteet_csv_file, 'w', newline='') as write_file:
                    fieldnames = ['product', 'price', 'product_id']
                    writer = csv.DictWriter(write_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(products)

                return True  # Product updated successfully

    return False  # Product not found
