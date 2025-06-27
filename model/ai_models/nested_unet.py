import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class NestedUNet(nn.Module):
    def __init__(self, in_ch=3, out_ch=1, base_ch=32, outSize=(256, 256)):
        super().__init__()
        self.out_size = outSize

        # Encoder
        self.conv0_0 = ConvBlock(in_ch, base_ch)
        self.conv1_0 = ConvBlock(base_ch, base_ch * 2)
        self.conv2_0 = ConvBlock(base_ch * 2, base_ch * 4)

        self.pool = nn.MaxPool2d(2, 2)

        # Decoder
        self.up1_0 = nn.ConvTranspose2d(base_ch * 2, base_ch, 2, stride=2)
        self.conv0_1 = ConvBlock(base_ch * 2, base_ch)

        self.up2_0 = nn.ConvTranspose2d(base_ch * 4, base_ch * 2, 2, stride=2)
        self.conv1_1 = ConvBlock(base_ch * 4, base_ch * 2)

        self.up1_1 = nn.ConvTranspose2d(base_ch * 2, base_ch, 2, stride=2)
        self.conv0_2 = ConvBlock(base_ch * 3, base_ch)

        self.final = nn.Conv2d(base_ch, out_ch, kernel_size=1)

    def forward(self, x):
        x0_0 = self.conv0_0(x)
        x1_0 = self.conv1_0(self.pool(x0_0))
        x2_0 = self.conv2_0(self.pool(x1_0))

        x1_1 = self.conv1_1(torch.cat([x1_0, self.up2_0(x2_0)], dim=1))
        x0_1 = self.conv0_1(torch.cat([x0_0, self.up1_0(x1_0)], dim=1))

        x0_2 = self.conv0_2(torch.cat([x0_0, x0_1, self.up1_1(x1_1)], dim=1))

        out = self.final(x0_2)
        out = F.interpolate(
            out, size=self.out_size, mode="bilinear", align_corners=False
        )
        return out
