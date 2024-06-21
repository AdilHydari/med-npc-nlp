from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
device = "mps"  # cuda or cpu
checkpoint = "dmis-lab/meerkat-7b-v1.0"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(
    checkpoint,
    torch_dtype=torch.bfloat16,  # You can choose to use this when there's not enough GPU memory available.
)

# Multi-turn dialogue example
messages = [
    {"role": "system", "content": "The following is a multiple-choice question about medical knowledge. Solve this in a step-by-step fashion, starting by summarizing the available information. Output a single option from the given options as the final answer. You are strongly required to follow the specified output format; conclude your response with the phrase \"the answer is ([option_id]) [answer_string]\".\n\n"},
    {"role": "user", "content": "Two weeks after undergoing an emergency cardiac catherization with stenting for unstable angina pectoris, a 61-year-old man has decreased urinary output and malaise. He has type 2 diabetes mellitus and osteoarthritis of the hips. Prior to admission, his medications were insulin and naproxen. He was also started on aspirin, clopidogrel, and metoprolol after the coronary intervention. His temperature is 38\u00b0C (100.4\u00b0F), pulse is 93/min, and blood pressure is 125/85 mm Hg. Examination shows mottled, reticulated purplish discoloration of the feet. Laboratory studies show:\nHemoglobin count 14 g/dL\nLeukocyte count 16,400/mm3\nSegmented neutrophils 56%\nEosinophils 11%\nLymphocytes 31%\nMonocytes 2%\nPlatelet count 260,000/mm3\nErythrocyte sedimentation rate 68 mm/h\nSerum\nUrea nitrogen 25 mg/dL\nCreatinine 4.2 mg/dL\nRenal biopsy shows intravascular spindle-shaped vacuoles. Which of the following is the most likely cause of this patient's symptoms?\" (A) Renal papillary necrosis (B) Cholesterol embolization (C) Eosinophilic granulomatosis with polyangiitis (D) Polyarteritis nodosa"},
]


encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

model_inputs = encodeds.to(device)
model.to(device)

generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True, pad_token_id=tokenizer.eos_token_id)
decoded = tokenizer.batch_decode(generated_ids)
print(decoded[0])
