#!/bin/bash
uv --project ~/ml run /home/cbmiller/Repos/MegaFlow2D_Fork/examples/train.py --dir /home/cbmiller/MegaFlow2D_subsample --dataset MegaFlow2DFromSplitH5 --transform normalize --model FlowMLError --epochs 5 --batch_size 32
