# rasa-workshop
Rasa workshop for Davidson meetup


## NLP WORKSHOP SETUP
## System requirements:
Must have python 3.6 or 3.7 version.

Steps:  
**1. Check if your Python environment is already configured:**
```
$ python3 --version  
$ pip3 --version
```
**2. Fetch the relevant packages and install virtualenv using pip or conda**
### Linux:
```python
$ sudo apt update
$ sudo apt install python3-dev python3-pip
```
### Windows:
>Make sure the Microsoft VC++ Compiler is installed, so python can compile any dependencies. You can get the compiler from [Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/). Download the installer and select VC++ Build tools in the list.

>Install [Python 3 (64-bit version)](https://www.python.org/downloads/windows/) for Windows.

```
C:\> pip3 install -U pip
```

### Mac OS
> Install the [Homebrew](https://brew.sh/) package manager if you haven’t already.  
>Once you’re done, you can install Python3.

```python
$ brew update
$ brew install python
```

**3. Create a virtual environment**
### Using Conda
```python
conda create --name workshop
```
> You can replace "workshop" with whatever name you like.   
> When conda asks proceed [y/n] - select y  
> Now activate your environment.

```python
conda activate workshop
```

### Using virstualEnv
Create a new virtual environment by choosing a Python interpreter and making a ./venv directory to hold it:

#### On Linux/mac
```
$ python3 -m venv ./venv
```
> Activate the virtual environment
```
$ source ./venv/bin/activate
```

#### On Windows
```
C:\> python3 -m venv ./venv
```
> Activate the virtual environment
```
C:\> .\venv\Scripts\activate
```

**4. Install RASA**
> Update your pip/conda
```
$ pip install -U pip
```

> Install Rasa
```
pip install rasa
```



