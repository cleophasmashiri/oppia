The following instructions outline how to install Oppia on a Windows machine and run the tests. Note that the resulting Oppia installation will omit the code editor widget, which depends on a library called jsrepl that we have not figured out how to install in Windows yet. If you would like to help with fixing this, please add a comment to [issue 100](https://code.google.com/p/oppia/issues/detail?id=100) -- thanks!

### First we'll get the back-end tests running. ###

1. Install Python 2.7.6 by selecting the appropriate MSI from [this page](https://www.python.org/download/releases/2.7.6/). (You can follow [these instructions](http://support.microsoft.com/kb/827218) to determine whether your computer uses the x64 or x86 architecture.) Do not install the latest Python version, 2.7.7, as it will trigger a problem in the GAE. During the installation, select the option "add python.exe to path" (if you see this option). If you do not see this option, manually add Python to the path by going to `
My Computer > Properties > Advanced System Settings > Environment Variables` and appending "C:\Python27" to the PATH environment variable.

2. Install the Python Imaging Library (PIL) 1.1.7 for Python 2.7 from here: http://www.pythonware.com/products/pil/ . If you run into issues, the following links may be helpful:
  * http://stackoverflow.com/questions/14177000/cant-install-pil-1-7
  * http://technet.microsoft.com/en-us/library/cc947813%28v=ws.10%29.aspx

3. Install Git Bash from here: http://git-scm.com/download/win . During the installation, select "Use Git from Git Bash only" and "Checkout Windows-style, commit Unix Style line endings". Launch a Git Bash terminal and ensure that python 2.7.6 is on the path by typing "python" at the command line.

4. Get wget.exe from here http://eternallybored.org/misc/wget/ and put it somewhere on the Git Bash path, such as $HOME/bin. [notes: Type `echo $PATH` in the git bash terminal. Find a directory like $HOME/bin that is on the path, and copy wget.exe into that directory. Then type `wget` into the Git Bash terminal -- it should run and provide a usage message.](Further.md)

5. Install Python setuptools by downloading ez\_setup.py from https://pypi.python.org/pypi/setuptools, putting ez\_setup.py in your home directory and, in the Git Bash terminal, typing `python ez_setup.py`.

6. Follow the steps [here](https://code.google.com/p/oppia/source/checkout) to git clone the oppia repository.

_The rest of these instructions assume that you are working on the `develop` branch._

7. Because Git Bash does not provide the `chown` command, comment out line 67 in scripts/setup.sh.

8. Go to http://nodejs.org. Click "Downloads", then "Other Releases", then "v0.10.1", then download and execute "node-v0.10.1-x86.msi". After executing this, restart your computer, in order to make "node" and "npm" accessible from the command line. (See [here](http://blueashes.com/2011/web-development/install-nodejs-on-windows/) for more info.)

9. Run `bash scripts/start.sh --nojsrepl` and wait for it to complete downloading and installing all the necessary dependencies. This will start the GAE. Note that node.js and jsrepl will not be installed by this script; you have already installed nodejs in the previous step.

10. Kill the GAE if necessary to get the prompt back, and run the back end tests by typing `bash scripts/test.sh`.

### Now we'll try to run the front end tests. ###

11. Edit line 75 of setup.sh to say `export NPM_INSTALL="npm install"`

12. Install Chrome.

13. Edit the line at the end of setup.sh to say something like

> `export CHROME_BIN="/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"`

> or wherever Chrome is installed on your system.

14. Run `bash scripts/run_js_tests.sh --nojsrepl`. The first time this runs it will install karma and other node modules. During the installation of karma you may get an MSBUILD error saying it can't load the Visual C++ component "VCBuild.exe". If you see this, ignore it and re-run the script; it should work the second time.

15. If all goes well, Chrome will launch, and the front-end tests will complete.

# Doing programming work on Windows #

## Configuring your Google Code username and password ##

At some point you will need to submit code to the repo, which requires you to provide login information. Google Code passwords are not very memorable and it's nice to have a way to have them transmitted automatically. In the Linux version of Git this can be done with the file ~/.netrc, but this file is ignored in Windows by Git Bash (as far as I can tell). A substitute is to code your username and password into .git/config in something like the following way:

```
[remote "origin"]
        url=https://<username>:<password>@code.google.com/p/oppia/
```

or

```
git remote set-url origin https://username:password@code.google.com/p/oppia

```