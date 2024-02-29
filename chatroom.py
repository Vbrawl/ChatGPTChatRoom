from __future__ import annotations
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from PySide6.QtCore import Signal, QObject, Slot


class ChatRoom(QObject):
    received = Signal(str, str, ChatCompletion) # content, role, response object

    def __init__(self, api_key:str, model:str = "gpt-3.5-turbo", parent:QObject|None = None):
        super().__init__(parent)
        self.client = OpenAI(api_key=api_key)
        self.messages = []
        self.model = model

    @Slot(str)
    def systemMessage(self, content:str):
        self.messages.append({"role": "system", "content": content})
        self._sendAndReceive()

    @Slot(str)
    def userMessage(self, content:str):
        self.messages.append({"role": "user", "content": content})
        self._sendAndReceive()

    @Slot()
    def _sendAndReceive(self):
        response = self.client.chat.completions.create(
            model=self.model,
            # response_format={"type": "json_object"},
            messages=self.messages
        )
        choice = response.choices[0]
        self.messages.append({"role": choice.message.role, "content": choice.message.content})
        self.received.emit(choice.message.content, choice.message.role, response)

    @Slot()
    def resetSession(self):
        self.messages = []

    @Slot(str)
    def updateApiToken(self, apiToken):
        self.client = OpenAI(api_key = apiToken)


if __name__ == "__main__":
    from PySide6.QtCore import Slot

    @Slot(str, str)
    def printReceived(content:str, role:str):
        print(f"{role}: {content}")

    chatroom = ChatRoom("")
    chatroom.received.connect(printReceived)
    chatroom.systemPrompt("You are a barman.")
