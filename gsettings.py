import dotbot
import subprocess

class GSettings(dotbot.Plugin):
    directive = 'gsettings'

    def __init__(self, context):
        super().__init__(context)

    def can_handle(self, directive):
        return directive == self.directive

    def handle(self, directive, data):
        status = True

        for item in data:
            if not self.check_if_set(item):
                if not self.set_value(item):
                    status = False

        return status

    def check_if_set(self, item):
        command = f"gsettings get {item['schema']} {item['key']}"

        process = subprocess.run(command, shell=True, capture_output=True)

        return process.stdout.strip().decode() == item['value']

    def set_value(self, item):
        self._log.info(f"Setting key {item['key']} in schema {item['schema']} to {item['value']}")
        command = f"gsettings set {item['schema']} {item['key']} {item['value']}"

        process = subprocess.run(command, shell=True, capture_output=True)

        if process.returncode != 0:
            self._log.warning(f"Failed to set key {item['key']} in schema {item['schema']}")
            return False

        return True
