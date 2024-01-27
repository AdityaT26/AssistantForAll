import os

file_name = "htmlRs.html"

h = open(file_name, 'w+')
h.write('')
h.close()

file_stats = os.stat(file_name)

print(file_stats)
print(f'File Size in Bytes is {file_stats.st_size}')
print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')