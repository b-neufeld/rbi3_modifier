#!/usr/bin/python

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
uploaded_rbi3_1990_file = form['rbi3_1990_file']
uploaded_csv_file = form['csv_file']
supplied_new_file_name = form['new_file_name']
# new modified game filename with full directory
new_file_name = ROOT_DIRECTORY + 'upload\\' + str(supplied_new_file_name.value)
# just the filename so it can be inserted into a download URL
filename_for_url = str(supplied_new_file_name.value)


# Test if the original game file was uploaded
if uploaded_rbi3_1990_file.filename:
    # strip leading path from file name to avoid directory traversal attacks
    rbi3_1990_file = ROOT_DIRECTORY + 'upload\\' + os.path.basename(uploaded_rbi3_1990_file.filename)
    # check and make sure this file doesn't exist already
    if os.path.isfile(rbi3_1990_file):
        rbi3_1990_file = ROOT_DIRECTORY + 'upload\\' + random_number_string + '-' + \
                         os.path.basename(uploaded_rbi3_1990_file.filename)
    # NOTE: on brahm.ca read/write permissions have to be set for folders via admin.brahm.ca control panel
    open(rbi3_1990_file, 'wb').write(uploaded_rbi3_1990_file.file.read())
    # check file size
    nes_file_size = int(os.stat(rbi3_1990_file).st_size)
    if 196000 <= nes_file_size <= 197000:
        nes_file_size_ok = 1
    else:  # delete the uploaded file and log some errors.
        os.remove(rbi3_1990_file)
        message += 'File size error - .nes file must be about 196624 bytes: ' + str(nes_file_size) + ' bytes <br>'
        write_to_web_logfile("Bad .nes file size in new ROM creation: " + str(nes_file_size))
else:
    message += 'No RBI 3 1990 file was uploaded or there was an unknown error. File size: ' + str(nes_file_size) + '<br>'
    write_to_web_logfile("It choked on the 1990 .nes file! File size: " + str(nes_file_size))


# Test if the csv file was uploaded - only if the .nes file upload is OK
if uploaded_csv_file.filename and nes_file_size_ok:
    # strip leading path from file name to avoid directory traversal attacks
    csv_file = ROOT_DIRECTORY + 'upload\\' + os.path.basename(uploaded_csv_file.filename)
    # check and make sure this file doesn't exist already
    if os.path.isfile(csv_file):
        csv_file = ROOT_DIRECTORY + 'upload\\' + random_number_string + '-' + \
                   os.path.basename(uploaded_csv_file.filename)
    # NOTE: on brahm.ca read/write permissions have to be set for folders via admin.brahm.ca control panel
    open(csv_file, 'wb').write(uploaded_csv_file.file.read())
    # check that .csv filesize won't crush server
    csv_file_size = int(os.stat(csv_file).st_size)
    if csv_file_size > 200000:
        os.remove(csv_file)
        # if the rbi3 1990 file is still on the server, delete it
        if os.path.isfile(rbi3_1990_file):
            os.remove(rbi3_1990_file)
        message += 'File size error - .csv file larger than 200 kB: ' + str(csv_file_size) + ' bytes<br>'
        write_to_web_logfile("Gigantic .csv file size detected: " + str(csv_file_size))

else:
    message += 'No csv file was uploaded or there was an error.<br>'
    write_to_web_logfile("It choked on the .csv file! ")


#test if a valid filename was given - if not, add to error message.
if filename_for_url == "" or filename_for_url[-4:].lower() != ".nes":
    message += "<br>There was a problem with the filename you provided - it must end in .nes<br>"
    write_to_web_logfile("Bad .nes filename attempt.")
elif message == "":
    # check and make sure this file doesn't exist already. If so, add in that random number
    if os.path.isfile(new_file_name):
        new_file_name = ROOT_DIRECTORY + 'upload\\' + random_number_string + '-' + str(supplied_new_file_name.value)
        filename_for_url = random_number_string + '-' + str(supplied_new_file_name.value)
    # patch the uploaded 1990 file with the latest patchfile
    modify_1990_file(rbi3_1990_file, ROOT_DIRECTORY + 'data_files/2013patchfile.pch',
                     new_file_name)
    # create a player editor instance so the .csv file can be applied to it
    editor = PlayerEditor(new_file_name)
    # import the .csv data and write it into the player editor instance
    editor.import_new_data(csv_file)
    # wrap it up and create the new game file.
    editor.write_game_file(new_file_name)
    # write to logfile that we have great success!
    write_to_web_logfile("New ROM created! New File:" + filename_for_url +
                         "\t 1990 File:" + os.path.basename(uploaded_rbi3_1990_file.filename) +
                         "\t .csv File: " + os.path.basename(uploaded_csv_file.filename))
    # remove .nes file if ROM creation is successful
    os.remove(rbi3_1990_file)
    os.remove(csv_file)

# if message is blank so far, the ROM creation was successful, so let's give some good news and serve a download URL
if message == "":
    message += '<br><br>All done! Your new patched game file can be downloaded here (right-click, Save As):<br>'
    # we can't use rbi.ca/upload/file.nes because the domain forwarding is not smart enough.
    message += '<a href="' + UPLOAD_FOLDER + filename_for_url +\
               '" type="application/octet-stream">DOWNLOAD</a><br>'
    message += '<b>This file will be deleted from the server within 24 hours</b>.'

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

# sleep for a period of time (5 minutes) and delete the newly created file
# is there a better way to do this?
# JAN 22/2014 COMMENTING THIS OUT BECAUSE IT DOESN'T SEEM TO WORK - BN
#time.sleep(300)
#os.remove(new_file_name)