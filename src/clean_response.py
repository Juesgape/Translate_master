def clean_response(response_text):
    final_answer = []
    #The response_text is separated by '---'
    responses = response_text.split('---')
    #Removing any unnecessary brackets
    response_list = [response.strip() for response in responses]

    for response in response_list:
        #Preventing empty string to be saved
        if len(response) < 1:
            continue
        final_answer.append(response)

    return final_answer