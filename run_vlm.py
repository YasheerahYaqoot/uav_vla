from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig
from PIL import Image
import requests
import torch
import os
import csv

#os.remove('Answers.txt')
LIST_OF_ANSWERS = []

NUMBER_OF_SAMPLES = len(os.listdir('benchmark-UAV-VLPA-nano-30/images'))
print('NUMBER_OF_SAMPLES',NUMBER_OF_SAMPLES)

# load the processor
processor = AutoProcessor.from_pretrained(
    'cyan2k/molmo-7B-O-bnb-4bit',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto'
)

print('here1')
# load the model
model = AutoModelForCausalLM.from_pretrained(
    'cyan2k/molmo-7B-O-bnb-4bit',
    trust_remote_code=True,
    torch_dtype='auto',
    device_map='auto'
)

print('here2')
# process the image and text
# inputs = processor.process(
#     images=[Image.open(requests.get("https://www.zerogravity.fi/wp-content/uploads/2019/11/satellite-data-e1572891876593-621x556.jpg", stream=True).raw)],
#     text="This is the satellite image of a city. Please, point all the stadiums."
# )

with open('identified_points.txt', 'w') as f:

    for i in range(1, NUMBER_OF_SAMPLES+1):
        print(i)
        string = 'benchmark-UAV-VLPA-nano-30/images/' + str(i) + '.jpg' 
    #process the image and text
        inputs = processor.process(
            images=[Image.open('benchmark-UAV-VLPA-nano-30/images/' + str(i) + '.jpg')],
            text="This is the satellite image of a city. Please, point all the buildings."
        )



    # move inputs to the correct device and make a batch of size 1
        inputs = {k: v.to(model.device).unsqueeze(0) for k, v in inputs.items()}

        #generate output; maximum 200 new tokens; stop generation when <|endoftext|> is generated
        output = model.generate_from_batch(
            inputs,
            GenerationConfig(max_new_tokens=2000, stop_strings="<|endoftext|>"),
            tokenizer=processor.tokenizer
        )

        # with torch.autocast(device_type="cuda", enabled=True, dtype=torch.bfloat16):
        #   output = model.generate_from_batch(
        #       inputs,
        #       GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
        #       tokenizer=processor.tokenizer
        #   )

        # model.to(dtype=torch.bfloat16)
        # inputs["images"] = inputs["images"].to(torch.bfloat16)
        # output = model.generate_from_batch(
        #     inputs,
        #     GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
        #     tokenizer=processor.tokenizer
        # )

        # only get generated tokens; decode them to text
        generated_tokens = output[0,inputs['input_ids'].size(1):]
        generated_text = processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)

        # print the generated text
        print(generated_text)

        f.write(str(i) + ', ' + generated_text + '\n')
        
        # LIST_OF_ANSWERS.append(generated_text)
        
        # # LIST_OF_ANSWERS.append('/n')

        # f.writelines(LIST_OF_ANSWERS)
        # # f.writelines(generated_text)
        # f.write('\n')
        # f.close()
        
f.close()
    


    # for line in LIST_OF_ANSWERS:
    #     f.write(line)
    #     f.write('\n')
    

# with open('Answers.txt', 'w') as f:
#     # f.write(str(LIST_OF_ANSWERS))

#     for line in LIST_OF_ANSWERS:
#         f.write(line)
#         f.write('\n')