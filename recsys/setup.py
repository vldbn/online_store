import json
import torch
from app import settings
from model import net


def setup():
    """Creates model's for first usage."""

    n_users = settings.N_USERS
    n_products = settings.N_PRODUCTS
    dimension = settings.DIMENSION
    model = net.Model(n_users, n_products, dimension)
    torch.save(model.state_dict(), './model/state')

    m = {"users": {}}
    with open('./model/map.json', 'w') as f:
        json.dump(m, f)


if __name__ == '__main__':
    setup()
