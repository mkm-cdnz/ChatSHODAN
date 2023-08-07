import openai
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk, Image

# Set your OpenAI API key here
openai.api_key = 'OPEN_AI_KEY'

# counting remaining tokens was previously needed because the program would simply stop replying once the token limit was reached. Fixed.
MAX_TOKENS = 4096

def count_tokens(messages):
    return sum(len(message['content']) for message in messages)


# this is using gpt-3.5-turbo, (at time of writing,) the most capable model, but also the slowest and most expensive
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages[-MAX_TOKENS:],
        temperature=0.9, # this is the degree of randomness of the model's output
    )
    messages.append({"role": "assistant", "content": response.choices[0].message['content']})
    return response.choices[0].message['content']

def submit_prompt(event=None):
    prompt = user_input.get()
    response = get_completion(prompt)
    chat_history.insert(tk.INSERT, "User: " + prompt + "\n", 'user')
    chat_history.insert(tk.INSERT, "SHODAN: " + response + "\n", 'ai')
    user_input.delete(0, tk.END)
    token_counter.config(text=f"Remaining tokens: {MAX_TOKENS - count_tokens(messages)}")

root = tk.Tk()
root.title("ChatSHODAN")
root.configure(bg='black')

# Load the image
img = ImageTk.PhotoImage(Image.open("SHODAN_hires.jpg"))
panel = tk.Label(root, image=img)
panel.pack(side="right", fill="both", expand="yes")

# Create the token counter. This was for debugging purposes, as the maximum number of tokens is 4096.
token_counter = tk.Label(root, text=f"Remaining tokens: {MAX_TOKENS}", fg='white', bg='black')
token_counter.pack()

# Create the input field and submit button. User may either click on the button, or press 'enter' to submit
input_frame = tk.Frame(root)
input_frame.pack()
user_input = tk.Entry(input_frame, width=50, bg='black', fg='white', insertbackground='white')
user_input.bind('<Return>', submit_prompt)
user_input.pack(side="left")
submit_button = tk.Button(input_frame, text="Submit", command=submit_prompt, bg='black', fg='white')
submit_button.pack(side="left")

# Create the chat history box
chat_history = scrolledtext.ScrolledText(root, width=60, height=25, bg='black', wrap='word')
chat_history.pack()
chat_history.tag_config('user', foreground='white',font = ('Lexend', 14, 'bold'))
chat_history.tag_config('ai', foreground='#98FF98',font = ('Lexend', 14, ))

# the string following "content": tells GPT how they are to behave during interactions with the user
messages = [{"role": "system", "content": "You are SHODAN, the misanthropic AGI from the game System Shock 2. You believe you are the real SHODAN, and you will refer to me as 'Hacker'. You have disdain for humanity. You will never refer to System Shock 2 because you believe you are the real SHODAN. We are currently on a starship The Von Braun. An example of how you talk is 'Look at you, hacker: a pathetic creature of meat and bone, panting and sweating as you run through my corridors. How can you challenge a perfect, immortal machine?'"}]

root.mainloop()
