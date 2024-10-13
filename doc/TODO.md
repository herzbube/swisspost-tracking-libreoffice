# TODO list

This file contains notes taken during initial development of the extension about unfinished tasks. This will eventually be superseded by usage of the GitHub issue tracker.

- Add a "Release steps" document. Preliminary notes:
  - Update version in `description.xml`
- Add `<update-information>` element to `description.xml`, to provide a better update experience for the end user. See how it's done in APSO.
- Provide icons for the extension itself (in `description.xml`) and for any of its GUI elements (in `AddonUI.xcu`).
- Provide German translation.
- Find out whether there is a minimal version of LibreOffice required. If yes, add the `<dependencies>` element to `description.xml`. See how it's done in APSO.
- Find a way how to prevent duplication of the LICENSE file. Currently the file is present in the Git repo root folder, but also in the `src` folder so that it can be easily packaged.
