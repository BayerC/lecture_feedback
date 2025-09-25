import streamlit as st
import json
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Counter data file path
COUNTER_FILE = "button_counts.json"

def load_counters():
    """Load counter data from JSON file"""
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Return default counters if file doesn't exist or is corrupted
    return {
        "green": 0,
        "yellow": 0,
        "red": 0,
        "last_updated": datetime.now().isoformat()
    }

def save_counters(counters):
    """Save counter data to JSON file"""
    counters["last_updated"] = datetime.now().isoformat()
    with open(COUNTER_FILE, 'w') as f:
        json.dump(counters, f, indent=2)

def increment_counter(button_type):
    """Increment counter for a specific button type"""
    counters = load_counters()
    counters[button_type] += 1
    save_counters(counters)
    return counters

def reset_counters():
    """Reset all counters to zero"""
    counters = {
        "green": 0,
        "yellow": 0,
        "red": 0,
        "last_updated": datetime.now().isoformat()
    }
    save_counters(counters)
    return counters

def main():
    st_autorefresh(interval=5000, key="data_refresh")

    st.title("Colored Buttons Demo")
    st.write("Click any of the colored buttons below:")
        
    # Create three columns for the buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Green Button", key="green", help="This is a green button"):
            counters = increment_counter("green")
            st.success(f"Green button clicked! Total clicks: {counters['green']}")
    
    with col2:
        if st.button("🟡 Yellow Button", key="yellow", help="This is a yellow button"):
            counters = increment_counter("yellow")
            st.warning(f"Yellow button clicked! Total clicks: {counters['yellow']}")
    
    with col3:
        if st.button("🔴 Red Button", key="red", help="This is a red button"):
            counters = increment_counter("red")
            st.error(f"Red button clicked! Total clicks: {counters['red']}")
    
    # Load current counters for display
    current_counters = load_counters()
    
    # Display counter statistics
    st.markdown("---")
    st.markdown("### 📊 Click Statistics")
    
    # Create columns for counter display
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("🟢 Green Clicks", current_counters["green"])
    
    with stat_col2:
        st.metric("🟡 Yellow Clicks", current_counters["yellow"])
    
    with stat_col3:
        st.metric("🔴 Red Clicks", current_counters["red"])
    
    with stat_col4:
        total_clicks = current_counters["green"] + current_counters["yellow"] + current_counters["red"]
        st.metric("📈 Total Clicks", total_clicks)
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Reset All Counters", key="reset", help="Reset all button click counters to zero"):
        reset_counters()
        st.success("All counters have been reset!")
        st.rerun()
    
    # Add some styling information
    st.markdown("---")
    st.markdown("### Button Colors:")
    st.markdown("- 🟢 **Green**: Success actions")
    st.markdown("- 🟡 **Yellow**: Warning actions") 
    st.markdown("- 🔴 **Red**: Error/critical actions")
    
    # Show last updated time
    if "last_updated" in current_counters:
        last_updated = datetime.fromisoformat(current_counters["last_updated"])
        st.markdown(f"*Last updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}*")
    
  

if __name__ == "__main__":
    main()
