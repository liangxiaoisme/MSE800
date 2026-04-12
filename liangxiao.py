# Ask the user for two numbers
number1 = input("Enter the first number: ")  # User input is a string by default
number2 = input("Enter the second number: ")

# Convert the string inputs to floats for mathematical operations
number1 = float(number1)
number2 = float(number2)

# Calculate the sum and product of the numbers
sum_result = number1 + number2
product_result = number1 * number2

# Output the results to the user
print("The sum of the numbers is:", sum_result)
print("The product of the numbers is:", product_result)