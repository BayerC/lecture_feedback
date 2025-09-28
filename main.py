import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh


class CounterManager:
    """Manages button counters with thread-safe operations"""

    def __init__(self):
        self.counters = {
            "green": 0,
            "yellow": 0,
            "red": 0,
            "last_updated": datetime.now().isoformat(),
        }

    def increment(self, button_type):
        """Increment counter for a specific button type"""
        self.counters[button_type] += 1
        self.counters["last_updated"] = datetime.now().isoformat()
        return self.counters.copy()

    def reset(self):
        """Reset all counters to zero"""
        self.counters = {
            "green": 0,
            "yellow": 0,
            "red": 0,
            "last_updated": datetime.now().isoformat(),
        }
        return self.counters.copy()

    def get_counters(self):
        """Get current counter values"""
        return self.counters.copy()


@st.cache_resource
def get_counter_manager():
    """Get or create the shared counter manager instance"""
    return CounterManager()


def main():
    # Get the shared counter manager
    counter_manager = get_counter_manager()

    st_autorefresh(interval=2000, key="data_refresh")  # Faster refresh for better UX

    st.title("Colored Buttons Demo")
    st.write("Click any of the colored buttons below:")

    # Create three columns for the buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🟢 Green Button", key="green", help="This is a green button"):
            counters = counter_manager.increment("green")
            st.success(f"Green button clicked! Total clicks: {counters['green']}")

    with col2:
        if st.button("🟡 Yellow Button", key="yellow", help="This is a yellow button"):
            counters = counter_manager.increment("yellow")
            st.warning(f"Yellow button clicked! Total clicks: {counters['yellow']}")

    with col3:
        if st.button("🔴 Red Button", key="red", help="This is a red button"):
            counters = counter_manager.increment("red")
            st.error(f"Red button clicked! Total clicks: {counters['red']}")

    # Get current counters for display
    current_counters = counter_manager.get_counters()

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
        total_clicks = (
            current_counters["green"]
            + current_counters["yellow"]
            + current_counters["red"]
        )
        st.metric("📈 Total Clicks", total_clicks)

    # Reset button
    st.markdown("---")
    if st.button(
        "🔄 Reset All Counters",
        key="reset",
        help="Reset all button click counters to zero",
    ):
        counter_manager.reset()
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
