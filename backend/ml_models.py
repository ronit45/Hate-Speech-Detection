import torch
import torch.nn as nn

class ThreatMLP(nn.Module):
    def __init__(self, input_dim):
        super(ThreatMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 3)
        )
        
    def forward(self, x):
        return self.network(x)
