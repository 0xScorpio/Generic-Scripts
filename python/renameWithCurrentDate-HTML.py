import os
from datetime import date

def main():
    # Specify the directory path where the HTML files are located
    dir_path = 'C:/helloWorld/VulnAssessReformat/'
    
    # Get the current date
    current_date = date.today()
    date_suffix = current_date.strftime("_%d%m%y")

    # Iterate through the files in the directory
    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            # Construct the new filename by removing the last 24 characters and appending the date suffix
            new_filename = filename[:-24] + date_suffix + '.html'
            # Construct the full file paths
            old_filepath = os.path.join(dir_path, filename)
            new_filepath = os.path.join(dir_path, new_filename)
            # Rename the file
            os.rename(old_filepath, new_filepath)
            print(f"Renamed '{filename}' to '{new_filename}'")

if __name__ == '__main__':
    main()
