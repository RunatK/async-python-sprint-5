from tcp_latency import measure_latency

from core.config import CONNECTED_SERVERS
from db.helpers.status import status


def servers_ping() -> dict[str]:
    """
    Return all connected servers ping
    """
    try:
        results: dict[str, str] = {}
        for server in CONNECTED_SERVERS:
            host = CONNECTED_SERVERS[server]["host"]
            port = CONNECTED_SERVERS[server]["port"]
            ping_result = measure_latency(host=host, port=port)
            if len(ping_result) == 0:
                results[server] = 'Error, server was not found.'
                continue
            results[server] = ping_result[-1]
        return results
    except KeyError:
        raise KeyError("Server from from CONNECTED_SERVERS must have params 'host' and 'port'")