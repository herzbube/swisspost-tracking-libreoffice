# LibreOffice Development

This file contains assorted notes on the topic of developing extensions and/or macros for LibreOffice. The notes are heavily biased towards using Python as the programing language.

## References

- [1] [LibreOffice SDK](https://api.libreoffice.org/)
- [2] [GitHub repo with SDK sources](https://github.com/LibreOffice/core/tree/master/odk) - specifically the `examples` subfolder can be interesting to find the raw code for an example shown in the built SDK documentation
- [3] [LibreOffice Developer's Guide: Chapter 4 - Extensions](https://wiki.documentfoundation.org/Documentation/DevGuide/Extensions)
- [4] [LibreOffice Developer's Guide: Chapter 18 - Scripting Framework](https://wiki.documentfoundation.org/Documentation/DevGuide/Scripting_Framework)
- [5] [Reference documentation for the UNO IDL API](https://api.libreoffice.org/docs/idl/ref/index.html)
- [6] [How to integrate exensions into the LibreOffice GUI](https://wiki.documentfoundation.org/Documentation/DevGuide/Writing_UNO_Components#Add-Ons) - essentially a documentation of how to write `.xcu` files
- [7] [Creating a Basic Dialog](https://help.libreoffice.org/latest/en-US/text/sbasic/guide/create_dialog.html)
- [8] [LibreOffice Python Scripts Help](https://help.libreoffice.org/latest/en-US/text/sbasic/python/main0000.html)
- [9] [APSO extension source code](https://gitlab.com/jmzambon/apso)

## Extension basics

The files that make up a LibreOffice extension are packaged and distributed as a ZIP archive. Instead of the `.zip` file extension the archive uses the `.oxt` file extension.

Inside the archive file an extension must conform to a specific filesystem structure, and the content of the extension files must follow certain prerequisites.

### Minimal filesystem structure

```
Archive
+-- META-INF
|   +-- manifest.xml
+-- pkg-description
|   +-- pkg-description.en.txt
+-- registration
|   +-- license.txt
+-- description.xml
+-- main.py
```

Notes:

- `META-INF/manifest.xml`: Contains a list of the main files that make up the extension, notably the entry point Python script. Typically an extension also contains other files that need to be listed in the manifest, such as `.xcu` files (for providing menubar and/or toolbar entries) or dialog library files.
- `description.xml`: Description of the extension in XML format, as displayed in the extension manager. Contains links to one or more description plain text files in different languages as well as to zero or more license plain text files.
  - **Note:** In many examples found in the net the description plain text files are referenced in `manifest.xml` - this is deprecated for modern versions of LibreOffice.
- `pkg-description/pkg-description.en.txt` : Description of the extension in plain text format. Folder and file name can be freely chosen, important is the reference in `description.xml`.
- `registration/license.txt`: License of the extension in plain text format. Folder and file name can be freely chosen, important is the reference in `description.xml`.
- `main.py`: The Python script that contains the extension's entry point. Folder and file name can be freely chosen, important is the reference in `META-INF/manifest.xml`.

### Packaging

When creating the `.oxt` file it is very important that there is no top-level folder in the
archive. For instance, selecting "Compress" in macOS Finder in the context menu of the top-level folder creates an incorrect `.oxt file`.

The command line for creating a correct `.oxt` file looks like this:

    cd src
    zip -r ../build/extension.oxt *

## How to ...

### Find name of menu item or toolbar button for XCU definition

An `.xcu` file may need to refer to an existing menu item or toolbar button, such as "uno:ScriptOrganizer" in the following example snippet:

```
<prop oor:name="MergePoint" oor:type="xs:string">
  <value>.uno:ToolsMenu\.uno:MacrosMenu\.uno:ScriptOrganizer</value>
</prop>
```

To find out the technical name of the thing to reference, open the "Customize" dialog (Tools > Customize...), then navigate to the thing that you want to reference. Hover with the mouse cursor over the thing and in the tooltip you will see

    Command: .uno:<technical name>

You can also use this tooltip method by hovering the mouse cursor over one of the available commands.

### Define a separator menu or toolbar item

A menu item or toolbar item that is a separator can be defined with this snippet:

```
<prop oor:name="URL" oor:type="xs:string">
  <value>private:separator</value>
</prop>
```

Note the "private:separator" value which is used instead of the usual "service:<name>" value.

## Troubleshooting

### Deleting user profile

If the user profile becomes corrupted it may be necessary to delete it entirely. [This page](https://wiki.documentfoundation.org/UserProfile] provides information where the user profile is located on the different platforms. The section "Resolving corruption" documents an interactive way how to reset the user profile.

On macOS cache and user profile can be deleted on the command like this::

    cd ~/Library/Application\ Support/LibreOffice/4
    rm -r cache user
