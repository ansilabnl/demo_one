# (c) 2025, Ton Kersten <tonk@ansiblelab.nl>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: grep
    author: Ton Kersten <tonk@ansiblelab.nl>
    version_added: "2.8"
    short_description: grep regexp from file contents
    description:
        - This lookup greps lines that match the regexp from the file and returns the matching lines
    options:
      file:
        description: path(s) of files to read
        type: str
        required: True
      regexp:
        description: Regular expression to search for in the text
        type: str
        required: True
    notes:
      - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
      - this lookup does not understand 'globbing', use the fileglob lookup instead.
"""

EXAMPLES = """
- ansible.builtin.debug:
    msg: "Found 'Hello' in foo.txt {{ lookup('grep', file='/etc/foo.txt', regexp='^Hello') }}"
"""

RETURN = """
  _raw:
    description:
      - content of file(s)
    type: list
    elements: str
"""

from ansible.errors import AnsibleError, AnsibleOptionsError, AnsibleLookupError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_text
from ansible.utils.display import Display
import re

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):

        ret = []
        self.set_options(var_options=variables, direct=kwargs)

        # Get filename
        try:
            fname = kwargs["file"]
        except (NameError, KeyError):
            raise AnsibleOptionsError(self.get_option("file"))

        # Get regular expression
        try:
            regexp = kwargs["regexp"]
        except (NameError, KeyError):
            raise AnsibleOptionsError(self.get_option("regexp"))

        # Show what we have found
        display.vvv(u"File   = %s" % fname)
        display.vvv(u"RegExp = %s" % regexp)

        # Open file and read contents
        with open(fname) as f:
            contents = f.readlines()

        # Check if line matches
        for line in contents:
            if re.search(regexp, line):
                ret.append(line)

        return ret
