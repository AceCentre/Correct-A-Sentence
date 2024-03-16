import csv
from happytransformer.happy_text_to_text import HappyTextToText, TTTrainArgs
from happytransformer import HappyGeneration
from datasets import load_dataset
import os
os.environ["WANDB_API_KEY"] = "339e8cbc62b895edfe6f9f7476adf12a96dd3ed6"

import pandas as pd
from pathlib import Path

def remove_non_string_rows(df, columns):
    indices_to_remove = set()
    for column in columns:
        for i, entry in enumerate(df[column]):
            if not isinstance(entry, str):
                indices_to_remove.add(i)
    if indices_to_remove:
        print(f"Removing rows with non-string entries in the following indices: {sorted(indices_to_remove)}")
        df = df.drop(index=list(indices_to_remove)).reset_index(drop=True)
    else:
        print("No non-string entries found in the specified columns.")
    return df, indices_to_remove



def main():
    happy_tt = HappyTextToText("T5", "t5-small")

    train_csv_path = "clean_train.csv"
    eval_csv_path = "clean_eval.csv"


    train_args = TTTrainArgs(
                        num_train_epochs=3,
                        learning_rate=5e-5,
                        batch_size=16,
                        fp16=True,
                        report_to = ('wandb'),
                        project_name = "t5-mini-grammar",
                        run_name = "grammar-correction",
                        save_steps = 1000,
                        output_dir = "happytransformer",
                        save_path = "t5-small-spoken-typo-new"
                        # deepspeed="ZERO-2"
    )

    happy_tt.train(train_csv_path, args=train_args, eval_filepath=eval_csv_path)
    happy_tt.save("t5-small-spoken-typo-new")

if __name__ == "__main__":
    # Specify your CSV file paths
    train_csv_path = "train.csv"
    eval_csv_path = "eval.csv"
    
    # Load the CSV files into pandas DataFrames
    train_df = pd.read_csv(train_csv_path)
    eval_df = pd.read_csv(eval_csv_path)
    
    # Clean the DataFrames
    train_df_clean, _ = remove_non_string_rows(train_df, ['input', 'target'])  # Adjust column names as needed
    eval_df_clean, _ = remove_non_string_rows(eval_df, ['input', 'target'])  # Adjust column names as needed
        # Save the cleaned DataFrames to new CSV files
    clean_train_csv_path = "clean_train.csv"
    clean_eval_csv_path = "clean_eval.csv"
    train_df_clean.to_csv(clean_train_csv_path, index=False)
    eval_df_clean.to_csv(clean_eval_csv_path, index=False)
    
    main()