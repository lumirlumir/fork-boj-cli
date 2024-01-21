from boj.browsers.login_browser import LoginBrowser
from boj.core import auth
from boj.core import constant
from boj.core import util
from boj.core.base import Command
from boj.core.out import BojConsole


class LoginCommand(Command):
    def execute(self, args):
        console = BojConsole()
        with console.status("Preparing login browser...") as status:
            browser = LoginBrowser(constant.boj_login_url())
            browser.open()
            credential = browser.wait_for_login()
            browser.close()

            status.update("Creating an encryption key...")
            key = auth.create_key()

            status.update("Encrypting the credential...")
            encrypted = auth.encrypt(key, credential.to_json())

            status.update("Writing to file...")
            util.write_file(constant.key_file_path(), key)
            util.write_file(constant.credential_file_path(), encrypted)

        console.print("[green]Login succeeded")