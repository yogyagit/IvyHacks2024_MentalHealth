import os

def convert_to_utf8(directory):
    # List all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Check if it's a file
        if os.path.isfile(filepath):
            try:
                # Open the file in its original encoding and read the content
                with open(filepath, 'r', encoding='iso-8859-1') as file:
                    content = file.read()
                
                # Write the content back to the file with UTF-8 encoding
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Converted {filename} to UTF-8.")
            except UnicodeDecodeError:
                print(f"Failed to convert {filename}. It may already be in UTF-8 or another encoding.")

# Specify the directory containing the files
data_directory = r'/Users/noelnebu/Library/CloudStorage/GoogleDrive-noelnebu@gmail.com/My Drive/Hackathons/IvyHacks/IvyHacks2024_MentalHealth/backend/data'
convert_to_utf8(data_directory)
