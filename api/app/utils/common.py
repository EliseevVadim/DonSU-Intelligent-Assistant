import gc
import torch


def free_memory():
    gc.collect()
    torch.cuda.empty_cache()
