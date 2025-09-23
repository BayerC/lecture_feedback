import streamlit as st

def main():
    st.title("Colored Buttons Demo")
    st.write("Click any of the colored buttons below:")
    
    # Create three columns for the buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🟢 Green Button", key="green", help="This is a green button"):
            st.success("Green button clicked!")
    
    with col2:
        if st.button("🟡 Yellow Button", key="yellow", help="This is a yellow button"):
            st.warning("Yellow button clicked!")
    
    with col3:
        if st.button("🔴 Red Button", key="red", help="This is a red button"):
            st.error("Red button clicked!")
    
    # Add some styling information
    st.markdown("---")
    st.markdown("### Button Colors:")
    st.markdown("- 🟢 **Green**: Success actions")
    st.markdown("- 🟡 **Yellow**: Warning actions") 
    st.markdown("- 🔴 **Red**: Error/critical actions")

if __name__ == "__main__":
    main()
