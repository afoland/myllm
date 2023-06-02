import requests

# This code assumes a version of openassistant is answering the API.
# API is run by oobabooga's text generation webui

# For local streaming, the websockets are hosted without ssl - http://
HOST = 'localhost:5000'
URI = f'http://{HOST}/api/v1/generate'

# For reverse-proxied streaming, the remote will likely host with ssl - https://
# URI = 'https://your-uri-here.trycloudflare.com/api/v1/generate'




import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
# Forces a download and check
assert enc.decode(enc.encode("hello world")) == "hello world"
# To get the tokeniser corresponding to a specific model in the OpenAI API:
# enc = tiktoken.encoding_for_model("gpt-3.5-turbo")



import sys


context_size=2048 # Sum of prompt and reply
response_minimum_room = 500 # Leave at least 500 tokens for response
margin=10 # Just to ensure some margin in the token count


def strip_strings_from_string(strings, original_string):
    for string in strings:
        original_string = original_string.replace(string, '')
    return original_string

def find_first_occurrence(string, substring1, substring2):
    index1 = string.find(substring1)
    index2 = string.find(substring2)

    # Check if both substrings were found
    if index1 != -1 and index2 != -1:
        return min(index1, index2)  # Return the earliest occurrence
    elif index1 != -1:
        return index1  # Only substring1 was found
    elif index2 != -1:
        return index2  # Only substring2 was found
    else:
        return -1  # Neither substring was found

def run(prompt):

    num_tokens=len(enc.encode(prompt, allowed_special={'<|endoftext|>'}))
    token_space=context_size-num_tokens-margin

    request = {
        'prompt': prompt,
        'max_new_tokens': token_space,
        'do_sample': True,
        'temperature': 0.5,
        'top_p': 0.90,
        'typical_p': 1,
        'repetition_penalty': 1.18,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': context_size,
        'ban_eos_token': False,
        'encoder_repetition_penalty': 1,
        'stream': True,
        'skip_special_tokens': False,
        'mode': "default",
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        strings_to_strip = ['</s>', '<|endoftext|>']
#       Return only the response
#       stripped_result = strip_strings_from_string(strings_to_strip, result)
        eos_index = find_first_occurrence(result,strings_to_strip[0],strings_to_strip[1])
        if (eos_index > -1):
            return result[:eos_index]
        else:
#           No endturn found, maybe cut off? [Actually I strip them off]
            return result


        return(stripped_result)


def read_textfile(file_path):
    file = open(file_path, "r")
    content = file.read()
    file.close()
    return content


# Read in the prompter tokens
prompter_token=read_textfile("prompter_token.txt")
assistant_token=read_textfile("assistant_token.txt")
endturn_token=read_textfile("end_turn_token.txt")

if __name__ == '__main__':

    history=[] # For single command-line response this is overkill but lays groundwork
    # Check if the argument exists
    if len(sys.argv) > 1:
        # Get the argument from the command-line
        input_prompt = sys.argv[1]
        history.append(input_prompt)
        # Call the function with the argument

#       Find token space left and truncate prompt if needed
        num_tokens=len(enc.encode(input_prompt, allowed_special={'<|endoftext|>'}))
        tokens_left=context_size-num_tokens-margin

        if tokens_left<response_minimum_room:
            max_prompt_length=context_size-response_minimum_room-margin-margin
            trunc_prompt=enc.decode(input_prompt[-max_prompt_length:])
            input_prompt=trunc_prompt

        prompt=prompter_token + input_prompt + endturn_token + assistant_token
        response=run(prompt)
        history.append(response)
        print(response)
    else:
        print("No argument provided.")


