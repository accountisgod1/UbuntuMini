import getpass
import psutil
import subprocess
import difflib
import cmd
import os
import sys
import datetime
import shutil
import urllib.request
import platform
import string

CUSTOM_COLORS = {
    ''
}

UBUNTU_COLOR_SCHEME = {
    'text_color': '\033[0m',
    'directory_color': '\033[38;5;39m',
    'executable_color': '\033[92m',
    'zip_color': '\033[0;31m',
    'normal_file': '\033[0m',
    'MD': '\033[33m',
    'IMG_FILE': '\033[95m'
}

class UbuntuMini(cmd.Cmd):
    
    def __init__(self):
      super().__init__()
      self.command_history = []  # Initialize an empty list for command history


    intro = 'Welcome to UbuntuMini Type help or ? to list commands.\n'
    version = '0.0.0'
    
    def preloop(self):
       user = getpass.getuser()
       host = platform.node()
       self.prompt = f'\033[1;32m{user}@{host}:\033[0m\033[1;34m~$\033[0m $ '
      
    version = '1.0.0'  # Change this to your current script version

    def do_update(self, args):
        """
        Updates UbuntuMini from GitHub.
        Usage: update
        """
        try:
            # Change the following URL to your GitHub repository URL
            github_repo_url = "git@github.com:accountisgod1/UbuntuMini.git"
            subprocess.run(["git", "pull", github_repo_url], cwd="C:/Users/User/Documents/A/PythonCMD/CMD.py")

            print("UbuntuMini updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

      
    def do_ln(self, arg):
        """
        Create a hard or symbolic link.
        Usage: ln [options] <target> <link_name>
        Options:
          -s, --symbolic    create a symbolic link
          -h, --help        display this help and exit
        """
        try:
            args = arg.split()
            if len(args) < 2:
                print("Error: Insufficient arguments. Provide at least a target and a link name.")
                return

            # Parse options
            symbolic = False
            while args and args[0].startswith("-"):
                option = args.pop(0)
                if option in ("-s", "--symbolic"):
                    symbolic = True
                elif option in ("-h", "--help"):
                    print(self.do_ln.__doc__)
                    return
                else:
                    print(f"Error: Unknown option '{option}'.")
                    return

            target = args.pop(0)
            link_name = args.pop(0) if args else None

            if symbolic:
                os.symlink(target, link_name)
                print(f"Symbolic link created: {link_name} -> {target}")
            else:
                os.link(target, link_name)
                print(f"Hard link created: {link_name} -> {target}")

        except Exception as e:
            print(f"Error: {e}")
            
    def do_diff(self, arg):
        """
        Compare two files line by line.
        Usage: diff <file1> <file2>
        """
        try:
            files = arg.split()
            if len(files) != 2:
                print("Error: Provide exactly two files for comparison.")
                return

            file1, file2 = files

            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()

                # Perform line-by-line comparison
                diff_result = list(difflib.unified_diff(lines1, lines2, lineterm=''))

                if not diff_result:
                    print("Files are identical.")
                else:
                    print("\n".join(diff_result))

        except FileNotFoundError:
            print(f"Error: One or both files not found.")
        except Exception as e:
            print(f"Error: {e}")
       
    def do_passwd(self, arg):
        """
        Change the password for a user, must be numbers only (simulate on Windows).
        Usage: passwd <username>
        """
        try:
            if platform.system() == "Windows":
                new_password = getpass.getpass("Enter new password (Numbers): ")
                subprocess.run(["net", "user", arg, new_password], shell=True)
                print(f"Password for user '{arg}' changed.")
            else:
                # Implement Unix-like password change for other platforms
                print("Error: Password change not supported on this platform.")
        except Exception as e:
            print(f"Error: {e}")

    def do_ping(self, arg):
        """
        Ping a host to check for network connectivity.
        Usage: ping <hostname or IP address>
        """
        try:
            subprocess.run(["ping", arg])
        except Exception as e:
            print(f"Error: {e}")

    def do_hostname(self, arg):
        """
        Display the hostname of the system.
        Usage: hostname
        """
        try:
            host_name = platform.node()
            print(host_name)
        except Exception as e:
            print(f"Error: {e}")

    def do_man(self, arg):
        """
        Display the manual page for a command.
        Usage: man <command>
        """
        try:
            all_commands = self.get_names()
            if f"do_{arg}" in all_commands:
                docstring = getattr(self, f"do_{arg}").__doc__
                if docstring:
                    print(docstring.strip())
                else:
                    print(f"No manual entry for {arg}.")
            else:
                print(f"Error: Unknown command '{arg}'.")
        except Exception as e:
            print(f"Error: {e}")

    def do_mkdir(self, arg):
        """
        Create a new directory.
        Usage: mkdir <directory_name>
        """
        try:
            os.mkdir(arg)
            print(f"Directory '{arg}' created.")
        except FileExistsError:
            print(f"Error: Directory '{arg}' already exists.")
        except Exception as e:
            print("mkdir: Missing operand")
            print("Try 'help mkdir' for more information.")
            
    def do_mv(self, arg):
        """
        Move or rename a file or directory.
        Usage: mv <source> <destination>
        """
        try:
            source, destination = arg.split()
            shutil.move(source, destination)
            print(f"Moved '{source}' to '{destination}'.")
        except ValueError:
            print("Error: Provide both source and destination.")
        except FileNotFoundError:
            print("Error: Source file or directory not found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_dir(self, arg):
        """
        Prints all of the available directories
        Usage: dir
        """
        
        directory = arg or os.getcwd()
        try:
            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                print(file)
        except FileNotFoundError:
            print(f"Error: Directory not found - {directory}")
        except PermissionError:
            print("No permissions for the directory.")

    def do_pwd(self, arg):
        """
        Print the current working directory.
        Usage: pwd
        """
        try:
            current_directory = os.getcwd()
            print(current_directory)
        except Exception as e:
            print(f"\033[1;31mError: {e}\033[0m")

    def do_run(self, arg):
        """
        Run an external application.
        Usage: run <application_name>
        """
        try:
            if platform.system() == "Windows":
                subprocess.run(["start", arg], shell=True)
            else:
                subprocess.run([arg])
        except FileNotFoundError:
            print(f"\033[1;31mError: Application '{arg}' not found.\033[0m")
        except Exception as e:
            print(f"\033[1;31mError: {e}\033[0m")

    def do_download(self, arg):
        """
        Download a file from the internet using urllib.
        Usage: download <url> [destination]
        """
        try:
            url, _, destination = arg.partition(" ")
            if not destination:
                destination = os.getcwd()

            # Use urllib for downloading files
            with urllib.request.urlopen(url) as response, open(os.path.join(destination, os.path.basename(url)), 'wb') as out_file:
                data = response.read()
                out_file.write(data)

            # Display success message with Ubuntu-style coloring
            success_message = f"\033[1;32mFile downloaded from {url} to {destination}.\033[0m"
            print(success_message)
        except Exception as e:
            # Display error message with Ubuntu-style coloring
            error_message = f"\033[1;31mError: {e}\033[0m"
            print(error_message)

    def do_whoami(self, arg):
         """
         Display the current username.
         Usage: whoami
        """
         user = getpass.getuser()
         print(user)


    def do_cd(self, arg):
        """
        Change the current working directory.
        Usage: cd <directory>
        """
    
        try:
          os.chdir(arg)
          print(f"Changed directory to: {os.getcwd()}")
        except FileNotFoundError:
          print(f"Error: Directory not found - {arg}")
        except PermissionError:
          print("No permissions to change directory.")

        
    def do_rm(self, arg):
        """
        Remove a file or directory.
        Usage: rm <file/directory>
        """
        try:
            if os.path.isdir(arg):
                shutil.rmtree(arg)
                print(f"Directory '{arg}' removed.")
            elif os.path.isfile(arg):
                os.remove(arg)
                print(f"File '{arg}' removed.")
            else:
                print(f"Error: '{arg}' not found.")
        except Exception as e:
            print(f"Error: {e}")
    
    def do_cat(self, arg):
        """
        Display contents of a file.
        Usage: cat <file>
        """
        try:
           with open(arg, 'r') as file:
             content = file.read()
             print(content)
        except FileNotFoundError:
           print(f"Error: File not found - {arg}")
        except Exception as e:
           print(f"Error: {e}")
    
    def do_cls(self, arg):
        """
        Clear the console screen.
        Usage: cls
        """
        try:
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")
        except Exception as e:
            print(f"Error: {e}")
            
    def do_echo(self, arg):
        """
        Display a message or write to a file.
        Usage: echo <message> [> <file>]
        """
        try:
            message, _, filename = arg.partition(" > ")
            print(message)
            if filename:
                with open(filename, 'w') as file:
                    file.write(message)
                    print(f"Message written to '{filename}'.")
        except Exception as e:
            print(f"Error: {e}")

    def do_ls(self, arg):
       """
       List files and directories in the current working directory.
       Usage: ls [directory]
       """
       
       directory = arg or os.getcwd()
       try:
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                if file.lower().endswith((".zip",".tar")):
                    color_code = UBUNTU_COLOR_SCHEME['zip_color']
                elif file.lower().endswith(".md"):
                    color_code = UBUNTU_COLOR_SCHEME["MD"]
                elif file.lower().endswith((".png",".jpeg",".jpg",".gif",".ico")):
                    color_code = UBUNTU_COLOR_SCHEME["IMG_FILE"]
                elif file.lower().endswith(".exe"):
                    color_code = UBUNTU_COLOR_SCHEME["executable_color"]
                else:
                    color_code = UBUNTU_COLOR_SCHEME["normal_file"]
            elif os.path.isdir(file_path):
                color_code = UBUNTU_COLOR_SCHEME['directory_color']
            else:
                color_code = UBUNTU_COLOR_SCHEME['text_color']

            print(f"{color_code}{file}\033[0m")
       except FileNotFoundError:
        print(f"Error: Directory not found - {directory}")
       except PermissionError:
        print("No permissions for the directory.")

    def ls_l(self, arg):
        """
        List files and directories in long format (detailed information).
        Usage: ls -l [directory]
        """
        directory = arg or os.getcwd()
        try:
            files = os.listdir(directory)
            for file in files:
                full_path = os.path.join(directory, file)
                stat_info = os.stat(full_path)
                print(
                    f"{file}\tSize: {stat_info.st_size} bytes\tLast Modified: {datetime.datetime.fromtimestamp(stat_info.st_mtime)}")
        except FileNotFoundError:
            print(f"Error: Directory not found - {directory}")

    def do_chmod(self, arg):
        """
        Change file permissions.
        Usage: chmod <permissions> <file>
        """
        try:
            permissions, file_path = arg.split()
            os.chmod(file_path, int(permissions, 8))
            print(f"Permissions of '{file_path}' changed to {permissions}.")
        except ValueError:
            print("Error: Provide both permissions and file path.")
        except Exception as e:
            print(f"Error: {e}")

    def do_cp_r(self, arg):
        """
        Copy directories recursively.
        Usage: cp -r <source_directory> <destination_directory>
        """
        try:
            source, destination = arg.split()
            shutil.copytree(source, destination)
            print(f"Copied '{source}' directory to '{destination}'.")
        except ValueError:
            print("Please provide both source and destination.")
        except Exception as e:
            print(e)

    def do_touch(self, arg):
        """
        Create an empty file or update the timestamp of an existing file.
        Usage: touch <file>
        """
        try:
            with open(arg, 'a'):
                os.utime(arg, None)
            print(f"File '{arg}' created or timestamp updated.")
        except Exception as e:
            print(f"Error: {e}")

    def do_grep(self, arg):
        """
        Search for a pattern in a file.
        Usage: grep <pattern> <file>
        """
        try:
            pattern, file_path = arg.split()
            with open(file_path, 'r') as file:
                lines = file.readlines()
                matching_lines = [line.strip() for line in lines if pattern in line]
                print("\n".join(matching_lines))
        except ValueError:
            print("Error: Provide both pattern and file path.")
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except Exception as e:
            print(f"Error: {e}")

    def do_head(self, arg):
        """
        Display the first few lines of a file.
        Usage: head <file>
        """
        try:
            with open(arg, 'r') as file:
                lines = file.readlines()[:10]  # Display the first 10 lines
                print("".join(lines))
        except FileNotFoundError:
            print(f"Error: File not found - {arg}")
        except Exception as e:
            print(f"Error: {e}")

    def do_tail(self, arg):
        """
        Display the last few lines of a file.
        Usage: tail <file>
        """
        try:
            with open(arg, 'r') as file:
                lines = file.readlines()[-10:]  # Display the last 10 lines
                print("".join(lines))
        except FileNotFoundError:
            print(f"Error: File not found - {arg}")
        except Exception as e:
            print(f"Error: {e}")

    def do_ps(self, arg):
        """
        Display information about running processes.
        Usage: ps
        """
        try:
            process_list = psutil.process_iter()
            for process in process_list:
                print(process)
        except Exception as e:
            print(f"Error: {e}")

    def do_kill(self, arg):
        """
        Terminate a process by its process ID.
        Usage: kill <process_id>
        """
        try:
            process_id = int(arg)
            process = psutil.Process(process_id)
            process.terminate()
            print(f"Process {process_id} terminated.")
        except ValueError:
            print("Error: Provide a valid process ID.")
        except psutil.NoSuchProcess:
            print(f"Error: Process {process_id} not found.")
        except Exception as e:
            print(f"Error: {e}")

    def do_df(self, arg):
        """
        Display disk space usage.
        Usage: df
        """
        try:
            disk_partitions = psutil.disk_partitions()
            for partition in disk_partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"Partition: {partition.device}\tTotal: {usage.total} bytes\tUsed: {usage.used} bytes\tFree: {usage.free} bytes")
        except Exception as e:
            print(f"Error: {e}")

    def do_du(self, arg):
        """
        Display the size of a directory or file in human-readable format.
        Usage: du <directory/file>
        """
        try:
            size = os.path.getsize(arg) if os.path.isfile(arg) else self.get_directory_size(arg)
            formatted_size = self.format_size(size)
            print(f"Size of {arg}: {formatted_size}")
        except FileNotFoundError:
            print(f"Error: Directory or file not found - {arg}")
        except Exception as e:
            print(f"Error: {e}")
            
    def get_directory_size(self, directory):
        total_size = 0
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_file():
                    total_size += entry.stat().st_size
                elif entry.is_dir():
                    total_size += self.get_directory_size(entry.path)
        return total_size

    def format_size(self, size):
        # Define the byte units and their respective sizes
        units = ['bytes', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0

        # Convert size to the appropriate unit
        while size > 1024 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1

        # Format the size with up to two decimal places
        formatted_size = "{:.2f} {}".format(size, units[unit_index])
        return formatted_size



    def do_history(self, arg):
        """
        Display command history.
        Usage: history
        """
        try:
            for idx, command in enumerate(self.command_history, start=1):
                print(f"{idx} {command}")
        except Exception as e:
            print(f"Error: {e}")
            
    

    def do_alias(self, arg):
        """
        Create an alias for a command.
        Usage: alias <alias_name>="<command>"
        """
        try:
            alias_name, command = arg.split("=")
            print(f"Alias '{alias_name}' created for command '{command}'.")
        except ValueError:
            print("Error: Provide both alias name and command.")
        except Exception as e:
            print(f"Error: {e}")

    def do_date(self, arg):
        """
        Display or set the system date and time.
        Usage: date [options]
        """
        try:
            if arg:
                subprocess.run(["date", arg])
            else:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Current date and time: {current_date}")
        except Exception as e:
            print(f"Error: {e}")

    def do_find(self, arg):
        """
        Search for files and directories.
        Usage: find <directory> -name <filename>
        """
        try:
            directory, _, filename = arg.partition(" -name ")
            matches = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if filename in file:
                        matches.append(os.path.join(root, file))
            if matches:
                print("Matches found:")
                for match in matches:
                    print(match)
            else:
                print("No matches found.")
        except ValueError:
            print("Error: Provide both directory and filename.")
        except Exception as e:
            print(f"Error: {e}")

    def do_locate(self, arg):
        """
        Quickly find the location of a file.
        Usage: locate <filename>
        """
        try:
            result = subprocess.run(["locate", arg], capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            elif result.stderr:
                print(result.stderr)
            else:
                print("No matches found.")
        except Exception as e:
            print(f"Error: {e}")
            
    def precmd(self, line):
        
        self.command_history.append(line)
        return line
        
if __name__ == "__main__":
    UbuntuMini().cmdloop()
