"""
========================================================
ZF AI TRADER
File    : weights.py
Folder  : config
Versi   : 0.1.0
Tanggal : 07 Juli 2026

Fungsi:
Menyimpan seluruh bobot (weight)
yang digunakan oleh ZF Score Engine.

Dipanggil oleh:
- strategy/zf_score.py
========================================================
"""

# ==================================================
# TREND SCORE
# ==================================================

TREND_STRONG_BULLISH = 40
TREND_BULLISH = 30

TREND_STRONG_BEARISH = -40
TREND_BEARISH = -30

TREND_SIDEWAYS = 0


# ==================================================
# MOMENTUM SCORE
# ==================================================

MOMENTUM_BULLISH = 25
MOMENTUM_BEARISH = -25

MOMENTUM_OVERBOUGHT = -15
MOMENTUM_OVERSOLD = 15

MOMENTUM_NEUTRAL = 0


# ==================================================
# VOLATILITY SCORE
# ==================================================

VOLATILITY_HIGH = 10
VOLATILITY_MEDIUM = 5
VOLATILITY_LOW = 0


# ==================================================
# MULTI TIMEFRAME SCORE
# (Dipakai pada versi berikutnya)
# ==================================================

MTF_FULL_CONFIRM = 30
MTF_PARTIAL_CONFIRM = 15
MTF_NO_CONFIRM = 0


# ==================================================
# SUPPORT & RESISTANCE
# (Dipakai pada versi berikutnya)
# ==================================================

SUPPORT_BOUNCE = 20
RESISTANCE_REJECTION = -20

BREAKOUT_VALID = 25
BREAKOUT_FALSE = -25


# ==================================================
# MARKET STRUCTURE
# (Dipakai pada versi berikutnya)
# ==================================================

HIGHER_HIGH = 20
HIGHER_LOW = 15

LOWER_HIGH = -15
LOWER_LOW = -20


# ==================================================
# CANDLE PATTERN
# (Dipakai pada versi berikutnya)
# ==================================================

BULLISH_ENGULFING = 15
BEARISH_ENGULFING = -15

PINBAR_BULLISH = 10
PINBAR_BEARISH = -10

DOJI = 0


# ==================================================
# SESSION SCORE
# (Dipakai pada versi berikutnya)
# ==================================================

LONDON_SESSION = 15
NEWYORK_SESSION = 15

ASIA_SESSION = 5

SESSION_CLOSED = -100


# ==================================================
# NEWS FILTER
# (Dipakai pada versi berikutnya)
# ==================================================

HIGH_IMPACT_NEWS = -100
MEDIUM_IMPACT_NEWS = -20
LOW_IMPACT_NEWS = 0


# ==================================================
# SPREAD FILTER
# (Dipakai pada versi berikutnya)
# ==================================================

GOOD_SPREAD = 10
NORMAL_SPREAD = 5
HIGH_SPREAD = -30


# ==================================================
# LIQUIDITY
# (Dipakai pada versi berikutnya)
# ==================================================

HIGH_LIQUIDITY = 10
LOW_LIQUIDITY = -10


# ==================================================
# ATR FILTER
# (Dipakai pada versi berikutnya)
# ==================================================

ATR_GOOD = 10
ATR_LOW = -10


# ==================================================
# ZF SCORE THRESHOLD
# ==================================================

BUY_SCORE = 40
SELL_SCORE = -40

WAIT_MIN = -39
WAIT_MAX = 39