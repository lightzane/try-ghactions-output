# Create Release

This is a fork of [actions/create-release](https://github.com/actions/create-release/) only basic

Demo example but this can be done on the **root directory** of your repository
so that the path will be shorter when being reference in `uses` of your workflow.

Example.

```
github.com/{owner}/{repo}/action.yml
-> uses: {owner}/{repo}

github.com/{owner}/{repo}/.github/actions/release/action.yml
-> uses: {owner}/{repo}/.github/actions/release
```
