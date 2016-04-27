# Dashboard for Dumfries and Galloway

This project was created as part of a University of Glasgow Level 3 Team Project.
The challenge was presented by the Crichton Institute who run a regional data
observatory in the Dumfries and Galloway area of Scotland.

## Installation

Create a directory for the project:
```
mkdir ~/TeamProject
```

Checkout the code:
```
cd ~/TeamProject
svn checkout svn+ssh://hoved/extra/2015/tp3/a/repos/trunk .
```

To create virtual environment:
Note: You can change the path at the end of this command to a more suitable
one for your machine, but you will need to recall this path in the future.
```
virtualenv --python=python2.7 ~/envs/tpenv
```

To start using virtual env:
```
source ~/envs/tpenv/bin/activate
```

To install the project requirements, cd into project directory and run: 
```
pip install -r requirements.txt
```


## Usage

Activate the virtual environment:
```
source ~/envs/tpenv/bin/activate
```

If you want to run the project tests and generate coverage reports, execute:
```
cd dashboard-project
python manage.py jenkins --enable-coverage --output-dir ../reports
```

This will create a directory in the project root called "reports" that will
contain two XML files. One contains an overview of the test results, and the
other an overview of how many lines of code was tested in each module.

To run the website locally:
```
cd dashboard-project
python manage.py migrate
python populate.py
python manage.py runserver
```

These commands will generate a SQLite3 file named db.sqlite3 in the dashboard-project
directory, populate it with some test data provided in the populate.py script,
which includes an admin user account with username "test@test.com", and password
"test".

You can now view the site at http://localhost:8000 if everyone has been set up
sucessfully.

## Project Structure

The project's folder structure is as follows:

- root
    - dashboard-project
        - api_processor
            - linked_data_processor
        - csv_processor
            - static
                - csv_processor
                    - test
                        - data
        - dashboard
            - media
            - settings
            - static
                - dashboard
                    - css
                    - data
                    - fonts
                    - img
                    - js
            - templates
                - admin
                - dashboard
                    - docs
                        - admin
                        - public
                    - pages
                    - partials
            - templatetags
        - dataset_importer
    - docs
        - dissertation
        - presentation
        
The dashboard-project directory contains 4 Django apps. The dataset_importer
app defines generic abstract models which the 3 other apps use and inherit from.
This model inheritance helps reduce repeated code across the project.

Each app has the possibility to contain static files and templates. The
csv_processor app uses it's static files folder to store CSV files to be used
in tests. The other other utility apps (dataset_importer, and api_processor) don't
make use of these folders, and just define models, and tests.

The dashboard app contains most of the application logic. It ties together the
other apps, and builds upon them to define what a visualisation contains, and
how it is linked to other models such as saved configurations.

The dashboard app also contains all the JavaScript code. In the directory 
static/dashboard/js in the dashboard folder you will find all the JavaScript code.
This file contains library code as well as application code. The application code
files are as follows:

- dashboard.js (Contains Angular controller code)
- daterangepicker_file.js (Contains code that handles the daterange picker)
- generate-pdf.js (Contains code to convert dashboard to a PDF file)
- graphs.js (Contains code that governs how the graphs are rendered using D3)

## History

* 01/11/15 - Project Begins
* 18/11/15 - First Team Retrospective
* 09/12/15 - Retrospective Two
* 28/01/16 - Retrospective Three
* 03/03/16 - Retrospective Four
* 23/03/16 - Demonstration to other teams and customers
* 24/03/16 - Final Team Retrospective
* 25/03/16 - No more coding as part of Level 3 Team Project course
* 11/04/16 - Hand-In of final dissertation
* 27/04/16 - Code moved to GitHub

## Credits

All development by:

* Isaac Jordan - 2080466j - Technical Lead
* Lewis Dicks - 2085749d - Project Manager
* Ross Yordanov - 2074214y - Retrospective Manager and Software Developer
* Branko Kourtellos - 2060408k - Software Developer
* Takis Nicolaides - 2084564n - Software Developer
* Michael Byars - 2028262b - Client Liason and Software Developer


## License

MIT License

Copyright (c) 2016 Isaac Jordan, Lewis Dicks, Ross Yordanov, Branko Kourtellos, Takis Nicolaides, Michael Byars

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
