# import torch

# print(torch.cuda.is_available())
# print(torch.version.cuda)
# print(torch.cuda.get_device_name(0))


# import tensorflow as tf
# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
# print(tf.__version__)


from transformers import AutoModelForSequenceClassification
import torch
print('here1')
model = AutoModelForSequenceClassification.from_pretrained("google-bert/bert-base-uncased")
model.config.pad_token_id