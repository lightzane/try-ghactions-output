```yaml
name: Access Output URL

on:
  push:
    branches: [main]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  runs-on: ubuntu-latest
  deploy:
    environment:
      name: ${{ github.base_ref }}
      url: ${{ steps.generate_url.outputs.URL }}

    steps:
      - name: Generate and Outputs URL
        id: generate_url
        run: |
          echo "URL=https://lightzane.github.io/sky-events" >> $GITHUB_OUTPUT
```
