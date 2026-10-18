"""Read-only MetaTrader 5 helper. No order submission methods are implemented."""


def get_mt5_status() -> dict[str, object]:
    try:
        import MetaTrader5 as mt5
    except ImportError:
        return {"available": False, "message": "Package MetaTrader5 non installé."}

    try:
        if not mt5.initialize():
            return {"available": False, "message": f"Initialisation MT5 impossible : {mt5.last_error()}"}
        terminal = mt5.terminal_info()
        account = mt5.account_info()
        return {
            "available": True,
            "terminal_connected": terminal is not None,
            "account_connected": account is not None,
            "login": getattr(account, "login", None) if account else None,
            "server": getattr(account, "server", None) if account else None,
            "mode": "read-only",
        }
    finally:
        mt5.shutdown()
