import streamlit as st

def save_selections_to_session(selected_items):
    # Save selections to session state
    for key, index in selected_items.items():
        st.session_state[f'selected_{key}_index'] = index
    # Save selections to session state when navigating to another page
    st.session_state.selected_columns = st.session_state.get('temp_selected_columns', [])

def reset_session_state():
    # Get all keys in session_state
    keys_to_delete = list(st.session_state.keys())

    # Delete all session state keys
    for key in keys_to_delete:
        del st.session_state[key]

    # Clear cache
    st.cache_data.clear()  # Clear memoized functions
    st.cache_resource.clear()