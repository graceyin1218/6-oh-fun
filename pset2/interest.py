# initial deposit of $100
# interest rate of 5%

def calculate_balance(balance, interest, years):
  if years == 0:
    return balance
  balance = balance*(1+interest)
  return calculate_balance(balance, interest, years-1)

print(calculate_balance(100, 0.05, 24))
