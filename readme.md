**far**: _simple mud engine_
========

This is a basic python-based MUD engine.  As of this version, there is no combat engine, and all client/server interaction occurs through the use of tagged commands.  The idea is that the client will parse these and present them nicely.  

Networking makes use of the Twisted Python libraries, databases use SQLAlchemy.

There's no combat, yet.  World, and mob definition, and mob-placement are handeld through static text files.  Thats about it.

If you happen across this and wish to use it, feel free.  

