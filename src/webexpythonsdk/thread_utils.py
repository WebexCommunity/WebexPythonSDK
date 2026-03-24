"""Thread utility functions for Webex Python SDK.

This module provides utilities for working with threaded conversations in both
1:1 conversations and spaces, handling the different permission models and
API limitations.

Copyright (c) 2016-2024 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def collect_thread_text_and_attachments(
    api, msg, max_scan=500, max_chars=60000
):
    """Robustly collect thread text + attachments for both 1:1 and spaces.

    This function provides a robust way to collect thread messages that works
    for both 1:1 conversations and spaces, handling the different permission
    models and API limitations described in issue #256.

    Strategy:
      1) Use the new thread-aware API methods
      2) Handle both direct and group room types appropriately
      3) Provide fallback mechanisms when direct retrieval fails
      4) Always include replies ordered oldest->newest
      5) Ensure the incoming message 'msg' is present
      6) If starter can't be found, add a placeholder notice

    Args:
        api: WebexAPI instance with messages API
        msg: The message object to collect thread for
        max_scan (int): Maximum number of messages to scan when searching for parent
        max_chars (int): Maximum characters for text content before truncation

    Returns:
        tuple: (thread_text, [attachment_text]) where attachment_text is list with single big string
    """
    author_cache = {}
    thread_text_lines = []
    attachment_blocks = []

    def process_single_message(m):
        """Process a single message and extract text and attachments."""
        author = get_display_name(
            getattr(m, "personId", "unknown"), author_cache
        )
        mtext = (getattr(m, "text", "") or "").strip()
        if mtext:
            thread_text_lines.append(f"[{author}]: {mtext}")

        files = getattr(m, "files", None)
        if files and hasattr(files, "__iter__") and not isinstance(files, str):
            for f_url in files:
                try:
                    content, fname, ctype = download_webex_file(f_url)
                    extracted = extract_text_from_file(content, fname, ctype)
                    attachment_blocks.append(
                        f"[Attachment {fname}]:\n{extracted}"
                    )
                except Exception as e:
                    # keep going; record the error in attachments so user sees it
                    attachment_blocks.append(
                        f"[Attachment error for {fname}]: {e}"
                    )

    # Use the new thread-aware API method
    try:
        thread_context = api.messages.get_thread_context(msg, max_scan)
        thread_messages = thread_context["thread_messages"]
        root_message = thread_context["root_message"]
        error = thread_context["error"]

        # Add error notice if we couldn't retrieve the root message
        if error and not root_message:
            thread_text_lines.append(f"[Thread retrieval error]: {error}")
            thread_text_lines.append(
                "[Starter message unavailable — bot may have joined after the thread started or lacks permission to read the original message.]"
            )

    except Exception as e:
        # Fallback to processing just the single message
        thread_messages = [msg]
        root_message = None
        error = f"Failed to retrieve thread context: {str(e)}"
        thread_text_lines.append(f"[Thread retrieval error]: {error}")

    # Process all messages in the thread
    seen_ids = set()
    for m in thread_messages:
        mid = getattr(m, "id", None)
        if mid and mid in seen_ids:
            continue
        if mid:
            seen_ids.add(mid)
        process_single_message(m)

    # Combine and apply size limits
    thread_text = "\n".join(thread_text_lines)
    if len(thread_text) > max_chars:
        thread_text = thread_text[:max_chars] + "\n...[truncated]"

    att_text = "\n\n".join(attachment_blocks)
    if len(att_text) > max_chars:
        att_text = att_text[:max_chars] + "\n...[attachments truncated]"

    return thread_text, [att_text] if att_text else []


def get_display_name(person_id, author_cache):
    """Get display name for a person ID with caching.

    This is a placeholder function. In a real implementation, you would
    use the People API to get the display name.

    Args:
        person_id: The person ID to get display name for
        author_cache: Cache dictionary to store results

    Returns:
        str: Display name or person ID if not found
    """
    if person_id in author_cache:
        return author_cache[person_id]

    # Placeholder implementation - in real usage, call People API
    display_name = f"User-{person_id[:8]}"
    author_cache[person_id] = display_name
    return display_name


def download_webex_file(file_url):
    """Download a file from Webex.

    This is a placeholder function. In a real implementation, you would
    download the file from the provided URL.

    Args:
        file_url: URL of the file to download

    Returns:
        tuple: (content, filename, content_type)
    """
    # Placeholder implementation - in real usage, download the file
    return b"", "placeholder.txt", "text/plain"


def extract_text_from_file(content, filename, content_type):
    """Extract text content from a file.

    This is a placeholder function. In a real implementation, you would
    extract text based on the file type.

    Args:
        content: File content as bytes
        filename: Name of the file
        content_type: MIME type of the file

    Returns:
        str: Extracted text content
    """
    # Placeholder implementation - in real usage, extract text based on file type
    return f"Text content from {filename} (type: {content_type})"
