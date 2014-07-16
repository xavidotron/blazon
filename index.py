#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi,cgitb

cgitb.enable()

fs = cgi.FieldStorage()

blazon = fs.getfirst("blazon", None)

print """Content-Type: text/html; charset=utf-8

<html>
<head>
<title>Kihō's Blazon to Complex Search Form Parser</title>
</head>
<body>

<form method="get">
<label>Blazon:<br /><textarea name="blazon" cols="100" rows="5">%s</textarea></label><br />
<input type="submit" value="Parse" />
</form>""" % (cgi.escape(blazon) if blazon
              else "Or, a Laurel wreath vert.")

if blazon:
    import complexify
    from parse import parse, BlazonException
    print '<h2>%s</h2>' % cgi.escape(blazon)
    try:
        p = parse(unicode(blazon, 'utf-8'))
        lst = list(p.describe())
    except BlazonException, e:
        print '<h3>Error: %s</h3>' % cgi.escape(e.text)
        if e.url:
            print '<a href="%s">%s</a>' % (e.url, e.linktext)
        print "<p>Try simplifying your blazon, removing unnecessary detail or using more common names for charges.  If you think this is something that should be fixed, feel free to email kihou at xavid dot us with your blazon.</p>"
    else:
        print '<h3>Armory descriptions:</h3>'
        print '<ul>'
        for l in lst:
            print '<li>%s</li>' % l
        print '</ul>'
        url = complexify.url_for(lst)
        print '<p><a href="%s">Search the Complex Search Form with these descriptions</a></p>' % (url)

print """
<small>Written by Kihou (at xavid dot us).  Powered by <a href="http://scripts.mit.edu/">scripts</a>.</small>

</body>
</html>"""
