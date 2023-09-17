# Import module

---

This module is responsible for handling import data to database tables.

---

### Variables description

1. private **__root_import_window** - root window for import module.

2. private **__tk_root_window_title** - title for root tk window

3. private **__import_formats** - available import formats

4. private **__import_folder**  - folder to which  uploaded file will be saved and from which it will be able to read files.

5. private **__files_list_listbox** - listbox object assigned when file open and filled with file names from given directory.

6. private **__selected_file** - selected file from which data will be imported.

---

### Methods description

1. public **open_import_window** - prepare root Tk import window: render upload button, prepare listbox with files in import folder.
   1. **save_selection** - save selected file name.
2. private **__show_existing_files** - show files existing in import folder.
3. private **__upload_new** - handle new file uploading. Once uploaded refresh existing files list.
4. private **__create_import_folder** - create folder for imported files (call in init).
5. private **__sanitize_string** - sanitize user input (in condition value and limit value) - prevent sql injection.
6. private **__get_date** - get current date in defined format to be used in printing info to console.
