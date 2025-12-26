# import streamlit as st
# import sys
# import io
# from datetime import datetime

# # Add your source path
# sys.path.append("src")
# from analysis.iparse_vq import IParser

# # Page configuration
# st.set_page_config(
#     page_title="Constituency Parser",
#     page_icon="🌳",
#     layout="wide"
# )

# # Initialize session state for history
# if 'history' not in st.session_state:
#     st.session_state.history = []

# if 'parser' not in st.session_state:
#     with st.spinner("Loading parser model..."):
#         st.session_state.parser = IParser("en_label_gpt2_medium_cat256")

# # Title and description
# st.title("🌳 Constituency Parsing with Learned Incremental Representation for Parsing")
# st.markdown("Parse sentences into constituency trees using Incremental Representations")

# # Create two columns for layout with 3:7 ratio
# col1, col2 = st.columns([3, 7])

# with col1:
#     st.subheader("Input")
    
#     # Input text area
#     input_text = st.text_area(
#         "Enter a sentence to parse:",
#         height=100,
#         placeholder="e.g., I knocked the man off his horse."
#     )
    
#     # Parse button
#     if st.button("Parse Sentence", type="primary", use_container_width=True):
#         if input_text.strip():
#             try:
#                 with st.spinner("Parsing..."):
#                     # Parse the sentence
#                     tree, code = st.session_state.parser.parse_sentence(input_text)
                    
#                     # Capture pretty print output
#                     output = io.StringIO()
#                     tree.pretty_print(stream=output)
#                     tree_str = output.getvalue()
                    
#                     # Add to history
#                     st.session_state.history.insert(0, {
#                         'sentence': input_text,
#                         'tree': tree,
#                         'tree_str': tree_str,
#                         'code': code,
#                         'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     })
                    
#                     # Keep only last 20 entries
#                     if len(st.session_state.history) > 20:
#                         st.session_state.history = st.session_state.history[:20]
                    
#                     st.success("Parsing complete!")
                    
#             except Exception as e:
#                 st.error(f"Error during parsing: {str(e)}")
#         else:
#             st.warning("Please enter a sentence to parse.")
    
#     # History section
#     st.subheader("History")
    
#     if st.session_state.history:
#         # Clear history button
#         if st.button("Clear History", use_container_width=True):
#             st.session_state.history = []
#             st.rerun()
        
#         # Display history items
#         for idx, item in enumerate(st.session_state.history):
#             with st.expander(f"📝 {item['sentence'][:50]}... - {item['timestamp']}"):
#                 st.text(f"Full sentence: {item['sentence']}")
#                 if st.button(f"Load", key=f"load_{idx}"):
#                     # Load this item as current
#                     st.session_state.current_item = item
#                     st.rerun()
#     else:
#         st.info("No parsing history yet. Parse a sentence to get started!")

# with col2:
#     st.subheader("Output")
    
#     # Display current or selected result
#     display_item = None
    
#     if 'current_item' in st.session_state:
#         display_item = st.session_state.current_item
#         del st.session_state.current_item
#     elif st.session_state.history:
#         display_item = st.session_state.history[0]
    
#     if display_item:
#         # Show sentence
#         st.markdown("**Parsed Sentence:**")
#         st.info(display_item['sentence'])
        
#         # Show ASCII tree
#         st.markdown("**Constituency Tree (ASCII):**")
#         st.code(display_item['tree_str'], language=None)
        
#         # Show code information
#         with st.expander("View Code Information"):
#             st.write("Code:", display_item['code'])
#             st.write("Tree object type:", type(display_item['tree']))
        
#         # Download button for tree
#         st.download_button(
#             label="Download Tree",
#             data=display_item['tree_str'],
#             file_name=f"parse_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#             mime="text/plain"
#         )
#     else:
#         st.info("👈 Enter a sentence and click 'Parse Sentence' to see the constituency tree here.")

# # Footer
# st.markdown("---")
# st.markdown("Built with Streamlit | Using IParser for constituency parsing")
import streamlit as st
import sys
import io
import time

# Add your source path
sys.path.append("src")
from analysis.iparse_vq import IParser

# --- Page Configuration ---
st.set_page_config(
    page_title="Incremental Parser",
    page_icon="🌳",
    layout="wide"
)

