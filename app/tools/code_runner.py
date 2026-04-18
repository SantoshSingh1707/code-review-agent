import io
import contextlib
import traceback

class ExecutionResult:
    def __init__(self, success: bool, output: str = "", error: str = "", return_value: any = None):
        self.success = success
        self.output = output
        self.error = error
        self.return_value = return_value

def run_code(code: str, timeout: int = 5) -> ExecutionResult:
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
        try:
            compiled = compile(code, "<string>", "exec")
            
            global_vars = {"__builtins__": __builtins__}
            
            exec(compiled, global_vars)
            
            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()
            
            if stderr_output:
                return ExecutionResult(
                    success=False,
                    output=stdout_output,
                    error=stderr_output
                )
            
            return ExecutionResult(
                success=True,
                output=stdout_output,
                return_value=global_vars
            )
            
        except Exception as e:
            error_msg = str(e)
            traceback_msg = traceback.format_exc()
            
            return ExecutionResult(
                success=False,
                output=stdout_capture.getvalue(),
                error=error_msg + "\n" + traceback_msg
            )

def run_function(code: str, function_name: str, args: tuple = (), kwargs: dict = None) -> ExecutionResult:
    if kwargs is None:
        kwargs = {}
    
    args_str = ", ".join(repr(a) for a in args)
    code_with_call = f"{code}\n__result__ = {function_name}({args_str})"
    
    result = run_code(code_with_call)
    
    if result.success and result.return_value:
        result.return_value = result.return_value.get("__result__")
    
    return result