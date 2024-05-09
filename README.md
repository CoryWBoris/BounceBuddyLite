i# BounceBuddyLite

![Stable Badge](https://img.shields.io/badge/-stable-blue)  
By: Cory Boris  
© 2024 MIT License
## A control surface based remote script for automatically and dynamically creating a blank midi clip starting and ending wherever a leftmost 'start' locator exists and a rightmost 'end' locator exists In Ableton Live 11+ WITHOUT PLUGINS ;)

# For Mac And Windows

## What it does:  
This control surface checks your arrangement view set for any locator named 'start' or 'end', and if there is at least one of each, then the control surface detects the left most 'start' locator and the right most 'end' locator, adds a new track at the top of your set named DefaultBounce, and creates a blank midi clip the same length as the timespan of the previously mentioned 'start' and end' locators, and with the clip inserted at the location in the timeline of the leftmost 'start' locator. This is done dynamically and in real time whether you:  
-move a start or end locator  
-delete an extra start or end locator  
-add or rename a new start or end locator  
-expand your arrangement inside your 'start' and 'end' span  
-delete a section of your arrangement inside your 'start' and 'end' span  

## 6 Steps to setup:  
**Note: this assumes you are using the default user library folder. If you have moved this folder externally or otherwise, make a Remote Scripts folder inside of whatever user library folder you have pointed Ableton to, and start from step 2:**
1. Mac users:  
   Go to `/Users/your_username/Music/Ableton/User Library`  
   Windows users:  
   Go to `\Users\your_username\Documents\Ableton\User Library`
2. Create a folder 'Remote Scripts' if it's not already created.
3. Create a folder titled ‘BounceBuddyLite’ inside the 'Remote Scripts' folder.
4. Download **both** .py files, “BounceBuddyLite.py" and "\_\_init\_\_.py", and place them in the 'Remote Scripts/BounceBuddyLite folder.
5. Restart or open Ableton Live
6. In Ableton, select ‘BounceBuddyLite in the "Link|Tempo|Midi" tab, and make sure the input and output are set to 'None'.

**Note**: You can add the 2 mentioned files from here to their respective folders as shown by my tutorial while Ableton is open or quit, but if Ableton is open, then you *will* have to restart Ableton for the selected control surface to go into effect. The reason being is that Ableton compiles python and loads python code into memory when Ableton starts, but not after it loads up. For you using the software, this means that in order to update this script if and when it is updated, then you will have to restart Ableton to use the updated software.  

## How to use (Assuming it is installed):
1. Make sure to set a 'start' and 'end' locator in your track, and make sure the 'start' locator comes before 'end'. I catch any out of bounds spans calculated here so nothing will happen if end is before start.
2. As soon as you make these locators, a new midi track named 'DefaultBounce' will appear with the blank midi clip starting from your 'start' locator and ending at your 'end' locator.
3. If you load a set with the locators already present in the set named 'start' or 'end, then the set will add the track named 'DefaultBounce' with its clip as soon as the set loads.  
4. These locators are dynamic and so as you drag them in real time, they remain glued to the start and end points of the blank midi clip which you create based on the newly dragged to location of your 'start' or 'end' locators.  

## Why tf did I make this?:  
This is my second iteration of my intention to make exporting easier within ableton with the method of making a blank and easily clickable midi clip spanning the duration of your set. Without my program, by default, if you want to export quickly, you can have the option of select all, which selects the lowest time of all clips, and the highest time of all clips, if there are no locators. If there are locators, then select all either selects the previously mentioned clip span, or the span between your earliest locator and your latest locator, whichever gets the lowest and highest value. This is very vague, and I’m sure you can see that unless you strictly define your set in terms of its clips by manually dragging and ensuring no clips exist outside of this, or define a leftmost and rightmost locator at the exact range of your midi clip span or greater, select all is almost useless for precision exporting.  

Furthermore, realistically, you may have some midi clips before your starting point. And you may have automation extending past your farthest midi clip which is necessary for an ending, a transition, some reverb, whatever. Consider how tedious it is to drag and highlight the exact spot you want to export every time, and so often locators are desirable for knowing what to highlight.  

But then, this leaves the issue of highlighting. Yes, you can just highlight, sure. But actually highlighting with many plugins and effects can often be a little laggy and this can present issues with trying to achieve a goal as simple as precise highlighting. The stakes are high - if you highlight your desired section in arrangement view and god forbid your hand accidentally slips on your mouse or trackpad, then you may have highlight all over again, or have the fail safe of pointing and clicking with shift.  

Or you can install BBL and forget about all your worries (with respect to selecting an exportable region of your ableton set that is). I offer a solution to always keep track of your exportable region provided that you add at least two locators to the set, one named ‘start’ and one named ‘end’. I think this is a convenient answer to those who would define the start and end pooints of their set anyway and would want to be able to click a blank midi clip and just select export in an easy two step workflow process.  
## Open Issues:  
I have not seen any errors so far when run by itself. The only thing which would potentially show an error would be when running with older versions of AutoClip. To avoid this error, I updated AutoClip to its latest version which ignores tracks named ‘DefaultBounce’. Also do not run at the same time as my other RemoteScript AutoBounceLength.py as it will cause a conflict since they are essentially the same program.

## Other Related Programs:
<a href="https://coryboris.gumroad.com/l/TrueAutoColor">TrueAutoColor</a>  
A stunning custom color layout maker for Ableton Live 11+ on Mac and Windows which instantly changes track and clip colors based on name, no plugins necessary.

### Coffees Welcome!
- [![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://github.com/sponsors/CoryWBoris)
- [![PayPal](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/coryboris)
- Venmo: @Cory-Boris
- Ethereum Address: `0x3f6af994201c17eF1E86ff057AB2a2F6CB0D1f6a`

And if this script means something to your workflow, consider showing your love with a star :) ⭐️
Thank you! 🔥🥰✌🏻🙏🏻

