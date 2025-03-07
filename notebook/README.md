# Note Taker App
A simple note-taking application that allows users to write and save notes with tags and timestamps.

## Overview
The Note Taker App is a GUI-based application that provides a simple and intuitive 
way to create and save notes. The app allows users to enter a tag and a note, and 
then saves (appends) the note (and a timestamp) to a file with the corresponding tag.

## How it Works
1. Launch the app and enter a tag in the "Tag" field.
2. Enter your note in the text area.
3. Click the "Submit" button to save the note.
4. The note and a timestamp will be added to a file with the corresponding tag (e.g. "tag_name.md").
5. The text field will be cleared.

## Features
* Simple and intuitive GUI interface
* Ability to create and save notes with tags
* Notes are saved to files with the corresponding tag

## Requirements
* Python 3.x
* Tkinter library (included with Python)

## Output file example
```markdown
---
### 2025-03-07 17:01:10

Note text.
```