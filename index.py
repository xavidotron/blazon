#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi,cgitb

import words, structs

cgitb.enable()

fs = cgi.FieldStorage()

print """Content-Type: text/html; charset=utf-8

<html>
<head>
<title>Kihō's Blazon to Complex Search Form Parser</title>
</head>
<body>"""

mode = fs.getfirst("mode", None)

if mode and mode[0].isupper() and hasattr(words, mode):
    words.loadwords()
    print """<ul>"""
    for w in getattr(words, mode):
        print """<li>%s</li>""" % cgi.escape(w)
    print """</ul>"""
else:
    double = fs.getfirst("double", False)
    structs.DOUBLE_PRIMARIES = double
    
    blazon = fs.getfirst("blazon", None)

    print """<h1>Kihō's Blazon to Complex Search Form Parser</h1>

    <h2>About</h2>

    <p>This page is a convenice interface to the <a href="http://oanda.sca.org/oanda_complex.cgi">Complex Search Form</a> for searching the <a href="http://oanda.sca.org/">SCA Armorial</a>.  Blazon is a highly structured language, and it
    takes advantage of that to automatically interpret blazon and convert
    it into the armory descriptions used in the Armorial.  This is primarily
    useful for conflict-checking.</p>

    <p>This is a work in progress; not all tags will be included and it
    <emph>will</emph> make mistakes in weird cases.  If you have suggestions
    or find bugs, please let me know at kihou at xavid dot us so I can improve
    it.</p>

    <h3>Nota Bene!</h3>

    <p>This page is here for convenience.  It does not replace
    understanding the SCA rules for conflict checking and knowledge of how
    to use the Complex Search Form.  For information about both these
    topics, see the materials available at <a href="http://yehudaheraldry.com/ekhu/">East Kingdom Herald University</a>.</p>

    <p>The parser makes heavy use of the "see also" references in the Ordinary
    (i.e., <a href="http://oanda.sca.org/my.cat">my.cat</a>).  This means
    that a single charge in your blazon may be represented by multiple armory
    descriptions, so keep this in mind when counting distinct changes from
    Complex Search Form score totals.</p>"""

    if blazon:
        import complexify
        from parse import parse, BlazonException
        print '<h2>Result for: %s</h2>' % cgi.escape(blazon)
        try:
            p = parse(unicode(blazon, 'utf-8'))
            lst = list(p.describe())
        except BlazonException, e:
            print '<h3>Error: %s</h3>' % cgi.escape(e.text.encode('utf-8'))
            if e.dym:
                print '<ul>'
                for d in e.dym:
                    print '<li>%s</li>' % cgi.escape(d)
                print '</ul>'
            if e.url:
                print '<a href="%s">%s</a>' % (e.url, e.linktext.encode('utf-8'))
            print "<p>Try simplifying your blazon, removing unnecessary detail or using more common names for charges.  If you think this is something that should be fixed, feel free to email kihou at xavid dot us with your blazon.</p>"
        else:
            print '<h3>Armory descriptions:</h3>'
            print '<ul>'
            for l in lst:
                print '<li>%s</li>' % l
            print '</ul>'
            url = complexify.url_for(lst)
            print '<p><a href="%s">Search the Complex Search Form with these descriptions</a></p>' % (url)

    print """<h2>Blazon Search</h2>

    <form method="get">
    <textarea name="blazon" cols="100" rows="5">%s</textarea><br />
    <label><input name="double" type="checkbox"%s /> Double Primaries (see below)</label><br />
    <input type="submit" value="Parse" />
    </form>""" % (cgi.escape(blazon) if blazon else "Or, a Laurel wreath vert.",
                  " checked" if double else "")

    print """<h3>Options</h3>

    <h4>Doubling Primaries</h4>
    <p>Sometimes, a straightforward search will give you large numbers of
    blazons that are a substantial change away, making it hard to see
    any conflicts.  To help with this, you can ask the parser to
    generate two descriptions for primary charge groups:
    a precise one and a simpler one without
    tags like tincture.  This will give two points to armory that has exactly
    your primary charge group and one point to armory that has something
    close to your primary charge group.  The intent is that armory with
    a substatial change to the primary charge group will lose two points this
    way, equivalent to two DCs; however, this won't necessarily be the case
    for armory with coprimary charges and such cases.  As always, check
    the descriptions being used.</p>"""

print """
<hr />

<p>Source for this site is available on Github at <a href="https://github.com/xavidotron/blazon">https://github.com/xavidotron/blazon</a>.

<p><small>Written by Kihou (at xavid dot us).  Powered by <a href="http://scripts.mit.edu/">scripts</a>.</small></p>

</body>
</html>"""
