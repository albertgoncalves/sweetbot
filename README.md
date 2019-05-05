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
$ nix-shell
[nix-shell:path/to/sweetbot]$ ./test
[nix-shell:path/to/sweetbot]$ ./main
```
`main` will basically just kickstart `src/main.py`, though it will bring the needed env variables along for the ride. This will get you across the finish line as well.
```
$ nix-shell
[nix-shell:path/to/sweetbot]$ env $(cat .env | xargs) python src/main.py
```

---
With `src/main.py` running, the bot can be interacted with in `Slack` by calling its name:
```slack
@sweetbot options
```
The terminal running the bot will print out some API request information as users interact with the bot. At the moment, unless the host crashes, the bot will run until the host cuts the cord with <kbd>ctrl + c</kbd>.

---
`python`, `pytest`, and `mypy` will all generate their own cache directories; it can get a little messy. If you'd like to submit these directories to the purge:
```
$ ./clean
```
