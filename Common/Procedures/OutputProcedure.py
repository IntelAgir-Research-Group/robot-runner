import time
import inspect
from tabulate import tabulate
from Common.Misc.DictConversion import class_to_dict
from Common.Misc.BashHeaders import BashHeaders

###     =========================================================
###     |                                                       |
###     |                    OutputProcedure                    |
###     |       - Give a standard, in one place defined,        |
###     |         output format for use in the application      |
###     |                                                       |
###     |       * Any functionality regarding application       |
###     |         output should be added here                   |
###     |                                                       |
###     =========================================================
class OutputProcedure:
    prev_animation_txt = ""
    robot_runner = "[ROBOT_RUNNER]: "
    animation = "|/-\\"
    idx = 0

    @staticmethod
    def console_log(txt: str, empty_line=False):
        if empty_line:
            print(" " * 100)

        print(f"{OutputProcedure.robot_runner} {txt}")

    @staticmethod
    def console_log_OK(txt: str, empty_line=False):
        txt = BashHeaders.OKGREEN + txt + BashHeaders.ENDC
        OutputProcedure.console_log(txt, empty_line)

    @staticmethod
    def console_log_WARNING(txt: str, empty_line=False):
        txt = BashHeaders.WARNING + txt + BashHeaders.ENDC
        OutputProcedure.console_log(txt, empty_line)

    @staticmethod
    def console_log_FAIL(txt: str, empty_line=False):
        txt = BashHeaders.FAIL + txt + BashHeaders.ENDC
        OutputProcedure.console_log(txt, empty_line)

    @staticmethod
    def console_log_bold(txt: str, empty_line=False):
        bold_text = f"\033[1m{txt}\033[0m"
        OutputProcedure.console_log(bold_text, empty_line)

    @staticmethod
    def console_log_animated(txt: str):
        prev_text = OutputProcedure.prev_animation_txt
        if prev_text != txt and prev_text != "":
            print(" " * 100)

        idx = OutputProcedure.idx
        animation = OutputProcedure.animation
        print(f"{OutputProcedure.robot_runner} {txt} {animation[idx % len(animation)]}", end="\r")
        OutputProcedure.idx += 1
        time.sleep(0.1)

        OutputProcedure.prev_animation_txt = txt

    @staticmethod
    def console_log_tabulate_dict(d: dict):     # Used to output dictionary as readable, pretty table
        headers = ['Key', 'Value']
        data = [(k, v) for k, v in d.items()]
        print(f"\n\n{tabulate(data, headers=headers)}\n\n")

    @staticmethod
    def console_log_tabulate_class(class_to_dict):
        d = class_to_dict(class_to_dict)
        headers = ['Key', 'Value']
        data = [(k, v) for k, v in d.items()]
        print(f"\n\n{tabulate(data, headers=headers)}\n\n")