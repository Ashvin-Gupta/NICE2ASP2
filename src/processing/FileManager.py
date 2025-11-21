import os 
import re
import subprocess
import tempfile

class FileManager():
    def __init__(self) -> None:
        pass

    def load_file(self, input_file:str) -> str:
        with open(input_file, 'r', encoding='utf-8') as f:
            file_text = f.read()
        return file_text

    def save_file(self, input_text:str, output_file:str) -> None:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(input_text)
            f.close()
        print(f"Saved response to {output_file}")
    


        
    