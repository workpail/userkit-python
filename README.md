# Python UserKit

## Summary
A UserKit client library for Python.

## Installation

Clone or download the repository from github:
```
git clone git@github.com:workpail/userkit-python
```
Then copy or symlink the `userkit-python/userkit` sub-directory into
your project.

## Documentation

For full examples and docs checkout [UserKit documentation][userkit-docs].

## Example usage

```python
import userkit
uk = userkit.UserKit("<YOUR_APP_SECRET_KEY>")

# Create a user
user = uk.users.create_user(email="jane.smith@example.com",
                            password="secretpass")

# Fetch a user
user = uk.users.get_user("<USER_ID>")

# Update a user
user = uk.users.update_user("<USER_ID>", name="Jane Smith")

# Login a user
session = uk.users.login_user("jane.smith@example.com", "secretpass")

# Fetch a logged in user by their session-token
user = uk.users.get_current_user(session.token)
if user:
    print("User is logged in:")
    print(user)
else:
    print("No logged in user, invalid session token")
```

## Test

To run tests you need to create a test-app.

Set the `USERKIT_KEY` environment variable to your test app key, then
run python's unittest:
```
USERKIT_KEY=<YOUR_APP_SECRET_KEY> python -m unittest discover
```


[userkit-docs]: https://docs.userkit.io
