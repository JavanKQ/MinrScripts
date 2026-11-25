"""Generates the repetitive Ocean Puzzle scripts: Room3_Altar/ (10), Room4_Instrument/ (10 + Start)
and Doors/ (4). Edit the templates here, then run: py tools/gen_room_scripts.py
(test server copies, in the repo root folders) and py tools/gen_room_scripts.py main
(main map copies, in MainMap/, using the MAIN settings near the end of the settings block).
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
# OCEAN PUZZLE - ROOM 3 ALTAR SIGN @N@ of 10 (script 9 of 12)
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


# ---------------- Settings ----------------
# Seconds from clicking the Start object to the 10th note.
INST_SECONDS = 15
# Seconds the parkour course stays up after a correct melody.
PARKOUR_SECONDS = 30
# Parkour course: single blocks, set to their block to show and air to hide.
# Each entry is "x y z" (uses PARKOUR_MATERIAL) or "x y z block" (its own block).
# Test server course (13 sea lanterns inside Room 4). The real course may be
# more detailed; if so, switch to /clone from a hidden copy.
PARKOUR_BLOCKS = [
    "-1824 75 1571", "-1826 76 1571", "-1829 77 1571", "-1832 78 1571",
    "-1835 79 1571", "-1838 80 1571", "-1838 81 1568", "-1838 82 1565",
    "-1838 83 1562", "-1838 84 1559", "-1836 85 1558", "-1833 86 1558",
    "-1830 87 1558",
]
PARKOUR_MATERIAL = "minecraft:sea_lantern"
# Seconds a player must wait between clicks on any door head.
DOOR_COOLDOWN = 5
# ---- MAIN MAP settings (py tools/gen_room_scripts.py main -> MainMap/) ----
# Empty values make the scripts say "coordinates haven't been set yet".
MAIN = {
    "INST_SECONDS": 15,
    "PARKOUR_SECONDS": 30,
    # Room 4 post-puzzle parkour, in jump order (2026-11-25).
    "PARKOUR_BLOCKS": [
        "11443 161 10994 minecraft:light_blue_stained_glass_pane",
        "11445 162 10994 minecraft:cyan_stained_glass_pane",
        "11446 163 10992 minecraft:blue_stained_glass_pane",
        "11447 164 10990 minecraft:cyan_stained_glass_pane",
        "11445 165 10988 minecraft:light_blue_stained_glass_pane",
        "11442 165 10988 minecraft:blue_stained_glass_pane",
        "11441 166 10990 minecraft:light_blue_stained_glass_pane",
        "11441 167 10992 minecraft:cyan_stained_glass_pane",
        "11443 168 10993 minecraft:blue_stained_glass_pane",
        "11445 169 10992 minecraft:light_blue_stained_glass_pane",
        "11445 170 10990 minecraft:cyan_stained_glass_pane",
    ],
    "PARKOUR_MATERIAL": "minecraft:sea_lantern",
    # Room 3 and 4 doors (2026-11-25): two regions each, separated by ;
    "DOOR_CORNERS": {"3": "11429 161 10990 11429 160 10991;11431 161 10991 11431 160 10990",
                     "4": "11457 162 10990 11457 160 10991;11454 162 10990 11454 160 10991"},
    "DOOR_MATERIAL": {"3": "minecraft:prismarine_wall", "4": "minecraft:prismarine_wall"},
    # Door head coordinates, by script name ("" = not known yet).
    "DOOR_HEADS": {"Room3_Outside": "11432 161 10989", "Room3_Inside": "",
                   "Room4_Outside": "11453 161 10992", "Room4_Inside": ""},
    "DOOR_COOLDOWN": 5,
}
# Doors: corners "x1 y1 z1 x2 y2 z2" and block, per door (3 = Room 3, 4 = Room 4).
# A door made of several regions lists each one, separated by ;
# Test server values; the real, more detailed doors will replace these.
DOOR_CORNERS = {"3": "-1846 77 1553 -1841 75 1553", "4": "-1839 76 1558 -1839 74 1560"}
DOOR_MATERIAL = {"3": "minecraft:sea_lantern", "4": "minecraft:sea_lantern"}
DOOR_HEADS = {}
# -------------------------------------------

DOOR = """# ==============================================================
# OCEAN PUZZLE - DOOR: @TITLE@ (script 8 of 12)
# ==============================================================
# Script type : interact
# Bind to     : @HEAD@
# Map/area    : [FILL IN: map name / room]
# Import      : /s i i <paste URL>, then click the head
#
# What it does:
#   Opens the Room @D@ door (fills it with air) for 5 seconds,
#   then seals it again. @WHO@
#   If someone clicks while it is already open, it stays open
#   until 5 seconds after the LAST click. Each player can click
#   a door head (any of them) only once every @DC@ seconds,
#   whether or not the door opens for them; extra clicks do
#   nothing.
#
# Settings: the 4 door scripts are identical except for the
#   lines under "Settings for this copy" below. Each door has an
#   outside head and an inside head that both control it, so
#   both Room @D@ copies must use the same door coordinates.
#
# Requires: puzzle1 namespace (see Submit script header),
#   including:
#   /variable define puzzle1 relative Boolean solved3 = false
#   /variable define puzzle1 relative Long door_ready_at = 0L
#   /variable define puzzle1 Long door3_close_at = 0L
#   /variable define puzzle1 Long door4_close_at = 0L
#   (the door variables are NOT relative: shared by all)
#
# Map coordinates used inside this script:
#   Room @D@ door: the "corners" setting below ([FILL IN] if empty)
#
# Related scripts: the other Doors (8), Altar signs (9),
#   Instrument (10), Submit (1)
# ==============================================================
@using puzzle1
# --- Settings for this copy ---
# need: 0 = anyone, 1 = solved Room 1, 2 = solved Rooms 1 and 3
@define Int need = @NEED@
# door: 3 = Room 3 door, 4 = Room 4 door
@define Int door = @D@
# corners: "x1 y1 z1 x2 y2 z2" of the door blocks (several
#   regions are separated by ;)
@define String corners = "@CORNERS@"
# material: the block the door is made of
@define String material = "@MATERIAL@"
# --- End settings ---
@if corners == ""
@player &7&o[Note] This door's coordinates haven't been set yet.
@return
@fi
# --- Per-player cooldown on all door heads (stops spam, allowed or not) ---
@define Long now = system::currentTimeMillis()
@if door_ready_at > now
@return
@fi
@var door_ready_at = now + @DCMS@L
@if need >= 1 && !solved
@player &3Oracle: &bThe seal does not yet know your song...
@return
@fi
@if need >= 2 && !solved3
@player &3Oracle: &bThe seal waits for the signs to be set in their true order...
@return
@fi
@define Long closeAt = now + 5000L
@if door == 3
@var door3_close_at = closeAt
@else
@var door4_close_at = closeAt
@fi
@for String c in corners.split(";")
@bypass /fill {{c}} air
@done
@bypass /playsound minecraft:block.conduit.activate record {{player.getName()}} ~ ~ ~ 1 1
@player &f&oThe seal parts before you... but not for long.
@delay 5s
@define Long last = door3_close_at
@if door == 4
@var last = door4_close_at
@fi
@if last <= closeAt
@for String c in corners.split(";")
@bypass /fill {{c}} {{material}}
@done
@fi
"""

DOORS = [
    ("Room3_Outside", "3", "1", "outside the Room 3 entrance", "Opens only for players who solved Room 1 (solved)."),
    ("Room3_Inside", "3", "0", "inside Room 3, next to its entrance", "Opens for anyone, so nobody gets stuck inside."),
    ("Room4_Outside", "4", "2", "outside the Room 4 entrance", "Opens only for players who solved Room 1 AND Room 3\n#   (solved and solved3)."),
    ("Room4_Inside", "4", "0", "inside Room 4, next to its entrance", "Opens for anyone, so nobody gets stuck inside."),
]

ORDINALS = 'String["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th"]'

START = """# ==============================================================
# OCEAN PUZZLE - ROOM 4 INSTRUMENT: START (script 10 of 12)
# ==============================================================
# Script type : interact
# Bind to     : [FILL IN: x y z of the Start object in Room 4
#               (a head, button or similar, near the instrument)]
# Map/area    : [FILL IN: map name / room]
# Import      : /s i i <paste URL>, then click the Start object
#
# What it does:
#   Starts a performance of the Room 4 melody. After clicking it,
#   the player has @SECS@ seconds to hit all 10 instrument note
#   blocks in order (see the Instrument voice scripts). Until it
#   is clicked, the note blocks are free to play and tune.
#   Clicking it again restarts the performance.
#   Only players who solved Rooms 1 and 3 can start it.
#
# Requires: puzzle1 namespace (see Submit script header),
#   including:
#   /variable define puzzle1 relative String inst_seq = ""
#   /variable define puzzle1 relative Long inst_started_at = 0L
#   /variable define puzzle1 relative Int inst_wrong = 0
#
# Map coordinates used inside this script: none
#
# Related scripts: Instrument voices 1-10 (10), Doors (8),
#   Finish (11)
# ==============================================================
@using puzzle1
@if !solved || !solved3 || answer == ""
@player &3Oracle: &bThe instrument does not yet know your song...
@return
@fi
@define Long now = system::currentTimeMillis()
@var inst_seq = ""
@var inst_wrong = 0
@var inst_started_at = now
@bypass /playsound minecraft:block.conduit.activate record {{player.getName()}} ~ ~ ~ 1 1
@player &f&oThe instrument awakens... its voices await your hand.
@delay @SECS@s
@if inst_started_at == now
@var inst_started_at = 0L
@var inst_seq = ""
@if player.isOnline()
@player &3Oracle: &bThe melody fades beneath the tide... too slow, seeker.
@fi
@fi
"""

INSTRUMENT = """# ==============================================================
# OCEAN PUZZLE - ROOM 4 INSTRUMENT VOICE @N@ of 10 (script 10 of 12)
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
#   click the Start object, then hit (left-click) the blocks in
#   order of the symbols' Room 3 values, lowest first:
#   Symbols 7, 9, 4, 6, 10, 5, 1, 2, 8, 3,
#   within @SECS@ seconds of clicking Start.
#   - Before Start is clicked, the blocks are free to play.
#   - Right-click (tuning) shows the new pitch, like Note Tune,
#     and breaks a performance in progress.
#   - A block hit out of order breaks the performance.
#   - Too slow: the Start script says the melody faded.
#   - All 10 in order and in time, but some blocks mistuned: the
#     Oracle says how many (never which). No hearts are lost.
#   - All 10 in order, in time and in tune: the parkour course
#     appears for @PSECS@ seconds, and the player and online
#     teammates are marked as having played it (solved4, which
#     Finish checks). Then the course disappears again.
#     Failing the parkour means playing the melody again.
#     Completing it leads to the Finish script (11), which
#     clears all progress and the team.
#   Only players who solved Rooms 1 and 3 can perform.
#
# Settings: the parkour blocks are the lines under "Settings"
#   below (identical in all 10 files).
#
# Requires: puzzle1 namespace (see Submit script header),
#   including:
#   /variable define puzzle1 relative String inst_seq = ""
#   /variable define puzzle1 relative Long inst_started_at = 0L
#   /variable define puzzle1 relative Int inst_wrong = 0
#   /variable define puzzle1 relative Boolean solved4 = false
#   /variable define puzzle1 Long parkour_close_at = 0L
#   (parkour_close_at is NOT relative: shared by all)
#
# Map coordinates used inside this script:
#   Parkour course: the "course" setting below
#
# Related scripts: Instrument voices 1-10 (identical except for
#   the symbol number below), Instrument Start (10), Finish (11),
#   Reset (4), Symbols (7), Altar signs (9)
# ==============================================================
@using puzzle1
@define Int symbol = @N@
@define String order = "7,9,4,6,10,5,1,2,8,3"
# --- Settings ---
# course: "x y z block" of each parkour block, separated by ;
@define String course = "@COURSE@"
# --- End settings ---
@define String before = block.getBlockDataValue("note")
@delay 1
@define String after = block.getBlockDataValue("note")
# --- Right-click (tuning): show the pitch; breaks a performance ---
@if after != before
@define String[] ordinals = @ORDINALS@
@player &f&oThe note shifts to its {{ordinals[Int(after)]}} position.
@if inst_started_at != 0L
@var inst_started_at = 0L
@var inst_seq = ""
@player &3Oracle: &bA voice shifts mid-song, and the melody breaks...
@fi
@return
@fi
# --- A hit: only counts during a performance ---
@if inst_started_at == 0L || !solved || !solved3 || answer == ""
@return
@fi
@define Long now = system::currentTimeMillis()
@if now - inst_started_at > @MS@L
@var inst_started_at = 0L
@var inst_seq = ""
@return
@fi
@define Int played = 0
@if inst_seq != ""
@var played = inst_seq.split(",").length()
@fi
@define String[] steps = order.split(",")
@if steps[played] != String(symbol)
@var inst_started_at = 0L
@var inst_seq = ""
@player &3Oracle: &bThe melody breaks... the voices strayed from their procession.
@return
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
@if played + 1 < 10
@return
@fi
# --- 10th note, in order and in time: check the tuning ---
@var inst_started_at = 0L
@var inst_seq = ""
@if inst_wrong > 0
@if inst_wrong == 1
@player &3Oracle: &bThe procession was true... yet one voice sang false.
@else
@player &3Oracle: &bThe procession was true... yet {{inst_wrong}} voices sang false.
@fi
@return
@fi
@player &3Oracle: &bThe ancient instrument sings, and the deep sings with it...
@player &3Oracle: &bA path falls into being, like raindrops upon still water... Make haste, before it fades.
# --- Mark the melody as played (Finish checks this), for online teammates too ---
@var solved4 = true
@if team != ""
@define String me = player.getUniqueId()
@define Player p = player
@for String id in team_members.split(",")
@if id != me
@var p = Player(id)
@if p != null
@if team[p] == team && p.isOnline()
@var solved4[p] = true
@var p.sendMessage("§3Oracle: §b{{player.getName()}} has awakened the ancient instrument... a path falls into being like raindrops. Make haste!")
@fi
@fi
@fi
@done
@fi
# --- Raise the course; sink it @PSECS@s after the LAST correct melody ---
@define Long closeAt = now + @PMS@L
@if course == ""
@player &7&o[Note] The parkour course's coordinates haven't been set yet.
@return
@fi
@var parkour_close_at = closeAt
@for String c in course.split(";")
@bypass /setblock {{c}}
@done
@delay @PSECS@s
@if parkour_close_at <= closeAt
@define String[] xyz = course.split(";")
@for String c in course.split(";")
@var xyz = c.split(" ")
@bypass /setblock {{xyz[0]}} {{xyz[1]}} {{xyz[2]}} air
@done
@fi
"""

import sys
OUT = ROOT
if len(sys.argv) > 1 and sys.argv[1] == "main":
    OUT = os.path.join(ROOT, "MainMap")
    INST_SECONDS = MAIN["INST_SECONDS"]
    PARKOUR_SECONDS = MAIN["PARKOUR_SECONDS"]
    PARKOUR_BLOCKS = MAIN["PARKOUR_BLOCKS"]
    PARKOUR_MATERIAL = MAIN["PARKOUR_MATERIAL"]
    DOOR_CORNERS = MAIN["DOOR_CORNERS"]
    DOOR_MATERIAL = MAIN["DOOR_MATERIAL"]
    DOOR_COOLDOWN = MAIN["DOOR_COOLDOWN"]
    DOOR_HEADS = MAIN["DOOR_HEADS"]

def write(folder, name, text):
    os.makedirs(os.path.join(OUT, folder), exist_ok=True)
    with open(os.path.join(OUT, folder, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def fill_inst(t):
    return (t.replace("@ORDINALS@", ORDINALS).replace("@SECS@", str(INST_SECONDS))
            .replace("@MS@", str(INST_SECONDS * 1000)).replace("@PSECS@", str(PARKOUR_SECONDS))
            .replace("@PMS@", str(PARKOUR_SECONDS * 1000)).replace("@COURSE@", ";".join(
                b if len(b.split()) == 4 else b + " " + PARKOUR_MATERIAL for b in PARKOUR_BLOCKS)))

for n in range(1, 11):
    t = ALTAR.replace("@TEAM@", TEAM_CHECK).replace("@N@", str(n)).replace("@L@", LETTERS[n - 1])
    write("Room3_Altar", f"Ocean_Puzzle_Altar_{n:02d}.msc", t)
    t = fill_inst(INSTRUMENT).replace("@N@", str(n)).replace("@L@", LETTERS[n - 1])
    write("Room4_Instrument", f"Ocean_Puzzle_Instrument_{n:02d}.msc", t)
write("Room4_Instrument", "Ocean_Puzzle_Instrument_Start.msc", fill_inst(START))
for name, d, need, where, who in DOORS:
    t = (DOOR.replace("@TITLE@", name.replace("_", " ").upper()).replace("@D@", d)
         .replace("@HEAD@", f"{DOOR_HEADS[name]} (the head {where})" if DOOR_HEADS.get(name)
                  else f"[FILL IN: x y z of the head {where}]")
         .replace("@NEED@", need).replace("@WHERE@", where).replace("@WHO@", who)
         .replace("@CORNERS@", DOOR_CORNERS[d]).replace("@MATERIAL@", DOOR_MATERIAL[d])
         .replace("@DCMS@", str(DOOR_COOLDOWN * 1000)).replace("@DC@", str(DOOR_COOLDOWN)))
    write("Doors", f"Ocean_Puzzle_Door_{name}.msc", t)
print("done")
