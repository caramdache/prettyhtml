# Beautify HTML
Beautifies the content of an HTML file.

## Example

```
$ cat dirty.html
<html><body><p>This is a test with a very long line that spans more than seventy characters and is going to be split into multiple lines.</p></body></html>
$ python3 prettyhtml.py dirty.html beautified.html
$ cat beautified.html
<html>
  <body>
    <p>
      This is a test with a very long line that spans more than seventy characters and is going
      to be split into multiple lines.
    </p>
  </body>
</html>
