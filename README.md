Gullom
======

Or Gif Ultra-Light Library Online Manager. (Yeah, it sounds weird, I know).
A simple manager to store and retrieve gifs. Useful when one is trying to
communicate through gifs or win a gif battle.

I pronounce gif "jif", but "Gullom" like "Gum". Sue me.

This is by no mean a masterpiece, it's a quick'n'dirty hack using Flask. And
frankly, calling it "Ultra-Light" is a bit of a stretch.

Note that it now comes with a Meme generator.

A major caveat : Gullom is NOT multi-user, and was not designed to be. So
each install is for one person only and there is only one admin account to rule them all.
A second major caveat : if you love gif as much as I do, do not forget that
you're going to store a lot of shit on your hard-drive. 

Dependencies
------------

Vanilla Gullom, without meme, didn't need anything fancy, but Flask.
Gullom now comes with a Meme generator, so we need image modification libraries.

You'll need PIL, wich can be rather tedious to install.
Make sure you have the jpeg decoders, since most meme use it.

You'll also need the Impact font. I used microsoft core fonts, that you can
easily install through your packet manager. Here in a Debian flavour :

    sudo apt-get install --reinstall ttf-mscorefonts-installer

Oh ! And you'll need a database. I use sqlite, but it should not be too difficult
to use it with mySQL.

Safety
------

OK, since Gullom is basically a file-uploader from the Internets, it comes
with major safety issues, mostly RFI risk. However, to achieve that, an attacker
would need to get to your account first.

The downloader should only accept images that PIL can open - and for each donwloaded file,
PIL does try to open them to make sure we're not dealing with a remote shell. So that should
normally do the trick.

SQL injection is covered by Flask sql functionalities, and there is no query concatenation so we
shoud be safe here.

That leaves us with (at least !) three major threat :
- XSS. No protection whatsoever.
- CSRF. No protection whatsoever (but trivial to add).
- Bruteforcing. No protection, so please DO use a long, hard-to-guess password.

Configuration
-------------

Make sure every folder where images will be written are owned by the www-data group (or
whatever group is used by the server). This also goes for your database and the folder it is in.

The database can be generated fairly easily. Launch python, import Gullom, and call :

    gullom.init_db()

Finally, you'll need a config.py file with the following :

    USERNAME = ""   # your username
    PASSWORD = ""   # your password (cleartexted... I plan to hash this, though, because it's ugly)
    SECRET_KEY = "" # add a secret key (smashing your keyboard furiously can do)
    ROOT = ""       # The absolute path of your app. (Used because saving image with relative
                    # path was a bit of a pain).
    DATABASE = ""   # Absolute path to the DB. So if it's a "giffy.db" file in your app folder,
                    # you can do a ROOT + "giffy.db".

(And yes, I will add this to the github one day)
