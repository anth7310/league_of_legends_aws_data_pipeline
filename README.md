# league_of_legends_aws_data_pipeline

## Architecture
https://app.diagrams.net/#G1fJ1W6g2-mm60orAUfKXTEBc6P9ZiJROk

## Riot Games API
https://developer.riotgames.com/

## Get LOL match stats from riot API tutorial
https://codepull.com/api/getting-league-of-legends-matches-stats-from-the-riot-api/


# Branching
## Quick Legend

https://app.diagrams.net/#G1o0cAKuwAXq0weoErkaH908U7vLIxuaHk

<table>
  <thead>
    <tr>
      <th>Branch</th>
      <th>Description, Instructions, Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>main</td>
      <td>Main Branch. Accepts merges from Release Branch</td>
    </tr>
    <tr>
      <td>[tag]-release</td>
      <td>Release Branch. Accepts merges from Develop Branch. [tag] represents production release version.</td>
    </tr>
    <tr>
      <td>develop</td>
      <td>Development branch. Accepts merges from Feature branch</td>
    </tr>
    <tr>
      <td>feature-[id]</td>
      <td>Feature branch. ID uniquely identifies feature</td>
    </tr>
  </tbody>
</table>