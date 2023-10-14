import os

# Directory containing your text files
directory = 'E:\BirdNet Audio 2023\GGOW Call Time Analysis\.2'

# Output file
output_file = directory + 'output.txt'

# Iterate through each file in the directory
with open(output_file, 'w') as output:
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            file_parts = filename.split('_')
            print(filename)
            with open(file_path, 'r') as file:
                for line in file:
                    # Write the filename and line content to the output file
                    line_parts = line.split('\t')
                    line_out = line_parts[2].replace('  ',',').replace('Strix nebulosa_Great Gray Owl', 'GGOW')
                    output.write(f'{file_parts[0]},{line_out}')

print(f'Concatenated files written to {output_file}')
