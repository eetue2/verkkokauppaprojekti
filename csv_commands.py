import csv
tilaukset_csv_file = 'tilaukset.csv'


def read_data_from_csv(file_path, column_names):
    data = {}
    with open(file_path, 'r') as file:
        if column_names is None:
            reader = csv.reader(file)
        else:
            reader = csv.DictReader(file)
        for row in reader:
            key = row[0] if column_names is None else row[column_names[0]]
            price = (row[1]) if column_names is None else (row[column_names[1]])
            values = (price,) if column_names is None else {col: row[col] for col in column_names[1:]}
            if key in data:
                data[key].append(values)
            else:
                data[key] = [values]

    return data


def write_data_to_csv(file_path, data, column_names):
    with open(file_path, 'w', newline='') as file:
        if isinstance(data, dict):
            writer = csv.DictWriter(file, fieldnames=column_names)
            writer.writeheader()
            for key, values in data.items():
                for value in values:
                    writer.writerow({col: val for col, val in zip(column_names, [key] + list(value))})
        elif isinstance(data, list):
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        else:
            raise ValueError("Unsupported data type for writing to CSV.")
