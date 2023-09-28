from newspaper import Article
import urllib.parse as urlparse
import requests
import time
from posixpath import split
from title_of_web import title_for_second

def article_summary(text_web):

    API_URL = "https://api-inference.huggingface.co/models/vishw2703/unisumm_3"
    headers = {
        "Authorization": "Bearer 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"}
    data = str(text_web)
            #minL=int(input("Enter the minimum length :"))
            #maxL=int(input("Enter the maxmimum length : "))
    def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload).json()
            #time.sleep(50)
            print(f"\n--------------------xxxxxxxxxx--------------------\n{(response)}\n--------------------xxxxxxxxxx--------------------\n")
            # exit(0)
            while isinstance(response, dict):
                time.sleep(0.00002)     

            return response
    output = str(query({
            "inputs": data,
           "parameters":{"min_length":150,"max_length":165},
            # "min_length":minL,
       }))
    article_summary=output    

    sq1=article_summary.replace("[{'summary_text': ' ","")

    sq2=sq1.replace("'}]","")


    dq1=sq2.replace("[{'summary_text': \"","")

    dq2=dq1.replace("\"}]","")

    last_sum=dq2.replace("\\","")

    file=last_sum
    count=0
    for i in range (0, len (file)):   
        #Checks whether given character is a punctuation mark  
        if file[i] in ("."):  
            count = count + 1;  

    final_string='.'.join(file.split('.')[:count])

    final_sum=(final_string+".")
    
    return final_sum



    
