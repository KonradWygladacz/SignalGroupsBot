import openai
import config
from telethon import TelegramClient, sync

openai.api_key = config.chat_gpt_aki_key
client = TelegramClient('Testtest1', config.api_id, config.api_hash).start()
def get_message_info():
    prompt = "Write text with this form:\nSymbol\nSide\nEntry zone\nTake profits\nStop loss\n" \
             "For example:\nBTC\nbuy\n1.3, 1.4\n1.5, 1.6, 1.7\n1.2\n" \
             "do not use any characters(like - or =) other than . and ,\n" \
             "Don't write descriptions, like take profit:, symbol:. Also don't write '/USDT' at the end of symbol. Write just the necessary text\n" \
             "Extract these information from this text:\n" \
              + client.get_messages("me", 1)[0].message

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'assistant', "content": prompt}]
    )
    response = completion.choices[0].message.content.upper()

    count = 0

    for char in response:
        if char == "\n":
            count += 1
    print(count)
    print("CHAT")
    print(response)

    return response

