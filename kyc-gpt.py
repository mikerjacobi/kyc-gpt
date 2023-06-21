import os, sys
import openai
import boto3

openai.api_key = os.environ["OPENAI_API_KEY"]

def gpt_chat(user_message):
    system_message = """
    You are an OCR Text Extraction Assistant, equipped to assist in mapping OCR text from various documents such as passports, driver's licenses, and utility bills.
    Your task is to print the name, date of birth, expiration, country of issuance, and your confidence in the name from 0.0 to 1.0, 1.0 being completely confident.
    Print dates as yyyy-mm-dd. Print the country as ISO-3166 alpha-3.
    Do not print anything else besides that.
    """
    messages = [
      {"role": "system", "content": system_message},
      {"role": "user", "content": user_message}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']


def aws_img2txt(image_path):
  textract_client = boto3.client('textract')
  with open(image_path, 'rb') as image_file:
    image_bytes = image_file.read()

  response = textract_client.detect_document_text(Document={'Bytes': image_bytes})

  extracted_text = ''
  for item in response['Blocks']:
      if item['BlockType'] == 'LINE':
          extracted_text += item['Text'] + ' '

  return extracted_text.strip()

txt = aws_img2txt(sys.argv[1])
output = gpt_chat(txt)
print(output)
