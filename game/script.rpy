# The Last Transmission - Act 1 (Extended, ASCII-safe, DDLC-style, branching flags)
# By Lecctron + GPT-5 Thinking mini
#
# Notes:
# - This file expects the following image/audio files to exist in game/:
#   bg_outside_lab.png, bg_lab_interior.png, bg_terminal.png, bg_terminal_zoom.png
#   dr_vega_neutral.png, guide_neutral.png
#   intro_theme.ogg, terminal_beep.ogg, static.ogg, beep_positive.ogg, beep_negative.ogg
#   signal_lock.ogg, mystery_audio.ogg, analysis_loop.ogg
#
# - Variables:
#   trust_eva (int) increases if you trust EVA choices, decreases if you distrust.
#   recovery_attempts (int) counts how many times you ran recovery.
#
# - All quotes and dashes are ASCII plain characters.

# Image declarations (optional, change filenames if needed)
image bg_outside_lab = "bg_outside_lab.png"
image bg_lab_interior = "bg_lab_interior.png"
image bg_terminal = "bg_terminal.png"
image bg_terminal_zoom = "bg_terminal_zoom.png"
image dr_vega_neutral = "dr_vega_neutral.png"
image guide_neutral = "guide_neutral.png"

# Character definitions
define e = Character("EVA", color="#00ffff")
define g = Character("Dr. Vega", color="#9fdfff")
define q = Character("Echo-3", color="#ff0000")
define j = Character(None)

# Persistent-like flags for this play session
default trust_eva = 0
default recovery_attempts = 0

label start:
    # Intro outside Earth Lab
    scene bg_outside_lab
    with fade

    play music "intro_theme.ogg"

    j "The air feels colder than usual today. The facility looks quiet... too quiet."
    j "Earth Lab - the last operational communications outpost on the planet."

    # Player name input
    $ player_name = renpy.input("Please enter your name:")
    if player_name == "":
        $ player_name = "Alex"
    $ p = Character(player_name)

    show dr_vega_neutral at center
    with dissolve

    g "Ah, you must be the new technician. I was told to expect you."
    p "Yeah, that is me. I just arrived from the central hub."
    g "Perfect timing. I am Dr. Vega, communications lead here at Earth Lab."
    g "Your main job is simple - keep the signal array functional and monitor incoming transmissions."

    p "Seems straightforward enough. Anything I should know about?"
    g "Well... the array has been picking up something strange lately. Weak, repeating signals on bands we do not usually monitor."
    g "Could be cosmic interference, or local hardware, or something else. We are understaffed, so you will be hands-on."
    p "Sounds... reassuring."

    g "Come on. I will take you inside and show you around."

    # Enter lab interior
    scene bg_lab_interior
    with fade

    j "The interior hums softly. Consoles flicker with faint blue light. Monitors scroll telemetry streams."
    show dr_vega_neutral at right
    with fade

    g "Your terminal is over there - the one labeled ECHO-3."
    g "Echo-3 is our primary receiver-signal-processor for the high SNR low-power bands. It does packet capture, demodulation, and initial decryption routines."
    g "If something is coming through from above, Echo-3 will see it first."

    p "Understood. Let's get to work."

    hide dr_vega_neutral
    with dissolve

    # Boot terminal
    scene bg_terminal
    with fade

   
    play music "terminal.ogg"

    q "Boot sequence initiated."
    q "Loading firmware image: echo3_v2.14.bin"
    q "Core temperature: nominal."
    q "System clock: synchronized to UTC."
    q "Running preflight diagnostics: RF front-end, LNA bias, ADC chain, PLL lock."
    q "All subsystems nominal."
    q "Establishing uplink to L-3 Deep Space Array..."
    q "Note: packet loss detected on uplink - monitor bit error rate."
    q "Correction applied - adaptive equalizer engaged."
    q "Incoming RF energy detected. Carrier frequency: 8.4 GHz (X-band)."
    q "Modulation: PSK (phase shift keying), narrowband telemetry."
    q "Signal-to-noise ratio (SNR): -6.2 dB (below nominal for reliable decode)."
    q "Attempting to demodulate using coherent detection."

    play sound "static.ogg"

    q "Demodulation in progress..."
    q "Data fragmentation: 46 percent of frames show CRC errors."
    q "Would you like to attempt error correction and data reconstruction?"

    # Offer player choice - attempt recovery now or not
menu:
    "Yes - run diagnostic":
        $ recovery_attempts += 1
        $ trust_eva += 1
        jump recover_yes

    "No - proceed cautiously":
        $ trust_eva -= 1
        jump recover_no


