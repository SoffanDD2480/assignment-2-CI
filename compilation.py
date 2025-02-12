from os import listdir, path, walk
import subprocess

class CompilationCheck():
    def __init__(self, file_path):
        '''Initialization of the syntax check class'''
        self.file_path = file_path
        self.results = self.syntax_control()

    def syntax_control(self):
        """Conduct syntex check.
        Return a boolean value: True if syntax check passed, False if error occurs or syntax check failed"""
        print(f"Checking syntax for {self.file_path}...")

        #check if the directory exists
        if not path.exists(self.file_path):
            print("Error: file not exist")
            return False
        
        '''The function subprocess.run() is used to run the pylint command as they were runned in the terminal.
        pylint is a tool that checks for errors in Python code. The --errors-only flag is used to only show errors and not warnings.
        The capture_output flag is used to capture the output of the command. The text flag is used to return the output as a string.'''
        try:
            results = subprocess.run(
                ["pylint","--errors-only", self.file_path], capture_output=True, text=True)
            
        #if pylint is not found, print an error message and return False
        except FileNotFoundError:
            print("Error: pylint not found")
            return False
        
        
        #Check output of pylint
        """Check the following cases:
        If the string "syntax-error" is in the output, print "Error: Syntax error detected" and return False.
        If the return code is not 0, print "Error: pylint failed" and return False.
        Otherwise, print "Syntax check passed" and return True."""

        if "syntax-error" in results.stdout:
            print("Error: Syntax error detected")
            return False


        if results.returncode != 0:
            print("Error: pylint failed, Syntax Error detected")
            return False
        else:
            print("Syntax check passed")
            return True
        

"""
if __name__ == "__main__":
    syntax_checker = CompilationCheck("hello_world.py")"""