"""
NEURALIS LIVE SENSOR - Real-time Human Score Display
Watch your typing authenticity score update as you type!
"""

import time
import math
from pynput import keyboard

print("🧠 NEURALIS LIVE - Real-time Human Score")
print("=" * 50)
print("Type naturally and watch your score evolve!")
print()

class LiveNeuralisSensor:
    def __init__(self):
        self.typing_gaps = []
        self.last_time = None
        self.key_count = 0
        self.start_time = time.time()
        self.is_recording = False
        
    def calculate_live_score(self):
        """Calculate real-time Human Score"""
        if len(self.typing_gaps) < 5:
            return 0, "Keep typing..."
        
        try:
            gaps = self.typing_gaps
            avg_gap = sum(gaps) / len(gaps)
            
            # Calculate standard deviation safely
            variance = sum((x - avg_gap) ** 2 for x in gaps) / len(gaps)
            std_gap = math.sqrt(variance)
            
            if avg_gap > 0:
                cv = (std_gap / avg_gap) * 100  # Coefficient of Variation
            else:
                cv = 0
            
            # Human scoring algorithm
            if cv < 10:
                score = 20
                feedback = "Too robotic 🤖"
            elif cv > 60:
                score = 40  
                feedback = "Too erratic 🎢"
            elif 15 <= cv <= 50:
                score = 85
                feedback = "Perfect human! 🎯"
            else:
                score = 60
                feedback = "Getting there... 📈"
                
            return score, feedback
            
        except Exception:
            return 0, "Calculating..."
    
    def on_press(self, key):
        if not self.is_recording:
            self.is_recording = True
            self.start_time = time.time()
        
        current_time = time.time()
        
        # Calculate gap since last key
        if self.last_time:
            gap = (current_time - self.last_time) * 1000  # Convert to milliseconds
            self.typing_gaps.append(round(gap, 2))
        
        self.last_time = current_time
        self.key_count += 1
        
        # Show key press
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key).replace("Key.", "")
        
        # Display formatting
        if key_char == " ":
            display = "␣"
        elif key_char == "'enter'":
            display = "↵"
        elif len(key_char) > 1:
            display = f"[{key_char}]"
        else:
            display = key_char
            
        print(display, end="", flush=True)
        
        # Update score every 5 keys (but only if we have enough data)
        if self.key_count % 5 == 0 and len(self.typing_gaps) >= 5:
            score, feedback = self.calculate_live_score()
            print(f"\n🎯 Score: {score}/100 | {feedback} | Keys: {self.key_count}")
            print("Continue typing... ", end="", flush=True)
    
    def on_release(self, key):
        if key == keyboard.Key.esc:
            final_score, feedback = self.calculate_live_score()
            total_time = time.time() - self.start_time
            
            print(f"\n\n" + "=" * 50)
            print(f"✅ SESSION COMPLETE!")
            print(f"🎯 Final Human Score: {final_score}/100")
            print(f"📊 Keys typed: {self.key_count}")
            print(f"⏱️  Time: {total_time:.1f}s")
            print(f"💡 {feedback}")
            print("=" * 50)
            return False
    
    def start(self):
        print("🎤 Start typing naturally...")
        print("💡 Score updates every 5 keystrokes")
        print("⏎ Press ESC when done\n")
        print("Typing: ", end="", flush=True)
        
        self.is_recording = True
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

# Run the live sensor
if __name__ == "__main__":
    sensor = LiveNeuralisSensor()
    sensor.start()
