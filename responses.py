import database

responses = database.fetch_responses()

def handle_response(message: str) -> str:
    p_message: str = message.lower()
    
    for response in responses:
        if response[1] == p_message:  
            return response[2]
    
    return 'huh?'