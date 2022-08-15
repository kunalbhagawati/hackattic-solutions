# Learnings
- Node `http` doesn't do body parsing by default.
- Node reads the request as a stream in chunks.
- Body parsing libs use content negotiation. If you don't get the `Content-Type` header, it will simply interpret the body as `undefined`.
