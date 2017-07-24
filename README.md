# Canvas Course Exporter
A Python-based command-line utility to export a user's courses to their local filesystem.

## Usage
This tool relies on two environmental variables: `CANVAS_ACCESS_TOKEN` and
`CANVAS_API_BASE`. The access token is documented [here](https://canvas.instructure.com/doc/api/file.oauth.html#using-access-tokens), although the easiest way to obtain one is via Canvas's web interface under "Profile/Account" and "Settings", then selecting "+New Access Token". The API base is simply the base address you use to access Canvas's web interface, e.g. "http://school-name.instructure.com/". You can set both environmental variables in your shell, e.g.:
```sh
export CANVAS_ACCESS_TOKEN="0123456789"
export CANVAS_API_BASE="http://school-name.instructure.com/"
```

If you plan on using this script often, you can add these commands to your `~/.bashrc`

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
BIOL-101    Intro to Biology
PSYC-100    Intro to Pyschology
    Intro to Biology Lab Component
```

## Warnings
As noted in the [API documentation](https://canvas.instructure.com/doc/api/), parts of the API, including the [Content Exports API](https://canvas.instructure.com/doc/api/content_exports.html#ContentExport) used here is still in beta and is subject to breaking changes.

## License

## Acknowledgements
