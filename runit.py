import subprocess
command="ls"

subprocess.run(command, stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE, encoding='utf-8')
