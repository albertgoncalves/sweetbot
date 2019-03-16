# sweetbot

Needed things
---
  * [Nix](https://nixos.org/nix/)
  * `.env` with Slack user and bot tokens:
    ```
    SLACK_USER_TOKEN="xoxp-..."
    SLACK_BOT_TOKEN="xoxb-..."
    ```

Quick start
---
```
$ bash main.sh
```
Which is really just wrapping the following commands together with some linting via `flake8`.
```
$ nix-shell
[nix-shell:~/sweetbot]$ pytest
[nix-shell:~/sweetbot]$ env $(cat .env | xargs) python src/main.py
```
`python` and `pytest` will both generate their own cache directories; it can get a little messy. If you'd like to submit these directories to the purge:
```
$ nix-shell
[nix-shell:~/sweetbot]$ bash clean.sh
```

With `src/main.py` running, the bot can be interacted with in `Slack` by calling its name:
```slack
@sweetbot options
```
The terminal running the bot will print out some API request information as users interact with the bot. At the moment, unless the host crashes, the bot will run until the host cuts the cord with <kbd>ctrl + c</kbd>.
