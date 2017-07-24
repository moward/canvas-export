# Canvas Course Exporter
A Python-based command-line utility to export a user's courses to their local filesystem.

## Dependencies
User must have Python 3 installed

## Usage
This tool relies on two environmental variables: `CANVAS_ACCESS_TOKEN` and
`CANVAS_API_BASE`. The access token is documented [here](https://canvas.instructure.com/doc/api/file.oauth.html#using-access-tokens), although the easiest way to obtain one is via Canvas's web interface under "Profile/Account" and "Settings", then selecting "+New Access Token". The API base is simply the base address you use to access Canvas's web interface, e.g. "https://school-name.instructure.com/". You can set both environmental variables in your shell, e.g.:
```sh
export CANVAS_ACCESS_TOKEN="0123456789"
export CANVAS_API_BASE="https://school-name.instructure.com/"
```

If you plan on using this tool often, you can add these commands to your `~/.bashrc`. Make sure you use `https` if your Canvas instance supports it, otherwise POST requests might be redirected to the secured version improperly.

Now you can start using the script. To list all of the courses available to you,
```sh
$ ./canvas-export.py --list
BIOL-101    Intro to Biology
PSYC-100    Intro to Pyschology
BIOL-101 Lab    Intro to Biology Lab Component
```

To export courses, list the ones you wish to export by code or id. Ids are exposed in the URL of a course's page through the Canvas web interface. You may need to surround course codes with quotes if they contain spaces or special characters.
```sh
$ ./canvas-export.py "BIOL-101 Lab" 100123
Requesting 'BIOL-101 Lab.zip'
Export 100% complete
Downloading 'BIOL-101 Lab.zip'
Download complete
Requesting 'PSYC-100.zip'
Export 1% complete
Export 100% complete
Downloading 'PSYC-100.zip'
Download complete
```

To see full list of options, run
```sh
$ ./canvas-export.py -h
```

## Warnings
As noted in the [API documentation](https://canvas.instructure.com/doc/api/), parts of the API, including the [Content Exports API](https://canvas.instructure.com/doc/api/content_exports.html#ContentExport) used here is still in beta and is subject to breaking changes.

## License
Copyright 2017 Matthew Howard

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgements
Two of the methods in the `CanvasClient` class, `_request` and `_consume_pagination` are due to Christian Barcenas ([@cbarcenas](https://github.com/cbarcenas)) and are used with permission.