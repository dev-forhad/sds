my_string = "This is a test string for dividing into four parts."

# Calculate the length of the string and divide by 4 to get the length of each part
part_length = len(my_string) // 4

# Use slicing to get each part of the string
part1 = my_string[:part_length]
part2 = my_string[part_length:2*part_length]
part3 = my_string[2*part_length:3*part_length]
part4 = my_string[3*part_length:]

# Print the parts to the console
print("Part 1:", part1)
print("Part 2:", part2)
print("Part 3:", part3)
print("Part 4:", part4)
