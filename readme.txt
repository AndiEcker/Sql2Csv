INSTALL 
========

* Copy the Sql2Csv folder onto the machine.

* Setup at least the Connect and the SqlQuery variables in the INI file.


USAGE
======

  Sql2Csv [ini-file] [CSV-output-file] [mean-price-file]


CONFIGURE
==========

An optional column header prefixing the content of the output CSV file can be
specified in the OutFileColumnHeader variable of the INI file.

Optional configure the mean-price merging by specifying the XmlFileName variable to
the (path and) file name of the XML file with the current mean prices.


TROUBLESHOOTING
===============

Use the pseudo machine name localhost if you execute Sql2Csv from the machine where
the SQL server is situated.

MS SQL Express Server note: add the string \sqlexpress to the machine name in the Connect
string of the INI file (see http://forums.microsoft.com/msdn-es/showpost.aspx?postid=2311401&siteid=11).
If you still get connection errors !!maybe!! install MSDE (not tested because the Sql Express
extension fixed my first problem when I tried it on TYAN_SERVER). For install instructions
see http://www.ajpdsoft.com/modules.php?name=News&file=article&sid=314.

