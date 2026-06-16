# HTTP Method Reference

This reference explains the common purpose of each HTTP request method used in REST APIs.

## GET
- Retrieves data from a server.
- Should be safe and idempotent: it does not change server state and can be repeated without side effects.
- Common use: fetch a list of resources or a single resource.

## POST
- Sends new data to the server to create a resource or trigger an action.
- Not idempotent: multiple identical POST requests can create multiple resources.
- Common use: create a new record, submit a form, or start a process.

## PUT
- Updates an existing resource or creates it if it does not exist.
- Idempotent: repeating the same PUT request should have the same result.
- Common use: replace a resource with the provided data.

## PATCH
- Applies a partial update to an existing resource.
- Not necessarily idempotent, but often implemented so repeated requests have the same effect.
- Common use: update one or more fields of a resource without replacing the entire object.

## DELETE
- Removes a resource from the server.
- Idempotent: deleting a resource multiple times typically has the same result (resource is gone).
- Common use: remove a resource by identifier.
