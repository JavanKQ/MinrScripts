"""Generates the repetitive Ocean Puzzle scripts: Room3_Altar/ (10), Room4_Instrument/ (10)
and Doors/ (5). Edit the templates here, then run: py tools/gen_room_scripts.py
WARNING: overwrites those files. Any hand edits (e.g. door corners) must be copied into
the templates/settings here first, or redone after regenerating."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LETTERS = "ABCDEFGHIJ"

TEAM_CHECK = """# --- Team check: drop teammates who are offline or on another team ---
@define String me = player.getUniqueId()
@define String stay = me
@define String leftNames = ""
@define Boolean dropped = false
@define Player p = player
@if team != ""
@for String id in team_members.split(",")
@if id != me
@var p = Player(id)
@if p == null
@var dropped = true
@if leftNames != ""
@var leftNames = leftNames + ", "
@fi
@var leftNames = leftNames + "a teammate"
@elseif team[p] != team || !p.isOnline()
@var dropped = true
@if leftNames != ""
@var leftNames = leftNames + ", "
@fi
@var leftNames = leftNames + p.getName()
@else
@var stay = stay + "," + id
@fi
@fi
@done
@if dropped
@if stay == me
@var team = ""
@var team_members = ""
@player &7&o[Note] You and {{leftNames}} are no longer on the same team. You are now playing solo.
@else
@define String newId = team + "~" + "{{system::currentTimeMillis() / 1000L}}"
@for String id in stay.split(",")
@var p = Player(id)
@if p != null
@var team[p] = newId
@var team_members[p] = stay
@var p.sendMessage("\u00a77\u00a7o[Note] {{leftNames}} is no longer on your team (went offline or joined another team).")
@fi
@done
@fi
@fi
@fi
# --- End team check ---
"""

ALTAR = """# ==============================================================
# OCEAN PUZZLE - ROOM 3 ALTAR SIGN @N@ of 10 (script 9 of 10)
# ==============================================================
# Script type : interact
# Bind to     : [FILL IN: x y z of altar head @N@ in Room 3]
#               This head must wear the SAME skin as Symbol @N@
#               (design letter @L@) in Rooms 2 and 4.
# Map/area    : [FILL IN: map name / room]
# Import      : /s i i <paste URL>, then click altar head @N@
#
# What it does:
#   Room 3's answer. Ten symbol heads sit on an altar inside
#   Room 3, one per symbol. Players click them in order of the
#   symbols' values (from the Room 3 grids), lowest first:
#   Symbols 7, 9, 4, 6, 10, 5, 1, 2, 8, 3.
#   Every click plays the same confirmation sound and shows a
#   count (n/10). Nothing says whether a click was right; the
#   order is only checked after the 10th click.
#   - More than 15 seconds between clicks: the offering is
#     cleared and the player is told to begin again.
#   - Clicking a head already used in this offering: cleared,
#     with a message, so the player can begin again.
#   - Wrong order: no hearts lost, the Oracle says it's wrong
#     (not where), and the altar waits 30 seconds per player.
#   - Right order: the player and their online teammates are
#     marked as having solved Room 3 (solved3), which lets the
#     Room 4 door open for them. Teammates who are offline or
#     on another team are dropped from the team first.
#   Left-clicking a head also counts as a click.
#
# Requires: puzzle1 namespace (see Submit script header),
#   including:
#   /variable define puzzle1 relative Boolean solved3 = false
#   /variable define puzzle1 relative String altar_seq = ""
#   /variable define puzzle1 relative Long altar_last_at = 0L
#   /variable define puzzle1 relative Long altar_ready_at = 0L
#
# Map coordinates used inside this script: none
#
# Related scripts: Altar signs 1-10 (identical except for the
#   symbol number on the line below), Doors (8), Reset (4),
#   Team Conduit (6). Design: Ocean_Puzzle_Room3_Grids.md
# ==============================================================
@using puzzle1
@define Int symbol = @N@
@define String order = "7,9,4,6,10,5,1,2,8,3"
@if solved3
@player &3Oracle: &bThe signs already rest in their true order... The way onward knows you.
@return
@fi
@define Long now = system::currentTimeMillis()
@if altar_ready_at > now
@define Long seconds = (altar_ready_at - now + 999L) / 1000L
@player &3Oracle: &bThe altar still trembles from your last offering... Wait {{seconds}} seconds.
@return
@fi
# --- Too slow since the last click: start over ---
@if altar_seq != "" && now - altar_last_at > 15000L
@var altar_seq = ""
@player &3Oracle: &bThe signs have forgotten your unfinished offering... It begins anew.
@fi
# --- Same head twice: start over ---
@define Boolean repeat = false
@if altar_seq != ""
@for String s in altar_seq.split(",")
@if s == String(symbol)
@var repeat = true
@fi
@done
@fi
@if repeat
@var altar_seq = ""
@player &3Oracle: &bEach sign may be offered but once... Your offering is undone. Begin again.
@return
@fi
@if altar_seq == ""
@var altar_seq = String(symbol)
@else
@var altar_seq = altar_seq + "," + String(symbol)
@fi
@var altar_last_at = now
@define Int count = altar_seq.split(",").length()
@bypass /playsound minecraft:block.amethyst_block.chime record {{player.getName()}} ~ ~ ~ 1 1
@if count < 10
@player &f&oThe sign stirs beneath your touch. &7({{count}}/10)
# --- Wait 15s; if no newer click came, the offering lapses ---
@delay 15s
@if altar_seq != "" && altar_last_at == now
@var altar_seq = ""
@if player.isOnline()
@player &3Oracle: &bThe signs fall silent, your offering unfinished... Begin again.
@fi
@fi
@return
@fi
# --- 10th click: check the order ---
@define String offered = altar_seq
@var altar_seq = ""
@if offered != order
@var altar_ready_at = now + 30000L
@player &3Oracle: &bThe signs stir... and fall still. This is not their true order.
@return
@fi
@TEAM@@var solved3 = true
@player &3Oracle: &bThe signs settle into their true order... The way onward knows you now.
@if team == ""
@return
@fi
@for String id in stay.split(",")
@if id != me
@var p = Player(id)
@if p != null
@var solved3[p] = true
@var p.sendMessage("\u00a73Oracle: \u00a7b{{player.getName()}} has set the signs in their true order... the way onward knows you all.")
@fi
@fi
@done
"""

DOOR = """# ==============================================================
# OCEAN PUZZLE - DOOR: @TITLE@ (script 8 of 10)
# ==============================================================
# Script type : interact
# Bind to     : [FILL IN: x y z of the head @WHERE@]
# Map/area    : [FILL IN: map name / room]
# Import      : /s i i <paste URL>, then click the head
#
# What it does:
#   Opens @DOORNAME@ (fills it with air) for 5 seconds,
#   then seals it again. @WHO@
#   If someone clicks while it is already open, it stays open
#   until 5 seconds after the LAST click.
#
# Settings: the 5 door scripts are identical except for the
#   lines under "Settings for this copy" below. The Room 3 and
#   Room 4 doors each have an outside and an inside head that
#   both control the same door, so those pairs must use the same
#   door coordinates. The Room 4 exit has only one head (inside).
#
# Requires: puzzle1 namespace (see Submit script header),
#   including:
#   /variable define puzzle1 relative Boolean solved3 = false
#   /variable define puzzle1 relative Boolean solved4 = false
#   /variable define puzzle1 Long door3_close_at = 0L
#   /variable define puzzle1 Long door4_close_at = 0L
#   /variable define puzzle1 Long door5_close_at = 0L
#   (the door variables are NOT relative: shared by all)
#
# Map coordinates used inside this script:
#   @DOORNAME@: [FILL IN] (the "corners" setting below)
#
# Related scripts: the other Doors (8), Altar signs (9),
#   Instrument voices (10), Submit (1)
# ==============================================================
@using puzzle1
# --- Settings for this copy ---
# need: 0 = anyone, 1 = solved Room 1, 2 = solved Rooms 1 and 3,
#       3 = completed Room 4
@define Int need = @NEED@
# door: 3 = Room 3 door, 4 = Room 4 door, 5 = Room 4 exit
@define Int door = @D@
# corners: "x1 y1 z1 x2 y2 z2" of the door blocks
@define String corners = ""
# material: the block the door is made of
@define String material = "minecraft:prismarine_bricks"
# --- End settings ---
@if corners == ""
@player &7&o[Note] This door's coordinates haven't been set yet.
@return
@fi
@if need >= 1 && !solved
@player &3Oracle: &bThe seal does not yet know your song...
@return
@fi
@if need >= 2 && !solved3
@player &3Oracle: &bThe seal waits for the signs to be set in their true order...
@return
@fi
@if need >= 3 && !solved4
@player &3Oracle: &bThe way onward opens only for those whose song the instrument has sung...
@return
@fi
@define Long closeAt = system::currentTimeMillis() + 5000L
@if door == 3
@var door3_close_at = closeAt
@elseif door == 4
@var door4_close_at = closeAt
@else
@var door5_close_at = closeAt
@fi
@bypass /fill {{corners}} air
@bypass /playsound minecraft:block.conduit.activate record {{player.getName()}} ~ ~ ~ 1 1
@player &f&oThe seal parts before you... but not for long.
@delay 5s
@define Long last = door3_close_at
@if door == 4
@var last = door4_close_at
@elseif door == 5
@var last = door5_close_at
@fi
@if last <= closeAt
@bypass /fill {{corners}} {{material}}
@fi
"""

DOORS = [
    ("Room3_Outside", "3", "1", "outside the Room 3 entrance", "the Room 3 door", "Opens only for players who solved Room 1 (solved)."),
    ("Room3_Inside", "3", "0", "inside Room 3, next to its entrance", "the Room 3 door", "Opens for anyone, so nobody gets stuck inside."),
    ("Room4_Outside", "4", "2", "outside the Room 4 entrance", "the Room 4 door", "Opens only for players who solved Room 1 AND Room 3\n#   (solved and solved3)."),
    ("Room4_Inside", "4", "0", "inside Room 4, next to its entrance", "the Room 4 door", "Opens for anyone, so nobody gets stuck inside."),
    ("Room4_Exit", "5", "3", "inside Room 4, next to its exit", "the Room 4 exit", "Opens only for players who completed Room 4\n#   (solved4), on the way to the next checkpoint."),
]

ORDINALS = 'String["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th"]'

INSTRUMENT = """# ==============================================================
# OCEAN PUZZLE - ROOM 4 INSTRUMENT VOICE @N@ of 10 (script 10 of 10)
# ==============================================================
# Script type : interact
# Bind to     : [FILL IN: x y z of the Room 4 note block for Symbol @N@]
#               This note block must be marked with the SAME skin
#               as Symbol @N@ (design letter @L@) in Rooms 2 and 3,
#               and sit on PACKED ICE (chime) like Room 1's blocks.
#               Do NOT also bind Note Tune (5) to Room 4's blocks:
#               this script already shows the same tuning message.
# Map/area    : [FILL IN: map name / room]
# Import      : /s i i <paste URL>, then click the note block
#
# What it does:
#   The ancient instrument. Players tune each Room 4 note block
#   to its symbol's note (the note that symbol plays in Room 2),
#   then hit (left-click) the blocks in order of the symbols'
#   Room 3 values, lowest first:
#   Symbols 7, 9, 4, 6, 10, 5, 1, 2, 8, 3,
#   all within 15 seconds of the first note.
#   - Right-click (tuning): shows the new pitch, like Note Tune,
#     and cancels any melody in progress.
#   - Hitting the wrong block first does nothing, so players can
#     test sounds freely. Hitting a block out of order mid-melody
#     breaks it (hitting Symbol 7 starts a new melody at once).
#   - More than 15 seconds after the first note: the melody fades.
#   - All 10 in order and in time, but some blocks mistuned: the
#     Oracle says how many (never which). No hearts are lost.
#   - All 10 in order, in time and in tune: the player and their
#     online teammates complete Room 4 (solved4), and the team is
#     disbanded. The Room 4 exit head (Doors) then opens for them.
#   Only players who solved Rooms 1 and 3 can perform. For anyone
#   else, and after completing, these are plain note blocks.
#   "Breaks" and "fades" messages only appear once at least 2
#   notes were played in order, so testing one block stays quiet.
#   SETTING: the 15 second limit is the 15000L on two lines below.
#
# Requires: puzzle1 namespace (see Submit script header),
#   including:
#   /variable define puzzle1 relative Boolean solved4 = false
#   /variable define puzzle1 relative String inst_seq = ""
#   /variable define puzzle1 relative Long inst_started_at = 0L
#   /variable define puzzle1 relative Int inst_wrong = 0
#
# Map coordinates used inside this script: none
#
# Related scripts: Instrument voices 1-10 (identical except for
#   the symbol number below), Doors (8), Reset (4), Symbols (7),
#   Altar signs (9)
# ==============================================================
@using puzzle1
@define Int symbol = @N@
@define String order = "7,9,4,6,10,5,1,2,8,3"
@define String before = block.getBlockDataValue("note")
@delay 1
@define String after = block.getBlockDataValue("note")
# --- Right-click (tuning): show the pitch, cancel any melody ---
@if after != before
@define String[] ordinals = @ORDINALS@
@player &f&oThe note shifts to its {{ordinals[Int(after)]}} position.
@var inst_seq = ""
@return
@fi
# --- A hit: only counts for players who reached Room 4 ---
@if solved4 || !solved || !solved3 || answer == ""
@return
@fi
@define Long now = system::currentTimeMillis()
@define Int played = 0
@if inst_seq != ""
@var played = inst_seq.split(",").length()
@fi
@if played > 0 && now - inst_started_at > 15000L
@var inst_seq = ""
@var played = 0
@fi
@define String[] steps = order.split(",")
@if steps[played] != String(symbol)
@if played >= 2
@player &3Oracle: &bThe melody breaks... the voices strayed from their procession.
@fi
@var inst_seq = ""
@var played = 0
@if steps[0] != String(symbol)
@return
@fi
@fi
@if played == 0
@var inst_started_at = now
@var inst_wrong = 0
@fi
@define String[] notes = answer.split(",")
@if after != notes[symbol - 1]
@var inst_wrong = inst_wrong + 1
@fi
@if played == 0
@var inst_seq = String(symbol)
@else
@var inst_seq = inst_seq + "," + String(symbol)
@fi
@var played = played + 1
@if played < 10
# --- The first note starts a 15s timer; if the melody isn't done, it fades ---
@if played == 1
@delay 15s
@if inst_seq != "" && inst_started_at == now
@define Int reached = inst_seq.split(",").length()
@var inst_seq = ""
@if reached >= 2 && player.isOnline()
@player &3Oracle: &bThe melody fades beneath the tide... too slow, seeker.
@fi
@fi
@fi
@return
@fi
# --- 10th note, in order and in time: check the tuning ---
@var inst_seq = ""
@if inst_wrong > 0
@if inst_wrong == 1
@player &3Oracle: &bThe procession was true... yet one voice sang false.
@else
@player &3Oracle: &bThe procession was true... yet {{inst_wrong}} voices sang false.
@fi
@return
@fi
@TEAM@@var solved4 = true
@player &3Oracle: &bThe ancient instrument sings, and the deep sings with it... Your song is complete.
@player &3Oracle: &bThe way onward lies open to you.
@if team == ""
@return
@fi
# --- Room 4 complete: mark teammates and disband the team entirely ---
@for String id in stay.split(",")
@if id != me
@var p = Player(id)
@if p != null
@var solved4[p] = true
@var team[p] = ""
@var team_members[p] = ""
@var p.sendMessage("§3Oracle: §b{{player.getName()}} has awakened the ancient instrument... the deep sings for you all. The way onward lies open.")
@var p.sendMessage("§7§o[Note] The puzzle is complete, so your team has disbanded.")
@fi
@fi
@done
@var team = ""
@var team_members = ""
@player &7&o[Note] The puzzle is complete, so your team has disbanded.
"""

def write(folder, name, text):
    os.makedirs(os.path.join(ROOT, folder), exist_ok=True)
    with open(os.path.join(ROOT, folder, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

for n in range(1, 11):
    t = ALTAR.replace("@TEAM@", TEAM_CHECK).replace("@N@", str(n)).replace("@L@", LETTERS[n - 1])
    write("Room3_Altar", f"Ocean_Puzzle_Altar_{n:02d}.msc", t)
    t = (INSTRUMENT.replace("@TEAM@", TEAM_CHECK).replace("@ORDINALS@", ORDINALS)
         .replace("@N@", str(n)).replace("@L@", LETTERS[n - 1]))
    write("Room4_Instrument", f"Ocean_Puzzle_Instrument_{n:02d}.msc", t)
for name, d, need, where, doorname, who in DOORS:
    t = (DOOR.replace("@TITLE@", name.replace("_", " ").upper()).replace("@D@", d)
         .replace("@NEED@", need).replace("@WHERE@", where).replace("@DOORNAME@", doorname)
         .replace("@WHO@", who))
    write("Doors", f"Ocean_Puzzle_Door_{name}.msc", t)
print("done")
