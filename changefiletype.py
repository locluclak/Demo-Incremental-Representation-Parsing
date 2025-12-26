import torch
from transformers import AutoModel

# Đường dẫn đến thư mục chứa các file của bạn
MODEL_PATH = 'en_label_gpt2_medium_cat256' 

# Tải mô hình từ thư mục cục bộ. 
# Thay 'AutoModel' bằng lớp mô hình chính xác (ví dụ: 'AutoModelForSequenceClassification' nếu có)
# Nếu là mô hình Benepar GPT-2, bạn có thể cần kiểm tra lớp chính xác Benepar sử dụng.
model = AutoModel.from_pretrained(MODEL_PATH)
# Lưu toàn bộ state dictionary (trọng số) của mô hình
torch.save(model.state_dict(), 'model/benepar_model.pt')

# HOẶC Lưu toàn bộ đối tượng mô hình (ít phổ biến hơn cho deployment)
# torch.save(model, 'full_benepar_model.pt')