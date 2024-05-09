from ableton.v2.control_surface import ControlSurface, ClipCreator
from functools import partial
from ableton.v2.base import liveobj_valid
import Live

class BounceBuddyLite(ControlSurface):
    def __init__(self, *a, **k):
        super(BounceBuddyLite, self).__init__(*a, **k)
        self.most_recent_cue = ''
        self.is_track_creation_scheduled = False
        self.cues_with_listeners = set()
        self.cue_points = set()
        self.start_cue_name = ''
        self.end_cue_name = ''
        self.prev_start_cue_name = ''
        self.prev_end_cue_name = ''
        self.start_cue = min((cue for cue in self.song.cue_points if cue.name.lower() == 'start'), key=lambda cue: cue.time, default=None)
        if self.start_cue:
            self.start_cue_name = self.start_cue.name.lower() + '_' + str(self.start_cue.time)
        self.end_cue = max((cue for cue in self.song.cue_points if cue.name.lower() == 'end'), key=lambda cue: cue.time, default=None)
        if self.end_cue:
            self.end_cue_name = self.end_cue.name.lower() + '_' + str(self.end_cue.time)
        self.song.add_cue_points_listener(self.on_cue_points_changed)  # Listen to changes in cue points
        self.song.add_cue_points_listener(self.on_cue_points_moved)
        for cue in self.song.cue_points:
            if cue not in self.cues_with_listeners:
                cue.add_time_listener(self.on_cue_points_moved)
                cue.add_name_listener(self.on_cue_name_changed)
                self.cues_with_listeners.add(cue)
        self.create_clip_from_cues()
        self.clip_slot_length = 0
        self.initial_cue_points = {f"{cue.name.lower()}_{cue.time}": cue.time for cue in self.song.cue_points}
        self.updated_cue_points = {f"{cue.name.lower()}_{cue.time}": cue.time for cue in self.song.cue_points}
    
    def on_cue_points_changed(self):
        self.prev_start_cue_name = self.start_cue_name
        self.prev_end_cue_name = self.end_cue_name
        self.start_cue = min((cue for cue in self.song.cue_points if cue.name.lower() == 'start'), key=lambda cue: cue.time, default=None)
        if self.start_cue:
            self.start_cue_name = self.start_cue.name.lower() + '_' + str(self.start_cue.time)
        self.end_cue = max((cue for cue in self.song.cue_points if cue.name.lower() == 'end'), key=lambda cue: cue.time, default=None)
        if self.end_cue:
            self.end_cue_name = self.end_cue.name.lower() + '_' + str(self.end_cue.time)
        print("Cue points changed")
        print("initial_cue_points: ", self.initial_cue_points)
        updated_cue_points = {f"{cue.name.lower()}_{cue.time}": cue.time for cue in self.song.cue_points}
        print("updated_cue_points: ", updated_cue_points)
        updated_cues = set(updated_cue_points.keys())
        initial_cues = set(self.initial_cue_points.keys())
        print("initial_cues: ", initial_cues)
        deleted_cues = None
        added_cues = None
        if len(updated_cues) < len(initial_cues):
            deleted_cues = initial_cues - updated_cues
        
        if len(updated_cues) > len(initial_cues):
            added_cues = updated_cues - initial_cues

        if deleted_cues is not None:
            print("we deleted a cue!!")
            print("deleted_cues: ", deleted_cues)
            # Find the actual cue objects that were deleted
            deleted_cue_names = {cue_name for cue_name in self.initial_cue_points if cue_name in deleted_cues}
            print("deleted_cue_names: ", deleted_cue_names)
            if deleted_cue_names:
                print("start or end cue deleted")
                for i in deleted_cue_names:
                    if 'start' in i.lower() or 'end' in i.lower():
                        print("we made it here after the if statement!")
                        self.on_cue_deletion(deleted_cue_names)

        if added_cues is not None:
            self.song.remove_cue_points_listener(self.on_cue_points_changed)
            self.song.add_cue_points_listener(self.on_cue_points_changed)

            for cue in self.song.cue_points:
                if liveobj_valid(cue) and cue not in self.cues_with_listeners:
                    cue.add_name_listener(self.on_cue_name_changed)  # Add name listener
                    cue.add_time_listener(self.on_cue_points_moved)  # Add time listener
                    self.cues_with_listeners.add(cue)
                    if 'start' in cue.name.lower() or 'end' in cue.name.lower():  # Only add the cue point if its name is 'start' or 'end'
                        self.cue_points.add(cue.name.lower())  # Add the new cue point name to self.cue_points
                        print("cue_points: ", self.cue_points)
            
        self.initial_cue_points = {f"{cue.name.lower()}_{cue.time}": cue.time for cue in self.song.cue_points}
        

    def on_cue_deletion(self, deleted_cue_names):
        for cue_name in deleted_cue_names:
            print(self.start_cue_name, self.end_cue_name)
            if cue_name == self.start_cue_name or cue_name == self.end_cue_name or cue_name == self.prev_start_cue_name or cue_name == self.prev_end_cue_name:
                print(f"{cue_name} cue deleted")
                # Execute the necessary logic for handling deletion of 'start' or 'end' cues in create clip from cues`
                self.schedule_message(0, partial(self.create_clip_from_cues, False))

    def adjust_clip_from_cues(self):
        self.start_cue = min((cue for cue in self.cue_points if cue.name.lower() == 'start'), key=lambda cue: cue.time, default=None)
        self.end_cue = max((cue for cue in self.cue_points if cue.name.lower() == 'end'), key=lambda cue: cue.time, default=None)
        if self.start_cue is None or self.end_cue is None or len(self.cue_points) < 2 or self.start_cue.time >= self.end_cue.time:
            print("Less than two clips or no presence of proper cues or invalid cue times")
            return
        self.clip_length = self.end_cue.time - self.start_cue.time
        self.schedule_message(0, self.defer_clip)

    def create_clip_from_cues(self, use_deferred=False):
        print(f"use_deferred: {use_deferred}")
        # Find 'start' and 'end' cue points first
        start_cue = next((cue for cue in self.song.cue_points if cue.name.lower() == 'start'), None)
        end_cue = next((cue for cue in self.song.cue_points if cue.name.lower() == 'end'), None)

        # If either 'start' or 'end' cue point is missing, return early
        if start_cue is None or end_cue is None:
            print("Missing 'start' or 'end' cue point. Skipping clip creation.")
            return
        track = next((t for t in self.song.tracks if t.name == 'DefaultBounce'), None)
        if liveobj_valid(track):
            self.cue_points = set(sorted(self.song.cue_points, key=lambda cue: cue.time))
            self.start_cue = min((cue for cue in self.cue_points if cue.name.lower() == 'start'), key=lambda cue: cue.time, default=None)
            self.end_cue = max((cue for cue in self.cue_points if cue.name.lower() == 'end'), key=lambda cue: cue.time, default=None)
            if self.start_cue is None or self.end_cue is None or len(self.cue_points) < 2 or self.start_cue.time >= self.end_cue.time:
                print("Less than two clips or no presence of proper cues or invalid cue times")
                return

            self.clip_length = self.end_cue.time - self.start_cue.time
            
            if liveobj_valid(track.clip_slots):
                first_clip_slot = track.clip_slots[0]
                if liveobj_valid(first_clip_slot) and first_clip_slot.has_clip and liveobj_valid(first_clip_slot.clip):
                    first_clip = first_clip_slot.clip
                    first_clip_length = first_clip.end_marker - first_clip.start_marker
                    if first_clip_length != self.clip_length:
                        if use_deferred is False:
                            first_clip_slot.delete_clip()
                        else:
                            self.schedule_message(0, first_clip_slot.delete_clip, ())

                for clip_slot in track.clip_slots[1:]:
                    if liveobj_valid(clip_slot) and clip_slot.has_clip and liveobj_valid(clip_slot.clip):
                        if use_deferred is False:
                            clip_slot.delete_clip()
                        else:
                            self.schedule_message(0, clip_slot.delete_clip, ())
            
            if liveobj_valid(track.arrangement_clips):
                for clip in track.arrangement_clips:
                    if liveobj_valid(clip):
                        clip_length = clip.end_marker - clip.start_marker
                        if clip_length != self.clip_length:
                            if use_deferred is False:
                                track.delete_clip(clip)
                            else:
                                self.schedule_message(0, partial(track.delete_clip, clip))
                    
            self.schedule_message(0, self.defer_clip)
        else:
            self.cue_points = set(sorted(self.song.cue_points, key=lambda cue: cue.time))
            self.start_cue = min((cue for cue in self.cue_points if cue.name.lower() == 'start'), key=lambda cue: cue.time, default=None)
            self.end_cue = max((cue for cue in self.cue_points if cue.name.lower() == 'end'), key=lambda cue: cue.time, default=None)

            if self.start_cue is None or self.end_cue is None or len(self.cue_points) < 2 or self.start_cue.time >= self.end_cue.time:
                print("Less than two clips or no presence of proper cues or invalid cue times")
                return
            if not self.is_track_creation_scheduled:
                self.is_track_creation_scheduled = True
                self.schedule_message(0, partial(self.song.create_midi_track, 0))
                self.schedule_message(0, self.rename_track)
            self.clip_length = self.end_cue.time - self.start_cue.time
            self.schedule_message(0, self.defer_clip)

    def defer_clip(self):
        track = next((t for t in self.song.tracks if t.name == 'DefaultBounce'), None)
        clip_slot = track.clip_slots[0]
        if clip_slot.has_clip:
            self.clip_slot_length = clip_slot.clip.end_marker - clip_slot.clip.start_marker

        clip = None
        if not clip_slot.has_clip:
            clip_slot.create_clip(self.clip_length)
        if clip_slot.has_clip:
            clip = clip_slot.clip
            if clip.length > 0:
                if 0 <= self.start_cue.time < clip.length:
                    clip.start_marker = self.start_cue.time
                else:
                    clip.start_marker = max(0, clip.length - .1)
                if 0 <= self.end_cue.time <= clip.length:
                    clip.end_marker = self.end_cue.time
                else:
                    clip.end_marker = clip.length
            else:
                clip.start_marker = 0
                clip.end_marker = 0

        if clip is not None:
            self.schedule_message(0, self._duplicate_clip_to_arrangement, (clip, self.start_cue.time))

    def rename_track(self):
        track = self.song.tracks[0]
        track.name = 'DefaultBounce'
        track.current_monitoring_state = 1
        self.is_track_creation_scheduled = False

    def _duplicate_clip_to_arrangement(self, params):
        clip, start_time = params
        if clip and clip.canonical_parent and clip.canonical_parent.canonical_parent:
            track = clip.canonical_parent.canonical_parent
            track.duplicate_clip_to_arrangement(clip, start_time)

    def on_cue_points_moved(self):
        self.song.remove_cue_points_listener(self.on_cue_points_moved)
        self.song.add_cue_points_listener(self.on_cue_points_moved)

        updated_cue_points = {}
        trigger_clip_creation = False

        for cue in self.song.cue_points:
            cue_id = f"{cue.name.lower()}_{cue.time}"

            if cue.name.lower() in ('start', 'end'):
                if cue_id not in self.initial_cue_points or self.initial_cue_points.get(cue_id) != cue.time:
                    trigger_clip_creation = True

        if trigger_clip_creation:
            self.schedule_message(0, self.create_clip_from_cues)
            
        self.initial_cue_points = {f"{cue.name.lower()}_{cue.time}": cue.time for cue in self.song.cue_points}
        # Update rightmost_end_cue_time and leftmost_start_cue_time
        self.start_cue = min((cue for cue in self.song.cue_points if cue.name.lower() == 'start'), key=lambda cue: cue.time, default=None)
        if self.start_cue:
            self.start_cue_name = self.start_cue.name.lower() + '_' + str(self.start_cue.time)
        self.end_cue = max((cue for cue in self.song.cue_points if cue.name.lower() == 'end'), key=lambda cue: cue.time, default=None)
        if self.end_cue:
            self.end_cue_name = self.end_cue.name.lower() + '_' + str(self.end_cue.time)

    def on_cue_name_changed(self):
        self.prev_start_cue_name = self.start_cue_name
        self.prev_end_cue_name = self.end_cue_name
        self.start_cue = min((cue for cue in self.song.cue_points if cue.name.lower() == 'start'), key=lambda cue: cue.time, default=None)
        if self.start_cue:
            self.start_cue_name = self.start_cue.name.lower() + '_' + str(self.start_cue.time)
        self.end_cue = max((cue for cue in self.song.cue_points if cue.name.lower() == 'end'), key=lambda cue: cue.time, default=None)
        if self.end_cue:
            self.end_cue_name = self.end_cue.name.lower() + '_' + str(self.end_cue.time)
        self.updated_cue_points = {f"{cue.name.lower()}_{cue.time}": cue.time for cue in self.song.cue_points}
        if self.updated_cue_points != self.initial_cue_points:
            # find the elements that were only in one set but not the other
            renamed_cues = set(self.updated_cue_points.keys()) ^ set(self.initial_cue_points.keys())
            print("renamed_cues: ", renamed_cues)
        if self.start_cue_name in renamed_cues or self.end_cue_name in renamed_cues or self.prev_start_cue_name in renamed_cues or self.prev_end_cue_name in renamed_cues:
            self.schedule_message(0, partial(self.create_clip_from_cues, True))
        self.initial_cue_points = self.updated_cue_points
