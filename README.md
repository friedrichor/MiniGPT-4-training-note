# MiniGPT-4-training-note

A personal note of training MiniGPT-4.

- [MiniGPT-4-training-note](#minigpt-4-training-note)
  - [Prepare the code and the environment](#prepare-the-code-and-the-environment)
  - [Prepare the datasets](#prepare-the-datasets)
  - [Prepare the pretrained Vicuna weights](#prepare-the-pretrained-vicuna-weights)
  - [Training](#training)
    - [Stage 1 pre-training](#stage-1-pre-training)
    - [Stage 2 fine-tuning](#stage-2-fine-tuning)
  - [Demo](#demo)
  - [Debug](#debug)
    - [1. socket error (Training Stage 1)](#1-socket-error-training-stage-1)
    - [2. DDP Error (Training Stage 1)](#2-ddp-error-training-stage-1)
    - [3. Share Demo (Demo)](#3-share-demo-demo)

## Prepare the code and the environment

```bash
git clone https://github.com/Vision-CAIR/MiniGPT-4.git
cd MiniGPT-4-training-note
cd MiniGPT-4
conda env create -f environment.yml
conda activate minigpt4
```

## Prepare the datasets

```bash
cd ..
```

For the subsequent operations, see [LAION_115M/README](LAION_115M)

****

## Prepare the pretrained Vicuna weights

see **[2. Prepare the pretrained Vicuna weights]** in [MiniGPT-4#installation](MiniGPT-4#installation)  

Change `line 16` in the [MiniGPT-4/minigpt4/configs/models/minigpt4.yaml](MiniGPT-4/minigpt4/configs/models/minigpt4.yaml) after downloading(Change this path to your own):

```
llama_model: "/path/to/vicuna/weights/"
```

The structure of this folder is (Take vicuna-7B, for example):
```
├── weights
│   ├── config.json
│   ├── generation_config.json
│   ├── pytorch_model-00001-of-00002.bin
│   ...  
│   ├── pytorch_model.bin.index.json
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   └── tokenizer.model
```


## Training

```bash
cd MiniGPT-4
```

### Stage 1 pre-training

```bash
torchrun --nproc_per_node $NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

`$NUM_GPU` indicates the number of GPUs to be used, such as 1,2,...  

For example, you can run normally the following command:
```bash
torchrun --nproc_per_node 2 train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

It takes about 11 hours to complete the Stage 1 of training(using 3 NVIDIA A6000(48G)).

### Stage 2 fine-tuning

`line 10` in the [MiniGPT-4/train_configs/minigpt4_stage2_finetune.yaml](MiniGPT-4/train_configs/minigpt4_stage2_finetune.yaml) should be replaced with the path to the checkpoint you saved in the Stage 1, such as:

```yaml
  ckpt: 'MiniGPT-4/minigpt4/output/minigpt4_stage1_pretrain/20230527100/checkpoint_3.pth'
```

To download and prepare the Stage 2 dataset, please check [second stage dataset preparation instruction](MiniGPT-4/minigpt4/dataset/README_2_STAGE.md).

`line 5` in the [MiniGPT-4/minigpt4/configs/datasets/cc_sbu/align.yaml](MiniGPT-4/minigpt4/configs/datasets/cc_sbu/align.yaml) should be replaced with the `cc_sbu_align` dataset path you saved, such as:

```yaml
      storage: /datas/llm_datasets/cc_sbu_align
```

Then, run the following command:
```bash
torchrun --nproc_per_node $NUM_GPU train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml
```

If you want to run on a/few specific GPU(s), you can use:
```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --nproc_per_node 2 train.py --cfg-path train_configs/minigpt4_stage2_finetune.yaml
```

## Demo

`line 11` in the [MiniGPT-4/eval_configs/minigpt4_eval.yaml](MiniGPT-4/eval_configs/minigpt4_eval.yaml) should be replaced with the path to the checkpoint you saved in the Stage 2, such as:

```yaml
  ckpt: 'MiniGPT-4/minigpt4/output/minigpt4_stage2_finetune/20230527215/checkpoint_4.pth'
```

Then, run the following command.

```bash
python demo.py --cfg-path eval_configs/minigpt4_eval.yaml  --gpu-id 0
```


<hr>

## Debug

### 1. socket error (Training Stage 1)

error:  
```
RuntimeError: The server socket has failed to listen on any local network address. The server socket has failed to bind to [::]:29500 (errno: 98 - Address already in use). The server socket has failed to bind to 0.0.0.0:29500 (errno: 98 - Address already in use).
```

&emsp;&emsp;If you encounter the above error, it may be that you have run `torchrun --nproc_per_node $NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml`, but did not terminate normally (terminate by `closing the terminal` or `Ctrl + Z`, and normal terminating means stop with `Ctrl + C`). You can solve this problem by following these steps：

```bash
netstat -nlp | grep :29500
```

With the above instruction you might get output in the following format  
`tcp6       0      0 :::29500                :::*                    LISTEN      3964655/python`

```bash
kill -9 3964655
```
&emsp;&emsp;Because the program that was accidentally terminated before is still using memory, it has not really stopped. So kill the process with the `kill -9 {pid}` command.  

Then run the instruction again：
```bash
torchrun --nproc_per_node $NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml
```

<hr>

### 2. DDP Error (Training Stage 1)

error: 
```
torch.distributed.elastic.multiprocessing.api.SignalException: Process 190221 got signal: 1
```

&emsp;&emsp;If you encounter the above error at runtime and it causes the program to terminate, it's probably because you used the `nohup` directive at runtime, that is, it runs through `nohup torchrun --nproc_per_node $NUM_GPU train.py --cfg-path train_configs/minigpt4_stage1_pretrain.yaml`.  

&emsp;&emsp;If you still want run the code on the server, disable the `nohup` directive and use the `screen` directive instead.

&emsp;&emsp;For how to use the `screen` directive, you can refer to [here](https://blog.csdn.net/qq_38101208/article/details/107840725)(a Chinese blog).

### 3. Share Demo (Demo)

&emsp;&emsp;Theoretically, the generated demo web page can be shared with others after `share=True` is set on the last line of `demo.py`.  

&emsp;&emsp;However, currently, the generated demo web page cannot be shared due to some issues with the `gradio`'s latest version.  

&emsp;&emsp;That is, You may encounter the following error:

```
Could not create share link. Please check your internet connection or our status page: https://status.gradio.app
Error while sending telemetry: HTTPSConnectionPool(host='api.gradio.app', port=443): Max retries exceeded with url: /gradio-launched-telemetry/ (Caused by  ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x7f78b24418e0>, 'Connection to api.gradio.app timed out. (connect timeout=3)'))
```

or the output of the program simply stops at the following line(without the sharing site `Running on public URL: http://...`).

```
Running on local URL:  http://127.0.0.1:7863/
```

&emsp;&emsp;If you are running `demo.py` on a server, you can set `server_name` so that the generated page can be shared with others.
&emsp;&emsp;that is, change the last line in `demo.py` to the following format:

```python
demo.launch(share=True, enable_queue=True, server_name="xxx.xxx.xxx.xxx")
```


 
