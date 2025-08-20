import os
import csv
import tkinter as tk
from tkinter import filedialog

# For PDF support, you'll need to install: pip install PyPDF2
try:
    import PyPDF2

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Note: PyPDF2 not installed. PDF support disabled.")


def read_pdf_file(file_path):
    """Read content from a PDF file"""
    if not PDF_AVAILABLE:
        raise Exception("PyPDF2 library not installed. Cannot read PDF files.")

    content = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"
    return content


def read_csv_file(file_path):
    """Read content from a CSV file"""
    content = ""
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            content += ",".join(row) + "\n"
    return content


def read_txt_file(file_path):
    """Read content from a TXT file"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_file_from_dialog():
    """Open file dialog to select a file"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_types = [
        ("All supported", "*.txt;*.csv"),
        ("Text files", "*.txt"),
        ("CSV files", "*.csv"),
        ("All files", "*.*")
    ]

    if PDF_AVAILABLE:
        file_types.insert(1, ("PDF files", "*.pdf"))
        file_types[0] = ("All supported", "*.txt;*.csv;*.pdf")

    file_path = filedialog.askopenfilename(
        title="Select a file to process",
        filetypes=file_types
    )

    root.destroy()
    return file_path


def read_and_modify_file():
    print("File Import Options:")
    print("1. Enter file path manually")
    print("2. Browse and select file")

    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "2":
        try:
            input_file = get_file_from_dialog()
            if not input_file:
                print("No file selected. Exiting...")
                return
        except Exception as e:
            print(f"Error opening file dialog: {e}")
            print("Falling back to manual file path entry...")
            input_file = input("Enter the input file path: ").strip()
    else:
        input_file = input("Enter the input file path: ").strip()

    # Remove quotes if user copied path with quotes
    input_file = input_file.strip('"\'')

    output_file = input("Enter the output file name (with extension): ")

    try:
        # Check if file exists
        if not os.path.exists(input_file):
            print(f"Error: The file '{input_file}' was not found.")
            return

        # Get file extension
        file_extension = os.path.splitext(input_file)[1].lower()

        # Read file based on extension
        if file_extension == ".pdf":
            if not PDF_AVAILABLE:
                print("Error: PDF support not available. Please install PyPDF2: pip install PyPDF2")
                return
            content = read_pdf_file(input_file)
            print("PDF file read successfully!")

        elif file_extension == ".csv":
            content = read_csv_file(input_file)
            print("CSV file read successfully!")

        elif file_extension == ".txt":
            content = read_txt_file(input_file)
            print("Text file read successfully!")

        else:
            print(f"Unsupported file format: {file_extension}")
            print("Supported formats: .txt, .csv, .pdf")
            return

        if not content.strip():
            print("Warning: The file appears to be empty or couldn't be read properly.")

        # Modify the content (convert to uppercase)
        modified_content = content.upper()

        # Add file info to output
        file_info = f"SOURCE FILE: {os.path.basename(input_file)}\n"
        file_info += f"FILE TYPE: {file_extension.upper()}\n"
        file_info += f"WORD COUNT: {len(content.split())}\n"
        file_info += "=" * 50 + "\n\n"

        final_content = file_info + modified_content

        # Write to output file
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write(final_content)

        print(f"Successfully processed '{os.path.basename(input_file)}'")
        print(f"Modified content saved to '{output_file}'")
        print(f"Word count: {len(content.split())}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{input_file}' or write to '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Add this to your existing code
if __name__ == "__main__":
    read_and_modify_file()
