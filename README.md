# OGOGI

**OGOGI** stands for **OTOG Grader that is Optimized. Plus it can now Grade Interactive problem** (previously known as otogGraderII)

This is an attempt to improve [otogGrader](https://otog.cf/) mainly by implementing interactive script. OGOGI is also planed to use Cython for better performance.

![srceenshot](/img/screenshot.jpg)

## Now implemented

- **Now implemented external comparing script**
- Modularization.
- Unlimited # of testcase.
- Improved debug console.
- Cleaner code for better maintainent.
- Minor performance improvement.

## Todo

Todo is short-term plans that ment to be done within current version.

- **Add more functionality to command mode**
- Debug.
- More error handling.

## Roadmap

Features to add in future version.

- Implement [Cython](https://cython.org/).
- Reimplement modules using class.
- Add support for other languages. (to be considered)

## How to write interactive script

Must be named ```interactive_script.py``` and put in source/probName.
Template:

```python
# interactive_script.py
import sys
resultPath   = sys.argv[1]
problemDir   = sys.argv[2]
atCase       = sys.argv[3]

# Do something

if answer_is_correct:
  print("P")
else:
  print("-")
```

## Folder Structure

```
/grader
  /compiled
  /env
  /img
  /install
  /source
  .gitignore
  LICENSE
  ogogi
  README.md
```

## Contributing

YES, please :) Pull requests are welcome.

## Authors

- **Karnjj** - *original work* - [Github](https://github.com/karnjj)
- **pannxe** - *OGOGI project* - [Github](https://github.com/pannxe)
- **Amethyst** - *supervisor* - [Github](https://github.com/sctpimming)
- **krist7599555** - *supervisor* - [Github](https://github.com/krist7599555)

## License

OGOGI is under [MIT](https://choosealicense.com/licenses/mit/) licence.
