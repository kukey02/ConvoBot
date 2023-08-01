#python -m uvicorn main:app
#python -m uvicorn main:app --reload

# Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse 
from starlette.middleware.cors import CORSMiddleware
from decouple import config 
import openai

# Custom Function Imports
from functions.text_to_speech import convert_text_to_speech
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text , get_chat_response

#initiate App
app = FastAPI()


#CORS -Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:8000",
]


#CORS -middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)
 

#check health
@app.get("/health")
async def check_health():
    return {"message": "Health"}

#reset messages 
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return{"message":"conversation reset"}

#AYLI bot response
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")
    
    #decode audio
    message_decoded = convert_audio_to_text(audio_input)
    
    # ensure message decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decode")
    
    #get chat response
    chat_response = get_chat_response(message_decoded)
    #store messages 
    store_messages(message_decoded,chat_response)

    
    # ensure message decoded
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to get chat response")

    # convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get eleven labs audio response")
    
    # create a generator that yiels chunks of data
    def iterfile():
        yield audio_output
        
    return StreamingResponse(iterfile(), media_type="application/octet-stream")
    
    
    