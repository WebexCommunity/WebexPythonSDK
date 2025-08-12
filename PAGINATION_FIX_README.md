# Pagination Fix for Webex Python SDK

## Overview

This fix addresses an issue with the `max` parameter in the `list_messages()` function and other list methods where the parameter wasn't being properly preserved across pagination requests.

## Problem Description

The original implementation had a flaw in the `_fix_next_url` function in `src/webexpythonsdk/restsession.py`. When handling pagination:

1. **Webex API behavior**: Webex returns "next" URLs in Link headers that may not include all original query parameters
2. **Parameter loss**: Critical parameters like `max`, `roomId`, `parentId`, etc. could be lost or modified during pagination
3. **Inconsistent results**: This led to unpredictable pagination behavior and inconsistent page sizes

## Solution Implemented

The fix improves the `_fix_next_url` function to:

1. **Always preserve critical parameters**: Parameters like `max`, `roomId`, `parentId`, `mentionedPeople`, `before`, and `beforeMessage` are always preserved with their original values
2. **Remove problematic parameters**: The `max=null` parameter (a known Webex API issue) is properly removed
3. **Smart parameter handling**: Non-critical parameters are preserved from the next URL if they exist, or added if they don't
4. **Consistent pagination**: Ensures the `max` parameter maintains consistent page sizes across all pagination requests

## Files Modified

- `src/webexpythonsdk/restsession.py` - Updated `_fix_next_url` function

## Testing

### Option 1: Run the Simple Test Runner

```bash
python test_pagination_fix_runner.py
```

This script tests the fix without requiring pytest and provides clear output about what's working.

### Option 2: Run with Pytest

```bash
# Install pytest if you don't have it
pip install pytest

# Run the comprehensive test suite
pytest tests/test_pagination_fix.py -v
```

### Option 3: Test the Fix Manually

You can test the fix manually by examining how the `_fix_next_url` function behaves:

```python
from webexpythonsdk.restsession import _fix_next_url

# Test case 1: Remove max=null and preserve original max
next_url = "https://webexapis.com/v1/messages?max=null&roomId=123"
params = {"max": 10, "roomId": "123"}
fixed_url = _fix_next_url(next_url, params)
print(f"Fixed URL: {fixed_url}")

# Test case 2: Preserve critical parameters
next_url = "https://webexapis.com/v1/messages?max=5&roomId=456"
params = {"max": 10, "roomId": "123", "parentId": "parent123"}
fixed_url = _fix_next_url(next_url, params)
print(f"Fixed URL: {fixed_url}")
```

## What the Fix Ensures

1. **Consistent Page Sizes**: The `max` parameter will always be applied consistently across all pagination requests
2. **Parameter Preservation**: Critical parameters are never lost during pagination
3. **Backward Compatibility**: Non-critical parameters are handled the same way as before
4. **Robust Pagination**: The pagination behavior is now predictable and reliable

## Impact on Existing Code

This fix is **backward compatible** and doesn't change the public API. It only improves the internal pagination logic to ensure that:

- `list_messages(roomId="123", max=10)` will consistently return pages of 10 messages
- `list_rooms(max=5)` will consistently return pages of 5 rooms
- All other list methods will maintain consistent page sizes

## Verification

After applying the fix, you should see:

1. **Consistent page sizes**: Each page returns the expected number of items (up to the max limit)
2. **Proper parameter preservation**: All specified parameters are maintained across pagination
3. **No more max=null issues**: The problematic `max=null` parameter is properly handled
4. **Predictable behavior**: Pagination works the same way every time

## Example Before/After

### Before (Problematic):
```
Page 1: 10 messages (max=10)
Page 2: 50 messages (max=null - default behavior)
Page 3: 50 messages (max=null - default behavior)
```

### After (Fixed):
```
Page 1: 10 messages (max=10)
Page 2: 10 messages (max=10)
Page 3: 10 messages (max=10)
```

## Support

If you encounter any issues with this fix or have questions about the implementation, please:

1. Run the test suite to verify the fix is working
2. Check that your pagination calls are now returning consistent results
3. Ensure that the `max` parameter is being respected across all pages

The fix addresses the root cause of the pagination issue and should resolve the problem where the `max` parameter wasn't being implemented correctly in the `list_messages()` function.
