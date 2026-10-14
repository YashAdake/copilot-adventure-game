SCENES = {
    "kickoff": {
        "text": "It's hackathon day. Your project runs, but the clock is already ticking.",
        "choices": [
            ("Triage the failing tests", "ci", -10, {"stable": True}),
            ("Build one last bonus feature", "feature", -20, {"stable": False, "feature": True}),
        ],
    },
    "ci": {
        "text": "CI is red because of a flaky test. The judges arrive soon.",
        "choices": [
            ("Fix the race condition properly", "scope", -15, {"stable": True}),
            ("Rerun CI and hope for green", "scope", -5, {"stable": False}),
        ],
    },
    "feature": {
        "text": "The bonus feature is half-integrated, and its tests haven't run.",
        "choices": [
            ("Cut it and stabilize the release", "scope", -10, {"stable": True, "feature": False}),
            ("Keep it and wire it in quickly", "scope", -15, {"stable": False, "feature": True}),
        ],
    },
    "scope": {
        "text": "The feature freeze is your last chance to protect the build.",
        "choices": [
            ("Freeze scope and check the release", "demo", -10, {"stable": True}),
            ("Squeeze in another enhancement", "demo", -20, {"stable": False}),
        ],
    },
    "demo": {
        "text": "Your app is ready for a judge-facing demo. Do you rehearse?",
        "choices": [
            ("Run through the demo once", "deploy", -10, {"rehearsed": True}),
            ("Skip rehearsal to save time", "deploy", 0, {"rehearsed": False}),
        ],
    },
    "deploy": {
        "text": "The submission portal is open. This is the moment.",
        "choices": [
            ("Ship the release build", "ship", 0, {}),
            ("Push the latest code without checking it", "lose", 0, {}),
        ],
    },
}


def ask_choice(prompt, options):
    """Return a valid 1-based choice, prompting again for invalid input."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer) - 1
        print(f"Please enter a number from 1 to {len(options)}.")


def play_game():
    state = {"minutes": 60, "stable": False, "feature": False, "rehearsed": False}
    scene_name = "kickoff"

    while scene_name in SCENES:
        scene = SCENES[scene_name]
        print(f"\n{scene['text']}\nTime left: {state['minutes']} minutes")
        for index, (description, _, _, _) in enumerate(scene["choices"], start=1):
            print(f"{index}. {description}")

        choice_index = ask_choice("Choose: ", scene["choices"])
        _, next_scene, time_cost, updates = scene["choices"][choice_index]
        state["minutes"] += time_cost
        state.update(updates)
        scene_name = next_scene

    if scene_name == "ship":
        won = state["minutes"] > 0 and state["stable"] and state["rehearsed"]
        scene_name = "win" if won else "lose"

    if scene_name == "win":
        print("\nThe release is stable, the demo lands, and you submit with time to spare. You shipped it!")
    else:
        print("\nThe deadline wins: the release wasn't ready, and the judges never see your best work.")


def main():
    while True:
        play_game()
        replay = input("\nPlay again? (y/n): ").strip().lower()
        while replay not in ("y", "n"):
            replay = input("Please enter y or n: ").strip().lower()
        if replay == "n":
            print("Good luck at the next hackathon!")
            break


if __name__ == "__main__":
    main()