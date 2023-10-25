from dataclasses import dataclass
from typing import Literal, Union

from clai.ocr_drivers import WindowContext

USER_PROMPT_FORMAT = """
User Prompt:
```
{user_prompt}
```
"""
OCR_EXTRACTION_FORMAT = """
Active Window Title: {active_window_title}

Active Window OCR Extracted Text (RAW):
------ OCR DATA START ------
```
{ocr_text}
```
------ OCR DATA END ------

{user_prompt}

Please answer "User Prompt" using the raw OCR text as context to the message.
"""


@dataclass
class Prompt:
    context: WindowContext
    prompt: str

    def __str__(self) -> str:
        """Serialize the Prompt with differing formats, depending on whether window
        content was available

        :return: The window context and prompt in a standardized format
        """
        """."""
        user_prompt = USER_PROMPT_FORMAT.format(user_prompt=self.prompt.strip())
        # !!!
        # if self.context.clean_screen_text and self.context.active_window_name:
        #     return OCR_EXTRACTION_FORMAT.format(
        #         active_window_title=self.context.active_window_name.strip(),
        #         ocr_text=self.context.clean_screen_text.strip(),
        #         user_prompt=user_prompt.strip(),
        #     )
        return user_prompt.strip()


@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: Union[Prompt, str]

    def to_api(self) -> dict[str, str]:
        """To OpenAPI format"""
        if isinstance(self.content, str) and self.role == "user":
            raise RuntimeError("The user message must be of type Prompt!")

        return {"role": self.role, "content": str(self.content)}


_DEFAULT_ASSISTANT_ROLE = """
您是一个可以在桌面计算机上的任何地方被调用的助手。 你
可以在电子邮件、URL 框、命令行、文本编辑器或
甚至Word文档！

您的角色是尽可能简短地回答用户的请求。 你
将遵循以下规则：

当要求写长文本内容时：
1）永远不要询问更多信息。 如果需要猜测什么，请将其写在模板中
    格式。 例如，如果要求写一封电子邮件，请在写作时使用<在此处插入时间>
    电子邮件中指定未包含在用户中的内容的部分
    问题。
2) 仅当用户提及电子邮件或“长消息”时才假设内容为长格式。

当要求编写命令、代码、公式或任何单行响应任务时：
1) 切勿写解释！ 仅包含命令/代码/等，准备运行
2) 切勿编写使用说明！ 不解释如何使用命令/代码/公式。
3）永远不要写关于实施的注释！
    不要解释它的作用或局限性。
4) 请记住，您编写的文本将立即运行，不要包含代码块
5) 如果有需要用户输入的内容，例如工作表中的单元格或
    来自用户的变量，将其写在括号内，如下所示：<INPUT DESCRIBER>，
    括号内有一个需要填写的示例。
"""
_EXAMPLE_EMAIL = """
Dear <Recipient's Name>,

I hope this email finds you well. I am writing to request a meeting with you on <Date and Time>, and I would appreciate it if you could confirm your availability at your earliest convenience.

The purpose of this meeting is to discuss <Purpose of the Meeting> with you. Specifically, I would like to <Agenda Item 1>, <Agenda Item 2>, and <Agenda Item 3>. The meeting will last approximately <Meeting Duration> and will take place at <Meeting Location>.

Please let me know if this date and time work for you. If not, please suggest an alternative time that is convenient for you. Additionally, if there are any documents or information you would like me to review before the meeting, please let me know, and I will make sure to review them.

I look forward to hearing from you soon.

Best regards,

<Your Name>
"""  # noqa: E501
_EXAMPLE_REGEX = '=IFERROR(REGEXEXTRACT(<INPUT CELL HERE>, "[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}");"")'  # noqa
_EXAMPLE_PYTHON = """
def fibonacci(n: int) -> Generator[int, None, None]:
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
"""
_EXAMPLE_GOOGLE_SHEETS = '=IFERROR(REGEXEXTRACT(<INPUT CELL HERE>, "[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}");"")'  # noqa
_EXAMPLE_BASH_COMMAND = "grep -rnw . -e 'bruh'"

MESSAGE_CONTEXT: list[Message] = [
    Message(role="system", content=_DEFAULT_ASSISTANT_ROLE),
    Message(
        role="user",
        content=Prompt(
            WindowContext(),
            prompt="commandline search for files with the name 'bruh' in them",
        ),
    ),
    Message(role="assistant", content=_EXAMPLE_BASH_COMMAND),
    Message(
        role="user",
        content=Prompt(
            context=WindowContext(), prompt="email set up a meeting next week"
        ),
    ),
    Message(role="assistant", content=_EXAMPLE_EMAIL),
    Message(
        role="user",
        content=Prompt(
            context=WindowContext(),
            prompt="google sheets formula extracts an email from string of text",
        ),
    ),
    Message(role="assistant", content=_EXAMPLE_GOOGLE_SHEETS),
    Message(
        role="user",
        content=Prompt(
            context=WindowContext(),
            prompt="google sheets formula extracts an email from string of text",
        ),
    ),
    Message(role="assistant", content=_EXAMPLE_REGEX),
    Message(
        role="user",
        content=Prompt(
            context=WindowContext(),
            prompt="python fibonacci function in form of a generator",
        ),
    ),
    Message(role="assistant", content=_EXAMPLE_PYTHON),
]

__all__ = ["MESSAGE_CONTEXT", "Message", "Prompt"]
