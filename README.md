## What is it?
A dynamic way to access python settings in *any* python project with a simple context 
manager + decorator interface. The usage of the interface is similar to django's settings interface, 
however this comes without the "heavy" framework setup of django.

## How do I wire up?
Let's say you have a project setup like so:
```
myproject
    |----settings
        |----__init__.py
        |----dev.py
        |----tst.py
    |----run.py
   
```
In the settings folder of your project, you need to have different `.py` files each corresponding to 
your environments e.g., `dev.py`, `tst.py` etc (much like django).

**And** in the `__init__.py` file of the settings folder, you want to define your settings instance
like so:
```python
from pysettings import PySettings


mysettings = PySettings(__path__)
```
## How to use it?
This works when you have a settings folder **anywhere** nested in your root project
```python
"""run.py"""
from myproject.settings import mysettings
import os

def run(env='dev'):
    do_state_of_art_stuff(env)


if __name__ == '__main__':
    env = os.getenv('env')  # or may be use your favorite arg parser
    with mysettings(env):
        run(env)
```
