import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('transactions.csv')


def exercise_0(file):
    # Load the dataset
    df = pd.read_csv(file)
    return df


def exercise_1(df):
    # Task 1: Return the column names as a list
    column_names = df.columns.tolist()
    return column_names


def exercise_2(df, k):
    # Task 2: Return the first k rows from the dataframe
    first_k_rows = df.head(k)
    return first_k_rows


def exercise_3(df, k):
    # Task 3: Return a random sample of k rows from the dataframe
    random_sample_k_rows = df.sample(k)
    return random_sample_k_rows


def exercise_4(df):
    # Task 4: Return a list of unique transaction types
    unique_transaction_types = df['type'].unique().tolist()
    return unique_transaction_types


def exercise_5(df):
    # Task 5: Return a Pandas series of the top 10 transaction destinations with frequencies
    top_10_destinations = df['nameDest'].value_counts().head(10)
    return top_10_destinations


def exercise_6(df):
    # Task 6: Return all the rows from the dataframe for which fraud was detected
    fraud_rows = df[df['isFraud'] == 1]
    return fraud_rows


def exercise_7(df):
    # Task 7: Additional exercise task (you can replace this with your custom code)
    pass


def visual_1(df):
    def transaction_counts(df):
        # Count of transaction types
        return df['type'].value_counts()

    def transaction_counts_split_by_fraud(df):
        # Count of transaction types split by fraud
        return df.groupby('type')['isFraud'].value_counts().unstack().fillna(0)

    fig, axs = plt.subplots(2, figsize=(10, 12))

    # Plot transaction counts
    transaction_counts(df).plot(ax=axs[0], kind='bar', color='skyblue')
    axs[0].set_title('Transaction Types Distribution')
    axs[0].set_xlabel('Transaction Type')
    axs[0].set_ylabel('Count')

    # Plot transaction counts split by fraud
    transaction_counts_split_by_fraud(df).plot(ax=axs[1], kind='bar', stacked=True, color=['blue', 'red'])
    axs[1].set_title('Transaction Types Distribution Split by Fraud')
    axs[1].set_xlabel('Transaction Type')
    axs[1].set_ylabel('Count')
    axs[1].legend(title='Fraud', labels=['Not Fraud', 'Fraud'])

    # Adding a super title
    fig.suptitle('Transaction Types Analysis', fontsize=16)

    # Adjust layout
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Annotate bars with counts
    for ax in axs:
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=9, color='black', xytext=(0, 5),
                        textcoords='offset points')

    plt.show()

    description = (
        "The first bar chart shows the distribution of transaction types across the dataset, highlighting which transaction types are most common. "
        "The second bar chart shows the same distribution but split by fraud status, providing insights into which types of transactions are more susceptible to fraud.")
    return description


description = visual_1(df)
print(description)


def visual_2(df):
    def query(df):
        # Filter for CASH_OUT transactions and calculate balance deltas
        cash_out_df = df[df['type'] == 'CASH_OUT'].copy()
        cash_out_df['origin_balance_delta'] = cash_out_df['oldbalanceOrg'] - cash_out_df['newbalanceOrig']
        cash_out_df['destination_balance_delta'] = cash_out_df['oldbalanceDest'] - cash_out_df['newbalanceDest']
        return cash_out_df

    # Run the query to get the filtered data
    filtered_df = query(df)

    # Plot the scatter plot
    plot = filtered_df.plot.scatter(x='origin_balance_delta', y='destination_balance_delta', alpha=0.5)
    plot.set_title('Origin Balance Delta vs. Destination Balance Delta for Cash Out Transactions')
    plot.set_xlabel('Origin Balance Delta')
    plot.set_ylabel('Destination Balance Delta')
    plot.set_xlim(left=-1e3, right=1e3)
    plot.set_ylim(bottom=-1e3, top=1e3)

    plt.tight_layout()
    plt.show()

    description = (
        "This scatter plot shows the relationship between the changes in the origin and destination account balances "
        "for Cash Out transactions. It provides insights into how balances shift during these transactions, which can help in detecting anomalies or suspicious activities.")
    return description


# Example usage
description = visual_2(df)
print(description)


def exercise_custom(df):
    # Calculate summary statistics for transaction amounts for fraud and non-fraud transactions
    fraud_amounts = df[df['isFraud'] == 1]['amount']
    non_fraud_amounts = df[df['isFraud'] == 0]['amount']

    summary_stats = {
        'fraud_mean': fraud_amounts.mean(),
        'fraud_median': fraud_amounts.median(),
        'fraud_std': fraud_amounts.std(),
        'non_fraud_mean': non_fraud_amounts.mean(),
        'non_fraud_median': non_fraud_amounts.median(),
        'non_fraud_std': non_fraud_amounts.std()
    }

    return summary_stats


def visual_custom(df):
    # Plot the distribution of transaction amounts for fraud and non-fraud transactions
    plt.figure(figsize=(14, 8))

    # Plot fraud transactions
    sns.histplot(df[df['isFraud'] == 1]['amount'], bins=50, color='red', label='Fraud', kde=True)
    # Plot non-fraud transactions
    sns.histplot(df[df['isFraud'] == 0]['amount'], bins=50, color='blue', label='Non-Fraud', kde=True)

    plt.title('Distribution of Transaction Amounts: Fraud vs Non-Fraud')
    plt.xlabel('Transaction Amount')
    plt.ylabel('Frequency')
    plt.legend()
    plt.xlim(0, df['amount'].quantile(0.99))  # Limit x-axis to the 99th percentile to reduce the effect of outliers

    plt.tight_layout()
    plt.show()

    # Call exercise_custom to get summary statistics
    stats = exercise_custom(df)

    description = (
        f"The distribution plot shows the frequency of transaction amounts for both fraud and non-fraud transactions. "
        f"The mean transaction amount for fraudulent transactions is {stats['fraud_mean']:.2f}, while the median is {stats['fraud_median']:.2f}. "
        f"For non-fraudulent transactions, the mean amount is {stats['non_fraud_mean']:.2f}, and the median is {stats['non_fraud_median']:.2f}. "
        f"These insights suggest that larger transaction amounts could be more closely monitored for potential fraud.")
    return description


description = visual_custom(df)
print(description)


#First six tasks example use
# Load the dataset
df = exercise_0('transactions.csv')

# Get column names
print(exercise_1(df))

# Get first 5 rows
print(exercise_2(df, 5))

# Get a random sample of 5 rows
print(exercise_3(df, 5))

# Get unique transaction types
print(exercise_4(df))

# Get top 10 transaction destinations
print(exercise_5(df))

# Get all rows where fraud was detected
print(exercise_6(df))
