import os
import json
import random

def get_recent_messages():
    file_name = "stored_data.json"
    learn_instructions = {
        "role" : "system",
        "content": "Your name is ayli.you are a conversational bot assist the user with anything he asks help for."
        }
    #initialize messages 
    messages = []
    
    # add a random element
    x = random.uniform(0,1)
    if x < 0.2:
        learn_instructions["content"] = learn_instructions["content"] + "Your response will have some light humour. "
    elif x < 0.5:
        learn_instructions["content"] = learn_instructions["content"]+ "Your response will include an interesting new fact about the congoing conversation topic."
    else:
        learn_instructions["content"] = learn_instructions["content"]+ "Your response will have some dry humor"
        
    # append instruction to messages
    messages.append(learn_instructions)
    
    #get last messages 
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
            
            #append last 5 items of data
            if data:
                if len(data) < 10:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-10:]:
                        messages.append(item)
    except:
        pass
    
    return messages

#store messages
def store_messages(request_message , response_message):
   
    file_name = "stored_data.json"
    
    #get recent messages
    messages = get_recent_messages()[2:]
    
    #add messages to data
    user_message = {"role":"user","content": request_message}
    assistant_message = {"role":"assistant","content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)
    
    # save the updated file 
    with open(file_name, "w") as f:
        json.dump(messages,f)
        
    #reset messages
def reset_messages():
    file_name = "stored_data.json"
    open(file_name, "w")
    