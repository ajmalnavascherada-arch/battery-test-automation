import subprocess

subprocess.run("git init", shell=True)
subprocess.run("git add .", shell=True)
subprocess.run('git commit -m "Initial commit"', shell=True)
subprocess.run("git branch -M main", shell=True)
subprocess.run("git remote add origin https://github.com/ajmalnavascherada-arch/battery-test-automation.git", shell=True)
subprocess.run("git push -u origin main", shell=True)