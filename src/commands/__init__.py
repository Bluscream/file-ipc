from logging import info

from src.commands.ListFiles import ListFiles


class commands:
    @staticmethod
    def handle(request):
        request: str = request.splitlines()
        command = request[0].lower()
        info("commands > Got command %s", command)
        match command:
            case "listfiles":
                return ListFiles.handle(dir=request[1], pattern=request[2])
