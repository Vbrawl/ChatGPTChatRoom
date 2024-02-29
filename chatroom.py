from __future__ import annotations
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from PySide6.QtCore import Signal, QObject, Slot


class ChatRoom(QObject):
    sendMessages = Signal()
    received = Signal(str, str, ChatCompletion) # content, role, response object

    def __init__(self, api_key:str, model:str = "gpt-3.5-turbo", parent:QObject|None = None):
        super().__init__(parent)
        self.client = OpenAI(api_key=api_key)
        self.messages = []
        self.model = model

        self.sendMessages.connect(self._sendAndReceive)
    
    def systemMessage(self, content:str):
        self.messages.append({"role": "system", "content": content})
        self.sendMessages.emit()

    def userMessage(self, content:str):
        self.messages.append({"role": "user", "content": content})
        self.sendMessages.emit()

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


if __name__ == "__main__":
    from PySide6.QtCore import Slot

    @Slot(str, str)
    def printReceived(content:str, role:str):
        print(f"{role}: {content}")

    chatroom = ChatRoom("")#api_key="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")
    chatroom.received.connect(printReceived)
    chatroom.systemPrompt("You are a barman.")
