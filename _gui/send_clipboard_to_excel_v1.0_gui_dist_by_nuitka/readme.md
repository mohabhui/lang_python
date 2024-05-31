
# Clipboard to Excel v1.0

![Application Screenshot](https://github.com/mohabhui/lang_python/blob/main/_gui_images/clipboard_to_excel.png?raw=true)

## Overview
This application allows you to monitor your clipboard content, select tags from an Excel sheet, and write clipboard data to specific cells in the Excel file. It provides a graphical user interface (GUI) to facilitate these tasks.

## Configuration
The application requires a configuration file named `config.json` which should be placed in the same directory as the application. This configuration file contains necessary information about the Excel file and the sheets to interact with.

## Configuring `config.json`
The `config.json` file should be structured as follows:

```json
{
    "filename": "target.xlsx",
    "sheets_info": [
        ["CreditCard", "A", "B"],
        ["Bank", "E", "F"],
        ["Mortgage", "C", "F"]
    ],
    "sheet_color": {
        "CreditCard": "red",
        "Bank": "green",
        "Mortgage": "blue"
    },
    "markup_pairs": ["*", "*"]
}
```

- **filename:** The path to the Excel file you want to interact with.
- **sheets_info:** A list of lists where each inner list contains:
  - The sheet name.
  - The column containing tags.
  - The target column where data will be written.
- **sheet_color:** A dictionary mapping sheet names to colors. These colors are used to distinguish entries in the GUI.
- **markup_pairs:** A list of markup pairs that surround the text in cells of a column to indicate a tag.

## Application Interface
When you run the application, you will see the following interface:

1. **Clipboard Content Area:**
   - Displays the current content of your clipboard.
   - Updates automatically when new content is copied to the clipboard.

2. **Console Output Area:**
   - Displays log messages and information about the application's operations.

3. **Tag Selection Listbox:**
   - Lists all the tags found in the specified columns of the Excel sheets.
   - Tags are color-coded based on the sheet they belong to.
   - Clicking on a tag will select it for the current clipboard content.

4. **Quit Button:**
   - Closes the application.

## Using the Application

**NOTE:** The target Excel file should not be open in any application.

1. **Start the Application:**
   - Ensure `config.json` is correctly configured and placed in the application directory.
   - Run the application script.

2. **Monitor Clipboard:**
   - The clipboard content area will display the current clipboard content.
   - Any new content copied to the clipboard will automatically appear in this area.

3. **Select a Tag:**
   - Browse through the tag list in the listbox.
   - Click on a tag to select it. The selected tag and the clipboard content will be paired for writing to the Excel file.
   - Note: The tags, but not the sheets' names, are alphabetically sorted.

4. **Write to Excel:**
   - The application automatically writes the clipboard content to the specified cell in the Excel sheet corresponding to the selected tag.

5. **Quit:**
   - Click the "Quit" button to close the application.

By following these instructions, you should be able to effectively use the application to manage clipboard content and interact with your Excel files.
