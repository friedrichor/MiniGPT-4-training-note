# MiniGPT-4-training-note
A personal note of training MiniGPT-4.

## Prepare the code and the environment

```shell
git clone https://github.com/Vision-CAIR/MiniGPT-4.git
cd MiniGPT-4-training-note
cd MiniGPT-4
conda env create -f environment.yml
conda activate minigpt4
```

## Prepare the datasets

```
cd ..
```

For the subsequent operations, see [LAION_115M/README](https://github.com/friedrichor/MiniGPT-4-training-note/tree/main/LAION_115M)

## Training

```
torchrun --nproc_per_node $NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

`$NUM_GPU` indicates the number of GPUs to be used, such as 1,2,...  
For example, you can run normally with the following instructions:
```
torchrun --nproc_per_node 2 train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```
