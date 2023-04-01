from __future__ import annotations

import ipaddress
from marshmallow.fields import IP, IPInterface
from marshmallow        import validate, utils, class_registry, types

_CVAR_HEAD='_cvar.'

class netdbIP(IP):

    def _serialize(self, value, attr, obj, **kwargs) -> str | None:
        if isinstance(value, str) and value.startswith('_CVAR_HEAD'):
            if value is None:
                return None
            return utils.ensure_text_type(value)
        else:
            super()._serialize(value, attr, obj, **kwargs)


    def _deserialize(
            self, value, attr, data, **kwargs
        ) -> ipaddress.IPv4Address | ipaddress.IPv6Address | str | None:
        if isinstance(value, str) and value.startswith(_CVAR_HEAD):
            if not isinstance(value, (str, bytes)):
                raise self.make_error("invalid")
            try:
                return utils.ensure_text_type(value)
            except UnicodeDecodeError as error:
                raise self.make_error("invalid_utf8") from error
        else:
            super()._deserialize(value, attr, data, **kwargs)


class netdbIPv4(netdbIP):
    """A IPv4 address field.

    .. versionadded:: 3.8.0
    """
    default_error_messages = {"invalid_ip": "Requires a valid IPv4 address, router id, GRE key or netdb cvar."}

    DESERIALIZATION_CLASS = ipaddress.IPv4Address


class netdbIPv6(netdbIP):
    """A IPv6 address field.

    .. versionadded:: 3.8.0
    """
    default_error_messages = {"invalid_ip": "Requires a valid IPv6 address or a netdb cvar."}

    DESERIALIZATION_CLASS = ipaddress.IPv6Address


class netdbIPInterface(IPInterface):

    def _serialize(self, value, attr, obj, **kwargs) -> str | None:
        if isinstance(value, str) and value.startswith('_CVAR_HEAD'):
            if value is None:
                return None
            return utils.ensure_text_type(value)
        else:
            super()._serialize(value, attr, obj, **kwargs)


    def _deserialize(
            self, value, attr, data, **kwargs
        ) -> ipaddress.IPv4Interface | ipaddress.IPv6Interface | str | None:
        if isinstance(value, str) and value.startswith('_CVAR_HEAD'):
            if not isinstance(value, (str, bytes)):
                raise self.make_error("invalid")
            try:
                return utils.ensure_text_type(value)
            except UnicodeDecodeError as error:
                raise self.make_error("invalid_utf8") from error
        else:
            super()._deserialize(value, attr, data, **kwargs)


class netdbIPv4Interface(netdbIPInterface):
    """A IPv4 Network Interface field."""

    default_error_messages = {"invalid_ip_interface": "Requires a valid IPv4 interface (prefix) or a netdb cvar."}

    DESERIALIZATION_CLASS = ipaddress.IPv4Interface


class netdbIPv6Interface(netdbIPInterface):
    """A IPv6 Network Interface field."""

    default_error_messages = {"invalid_ip_interface": "Requires a valid IPv6 interface (prefix) or a netdb cvar."}

    DESERIALIZATION_CLASS = ipaddress.IPv6Interface
