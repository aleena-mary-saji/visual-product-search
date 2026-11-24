import torch, transformers, PIL, qdrant_client, fastapi
print("All imports OK")
print("torch", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))
    x = torch.randn(1000, 1000, device="cuda")
    print("GPU test sum:", (x @ x).sum().item())