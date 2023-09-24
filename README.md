# CS-449-Project-1

## Getting Started

### Prerequisites

Before you begin, make sure you have completed the setup steps provided by Prof. Avery [here](https://sites.google.com/view/cpsc-449). You can stop following his setup instructions after the FastAPI installation step.

Also, ensure that you have completed the setup steps from Exercise 1.

### Installation

1. Clone this repository:

    ```
    git clone https://github.com/jorgeemejia/CS-449-Project-1.git
    ```

2. Populate the Database

    If you are using Windows, you can use PowerShell scripts located in the `scripts/populate` directory to populate the database. For example, to populate the entire database, run:

    ```
    ./titanonline_clone.ps1
    ```

    To populate a specific table, run:

    ```
    ./instructors.ps1
    ```

    If you are using Linux/MacOS, please find and add the equivalent scripts to the `scripts` folder so that others can use them.

3. Start Foreman

    Run the following command to start the application with Foreman:

    ```
    foreman start
    ```

## Workflow

When you are ready to start working on the project, follow these steps:

1. Create a new branch for your task:

    ```
    git branch task/fixing-something
    ```

2. Work on your changes on the branch.

3. Create a pull request and have another classmate approve it when you are confident in your work.
