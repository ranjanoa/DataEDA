import pandas as pd


def filter_csv_by_timeframe(input_file, output_file, time_column, start_time, end_time):
    """
    Filters a CSV file to only include rows within a specific timeframe.
    """
    try:
        # 1. Load the CSV file into a pandas DataFrame
        print(f"Loading data from {input_file}...")
        df = pd.read_csv(input_file)

        # 2. Convert the timestamp column to actual datetime objects
        # The 'errors="coerce"' argument handles any malformed dates by turning them into NaT (Not a Time)
        print(f"Converting column '{time_column}' to datetime...")
        df[time_column] = pd.to_datetime(df[time_column], errors='coerce')

        # Drop rows where the timestamp couldn't be parsed (optional, but recommended)
        df = df.dropna(subset=[time_column])

        # 3. Create the timeframe boundaries as datetime objects
        start = pd.to_datetime(start_time)
        end = pd.to_datetime(end_time)

        # 4. Filter the DataFrame
        # This keeps only the rows where the timestamp is >= start and <= end
        print(f"Filtering data from {start} to {end}...")
        filtered_df = df[(df[time_column] >= start) & (df[time_column] <= end)]

        # 5. Save the filtered data to a new CSV file
        # index=False prevents pandas from writing the row numbers into the file
        filtered_df.to_csv(output_file, index=False)
        print(f"Success! Filtered data saved to {output_file}.")
        print(f"Original row count: {len(df)} | Filtered row count: {len(filtered_df)}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except KeyError:
        print(f"Error: The column '{time_column}' does not exist in the CSV file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# ==========================================
# CONFIGURATION - Change these variables!
# ==========================================
INPUT_CSV = 'fingerprint4DEMO.csv'  # The name of your existing file
OUTPUT_CSV = 'fingerprint4DEMOSMALL.csv'  # The name of the new file to be created
TIMESTAMP_COLUMN = 'TimeStamp'  # The exact header name of your date/time column

# Define your timeframe (Format: 'YYYY-MM-DD HH:MM:SS' or just 'YYYY-MM-DD')
START_DATE = '2025-05-01 00:00:00'
END_DATE = '2025-09-30 23:59:59'

# Run the function
if __name__ == "__main__":
    filter_csv_by_timeframe(INPUT_CSV, OUTPUT_CSV, TIMESTAMP_COLUMN, START_DATE, END_DATE)