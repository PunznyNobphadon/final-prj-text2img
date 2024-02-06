import torch

torch.backends.cudnn.benchmark = False  # ตั้งค่า cudnn.benchmark เป็น False เพื่อเปิดใช้ max_split_size_mb
torch.backends.cudnn.enabled = True  # ตั้งค่า cudnn.enabled เป็น True เพื่อเปิดใช้สิ่งอื่นๆ ของ cudnn

torch.cuda.set_per_process_memory_fraction(1.0, device=0)  # ตั้งค่าตามที่คุณต้องการ