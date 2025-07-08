from forex_python.converter import CurrencyRates

def convert_currency(amount, from_currency, to_currency):
    c = CurrencyRates()
    try:
        result = c.convert(from_currency.upper(), to_currency.upper(), amount)
        return result
    except Exception as e:
        print(f"Error:{e}")
        return None
    
def main():
    print("Offline currency converter CLI")
    amount = float(input("Enter the amount:"))
    from_currency =  input("Enter FROM currency code (e.g. USD):")
    to_currency = input("Enter to currency code(e.g. INR)")

    converted = convert_currency(amount, from_currency, to_currency)

    if converted is not None:
        print(f"\n {amount} {from_currency.upper()} = {converted:.2f}{to_currency.upper()}")
    else:
        print("\n Conversion failed. Please check your inputs or connection.")

if __name__ == "__main__":
    main()