# Endpoint to Use

## 1. Get user task lists

Let user choose which task list to use and get its ID

`GET https://tasks.googleapis.com/tasks/v1/users/@me/lists`

https://developers.google.com/tasks/reference/rest/v1/tasklists/list

## 2. Get user tasks in chosen task list

`GET https://tasks.googleapis.com/tasks/v1/lists/{tasklist}/tasks`

https://developers.google.com/tasks/reference/rest/v1/tasks/list

Query parameters:
* showCompleted = false
