import os

class FileReaderTool_dict:
    def __init__(self, base_path="docs", name="file_reader"):
        self.name = name
        self.description = "Read all text files in docs folder."
        self.base_path = os.path.abspath("docs")

    def run(self, _=None):  # ignore input completely
        contents = {}

        for fname in os.listdir(self.base_path):
            full_path = os.path.join(self.base_path, fname)

            if os.path.isfile(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    contents[fname] = f.read()

        return contents
    
class FileReaderTool_old:
    def __init__(self, base_path="docs", name="file_reader"):
        self.name = name
        self.description = "Read all text files in the docs folder and return their contents."
        self.base_path = os.path.abspath("docs")

    def run(self, _=None):
        if not os.path.exists(self.base_path):
            return f"Error: Folder '{self.base_path}' not found."

        output_parts = []
        files = os.listdir(self.base_path)
        
        if not files:
            return "Observation: The docs folder is empty."

        for fname in files:
            full_path = os.path.join(self.base_path, fname)
            if os.path.isfile(full_path) and fname.endswith(".txt"):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Wrap each file in a very clear visual boundary
                        output_parts.append(f"--- START OF FILE: {fname} ---\n{content}\n--- END OF FILE: {fname} ---")
                except Exception as e:
                    output_parts.append(f"Error reading {fname}: {e}")

        # Join everything into one large text block

        print(f"------------------ file ---------------\n{"\n\n".join(output_parts)}")
        return "\n\n".join(output_parts)
    

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