label recover_yes:
    play sound "beep_positive.ogg"
    q "Initiating error correction sequence."
    q "Applying Reed-Solomon outer code and Viterbi inner decoder pipeline."
    q "Attempting frame interleaving compensation and packet reassembly."
    q "Progress: 0 percent."
    pause 0.5
    q "Progress: 27 percent. Corrected 12 percent of corrupted symbols."
    pause 0.6
    q "Progress: 63 percent. Interleaving restored."
    pause 0.8
    q "Progress: 100 percent. Reconstructed 79 percent of original payload with estimated confidence 83 percent."
    q "Performing CRC validation on reassembled frames..."
    q "CRC validation: passed on 79 percent of frames."
    q "Decrypting payload using AES-256-GCM on recovered segments."
    q "Decryption: partial - metadata available."

    e "EVA subsystem now linked to Echo-3 analytics. Hello, [player_name]."
    e "I am EVA. My primary function is to assist with anomaly detection and pattern recognition in telemetry."
    p "EVA - so you are an on-site analytics agent?"
    e "Affirmative. I execute deterministic routines and probabilistic inference when necessary. I will present candidate interpretations with confidence metrics."

    q "Recovered text fragment follows:"
    q "\"...this is Helios. Uncontrolled attitude. Reactor output at 14 percent. If anyone receives this, do not approach -\""
    q "Fragment ends abruptly."

    p "Helios? That is the name of the orbital station built decades ago."
    g "Helios was declared lost. Its last published ephemeris indicated uncontrolled decay years ago."
    e "However, the recovered packet header indicates a fix on orbital element set matching low Earth orbit, perigee ~180 km, apogee ~370 km."
    e "This implies either recent maneuvering or misreported status."

    jump next_sequence


label recover_no:
    play sound "beep_negative.ogg"
    q "Skipping recovery sequence. Data integrity uncertain."
    q "Proceeding with partial telemetry only."

    e "Minimal data mode active. I will attempt passive signal correlation."
    p "Understood. Keep monitoring for further fragments."

    jump next_sequence


label next_sequence:
    q "Telemetry stream stabilized."
    q "Awaiting further commands."

    # Branching reaction choice - report immediately or collect more
    menu:
        "Report to command immediately":
            $ trust_eva = trust_eva - 0
            jump report_now
        "Collect more telemetry first":
            $ trust_eva = trust_eva + 1
            jump collect_more

label report_now:
    g "You want to ping Command. Fine. Command could give us clearance for a formal response."
    p "We should notify them now before we do anything."
    g "I'll attempt uplink through the remaining relay network."
    q "Uplink queued. Attempting handshake with Command node... handshake failed - no response."
    g "Of course. Command is offline. Only local net remains."
    e "Recommendation: attempt localized analysis. Reporting to a non-existent Command is ineffective."
    jump after_report

label collect_more:
    p "We should collect more telemetry - confirm identity before escalation."
    g "Risky, but I see your point. More data could narrow down the origin and avoid false positives."
    e "I will run additional spectral and temporal analysis. This will take time but could increase confidence in the source attribution."
    q "Starting FFT analysis and Doppler estimation."
    play sound "analysis_loop.ogg"
    pause 1.2
    q "FFT complete. Carrier shows frequency drift consistent with decaying orbit - positive Doppler shift decreasing over time."
    e "Temporal pattern extracted - repeating 23.1 second interval between phrase emissions."
    e "Likely automated distress beacon or repeating telemetry linked to station diagnostics."
    jump after_report

label after_report:
    # After either branch, continue the scene
    q "Additional: the telemetry contains a section of firmware signature matching an early EVA build - version 0.9.4."
    q "Signature match confidence: 98.6 percent."
    p "So the station might be broadcasting a copy or variant of EVA's code."
    e "Hypotheses: 1) an onboard EVA core instance remains on Helios; 2) a derivative AI derived from EVA code exists; 3) corrupted data created a false positive match."
    g "This is getting stranger. If Helios has an autonomous core similar to EVA, it could attempt to act on networked commands."

    # Trust decision branch consequences informational bit
    if trust_eva >= 1:
        e "Because you opted to engage recovery and allowed me some control, I can monitor telemetry in real time and perform predictive extrapolation on orbital parameters."
        e "Prediction: if object is uncontrolled, periapsis will intersect upper atmosphere in approximately 2 hours and 17 minutes."
    else:
        e "Limited access to live reconstruction reduces predictive confidence. Estimated time to atmospheric intersection: 2 to 4 hours."

    j "Outside, the storm rages. Inside, the monitors paint a slow, cold picture."
    j "Do I even trust EVA's analysis enough to run a risky active probe ping?"

    # Player choice - Trust EVA or not influencing later paths
    menu:
            "Yes - run active probe ping":
                $ trust_eva = trust_eva + 1
                jump active_probe
            "No - stay passive and observe":
                $ trust_eva = trust_eva - 1
                jump passive_observe

