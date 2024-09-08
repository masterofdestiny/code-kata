import csv
import csv
from hashlib import sha256
from faker import Faker

# This is to ensure we can generate some random data using this 
fake = Faker()



class GenerateCSV:

    def __init__(self, file_name, num_rows):
    
        self.file_name = file_name
        self.num_rows = num_rows
        
    def generate_csv(self):
    
        with open(self.file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header
            writer.writerow(['first_name', 'last_name', 'address', 'date_of_birth'])
            # Generate random rows
            for _ in range(self.num_rows):
                first_name = fake.first_name()
                last_name = fake.last_name()
                address = fake.address().replace('\n', ' ')  # Replace newlines in address with space
                date_of_birth = fake.date_of_birth()
                writer.writerow([first_name, last_name, address, date_of_birth])



class Anonymiser:


    def __init__(self, csv_file, outfile):
    
        self.csv_file = csv_file
        self.outfile = outfile


    def hash_string(self, field):
        return sha256(field.encode()).hexdigest()

    def anonymize_row(row):

        row['first_name'] = hash_string(row['first_name'])
        row['last_name'] = hash_string(row['last_name'])
        row['address'] = hash_string(row['address'])
        return row

    def csv_row_generator(self):

        with open(self.csv_file, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                yield row  # Yield each row from the CSV file

    def anonymize_csv(self):
        """Anonymize the CSV file using generators and write to a new CSV file."""
        with open(self.outfile, 'w', newline='', encoding='utf-8') as outfile:
            # Read the input CSV file row by row
            row_generator = self.csv_row_generator()
            # Initialize CSV writer
            first_row = next(row_generator)
            writer = csv.DictWriter(outfile, fieldnames=first_row.keys())
            writer.writeheader()

            # Process the first row
            anonymized_row = self.anonymize_row(first_row)
            writer.writerow(anonymized_row)

            # Process the remaining rows
            for row in row_generator:
                anonymized_row = self.anonymize_row(row)
                writer.writerow(anonymized_row)




if __name__ == "__main__":
    # Generate a CSV with 1 million rows (or any number you need)
    input_file = 'large_dataset.csv'
    gs = GenerateCSV(input_file, 1000000)
    gs.generate_csv()  # You can adjust the number of rows as needed
    output_file = 'anonymized_dataset.csv'
    aa = Anonymiser(input_file, output_file)
    aa.anonymize_csv()
