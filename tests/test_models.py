from src.spork import models

def test_view_model():
    class ChatMessage(models.ViewModel):
        role: str = "user"
        message: str

        def render(self):
            return f"<b>{self.role}</b>: <span>{self.message}</span>"


    cm = ChatMessage(message="Hello, world!")
    assert cm.display_id is not None
    assert isinstance(cm.display_id, str)

    cm.display()
