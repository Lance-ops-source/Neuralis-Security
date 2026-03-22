
"""
NEURALIS SENSOR v1.0 - DEBUGGED
The beginning of something big.
"""

import time
import json
from pynput import keyboard
from datetime import datetime
import os

print("🧠 NEURALIS SENSOR v1.0")
print("=" * 50)
print("Capturing your unique typing fingerprint...")
print()

class NeuralisSensor:
    def __init__(self):
        self.typing_data = []
        self.start_time = None
        self.key_count = 0
        self.is_recording = False
        
    def on_press(self, key):
        """Called when you press a key"""
        if not self.is_recording:
            # Don't record until user starts
            return
        
        if self.start_time is None:
            self.start_time = time.time()
            print("🎤 Recording started...")
            print("Type naturally. Press ESC when done.")
            print("-" * 40)
        
        self.key_count += 1
        
        # Get the key character
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key).replace("Key.", "")
        
        # Calculate time since start
        current_time = time.time()
        time_since_start = (current_time - self.start_time) * 1000  # Convert to milliseconds
        
        # Store the data
        self.typing_data.append({
            'key': key_char,
            'time_ms': round(time_since_start, 2),
            'count': self.key_count
        })
        
        # Show what you're typing
        if key_char == " ":
            display = "[SPACE]"
        elif key_char == "'enter'":
            display = "[ENTER]"
        elif len(key_char) > 1:
            display = f"[{key_char.upper()}]"
        else:
            display = key_char
        
        print(f"Key {self.key_count}: {display}", end=" ", flush=True)
    
    def on_release(self, key):
        """Called when you release a key"""
        if key == keyboard.Key.esc:
            print("\n\n🛑 Recording stopped.")
            self.is_recording = False
            self.save_data()
            return False
    
    def start_recording(self):
        """Start the recording session"""
        print("Ready to record your typing rhythm...")
        self.is_recording = True
        self.typing_data = []
        self.start_time = None
        self.key_count = 0
        
    def save_data(self):
        """Save your typing data"""
        if len(self.typing_data) < 5:
            print("❌ Not enough data. Please type more.")
            return
        
        # Create data folder
        if not os.path.exists("neuralis_data"):
            os.makedirs("neuralis_data")
        
        # Calculate time gaps between keys
        gaps = []
        for i in range(1, len(self.typing_data)):
            gap = self.typing_data[i]['time_ms'] - self.typing_data[i-1]['time_ms']
            gaps.append(round(gap, 2))
        
        # Create session data
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'total_keys': self.key_count,
            'total_time_ms': round((time.time() - self.start_time) * 1000, 2),
            'keys_typed': [d['key'] for d in self.typing_data],
            'gaps_ms': gaps,
            'average_gap': round(sum(gaps) / len(gaps), 2) if gaps else 0
        }
        
        # Save to file
        filename = f"neuralis_data/session_{session_id}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved: {filename}")
        print(f"📊 Keys typed: {self.key_count}")
        if gaps:
            print(f"⏱️  Average gap: {data['average_gap']} ms")
        print(f"🔑 Your neural signature captured!")

def main():
    """Main function"""
    sensor = NeuralisSensor()
    
    print("Welcome to Neuralis.")
    print("We're going to capture your unique typing rhythm.")
    print()
    
    input("Press Enter to begin...")
    print()
    
    sensor.start_recording()
    
    # Start listening to keyboard
    with keyboard.Listener(
        on_press=sensor.on_press,
        on_release=sensor.on_release
    ) as listener:
        listener.join()
    
    print("\n" + "=" * 50)
    print("✅ NEURALIS SENSOR COMPLETE!")
    print("Your typing fingerprint has been saved.")
    print("Check the 'neuralis_data' folder.")

if __name__ == "__main__":
    main()