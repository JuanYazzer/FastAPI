import streamlit as st
import requests

from frontend_utils import create_transformed_url, get_header


def feed_page():
    st.title("🏠 Feed")

    response = requests.get("http://localhost:8000/feed", headers=get_header())
    if response.status_code == 200:
        posts = response.json().get("posts", [])

        if not posts:
            st.info("No posts yet! Be the first to share something.")
            return

        for post in posts:
            st.markdown("---")

            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{post.get('email', 'Unknown')}** • {post.get('created_at', '')[:10]}")
            with col2:
                if post.get("is_owner", False):
                    if st.button("🗑️", key=f"delete_{post.get('id')}", help="Delete post"):
                        response = requests.delete(f"http://localhost:8000/posts/{post.get('id')}", headers=get_header())
                        if response.status_code == 200:
                            st.success("Post deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete post!")

            caption = post.get("caption", "")
            if post.get("file_type") == "image":
                uniform_url = create_transformed_url(post.get("url", ""), "", caption)
                st.image(uniform_url, width=300)
            else:
                uniform_video_url = create_transformed_url(post.get("url", ""), "w-400,h-200,cm-pad_resize,bg-blurred")
                st.video(uniform_video_url, width=300)
                st.caption(caption)

            st.markdown("")
    else:
        st.error("Failed to load feed")
