# gpss-server
A web service to run GPSS programs, using [gpss.py][gpss.py]

Server hosted at https://gpss-server.herokuapp.com

## Running a Simulation
To run a gpss.py program with gpss-server, send a `POST` request with
the program in the request body.

[Web gpss.py][web-gpss.py] uses something along the lines of this:
```javascript
const request = new XMLHttpRequest();
request.open("POST", "https://gpss-server.herokuapp.com");
request.send(program);
```

## Response
gpss-server will respond in [JSON][json]. Based on the status, the
object that is sent back will look a little different.

### Success
The simulation has completed successfully.

The response object will look like this:
```javascript
{
  status: "success",
  report: string,
  warnings: [{
    linenum: integer,
    message: string,
  }, ... ],
  messages: [{
    linenum: integer,
    message: string,
    type: ("parser-error" | "simulation-error" | "warning"),
  }, ... ],
}
```

For some examples of what the simulation report might look like, see
[the gpss.py examples page][gpss.py-examples].

### Parser Error
One or more errors occurred while parsing the program.

The response object will look like this:
```javascript
{
  status: "parser-error",
  message: "Parsing failed with X error(s)",
  errors: [{
    linenum: integer,
    message: string,
  }, ... ],
  warnings: [{
    linenum: integer,
    message: string,
  }, ... ],
  messages: [{
    linenum: integer,
    message: string,
    type: ("parser-error" | "simulation-error" | "warning"),
  }, ... ],
}
```

### Simulation Error
An error occurred during simulation.

The response object will look like this:
```javascript
{
  status: "simulation-error",
  message: "Simulation Error",
  error: {
    linenum: integer,
    message: string,
  },
  warnings: [{
    linenum: integer,
    message: string,
  }, ... ],
  messages: [{
    linenum: integer,
    message: string,
    type: ("parser-error" | "simulation-error" | "warning"),
  }, ... ],
}
```

[gpss.py]: https://github.com/martendo/gpss.py
[gpss.py-examples]: https://martendo.github.io/gpss.py/examples
[web-gpss.py]: https://martendo.github.io/gpss.py/web
[json]: https://json.org
