"""
Technical analysis service - Technical analysis service
"""
import math
from typing import Dict, List, Optional, Any

class TechnicalAnalysis:
    """Technical analysis service"""
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50.0  # Default neutral value
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50.0
        
        # Calculate average gains and losses
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(rsi, 2)
    
    def calculate_macd(self, prices: List[float], fast_period: int = 12, 
                      slow_period: int = 26, signal_period: int = 9) -> Dict[str, float]:
        """Calculate MACD indicator"""
        if len(prices) < slow_period:
            return {"macd": 0, "signal": 0, "histogram": 0}
        
        # Calculate EMA
        def calculate_ema(data: List[float], period: int) -> List[float]:
            if len(data) < period:
                return data
            
            ema = [data[0]]
            multiplier = 2 / (period + 1)
            
            for i in range(1, len(data)):
                ema_value = (data[i] * multiplier) + (ema[i-1] * (1 - multiplier))
                ema.append(ema_value)
            
            return ema
        
        ema_fast = calculate_ema(prices, fast_period)
        ema_slow = calculate_ema(prices, slow_period)
        
        # Calculate MACD line
        macd_line = []
        for i in range(len(ema_fast)):
            if i < len(ema_slow):
                macd_line.append(ema_fast[i] - ema_slow[i])
        
        if len(macd_line) < signal_period:
            return {"macd": 0, "signal": 0, "histogram": 0}
        
        # Calculate signal line
        signal_line = calculate_ema(macd_line, signal_period)
        
        # Calculate histogram
        histogram = []
        for i in range(len(macd_line)):
            if i < len(signal_line):
                histogram.append(macd_line[i] - signal_line[i])
        
        return {
            "macd": round(macd_line[-1], 4),
            "signal": round(signal_line[-1], 4),
            "histogram": round(histogram[-1], 4)
        }
    
    def calculate_support_resistance(self, prices: List[float]) -> Dict[str, float]:
        """Calculate support and resistance levels"""
        if len(prices) < 10:
            return {"support": prices[-1] * 0.95, "resistance": prices[-1] * 1.05}
        
        # Simple support and resistance calculation
        recent_prices = prices[-20:]  # Recent 20 price points
        min_price = min(recent_prices)
        max_price = max(recent_prices)
        current_price = prices[-1]
        
        # Support level: 90% of recent low
        support = min_price * 0.9
        
        # Resistance level: 110% of recent high
        resistance = max_price * 1.1
        
        return {
            "support": round(support, 4),
            "resistance": round(resistance, 4)
        }
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, 
                                 std_dev: float = 2) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            current_price = prices[-1] if prices else 0
            return {
                "upper": current_price * 1.1,
                "middle": current_price,
                "lower": current_price * 0.9
            }
        
        recent_prices = prices[-period:]
        sma = sum(recent_prices) / len(recent_prices)
        
        # Calculate standard deviation
        variance = sum((price - sma) ** 2 for price in recent_prices) / len(recent_prices)
        std = math.sqrt(variance)
        
        return {
            "upper": round(sma + (std * std_dev), 4),
            "middle": round(sma, 4),
            "lower": round(sma - (std * std_dev), 4)
        }
    
    def analyze_trend(self, prices: List[float]) -> str:
        """Analyze trend"""
        if len(prices) < 5:
            return "Sideways"
        
        recent_prices = prices[-5:]
        
        # Calculate short-term and long-term moving averages
        short_ma = sum(recent_prices[-3:]) / 3
        long_ma = sum(recent_prices) / 5
        
        if short_ma > long_ma * 1.02:
            return "Uptrend"
        elif short_ma < long_ma * 0.98:
            return "Downtrend"
        else:
            return "Sideways"
    
    def get_technical_indicators(self, prices: List[float]) -> Dict[str, Any]:
        """Get all technical indicators"""
        if not prices or len(prices) < 5:
            return {
                "rsi": 50,
                "macd": {"macd": 0, "signal": 0, "histogram": 0},
                "support_resistance": {"support": 0, "resistance": 0},
                "bollinger_bands": {"upper": 0, "middle": 0, "lower": 0},
                "trend": "Sideways"
            }
        
        return {
            "rsi": self.calculate_rsi(prices),
            "macd": self.calculate_macd(prices),
            "support_resistance": self.calculate_support_resistance(prices),
            "bollinger_bands": self.calculate_bollinger_bands(prices),
            "trend": self.analyze_trend(prices)
        }
