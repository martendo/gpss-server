# gpss-server
A web service to run GPSS programs, using [gpss.py][gpss.py]

Server hosted at https://gpss-server.herokuapp.com

## Running a Simulation
To run a gpss.py program with gpss-server, send a `POST` request with
the program in the request body.

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
}
```

[gpss.py]: https://github.com/martendo/gpss.py
[gpss.py-examples]: https://martendo.github.io/gpss.py/examples
[json]: https://json.org
