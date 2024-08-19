from chatbot import ChatBot

if __name__ == "__main__":
    bot = ChatBot()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("Bot: " + bot.responses["goodbye"])
            break
        response = bot.get_response(user_input)
        print("Bot: " + response)
