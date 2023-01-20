#define exchange rates
print("Currency Converter")
inr_to_eur=0.011
inr_to_usd=0.012
inr_to_yen=1.59

while True:
    amount=float(input("Enter the amount you want to exchange in INR: "))
    print("Choose the currency you want to exchange it to:")
    print("1. Euro")
    print("2. US Dollar")
    print("3. Japanese Yen")
    exchange_choice=input()
    if exchange_choice == "1":
        conv_curr=amount*inr_to_eur
        conv_curr=round(conv_curr,2)
        print("The amount after conversion is: ",conv_curr," €")
    elif exchange_choice == "2":
        conv_curr=amount*inr_to_usd
        conv_curr=round(conv_curr,2)
        print("The amount after conversion is: ",conv_curr," $")
    elif exchange_choice == "3":
        conv_curr=amount*inr_to_yen
        conv_curr=round(conv_curr,2)
        print("The amount after conversion is: ",conv_curr," ¥")
    else:
        print("Incorrect input.")
    print("****************************************")
    
    
        