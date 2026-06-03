import time
import random
from functools import wraps

# @timer — measures execution time
def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - t0) * 1000
        print(f"[timer] {fn.__name__} took {elapsed_ms:.3f} ms")
        return result
    return wrapper

# @retry(n) — reruns on failure up to n times, re-raises last error
def retry(n):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, n + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"[retry] {fn.__name__} attempt {attempt}/{n} failed: {e}")
            raise last_exc
        return wrapper
    return decorator

# @log_calls — prints inputs, calls fn, prints output, returns it
def log_calls(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        arg_str = ", ".join(repr(a) for a in args)
        kw_str  = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
        signature = ", ".join(s for s in (arg_str, kw_str) if s)
        print(f"[log] {fn.__name__}({signature})")
        result = fn(*args, **kwargs)
        print(f"[log] {fn.__name__} -> {result!r}")
        return result
    return wrapper

# Dummy functions
@timer
def slow_sum(n):
    """sum 0..n-1 the lazy way"""
    total = 0
    for i in range(n):
        total += i
    return total

# fails twice, then works — to prove retry actually retries
_flaky_calls = {"count": 0}

@retry(3)
def flaky_fetch(url):
    """pretends to be a network call that fails twice"""
    _flaky_calls["count"] += 1
    if _flaky_calls["count"] < 3:
        raise ConnectionError(f"could not reach {url}")
    return {"url": url, "status": 200}

@log_calls
def greet(name, loud=False):
    msg = f"hi {name}"
    return msg.upper() if loud else msg

# Stacking: order matters

# Decorators apply BOTTOM-UP. Reading the source from top to bottom,
# the bottom decorator wraps fn first, then the one above wraps THAT.
# At call time, the OUTER (topmost) wrapper runs first.
@timer
@log_calls
def add(a, b):
    """timer wraps log_calls(add). call order: timer -> log -> add."""
    return a + b

@log_calls
@timer
def multiply(a, b):
    """log_calls wraps timer(multiply). call order: log -> timer -> multiply."""
    return a * b

# Main
def main():
    print("=== @timer ===")
    slow_sum(100_000)

    print("\n=== @retry(3) ===")
    result = flaky_fetch("https://example.com")
    print(f"got: {result}")

    print("\n=== @log_calls ===")
    greet("yuvraj", loud=True)

    print("\n=== stacked: @timer over @log_calls ===")
    add(2, 3)
    # timer prints LAST because it's the outer wrapper —
    # it sees the whole log_calls(add) call as a single unit.

    print("\n=== stacked: @log_calls over @timer ===")
    multiply(4, 5)
    # timer prints in the MIDDLE — log_calls wraps it, so log's
    # "called" line is first, timer runs inside, log's "returned" is last.

    print("\n=== metadata check (functools.wraps doing its job) ===")
    print(f"slow_sum.__name__ = {slow_sum.__name__}")
    print(f"slow_sum.__doc__  = {slow_sum.__doc__}")

if __name__ == "__main__":
    main()