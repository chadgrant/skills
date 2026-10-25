# Pstack attribution

Selected practices are adapted and condensed from [Lauren Tan's pstack](https://github.com/cursor/plugins/tree/99b609a72323b70204eab407c622f436e858e112/pstack) and informed by [Michael Denyer's Claude/Codex port](https://github.com/michael-denyer/pstack-claude/tree/356c6e0f978df729eb16f227d795f34d221c5aad). This is a selective integration, not a vendored copy or a claim of compatibility with all pstack workflows.

- `create-verification-skill` → verification lifecycle, project recipe, and evidence retention.
- `how` / `why` → bounded investigation and separation of evidence from inferred intent.
- `blast-radius` / `interrogate` → downstream review and evidence-based adjudication.
- `architect` → caller sketches and consequential design alternatives before contracts freeze.
- Type-system and idempotency principles → clean-code boundary and partial-failure guidance.
- Port host adapters → capability-aware Claude/Codex dispatch; tool details are checked against the active host.

The upstream MIT notices are retained below and in the two new skill folders so local installations carry attribution.

MIT License

Copyright (c) 2026 Lauren Tan
Copyright (c) 2026 Michael Denyer

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
