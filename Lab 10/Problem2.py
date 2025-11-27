# Input
N = int(input("Enter the value of N: "))

# Count numbers divisible by each number
count_2 = N // 2      # divisible by 2
count_3 = N // 3      # divisible by 3
count_5 = N // 5      # divisible by 5

# Count numbers divisible by pairs (inclusion)
count_2_3 = N // (2 * 3)   # divisible by both 2 and 3
count_2_5 = N // (2 * 5)   # divisible by both 2 and 5
count_3_5 = N // (3 * 5)   # divisible by both 3 and 5

# Count numbers divisible by all three (inclusion)
count_2_3_5 = N // (2 * 3 * 5)  # divisible by 2, 3, and 5

# Apply Principle of Inclusion-Exclusion
total = count_2 + count_3 + count_5 - count_2_3 - count_2_5 - count_3_5 + count_2_3_5

# Print results
print(f"\nNumbers from 1 to {N} divisible by 2, 3, or 5: {total}")
print(f"\nBreakdown:")
print(f"Divisible by 2: {count_2}")
print(f"Divisible by 3: {count_3}")
print(f"Divisible by 5: {count_5}")
print(f"Divisible by 2 and 3: {count_2_3}")
print(f"Divisible by 2 and 5: {count_2_5}")
print(f"Divisible by 3 and 5: {count_3_5}")
print(f"Divisible by 2, 3 and 5: {count_2_3_5}")

# Print the actual numbers (optional)
print(f"\nActual numbers divisible by 2, 3, or 5:")
divisible_numbers = []
for i in range(1, N + 1):
    if i % 2 == 0 or i % 3 == 0 or i % 5 == 0:
        divisible_numbers.append(i)
print(divisible_numbers)