class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, user_input, agent_response):
        self.history.append({"user": user_input, "agent": agent_response})

    def get_context(self, n=3):
        return self.history[-n:]
