def process_moneyline(moneyline):

    moneyline = float(moneyline)

    if moneyline < 0:
        result = abs(moneyline) / (abs(moneyline) + 100)
    else:
        result = 100 / (abs(moneyline) + 100)
    return result

moneyline = '+150'

result = process_moneyline(moneyline)

print(result)