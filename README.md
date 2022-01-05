# PyWordle

A simple Python implementation of Wordle from Josh Wardle. I thought it was brilliant but wanted to play it more often than once a day, so I sketched this together fast. PRs and feedback welcome.

You will need the list of frequent English words from [https://github.com/first20hours/google-10000-english](https://github.com/first20hours/google-10000-english). Clone this repo, then clone that repo within this one.

To play the standard 5-letter word game:
`python wordle.py`

You can modify the code to use different length words and change the number of guesses:
`python wordle.py --char_min 4 --char_max 6 --max_guesses 6`

Use debug mode to show the answer, useful for testing changes:
`python wordle.py --debug`

Example game:

![Example Game](https://github.com/gaurav-scio/pywordle/blob/main/example.png?raw=true)