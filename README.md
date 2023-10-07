# THIS IS THE README FOR THE GITHUB REPO, PROJECT REPORT IS IN Project1Report.pdf

# CS-449-Project-1

## Getting Started

### Prerequisites
Ensure that you have completed the setup steps from Exercise 1.
Also, make sure you have completed the additional setup steps provided by Prof. Avery [here](https://sites.google.com/view/cpsc-449). You can stop following his setup instructions after the FastAPI installation step.

### Installation

1. Clone this repository:

    ```
    git clone https://github.com/jorgeemejia/CS-449-Project-1.git
    ```

2. Populate the Database

    If you are using Windows, you can use PowerShell scripts located in the `scripts/populate` directory to populate the database. For example, to populate the entire database, run:

    ```
    /scripts/populate/titanonline_clone.**ps1**
    ```

    To populate a specific table, run:

    ```
    /scripts/populate/instructors**.ps1**
    ```

    If you are using Linux/MacOS, you can use Bash scripts locaed in the `scripts/populate` directory. For example, to populate the entire database, run:

    ```
    /scripts/populate/titanonline_clone**.sh**
    ```

    To populate a specific table, run:

    ```
    /scripts/populate/instructors**.sh**
    ```

3. Start Foreman

    Run the following command to start the application with Foreman:

    ```
    foreman start
    ```

## Workflow

### Issue Management

- **Creating Issues:** Issues can be created by anyone and will be assigned to everyone. Ensure that issues are well-structured with clear titles and descriptions (if neccessary).

### Tackling Issues

- **Issue Selection:**  Team members are encouraged to choose issues that align with their skills and interests. That being said, prioritize issues based on importance and dependencies.

- **Starting Work:** Before you begin working on an issue, please inform the team to prevent duplication of effort and ensure efficient collaboration. Then, create a branch that clearly indicates the issue it aims to resolve. For example, if the issue title is "Add SQL script for foods table," your branch should be named something like "add/sql-script-for-foods."

### Pull Request Process

- **Pull Request Review:** If you're not fully confident in your code, seek a review from another project member (if you are, just merge it). Request reviews by mentioning team members in the PR comments or mentioning it in Discord.

- **Code Review:** Reviewers are expected to provide constructive feedback to improve code quality.

- **Merging Pull Requests:** After addressing review comments, and with the approval of at least one team member (unless you merged it yourself), you can merge your own pull request. Ensure that any conflicts are resolved before merging.

## Getting Lost

"Wait, what's a ___?" "How the do you ____?" Some of these things like branches, pull requests, merging, issues, and so on might be new and confusing, and that's perfectly fine! Don't hesitate to hop into our Discord and ask for help or clarification.
