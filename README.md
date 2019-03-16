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
