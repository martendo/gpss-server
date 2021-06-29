from os import environ
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from json import dumps
from gpss import gpss

# Put important properties from an error object into a serializable dict
def errordict(error):
    if isinstance(error, gpss.error.SimulationError):
        type_ = "simulation-error"
    elif isinstance(error, gpss.error.ParserError):
        type_ = "parser-error"
    elif isinstance(error, gpss.error.ExecutionWarning):
        type_ = "warning"
    else:
        raise TypeError(f"Unknown error type \"{error.__name__}\"")
    return {
        "linenum": error.linenum,
        "message": error.message,
        "type": type_
    }

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get program from request
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length).decode("utf-8")
        
        response = {}
        
        # Clear any warnings and messages from a previous simulation
        gpss.warnings.clear()
        gpss.messages.clear()
        
        # Parse program from request
        gpss.parse(program=data)
        
        if len(gpss.parser.errors):
            # There were parser errors
            response["status"] = "parser-error"
            response["message"] = (
                f"Parsing failed with {len(gpss.parser.errors)} "
                f"error{'s' if len(gpss.parser.errors) != 1 else ''}"
            )
            response["errors"] = list(map(errordict, gpss.parser.errors))
        else:
            # No parser errors, try to run the simulation
            try:
                # Reset simulation for fresh run
                gpss.simulation.__init__()
                gpss.run()
            except gpss.error.SimulationError as error:
                # Simulation failed
                response["status"] = "simulation-error"
                response["message"] = "Simulation Error"
                response["error"] = errordict(error)
            else:
                # Simulation was completed successfully
                response["status"] = "success"
                response["report"] = gpss.createReport()
        response["warnings"] = list(map(errordict, gpss.warnings))
        response["messages"] = list(map(errordict, gpss.messages))
        
        # Send response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(dumps(response).encode("utf-8"))

def run():
    server = ThreadingHTTPServer(("", int(environ["PORT"])), RequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
