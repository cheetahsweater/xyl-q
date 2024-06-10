
# XyL-Q

Hello-Q! XyL-Q is a multiple utility Discord bot designed for general use in servers as well as more specific use for things me or my friends might need.

## Commands
(Note: *italicized* parameters are optional, regular parameters are mandatory)

As of right now, there are 13 commands, 12 of which can be used by all members of any server XyL-Q is in:
- ~~**/meme** *[top_text]* *[bottom_text]* *[image_link]* *[image_upload]* *[wiki]*  - This command generates a meme. If given top_text, bottom_text, or both, this will be the text on the bottom and bottom of the meme. If not, the text will be randomly chosen from a list of indexed messages in the server that the command is being used in. If given an image_link or image_upload, then that image will be the background of the meme. If not, then a random image will be chosen from one of the list of wikis available, unless a specific one is chosen by the user. ([Jan. 27, 2024](https://github.com/cheetahsweater/xyl-q/commit/38eefcdcae4c547d9b2a855148977a54e99d527b))~~ **Temporarily disabled for major updates**
- **/disable** [command] [channel] - Disables use of a certain command in a certain channel. This command is extremely out of date and should probably be updated or removed. ([Jan. 27, 2024](https://github.com/cheetahsweater/xyl-q/commit/ccb9d0640720c46fd9aa1e33f645e6c20e5f17cb))
- **/disable_cache** [channel] OR [user] - Disables message caching (for use in /meme command) for messages in the given channel or by the given user. ([Jan. 27, 2024](https://github.com/cheetahsweater/xyl-q/commit/ccb9d0640720c46fd9aa1e33f645e6c20e5f17cb))
- **/version** - This command outputs the current version XyL-Q is running on, as well as the changelog for the current version and any previous iterations of the current version as well. ([Jan. 27, 2024](https://github.com/cheetahsweater/xyl-q/commit/e3faa6a6938dd86cefaba38dabd1a5aa2de113fd))
- **/reputation** *[user]* - This command sends an embed with info on the desired user's reputation stats (amount of rep, who you've given the most to, and who you've received the most from). For more info on reputation, see below. ([Feb. 5, 2024](https://github.com/cheetahsweater/xyl-q/commit/300ed0a32c27121d91706d96716e5da1075ca884))
- **/love_character** [character] [source] *[user]* - **(Mudae utility)** Adds a character to your lovelist, or the given user's lovelist if one is provided. ([Mar. 4, 2024](https://github.com/cheetahsweater/xyl-q/commit/9758efb0dfafb512ba1c7fd29ff0c2a35ad846ec))
- **/love_source** [source] *[user]* - **(Mudae utility)** Adds a source to your lovelist, or the given user's lovelist if one is provided. ([Mar. 5, 2024](https://github.com/cheetahsweater/xyl-q/commit/84ba8c4ba29fc5e67ff3f526002855f0af2baf3c))
- **/care_bear** *[bear]* - This command sends an embed containing information on a random bear from Care Bears, or the first search result for whatever the user inputs in the "bear" parameter. ([April 10, 2024](https://github.com/cheetahsweater/xyl-q/commit/68e445665af878916c23e09f7b565648898128fc))
- **/cookie** *[game]* - This command sends an embed containing information on a random character from Cookie Run: OvenBreak, Kingdom, or Tower of Adventure. ([April 11, 2024](https://github.com/cheetahsweater/xyl-q/commit/caab487f8caa4015ba0948dd204a782bd394f5a1))
- **/refresh_vars** - This command refreshes all of the variables XyL-Q pulls from external files, just in case I've updated any of those files manually. This should only work if I'm the one using the command. ([April 12, 2024](https://github.com/cheetahsweater/xyl-q/commit/c0f576d6d1ee6ded90726f252fb0e2ac61a53a5f))
- **/view_lovelist** - This command outputs your lovelist or sourcelist split into pages of 15 characters per page. ([April 12, 2024](https://github.com/cheetahsweater/xyl-q/commit/cebb696ee90b8e0d2703c821efdc92b450991197))
- **/set_reminder** - This command allows you to set a reminder on any given date at any given time. ([May 10, 2024](https://github.com/cheetahsweater/xyl-q/commit/6067d8aa233f5d30e04d6c2cb4371b0fbfff23e0))
- **/bjd_embed** - Personal use command that fixes faulty embedding on some ball-jointed doll merchant websites, specifically acbjd.com and dolkbjd.com, with probably more on the way. ([May 22, 2024](https://github.com/cheetahsweater/xyl-q/commit/db2103c0a0403176880903fc033a60f786932943))
- **/urban_dictionary** - This command allows you to search for the definition of a word on Urban Dictionary. ([June 10, 2024](https://github.com/cheetahsweater/xyl-q/commit/4534d44e4fc9d6dbeeb324fd0ae98a4e83784bc8))

## Reputation
The reputation functionality of XyL-Q was inspired by the rep functionality in UB3R-B0T, a Discord bot that I respect very much but I disagreed with the way they implemented their rep function, so I made my own!

When a user sends a message that you appreciate and you want to give them a token of your appreciation, react with the medal emoji (🏅) and they will be given +1 reputation point! 

Now, you may be asking, what if I particularly despise a message somebody's sent, and I want to take away reputation from them? Well, you can do that too! Simply throw a tomato at them with the tomato emoji (🍅) and -1 reputation point will be taken away from them! Isn't democracy beautiful?!

## Roadmap
Here are some things I'm hoping to add soon!
- [ ]   A way for users to remove characters/sources from their lovelist
- [x]   A way for users to check their lovelist
- [ ]   Commands that allow configuration of reaction roles (Inspired by Carl-bot)
- [ ]   Commands that allow setup of a starboard feature with custom emojis
- [ ]   A command that searches Urban Dictionary for definitions
- [ ]   A more thorough version of fm-bot's affinity feature
- [ ]   A command to pet XyL-Q for his good work :)

Thank you for reading this! I'm glad I finally put it together!!! :3
