# Beautify HTML
Beautifies the content of an HTML file.

## Example

```
$ cat test.html
<html><body><p>This is a test.</p></body></html>
$ python3 prettyhtml.py test.html beautified.html
$ cat beautified.html
<html>
  <body>
    <p>
      This is a test.
    </p>
  </body>
</html>
