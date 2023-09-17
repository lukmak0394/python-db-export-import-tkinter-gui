# Export module

---

This module is responsible for handling export data from selected database and columns to selected format file and saving it in directory.

---

### Variables description

1. private **__conn** - new connection with database

2. private **__tk_root_window** - root window for Tk

3. private **__tk_root_window_title** - title for root tk window

4. private **__top_level_window** - variable reserved for Toplevel object with query conditions. Assigned when Toplevel is created. 

5. private **__export_formats**  - available export formats

6. private **__query_conditions** - conditions to be used in select query for data export.

7. private **__conditions_start_row** - start row for query conditions dropdowns. incremented when adding new row with condition.

8. private **__queries_to_add** - dictionary with queries including conditions. Updated when conditions are saved / modified. 

9. private **__query_limits_input** - Entry (input) from which query limit will be taken and set to select query.

10. private **__selected_table** - selected db table.

11. private **__selected_columns** - selected db columns

12. priave **__export_folder** - folder to which file should be exported. 

---

### Methods description

1. public **open_window** - prepare root Tk window, render labels for tables and columns listboxes, render listboxes, apply column styling.
2. private **__display_db_tables_listbox** - insert available tables to tables listbox, display save tables button.
   1. **save_selection** - save selected table, when saved call insert column names to columns listbox.
3. private **__insert_column_names_to_listbox** - get column names from db schema for selected table, insert them to columns listbox.
   1. **save_selection** - update selected columns, then open window with query conditions. Display button for export action.
4. private **__display_export_buttons** - render buttons that triggers exprot action for each format.
5. private **__open_condtions_window** - open Toplevel (if not exists) OR refresh if exists (when column and table change in root tk window). Prepare labels for listboxes with available conditions. Display entry to define query limit.
6. private **__add_conditions_row** - add row with available query conditions.:
   1. where/and/or
   2. column
   3. operator
   4. condition value
7. private **__submit_query_conditions** - submit conditions for query.
8. private **__set_queries_to_add** - prepare queries to add to main select query. Add each query as new key value pair to object queries_to_add. 
9. private **__prepare_export_query** - prepare query to retreive data from db for selected column - include limit and conditions if defined.
10. private **__export_to_excel/csv** - actual export for selected format.
11. private **__export** - get data to export for prepared query, make folders, call method that handles export for selected format. Files are saved to export dir and inside to subfolder for selected table name.
12. private **__apply_columns_style** - apply styling for columns in root tk window.
