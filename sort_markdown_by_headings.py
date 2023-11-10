#!/usr/bin/env python
"""
Sorts a Markdown file based on headings.

Usage: 
    python sort_markdown_by_headings.py input

Author: 
    Paul Stothard
"""

import argparse
import re
from collections import OrderedDict


def parse_markdown(md_text):
    in_code_block = False
    structure = {"pre_heading_content": "", "headings": OrderedDict()}

    # Prepare the regex for matching headings
    heading_regex = re.compile(r"^(#{1,6})\s+(.*)")

    # Initialize a list to keep track of the current heading hierarchy
    heading_stack = []

    # Parse each line
    for line in md_text.split("\n"):
        if line.strip().startswith("```"):
            # Toggle the in_code_block flag
            in_code_block = not in_code_block

        if in_code_block or not line.strip():
            # Add the line to the current context in the hierarchy
            if heading_stack:
                heading_stack[-1]["content"] += line + "\n"
            else:
                structure["pre_heading_content"] += line + "\n"
            continue

        # Check for heading matches
        match = heading_regex.match(line)
        if match:
            level, text = match.groups()
            level_num = len(level)

            # Pop from stack until we find our parent level or empty
            while heading_stack and len(heading_stack[-1]["level"]) >= level_num:
                heading_stack.pop()

            new_heading = {
                "level": level,
                "content": line + "\n",
                "subheadings": OrderedDict(),
            }

            # If stack is empty, we are at root level
            if not heading_stack:
                structure["headings"][text] = new_heading
            else:
                # Else we add as a subheading of the last heading on the stack
                heading_stack[-1]["subheadings"][text] = new_heading

            # Push the new heading onto the stack
            heading_stack.append(new_heading)
        else:
            # Non-heading lines get added to the content of the current heading
            if heading_stack:
                heading_stack[-1]["content"] += line + "\n"
            else:
                structure["pre_heading_content"] += line + "\n"

    return structure


def sort_markdown_structure(structure):
    sorted_headings = OrderedDict()
    for heading, content in sorted(structure.items(), key=lambda x: x[0].lower()):
        # Recursively sort subheadings
        content["subheadings"] = sort_markdown_structure(content["subheadings"])
        sorted_headings[heading] = content
    return sorted_headings


def flatten_structure(structure, level=1):
    sorted_md = ""

    # Add pre_heading_content if it's the root of the structure and contains content
    if (
        level == 1
        and "pre_heading_content" in structure
        and structure["pre_heading_content"].strip()
    ):
        # Ensure there is exactly one newline after pre_heading_content
        sorted_md += structure["pre_heading_content"].rstrip("\n") + "\n\n"

    for heading, content in structure["headings"].items():
        # Add headings with appropriate level
        sorted_md += f"{'#' * level} {heading}\n"  # Add heading with one newline
        # Add the content for the heading, excluding the line with the heading text itself
        content_lines = content["content"].split("\n")
        # Skip the first line which is the heading
        content_without_heading = "\n".join(content_lines[1:])
        if content_without_heading.strip():  # If there is actual content
            sorted_md += content_without_heading.rstrip("\n") + "\n\n"
        else:
            sorted_md += "\n"  # If there's no content, just add one newline for spacing

        # Recursively flatten subheadings
        if content["subheadings"]:
            sorted_md += flatten_structure(
                {"headings": content["subheadings"]}, level + 1
            )

    # Remove the trailing newlines for the last section
    if level == 1:
        sorted_md = sorted_md.rstrip("\n")

    return sorted_md


def sort_markdown(md_text):
    parsed_structure = parse_markdown(md_text)
    parsed_structure["headings"] = sort_markdown_structure(parsed_structure["headings"])

    return flatten_structure(parsed_structure)


def sort_markdown_sections(markdown_text):
    # Split the text into lines
    lines = markdown_text.split("\n")

    # Initialize variables
    sorted_text = []  # List to hold the sorted text
    current_section = []  # List to hold the lines of the current section
    in_code_block = False  # Flag to track if the current line is inside a code block

    # Helper function to sort and add the current section to sorted_text
    def sort_and_add_current_section():
        if current_section:
            # Sort the current section while ignoring the heading line
            heading = current_section[0]
            sorted_section = sorted(current_section[1:], key=str.lower)

            # Remove all blank lines from the section
            sorted_section = [line for line in sorted_section if line.strip()]

            # If the section is not empty, add a blank line before and after
            if sorted_section:
                sorted_section.insert(0, "")
                sorted_section.append("")
            else:
                # Otherwise, add a single blank line
                sorted_section.append("")

            # Combine the heading and the sorted lines, then append to sorted_text
            sorted_text.extend([heading] + sorted_section)

    # Iterate over the lines
    for line in lines:
        # Toggle the in_code_block flag if a code block delimiter is found
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            # Add the line to the current section or start a new one
            if current_section:
                current_section.append(line)
            else:
                sorted_text.append(line)
            continue

        # Check if the line is a heading and not in a code block
        if line.startswith("#") and not in_code_block:
            # Sort the current section and add it to sorted_text
            sort_and_add_current_section()
            # Start a new section with the current heading
            current_section = [line]
        else:
            # Add the line to the current section or to the sorted text if outside of any section
            if current_section:
                current_section.append(line)
            else:
                sorted_text.append(line)

    # Sort and add the last section after the loop ends
    sort_and_add_current_section()

    # Join the sorted sections into a single string
    sorted_markdown_text = "\n".join(sorted_text)

    return sorted_markdown_text


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def eprint_exit(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


def is_text_file(filename):
    with open(filename, mode="rb") as f:
        try:
            f.read().decode("utf-8")
        except UnicodeDecodeError:
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="sort_markdown_by_headings.py",
        description="Sorts a Markdown file based on headings.",
        epilog="python sort_markdown_by_headings.py input",
    )
    parser.add_argument("input", help="Markdown file to parse")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Markdown file to create, otherwise write to stdout",
    )
    parser.add_argument(
        "-s",
        "--sort",
        action="store_true",
        help="sort the content between headings",
        default=False,
    )
    args = parser.parse_args()

    if not is_text_file(args.input):
        eprint_exit("Input file '" + args.input + "' is not a text file.")

    # Read the file into string
    with open(args.input, "r") as f:
        md_text = f.read()

    sorted_markdown = sort_markdown(md_text)

    if args.sort:
        sorted_markdown = sort_markdown_sections(sorted_markdown)

    # add a newline at the end of the file if it doesn't already exist
    if sorted_markdown[-1] != "\n":
        sorted_markdown += "\n"
    
    if args.output:
        with open(args.output, "w") as f:
            f.write(sorted_markdown)
    else:
        print(sorted_markdown)
