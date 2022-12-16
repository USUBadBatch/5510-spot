# Spot the Guide Dog
## Overview
This is our codebase for our 5510 Spot the Guide Dog final project. To use this codebase, you will need a boston dynamic support python version. Valid versions are python 3.6, 3.7, and 3.8. Once you have a valid python version installed, install the packages in the `requirements.txt` file.
## Running python files
All python files should be ran from the project root
## Layout
* `test/`
    * In the `test/` directory, we have a bunch of single python test files. These were used to validate certain features or functionality before trying to implement them into the spot controller logic so we could verify we had a working version beforehand.
* `src/`
    * This is the directory for spots main controller logic. In it are 1-2 files. `main.py` and `config.py`. If there is no `config.py` then running the main file will create a templated one for you. `config.py` contains a dict of the hand gestures names that the model can recognize as the keys, where the values contains callbacks to be executed when a classname is classified by the model. The value's exact type is an array, where the first element is the callback, and the second element is another dict. The keys are of the second dict are parameter names to the callback functions and the values are the values to set those parameters to.
    * EX: You have a function
        ```py
        def doPrintSomething(msg = "Default message"):
            print(msg)
        ```
        If the config file looked like this
        ```py
        config = {
        "okay"        : [doPrintSomething, {}],
        "peace"       : [doPrintSomething, {"msg":"this is not the default msg"}],
        "thumbs up"   : [None, {}],
        "thumbs down" : [None, {}],
        "call me"     : [None, {}],
        "stop"        : [None, {}],
        "rock"        : [None, {}],
        "live long"   : [None, {}],
        "fist"        : [None, {}],
        "smile"       : [None, {}],
        }
        ``` 
        Then when the model recognized an okay sign, it would run the function which would print "default message", but when it recognized a peace sign it would print "this is not the default msg".
    * Spot current controller implementation will print out the count of the nuber of times is recognized different gestures. It will then execute the callback after it recognizes a hand gesture 10 times. This was to prevent execution of an unwanted gesture because it wrongly classified the given hand gesture.
    * `src/hand-gesture-recognition-code-tensorflow/`
        * This is the pretrained tensorflow model to classify hand gestures
        * It was pulled from [this](https://techvidvan.com/tutorials/hand-gesture-recognition-tensorflow-opencv/) article.
    * `utils/` 
        * This contains some utility files for authenticating the boston dynamics api with spot as well as the functions to make spot do certain actions
## Spot sdk
The Boston Dynamics spot sdk is included with this repo as a submodule. To inflate run `git submodule init` then `git submodule update`.

## References
### 1. [First Reference](http://bingbingbong.ga)
