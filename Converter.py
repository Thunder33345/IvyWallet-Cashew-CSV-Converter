import sys
import pandas as pd

def transform(infile):
    """
    Transform the data from the input file and save it to a new CSV file.

    Parameters:
        infile (str): The path to the input CSV file.

    Returns:
        None
    """
    df_ivy = pd.read_csv(infile, encoding="utf-16")
    transformed_data = []

    # Iterate through each row in the expenses DataFrame
    for _, row in df_ivy.iterrows():
        # Transform the Amount based on Type
        amount = float(row['Amount'].replace(',', ''))
        if row['Type'] == 'TRANSFER':
            amount = float(row['Transfer Amount'].replace(',', ''))
            row['Category'] = "Balance Correction"
            if pd.isna(row['Description']):
                row['Description'] = f"Transferred Balance: {row['Account']} -> {row['To Account']}"

        if row['Type'] == 'EXPENSE' or row['Type'] == 'TRANSFER':
            amount = -1 * amount

        # Append the original row to the transformed DataFrame
        transformed_data.append({
            'Date': row['Date'],
            'Amount': amount,
            'Category': row['Category'],
            'Title': row['Title'],
            'Note': row['Description'],
            'Account': row['Account']
        })

        # If it's a Transfer, create a new record with the same columns
        if row['Type'] == 'TRANSFER':
            transformed_data.append({
                'Date': row['Date'],
                'Amount':amount * -1,
                'Category': row['Category'],
                'Title': row['Title'],
                'Note': row['Description'],
                'Account': row['To Account']
            })

    # Create DataFrame from transformed data and save it
    transformed_df = pd.DataFrame(transformed_data)
    transformed_df.to_csv('./CashewPrelim.csv', index=False)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Error: Add the input Ivy Wallet csv file as an argument.")
        sys.exit()
    infile = sys.argv[1]
    transform(infile)

if __name__  == "__main__":
    main()
