"""Utility functions.
"""
import base64
import logging
import re
from typing import Any, Dict, List, NoReturn, Optional, Set, Tuple, Union

from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message

def fromStr(valstr: str) -> Any:
    """Try to parse as int, float or bool (and fallback to a string as last resort)

    Returns: an int, bool, float, str or byte array (for strings of hex digits)

    Args:
        valstr (string): A user provided string
    """
    val: Any
    if len(valstr) == 0:  # Treat an emptystring as an empty bytes
        val = bytes()
    elif valstr.startswith("0x"):
        # if needed convert to string with asBytes.decode('utf-8')
        val = bytes.fromhex(valstr[2:].zfill(2))
    elif valstr.startswith("base64:"):
        val = base64.b64decode(valstr[7:])
    elif valstr.lower() in {"t", "true", "yes"}:
        val = True
    elif valstr.lower() in {"f", "false", "no"}:
        val = False
    else:
        try:
            val = int(valstr)
        except ValueError:
            try:
                val = float(valstr)
            except ValueError:
                val = valstr  # Not a float or an int, assume string
    return val



def toStr(raw_value):
    """Convert a value to a string that can be used in a config file"""
    if isinstance(raw_value, bytes):
        return "base64:" + base64.b64encode(raw_value).decode("utf-8")
    return str(raw_value)


def pskToString(psk: bytes) -> str:
    """Given an array of PSK bytes, decode them into a human readable (but privacy protecting) string"""
    if len(psk) == 0:
        return "unencrypted"
    elif len(psk) == 1:
        b = psk[0]
        if b == 0:
            return "unencrypted"
        elif b == 1:
            return "default"
        else:
            return f"simple{b - 1}"
    else:
        return "secret"


def stripnl(s) -> str:
    """Remove newlines from a string (and remove extra whitespace)"""
    s = str(s).replace("\n", " ")
    return " ".join(s.split())


def fixme(message: str) -> None:
    """Raise an exception for things that needs to be fixed"""
    raise Exception(f"FIXME: {message}") # pylint: disable=W0719


def catchAndIgnore(reason: str, closure) -> None:
    """Call a closure but if it throws an exception print it and continue"""
    try:
        closure()
    except BaseException as ex:
        logging.error(f"Exception thrown in {reason}: {ex}")


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__ # type: ignore[assignment]
    __delattr__ = dict.__delitem__ # type: ignore[assignment]


def remove_keys_from_dict(keys: Union[Tuple, List, Set], adict: Dict) -> Dict:
    """Return a dictionary without some keys in it.
    Will removed nested keys.
    """
    for key in keys:
        try:
            del adict[key]
        except:
            pass
    for val in adict.values():
        if isinstance(val, dict):
            remove_keys_from_dict(keys, val)
    return adict


def hexstr(barray: bytes) -> str:
    """Print a string of hex digits"""
    return ":".join(f"{x:02x}" for x in barray)


def snake_to_camel(a_string: str) -> str:
    """convert snake_case to camelCase"""
    # split underscore using split
    temp = a_string.split("_")
    # joining result
    result = temp[0] + "".join(ele.title() for ele in temp[1:])
    return result

def camel_to_snake(a_string: str) -> str:
    """convert camelCase to snake_case"""
    return "".join(["_" + i.lower() if i.isupper() else i for i in a_string]).lstrip(
        "_"
    )
