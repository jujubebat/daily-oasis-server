#!C:\Users\bbwwp\PycharmProjects\DailyOaisBackEnd\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'gprof2dot==2017.9.19','console_scripts','gprof2dot'
__requires__ = 'gprof2dot==2017.9.19'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('gprof2dot==2017.9.19', 'console_scripts', 'gprof2dot')()
    )
