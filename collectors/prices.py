"""
Collector: daily stock prices.

Reads tickers from config/tickers.yaml and writes rows in the shared data format:
  date, ticker, signal, value, source

Run from the repo root:
  python collectors/prices.py
"""

# TODO: implement in a follow-up issue (pull daily closes, cache results).


def main() -> None:
    print("prices collector: not implemented yet")


if __name__ == "__main__":
    main()
