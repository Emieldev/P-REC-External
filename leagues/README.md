# League & Tournament Ruleset Profiles

P-REC uses modular JSON profiles to support different competitive leagues and tournament rulesets.

## How to Add Your League (Pull Requests Welcome!)

If you run or represent a competitive TF2 league, tournament, cup, or pug group (e.g. AsiaFortress, Pure League, Respawn League, United Gaming, etc.):

1. Copy `leagues/template.json` to `leagues/<your_league_id>.json`.
2. Configure your league's specific settings:
   * **`id`**: Unique identifier (e.g. `"asiafortress"`). This is what players enter in `prec_league`.
   * **`name`**: Full display name of the league.
   * **`rules_url`**: Link to your official rules page covering POV demo requirements.
   * **`prefix`**: Default demo file prefix (e.g. `"af"`).
   * **`ds_enable`**: `0` for manual auto-trigger (recommended), or `3` if your servers run plugin query checks.
   * **`ds_autodelete`**: Always `0` to prevent demo deletion.
   * **`ds_screens`**: `1` to capture end-of-round status/scoreboard screenshots.
   * **`mandatory_status_screenshot`**: Set `true` if your league requires `status` screenshots with player SteamIDs (like ETF2L).
   * **`server_config_patterns`**: List of regex patterns matching your server's `.cfg` executions or config chat prints.
   * **`chat_triggers`**: Phrases printed by your match plugins when a game officially goes live.
3. Open a **Pull Request** on GitHub!
   Once merged, all players using P-REC worldwide will automatically have native compliance with your league!