# --- Session State Initialization ---
if 'parser' not in st.session_state:
    with st.spinner("Loading parser model..."):
        st.session_state.parser = IParser("en_label_gpt2_medium_cat256")

# State for storing parsed steps to avoid re-parsing during animation
if 'steps' not in st.session_state:
    st.session_state.steps = []
if 'current_step_idx' not in st.session_state:
    st.session_state.current_step_idx = 0
if 'animating' not in st.session_state:
    st.session_state.animating = False

# --- Title ---
st.title("🌳 Incremental Representation for Parsing")

# --- Two Column Layout (4:6 Ratio) ---
col_input, col_output = st.columns([4, 6], gap="large")
def on_slider_change():
    # This empty function ensures the slider state is committed 
    # before the rest of the script logic runs
    pass
with col_input:
    st.subheader("Input")
    
    input_text = st.text_area(
        "Enter a sentence to parse:",
        value="I knocked the man off his horse .",
        height=120,
        key="sentence_input"
    )
    
    # Trigger button
    if st.button("Generate & Play Process", type="primary", use_container_width=True):
        if input_text.strip():
            tokens = input_text.strip().split()
            generated_steps = []
            
            # Step 1: Parse all states first with a single spinner
            with st.spinner("Parsing tokens..."):
                for i in range(1, len(tokens) + 1):
                    partial_sent = " ".join(tokens[:i])
                    # Ensure we use the model to get the tree
                    tree, _ = st.session_state.parser.parse_sentence(partial_sent)
                    
                    out = io.StringIO()
                    tree.pretty_print(stream=out)
                    
                    generated_steps.append({
                        "token": tokens[i-1],
                        "tree_str": out.getvalue(),
                        "tokens": tokens,
                        "is_final": i == len(tokens)
                    })
            
            # Step 2: Save to session state and set animation flag
            st.session_state.steps = generated_steps
            st.session_state.animating = True
            st.session_state.current_step_idx = 0
        else:
            st.warning("Please enter text.")

# --- Fixed Slider (The Navigation Bar) ---
    if st.session_state.steps and not st.session_state.animating:
        st.divider()
        st.subheader("Navigation")
        # Removed the 'value=' parameter to let Streamlit's internal state handle the position
        # Added a key to maintain state persistence
        st.select_slider(
            "Review specific step:",
            options=range(len(st.session_state.steps)),
            key="current_step_idx", # Using the session_state key directly here
            format_func=lambda x: f"Step {x+1}: {st.session_state.steps[x]['token']}",
            on_change=on_slider_change
        )

with col_output:
    st.subheader("Tree Visualization")
    output_container = st.empty()

    # Case A: Handle Animation
    if st.session_state.animating:
        for idx in range(len(st.session_state.steps)):
            step = st.session_state.steps[idx]
            st.session_state.current_step_idx = idx
            
            with output_container.container():
                # Highlight logic
                token_html = "".join([
                    f"<b style='color:#FF4B4B; border-bottom: 2px solid #FF4B4B;'>{t}</b> " if i == idx 
                    else f"{t} " if i < idx 
                    else f"<span style='opacity:0.3'>{t}</span> " 
                    for i, t in enumerate(step['tokens'])
                ])
                st.markdown(token_html, unsafe_allow_html=True)
                st.code(step['tree_str'], language=None)
            
            time.sleep(0.8)
        
        # Stop the animation state and refresh to show the slider
        st.session_state.animating = False
        st.rerun()

    # Case B: Display Static Step (Manual or Post-Animation)
    elif st.session_state.steps:
        step = st.session_state.steps[st.session_state.current_step_idx]
        with output_container.container():
            token_html = "".join([
                f"<b style='color:#FF4B4B;'>{t}</b> " if i == st.session_state.current_step_idx 
                else f"{t} " if i < st.session_state.current_step_idx 
                else f"<span style='opacity:0.3'>{t}</span> " 
                for i, t in enumerate(step['tokens'])
            ])
            st.markdown(token_html, unsafe_allow_html=True)
            st.code(step['tree_str'], language=None)
            if step['is_final']:
                st.success("✨ Final Parse Tree Complete")
    else:
        st.info("Waiting for input...")

# --- Footer ---
st.markdown("---")
st.caption("Incremental Parser | Word-by-word Construction")