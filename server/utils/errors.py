# Copyright 2019-2020 SURF.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import random
import string
import sys
import traceback
from http import HTTPStatus
from typing import TYPE_CHECKING, Dict, Optional, Tuple, cast

import structlog

from server.types import ErrorDict, ErrorState

logger = structlog.get_logger(__name__)


def format_ex(ex, stacklimit=None):
    """
    Format an exception with a pseudo-random key and the shown exception.

    Returns a tuple of the exception string and key.
    """
    key = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    s = show_ex(ex, stacklimit)
    return key, "[{}] {}".format(key, s)


def show_ex(ex, stacklimit=None):
    """
    Show an exception, including its class name, message and (limited) stacktrace.

    >>> try:
    ...     raise Exception("Something went wrong")
    ... except Exception as e:
    ...     print(show_ex(e))
    Exception: Something went wrong
    ...
    """
    tbfmt = "".join(traceback.format_tb(ex.__traceback__, stacklimit))
    return "{}: {}\n{}".format(type(ex).__name__, ex, tbfmt)


# Todo: decide if this can be removed.
class ApiException(Exception):
    """Api Exception Class.

    This is a copy of what is generated in api_clients that are used to connect to external REST api's.
    """

    status: Optional[HTTPStatus]
    reason: Optional[str]
    body: Optional[str]
    headers: Dict[str, str]

    def __init__(
        self,
        status: Optional[HTTPStatus] = None,
        reason: Optional[str] = None,
        http_resp: Optional[object] = None,
    ):
        super().__init__(status, reason, http_resp)
        if http_resp:
            self.status = http_resp.status  # type:ignore
            self.reason = http_resp.reason  # type:ignore
            self.body = http_resp.data  # type:ignore
            self.headers = http_resp.getheaders()  # type:ignore
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = {}

    def __str__(self) -> str:
        """Create custom error messages for exception."""
        error_message = "({})\n" "Reason: {}\n".format(self.status, self.reason)
        if self.headers:
            error_message += f"HTTP response headers: {self.headers}\n"

        if self.body:
            error_message += f"HTTP response body: {self.body}\n"

        return error_message


def is_api_exception(ex: Exception) -> bool:
    """Test for swagger-codegen ApiException.

    For each API, swagger-codegen generates a new ApiException class. These are not organized into
    a hierarchy. Hence testing whether one is dealing with one of the ApiException classes without knowing how
    many there are and where they are located, needs some special logic.

    Args:
        ex: the Exception to be tested.

    Returns:
        True if it is an ApiException, False otherwise.

    """
    return ex.__class__.__name__ == "ApiException"


# Todo: decide if this can be removed.
def error_state_to_dict(err: ErrorState) -> ErrorDict:
    """Return an ErrorDict based on the exception, string or tuple in the ErrorState.

    Args:
        err: ErrorState from a api error state

    Returns:
        An ErrorDict containing the error message a status_code and a traceback if available

    """
    # Import here to prevent cyclic imports
    from server.forms import FormNotCompleteError, FormValidationError

    if isinstance(err, FormValidationError):
        return {
            "class": type(err).__name__,
            "error": str(err),
            "traceback": err,
            "validation_errors": err.errors,  # type:ignore
            "status_code": HTTPStatus.BAD_REQUEST,
        }
    elif isinstance(err, FormNotCompleteError):
        return {
            "class": type(err).__name__,
            "error": str(err),
            "traceback": err,
            "form": err.form,
            "status_code": HTTPStatus.NOT_EXTENDED,
        }
    elif isinstance(err, Exception):
        if is_api_exception(err):
            err = cast(ApiException, err)
            return {
                "class": type(err).__name__,
                "error": err.reason,
                "status_code": err.status,
                "body": err.body,
                "headers": "\n".join(f"{k}: {v}" for k, v in err.headers.items()),
                "traceback": err,
            }
        return {
            "class": type(err).__name__,
            "error": str(err),
            "traceback": show_ex(err),
        }
    elif isinstance(err, tuple):
        cast(Tuple, err)
        error, status_code = err
        return {"error": str(error), "status_code": int(status_code)}
    elif isinstance(err, str):
        return {"error": err}
    elif isinstance(err, dict) and "error" in err:  # type: ignore
        return err
    else:
        raise TypeError("ErrorState  should be a tuple, exception or string")


def post_mortem(debugger: str, error: ErrorState) -> ErrorState:
    if isinstance(error, Exception) and hasattr(error, "__traceback__"):
        if debugger == "web_pdb":
            try:
                import web_pdb
            except ImportError:
                logger.critical("web_pd could not be imported for post mortem debugging")
                return error
            web_pdb.post_mortem(error.__traceback__)
        elif debugger == "print":
            print(error, file=sys.stderr)  # noqa: T001
        elif debugger == "reraise":
            # This exception will normally be suppressed by threadpoolexecutor.
            # When env var TESTING is set the exception will be raised when .result() is called on the future
            raise error
    return error
