def count_significant_digits(num_str):
    if num_str.startswith(("-", "+")):  # Remove sign if present
        num_str = num_str[1:]
    num_str = num_str.lstrip("0")  # Remove leading zeros
    
    if "." in num_str:
        integer_part, decimal_part = num_str.split(".")  # Split into parts
        # Remove trailing zeros in decimal part
        decimal_part = decimal_part.rstrip("0")
        # Combine parts for counting
        sig_str = integer_part + decimal_part
    else:
        sig_str = num_str.rstrip("0")  # No decimal point, just strip trailing zeros
    
    return len(sig_str)

def custom_round(num, k):
    factor = 10 ** k
    shifted = num * factor  # Multiply and shift
    
    if shifted >= 0:  # Extract integer part
        rounded = int(shifted + 0.5)
    else:
        rounded = int(shifted - 0.5)
    return rounded / factor  # Shift back

# Main program
num_str = input("Enter a real number: ")
k = int(input("Enter value of k: "))
num = float(num_str)
sig_digits = count_significant_digits(num_str)
rounded_num = custom_round(num, k)

print("\nOutput1: Number of significant digits", sig_digits)
print("Output2: The rounded number", rounded_num)