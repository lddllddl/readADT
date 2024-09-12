# readADT

# Parse ADT from Haskell in a quick and dirty way.

Most Haskell data types implement a Show class (that is, you would be able to `print` it). In most cases, but not certainly, the printed string contains all information necessary to reconstruct the actual value.
Often the code you have at hand may have the Show class implemented but not other typeclasses for serialization or interoperability.

This short script read the typical `Show`n string representation into Python values (and hence JSON) so that you can process it out of Haskell in a pinch, without implementing additional typeclasses for serialization.

The only extra dependency is the [parsy](https://github.com/python-parsy/parsy) library.