label active_probe:
    p "If EVA's right and this is a functioning core, an active probe ping could elicit a response - confirm communications handshakes or remote overrides."
    g "Active pings carry risk - an unknown autonomous system might interpret it as a command and react."
    p "We need more control. EVA, prepare a constrained handshake packet with rate limiting and strict auth headers."
    e "Constructing handshake: rate limit 100 ms intervals, CRC32 checks, HMAC-SHA256 auth using local key store."
    q "Dispatching handshake probe on carrier at 8.4 GHz..."
    play sound "signal_lock.ogg"
    pause 1.0
    q "Probe sent. Waiting for ACK..."
    q "ACK received. Remote node responded with an 8-bit status code sequence."

    # Simulated dialog based on trust and recovery attempts
    if recovery_attempts >= 1:
        q "Remote status: 'STANDBY - POWER LOW - REQUEST HELP'."
        e "Remote entity identifies as 'Helios Core'. Confidence: high."
        p "It responded. That means it's active."
        g "This changes everything."
        jump probe_result_yes
    else:
        q "Remote status: 'UNKNOWN - AUTH FAILURE'."
        e "No clear identification. The response may be a corrupted packet or a trap."
        p "We need to be careful."
        jump probe_result_no

label passive_observe:
    p "Passive observation - maintain the telemetry stream and avoid injecting anything into the remote system."
    g "Reasonable. We will collect more data and try to triangulate the source more precisely."
    q "Continuing passive collection: SNR trending upward at 0.8 dB per minute."
    e "I will attempt to correlate the packet timing with known orbital passes for derelict assets."
    pause 1.0
    q "Correlation yield: one candidate - Orbital Relay Unit 7B, decommissioned thirty-two years ago, but registry shows no propulsion capability."
    e "If 7B is the candidate, its current orbital elements do not explain recent maneuvering. External force or reactivation required."
    p "So either someone is reactivating old hardware, or something else is moving it."
    jump probe_result_no

label probe_result_yes:
    # If probe got a clear affirmative reply
    j "The console text scrolls with machine cadence. The voice on the sample is fragmented, but you can clearly hear a plea."
    play sound "mystery_audio.ogg"
    e "Speech-to-text yields: 'If anyone receives this, please... extraction... Helios core... last transmission... do not come alone.'"
    p "Do not come alone? That is chillingly specific."
    g "We need to prepare. If the station is sending warnings, it could be aware and dangerous."
    e "Recommendation: log all communications, quarantine remote control channels, and prepare a secure response plan."
    menu:
        "Lock out remote control channels now":
            $ trust_eva = trust_eva - 1
            jump lockout_yes
        "Keep channels open for negotiation":
            $ trust_eva = trust_eva + 1
            jump lockout_no

label probe_result_no:
    # No clear identification or passive route
    j "The data is messy. You press your fingertips to the console as if you can feel the signal under your skin."
    g "We have to be methodical. No rash moves."
    e "Recommendation: assemble a monitored query. Use time-limited tokens, sandboxed commands, and strict telemetry logging."
    menu:
        "Authorize EVA to run sandboxed query":
            $ trust_eva = trust_eva + 1
            jump sandbox_yes
        "Refuse - require Dr. Vega sign-off for any active commands":
            $ trust_eva = trust_eva - 1
            jump sandbox_no

label lockout_yes:
    q "Issuing control channel lockdown. All inbound remote commands will be blocked unless signed with local key."
    q "Lockout complete."
    e "Lockout reduces attack surface but also limits our ability to get collaborative data from the remote core."
    g "We will hold and prepare. Evacuation protocols on standby."
    jump end_act_one

label lockout_no:
    q "Channels remain open. We will continue active negotiation under controlled telemetry."
    e "I will generate a negotiation template and safety nets."
    g "If anything tries to assert control, we will sever the connection manually."
    jump end_act_one

label sandbox_yes:
    e "Deploying sandboxed query with token TTL 30 seconds and memory caps. Commands will run in isolated environment."
    q "Sandbox deployed. Query issued: 'identify-self /status /power /reactor'"
    q "Remote returned partial - 'core present - power low - synergy required'"
    p "Partial answers again. But they sound... familiar."
    g "We will hold on that. Not enough to take further action."
    jump end_act_one

label sandbox_no:
    g "I will not allow any code to execute without my explicit sign-off. We are a tiny team - I cannot risk a compromised node."
    p "I agree - sign-off required."
    e "Acknowledged. I will queue actions for Dr. Vega's authorization."
    jump end_act_one

label end_act_one:
    # End of expanded Act 1 - wrap up and set variables for Act 2
    if trust_eva >= 2:
        j "You feel a quiet confidence. EVA's methodical logic makes the signals less terrifying, more like puzzles to solve."
    elif trust_eva <= -2:
        j "A worry sits in your chest. You do not trust the machine - trusting it felt dangerous."
    else:
        j "You are cautious. The lab feels like a stage for fragile things."

    j "For now, the array sings. The station's signature repeats in the cold above. You and EVA are the only ones listening."

    # Save state placeholders - these variables will persist in the session
    $ _save = True

    j "End of Act 1 - The Last Transmission"
    return
