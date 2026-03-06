import os

class FileReaderTool:
    def __init__(self, base_path="docs", name="file_reader"):
        self.name = name
        self.description = (
            "Reads the COMPLETE text content of a single file. "
            "Input MUST be a specific filename (e.g., 'Report.txt'). "
            "Use this ONLY after you know which file you need."
        )
        self.base_path = base_path

    def run(self, file_name: str):

        # Clean input (LLM sometimes adds spaces or new lines)
        file_name = file_name.strip().split("\n")[0]

        # If search tool returned something like:
        # "invitations.txt (2 matches)"
        file_name = file_name.split(" ")[0]

        # Keep only the filename (remove any path)
        file_name = os.path.basename(file_name)

        full_path = os.path.join(self.base_path, file_name)

        print(f"--------------- full_path: {full_path} --------------")

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content= f.read()

                if content:
                    return f"FILE CONTENT OF {file_name}:\n{content}\n\nINSTRUCTION: You have the data. Use 'final' to answer the user's question now."

        except FileNotFoundError:
            return f"File '{file_name}' not found in docs folder."
        except Exception as e:
            return f"Error reading file: {str(e)}"