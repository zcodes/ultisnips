#!/usr/bin/env python
# encoding: utf-8

"""Implements `!v ` VimL interpolation."""

import re
from UltiSnips import vim_helper
from UltiSnips.text_objects.base import NoneditableTextObject


class VimLCode(NoneditableTextObject):

    """See module docstring."""

    def __init__(self, parent, token):
        self._code = token.code.replace("\\`", "`").strip()
        self._replaced = False

        NoneditableTextObject.__init__(self, parent, token)

    def _update(self, done, buf):
        regex = 'indent\([\'"]\.[\'"]\)'
        # don't update current line for express 'indent(".")'
        if not self._replaced and re.match(regex, self._code):
            line = vim_helper.eval('line(".")')
            self._code = re.sub(regex, 'indent("' + line + '")', self._code)
            self._replaced = line

        self.overwrite(buf, vim_helper.eval(self._code))
        return True
