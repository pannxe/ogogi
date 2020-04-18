# OGOGI

**OGOGI** stands for **OTOG Grader that is Optimized. Plus it can now Grade Interactive problem** (previously known as otogGraderII)

This is an attempt to improve [otogGrader](https://otog.cf/) mainly by implementing interactive script. OGOGI is also planed to use Cython for better performance.

## Now implemented

- **Now implemented external comparing script**
- Modularization.
- Unlimited # of testcase.
- **Command mode (type ' : ')**
  - Featuring '**reload**' command. Reload any module without having to restart the grader.
- Improved debug console.
- Cleaner code for better maintainent.
- Minor performance improvement.

## Todo

Todo is short-term plans that ment to be done within current version.

- **Add more functionality to command mode**
- Debug.
- Error handling.

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
def cmp(
  resultPath  : "Path to result file",
  solutionPath: "Path to solution file") -> bool:
  # Do some stuff
  return result # True = P; False = -
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
