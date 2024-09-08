import json
import random
import string
import csv



class SpecConfigLoader:
    def __init__(self, spec_file):
        self.spec_file = spec_file
        self.spec = self.load_spec()

    def load_spec(self):
        """Load the specification from the JSON file."""
        with open(self.spec_file, 'r') as json_file:
            spec = json.load(json_file)
        # Convert IncludeHeader to boolean if it's a string in JSON
        spec['IncludeHeader'] = spec['IncludeHeader'] in ["True", True]
        return spec


class FixedWidthFileGenerator:
    def __init__(self, config_loader):
        self.spec = config_loader


    def random_string(self, length):
        """Generate a random alphanumeric string"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def pad_or_truncate(self, value, length):
        return value[:length].ljust(length)

    def generate_random_data(self, rows=100):
        """Generate random data for the specified number of rows.Default is 100"""
        data = []
        print (self.spec)
        for _ in range(rows):
            row = [
                self.random_string(int(self.spec['Offsets'][0])), 
                self.random_string(int(self.spec['Offsets'][1])), 
                self.random_string(int(self.spec['Offsets'][2])), 
                self.random_string(int(self.spec['Offsets'][2])), 
                self.random_string(int(self.spec['Offsets'][4])), 
                self.random_string(int(self.spec['Offsets'][5])), 
                self.random_string(int(self.spec['Offsets'][6])), 
                self.random_string(int(self.spec['Offsets'][7])), 
                self.random_string(int(self.spec['Offsets'][8])), 
                self.random_string(int(self.spec['Offsets'][9]))  
            ]
            data.append(row)
        return data

    def write_fixed_width_file(self, output_file, rows=100):
        """Write the fixed-width file based on the specification."""
        data = self.generate_random_data(rows)

        with open(output_file, 'w', encoding=self.spec['FixedWidthEncoding']) as fw_file:
            # Write the header if required
            if self.spec['IncludeHeader']:
                header = ''.join([self.pad_or_truncate(name, int(length)) for name, length in zip(self.spec['ColumnNames'], self.spec['Offsets'])])
                fw_file.write(header + '\n')

            # Write the data rows
            for row in data:
                fixed_width_row = ''.join([self.pad_or_truncate(str(value), int(length)) for value, length in zip(row, self.spec['Offsets'])])
                fw_file.write(fixed_width_row + '\n')

        print(f"Fixed-width file '{output_file}' with {rows} rows of random data generated successfully!")



class FixedWidthToCSVConverter:
    def __init__(self, spec_file_loader, fixed_width_file):
        self.fixed_width_file = fixed_width_file
        self.spec = spec_file_loader


    def parse_fixed_width_line(self, line):
        """Parse a single line from the fixed-width file according to the offsets mentioned in spec.json"""
        offsets = [int(offset) for offset in self.spec['Offsets']]
        parsed_line = []
        start = 0
        for offset in offsets:
            parsed_line.append(line[start:start+offset].strip())  # Extract field and remove any extra spaces
            start += offset
        return parsed_line

    def convert_to_csv(self, output_csv_file):
        """Convert the fixed-width file to CSV format."""
        with open(self.fixed_width_file, 'r', encoding=self.spec['FixedWidthEncoding']) as fw_file, \
             open(output_csv_file, 'w', newline='', encoding=self.spec['DelimitedEncoding']) as csv_file:
            
            csv_writer = csv.writer(csv_file)
            
            # Write the header if specified in the JSON spec
            if self.spec['IncludeHeader']:
                csv_writer.writerow(self.spec['ColumnNames'])
                next(fw_file)  # Skip the header line in the fixed-width file
            
            # Process each line in the fixed-width file
            for line in fw_file:
                parsed_line = self.parse_fixed_width_line(line)
                csv_writer.writerow(parsed_line)

        print(f"CSV file '{output_csv_file}' generated successfully from the fixed-width file!")

if __name__ == "__main__":
    spec_loader = SpecConfigLoader('spec.json')
    print (spec_loader.spec)
    
    generator = FixedWidthFileGenerator(spec_loader.spec)
    generator.write_fixed_width_file('fixed_width_file.txt', rows=100)

    converter = FixedWidthToCSVConverter(spec_loader.spec, 'fixed_width_file.txt')
    converter.convert_to_csv('output.csv')
        
    
        

