#!/usr/bin/python

# RBI Baseball 3 - ROM Modifier
# Brahm Neufeld
# January 2014

import cgi, os
import cgitb; cgitb.enable()
import os.path
from PlayerEditor import *
from PatchFileGenerator import *
from Values import *
from random import randint

# if a file with an identical name exists on the server, a random number will be appended
random_number_string = str(randint(0,100000))

form = cgi.FieldStorage()
message = ""
nes_file_size_ok = 0
nes_file_size = 0

# Get filenames here from POST
file_item_nes = form['nes_file']
file_item_csv = form['new_csv_file_name']
# new modified csv filename with full directory
new_csv_file_name = ROOT_DIRECTORY + 'upload\\' + str(file_item_csv.value)
# just the filename so it can be inserted into a download URL
new_csv_file_url_name = str(file_item_csv.value)

# Test if the .nes file was uploaded
if file_item_nes.filename:
    # strip leading path from file name to avoid directory traversal attacks
    nes_file_to_read = ROOT_DIRECTORY + 'upload\\' + os.path.basename(file_item_nes.filename)
    # check and make sure this file doesn't exist already
    if os.path.isfile(nes_file_to_read):
        nes_file_to_read = ROOT_DIRECTORY + 'upload\\' + random_number_string + '-' + \
                           os.path.basename(file_item_nes.filename)
    # NOTE: on brahm.ca read/write permissions have to be set for folders via admin.brahm.ca control panel
    open(nes_file_to_read, 'wb').write(file_item_nes.file.read())
    # check file size, if it fails then delete the file.
    nes_file_size = int(os.stat(nes_file_to_read).st_size)
    if 196000 <= nes_file_size <= 197000:
        nes_file_size_ok = 1
    else:
        os.remove(nes_file_to_read)
        message += 'File size error - .nes file size must be about 196624 bytes: ' + str(nes_file_size) + ' bytes<br>'
        write_to_web_logfile("Bad .nes file size in .nes-to-.csv conversion: " + str(nes_file_size))
else:
    message += 'No RBI 3 .nes file was uploaded or there was an error. File size: ' + str(nes_file_size) + ' bytes<br>'
    write_to_web_logfile("There was a problem uploading a .nes file to turn into .csv! File size: " +
                         str(nes_file_size))


#test if a valid filename was given - if not, add to error message. - only if the .nes file upload is OK
if (new_csv_file_url_name == "" or new_csv_file_url_name[-4:].lower() != ".csv") and nes_file_size_ok:
    message += "<br>There was a problem with the filename you provided - it must end in .csv<br>"
    write_to_web_logfile("Bad .csv filename attempt.")
else:
    # check and make sure this file doesn't exist already. If so, add in that random number
    if os.path.isfile(new_csv_file_name):
        new_csv_file_name = ROOT_DIRECTORY + 'upload\\' + random_number_string + '-' + str(file_item_csv.value)
        new_csv_file_url_name = random_number_string + '-' + str(file_item_csv.value)
    # open the .nes file as a new editor object
    editor = PlayerEditor(nes_file_to_read)
    # now it's as simple as writing the .csv file to the right folder.
    editor.write_file(new_csv_file_name)
    # write to logfile that we have great success!
    write_to_web_logfile(".csv file successfully created from .nes file:" + new_csv_file_url_name +
                         "\t .nes File: " + os.path.basename(file_item_nes.filename))

# if message is blank so far, the ROM creation was successful, so let's give some good news and serve a download URL
if message == "":
    message += '<br><br>All done! Your .csv file can be downloaded here (right-click, Save As):<br>'
    # we can't use rbi.ca/upload/file.nes because the domain forwarding is not smart enough.
    message += '<a href="' + UPLOAD_FOLDER + new_csv_file_url_name +\
               '" type="application/octet-stream">DOWNLOAD</a><br>'
    message += '<b>This file will be deleted from the server within 24 hours</b>.<br>'

# to do: make the output page prettier
print """\
Content-Type: text/html\n
<html>
    <body>
    <head>
        <title>RibEye3 Modifier - Create Gamefile</title>
            <link href="static/glike.css" rel="stylesheet" type="text/css" />
    </head>

    <div id="header">
        <h1><a href="index.htm">RibEye3 Modifier</a></h1>
        <ul class="toolbar">
            <li><a href="index.html">Home</a></li>
            <li><a href="create.html">Create RBI 3 Gamefile</a></li>
            <li><a href="help.html">Gamefile Creation Help</a></li>
            <li><a href="about.html" >About Project</a></li>
        </ul>
    </div>
    <div id="bodycontent">
   <p>%s</p>
    </div>
    </body>
</html>
""" % (message,)