import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from datetime import datetime
from sklearn.utils import shuffle
from app import settings


class Model(nn.Module):
    def __init__(self, n_users, n_items, embed_dim, n_hidden=1024):
        super(Model, self).__init__()
        self.N = n_users
        self.M = n_items
        self.D = embed_dim

        self.u_emb = nn.Embedding(self.N, self.D)
        self.m_emb = nn.Embedding(self.M, self.D)
        self.fc1 = nn.Linear(2 * self.D, n_hidden)
        self.fc2 = nn.Linear(n_hidden, 1)

        self.u_emb.weight.data = nn.Parameter(
            torch.Tensor(np.random.randn(self.N, self.D) * 0.01))
        self.m_emb.weight.data = nn.Parameter(
            torch.Tensor(np.random.randn(self.M, self.D) * 0.01))

    def forward(self, u, m):
        u = self.u_emb(u)
        m = self.m_emb(m)

        out = torch.cat((u, m), 1)

        out = self.fc1(out)
        out = F.relu(out)
        out = self.fc2(out)
        return out


model = Model(settings.N_USERS, settings.N_PRODUCTS,
              settings.DIMENSION)

criterion = nn.MSELoss()

optimizer = torch.optim.SGD(model.parameters(), lr=0.08, momentum=0.9)


def fit(model, criterion, optimizer, train_data, test_data, epochs,
        bs=512):
    train_users, train_products, train_ratings = train_data
    test_users, test_products, test_ratings = test_data

    train_losses = np.zeros(epochs)
    test_losses = np.zeros(epochs)

    # batches per epoch
    Ntrain = len(train_users)
    batches_per_epoch = int(np.ceil(Ntrain / bs))

    for it in range(epochs):
        t0 = datetime.now()
        train_loss = []

        # shuffle each batch
        train_users, train_products, train_ratings = shuffle(
            train_users, train_products, train_ratings
        )

        for j in range(batches_per_epoch):
            # get the batch
            users = train_users[j * bs:(j + 1) * bs]
            products = train_products[j * bs:(j + 1) * bs]
            targets = train_ratings[j * bs:(j + 1) * bs]

            # conver to tensor
            users = torch.from_numpy(users).long()
            products = torch.from_numpy(products).long()
            targets = torch.from_numpy(targets)

            # reshape targets
            targets = targets.view(-1, 1).float()

            # zero the parameter gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(users, products)
            loss = criterion(outputs, targets)

            # Backward and optimize
            loss.backward()
            optimizer.step()

            train_loss.append(loss.item())

        # Get train loss and test loss
        train_loss = np.mean(train_loss)  # a little misleading

        # we could do this if the test set size was manageable
        # test_outputs = model(test_users, test_movies)
        # test_loss = criterion(test_outputs, test_ratings).item()
        test_loss = []
        for j in range(int(np.ceil(len(test_users) / bs))):
            # get the batch
            users = test_users[j * bs:(j + 1) * bs]
            products = test_products[j * bs:(j + 1) * bs]
            targets = test_ratings[j * bs:(j + 1) * bs]

            # conver to tensor
            users = torch.from_numpy(users).long()
            products = torch.from_numpy(products).long()
            targets = torch.from_numpy(targets)

            # reshape targets
            targets = targets.view(-1, 1).float()

            outputs = model(users, products)
            loss = criterion(outputs, targets).item()
            test_loss.append(loss)
        test_loss = np.mean(test_loss)

        # Save losses
        train_losses[it] = train_loss
        test_losses[it] = test_loss

        dt = datetime.now() - t0
        print(f'Epoch {it + 1}/{epochs}, Train Loss: {train_loss:.4f}, '
              f'Test Loss: {test_loss:.4f}, Duration: {dt}')


current_user_id = 0
custom_user_map = {}
current_movie_id = 0
custom_movie_map = {}


def map_user_id(row):
    global current_user_id, custom_user_map
    old_user_id = row['user']
    if old_user_id not in custom_user_map:
        custom_user_map[old_user_id] = current_user_id
        current_user_id += 1
    return custom_user_map[old_user_id]


def map_movie_id(row):
    global current_movie_id, custom_movie_map
    old_movie_id = row['product']
    if old_movie_id not in custom_movie_map:
        custom_movie_map[old_movie_id] = current_movie_id
        current_movie_id += 1
    return custom_movie_map[old_movie_id]
