# -----------------------------------------------------------------------------
# Copyright 2024 Patrick Näf (herzbube@herzbube.ch)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import sys
import unohelper
import officehelper
from com.sun.star.task import XJobExecutor

EXTENSION_ID = 'swisspost-tracking-libreoffice.ch.herzbube'

def writeIntoTextDocument(desktop, textToAdd):
    xModel = desktop.getCurrentComponent()
    if not hasattr(xModel, "Text"):
        xModel = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())
    text = xModel.Text
    cursor = text.createTextCursor()
    text.insertString(cursor, textToAdd + "\n", 0)

def showMessageBox(desktop, message, title):
    from com.sun.star.awt.MessageBoxType import MESSAGEBOX, INFOBOX, WARNINGBOX, ERRORBOX, QUERYBOX
    from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK, BUTTONS_OK_CANCEL, BUTTONS_YES_NO, BUTTONS_YES_NO_CANCEL, BUTTONS_RETRY_CANCEL, BUTTONS_ABORT_IGNORE_RETRY
    from com.sun.star.awt.MessageBoxResults import OK, YES, NO, CANCEL

    xModel = desktop.getCurrentComponent()
    xController = xModel.getCurrentController()
    xFrame = xController.getFrame()
    xWindow = xFrame.getContainerWindow()
    xToolkit = xWindow.getToolkit()

    eType = MESSAGEBOX
    nButtons = BUTTONS_OK_CANCEL

    xMessageBox = xToolkit.createMessageBox(xWindow, eType, nButtons, title, message)
    xMessageBox.execute()

class TheJobExecutor(unohelper.Base, XJobExecutor):
    # When invoked from within LibreOffice, context is an XComponentContext.
    # This is notably different from Python macros which operate with an XScriptContext (available via global XSCRIPTCONTEXT)
    def __init__(self, context):
        self.context = context

        # Type = XMultiComponentFactory
        # Can also be retrieved with property syntax (context.ServiceManager)
        self.serviceManager = self.context.getServiceManager()

        # Type = XDesktop2
        self.desktop = self.serviceManager.createInstanceWithContext("com.sun.star.frame.Desktop", self.context)

    # When invoked from a menu item, args is the string supplied to the service as an URL parameter
    def trigger(self, args):
        if args == "":
            showMessageBox(self.desktop, "Hello World: No arguments", "Amazing!")
        elif args == "AllDocuments":
            showMessageBox(self.desktop, "Hello World: All documents", "Amazing!")
        elif args == "Writer":
            showMessageBox(self.desktop, "Hello World: Writer document", "Amazing!")
        elif args == "Calc":
            showMessageBox(self.desktop, "Hello World: Calc document", "Amazing!")
        else:
            showMessageBox(self.desktop, "Hello World: Unexpected argument", "Amazing!")

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(TheJobExecutor, EXTENSION_ID + ".implementation", ("com.sun.star.task.Job",), )
