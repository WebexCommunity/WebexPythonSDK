#!/usr/bin/env python3
"""Example demonstrating the new thread-aware message retrieval functionality.

This example shows how to use the new thread utilities to collect thread messages
in both 1:1 conversations and spaces, addressing the issues described in #256.

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

import os
import sys

# Add the src directory to the path so we can import webexpythonsdk
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import webexpythonsdk
from webexpythonsdk.thread_utils import collect_thread_text_and_attachments


def main():
    """Main example function."""
    # Initialize the Webex API
    # You'll need to set your access token as an environment variable
    access_token = os.getenv("WEBEX_ACCESS_TOKEN")
    if not access_token:
        print("Please set WEBEX_ACCESS_TOKEN environment variable")
        return

    api = webexpythonsdk.WebexAPI(access_token=access_token)

    print("Webex Thread-Aware Message Retrieval Example")
    print("=" * 50)

    # Example 1: Using the new thread-aware API methods directly
    print("\n1. Using thread-aware API methods:")
    print("-" * 30)

    # This would be a message object from a webhook or API call
    # For demonstration, we'll create a mock message
    class MockMessage:
        def __init__(self, message_id, parent_id, room_id, room_type, text):
            self.id = message_id
            self.parentId = parent_id
            self.roomId = room_id
            self.roomType = room_type
            self.text = text
            self.personId = "person123"
            self.created = "2024-01-01T10:00:00Z"

    # Example message from a space (group room)
    space_message = MockMessage(
        message_id="msg123",
        parent_id="parent456",
        room_id="room789",
        room_type="group",
        text="This is a reply in a space thread",
    )

    try:
        # Get thread context using the new API method
        thread_context = api.messages.get_thread_context(space_message)

        print(f"Room Type: {thread_context['room_type']}")
        print(f"Is Thread: {thread_context['is_thread']}")
        print(f"Reply Count: {thread_context['reply_count']}")
        print(f"Thread Messages: {len(thread_context['thread_messages'])}")

        if thread_context["error"]:
            print(f"Error: {thread_context['error']}")
        else:
            print("Thread retrieved successfully!")

    except Exception as e:
        print(f"Error retrieving thread context: {e}")

    # Example 2: Using the utility function (drop-in replacement)
    print("\n2. Using the utility function:")
    print("-" * 30)

    try:
        # This is the drop-in replacement for the user's original function
        thread_text, attachments = collect_thread_text_and_attachments(
            api, space_message
        )

        print(f"Thread Text Length: {len(thread_text)} characters")
        print(f"Attachments: {len(attachments)}")
        print(f"Thread Text Preview: {thread_text[:100]}...")

    except Exception as e:
        print(f"Error using utility function: {e}")

    # Example 3: Handling different room types
    print("\n3. Handling different room types:")
    print("-" * 30)

    # Direct room message
    direct_message = MockMessage(
        message_id="msg456",
        parent_id="parent789",
        room_id="room123",
        room_type="direct",
        text="This is a reply in a 1:1 conversation",
    )

    try:
        # Check room type
        is_direct = api.messages._is_direct_room(direct_message)
        is_group = api.messages._is_group_room(direct_message)

        print(f"Message is from direct room: {is_direct}")
        print(f"Message is from group room: {is_group}")

    except Exception as e:
        print(f"Error checking room type: {e}")

    print("\nExample completed!")
    print("\nTo use this in your bot:")
    print(
        "1. Replace your existing collect_thread_text_and_attachments function"
    )
    print(
        "2. Import: from webexpythonsdk.thread_utils import collect_thread_text_and_attachments"
    )
    print(
        "3. Call: thread_text, attachments = collect_thread_text_and_attachments(api, msg)"
    )


if __name__ == "__main__":
    main()
