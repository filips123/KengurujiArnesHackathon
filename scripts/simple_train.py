import copy
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def train_model(target_gauge_id, predict_next_hours):
    print(f"Training model for {target_gauge_id} for {predict_next_hours} hours")

    data = pd.read_csv(f"../dataset/processed/simple/{target_gauge_id}/{predict_next_hours}.gz")
    data.dropna(how="any", inplace=True)

    x_data = data.loc[:, (data.columns != "DATE") & (data.columns != "TARGET")]
    y_data = data["TARGET"]

    # Split datasets into train and test
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=42)

    # Normalize datasets with scaler
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Select PyTorch device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Convert to PyTorch tensors
    x_train_tensor = torch.tensor(x_train_scaled, dtype=torch.float32).to(device)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1).to(device)
    x_test_tensor = torch.tensor(x_test_scaled, dtype=torch.float32).to(device)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1).to(device)

    # Instantiate the model
    model = nn.Sequential(
        nn.Linear(x_train_tensor.shape[1], x_train_tensor.shape[1] * 2),
        nn.ReLU(),
        nn.Linear(x_train_tensor.shape[1] * 2, x_train_tensor.shape[1]),
        nn.ReLU(),
        nn.Linear(x_train_tensor.shape[1], x_train_tensor.shape[1] // 4),
        nn.ReLU(),
        nn.Linear(x_train_tensor.shape[1] // 4, 1),
        nn.Softplus(),
    ).to(device)

    # Training parameters
    number_epochs = 500
    learning_rate = 0.0001
    batch_size = 256
    batch_start = torch.arange(0, len(x_train), batch_size)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Hold the best model
    best_mse = np.inf
    best_weights = None
    history = []

    # Training loop
    for epoch in range(number_epochs):
        model.train()

        with tqdm.tqdm(batch_start, unit="batch", mininterval=0) as bar:
            bar.set_description(f"Epoch {epoch}")

            for start in bar:
                # Take a batch
                x_batch = x_train_tensor[start:start + batch_size]
                y_batch = y_train_tensor[start:start + batch_size]

                # Forward pass
                y_pred = model(x_batch)
                loss = criterion(y_pred, y_batch)

                # Backward pass
                optimizer.zero_grad()
                loss.backward()

                # Update weights
                optimizer.step()

                # Print progress
                bar.set_postfix(mse=float(loss))

        # Evaluate accuracy at end of each epoch
        model.eval()
        y_pred = model(x_test_tensor)
        mse = criterion(y_pred, y_test_tensor)
        mse = float(mse)
        history.append(mse)
        if mse < best_mse:
            best_mse = mse
            best_weights = copy.deepcopy(model.state_dict())

    # Restore model and return best accuracy
    model.load_state_dict(best_weights)

    print("MSE: %.2f" % best_mse)
    print("RMSE: %.2f" % np.sqrt(best_mse))

    # Create models directory
    directory = f"../models/simple/{target_gauge_id}"
    os.makedirs(directory)

    # Save the scaler
    dump(scaler, f"{directory}/{predict_next_hours}.bin", compress=True)

    # Save the model
    torch.save(model.state_dict(), f"{directory}/{predict_next_hours}.pth")

    print()


def main():
    predict_next_hours = int(sys.argv[1])

    print("TRAINING MODELS\n")

    for file in Path("../dataset/hydro/aggregated").glob("*.csv"):
        target_gauge_id = int(file.name.replace(".csv", ""))
        train_model(target_gauge_id, predict_next_hours)


main()
