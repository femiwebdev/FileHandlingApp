def read_and_modify_file():
    input_file = input("Enter the input file name (with extension): ")
    output_file = input("Enter the output file name (with extension): ")

    try:
        with open(input_file, "r") as infile:
            content = infile.read()
            # Modify the content (for example, convert to uppercase)
            modified_content = content.upper()

        with open(output_file, "w") as outfile:
            outfile.write(modified_content)

        print(f"Successfully processed '{input_file}' and created '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{input_file}' or write to '{output_file}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    read_and_modify_file()
