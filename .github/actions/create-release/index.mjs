// @ts-check
import core from '@actions/core'
import github from '@actions/github'

async function run() {
  try {
    // This should be a token with access to your repository scoped in as a secret.
    // The YML workflow will need to set token with the GitHub Secret GH_TOKEN
    // token: ${{ secrets.GH_TOKEN }}
    // https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_GH_TOKEN#about-the-github_GH_TOKEN-secret
    const token = core.getInput('token', { required: true })

    // Get actor and repo from context of payload that triggered the action
    const { owner, repo } = github.context.repo

    // Get the tag_name input from workflow file
    const tagName = core.getInput('tag-name', { required: true })

    // This removes the 'refs/tags' portion of the string, i.e. from 'refs/tags/v1.10.15' to 'v1.10.15'
    const tag = tagName.replace('refs/tags/', '')

    // Get authenticated GitHub client (Ocktokit): https://github.com/actions/toolkit/tree/main/packages/github#usage
    const octokit = github.getOctokit(token)

    // Create a release
    // https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#create-a-release
    await octokit.request('POST /repos/{owner}/{repo}/releases', {
      headers: {
        'X-GitHub-Api-Version': '2022-11-28',
      },
      owner,
      repo,
      tag_name: tag,
      // target_commitish: 'main',
      // name: 'v1.0.0',
      // draft: false,
      // prerelease: false,
    })
  } catch (error) {
    // https://github.com/actions/toolkit/tree/main/packages/core#exit-codes
    core.setFailed(`Action failed with error ${error}`)
  }
}

run()
