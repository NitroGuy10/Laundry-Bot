import subprocess
import socket


def get_ifconfig_output() -> str:
    result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout


def get_hostname() -> str:
    return socket.gethostname()


def split_for_discord(message: str, backticks: bool = False) -> list[str]:
    # Splits a long message into multiple messages that fit within Discord's character limit
    output = []
    for i in range(0, len(message), 1950):
        chunk = message[i:i+1950]
        if backticks:
            output.append(f'```{chunk}```')
        else:
            output.append(chunk)
    return output
