# ibl

ibl ("interface between languages", pronounced like "tribble" with no
"tr") is a toy project I've written that allows source code written in
different languages to coinhabit the same file and share
variables. Every time an annotation is encountered that consists of a
comment character and then the name of another language that ibl supports,
ibl gathers in scope variables and writes them to a file. Then, it starts
the other language's interpreter and reads the variables back out to a file.

Currently supported languages:
* bash (sh,bash)
* python 2.x (py,python)

Martin Kellogg, June 2016