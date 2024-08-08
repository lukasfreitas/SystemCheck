from subprocess import CompletedProcess, run, CalledProcessError, PIPE
from dataclasses import dataclass, field
import re, json
from typing import Any, Dict


@dataclass
class DistroReleaseCheck:
    distributor_id: str = field(init=False)
    descriptions: str = field(init=False)
    release: str = field(init=False)
    codename: str = field(init=False)
    process: Any = field(init=False)
    os_info_json: Dict[str, Any] = field(init=False)

    def parse_os_info_to_json(self, info_string):
        # Expressão regular para extrair os atributos
        pattern = re.compile(
            r"Distributor ID:\s*(.*?)\s*Description:\s*(.*?)\s*Release:\s*(.*?)\s*Codename:\s*(.*?)\s*"
        )

        match = pattern.search(info_string)
        if match:
            self.distributor_id, self.descriptions, self.release, self.codename = (
                match.groups()
            )
            os_info_dict = {
                "distributor_id": self.distributor_id,
                "description": self.descriptions,
                "release": self.release,
                "codename": self.codename,
            }

            self.os_info_json = os_info_dict
        else:
            raise ValueError("Formato de string inválido")

    def get_lsb_release_command(self):
        command = []
        command.append("lsb_release")
        command.append("--all")

        return command

    def __post_init__(self):
        # raise FileExistsError("Release command already exists")
        try:
            self.process: CompletedProcess = run(
                self.get_lsb_release_command(), capture_output=True, text=True
            )
            self.parse_os_info_to_json(self.process.stdout)
        except CalledProcessError as e:
            print(e.returncode)
