import torch
import datasets
from network import MLP
import matplotlib.pyplot as plt
import runners
from tqdm import tqdm as tdqm

train_dataset, val_dataset, test_dataset = datasets.load_data_set("data/nerf_synthetic", "tiny_lego")
train_data_loader = torch.utils.data.DataLoader(train_dataset, batch_size=1, shuffle=True, num_workers=0)
val_data_loader = torch.utils.data.DataLoader(val_dataset, batch_size=1, shuffle=True, num_workers=0)

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
criterion = torch.nn.MSELoss()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
# device = torch.device("cpu")

with tdqm( range(100) ) as t:
    for i in t:
        runners.train_epoch(model,optimizer,criterion,train_data_loader,device=device)
        if i % 5 == 0:
            runners.valid_epoch(model,optimizer,criterion,val_data_loader,device=device)
    torch.save(model.state_dict(), "model.pth")
