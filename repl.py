import sys
import signal
from gmail import Mail
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter

MailVerbs=WordCompleter([
           "archive",
           "report Spam",
           "delete",
           "mark as unread",
           "mark as not important",
           "add to tasks",
           "add Star",
           "create Event",
           "mute",
           "inbox",
           "back to inbox",
           ])


if __name__ == "__main__":
    mail=Mail()
    while 1:
        try:
            inp = prompt(u'> ',
                    history=InMemoryHistory(),
                    auto_suggest=AutoSuggestFromHistory(),
                    completer=MailVerbs)
            print(inp)
        except EOFError:
            break
        except KeyboardInterrupt:
            exit()

