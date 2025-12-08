python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import re

# Read the SQL file and extract data
def parse_world_sql():
    with open('world db (1).sql', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find CREATE TABLE statements to understand structure
    create_tables = re.findall(r'CREATE TABLE.*?;', content, re.DOTALL | re.IGNORECASE)
    for table in create_tables:
        print("Found table structure:")
        print(table[:200] + "...")
        print("-" * 50)
    
    # Create in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    
    # Clean the SQL content for SQLite compatibility
    # Remove MySQL-specific commands
    cleaned_sql = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Remove comments
    cleaned_sql = re.sub(r'ENGINE=.*?;', ';', cleaned_sql)  # Remove ENGINE specifications
    
    try:
        # Execute the SQL to create tables and insert data
        conn.executescript(cleaned_sql)
        
        # Get all table names
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Available tables:")
        for table in tables:
            print(f"- {table[0]}")
            
            # Get sample data from each table
            df_sample = pd.read_sql_query(f"SELECT * FROM {table[0]} LIMIT 5", conn)
            print(f"Sample data from {table[0]}:")
            print(df_sample)
            print("-" * 50)
        
        return conn, [table[0] for table in tables]
        
    except Exception as e:
        print(f"Error processing SQL: {e}")
        return None, []

# Main analysis
print("=== WORLD DATABASE ANALYSIS ===")
conn, table_names = parse_world_sql()

if conn and table_names:
    # Example visualizations (adjust based on what tables you find)
    for table_name in table_names:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            print(f"\n=== {table_name.upper()} TABLE ANALYSIS ===")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            
            # Create basic visualizations
            plt.figure(figsize=(15, 10))
            
            # If table has numeric columns, create some plots
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                for i, col in enumerate(numeric_cols[:4], 1):  # Max 4 plots
                    plt.subplot(2, 2, i)
                    df[col].hist(bins=20)
                    plt.title(f'Distribution of {col}')
                    plt.xlabel(col)
                    plt.ylabel('Frequency')
            
            plt.tight_layout()
            plt.suptitle(f'Analysis of {table_name} table', y=1.02)
            plt.show()
            
        except Exception as e:
            print(f"Error analyzing {table_name}: {e}")
    
    conn.close()
else:
    print("Could not process the SQL file. Please check the file format.")
