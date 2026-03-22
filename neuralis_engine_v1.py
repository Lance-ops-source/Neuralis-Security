"""
NEURALIS ENGINE v1.0 - DEBUGGED
Analyzes typing patterns to detect humans vs bots.
"""

import json
import os
import numpy as np
from datetime import datetime

print("🧠 NEURALIS ENGINE v1.0")
print("=" * 60)

class NeuralisEngine:
    def __init__(self):
        self.data_dir = "neuralis_data"
        self.profiles_dir = "neuralis_profiles"
        
        # Create directories if they don't exist
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)
    
    def load_sessions(self):
        """Load all typing sessions"""
        if not os.path.exists(self.data_dir):
            print("❌ No neuralis_data folder found!")
            print("Run the sensor first to collect data.")
            return []
        
        sessions = []
        data_files = os.listdir(self.data_dir)
        
        if not data_files:
            print("❌ No session files found in neuralis_data/")
            return []
        
        for filename in data_files:
            if filename.startswith("session_") and filename.endswith(".json"):
                try:
                    with open(os.path.join(self.data_dir, filename), 'r') as f:
                        session_data = json.load(f)
                    sessions.append(session_data)
                    print(f"✅ Loaded: {filename}")
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
        
        return sessions
    
    def analyze_session(self, session):
        """Analyze a single typing session"""
        gaps = session.get('gaps_ms', [])
        
        if not gaps or len(gaps) < 2:
            print(f"⚠️  Not enough gaps data in session {session.get('session_id', 'unknown')}")
            return None
        
        try:
            # Convert to numpy array for calculations
            gaps_array = np.array(gaps, dtype=float)
            
            # Calculate statistics
            stats = {
                'session_id': session.get('session_id', 'unknown'),
                'total_keys': session.get('total_keys', 0),
                'total_time': session.get('total_time_ms', 0),
                'average_gap': float(np.mean(gaps_array)),
                'std_gap': float(np.std(gaps_array)),
                'min_gap': float(np.min(gaps_array)),
                'max_gap': float(np.max(gaps_array)),
                'human_score': self.calculate_human_score(gaps_array)
            }
            
            return stats
            
        except Exception as e:
            print(f"❌ Error analyzing session: {e}")
            return None
    
    def calculate_human_score(self, gaps_array):
        """Calculate how human-like the typing is (0-100)"""
        if len(gaps_array) < 5:
            return 0
        
        try:
            std = np.std(gaps_array)
            mean = np.mean(gaps_array)
            
            # Avoid division by zero
            if mean == 0:
                return 0
                
            # Coefficient of Variation (measure of consistency)
            cv = (std / mean) * 100
            
            # Scoring logic
            if cv < 10:
                return 20  # Too robotic
            elif cv > 60:
                return 40  # Too erratic
            elif 15 <= cv <= 50:
                return 85  # Very human-like
            else:
                return 60  # Neutral
                
        except Exception as e:
            print(f"❌ Error calculating human score: {e}")
            return 0
    
    def generate_report(self, sessions):
        """Generate analysis report"""
        print("\n📊 NEURALIS ANALYSIS REPORT")
        print("=" * 40)
        
        if not sessions:
            print("No data to analyze")
            return
        
        print(f"Sessions analyzed: {len(sessions)}")
        
        for session in sessions:
            stats = self.analyze_session(session)
            if stats:
                print(f"\n📈 Session: {stats['session_id']}")
                print(f"   Keys: {stats['total_keys']}")
                print(f"   Time: {stats['total_time']/1000:.1f}s")
                print(f"   Avg gap: {stats['average_gap']:.1f}ms")
                print(f"   Consistency: ±{stats['std_gap']:.1f}ms")
                print(f"   Human Score: {stats['human_score']}/100")
                
                if stats['human_score'] >= 70:
                    print("   ✅ LIKELY HUMAN")
                elif stats['human_score'] >= 40:
                    print("   ⚠️  UNCERTAIN")
                else:
                    print("   ❌ LIKELY ROBOTIC")
            else:
                print(f"\n⚠️  Could not analyze session: {session.get('session_id', 'unknown')}")
        
        print("\n" + "=" * 40)
        print("💡 INSIGHTS:")
        print("• Human typing has natural variability")
        print("• Bots are too consistent (low std deviation)")
        print("• Your pattern is unique like a fingerprint")
    
    def create_user_profile(self, sessions, username="founder"):
        """Create a user profile from sessions"""
        if not sessions:
            print("❌ No sessions to create profile")
            return None
        
        profile = {
            'username': username,
            'created': datetime.now().isoformat(),
            'sessions_analyzed': len(sessions),
            'average_stats': {},
            'human_scores': []
        }
        
        # Collect all stats
        all_stats = []
        for session in sessions:
            stats = self.analyze_session(session)
            if stats:
                all_stats.append(stats)
                profile['human_scores'].append(stats['human_score'])
        
        if not all_stats:
            print("❌ No valid session data for profile")
            return None
        
        # Calculate averages
        try:
            profile['average_stats'] = {
                'avg_gap': float(np.mean([s['average_gap'] for s in all_stats])),
                'avg_std': float(np.mean([s['std_gap'] for s in all_stats])),
                'avg_human_score': float(np.mean(profile['human_scores']))
            }
        except Exception as e:
            print(f"❌ Error calculating averages: {e}")
            return None
        
        # Save profile
        profile_file = os.path.join(self.profiles_dir, f"{username}_profile.json")
        try:
            with open(profile_file, 'w') as f:
                json.dump(profile, f, indent=2)
            print(f"💾 Profile saved: {profile_file}")
            return profile
        except Exception as e:
            print(f"❌ Error saving profile: {e}")
            return None

def main():
    """Main function"""
    engine = NeuralisEngine()
    
    print("Loading your neural signatures...")
    sessions = engine.load_sessions()
    
    if not sessions:
        print("❌ No sessions found. Run the sensor first!")
        print("Command: python neuralis_sensor_v1.py")
        return
    
    print(f"✅ Loaded {len(sessions)} session(s)")
    
    # Generate report
    engine.generate_report(sessions)
    
    # Create profile
    username = input("\nEnter your name for profile: ").strip() or "founder"
    profile = engine.create_user_profile(sessions, username)
    
    if profile:
        print(f"\n👤 PROFILE CREATED: {username}")
        print(f"   Average Human Score: {profile['average_stats']['avg_human_score']:.1f}/100")
        print(f"   Typical speed: {profile['average_stats']['avg_gap']:.1f}ms")
        print(f"   Sessions: {profile['sessions_analyzed']}")
    else:
        print("❌ Failed to create profile")
    
    print("\n" + "=" * 60)
    print("✅ NEURALIS ENGINE COMPLETE")

if __name__ == "__main__":
    main()