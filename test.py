import openai
import telegram
import asyncio

#set the API key for OpenAI
openai.api_key = "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"

#set the Telegram bot token
bot = telegram.Bot(token="5889933064:AAEaf9kzZSN9rHx0emJ-q1dl17Wd8FKJTqc")

#handle the command received from Telegram
async def handle_command(command, context_id):
# send the command to ChatGPT and get the response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt='Your command: ' + command,
        max_tokens=2048,
        temperature=0.5,
)
# return the response
    return response.choices[0].text

#main loop to listen for commands
async def main():
    offset = None
    context_id = ""
    while True:
        try:
            updates = await bot.get_updates(offset=offset)
        except telegram.error.TimedOut:
            await asyncio.sleep(5)
            continue
        for update in updates:
            if update is not None and update.message is not None and update.message.text is not None and update.message.text.startswith("/command"):
                command = update.message.text[8:]
                response = await handle_command(command, context_id)
                await bot.send_message(chat_id=update.message.chat_id,text=response)
            offset = update.update_id + 1

asyncio.run(main())