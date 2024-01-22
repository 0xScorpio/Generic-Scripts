import csv

def read_csv(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            # Skip header row if it exists
            next(reader, None)
            # Extract columns (name and data) from each row
            data = [(row[0], row[1]) for row in reader]
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except csv.Error as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return []

def compare_csv_files(file_path1, file_path2, output_file_path):
    # Read CSV data from files
    csv_data1 = read_csv(file_path1)
    csv_data2 = read_csv(file_path2)

    # Check if data is not empty
    if csv_data1 and csv_data2:
        # Convert lists of tuples to sets for easy comparison
        set1 = set(csv_data1)
        set2 = set(csv_data2)

        # Find common elements
        common_elements = set1.intersection(set2)

        # Find unique elements in each CSV file
        unique_elements_csv1 = set1 - set2
        unique_elements_csv2 = set2 - set1

        # Write output to a new CSV file
        with open(output_file_path, 'w', newline='') as output_file:
            fieldnames = ['Name', 'IP Address', 'Source']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()

            # Write common elements
            for element in common_elements:
                writer.writerow({'Name': element[0], 'IP Address': element[1], 'Source': 'Both'})

            # Write unique elements from CSV File 1
            for element in unique_elements_csv1:
                writer.writerow({'Name': element[0], 'IP Address': element[1], 'Source': 'FILE1'})

            # Write unique elements from CSV File 2
            for element in unique_elements_csv2:
                writer.writerow({'Name': element[0], 'IP Address': element[1], 'Source': 'FILE2'})
    else:
        print("One or both CSV files are empty.")

def main():
    # Example file paths
    file_path1 = 'FILE1.csv'
    file_path2 = 'FILE2.csv'
    output_file_path = 'CSVCompare_output.csv'

    # Compare CSV files and write output to a new CSV file
    compare_csv_files(file_path1, file_path2, output_file_path)

if __name__ == "__main__":
    main()
